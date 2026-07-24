# CLAUDE.md — array-thinking-to-q

Teaching repo: array thinking via a short J laboratory, then q as the main event.
Read SPEC.md first. It is the contract; this file is operational guidance.

## Objective hierarchy (settles conflicts — higher wins)

1. Learning (author writes real q; learns skill evaluation) 2. Curriculum (verified lessons)
3. Skill + marketplace 4. Blog. Marketplace discoverability NEVER reshapes pedagogy.

## Non-negotiable rules

1. **Q-first authoring.** Never write or extend a J prelude before its q side runs.
2. **J is illustrative, not installable.** Part I is 1–2 read-along lessons with captured outputs;
   readers need no J toolchain. J examples DO stay executable in author-side CI (jconsole is
   license-free — the only green check that never depends on KX). J is cut from skill scope.
3. **Everything executes.** No code block lands in a lesson unless `make verify` runs it.
   J via `jconsole`; q via KDB-X CE. If q isn't licensed/installed yet, the lesson stays in
   `drafts/` and out of `lessons/`.
4. **No commercial-friendliness claims about KDB-X CE** anywhere until TASK ZERO (below) is done.
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
4. Part I (J laboratory) compression pass + transition chapter.
5. CI: `j-verify.yml` (blocking, on PR) and `q-verify.yml` (nightly + manual, trusted branches
   only, license key from repo secret; failures notify, never block).
6. README: thesis, why-J-not-BQN, prior art, disclaimers, quickstart.

## Environment notes

- Plain Makefile drives everything: `make verify-j`, `make verify-q`, `make verify`.
- Pin and document exact J and KDB-X versions in `docs/toolchain.md`.
- q golden files live next to the showcase only: `showcase/aj/expected.txt`.
- Session state or scratch must never leak into lessons; use `drafts/`.

## Blog series duty (per milestone)

Each milestone M1–M5 produces a blog article draft in `writings/` (see SPEC.md). An article is
publishable ONLY when its milestone's artifacts verify. Article #3 must report the real eval
result, positive or negative. Article #4 is the at-risk one (least novelty for the author) —
draft it during M1. Article #6 is PACKAGING of docs/COMPOUND.md, so append to COMPOUND.md at
every milestone. Publishing/syndication steps live in RELEASE-CHECKLIST.md, not here and not in
SPEC.md. The skill targets the Claude Skills marketplace: its README cites the eval verdict as
evidence, and marketplace metadata is part of M5, not an afterthought.

## Compound step (mandatory at each milestone)

Append lessons-learned to `docs/COMPOUND.md`: what the eval showed (positive OR negative),
licensing findings, model failure modes discovered while writing the skill, and anything
transferable to other projects (skill-authoring patterns especially).
