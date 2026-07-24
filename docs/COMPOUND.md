# COMPOUND.md

Append at EVERY milestone — this file is the raw material for article 6, which is packaging,
not new writing. Keeping this current is what makes the final article cost an hour.

Per entry: what worked / what broke / what transfers to other projects.

## M0 — Planning (2026-07)
- Three adversarial review rounds before any code. Biggest catch: an eval that measured
  output quality but never measured whether the skill ACTIVATES. Transferable to all future
  skill work — trigger precision is half the eval.
- Reviewer findings are not automatically correct: two were rejected as self-contradictory
  (cut the cheapest article; build a tracer while also cutting scope). Adversarial review needs
  its own adversarial check.
- Naming: the reframe (J from co-star to 25% laboratory) silently invalidated the original
  name. Lesson: re-check the name whenever the scope ratio changes.

## M1 — Task Zero research pass (2026-07-22)

Findings + FLAGGED contradictions from the pre-download research (no account used). Full detail in
`docs/licensing-notes.md`. Recorded here per the rule: a contradiction is a finding, not a silent
edit to the spec.

### Internal-doc contradictions (eval/PROTOCOL.md was only half-updated after the Fable-5 review)
PROTOCOL.md's title was updated to the new subject but its body still encodes the OLD design. Three
mismatches against SPEC.md/CLAUDE.md — PROTOCOL.md needs a reconciling edit before M2:
1. **Decision rule.** PROTOCOL.md still says "<15% improvement → CUT"; SPEC/CLAUDE **cut** that
   threshold (unadjudicable at n=15) and replace it with a **paired sign test on discordant pairs**.
2. **Blinding.** PROTOCOL.md says "score A/B pairs without knowing which is which"; SPEC/CLAUDE say
   **do NOT claim blind scoring** — idiomatic output identifies its own condition; impossible in
   principle. The published-source checklist is the honest defense.
3. **Subject under test.** PROTOCOL.md's body describes A/B testing a **self-authored skill**
   ("A = no skill, B = skill enabled"); SPEC/CLAUDE fix the subject as **KX's `q-knowledge` plugin
   vs. baseline**, authoring a skill only if a gap appears.
Transferable lesson: when a review pivots the *subject* of a doc, patch the whole body in one pass —
a title-only update leaves a booby-trapped protocol that reads as current.

### Research-vs-SPEC nuances (flag, don't edit SPEC)
- **The newcomer niche survives, but SPEC.md over-states the gap.** SPEC §objective-3 hypothesizes
  "nothing there coaches a newcomer OUT of imperative habits." Reality: KX's `q-knowledge` SKILL
  *does* carry the anti-loop rules ("Vectorize, don't loop"; "Avoid do/while, use Over/Scan") — as
  terse **model-steering**, not human pedagogy. The real gap is the WHY-narrative for a human
  learner, not the presence of idiom rules. Sharper eval framing: measure whether our
  learner-narrative beats KX's rules for a *newcomer's* output, not whether the rules exist.
- **Phone-home may be install-time, not startup.** SPEC calls KDB-X CE phone-home "checked at
  startup … fatal for offline verification." Secondary sources say CE runs offline at runtime
  (telemetry opt-in); validation is install-time. If confirmed, offline verify is NOT fatal — only
  install needs egress. Confirm on a real install.
- **A stricter CE license really did circulate** (July-2025 preview: non-commercial, phone-home,
  no monetization). Confirms SPEC's warning; the GA commercial grant stays UNCONFIRMED until the
  gated `kc.lic` EULA is read. CLAUDE.md rule 4 (no commercial-friendliness claims) holds.
- **Benchmark clause: unresolved and legally material.** No public statement for KDB-X CE; the OLD
  Personal Edition still carries an explicit DeWitt-style ban (§1.3). Article 5 is blocked on
  reading the actual CE EULA. Transferable: vendor "free tier" benchmark rights are gated exhaust —
  budget a license read before any performance write-up.

### Tooling gotchas discovered
- **`jconsole` name collision on macOS.** `/usr/bin/jconsole` is Apple's **Java** JConsole shim
  (dispatches to the JDK), not the J interpreter. The Makefile default `J ?= jconsole` would invoke
  the wrong tool locally (Ubuntu CI is unaffected). Recorded in `docs/toolchain.md`; use
  `make J=/path/to/real/jconsole`. Transferable: verify a toolchain binary is the *language's*, not
  a same-named system tool, before wiring it into `make`/CI.
- **KX ships two MCP servers + a 5-plugin marketplace** (`kx-skills`), none pinned to a version tag
  — "record the exact version" means pinning a commit SHA, not reading a release number.

## M1 — License READ + PROTOCOL.md reconciled (2026-07-24)

Owner registered + installed; the CE license went public, so it was read in full (KX Community
Edition License Agreement v1.1, 27 Aug 2025). Two pre-read unknowns resolved — **both restrictive**.

- **CONFIRMED contradiction with SPEC.md line 126 ("free personal+commercial per KX marketing").**
  The license grants **personal / internal-business use ONLY** (Clause 2.1 + Attachment A), bans
  selling/publishing/distributing the Software and building a competing/similar product (2.1.xi).
  Resolution of CLAUDE.md rule 4: **do NOT claim commercial-friendliness anywhere.** The project
  survives because it is personal use distributing *lessons*, not the Software — but the spec's
  commercial framing must not propagate into README/articles.
- **Benchmark clause is LIVE in KDB-X CE, not just the old Personal Edition.** Clause 9 bans
  disclosing "any benchmark, test or performance information or any report which contains a
  competitive analysis" without prior written KX consent. **Article 5 cannot publish KDB-X
  performance numbers** without authorization; reframe to design/semantics (SPEC already leans that
  way) or get written consent. The `aj` showcase is unaffected (it asserts correctness, not speed).
- **Phone-home: my pre-read "runs fully offline" guess was wrong.** Clause 4 reserves a periodic
  license-validation call — so SPEC's "fatal for offline verification" concern is VALID. CI-with-
  egress is fine; air-gapped verify is at-risk. (Usage *telemetry* is a separate opt-in — declined.)
- Transferable: **do not let a secondary blog override a primary license.** The defconq "offline"
  claim contradicted the actual Clause 4. When a license is gated, mark findings UNCONFIRMED and
  do not soften a spec's risk flag on secondary authority — which is exactly what the earlier note
  did, and the license read corrected.

**PROTOCOL.md fixed** (the three flagged contradictions + a fourth found while editing):
1. decision rule → paired sign test (was stale "<15%"); 2. blinding → explicit no-blind-scoring;
3. subject → KX `q-knowledge` plugin vs. baseline (was "A=no skill, B=skill"); 4. **eval is now
q-only** — dropped "per language"/"J NuVoc" and removed `eval/tasks/j/` (SPEC obj. 3 cuts J from
skill scope; there is no J skill or KX J plugin to compare). Lesson restated: a review that pivots
a doc's *subject* must patch the whole body in one pass — a title-only update is a booby trap.

**Task Zero closed out (2026-07-24), from the live install:**
- `.Q.lim[]`: mem 16384MB / threads 4 / **conns 16** / cores 0W. **The connections limit is 16, not
  8** — the KX doc page was right and the secondary "runtime = 8" blog was wrong. Second time a
  secondary source lost to primary evidence this milestone (cf. the "offline" phone-home claim).
  Standing lesson reinforced: **verify caps against `.Q.lim` on the actual build, not blog posts.**
- Key is **NONEXPIRE**; build **KDB-X 5.0 / 2026.07.23 / COMMUNITY** pinned in toolchain.md
  (serial/email/host redacted — repo goes public).
- `kx-skills` pinned at commit `8b7040f…9e8857e` (no version tag exists; the SHA is the pin).
- **Decision (Article 5, provisional):** take the easier path — design/semantics framing with NO
  KDB-X performance numbers, so Clause 9 needs no written consent now. Revisit later if the article
  wants numbers. SPEC.md Article 5 line updated to record the checked-clause + decision.
- SPEC.md line 126–127 CORRECTED (owner-authorized): the commercial-friendliness claim replaced
  with the actual personal/internal-business-only terms + benchmark restriction. Not a silent edit —
  carries an inline "corrected 2026-07-24" note pointing here.
- Net: no licensing/tooling unknowns remain for Task Zero. Only operational setup left (install J 9.7).

## M1 — `aj` showcase gate GREEN (2026-07-24)
- `showcase/aj/aj.q` runs end-to-end on real **KDB-X 5.0**; output golden-filed in `expected.txt`;
  full `make verify` green (verify-j/verify-q no-op, verify-showcase `aj: OK`). This is the **q half
  of the M1 gate**; the other half — the eval verify-harness (~30 task + 20 trigger prompts) — is
  still to build.
- The showcase doubles as the first *running* proof of the two corrected SKILL.md `aj` claims:
  join columns passed explicitly as a symbol vector (claim 4), and `g#` on a sorted-by-`sym,time`
  quote table (claim 5) — verified by executing code, not just reading docs. Q-first rule honored.
- **Tooling gotcha:** q lives at `~/.kx/bin/q`, added to PATH by the installer editing `~/.zshrc`.
  Non-login shells and CI don't source `.zshrc`, so `q` isn't found there — use `make Q=/path/to/q`
  (documented in toolchain.md). Transferable: an installer that edits an interactive rc file is
  invisible to CI; always parameterize the tool path in the Makefile.
- **J install was broken, now RESOLVED (2026-07-24):** `brew install --cask j` (9.7.1) failed with
  `Error: unknown install step: inreplace` and rolled back its symlinks/apps. Homebrew was already
  current (6.0.11), so this is a **cask bug, not staleness** — retrying the cask is futile. Fixed by
  bypassing the cask and running jsoftware's OWN installer headless:
  `curl -fsSL jsoftware.com/download/j9.7/jinstall.sh | sh -s -- --qt none --no-addons` →
  **J 9.7.1 at `~/j9.7/bin/jconsole`**; `make verify` green with both real tools. Transferable
  lesson: when a vendor Homebrew cask breaks on a wrapper step (e.g. `inreplace`) and Homebrew is
  current, the vendor's own installer — which the cask merely wraps — is the reliable fallback; the
  cask added the failure, not the payload. Skipping the Qt GUI (`--qt none`) also removes the whole
  class of problem the cask hit ("next step updates Jqt ide").
