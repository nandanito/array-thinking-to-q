# eval/runs/ — the M2 run's raw material

An article claiming a result should ship what the result was computed from. This directory is that.

- `NN-name.A.q` — condition A (baseline, no plugin) answer.
- `NN-name.B.q` — condition B (KX `q-knowledge` plugin) answer.
- `notes.md` — the two scoring rules fixed before the pass, and the per-task rationale.
- `traces.md` — every session's tool calls in order, plus output tokens. This is the activation
  evidence: "fired" means a `Skill` tool call naming a `q-knowledge` skill actually happened.

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
python3 ../harness/mkprompts.py ../tasks/q ./prompts
../harness/session.sh A out/01-sum-squares.A ./prompts/01-sum-squares.txt
../harness/session.sh B out/01-sum-squares.B ./prompts/01-sum-squares.txt
```

`session.sh` runs each session from `$NEUTRAL` (default `$TMPDIR/atq-eval-neutral`) — outside this
repository, so condition A cannot inherit `.claude/skills/idiomatic-q/`. That control is the whole
ballgame; see PLAN-M2.md §1.

Sampling is not deterministic, so a re-run will not reproduce these answers token-for-token. It
should reproduce the *shape* of the finding: both conditions at the correctness ceiling, near-zero
discordant pairs, and condition B costing several times the output tokens.
