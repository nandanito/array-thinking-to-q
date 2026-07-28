# CLAUDE.md — array-thinking-to-q

Teaching repo: array thinking via a short J laboratory, then q as the main event.
Read SPEC.md first. It is the contract; this file is operational guidance.

## Objective hierarchy (settles conflicts — higher wins)

1. Learning (author writes real q; learns skill evaluation) 2. Curriculum (verified lessons)
3. Skill EVALUATION (discharged at M2 by publishing the eval; it authored no skill, so there is
   no marketplace track) 4. Blog. Marketplace discoverability NEVER reshapes pedagogy.

## Non-negotiable rules

1. **Q-first authoring.** Never write or extend a J prelude before its q side runs.
2. **J is illustrative, not installable.** Part I is 1–2 read-along lessons with captured outputs;
   readers need no J toolchain. J examples DO stay executable in author-side CI (jconsole is
   license-free — the only green check that never depends on KX). J is cut from skill scope.
3. **Everything executes.** A q or J example does not land in a lesson unless `make verify` runs
   it. J via `jconsole`; q via KDB-X CE. Exactly two blocks are exempt, both marked in place: an
   illustrative Python snippet, and one q expression that fails to parse on purpose (it cannot
   live in a verify-clean file, so it is quoted as a real REPL transcript). A lesson whose q side
   does not yet run stays **on its feature branch** until `make verify` is green — never
   half-verified on `main`. There is no `drafts/`; git branches already do this job.
4. **No commercial-friendliness claims about KDB-X CE**, ever. TASK ZERO is DONE and settled this:
   the license grants personal / internal-business use ONLY and restricts benchmark publication
   (Clause 9). This is not a hold pending research — it is the finding. See docs/licensing-notes.md.
5. **Narrative is the product.** Each lesson explains WHY the idiom is shaped that way and what
   the imperative instinct gets wrong. Two code blocks + a sentence = cut or merge.
6. Names "q", "kdb+", "KDB-X", "J" are third-party marks used nominatively. Keep the
   non-affiliation disclaimer in README intact.

## Task zero (before anything else)

Three reads in one sitting, into `docs/licensing-notes.md` (quote sparingly, summarize):
(1) the ACTUAL license text bundled with the downloaded build; (2) any BENCHMARK-PUBLICATION
clause (article 5 touches performance); (3) KX's official Claude Code plugins for q/PyKX/KDB-X/
KDB.AI and the KDB-X MCP server — what they cover and what they don't. Record the exact version
as the pinned known-good release. Note WSL-only on Windows. Then the week-1 gate: `showcase/aj/`
runs end-to-end, and the eval verify-harness exists.

## Build order

1. Task zero + `aj` end-to-end gate.
2. Eval (`eval/PROTOCOL.md`) — subject is **KX's official q plugin vs. baseline**, not a
   self-authored skill (KX shipped first; see SPEC.md objective 3). Both parts: (A) trigger
   precision, fresh prompts on re-test; (B) output quality, paired, binary checklist, PAIRED SIGN
   TEST on discordant pairs (the old 15% threshold is cut — unadjudicable at n=15). Do NOT claim
   blind scoring. Author a skill only if a gap appears, scoped to it, q-only.
3. Part II (q) lessons, one at a time: q code → verify → narrative → J twin (short) → verify.
   Remaining: attributes & sort discipline (`s#`/`g#`/`p#`) — REQUIRED before the showcase — then
   the `aj` showcase lesson. (This is SPEC's **M3**; SPEC's milestones were swapped 2026-07-28 to
   match this order, which the Q-first rule requires.)
4. Part I (J laboratory) compression pass + transition chapter. (SPEC's **M4**.)
5. CI: `j-verify.yml` (blocking, on PR) and `q-verify.yml` (nightly + manual, trusted branches
   only, license key from repo secret; failures notify, never block). **`q-verify.yml` does not
   exist yet** — so `verify-q`, `verify-eval` and `verify-eval-run` run on the author's machine
   only, and nothing in CI protects the published eval numbers. It must run `make verify`, not
   just `verify-q`, or the eval-run checks stay unenforced.
6. README: thesis, why-J-not-BQN, prior art, disclaimers, quickstart.

## Environment notes

- Plain Makefile drives everything: `make verify-j`, `make verify-q`, `make verify`.
- Pin and document exact J and KDB-X versions in `docs/toolchain.md`.
- q golden files live next to the showcase only: `showcase/aj/expected.txt`.
- Session state or scratch must never leak into the repo at all — use a temp dir OUTSIDE it, so a
  stray `git add` cannot pick it up. Nothing in the working tree is a scratchpad.

## Blog series duty (per milestone)

Each milestone M1–M5 produces a blog article draft in `writings/` (see SPEC.md). An article is
publishable ONLY when its milestone's artifacts verify. Article #3 reported the real eval result
(it was negative — DONE, 2026-07-27). Article #5 "Unlearn the loop" is the low-novelty one whose
"draft it early" mitigation was missed; it gets drafted out of milestone order to close that.
Article #6 is PACKAGING of docs/COMPOUND.md, so append to COMPOUND.md at every milestone.
Publishing/syndication steps live in RELEASE-CHECKLIST.md, not here and not in SPEC.md.

**There is no skill and no marketplace submission.** The M2 eval authored none — objective 3's
gate held — so M5 ships the curriculum plus `eval/harness/` packaged as a reusable
plugin-A/B artifact. Do not reintroduce a skill deliverable without a NEW eval showing a gap.

## Compound step (mandatory at each milestone)

Append lessons-learned to `docs/COMPOUND.md`: what the eval showed (positive OR negative),
licensing findings, model failure modes discovered while writing the skill, and anything
transferable to other projects (skill-authoring patterns especially).

**Then re-read SPEC.md and this file against reality and fix what has gone stale.** The recurring
defect in this repo is not wrong code — it is documents that were true when written and silently
became false, with nothing failing. Lessons have `make verify`; governing docs have only this step.
