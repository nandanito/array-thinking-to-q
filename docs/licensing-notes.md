# Licensing & tooling notes — TASK ZERO (research pass)

> Status: research complete for the parts that need no account. Dated 2026-07-22.
> Quotes are kept short; most items are summarized. Secondary (non-KX) sources are labeled as such.
>
> **UPDATE 2026-07-24:** the owner registered and installed, and the actual CE license is now
> public. The license has been READ (KX Community Edition License Agreement v1.1, 27 Aug 2025,
> https://kx.com/legal/community-edition-license-agreement-08-27/). This RESOLVED the two
> highest-priority open items (commercial grant, benchmark clause) — **both came back restrictive.**
> See "License terms — CONFIRMED" below; superseded pre-read speculation is struck through.

This doc covers the three TASK ZERO reads: (A) KX's official Claude Code plugins + MCP servers,
(B) the KDB-X CE license/download flow incl. the benchmark clause, (C) the SKILL.md claim audit.
Contradictions with SPEC.md are flagged here and recorded in `docs/COMPOUND.md` (not silently
patched into the spec).

---

## A. KX official Claude Code plugins & MCP servers

**The marketplace.** KX ships an open-source Claude Code plugin marketplace, `KxSystems/kx-skills`
(Apache-2.0), announced in "Teaching Claude Code to Speak KX." Install:
`/plugin marketplace add KxSystems/kx-skills`. Plugins are folders of markdown Skills that
auto-load; the knowledge skills need no external deps.
- Repo: https://github.com/KxSystems/kx-skills
- Blog: https://kx.com/blog/teaching-claude-code-to-speak-kx-open-source-plugins-for-q-pykx-kdb-x-and-kdb-ai/

**The plugins** (blog announces 4; repo now lists a 5th, `kdbie-knowledge`, for KX Insights Enterprise):
- **`q-knowledge`** — idiomatic q, qSQL, IPC, common errors, Python→q. Ships a `/qlint-snippet`
  command. `/plugin install q-knowledge@kx-skills`.
- **`pykx-knowledge`** — PyKX Column API, IPC, type conversion, on-disk DB management.
- **`kdbx-knowledge`** — KDB-X module system (`use`, not `\l`), AI libs (HNSW/BM25/TSS/DTW), GPU,
  `aimeta`, DB Service.
- **`kdbai-knowledge`** — KDB.AI schema, hybrid search, time-series similarity, reranking.
- Source: https://github.com/KxSystems/kx-skills and the q SKILL:
  https://raw.githubusercontent.com/KxSystems/kx-skills/main/plugins/q-knowledge/skills/q/SKILL.md

**qlint.** Integrated only in `q-knowledge`, via the optional `/qlint-snippet` executable skill —
it shells out to KX qlint and reports findings before code reaches you. **Not bundled**: needs `q`
on PATH (or `Q` env var) plus `QLINT_DIR` pointing at `qlint.q_`. Emits a table (label, errorClass,
description, problemText, startLine/Col…); exit 0 clean / 1 findings / 2 misconfig. qlint rules
are static checks like `UNDECLARED_VAR`, `UNPARENTHESIZED_JOIN`, `RESERVED_NAME`, `UNREACHABLE_CODE`.
- qlint docs: https://code.kx.com/developer/libraries/linter/ , https://code.kx.com/analyst/linting/

**MCP servers** (two, both separate from the plugins, both Apache-2.0, Python/`uv`):
- **`kdb-x-mcp-server`** — natural-language querying of a KDB-X/kdb+ service. Tools:
  `kdbx_run_sql_query`, `kdbx_similarity_search`, `kdbx_hybrid_search` (similarity needs KDB-X ≥0.1.2).
  Env: `KDBX_DB_HOST/PORT/USERNAME/PASSWORD/TLS`. Transports: streamable-http (default), stdio.
  https://github.com/KxSystems/kdb-x-mcp-server
- **`kdbai-mcp-server`** — query/vector-search against a KDB.AI endpoint.
  https://github.com/KxSystems/kdbai-mcp-server
- Both are **data-query tools**; neither teaches the q language.

**Does anything coach a NEWCOMER out of imperative habits? — the objective-3 question.**
No official KX offering does human-facing pedagogy. The plugins are reference knowledge that make
*Claude* emit correct idiomatic q for an already-competent user; the MCP servers only query data.
- **Nuance that sharpens the eval (and partly challenges SPEC.md's hypothesis):** the `q-knowledge`
  SKILL *does* encode the exact anti-imperative rules this repo cares about — e.g. "Vectorize, don't
  loop", "Avoid `do[]`/`while[]`. Use Over (`/`) and Scan (`\`)", "Prefer `(+/)x` over a `{r+:x}each`
  accumulator" — but as **one-line model-steering reminders that assume the reader already knows
  why**, not a narrative that walks a human through the paradigm shift. SPEC.md §objective-3 says
  "nothing there coaches a newcomer OUT of imperative habits"; more precisely, *the anti-loop rules
  DO exist in KX's plugin — what's absent is the human WHY-narrative.* The learner-narrative niche
  survives; the gap is pedagogy, not the mere presence of idiom rules. → recorded in COMPOUND.md.
- **Consequence for the M2 eval:** the "subject under test" per SPEC/CLAUDE is concretely
  `q-knowledge@kx-skills` (baseline = no plugin). This is now a named, installable artifact.

Open (needs a repo check, not an account): `kx-skills` has **no pinned version/tag** in README/blog
— TASK ZERO's "record the exact version" means pinning a commit SHA. MCP server versions uncaptured.

---

## B. KDB-X Community Edition — download, license, phone-home, benchmark clause

**Download / key / install.** Signup is at the **KX Developer Center**
(https://developer.kx.com/products/kdb-x); the install guide is public
(https://code.kx.com/kdb-x/get_started/kdb-x-install.html). After signup you receive a welcome
email with a base64 `kc.lic` key (commercial uses `k4.lic`). Install is an **authenticated curl
script** with an OAuth bearer token that passes the license inline
(`… install_kdb.sh --b64lic <KEY>`); it validates online during install. An `--offline` air-gapped
bundle path exists.

**Phone-home — CONFIRMED the license RESERVES it (SPEC's concern stands).** Two separate things:
- **License validation (MANDATORY, no opt-out).** License Clause 4: *"The Software may periodically
  communicate with a license manager application running on a KX server by sending usage information
  to it to confirm that you have a valid license."* So the license explicitly reserves a periodic
  runtime phone-home. My pre-read guess that CE "runs fully offline" was based on a secondary blog
  and is ~~superseded~~ — the license permits a validation call, even if observed runtime behavior
  is quieter. **Consequence: SPEC's "fatal for any future offline verification" concern is VALID.**
  CI runners with egress are fine; treat offline/air-gapped verification as at-risk (an `--offline`
  install bundle exists, but the license still reserves periodic validation).
- **Usage telemetry (OPT-IN, separate).** The installer prompt is a *distinct* consent for analytics
  (identifiers, performance metrics, "potential interest in our products"). Recommend declining;
  it's reversible and unrelated to the mandatory license check. `KX_UPLOAD_TELEMETRY=YES` enables it.
  Telemetry docs: https://code.kx.com/kdb-x/releases/telemetry.html ; Telemetry Data Statement:
  https://kx.com/legal/kdb-x-telemetry-data-statement-07-26

**Resource limits** (public usage-restrictions page corroborates SPEC's 16/4/8/24, with caveats):
- RAM **16 GB** — confirmed (license text; `.Q.lim` mem = 16 GiB).
- Secondary threads **4** — confirmed.
- Connections — **16**, confirmed on the real install (`.Q.lim` conns=16), matching the KX doc
  page. ~~Pre-read guess said 8 at runtime, "treat 8 as operative"~~ — SUPERSEDED 2026-07-24: the
  secondary blog was wrong and the doc page was right.
- **24 cores is an aggregate *license* cap across all instances, not a per-process runtime limit**
  (`.Q.lim` cores=0W). SPEC lists it among runtime limits — it's a legal ceiling. Minor flag.
- Also: single instance only; multi-process OK if aggregate RAM <16 GB. ~~A 12-month key period is
  reported~~ — SUPERSEDED 2026-07-24: the issued CE key's install banner reads **NONEXPIRE**. The
  *agreement* is separately terminable at will by KX (Clause 10); that is not a key expiry.
- Public restrictions page: https://code.kx.com/insights/1.18/licensing/usage-restrictions.html
- Runtime `.Q.lim` figures (secondary): https://dataintellect.com/blog/running-torq-with-kdb-x-community-edition/

### License terms — CONFIRMED (read 2026-07-24)
Source: KX Community Edition License Agreement **v1.1, 27 Aug 2025**,
https://kx.com/legal/community-edition-license-agreement-08-27/ — this is the operative text the
owner accepted at install. (My pre-read speculation about a "gated GA EULA that might supersede the
stricter preview" is superseded: the stricter text IS the license. The earlier July-2025 preview
concern was correct.)

- **Commercial use — NO. Personal / internal-business only.** Clause 2.1 grants a "limited,
  non-transferable, non-exclusive license, without right of sublicense … solely for the Permitted
  Use"; Attachment A: *"Permitted Use means personal or internal business use."* You may **not**
  "sell, rent, lease, license, sublicense … publish, transfer, distribute or otherwise make
  available to any third party" the Software (2.1), nor "build or offer a product or service … which
  competes with, or provides the same or similar features" (2.1.xi); revenue-generating bundling
  needs an **OEM license** (2.2). → **This contradicts SPEC.md's "free personal+commercial per KX
  marketing" (line 126). CLAUDE.md rule 4 resolves to: DO NOT claim commercial-friendliness.**
  The project itself is fine — it is *personal use* that distributes lessons/prose, not the Software
  — but no README/article may say "free for commercial use."
- **Benchmark / performance publication — PROHIBITED without prior written consent.** Clause 9
  (Confidentiality): *"You will not disclose any benchmark, test or performance information or any
  report which contains a competitive analysis regarding the Software to any third party except as
  explicitly authorized in advance by us in writing."* → **This is the DeWitt-style clause, and it
  is live in KDB-X CE, not just the old Personal Edition.** Direct hit on **the as-of-join article**
  (Article 4 since the 2026-07-28 renumber): it may NOT publish KDB-X performance
  numbers/benchmarks without written KX authorization. The `aj` **showcase
  is unaffected** — its golden file asserts *correctness/output*, not performance. That article must
  reframe to design/semantics/co-design (SPEC already leans this way) OR obtain written consent.
- **Liability cap US$100** (Clause 7); **governing law New York** (Clause 15).
- **Term: indefinite, terminable at-will by KX on email/website notice** (Clause 10) — NOT the fixed
  12-month I guessed (that figure, if real, is a `kc.lic` key expiry, separate from the agreement).
- **Resource limits are NOT in the license text** — they live in the runtime (`.Q.lim`) and the
  public usage-restrictions page. So 16GB/4-thread/etc. are technical/enforced, not contractual here.
- Old, DIFFERENT kdb+ Personal Edition EULA (do not use as CE terms):
  https://kx.com/legal/kdb-free-personal-edition-license-agreement/

**Platform** (confirms SPEC): Linux x86_64/ARM, macOS Intel + Apple Silicon (install expects
Homebrew), Windows **WSL-only** — native Windows not supported.
https://code.kx.com/kdb-x/get_started/kdb-x-install.html

**KDB-X CE vs. old kdb+ Personal Edition** — both still exist, different licenses. Personal Edition:
non-commercial, local-only, phones home, carries the §1.3 benchmark ban (SPEC already rejects it,
line 138). KDB-X CE (GA 2025-11-19): cloud-deployable, next-gen engine.

> **CORRECTED 2026-07-28.** This line previously ended "commercial permitted within limits,
> cloud-deployable, **offline runtime**, next-gen engine" — pre-read speculation that survived the
> license read and sat here contradicting the CONFIRMED section *above it in this same file*.
> Both struck claims are false: Clause 2.1 + Attachment A restrict use to **personal or internal
> business** (no commercial grant), and Clause 4 **reserves a periodic license-validation call**
> (no guaranteed offline runtime). Leaving a stale summary next to the correct finding is how a
> reader gets the wrong answer from a document that also contains the right one — the same defect
> class as the `p#` retraction in docs/COMPOUND.md.

---

## C. SKILL.md q-gotchas claim audit (vs. code.kx.com)

Audited every technical claim in `.claude/skills/idiomatic-q/SKILL.md`. **9 VERIFIED, 2 CORRECTED**
— both corrections are in the `aj` cluster. SKILL.md is a conditional stub and was left unedited;
these corrections should be folded in *if and when* the skill is built (M2+).

| # | Claim (abbrev.) | Verdict | Source |
|---|---|---|---|
| 1 | right-to-left, no precedence; `2*3+1`=8 | VERIFIED | code.kx.com/q/basics/syntax/ |
| 2 | `til n` is 0..n-1 | VERIFIED | code.kx.com/q/ref/til/ |
| 3 | table = flip of column dict; keyed table IS a dict | VERIFIED | code.kx.com/q4m3/14_Introduction_to_Kdb+/ |
| 4 | **aj join columns** | **CORRECTED** | code.kx.com/q/ref/aj/ |
| 5 | **attributes by regime (g#/p#)** | **CORRECTED** | code.kx.com/q/ref/aj/ , /ref/set-attribute/ |
| 6 | unsorted quote table → silently wrong aj | VERIFIED | code.kx.com/q/ref/aj/ |
| 7 | `aj0` uses quote-side time | VERIFIED | code.kx.com/q/ref/aj/ |
| 8 | symbols vs strings distinct; qSQL cols are symbols | VERIFIED | code.kx.com/q/basics/datatypes/ , /basics/funsql/ |
| 9 | no tacit trains; explicit composition (`'[f;g]`) | VERIFIED | code.kx.com/q/ref/compose/ |
| 10 | no true multidimensional arrays (nested lists) | VERIFIED | code.kx.com/q4m3/3_Lists/ |
| 11 | `do`/`while` exist but unidiomatic | VERIFIED | code.kx.com/q/ref/do/ , /ref/while/ |

**CORRECTION — Claim 4 (aj join columns).** SKILL.md says the join columns "are the columns COMMON
to both tables — not necessarily the leading ones." Imprecise: the caller **passes them explicitly**
as the first arg (a symbol vector); the doc requires them "common to t1 and t2, and of matching
type." Equality/as-of mechanics were right (all but last by equality; last as-of ≤).
- Corrected: *"aj join columns are the ones you pass as the first argument (a symbol vector); they
  must exist in both tables with matching type. All but the last match by equality; the last matches
  as-of (≤), taking the prevailing/most-recent value."*

**CORRECTION — Claim 5 (`p#` in memory).** SKILL.md says `p#` "does nothing useful in memory."
Wrong: the set-attribute page states parted works in memory too and can beat grouped — "If the data
can be sorted such that `p` can be set, it effects better speedups than grouped, both on disk and in
memory." `g#`-on-sym is still the standard in-memory aj prescription and `p#` the on-disk one, but
`p#` is not useless in memory.
- Corrected: *"`g#` on sym is the standard in-memory aj prescription (time sorted within sym); `p#`
  is the on-disk prescription — but `p#` also works in memory and can outperform `g#` when values
  are contiguous. It is not useless in memory."*

Claim-6 nuance: the doc states the mechanism ("last (in row order) matching record") and the
time-sorted-within-sym requirement; it does not itself print a "silently wrong" warning — the silent
failure is the correct *consequence*, which SKILL.md states correctly.

---

## Consolidated open questions

RESOLVED 2026-07-24 by reading the license (see "License terms — CONFIRMED"):
- ~~[EULA] benchmark-publication clause?~~ → **YES, Clause 9. The as-of-join article is blocked from publishing
  performance numbers without written KX consent.**
- ~~[EULA] unqualified commercial use?~~ → **NO. Personal / internal-business only (Clause 2.1 /
  Attachment A). Drop any commercial-friendliness claim.**
- ~~[install] runtime phone-home?~~ → **License RESERVES periodic validation (Clause 4); treat
  offline verification as at-risk.**

RESOLVED 2026-07-24 by the install banner:
- ~~[install] key expiry / 12-month?~~ → **NONEXPIRE** — the CE key does not expire (banner).
- ~~[version] KDB-X build~~ → **KDB-X 5.0, build 2026.07.23, COMMUNITY** — pinned in
  `docs/toolchain.md` (serial/email/host redacted; repo is public).

RESOLVED 2026-07-24:
- ~~[install] enforced caps / 8-vs-16 conns~~ → `.Q.lim[]` = **mem 16384MB · threads 4 · conns 16 ·
  cores 0W**. The connections limit is **16** (the doc page was right; the secondary "runtime = 8"
  blog was wrong). Cores unlimited per-process; 24 is an aggregate license cap. Pinned in toolchain.md.
- ~~[version] `kx-skills` SHA~~ → **`8b7040f769c6653db67b063aa34c944729e8857e`** (pinned in toolchain.md).
- ~~[decision] the as-of-join article~~ → **DECIDED (provisional): easier path — design/semantics framing, NO
  KDB-X performance numbers, so no KX authorization needed now. Revisit later if wanted.**

No open licensing/tooling items remain for Task Zero. Remaining setup is operational (install J 9.7).
