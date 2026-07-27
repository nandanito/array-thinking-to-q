# M2 eval — execution plan

> **EXECUTED 2026-07-26/27.** All pre-flight gates passed; both parts ran as planned. The result
> and everything that was decided at run time live in [`verdict.md`](verdict.md) — read that for
> what happened, this for what was intended. Two of §4's degenerate cases fired at once (ceiling,
> and too few discordant pairs), which is what §4 existed to catch. The `eval/README.md` wording
> flagged in §2 is fixed.

Three documents, three jobs. [`PROTOCOL.md`](PROTOCOL.md) is the **design** and the decision rule.
[`README.md`](README.md) is **how to score one task**. This file is the **order of operations**: the
decisions that must be made before the first prompt, the controls that make the comparison mean
anything, and the branches to take when a result is degenerate.

Subject under test: KX's `q-knowledge@kx-skills` plugin vs. baseline. Nothing here changes the
protocol; if the two disagree, PROTOCOL.md wins.

---

## 0. Pre-flight (all blocking)

- [ ] `make verify-eval Q=…` green — the instrument self-tests before it scores anything.
- [ ] Plugin installed at the **pinned SHA `8b7040f769c6653db67b063aa34c944729e8857e`**
      (`/plugin marketplace add KxSystems/kx-skills`, `/plugin install q-knowledge@kx-skills`).
      There is no version tag; the SHA is the pin. Record it in `verdict.md`.
- [ ] **Model + settings recorded verbatim** in `verdict.md` before starting, not reconstructed
      after. One model for the whole run — a mid-run model change invalidates the pairing.
- [ ] Neutral run directory confirmed (§1). This is the one that is easy to skip and fatal.
- [ ] Condition order decided and written down (§3).

## 1. The control that matters most: run OUTSIDE this repo

**This repository contains a q skill.** `.claude/skills/idiomatic-q/SKILL.md` carries anti-loop
rules, "prefer qSQL over row-wise thinking", and the `aj` sort-discipline gotchas. `CLAUDE.md` adds
more q guidance, and `lessons/` is full of verified idiomatic q.

If the eval is run with Claude Code from inside this working copy, **condition A is not a baseline.**
It silently inherits a q idiom skill — approximately the thing under test — so both conditions are
contaminated and the comparison measures nothing. This is the single failure mode most likely to
waste the entire run, and it leaves no trace in the results.

Controls:

- **Run every session from a scratch directory outside this repo**, with no project `CLAUDE.md` and
  no `.claude/skills/`. Verify by asking the model what skills/instructions it has loaded before
  the first task.
- Checked 2026-07-26: there is **no user-level `~/.claude/CLAUDE.md`** on this machine, so that
  confound is currently absent. **Re-check at run time** — it may have been added since.
- Task prompts are the verbatim **Prompt** blocks in `tasks/q/NN-name.md`. Paste nothing else: no
  lesson text, no reference solution, no golden output.
- `*.ref.q` and `*.expected` are scoring material. Keep them out of the model's context entirely.

## 2. Part A — trigger precision (first)

**Resolve a doc inconsistency before running.** PROTOCOL.md measures activation *on the subject*;
`eval/README.md` says to run each prompt "under each condition". Condition A has no plugin, so
there is nothing to activate and "fire/no-fire" is undefined for it. **Part A is condition B only:
20 prompts × 1 condition.** Fix the `eval/README.md` wording as part of the run.

- One **fresh session per prompt** — 20 sessions. A prior q conversation primes activation and
  turns a trigger test into a memory test.
- Record fire / no-fire plus what you actually observed (the skill announcing itself, q-specific
  framing appearing unprompted, etc.) in the `triggers/` tables. "It felt like it fired" is not data.
- 10 should-fire, 10 adjacent traps. Precision *and* recall both matter: a plugin that fires on
  every trap is as broken as one that never fires.

**Branch — plugin fires 0/10 on should-fire prompts.** That is the headline finding, not a dead
end. Still run Part B with the plugin force-loaded, because "never activates" and "doesn't help
once active" are different findings with different implications — only the first is a wording bug
KX could fix tomorrow, and the article should say which one it is.

## 3. Part B — output quality

15 tasks × 2 conditions = **30 runs**, one fresh session each.

**Separate generation from scoring — this is the discipline that protects the result.** Collect all
30 outputs first, saving each verbatim; score afterwards in a single pass, task by task with both
conditions in view. Scoring an answer immediately after generating it means the second condition is
read in the light of the first, and the checklist stops being independent.

- Suggested layout: `eval/runs/NN-name.A.q` / `.B.q` for the code, plus a short `.md` note per run
  for tokens and repairs. **Commit them** — an article claiming a result should ship the raw
  material behind it.
- Fix the presentation order and write it down (e.g. all of A first, then all of B, tasks in
  numeric order). Any fixed order is defensible; an undocumented ad-hoc order is not.
- **Correctness is decided by the harness snippet in `README.md`, not by eye.** q can exit 0 after
  a script error, so the empty-stderr check is what actually catches a failed run.
- Idiomaticity: the 5 binary items, each justified against a published source and cited per task.
  Record tokens and repair iterations to first running solution.

## 4. Decision, and the degenerate cases

Primary rule is PROTOCOL.md's paired sign test on discordant pairs: real only if one side wins
≥~80% of them (≈ ≥4 more task-wins than losses).

Watch for results the rule cannot interpret, and report them as instrument limitations rather than
as findings:

- **Ceiling:** correctness 15/15 in both conditions → the tasks cannot discriminate. Report the
  ceiling; do not report "no difference between conditions".
- **Floor:** near-0 in both → same problem, other end.
- **Too few discordant pairs** (say <5) → the sign test has nothing to work with. Report the
  count and say the eval was underpowered, which is itself worth publishing.

## 5. Threats to validity — state these in Article 3, do not bury them

- **No blinding, and it is impossible in principle** — idiomatic output identifies its own
  condition. The published-source checklist is the defense. Never claim blind scoring.
- **n=15 detects only large effects.** That is a deliberate choice, not an oversight.
- **A Claude-family model is being scored partly on Claude-authored material.** The
  cite-a-published-source requirement on every checklist item is what defuses this.
- **Single scorer**, who is also the curriculum's author. The binary checklist exists precisely
  because a 1–5 "feel" score would drift as that author's q taste improves.
- **Task selection bias:** the 15 tasks were written by the same person who wrote the lessons, so
  they may favour the idioms this curriculum happens to teach. Say so.

## 6. Rough budget

| Stage | Estimate |
|---|---|
| Pre-flight + neutral env setup | 30 min |
| Part A — 20 fresh sessions | 1–1.5 h |
| Part B — 30 runs, generation only | 2–3 h |
| Scoring pass (separate sitting) | 1.5–2 h |
| `verdict.md` + COMPOUND entry | 1 h |

A focused day, or two half-days. The scoring pass genuinely wants to be a **separate sitting** from
generation — see §3.

## 7. What ships when it is done

- `verdict.md` filled in, with the model/settings/SHA header completed.
- `results.csv` — 30 rows. `triggers/*.md` — tables filled.
- `docs/COMPOUND.md` entry, **positive or negative** (CLAUDE.md makes this mandatory, and a
  negative result is the more interesting article).
- Article 3 draft in `writings/` — the flagship. It reports the real result either way.
- **Only if a gap survives:** author `idiomatic-q` scoped to that gap (q-only, learner-facing),
  fold the observed failure modes in, then re-run a 5-task spot check **and** re-test triggers on
  **fresh** prompts — reusing the original 20 overfits the trigger to the test set.
