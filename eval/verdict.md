# Eval verdict (M2) — TEMPLATE, fill after running

> Subject: KX's `q-knowledge@kx-skills` vs. baseline (no plugin). Model + settings: _record here._
> Date run: _TBD._ Harness commit: _TBD._ Do NOT claim blind scoring (impossible in principle;
> the published-source checklist is the defense — see PROTOCOL.md).

## Part A — trigger precision
- Should-fire true positives: __/10 (eval/triggers/should-fire.md)
- Should-not-fire true negatives: __/10 (eval/triggers/should-not-fire.md)
- Notes: _which prompts mis-fired / missed, and why._

## Part B — output quality (n = 15 q tasks, paired A vs B)
- Combined per-task score = correctness (0/1) + idiom_total (0-5). A task is a **win** for the
  condition with the higher combined score; ties are non-discordant and excluded.
- Discordant pairs (conditions differ): __
- Wins B: __  ·  Wins A: __
- **Decision rule (PROTOCOL.md):** effect is real only if one side wins **≥~80% of discordant
  pairs** (≈ ≥4 more wins than losses). The old "<15%" threshold is CUT.

## Verdict — pick one exit
- [ ] **No lift** → publish the negative result (Article 3); ship curriculum-only, author no skill.
- [ ] **Lift, but KX's plugin already delivers it** → publish the comparison; author nothing.
- [ ] **Lift AND a gap KX's plugin does not fill** (likely learner-facing) → author a skill scoped
      to that gap (q-only), fold observed failure modes back in, re-run a 5-task spot check.

## Evidence / reasoning
_Summarize per-task wins/losses, notable failure modes, token + repair deltas. Link results.csv._
