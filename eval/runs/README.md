# eval/runs/ — the M2 run's raw material

An article claiming a result should ship what the result was computed from. This directory is that.

- `NN-name.A.q` — condition A (baseline, no plugin) answer.
- `NN-name.B.q` — condition B (KX `q-knowledge` plugin) answer.
- `notes.md` — the two scoring rules fixed before the pass, and the per-task rationale.
- `prompts/A/*.txt`, `prompts/B/*.txt` — the exact bytes fed to `claude -p` for all 50 sessions.
- `logs/partA/*.jsonl`, `logs/partB/*.jsonl` — the **raw stream-json session logs**, all 50.
- `traces.md` — every session's tool calls in order, plus output tokens. **Derived** from `logs/`
  by `../harness/mktraces.py`, not hand-written; `make verify-eval-run` re-derives it and fails on
  any drift. "Fired" means a `Skill` tool call naming a `q-knowledge` skill actually happened.

### What the logs prove, and what was removed from them

Each log opens with a `system/init` line recording that session's `model`, `tools`,
`permissionMode`, and — the load-bearing one — its `plugins` and `skills`. **This is the
contamination control, per session, machine-checkable:** condition A logs carry `"plugins": []`
with no q skill in the list; condition B logs carry exactly `q-knowledge` `0.1.0` plus
`q-knowledge:q` and `q-knowledge:qlint-snippet`. The `memory_paths.auto` directory those lines name
was **empty**, so no session loaded any stored memory — an unexamined contamination vector until
the redaction pass surfaced the path.

`../harness/redact.py` made exactly two changes for publication, and they are the only two:
`rate_limit_event` lines were dropped (they carry the *author's account* quota, not eval data), and
machine-specific absolute paths were rewritten to `$NEUTRAL` / `$KX` / `$HOME`. Everything else is
byte-for-byte session output.

**The `.q` files are the model's replies verbatim.** All 30 answers obeyed the output contract
exactly — one fenced q block, no prose — so stripping the fences loses nothing. (Checked, not
assumed.) The contract itself is quoted in [`../verdict.md`](../verdict.md).

## Reproducing the scores

```sh
Q=$HOME/.kx/bin/q ../harness/correctness.sh
```

recomputes the `correctness` column of `../results.csv` from these files, using the same rule as
`make verify-eval`: q must exit 0 **and** write nothing to stderr **and** match the golden. Expect
`correctness = 0 on 2 of 30` — task 15 under both conditions, which appended `show meta quote` to
an otherwise exactly-correct join.

## Re-running the generation

Needs the plugin checked out at the pinned SHA in `../verdict.md`:

```sh
git clone https://github.com/KxSystems/kx-skills && git -C kx-skills checkout 8b7040f
export KX="$PWD/kx-skills/plugins/q-knowledge"
mkdir -p out                       # session.sh redirects into it; it will not create it
python3 ../harness/mkprompts.py ../tasks/q ./prompts
../harness/session.sh A out/01-sum-squares.A ./prompts/01-sum-squares.txt
../harness/session.sh B out/01-sum-squares.B ./prompts/01-sum-squares.txt
```

`mkprompts.py` regenerates exactly the bytes in [`prompts/B/`](prompts/B/) from the task sheets —
`diff -r` them if you want to check that the committed prompts are the ones the sheets describe.

`session.sh` runs each session from `$NEUTRAL` (default `$TMPDIR/atq-eval-neutral`) — outside this
repository, so condition A cannot inherit `.claude/skills/idiomatic-q/`. That control is the whole
ballgame; see PLAN-M2.md §1.

Sampling is not deterministic, so a re-run will not reproduce these answers token-for-token. It
should reproduce the *shape* of the finding: both conditions at the correctness ceiling, near-zero
discordant pairs, and condition B costing several times the output tokens.
