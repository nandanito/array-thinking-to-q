# COMPOUND.md

Append at EVERY milestone — this file is the raw material for article 6, which is packaging,
not new writing. Keeping this current is what makes the final article cost an hour.

Per entry: what worked / what broke / what transfers to other projects.

> **Milestone renumbering, 2026-07-28.** SPEC's M3 and M4 were swapped (q core now M3, J laboratory
> now M4). This file is an append-only log, so **earlier entries keep their original labels**:
> anything below titled "M4 — Part II …" is work on what is now **M3**. Entries are not rewritten
> to match — a log that gets edited to agree with the present is not evidence of anything.

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
- Transferable: **do not let a secondary blog override a primary license.** A community blog's
  "offline" claim contradicted the actual Clause 4. When a license is gated, mark findings UNCONFIRMED and
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

## M1 — eval verify-harness built (2026-07-24)
- Built on branch `eval-verify-harness` (kept off `main` so the codex review is a clean, focused
  diff vs the foundation baseline). 15 q reference tasks (translate/spec/fix; ≥3 qSQL, ≥2 aj) +
  20 trigger prompts (10 should-fire, 10 adjacent traps) + results.csv/verdict.md/README templates.
- **Goldens are GENERATED by running each reference on the pinned KDB-X build, never hand-written.**
  Hand-computed expected output drifts from q's actual display (e.g. `3f`, trailing-space padding,
  keyed-table key order) — the diff would then fail on formatting, not correctness. Same rule as the
  showcase. Transferable: for any golden-file harness, capture the golden from the real tool.
- **The eval is the measurement instrument, so it needs its own self-test.** `make verify-eval`
  re-runs all references vs goldens (and is in `make verify`), catching silent rot when the q build
  changes before the instrument is trusted to score candidates. A broken instrument reports noise.
- Eval is q-only (J cut, SPEC obj. 3). Subject pinned to `q-knowledge@kx-skills` — the trap set
  deliberately includes J-rank and pandas-`merge_asof` prompts to test precision, not just recall.

## M4 — Part II kickoff: lesson 01 (atoms/lists) (2026-07-24)

First curriculum lesson written q-first and verified end-to-end (`make verify` green: q +
J twin + showcase + eval all pass). `lessons/01-atoms-and-lists/` + a Part II index
(`lessons/README.md`). Transferable findings, mostly about the *authoring mechanics* of an
everything-executes teaching repo:

- **Erroring code cannot live in a verify-clean lesson file — so "this is wrong" demos must be
  prose transcripts, not executable artifacts.** The lesson's whole payoff is that the J mean-fork
  `(+/ % #) til 5` FAILS in q. But `make verify-q` requires every `*.q` to exit 0, so the failure
  can't be a lesson file. Pattern that resolves the tension: the runnable file holds only the
  CORRECT idioms; the failure is a captured REPL transcript embedded in the narrative, clearly
  marked. Keeps rule 3 (everything executes) intact without lying about what runs.
- **q's fork rejection is a PARSE error, not a runtime type error — and the distinction is
  testable.** `@[{(+/ % #) til 5};::;...]` does NOT trap it (protected eval catches runtime
  signals, but there's nothing to evaluate — the parse already failed). `@[value;"(+/ % #) til 5";...]`
  DOES trap it, because now the parse happens inside the protected call. Sharpens the pedagogy
  ("q has no fork *production* in its grammar") and is a transferable q-harness fact: to trap a
  malformed-q string, wrap `value`/`parse`, not the expression.
- **Derived functions (`/`, `\`) applied prefix must be parenthesized:** `(+/) til 5` → 10, bare
  `+/ til 5` does not parse. Day-to-day you dodge it with the named fold (`sum`), but a lesson that
  shows the mechanism has to wrap it. Verified on the pinned build, not asserted from memory.
- **Every displayed output is captured from the real tool, then pasted into the narrative** (same
  rule as goldens): `avg til 5` shows `2f` not `2` (float promotion), booleans render `00011b`.
  Hand-typed "expected" output drifts from q's actual display; run it, then quote it.
- Process: the Q-first rule (CLAUDE.md #1) paid off — pinning q's *actual* behavior (incl. three
  dead-end parse experiments) BEFORE writing narrative meant the prose had zero claims to walk back.

## M4 — Part II lesson 02 (dict → table) (2026-07-24)

The conceptual core lesson: a table is `flip` of a column dict (`98h`); a keyed table is a dict
(`99h`) mapping a key-table to a value-table. Written q-first, `make verify` green. Transferable:

- **Prefer a `~` equivalence proof over type-casting cleverness.** First draft tried
  `99h$type each (cd;t)` to "show" the dict/table relationship — it errored AND obscured the point.
  The clean teach is `t ~ flip cd` → `1b` and `t ~ ([] …)` → `1b`: q's own equality operator proves
  "a table IS the flipped dict" and "the `([]` literal IS that flip," with zero ceremony. When
  teaching an identity, assert the identity (`~`), don't reconstruct it.
- **The type numbers ARE the lesson, so display them.** `type d`=`99h`, `type t`=`98h`,
  `type kt`=`99h` — showing the *same* `99h` for a plain dict and a keyed table is the whole
  "a keyed table is a dictionary" claim, made by the interpreter rather than by prose. Added
  `show type d` purely so step 1 and step 6 rhyme numerically.
- **J-twin recipe that works: find the ONE shared operation, show identical output, then name the
  delta.** `|: (2 3 $ 1 2 3 4 5 6)` is byte-for-byte q's `flip (1 2 3;4 5 6)`. Identical bytes make
  "transpose transfers" undeniable; the divergence (J transposes positions → a matrix; q transposes
  *named* columns → a table) then lands as the real content. Ties back to lesson 01's wall from the
  other side: J has the rank/plumbing q lacks; q has the named structure J lacks.
- **Verify EVERY external URL in a public doc — memory is not a source.** Checked 6 links across the
  two lessons; 2 were wrong: the J dictionary `d331.htm` is *Cut*, not Transpose, and
  `code.jsoftware.com/wiki/*` returns 403 to all automated fetchers (live for humans, unverifiable
  by me → don't cite it). Fix: cite only fetch-verifiable URLs (`code.kx.com`,
  `jsoftware.com/help/learning`) and reframe the J reference to the *Ranks* chapter, which actually
  supports the twin's thesis better than a transpose page would. Transferable to every doc with
  citations: a plausible-looking URL from model memory is a coin flip; fetch it or drop it.

## M4 — independent review pass on lessons 01–02 (2026-07-24)

Ran an independent reviewer (fresh subagent, handed the pinned binaries) over both lessons after
they were committed and pushed. It found real defects a self-review had missed — the round-trip paid:

- **`count each ("aa";"bbb";"c")`: `"c"` is a char ATOM (`type` `-10h`), not a one-char "string".**
  Its count is 1 for the SAME reason lesson 01 §1 teaches (an atom answers `count` with 1), so
  calling it a "string" quietly undercut the lesson's own opening. Chasing that flag surfaced a
  NEIGHBOURING bug the reviewer had not named: plain `count (…)` is `3` (three items), not the
  character total — so the old "each stops count drilling into the characters" was also false.
  Lesson: a flagged inaccuracy usually has an adjacent one; fix the neighbourhood, not just the line.
- **q stamps parse errors with a wall-clock timestamp in BOTH interactive and piped modes.** Verified
  by driving q through a real pty (python `pty.fork`), not just a pipe — the doc had claimed the
  timestamp was a non-interactive-only artifact, a claim a piped capture cannot disprove. Lesson: to
  characterise a REPL's *interactive* output, run it through a pty; piped stdin is a different path.
- **"Shown code" must equal "the file it points to."** The README J blocks had drifted from the
  `.ijs` files (extra inline result-comments, reworded `NB.` text). Fixed by showing the file's lines
  verbatim plus a separate captured-output block — the same code/output split already used for q.
- Minor but telling: the lesson headers said "Run it: `q …`" while the index they link to stresses
  the binaries are NOT on `PATH`; and one center/centre spelling split the same phrase. An
  independent reader catches "contradicts our own stated rule" bugs the author is blind to.

Process note: reviewer findings are not automatically correct (standing rule), so each was
re-verified on the pinned build before applying — all held. Fixes shipped as a follow-up commit, not
an amend, because the reviewed commits were already on the remote (no history rewrite of pushed work).

## M4 — CI enablement for the J twins (2026-07-24, recorded late)

`j-verify.yml` had shipped as a valid-but-EMPTY stub: its "Install J" step was a commented TODO
gated on "the first `.ijs` lands". When lesson 01–02's twins landed, the gate condition was met but
the workflow was not updated, so the check went green having verified nothing. Two transferable
findings, both about **green checks that are lying**:

- **`curl … | sh` reports the SHELL's exit status, not curl's.** The install step was
  `curl -fsSL <url> | sh -s -- …`; when the fetch failed, `sh` received an empty script, did
  nothing, and exited 0 — so the step passed and J was never installed. Fix: download to a file,
  assert the download, run it, then assert the artifact exists (`test -x …/jconsole`). Standing
  rule for CI: **a pipeline's exit status is its LAST command; never let a network fetch be
  anything but the last command in a step**, and always end an install step with a positive
  assertion that the thing installed.
- **`jsoftware.com`'s TLS cert does not cover the bare host** — only `www.jsoftware.com` (curl
  error 60). Local installs used the bare host and worked from a browser-warmed context; CI did
  not. Transferable: pin the exact host that the cert covers, and prefer `www.` when a vendor's
  apex is a redirect.
- Process: a "TODO, enable when X lands" comment in CI is a **time bomb with no alarm**. Nothing
  fails when X lands; the check just keeps passing vacuously. If a gate cannot be enforced, make
  the stub FAIL (`exit 1` with the reason) rather than pass, so landing X forces the update.

## M4 — Part II lesson 03 (qSQL) (2026-07-25)

`select … by … from` taught as a surface over lesson 02's row-dict / column-list views. Written
q-first, `make verify` green (q + 3 J twins + `aj` golden + 15 eval refs). Content findings:

- **The teachable core of `by` is that it does NOT aggregate.** `select px by sym from t` — illegal
  in standard SQL — returns one *list per group*, and the aggregation in `select sum qty by sym`
  happened only because `sum` of a list is an atom. Framing `by` as "cut each column into per-group
  lists" (with aggregation as an optional second step) explains in one sentence why `by` is strictly
  more general than `GROUP BY`, and why `select sum qty from t` returns one row without `select`
  knowing anything about "aggregates".
- **The real imperative failure mode in q is not the loop — it is forgetting a column spans every
  group.** `update ma:2 mavg px from t` (no `by`) averages an AAPL price against an MSFT price and
  returns a full column of confident nonsense, no error. Nobody wrote a loop; the bug is that any
  operation *with memory* (window, delta, cumulative) runs straight across group boundaries by
  default. This is a better "what the imperative instinct gets wrong" beat than the loop itself,
  because the reader has already accepted vectorization by lesson 03 and would not see it coming.
- **`group` vs `by` ORDER differs and is `~`-observable:** `group` preserves first-appearance order;
  `by` sorts its keys and stamps them `` `s# ``. `(count each group w) ~ exec count i by w from …`
  is `0b` even though every count agrees. That stray `` `s `` is a free, honest hand-off into
  lesson 04 (attributes) — the curriculum's next beat is discovered in the output, not bolted on.
- **J-twin recipe (second application, still works): one shared operation, then name the delta.**
  `#/.~ w` is `count each group w` and gives the same five counts — but J returns bare counts with
  the labels as a *separate* `~. w` result, aligned only by a documented ordering convention.
  Same names-vs-positions delta as lesson 02, now with a consequence: q's grouped result is still
  queryable/joinable because the labels ride along. Bonus trap: J's infix `3 (+/ % #)\` yields
  COMPLETE windows only (4 results from 6 inputs) while q's `3 mavg` ramps up (6 from 6) — a
  translated idiom that silently changes its result LENGTH is the kind of bug that survives review.

Process findings:

- **Consult COMPOUND.md BEFORE repeating a class of work, not just when appending to it.** The
  lesson-02 entry already records that `code.jsoftware.com/wiki/*` 403s every automated fetcher and
  must not be cited. This lesson's first draft cited two such URLs anyway, and the finding was
  re-derived from scratch by curl. The file earned its keep — but only at review time, when it
  should have been read at draft time. A compounding doc that is only ever *written* is a diary;
  reading it first is what makes it an asset.
- **Hand-assembled output is a rule violation even when every character is real.** A draft §7 laid
  two captured q outputs side by side in one fenced block to save space. Both halves were genuine,
  but the composite was typed by me and appears nowhere in any run — exactly what "outputs are
  captured, never hand-typed" exists to forbid. Fix: separate blocks, each quoting one real run.
  Transferable: the golden-file discipline covers *arrangement*, not just content.
- **Make prose claims about a verb FAMILY verify-backed by exercising the family.** The draft
  asserted the whole `m`-family ramps up the same way while the runnable file showed only `msum`.
  Cheapest honest fix is not to soften the prose but to add `mmax`/`mmin` to the `.q` file so
  `make verify` exercises the claim and the lesson can quote three real outputs. If a sentence
  generalises, make the harness generalise with it.

### Review pass on lesson 03 — mechanise the "outputs are captured" rule

`make verify` proves the lesson's *files* run. It says nothing about whether the outputs pasted
into the *narrative* are the ones those files produce — the gap every previous lesson checked by
eye. A ~30-line throwaway script closes it: extract every unlabelled fenced block from the README,
rstrip both sides, and assert each appears as a contiguous run in a fresh capture — then assert the
match positions increase monotonically, which also catches narrative shown out of execution order.
Result on lesson 03: 22/22 blocks matched, in order. **Transferable to any everything-executes
teaching repo: the golden-file discipline should cover the PROSE, not just the harness.** Cheap
enough to run per-lesson; worth promoting to a `make` target if a fourth lesson needs it.

Two things the mechanised pass found that reading had missed:

- **`~` ignores attributes — so the lesson's own `0b` had the wrong explanation.** The draft said
  `by` "sorts its keys AND marks them `` `s# ``" and then showed `(count each group w) ~ exec …`
  → `0b`, inviting the reader to credit the attribute. Proved otherwise: `(`s#1 2 3) ~ 1 2 3` is
  `1b`, and re-keying the `group` result into `by`'s order makes the two dictionaries `~`-identical
  despite the attribute. The `0b` is ordering, full stop. Lesson: when prose lists two differences
  and then shows one test failing, the test must be attributed to the difference that actually
  caused it — otherwise the lesson teaches a false mechanism while displaying a true output.
  (Bonus: "attributes are metadata `~` does not look at" is a *better* hand-off to lesson 04.)
- **Series drift found in MERGED work, then fixed (owner-directed): lesson 02 hand-added `q)`
  prompt lines inside 4 output blocks.** A piped `q file.q -q < /dev/null` emits no prompt, so
  those lines were typed, not captured — the same class of defect as the side-by-side block above,
  sitting on `main` since PR #1. Removing the prompt line is the whole fix: the preceding ```q
  block already shows what produced the output, which is lesson 03's convention anyway.
  **Running the checker over the whole series (not just the lesson under review) is what turned one
  noticed defect into a complete list** — 31 output blocks across 3 lessons now verify. Generalise
  the check before trusting it: scoping it to the file you are already suspicious of finds only
  what you already knew.
- **Lesson 01's `q)` line is NOT the same defect — context decides.** It sits inside a ```q block
  as the deliberate interactive REPL transcript of the fork parse-error (the pattern this file
  records for demos that cannot live in a verify-clean file), where a prompt is honest. A blind
  `grep '^q)'` + bulk delete would have destroyed a correct artifact. Mechanised checks locate
  candidates; they do not adjudicate them.
- Spelling harmonised to British across lessons (`vectorise`, `parenthesised` in lesson 01, which
  was the odd one out against `memorise`/`centre` in 02 and 03). Left `SPEC.md`'s "NumPy
  vectorization" alone — it is a contract doc quoting a NumPy term of art, not lesson prose.

## M2 — the eval ran, and returned a null result (2026-07-26/27)

Subject: KX's `q-knowledge@kx-skills` pinned at `8b7040f`, vs. baseline, on `claude-opus-5`.
Full writeup in [`eval/verdict.md`](../eval/verdict.md); raw material in `eval/runs/`.

**Headline: no measurable lift — and the qualifier matters more than the headline.** 15 paired
tasks produced **1 discordant pair**. The decision rule (paired sign test, ≥~80% of discordant
pairs) needs ~5 to say anything, so *the test never engaged*. Correctness was 14/15 in both arms —
the same task, failing the same way, on an extra output line rather than a q error — and 5 of the
15 task pairs came back byte-for-byte identical q. That is PLAN-M2 §4's **too-few-discordant-pairs**
case outright, plus its **ceiling** case in substance (§4 defines ceiling as a literal 15/15, which
this did not reach — worth stating precisely, since the whole value of pre-registering degenerate
cases is lost if you then wave at them approximately).

### What transfers

- **"No difference between conditions" and "the instrument has no headroom" are different claims,
  and only the second one was earned.** The temptation is to publish the first — it is a cleaner
  sentence and it is the one the reader expects. Writing tasks that are easy to *verify* selects
  hard for tasks that are easy to *solve*; those are the same tasks. Any A/B on a frontier model
  needs its baseline failure rate established BEFORE the comparison is designed. A pilot of the
  baseline arm alone would have caught this in an hour and cost 15 sessions instead of 50.
- **Decide activation mechanically or not at all.** "Fired" here means the session emitted a
  `Skill` tool call naming the plugin — read off the stream-json log, not judged from prose. This
  mattered immediately: one Part A prompt produced fluent, correct q idioms (`xs where p xs`,
  `a f' b`) with **no skill loaded**, and one Part B task (12) matched its condition-A twin
  without ever invoking the plugin. Eyeballing would have scored both as fires.
- **The measurement environment must be built to be *worse* than the thing it measures.** The
  single control that decided whether this run meant anything was cwd: run from inside the working
  copy and condition A silently inherits `.claude/skills/idiomatic-q/SKILL.md` — approximately the
  subject under test — with no trace in the results. A contaminated null looks exactly like a
  clean null. Generalises past evals: for any A/B where the environment can leak the treatment,
  the control is a property of the *harness*, not of the analysis, and it cannot be checked after
  the fact.
- **Verify the tool policy before trusting the arms are fair.** A smoke run showed condition B's
  `Read` of its own bundled `references/*.md` being permission-denied — the plugin's SKILL.md
  delegates Python→q translation to a sibling file, so the treatment arm was being handicapped
  against its own design by the harness. Caught before the run, zero denials across the 50 recorded
  sessions. **Smoke-test the treatment arm's happy path specifically**; a harness bug that weakens
  the treatment reads as a null result.
- **The formatting contract is part of the instrument, so publish it verbatim.** Un-constrained
  answers arrive as prose plus several alternative snippets carrying `q)` prompts, and "which block
  is the answer" becomes a scorer judgment 30 times over. One fixed contract, identical in both
  arms, naming no idiom under test, moved extraction from judgment to `re.search`. All 30 answers
  obeyed it — which is itself worth knowing about instruction-following at this model tier.
- **Fix the taste-dependent scoring rules in writing BEFORE the pass, and anchor them to an
  artifact.** "No unnecessary temporaries" is pure taste until it is anchored: here, *fails only if
  it introduces a binding the verified reference solution does not need*. Note what that anchoring
  exposed — the run's **entire** margin was one such judgment (task 08, `t:update…from t; show t`),
  and a second defensible reading makes it a tie. Writing the rule down first is what turned a
  result into a caveat instead of a headline.
- **Cost separated the arms even when quality could not.** 2.8× total output tokens, 3.9× median
  per task, for 13/15 tasks of identical or equivalently-scored code. When the primary metric hits
  a ceiling, the secondary metrics are the finding — record them even when you expect the primary
  to carry the article.

### Model failure mode found (relevant to any future skill)

> **[RETRACTED 2026-07-28 — see "M2 correction" below.]** This finding is wrong. `` `p# `` on a
> sorted in-memory table is documented as legitimate and can outperform `` `g# ``; the defect was in
> the task sheet, not in either condition. The paragraph is left standing because this file is a
> log, but do not carry it forward.

On the `aj` fix task, **both** conditions applied `` `p# `` to an **in-memory** quote table.
<https://code.kx.com/q/ref/aj/> gives memory → `` `g# ``, disk → `` `p# ``. Both returned correct
rows, so nothing errored — the wrong-answer-that-runs-clean shape this curriculum's `aj` showcase
exists to teach. **KX's own plugin, loaded and active, did not correct a deviation from KX's own
published guidance.**

Deliberately NOT acted on: PROTOCOL.md permits authoring a skill only if a gap survives, and one
observation from one task in one run is a hypothesis, not a gap. Authoring against it would be
fitting a skill to n=1. Logged here as the seed for a harder task set.

### Governing-doc drift check (new standing step)

Carried in from the last session's observation: the recurring failure here has never been wrong
code — it is documents that were true when written and silently became false, with nothing failing.
Lessons have `make verify`; governing docs had nothing. So the compound step now includes re-reading
SPEC.md and CLAUDE.md against reality (CLAUDE.md updated to match). This pass found and fixed one:
`eval/README.md` told the reader to run Part A "under each condition", which is undefined for
condition A — it has no plugin to activate. It had read as current since the harness was built.

### Independent review pass on the M2 writeup (Codex, adversarial)

Five findings, all accepted. Three were substantive, and two of those are the interesting kind —
the reviewer attacked the *epistemics of the writeup*, not the code.

- **"Your evidence is not auditable from committed artifacts."** The first cut shipped a generated
  `traces.md` summarising session logs that were never committed — so every activation and token
  claim rested on my say-so, in a repo whose entire discipline is that outputs are captured, not
  typed. Fixed by committing all 50 raw stream-json logs (1 MB, 265 K packed) plus the exact prompt
  bytes, and making `traces.md` a *derived* file that `make verify` re-derives and diffs.
  **Generalises: if a claim in your prose came from a run, the run's output belongs in the repo —
  a summary you generated is not evidence, it is a second copy of the claim.**
- **Redacting for publication found a contamination vector the pre-flight had missed.** Rewriting
  absolute paths surfaced `memory_paths.auto` — Claude Code derives a per-cwd auto-memory directory,
  including for the neutral eval directory. It was empty, so nothing leaked. But had that scratch
  directory been reused from an earlier q session, stored memory would have entered *both* arms
  invisibly, and no line in PLAN-M2 §1 would have caught it. **Preparing artifacts for a hostile
  reader is itself a review technique** — it forces you to look at fields you never read.
- **"You changed the denominator after seeing the misses."** Two of twenty trigger prompts referred
  to code the table never supplied, so the model asked for input instead of writing q. I reported
  8/10 *and* an "8/8 on well-formed prompts". The diagnosis is sound; minting the second number is
  not. It is precisely the overfitting the protocol forbids when tuning a trigger against a test
  set — and I would not have accepted it from the plugin's authors. Now 8/10 only, with the two
  items recorded as defective and any repaired set requiring a fresh run.
  **The bias to watch for is not inventing data; it is quietly picking the flattering denominator
  for data you really did collect.**
- **A verification script that only prints is not verification.** `correctness.sh` recomputed the
  correctness column and printed it — while `results.csv` could have said anything. It now compares
  against the committed CSV and exits nonzero on mismatch, and both new checks were **negative
  tested** (corrupt a row, confirm the build fails) rather than assumed. Same lesson as the prose
  checker in M1, one layer up: the check that never fails is indistinguishable from no check.
- **Pre-registered thresholds must be applied to the letter or the deviation stated.** PLAN-M2 §4
  defines the ceiling case as correctness 15/15 in both arms; this run got 14/15 and the writeup
  called it "the ceiling case" flat out. Now stated as "in substance, not to §4's letter", with the
  reason. Pre-registering degenerate cases buys nothing if you then gesture at them approximately.

**Transferable meta-point:** the review found nothing wrong with the q, the harness logic, or the
arithmetic. Every finding was about the *distance between what the artifacts prove and what the
prose claimed*. For an evaluation, that distance IS the defect class — point the reviewer at it
explicitly rather than at the code.

## M2-close — governing-doc reconciliation (2026-07-28)

First run of the "re-read SPEC.md and CLAUDE.md against reality" step that the M2 entry added to
the compound duty. It found three defects, and the most instructive thing about them is that **all
three were created or exposed by shipping M2 itself** — the milestone that adds a doc-drift check
is the milestone whose own output invalidates the docs.

- **M5 lost its subject the moment the verdict landed.** SPEC read "skill hardened from eval
  findings; marketplace submission; v1 tag" and CLAUDE.md said "marketplace metadata is part of M5,
  not an afterthought" — while the verdict authored no skill. RELEASE-CHECKLIST.md carried a
  four-item "M5 only (marketplace submission)" block for an artifact that will never exist.
  **Nothing failed, and the M2 compound step missed it**: I checked SPEC's eval-gate section (which
  was accurate, because it describes the *design*) and never opened the milestone list, which is
  where the *consequences* live. Generalises: when a result invalidates a plan, the stale text is
  rarely in the section describing the thing you just did — it is downstream, in whatever was
  supposed to consume the result.
  M5 is now curriculum v1 + `eval/harness/` packaged as a reusable plugin-A/B artifact. That choice
  also serves objective 1's actual words — "skill authoring AND EVALUATION as a *transferable
  discipline*" — better than a marketplace listing would have.
- **SPEC and CLAUDE.md disagreed about what to build next, and had for weeks.** SPEC: M3 = J
  laboratory, M4 = q core. CLAUDE.md build order: Part II lessons, then the Part I compression
  pass. Three Part II lessons had shipped against the CLAUDE.md order while SPEC said otherwise,
  and no check could have caught it because both files were internally consistent. Diagnosis that
  settled it: SPEC's ordering **predates J's demotion** from co-star to illustrative laboratory,
  and it contradicts the Q-first non-negotiable (a J prelude cannot be extended before its q side
  runs). Swapped SPEC to match; articles moved with their milestones so the series still publishes
  in order. **Two docs can each be self-consistent and still contradict each other — "does it
  verify" and "do the contracts agree" are different questions, and only the first is mechanised.**
- **Constraint docs should not cite article NUMBERS.** `docs/licensing-notes.md` pinned the Clause 9
  benchmark prohibition to "Article 5" in four places; renumbering silently pointed a real legal
  constraint at the wrong article. Now cited by subject ("the as-of-join article"). Transferable:
  **reference stable identifiers, not positional ones, in any doc whose job is to constrain future
  work** — position is exactly what gets reorganised.

Also recorded, since it was found by CI rather than by reading: **`q-verify.yml` still does not
exist**, so `verify-q`, `verify-eval` and the new `verify-eval-run` run on one laptop only. The
checks protecting the published eval numbers are not enforced anywhere a reviewer can see them.
Noted in CLAUDE.md build order §5 with the requirement that it run `make verify`, not `verify-q`.

## M2 correction — the `p#` finding was wrong, and the repo already said so (2026-07-28)

The M2 entry above reports, as its headline model-failure finding, that both eval conditions applied
`` `p# `` to an in-memory table where "KX's own documentation" prescribes `` `g# ``, and that KX's
plugin failed to correct a deviation from KX's own guidance. **Retracted.** Corrected in
`eval/verdict.md`, `eval/runs/notes.md`, and articles 3 and 5; the entry above is left standing
because this file is a log, and this section is the correction.

<https://code.kx.com/q/ref/set-attribute/>: *"If the data can be sorted such that `p` can be set, it
effects better speedups than grouped, both on disk and in memory."* Both candidates ran
`` `sym`time xasc quote `` before setting the attribute, which is exactly that precondition. `` `p# ``
was defensible, possibly faster. The models were not wrong; **my task sheet was too narrow**, naming
one attribute as though it were the only correct answer.

Scores unchanged: item 5 is scored against the task's own cited idiom, that rule was fixed before
the pass, and it applies symmetrically to both arms — so the retraction touches the interpretation
and never touched the comparison.

### Why this one is worth more than the finding it replaces

- **The correction was already in this repository, in writing, three days before the eval was
  scored.** `docs/licensing-notes.md` §C is a claim-by-claim audit of the repo's own draft skill
  against code.kx.com, and its **CORRECTED claim 5** says verbatim: *"`p#` also works in memory and
  can outperform `g#` when values are contiguous. It is not useless in memory."* The scoring pass
  cited the `aj` page, drew the opposite conclusion, and never opened either the sibling
  `set-attribute` page or the repo's own audit of precisely that claim. **Prior work does not
  protect you if nothing routes you back to it.** A verified finding filed in a doc nobody re-reads
  is indistinguishable from a finding never made.
- **The failure mode is motivated reasoning, not carelessness.** This was the one *interesting*
  result in an otherwise null eval — the single paragraph that made a negative writeup feel like it
  had teeth. That is exactly the claim that should have been attacked hardest, and instead it got
  the least scrutiny of anything in the verdict. **When a result flatters the thesis, treat it as
  the highest-priority thing to try to kill.** Two adversarial review passes over the M2 work did
  not catch it either; both reviewed what the artifacts proved versus what the prose claimed, and
  this was a claim about the *outside world* that no artifact in the repo could contradict.
- **"Cite a published source" is weaker than it sounds when a topic spans pages.** PROTOCOL.md's
  defence against evaluator drift is that every checklist item be justifiable against a published
  source. It was — the `aj` page really does say memory→`g#`, disk→`p#`. One page, cited accurately,
  still produced a wrong conclusion because the qualifying sentence lives on a sibling page.
  Sharpen the rule: **cite the source, then look for the page that contradicts it.**
- Instrument note carried forward: any future task set must either widen task 15 to accept `` `p# ``
  on a sorted table, or state why not.

## M3 — q CI live; and a guess that forged its own evidence (2026-07-29)

`q-verify.yml` is green on its first real run. `make verify` — J twins, q lessons, the `aj` golden,
the eval reference solutions, **and** the two eval-run checks — now executes on a GitHub runner
rather than only on the author's laptop. The numbers published in Article 3 are, for the first
time, enforced somewhere a reader can inspect.

### The expensive mistake: I confirmed my own guess with an artifact my guess created

The first revision demanded a second secret, `KX_INSTALL_TOKEN`. That requirement was **inferred**
from a phrase in `docs/licensing-notes.md` — "authenticated curl script with an OAuth bearer token"
— and never measured. To sanity-check it I curled the install URL, got **401**, and treated that as
confirmation.

The 401 came from **my own mistyped URL**, missing the `/install_kdb/~latest~/` segment. The real
endpoint returns 200 with no credential at all, as does every payload the installer fetches, and
the installer's own `download_file()` uses a bare `curl --fail -Lo` with no auth header. Three
independent signals, all available before I wrote a line of YAML, all pointing the other way.

**A guess that produces a plausible error code is the most expensive kind**, because the error
looks like evidence. The 401 did not test my hypothesis — it tested my typing, and I read the
result as though it had tested the hypothesis. Transferable rule: **when a check appears to confirm
what you already believed, verify the check itself before the conclusion.** Cheap here (one wrong
secret, one wasted round trip); the same shape retracted a published finding two days earlier,
where a correctly-cited page produced a wrong conclusion because I never looked for the page that
would contradict it. Twice in one week, same failure, different costume: **seeking confirmation
where the confirmation is easy to manufacture.**

### Reading the installer was worth more than the token fix

`setup_telemetry()` runs q against the licence and tests `.z.l[4]` for `"tld"`. If it matches,
`KX_UPLOAD_TELEMETRY=YES` is set **before** control reaches the non-interactive branch that would
otherwise default it to `NO`. The author declined telemetry locally, and `docs/licensing-notes.md`
records that as a decision — but on CI it would have been decided by whatever a licence flag
happens to say on a given day.

Now forced to `NO` after install and asserted, so a recorded decision stays a decision.
**Generalises: a policy you chose interactively is not in force anywhere you automated; a
non-interactive path is a different code path, and vendor installers often decide defaults for
you there.**

### Two smaller things worth keeping

- **Verify the log, not the tick.** The run was checked for leakage before being called clean:
  zero author identifiers, no kdb+ startup banner (which carries serial/email/host), `.z.K`
  printing `5f` alone. On a public repo, "the job passed" and "the job was safe" are different
  questions.
- **The loud-failure design paid off immediately.** Merging the first revision without secrets
  produced a red `main` with `::error::secret KX_B64LIC is not set` — which is how the missing
  secret got noticed at all. The alternative (`if: secrets…` skip) would have shown green while
  verifying nothing, which is precisely the `j-verify` stub defect recorded above.

## M3 — lesson 04 (attributes); and a true claim with a demonstration that didn't prove it (2026-07-29)

Lesson 04 (attributes & sort discipline) lands, closing the last Part II prerequisite before the
`aj` showcase lesson. `make verify` gains a sixth leg, `verify-prose`.

### The finding the lesson is built on

`aj`'s correctness comes from **row order**, not from the attribute. Four joins over one dataset:
unsorted is wrong (98.5) with *and* without `` `g# ``; sorted is right (99.1) with *and* without it.
The attribute is the speed decision; the sort is the correctness decision, and q reports nothing
when you get the second one wrong. Two things sharpen it: `xasc` attributes only the **first** sort
column, because "ascending within groups of another column" is precisely the property q has no
attribute for — and it is the only property `aj` needs. And the failure is **partial**: symbols with
one quote in the window are right regardless, so a mis-sorted quote table yields output that looks
mostly fine. That is why the bug ships.

### The mistake worth recording: the claim was true, the demonstration was not

The 2×2's "sorted, no attribute" cell joined against a table built with `` `sym`time xasc ``, which
stamps `` `s# `` on the sort column — as the same lesson demonstrates two sections earlier. So the
cell labelled "no attribute at all" had one, and the comparison did not isolate the variable it
claimed to isolate. The conclusion was still correct (a stripped-and-sorted table joins correctly;
that had been checked while drafting) — but the evidence printed under it did not establish it.

This is a distinct failure from the `p#` retraction and the forged 401, and worth naming separately:
not a wrong claim, and not manufactured confirmation, but **a right claim resting on a demonstration
that doesn't support it**. It is harder to catch precisely because verification passes — every
output was real, captured, and correctly transcribed; `make verify` was green; the prose checker was
green. Nothing mechanical could see it, because the defect was in what the arrangement *implied*,
not in any output. Transferable rule: **when a demonstration exists to isolate a variable, verify
that it actually isolates it** — a controlled comparison is a claim about the setup, and setups are
where the assumption hides. Found by Codex review, not by any gate in this repo.

### `verify-prose`: the lesson-03 thread, finished

Lesson 03's entry recorded the gap — `make verify` proves lesson *files* run and says nothing about
whether the outputs pasted into the narrative came from them — and pre-registered promoting the
check to a `make` target at the fourth lesson. Done: `tools/check-lesson-outputs.py` re-runs each
lesson's sources and requires every unlabelled block to appear as a contiguous run of the fresh
capture, **in execution order** (which also catches genuine outputs shown out of the order they ran).

Three things learned building it:

- **It passed on the first run, which is not evidence.** Same shape as the 401. So the check was
  checked: a one-digit corruption fires 2 `NOT IN CAPTURE`, swapping two genuine blocks fires
  `OUT OF ORDER`, and it extracts **49** blocks (1 / 8 / 22 / 18 across lessons 01–04) rather than
  trivially passing on zero. A verifier that has never been observed to fail has not been observed
  at all. — *That 49 was 47 when this entry was first written, and went stale within the hour when
  the review fix added two blocks. Counts in prose are the thing this file keeps warning about;
  re-measure them at the moment of the commit that publishes them.*
- **Exit code is not sufficient.** The first version failed only on a nonzero return code and
  discarded stderr — so a lesson could report an error on stderr, exit 0, and still be reported OK.
  `verify-eval` already guards this exact case in the Makefile ("error masked by exit 0"); the new
  gate did not, until adversarial review pointed at it. **When a repo has already written down a
  failure mode, new code is the first place to check for it, not the last.**
- **Known gap, stated rather than scoped around.** This checks output *blocks*. Outputs written as
  trailing `/ 2f` comments inside ` ```q ` blocks remain unverified, and lesson 01 is written almost
  entirely that way — it has exactly **one** output block. Recorded in the Makefile so the gate's
  coverage is not mistaken for its scope.

The two blocks CLAUDE.md exempts needed no special case: both are language-tagged, and the tag is
already the marker.

### `p#` — the retraction held under pressure

The `aj` page prescribes `` `g# `` in memory and `` `p# `` on disk; the set-attribute page says
parted *"effects better speedups than grouped, both on disk and in memory"* when the data can be
sorted so `p` can be set. The lesson ships `` `g# `` as the default and says plainly that naming
either as *the* answer on one page's strength is what produced the retracted finding. All quoted
vendor text was grepped from the raw pages rather than taken from a fetch summary — one "quote" the
summarizer produced ("on disk, the `g#` attribute does not help") turned out to be verbatim, but
only checking established that.

### Closing the inline-claim gap — and why "it appears in the output" is not verification

The `verify-prose` entry above recorded a known gap: the gate checked output *blocks*, while
lesson 01 states nearly all of its outputs as trailing `/ 2f` comments and so was almost
uncovered (1 block against 18 such claims). Closed on 2026-07-29 — **49 blocks and 37 inline
claims** now checked across lessons 01–04.

Two things worth keeping from building it.

**The obvious design was the wrong one.** The natural approach is to execute the README's own q
lines, since they are complete expressions. Prototyping killed it: lessons legitimately contain
```q blocks that *error by design* (lesson 01's fork parse failure, lesson 04's `s-fail`/`u-fail`
demos), so running the README aborts. And lesson 01 deliberately re-shows an earlier result out of
execution order — `10` again, when `(+/)` is introduced as the mechanism under `sum` — so
order-checking inline claims would flag good writing. **A verifier's design constraints come from
the prose it verifies, not from the data model that looks tidiest.**

**The first working version passed its own negative control by accident.** Membership testing —
"the claimed value appears somewhere in the capture" — caught 2 of 3 deliberate corruptions. The
one it missed: flipping lesson 02's `type d` annotation from `99h` to `98h`, which passes because
`98h` is a *real value elsewhere in that same lesson*. A wrong claim that collides with a genuine
value is exactly the wrong claim a reader would believe. Fixed by re-**evaluating** each claimed
expression, appended to the lesson's own verify-clean q source so the narrative's state (`d`, `t`,
`kt`, `r`, `w`) already exists; the deliberate error demos are never appended because their
comments are prose, not values.

Generalises past this repo: **a containment check is not an equality check.** "The expected value
appears in the output" is the weaker assertion, it is the one that is easier to write, and it
fails precisely on the inputs where the two differ — which is to say, on the interesting ones.
Three corruptions is also the smallest control set that could have exposed this; one would have
passed and been called proof.

Also bumped `actions/checkout` v4 → v7 in both workflows (v4 runs on deprecated Node 20). Checked
first that v7's fork-PR hardening applies to `pull_request_target`/`workflow_run`, which neither
workflow uses — `j-verify` is `pull_request`, `q-verify` is schedule/dispatch/push-to-main.
