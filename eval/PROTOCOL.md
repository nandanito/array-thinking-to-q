# Eval protocol (M2 gate) — subject: KX's official q plugin vs. baseline

Claim under test: KX's official q plugin (`q-knowledge@kx-skills`) measurably improves
frontier-model q output over baseline. A self-authored skill is tested ONLY if this eval exposes a
gap KX's plugin does not fill — and then it is scoped to that gap (learner-facing, q-only; see
SPEC.md objective 3). This is a research claim; it gets tested BEFORE mass content production.

## Part A — Trigger precision (activation)

A skill that never fires is worth zero regardless of content quality. Measure this FIRST, on the
subject under test (KX's `q-knowledge` plugin).

- 10 prompts where it SHOULD fire (write q, fix J, translate to kdb+, qSQL query...).
- 10 adjacent traps where it should NOT (NumPy vectorization, plain SQL, APL/BQN, "write a
  query" with no q context, generic "make this faster").
- Record fire / no-fire for each. For KX's plugin we only MEASURE (we don't control its triggers).
- If a learner-gap skill IS authored, tune ITS `description`/trigger wording — NOT by expanding
  the body — then **re-test on FRESH prompts**: iterating on the same 20 overfits the trigger to
  the test set (SPEC.md). The fresh-prompt numbers, not the tuning-set numbers, are what publish.
- Publish these numbers in the skill README at M5; they are the marketplace quality evidence.

## Part B — Output quality (post-activation)

- **Tasks:** ~15 per condition, **q-only** (J is cut from skill scope — SPEC.md obj. 3; there is
  no J skill or KX J plugin to compare). Three types: (a) translate a short Python snippet,
  (b) write from an English spec, (c) fix a deliberately unidiomatic solution.
  Include at least 3 tasks touching tables/qSQL and 2 touching `aj`.
- **Conditions:** identical prompts, same model+settings; **A = baseline (no plugin), B = KX
  `q-knowledge` plugin enabled.** (If a learner-gap skill is later authored, evaluate it as an
  ADDITIONAL condition on the same tasks — never in place of the KX-vs-baseline comparison.)
- **No blind scoring — and say so.** Idiomatic output identifies its own condition; blinding is
  impossible in principle here. The defense against evaluator drift is the published-source
  checklist below (every item justifiable against Q for Mortals / code.kx.com), NOT a blinding claim.
- **Scores per task:** correctness (runs + right output, via `make verify` harness, 0/1),
  and idiomaticity as a BINARY CHECKLIST (not a 1–5 feel score — a numeric feel score drifts as
  the author's own q taste improves between week 2 and week 8 while the benchmark stays fixed):
    [ ] no explicit loop where a vector op exists
    [ ] uses qSQL where a table operation is expected
    [ ] uses built-ins over hand-rolled iteration
    [ ] no unnecessary temporaries
    [ ] matches a CITED published idiom (Q for Mortals / code.kx.com)
  Each checklist item must be justifiable against a published source, not the author's taste —
  this also defuses the confound of a Claude-family model being scored on a Claude-authored skill.
  Also record token count + repair iterations to first running solution.

## Decision rule

- **Paired sign test on discordant pairs** (the old "<15% improvement" threshold is CUT — at n≈15
  binary outcomes the sampling noise is the size of the effect, so that rule could not adjudicate
  itself). Count only tasks where the two conditions differ; the effect counts as real only if one
  side wins **≥~80% of discordant pairs** (roughly: ≥4 more task-wins than losses). This detects
  only large effects — appropriate for a language models are measurably bad at.
- **Two exits, both real findings:** (1) no lift → publish the negative result (docs/COMPOUND.md
  and Article 3), ship curriculum-only. (2) lift exists but KX's plugin already delivers it →
  publish the comparison, author nothing. A self-authored skill ships ONLY if the eval exposes a
  gap KX's plugin does not fill — scoped to that gap; then fold observed failure modes back in and
  re-run a 5-task spot check.

## Files

- triggers/should-fire.md, triggers/should-not-fire.md — Part A prompts + observed results
- tasks/q/NN-name.md — task + reference solution + verify snippet (q-only; see Part B)
- results.csv — task, condition, correctness, idiomaticity, tokens, repairs
- verdict.md — the go/no-go call and reasoning
