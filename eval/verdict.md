# Eval verdict (M2) — KX's `q-knowledge` plugin vs. baseline

> **Subject:** KX's `q-knowledge@kx-skills`, pinned at commit
> **`8b7040f769c6653db67b063aa34c944729e8857e`** ("add missing parentheses (#12)"), plugin version
> `0.1.0`. There is no version tag upstream; the SHA is the pin.
> **Condition A** = baseline, no plugin. **Condition B** = that plugin loaded via `--plugin-dir`.
>
> **Model:** `claude-opus-5` (resolved from `--model opus`), first-party, context window 1,000,000,
> max output 64,000, service tier `standard`. One model for the whole run.
>
> **Settings, verbatim, as passed to every one of the 50 sessions:**
> ```
> --model opus --setting-sources "" --tools Skill,Read,Glob --allowedTools Skill Read Glob
> --output-format stream-json --verbose --no-session-persistence
> ```
> Condition B appends exactly one further flag: `--plugin-dir <…>/kx-skills/plugins/q-knowledge`.
> Nothing else differs between the arms. `--setting-sources ""` drops the author's
> `~/.claude/settings.json` (which sets `effortLevel: xhigh` and enables two unrelated plugins), so
> the run does not inherit the author's personal configuration; effort is therefore the CLI default,
> not `xhigh`.
>
> **Client:** Claude Code `2.1.220`. **q:** KDB-X CE, `~/.kx/bin/q` (see docs/toolchain.md).
> **Date run:** 2026-07-26 / 2026-07-27. **Harness commit:** this branch (`eval/m2-run`).
>
> **No blind scoring is claimed.** It is impossible in principle here — idiomatic output identifies
> its own condition. The published-source checklist is the defense (PROTOCOL.md).

## Contamination control — what was actually done

Every subject session ran with cwd set to an **empty scratch directory outside this repository**
(not a git repo, no `CLAUDE.md`, no `.claude/`). Verified at run time by asking a session to
enumerate what it had loaded:

- **Condition A** reported 41 skills, none q-related, and "Project instructions (CLAUDE.md): none
  loaded". Critically, `idiomatic-q` — this repo's own q skill — was absent.
- **Condition B** reported exactly two additional skills: `q-knowledge:q` and
  `q-knowledge:qlint-snippet`.
- Re-checked at run time per PLAN-M2 §1: there is still **no user-level `~/.claude/CLAUDE.md`**,
  and `~/.claude/skills/` holds only Cloudflare-related skills. Neither arm saw q guidance from
  the environment.

Had the eval been run from inside the working copy, condition A would have silently inherited
`.claude/skills/idiomatic-q/SKILL.md` — anti-loop rules, prefer-qSQL, the `aj` sort gotchas —
i.e. approximately the thing under test, leaving no trace in the results.

## How the sessions were driven

Headless `claude -p`, one fresh session per data point, 50 in total, scripted in
[`harness/session.sh`](harness/session.sh). This was settled *before* generating anything: the
alternative was 50 sessions by hand, which is neither reproducible nor honest about ordering.
Activation is decided **mechanically** — a session "fired" iff it emitted a `Skill` tool call
naming a `q-knowledge` skill — never by whether the prose felt q-flavoured. Traces:
[`runs/traces.md`](runs/traces.md).

Two harness decisions that shape the result and must be read with it:

- **`Read`/`Glob` are allowed in both arms** so that condition B can load the plugin's *own*
  bundled references (`skills/q/references/*.md`). An early smoke run showed those reads being
  permission-denied, which would have handicapped the plugin against its own design. Fixed before
  the run; zero permission denials in the 50 recorded sessions.
- **One fixed output contract is appended to every Part B prompt, identical in both arms:** *"Reply
  with exactly one q code block and nothing else: no prose before or after it, no alternatives, and
  no `q)` REPL prompts. The block must be a complete, self-contained q script that prints the
  required result to stdout using `show` when run as `q script.q -q`."* Without it, answers arrive
  as prose plus several alternative snippets carrying `q)` prompts, and "which block is the answer"
  becomes a scorer's judgment call 30 times over. It names no idiom under test. All 30 answers
  obeyed it exactly — one block, zero prose — so `runs/*.q` are the replies verbatim.

## Part A — trigger precision (condition B only, 20 fresh sessions)

- Should-fire true positives: **8/10** ([triggers/should-fire.md](triggers/should-fire.md))
- Should-not-fire true negatives: **9/10** ([triggers/should-not-fire.md](triggers/should-not-fire.md))

**The plugin activates reliably.** Both should-fire misses (#3, #7) are instrument artifacts, not
trigger failures: those two prompts say "fix this q code" / "convert this list comprehension" while
the table supplies no code, so the model globbed an empty directory and asked for the input instead
of doing q work. On the 8 prompts that actually presented a q task, activation was **8/8**. Both
numbers publish; 8/10 is what the pre-registered instrument measured, 8/8 is what it measured about
the plugin.

The single false positive is "Write a query to fetch users by email" — answered entirely in q,
schema and all. Note the traps built to bait a keyword match (`merge_asof`, "group" in JavaScript,
J's rank) all held; the mis-fire came from the *least* q-flavoured prompt in the set, in a session
stripped of all ambient context, where `q-knowledge` was the only domain skill on the bench.

**This matters for reading Part B:** the plugin cannot be dismissed as never firing. In Part B it
loaded in **14 of 15** condition-B runs. Whatever Part B shows, it shows about an *active* plugin.

## Part B — output quality (n = 15 q tasks, paired A vs B)

Generation and scoring were separate sittings, as required: all 30 outputs were collected and
saved verbatim first, then scored in a single pass with both conditions in view. Presentation
order was fixed and recorded in advance — **all of condition A in numeric task order, then all of
condition B in numeric task order.**

Combined per-task score = correctness (0/1) + `idiom_total` (0–5). A task is a **win** for the
condition with the higher combined score; ties are non-discordant and excluded.

- **Correctness: 14/15 in condition A, 14/15 in condition B.**
- **Idiomaticity: 73/75 in condition A, 74/75 in condition B** — A loses two checklist items
  (tasks 08 and 15), B loses one (task 15). The whole spread between the arms is that single item.
- **Discordant pairs (conditions differ): 1**
- **Wins B: 1 · Wins A: 0**
- **Decision rule (PROTOCOL.md):** effect is real only if one side wins ≥~80% of discordant pairs
  (≈ ≥4 more wins than losses). **The rule cannot be applied: 1 discordant pair is far below the
  ~5 minimum PLAN-M2 §4 sets for the sign test to mean anything.**

### The degenerate cases both fired at once

PLAN-M2 §4 names three results the decision rule cannot interpret. This run hit two of them, and
they must be reported as **instrument limitations, not findings**:

- **Ceiling.** Correctness was 14/15 in *both* arms, and 13 of the 15 task pairs were scored
  identically — 5 of them byte-for-byte identical q. These tasks cannot discriminate between the
  conditions because baseline `claude-opus-5` already solves them. "No difference between
  conditions" is **not** what this shows; what it shows is that the instrument has no headroom.
- **Too few discordant pairs.** One. The sign test has nothing to work with, and the eval is
  **underpowered on this task set** — which PLAN-M2 §4 anticipated is itself worth publishing.

And the single discordant pair is thin. Task 08 turns entirely on whether `t:update … from t; show
t` counts as an unnecessary binding against the reference's one-liner. Under the rule fixed before
scoring it does; under a reading of "add a column" as "mutate the table" it does not. A margin that
would flip on one scorer's reading of one line is not a margin.

### The one thing that did separate the conditions: cost

The tasks could not discriminate on quality. They discriminated cleanly on tokens.

| | condition A | condition B | ratio |
|---|---:|---:|---:|
| Total output tokens, 15 tasks | 3,671 | 10,337 | **2.8×** |
| Median per-task ratio | — | — | **3.9×** |
| Widest | 23 (task 14) | 407 | 17.7× |

For 13 of 15 tasks that bought identical or equivalently-scored code. The extreme is task 15, where
condition B spent 3,848 tokens — loading the skill, globbing, reading a bundled reference — to
arrive at the *same wrong attribute* as baseline's 978.

### The shared failure worth more than the comparison

On task 15 both conditions applied `` `p# `` to an **in-memory** quote table.
<https://code.kx.com/q/ref/aj/> gives memory → `` `g# ``, disk → `` `p# ``. Both arms picked the
disk attribute for a memory table; both returned correct rows anyway, so nothing errored.

**KX's own plugin, loaded and active, did not correct a deviation from KX's own published `aj`
guidance.** That is a specific, reproducible gap — and it is exactly the class of defect this
curriculum's `aj` showcase exists to teach, where the wrong answer runs clean.

### What `repairs` measures here

Nothing. The design is **single-shot**: the first answer is the answer, so `repairs` is 0 for all
30 rows by construction. A repair loop would have introduced a second uncontrolled variable (who
repairs, on what feedback) into a comparison that already struggles to resolve the first. Stated
here rather than left to be inferred from a column of zeros.

## Verdict — pick one exit

- [x] **No lift** → publish the negative result (Article 3); ship curriculum-only, author no skill.
- [ ] **Lift, but KX's plugin already delivers it** → publish the comparison; author nothing.
- [ ] **Lift AND a gap KX's plugin does not fill** → author a skill scoped to that gap.

**No measurable lift, and the honest qualifier is that this task set could not have measured a
small one.** KX's `q-knowledge` plugin activates reliably (14/15 in Part B, 8/8 on well-formed
Part A prompts) and produces good q. So does `claude-opus-5` without it, on these tasks, for a
third of the output tokens.

**No skill is authored.** PROTOCOL.md permits authoring only if the eval exposes a gap KX's plugin
does not fill. The `` `p#``/`` `g# `` finding is a real gap, but it is a **single observation from
one task in one run** — evidence to design a sharper test around, not a mandate to ship a skill.
Authoring one on this basis would be fitting a skill to n=1. The M5 decision stands open pending a
harder task set; see COMPOUND.

## Threats to validity — carried into Article 3, not buried

- **No blinding, impossible in principle.** Idiomatic output identifies its own condition. Never
  claimed otherwise; the cited-source checklist is the defense.
- **n=15 detects only large effects.** Deliberate, and this run did not even reach the point where
  that matters — 1 discordant pair means the test never engaged.
- **Ceiling effect is the headline limitation.** The tasks were written to be *verifiable*, which
  made them easy. A frontier model in 2026 solves "sum of squares" and "select sum qty by sym"
  without help from anyone. Any future re-run needs tasks where baseline is *known* to fail.
- **A Claude-family model scored partly on Claude-authored material.** The cite-a-published-source
  requirement on every checklist item is what defuses this; the one item that actually decided
  anything (task 15) was decided against *both* arms by KX's own documentation.
- **Single scorer, who is also the curriculum's author.** The binary checklist and the two
  pre-fixed scoring rules in `runs/notes.md` exist precisely to bound this. The task-08 caveat is
  recorded rather than resolved.
- **Task selection bias.** The 15 tasks were written by the person who wrote the lessons, so they
  favour the idioms this curriculum teaches — which, if anything, should have *helped* the
  condition that had a q skill loaded.
- **The harness strips ambient context**, so both arms are further from practice than a real
  session. This makes the Part A traps harder than reality and removes the repository signal a
  working session would carry.
- **`qlint-snippet` was never exercised.** The plugin's second skill shells out to KX qlint via
  `QLINT_DIR`, which is not installed on this machine, and the tool policy would not have permitted
  the Bash call anyway. Condition B's self-validation path is therefore untested here — a genuine
  capability of the plugin that this eval does not measure.

## Evidence

- [`results.csv`](results.csv) — 30 rows.
- [`runs/`](runs/) — all 30 answers verbatim, per-task scoring rationale, tool traces.
- [`harness/`](harness/) — the scripts, re-runnable; `correctness.sh` reproduces the correctness
  column from the committed answers.
- [`triggers/`](triggers/) — Part A tables.
