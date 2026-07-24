# array-thinking-to-q — Project Specification

> Status: reviewed seed (Claude self-review + 2 ChatGPT cross-reviews incorporated; Fable 5 pass pending) 2026-07-22
> Owner: Nandan (personal). Home: `nandanito/array-thinking-to-q`.
> (Deliberately NOT under qmilab — this is a personal learning-in-public project.)
> Renamed from `from-j-to-q` after the reframe made J ~25% of content: the old name gave equal
> billing to a means and a destination. (`q-by-way-of-j` was an intermediate candidate, rejected
> as needing too much parsing.) Final name states the paradigm and the destination; J is the how,
> explained in one README line. Discoverability is handled by README keywords + GitHub topics
> (kdb+, q, array-programming, apl), not by the repo name. Note: "array thinking" is adjacent to
> Jim Pivarski's "Thinking in Arrays" series — different word order, generic term of art, and the
> prior-art section credits him explicitly.

## Thesis

Learn array thinking in the **J laboratory**, then apply it where industry pays for it: **q/kdb+**.
J is a compact laboratory for the paradigm shift ("unlearn the loop"); after the transition
chapter, **everything is q**.

## Hierarchy of objectives (resolves all conflicts — higher wins)

1. **Learning.** The author writes real running q (tables, qSQL, `aj`) and learns skill
   authoring AND skill evaluation as a transferable discipline. This is why the project exists.
2. **Curriculum.** ~10 verified lessons: imperative programmer → array-native. Every code block
   executes via `make verify`; no unverified snippets ever.
3. **Skill EVALUATION (authoring only if a gap is proven).** REVISED after discovering KX ships
   official Claude Code plugins for q/PyKX/KDB-X/KDB.AI (with qlint integration, own marketplace).
   Authoring a competing general q skill is redundant. The learning objective was skill authoring
   AND EVALUATION — so the deliverable is now an independent evaluation of KX's official q plugin
   vs. baseline, published. A skill is authored ONLY if that eval exposes a specific gap, and is
   scoped narrowly to it. Hypothesis to test, not assume: KX's plugins serve practitioners writing
   production q; nothing there coaches a newcomer OUT of imperative habits (this repo's thesis).
4. **Blog series.** Six articles as forcing function. Exhaust of the work, never its driver.

Standing rule: when objectives conflict, the lower-numbered one wins. Specifically, marketplace
discoverability never reshapes pedagogy.

**Compounding (cross-cutting):** every milestone appends to docs/COMPOUND.md; eval methodology
and skill-authoring patterns transfer to other projects.

**Non-goals:** easiest array intro (BQN's lane; README says so), quant training, building
playgrounds/tracers, covering k/APL/BQN beyond honest pointers.

## Users

- **First user: the author.** The learning axis is real, not a framing device.
- **Second user of any SKILL we ship:** a LEARNER moving from imperative habits into q — NOT the
  kdb+ practitioner (KX's official plugins already serve that user better, with qlint). If the
  eval shows no gap for the learner either, no skill ships. Any skill we do author is q-only;
  J is cut from skill scope entirely (the J-asking user does not exist).
- **Second user of the CURRICULUM:** a programmer curious about array languages, with q as a
  destination worth arriving at.
- These two diverge. Per the hierarchy, the curriculum's reader wins any conflict.

## Product shape (MVP — hard scope)

1. **Curriculum (~10 lessons):**
   - Part I — The J prelude (1–2 lessons, ILLUSTRATIVE): snippets with captured outputs showing
     where the paradigm comes from — mean-as-fork `(+/ % #)`, rank, trains. **No reader toolchain
     required**; J is read-along, not install-and-run. (Examples stay executable in author-side CI
     because jconsole is free and license-free — the one green check independent of KX.)
     Rationale: q teaches the array shift natively (til, vector ops, each/over/scan); what J
     uniquely shows is exactly the non-transferable part, so it earns illustration, not a chapter.
   - Transition chapter: "Everything after this point is q." Honest paragraph on what J idioms
     do NOT carry over (no trains/forks/rank in q; q idioms are each/over/qSQL).
   - Part II — q (the overwhelming majority): atoms/lists (HALF a lesson — not the payload),
     then the real conceptual core: **dict → table (a table is a flip of a column dict; a keyed
     table is a dict)**. Then qSQL (select…by…from), word frequency + moving average,
     **an attributes & sort-discipline lesson (`s#`/`g#`/`p#`)** — required BEFORE the showcase,
     because aj's correctness and performance both depend on it — and the showcase: **as-of join**
     (`aj`) matching trades to prevailing quotes, end-to-end.
     Showcase framing (corrected): NOT "the primitive quants pay for" — as-of joins now exist in
     pandas merge_asof, Polars, DuckDB, QuestDB, ClickHouse. The honest and better frame is
     "you already know this join; here is what it looks like when the language and storage engine
     are designed around it."
2. **AI-authoring skill** (`.claude/skills/idiomatic-q/`): thin, high-density idiom/gotcha
   doc so models emit idiomatic J/q instead of loop transliterations. **Gated by eval (below).**
3. **Verification:** every example runs locally via `make verify`. J CI blocking. q CI nightly +
   opportunistic (trusted branches only), pinned known-good versions. Golden files: showcase only.

## Authoring rules (mechanical guards against known stall modes)

- **Q-first authoring:** every lesson's q side is written and RUNNING before any J prelude text.
  (The old "no J longer than q" rule is CUT — J is 3–6x terser than q, so byte counts never bound
  the real stall resource, which is hours. Q-first sequencing does bind.)
- **Week-1 gate:** `aj` runs end-to-end with a real KDB-X CE license before any polish work.
- Any lesson that is just code blocks + a sentence gets cut or merged (narrative is the product).

## Eval gate (M2) — REVISED TARGET

Subject under test is now **KX's official Claude Code q plugin** (plus baseline), not a
self-authored skill. Deliverable: a published independent evaluation. Author a skill only if a
gap appears, scoped to that gap.

**A. Trigger precision (activation).** 10 prompts that SHOULD fire, 10 adjacent traps that should
not (NumPy vectorization, plain SQL, APL/BQN, generic "write a query"). A skill that never fires
is worth zero. After tuning trigger wording, **re-test on FRESH prompts** — iterating on the same
20 overfits the trigger to the test set.

**B. Output quality.** ~15 tasks per condition (translate-from-Python, write-from-spec,
fix-unidiomatic). Paired design: same tasks, both conditions.
- **Correctness:** runs + right output via the verify harness (0/1).
- **Idiomaticity: 5-item BINARY CHECKLIST**, each item justifiable against a PUBLISHED source
  (Q for Mortals / code.kx.com), never the author's taste — this is the real defense against
  evaluator drift between week 2 and week 8:
  [ ] no explicit loop where a vector op exists  [ ] uses qSQL where a table op is expected
  [ ] built-ins over hand-rolled iteration  [ ] no unnecessary temporaries
  [ ] matches a cited published idiom
- Record token count and repair iterations to first running solution.
- **Do NOT claim blind scoring.** Idiomatic output identifies its own condition; blinding is
  impossible in principle here. The published-source checklist is the honest defense — say so.

**Decision rule (fixed):** the old "<15% improvement" threshold is CUT — at n=15 binary outcomes
the sampling noise is the size of the effect, so the instrument could not adjudicate its own rule.
Replace with a **paired sign test on discordant pairs**: count tasks where the two conditions
differ; the effect counts as real only if one side wins ≥~80% of discordant pairs (roughly: wins
at least 4 more tasks than it loses). This detects only large effects — appropriate, since a skill
worth maintaining should show a large effect on a language models are measurably bad at.

**Two exits, not one:** (1) no lift → publish the negative result; (2) lift exists but KX's plugin
already delivers it → publish the comparison, author nothing. Both are real findings.

## Toolchain & licensing

- **J 9.7** (GPLv3, jsoftware) — `jconsole` headless; CI-safe; blocking checks.
- **q via KDB-X Community Edition** (GA Nov 2025; **personal / internal-business use ONLY** — NOT
  commercial distribution or monetization, and **benchmark/performance publication prohibited
  without prior written KX consent** — per the actual license read at Task Zero, KX Community
  Edition License Agreement v1.1 (27 Aug 2025), see docs/licensing-notes.md. `.Q.lim`-confirmed caps:
  16GB RAM / 4 secondary threads / 16 conns / no per-process core limit (24-core aggregate license
  cap); license key + license-validation phone-home reserved by Clause 4).
  NOTE: the earlier "free personal+commercial per KX marketing" was NOT supported by the license text
  — corrected 2026-07-24 (see docs/COMPOUND.md).
- **TASK ZERO — RESOLVED 2026-07-24** (full findings + sources: docs/licensing-notes.md). The three
  reads, done:
  (1) license read (KX CE License Agreement v1.1, 27 Aug 2025): **personal / internal-business use
      ONLY**, benchmark-restricted — the "more restrictive text" IS the license; no commercial claim;
  (2) benchmark clause **FOUND** (Clause 9: no publishing performance/benchmark info without prior
      written KX consent) → Article 5 takes the no-numbers, design/semantics path;
  (3) KX ships `KxSystems/kx-skills` (5 plugins, incl. `q-knowledge` + qlint) + 2 MCP servers; none
      coach a newcomer out of imperative habits, so the learner niche survives (see objective 3).
- Native Windows is not supported (WSL only) — state this in the README.
- License key is delivered via an authenticated install script and checked at startup: fine on
  CI runners with egress, fatal for any future offline verification.
- Older kdb+ Personal Edition explicitly rejected (non-commercial, local-only; kills CI).

## Repo conventions

- Plain repo + **Makefile** (no Bun/JS — nothing here is JavaScript).
- Layout: `lessons/NN-name/{README.md,q/,j/}`, `showcase/aj/`,
  `.claude/skills/idiomatic-q/`, `eval/`, `writings/`, `.github/workflows/`.
- License: Apache-2.0 for code; CC-BY-4.0 for prose/lessons (decide at M1, document the choice).

## README obligations

- Non-affiliation disclaimer (KX Systems, Jsoftware). Names used nominatively.
- **Why J, not BQN:** honest paragraph — J is the laboratory because it is the author's native
  array language; newcomers with no destination may prefer BQN (link); concepts transfer.
- Prior art: Jim Pivarski's "Thinking in Arrays" (SciPy/PyCon, NumPy/JAX — different lane),
  Rosetta Code, Q for Mortals, J for C Programmers.
- Keywords + GitHub topics carrying the discoverability the name deliberately doesn't.

## Explicitly cut / deferred

- Human-tutor skill (defer until demand exists). Game of Life, FizzBuzz. Bun monorepo.
- Golden files for every example. Building playgrounds/tracers (link J playground & KX sandbox).

## Milestones & blog series (each article gated on its milestone WORKING)

- **M1 — Foundation (wk 1):** TASK ZERO's three reads; toolchain pinned; `aj` end-to-end;
  **the eval verify-harness built** (it is a week-2 dependency and is itself content work:
  ~30 task prompts + 20 trigger prompts); repo public.
  → Article 1 "Array thinking, all the way to q: learning in public";
  → Article 2 "Running q in a public repo: the KDB-X licensing maze" (stagger 3–5 days).
- **M2 — Eval gate (wk 2–3):** trigger precision + output quality run; verdict written.
  → Article 3 "Does KX's official q plugin actually make Claude better at q?" (flagship —
  an independent evaluation of a vendor plugin; genuinely new data for the community).
- **M3 — J laboratory (wk 3–4):** Part I + transition chapter verified.
  → Article 4 "Unlearn the loop: what J shows that q hides". **AT-RISK ARTICLE** — least novelty
  for the author (he already knows J), arrives right after the two exciting milestones. Draft it
  during M1 while enthusiasm is high.
- **M4 — The q core (wk 5–7):** Part II + `aj` showcase golden-filed; nightly q CI live.
  → Article 5 "The as-of join: what changes when the engine is built around one primitive"
  (NOT "why quants pay" — the primitive has spread to pandas/Polars/DuckDB/QuestDB/ClickHouse;
  the story is co-design, not scarcity). Benchmark clause CHECKED (2026-07-24): license Clause 9
  bars publishing KDB-X performance/benchmark numbers without prior written KX consent →
  DECISION (provisional): design/semantics framing, NO benchmark numbers; revisit authorization
  later if wanted. See docs/licensing-notes.md.
- **M5 — Ship (wk 8):** skill hardened from eval findings; marketplace submission; v1 tag.
  → Article 6 "Teaching an AI a niche language: what compounds" — **packaging, not new writing.**
  COMPOUND.md is appended continuously at every milestone; article 6 publishes what it already
  contains. If that discipline holds, this article costs an hour.

Article drafts live in `writings/`. Publishing/syndication is an operational checklist
(`RELEASE-CHECKLIST.md`), not product scope.

## Review trail (for Compound step)

- Claude self-review: CI fragility; dual-axis inversion → q-first; commodity-snippet risk; cuts.
- ChatGPT round 1: family→laboratory reframe; "no J > q" rule; eval as gate; opportunistic CI;
  BQN question → honesty paragraph.
- Fable 5 (round 3, deepest): KX ALREADY SHIPS official Claude Code q plugins → pivot from
  authoring a skill to EVALUATING theirs; J demoted from executable chapter to illustrative
  prelude (25% was a reviewer compromise, not a derived number); length rule cut as toothless;
  aj-as-quant-moat framing is stale; eval threshold statistically unadjudicable at n=15 → sign
  test; blinding impossible in principle; missing attributes/sorting lesson; aj technical
  corrections; q has no true multidimensional arrays; benchmark-clause + WSL-only warnings.
- ChatGPT round 2: rename; trigger-precision eval (the biggest miss — quality after activation
  is worthless if it never fires); binary checklist vs. drifting idiomaticity score; syndication
  out of spec; demand for an objective hierarchy; "who is the second user".
- Rejected from round 3: "the verified curriculum, not the skill, justifies the repo" is CORRECT
  and adopted — but note the consequence: the KX discovery did NOT dent the repo's reason to
  exist, which is the test that proves it. J stays executable in author-side CI (reviewer would
  have dropped it) because jconsole is license-free and is the only CI leg independent of KX.
- Rejected, with reasons: "fatal unless reframed" severity (personal learning project, not
  PMF-seeking); "needs a built tracer or cut" (skill IS the tool); "naming before validation is
  waste" (standing principle, cheap); "cut article 6" (self-contradictory — pre-existing content
  makes it the CHEAPEST article, and its own fix already de-risks it); "make the marketplace skill
  the centre of gravity" (would make curriculum into marketing collateral and invert the learning
  axis; marketplace was additive, not repositioning); "there is one second user" (two artifacts,
  two audiences — named explicitly above rather than collapsed).
