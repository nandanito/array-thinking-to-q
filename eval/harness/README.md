# eval/harness: A/B test a Claude Code plugin against no plugin

These scripts ran this repo's M2 eval of KX's q plugin (`../verdict.md`), and they are packaged
here so you can point them at any other plugin. The design question they answer is narrow: with
everything else held equal, does loading this plugin change what the model produces? Condition A
is a headless `claude -p` session with no plugin; condition B is the same session plus one
`--plugin-dir` flag. Everything the harness does is in service of making that one flag the only
difference, and of making every published number fall out of committed files.

It needs `bash`, `python3` (standard library only) and the `claude` CLI, plus whatever runs your
task set's answers (q for M2, Python for the example in `examples/document-skills/`). It does not
need this repository: copy the directory, or check it out, and run it from anywhere.

## The three ideas

### 1. A neutral cwd per session (contamination control)

Claude Code reads a lot from where it starts: `CLAUDE.md` files, `.claude/skills/`, project
settings, and an auto-memory directory derived from the cwd. Run an eval from inside a working
copy and the baseline quietly inherits that project's guidance. In M2 that would have handed
condition A this repo's own q skill, which is roughly the thing under test.

`session.sh` therefore starts every session in a directory made by `mktemp -d` for that session
alone, outside any repository, writes what the directory and its would-be auto-memory held into
`<name>.pre` before the model starts, and deletes the directory afterwards. It refuses to run if
that memory directory is not empty, or if any parent of the directory holds a `CLAUDE.md` or a
`.claude/` (Claude Code reads parents' `CLAUDE.md` too, and `system/init` does not record it; if
your `TMPDIR` sits inside a project, point it elsewhere). `--setting-sources ""` drops user and project settings;
account connectors are switched off (see gap b); the tool policy is identical in both conditions.
Afterwards, `audit.py` checks from each session's own `system/init` line that this held: see
"The gate" below.

### 2. Activation is read off the log, never judged

A plugin whose skill never loads is worth nothing, and an answer can look plugin-shaped with no
plugin involved. So a session **fired** if and only if its log contains a `Skill` tool call
naming one of the plugin's skills (`<plugin>:<skill>`). `extract.py --field fired` reads that for
one log; `mktraces.py` tabulates it for a run. Which plugin counts as "the plugin" is read from
the condition-B logs' `system/init` too, so nothing is configured by hand.

### 3. A scorer that checks its own published numbers

A number in an article is only as good as the memory of whoever typed it, unless something
breaks when it drifts. Each of these regenerates a published file from committed evidence and
exits nonzero on any difference, so `make` catches a stale or hand-edited figure:

- `correctness.sh` re-runs every committed answer against its task's golden output and compares
  the result with the `correctness` column of `results.csv`. An answer passes only if it exits 0,
  writes nothing to stderr (q exits 0 after a script error, so stderr is the real signal) and
  matches the golden byte for byte. Each answer runs in its own fresh directory, so one answer's
  leftover files cannot make another pass.
- `mktraces.py --check` regenerates the per-session table: tool calls in order, fired or not,
  output tokens.
- `aggregates.py --check` regenerates the totals built on that table: token totals and ratios,
  dollar cost, plugin load and invocation counts, run order, and the sensitivity row that drops
  any pair whose sessions saw tools beyond the common set.

What stays human: the idiomaticity checklist in `results.csv` (M2 scored it against published
sources, see `../PROTOCOL.md`), and the interpretation.

## The gate: `audit.py`

Run it on a finished run before scoring anything. It fails the run unless every session's
`system/init` shows: condition A loaded no plugin and condition B exactly the plugin under test;
the same tools, MCP servers, skills and agents in every session once the plugin's own entries
are set aside; the same model, Claude Code version, permission mode and output style; no
`claude.ai` account connector; a different cwd and auto-memory path for every session; and, with
`--order`, that the sessions ran in the order `schedule.py` recorded. A run that fails measured
something other than the plugin, and none of its numbers should be published.

## Known gaps from M2, and what changed

The M2 run and its 2026-09-28 content review found four weaknesses in the harness as it was then.
The committed M2 logs keep them (they are evidence and are not rewritten), and `audit.py` fails
those logs for exactly these reasons, which is how `selftest.py` proves the audit bites.

| | Gap in the M2 run | Fixed here by |
|---|---|---|
| (a) | `session.sh` reused one `mkdir -p` directory for all 50 sessions and never logged its contents | a fresh `mktemp -d` per session (and per retry), a `<name>.pre` listing of it and of its auto-memory path, and `audit.py` failing any shared cwd or memory path |
| (b) | an account connector (claude.ai Google Drive) put eight extra tools into 3 of 15 condition-B sessions; `--tools` did not stop it | `ENABLE_CLAUDEAI_MCP_SERVERS=false` and `--strict-mcp-config` on every session, and `audit.py` failing any connector or any difference in non-plugin tools, servers or skills |
| (c) | all 15 condition-A sessions ran before all 15 condition-B sessions, so drift during the run (the connector finishing its connection) landed on B only | `schedule.py`: shuffled tasks, each task's two conditions back to back in random order, the seed and order written to `order.tsv` before the first session, checked by `audit.py --order` |
| (d) | the verdict first rested partly on a model's account of its own context, and the scripts carried the M2 task set in their text (a hardcoded 30, the plugin's name) | every count, name and pair set is derived from the logs or the task directory; `correctness.sh INIT=1` writes a new study's `results.csv` from the scores rather than by hand |

On (d): M2's published numbers are unchanged. `make verify-eval-run` re-derives them with these
scripts from the same committed logs, byte for byte.

## Quickstart

```sh
H=/path/to/eval/harness                 # a checkout of this directory
export PLUGIN=/path/to/plugin           # pinned to a commit you will report
mkdir study && cd study

# 1. Task sheets: tasks/NN-name.md (a "## Prompt" blockquote), NN-name.expected (golden
#    stdout), and optionally tasks/CONTRACT.txt, appended to every prompt.
python3 $H/mkprompts.py tasks prompts

# 2. Generate: one session per task and condition, in a seeded interleaved order.
python3 $H/schedule.py --prompts prompts --out logs --seed 20260928

# 3. Gate: stop here if this fails.
python3 $H/audit.py logs --order logs/order.tsv

# 4. Answers: the first fenced block of each reply.
mkdir answers
for l in logs/*.jsonl; do python3 $H/extract.py "$l" --field code > "answers/$(basename "$l" .jsonl).py"; done

# 5. Score once to write results.csv, then check it on every later run.
INIT=1 TASKS=tasks ANSWERS=answers CSV=results.csv EXT=py RUN='python3 {}' $H/correctness.sh
TASKS=tasks ANSWERS=answers CSV=results.csv EXT=py RUN='python3 {}' $H/correctness.sh

# 6. Derived tables. Copy or move the logs under logs/partB/ first (mktraces reads partA/ too,
#    if you ran activation prompts with --conditions B).
python3 $H/mktraces.py runs/logs --title "my study" > runs/traces.md
python3 $H/aggregates.py runs/logs/partB > runs/aggregates.md

# 7. Before publishing logs: drop account quota lines and rewrite local paths.
python3 $H/redact.py logs public-logs
```

`MODEL` (default `opus`) and `TOOLS` (default `Skill,Read,Glob`, granted to both conditions)
are environment variables of `session.sh`. `Read` and `Glob` are there so a plugin can open its
own bundled reference files; widen `TOOLS` if your plugin needs more, but both conditions always
get the same list. If the plugin ships its own MCP server, set `STRICT_MCP=0`, since strict mode
would drop that server from condition B; the audit still fails any run whose sessions differ in
anything else.

## Files

| file | role |
|---|---|
| `session.sh` | one headless session, fresh neutral directory, connectors off |
| `schedule.py` | seeded interleaved run order, recorded before running |
| `audit.py` | the gate: identical non-treatment context, no connectors, fresh dirs, recorded order |
| `mkprompts.py` | task sheet to prompt file, plus the output contract |
| `extract.py` | one field from one log: answer, code, tools, fired, tokens, turns |
| `correctness.sh` | re-run answers against goldens; check or initialise `results.csv` |
| `mktraces.py`, `aggregates.py` | derived tables, with `--check` to fail on drift |
| `redact.py` | prepare logs for a public repo |
| `ok.py` | did a session end in a clean result (used by `session.sh` for retries) |
| `sessionlog.py` | the one log parser the Python scripts share |
| `selftest.py` | shows each gate failing as well as passing; `make verify-harness` |
| `examples/document-skills/` | the task set used to prove the harness outside this repo |

## Limits

Sampling is not deterministic, so a re-run reproduces the shape of a finding, not its tokens.
There is no blinding and no statistics beyond counts; M2's decision rule (a paired sign test on
discordant pairs) is in `../PROTOCOL.md`. The harness strips ambient context on purpose, so both
conditions sit further from a real working session than practice does. Activation detection
sees `Skill` calls only: a plugin that acts through hooks, agents or MCP tools alone needs a
different signal, and `extract.py --field tools` is where to start.

## Proof outside this repo

"Run it from a neutral directory" is the one claim that cannot be tested from inside this
repository, so it was tested from outside it: see "Clean-checkout run" below.
