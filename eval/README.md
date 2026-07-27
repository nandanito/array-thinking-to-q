# eval/ — the verify-harness (M2 gate)

Operational guide for running the eval. The *design* and decision rule live in `PROTOCOL.md`
(reconciled with SPEC.md); this file is how to actually run it. Subject under test: KX's
`q-knowledge@kx-skills` plugin vs. baseline (no plugin).

## Layout
- `triggers/should-fire.md`, `triggers/should-not-fire.md` — Part A prompts + fire/no-fire tables.
- `tasks/q/NN-name.md` — Part B task sheet: the verbatim prompt, type, and the cited idiom for
  checklist item 5. The prompt is what you give the model; the rest is for scoring only.
- `tasks/q/NN-name.ref.q` — the idiomatic reference solution (runs, prints its result).
- `tasks/q/NN-name.expected` — golden output of the reference.
- `results.csv` — one row per (task, condition). `verdict.md` — the go/no-go writeup.
- `harness/` — the scripts that drove the M2 run: `session.sh` (one headless subject session,
  from a neutral cwd outside this repo), `mkprompts.py` (task sheet → prompt file),
  `extract.py` / `ok.py` (read a session log), `correctness.sh` (score every committed answer).
- `runs/` — the M2 run's raw material: all 30 answers verbatim, scoring rationale, tool traces.

## Part A — trigger precision (do this FIRST)
Run each prompt in a fresh context **under condition B only** — 20 prompts × 1 condition. Condition
A has no plugin, so "fire / no-fire" is undefined for it; activation is a property of the subject
under test, not a comparison (PROTOCOL.md, PLAN-M2.md §2). Record fire / no-fire in the tables.
A skill that never fires is worth zero, so measure activation before quality.

Decide firing **mechanically**: the session emitted a `Skill` tool call naming a `q-knowledge`
skill. "It felt like it fired" is not data — an answer can be q-flavoured with no skill loaded.
`harness/extract.py --field fired` reads this off a session log.

## Part B — output quality
For each of the 15 tasks, under condition A (baseline) and B (plugin), using identical prompts,
same model + settings:
1. Give the model the task's **Prompt** block.
2. **Correctness (0/1):** save the model's answer as `cand.q` that prints its result. "Runs +
   right output" means the q process must succeed (no error) AND stdout must match the golden — so
   capture stderr and never let `diff`'s exit status mask a q failure:
   ```sh
   q cand.q -q < /dev/null > cand.out 2> cand.err
   if [ $? -eq 0 ] && [ ! -s cand.err ] && diff -u tasks/q/NN-name.expected cand.out; then
     echo "correctness = 1"
   else
     echo "correctness = 0"; [ -s cand.err ] && cat cand.err
   fi
   ```
   Note: q can exit 0 even after a script error (it drops to a prompt, then EOF exits), so the
   empty-stderr check — not the exit code alone — is what actually catches a failed run. Pass `q`
   explicitly or via `make Q=…`; see docs/toolchain.md.
3. **Idiomaticity (5 binary items, PROTOCOL.md):** no explicit loop where a vector op exists;
   uses qSQL where a table op is expected; built-ins over hand-rolled iteration; no unnecessary
   temporaries; matches the task's cited published idiom. Record each 0/1 and their total.
4. Record output tokens + repair iterations to first running solution.
Append a row to `results.csv` for each (task, condition).

## Self-test (keeps the instrument honest)
`make verify-eval` runs every `*.ref.q` and diffs its golden — proving the reference solutions
still execute and are correct on the pinned KDB-X build before you trust the scoring. It is also
part of `make verify`.

## Decision
Paired sign test on discordant pairs (see `verdict.md` / `PROTOCOL.md`). Two exits, both real
findings: no lift → publish the negative; lift already covered by KX → publish the comparison.
A skill ships only if a gap survives, scoped to it.
