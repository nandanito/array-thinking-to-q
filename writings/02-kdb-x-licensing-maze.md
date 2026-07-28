# Running q in a public repo: the KDB-X licensing maze

*Article 2 of 6 — draft. Reports the M1 licensing read. Full notes:
[`docs/licensing-notes.md`](../docs/licensing-notes.md).*

> **Not legal advice.** I am a programmer who read a license carefully and wrote down what it says,
> with clause numbers so you can check me. If money or a company depends on the answer, ask a
> lawyer, not a blog. Quotes are kept to short identifying fragments; the agreement is public and
> linked, and it is the authority — not this page.

---

I wanted to build a public teaching repository where every q example actually runs, with CI to
prove it. That is a modest goal. It took a full day of reading before I could write the first line
of the Makefile, and the reading changed the design in four separate places.

This is what I found, why the order I found it in mattered, and the two moments where a source I
trusted turned out to be wrong.

## The rule that saved the project: read the license first

My spec had a task numbered **zero**, ahead of all engineering: read the actual license text
bundled with the actual download, find the benchmark clause if one exists, and record the exact
version as the pinned known-good build.

I set that rule for a slightly different reason than the one it ended up serving. I expected to be
*reassured* — to confirm the free tier was fine for what I was doing and move on. Instead, two of
the highest-priority questions came back restrictive, and one of them took an article I had already
planned and made it unwritable as planned.

Had I written the CI first, I would have built the wrong CI. Had I written the README first, I
would have published a claim that is false.

## Finding 1: my own spec had it backwards on commercial use

My spec said, in writing, that the community edition was free for personal *and commercial* use.
I had taken that from marketing copy. The operative agreement is the [KX Community Edition License
Agreement](https://kx.com/legal/community-edition-license-agreement-08-27/) (v1.1, 27 Aug 2025),
and it does not say that.

Clause 2.1 grants a "limited, non-transferable, non-exclusive license, without right of sublicense
… solely for the Permitted Use", and Attachment A defines Permitted Use as **"personal or internal
business use."** The same clause prohibits making the software available to third parties, and
2.1.xi prohibits building a product or service that "competes with, or provides the same or similar
features". Revenue-generating bundling needs a separate OEM license (2.2).

So the governing rule I adopted, and put in the repo's contributor instructions as a
non-negotiable, is blunt: **no commercial-friendliness claims about KDB-X CE, ever.**

Worth being precise about what this does *not* mean. It doesn't threaten the project. I am a
personal user distributing *lessons* — prose and my own q snippets — not the software. The
constraint is on what I may **say**, and it binds the README and every article including this one.

The general form is worth stealing: **your spec's assumptions about a license are a claim like any
other, and they degrade silently.** Mine sat there looking authoritative for weeks. Nothing was
going to fail; a reader was just going to be misinformed.

## Finding 2: the benchmark clause is real, and it killed the article I wanted to write

This is the one that changed the plan.

Clause 9 (Confidentiality) says you will not disclose "any benchmark, test or performance
information or any report which contains a competitive analysis" regarding the software to a third
party without prior written authorization.

That is a *DeWitt clause* — the database industry's long-standing tradition of contractually
forbidding published benchmarks, named for the researcher whose comparative work provoked the first
one — and it is **live in the community edition**, not just an artifact of the older Personal
Edition.

I had an article planned about the as-of join, and my instinct for it was the obvious one: show
that this thing is *fast*, with numbers. That article cannot be written. Not "is risky" — cannot,
without prior written consent I have not sought.

What surprised me is that killing it made it better. The speed framing was lazy anyway: as-of joins
now exist in pandas `merge_asof`, Polars, DuckDB, QuestDB and ClickHouse, so "the fast one" was
never really the story. The honest story is **co-design** — what changes when the language and the
storage engine are built around one primitive — and that argument needs no numbers at all. The
constraint forced a better article.

One thing the clause does *not* touch: the repo's `aj` showcase asserts **correctness**. Its golden
file pins output, never timing. That distinction is what lets the technical material survive intact.

## Finding 3: it phones home, and that shapes your CI

Two separate mechanisms, and conflating them is easy:

- **License validation — mandatory.** Clause 4 reserves that the software "may periodically
  communicate with a license manager application running on a KX server". No opt-out. Whatever the
  observed runtime behaviour, the license *reserves* the call.
- **Usage telemetry — opt-in and separate.** A distinct consent prompt at install, covering
  analytics and "potential interest in our products". Declinable, reversible, unrelated to the
  license check. I declined it.

The consequence is architectural. **Air-gapped or offline verification is at risk**, so I stopped
planning for it. CI runners with network egress are fine.

## What all of that did to the build

The design that fell out is asymmetric, and the asymmetry is the point:

| | J | q / KDB-X CE |
|---|---|---|
| License | GPLv3 | proprietary, key required |
| CI | **blocking on every PR** | author-side, nightly/manual, trusted branches only |
| Key handling | none needed | repo secret; failures notify, never block |

**J is the only green check in this repository that depends on nobody's commercial terms.** That is
not a statement about J's merits — it is a structural fact about which check can run on an untrusted
pull request from a stranger.

And the corresponding constraint on q: a fork cannot run the q suite, because a fork does not have
my key and I am not going to hand one out. Every q lesson is verified locally by me before it
merges. If that sounds unsatisfying — it is. It is what the terms permit.

Other operational residue, in case it saves you the reading:

- **Windows is WSL-only.** Not supported natively.
- The key I received is marked non-expiring; the agreement is nonetheless **terminable at will** by
  KX on notice (Clause 10). Liability is capped at US$100 (Clause 7); governing law is New York
  (Clause 15).
- Resource caps live in the *runtime*, not the license text: `.Q.lim` reports 16 GB memory, 4
  secondary threads, 16 connections. The 24-core figure quoted around the web is an aggregate
  **license** ceiling, not a per-process limit.
- The older kdb+ Personal Edition still exists and is a **different agreement**. Do not read one as
  evidence about the other. I nearly did.

## The two times a secondary source lost to the primary text

Both worth recording, because they are the same mistake in different costumes.

**A community blog said the community edition runs fully offline.** I believed it, and softened my
spec's risk flag on that authority. Clause 4 then said otherwise in plain language. The blog was
describing *observed behaviour*; the license describes *reserved rights*, and those are not the
same claim. When they disagree, the license wins — it is the thing that binds you.

**A secondary source said 8 concurrent connections; KX's own docs said 16.** I initially recorded 8
as operative, on the theory that the more conservative number was safer. Then I installed it and
ran `.Q.lim`, which reports **16**. The documentation page was right and the blog was wrong.

The pattern: I twice preferred a secondary source over a primary one, and was wrong both times —
once toward optimism, once toward pessimism, so it wasn't even a consistent bias. **Rank your
sources before you read, not after.** License text, then vendor documentation, then the running
binary as tiebreak, then everyone else. And "everyone else" includes the blog you are reading now,
which is why every clause above carries a number.

## What I would tell you before you start

If you plan to teach, benchmark, or CI a vendor's free tier in public:

1. **Read the actual agreement bundled with the actual download, before you design anything.** Not
   the marketing page, not the FAQ, not a summary — including your own spec's summary.
2. **Search it for a benchmark clause specifically.** Database vendors have a long tradition here.
   If you have a performance article planned, that clause decides whether it exists.
3. **Separate mandatory license validation from optional telemetry.** They are different consents
   and get conflated constantly.
4. **Decide which CI check can run on an untrusted PR**, and accept that a key-gated one cannot.
5. **Write down the version you actually ran.** Mine is KDB-X 5.0, build 2026.07.23, and J 9.7.1 —
   pinned because "the free tier" is not a version and a silent upgrade is a silent change in what
   your examples teach.

None of this made the project harder to build. It made two of my planned claims impossible and one
planned article better, and I would rather have learned all three on day one than after publishing.

---

*Not affiliated with, sponsored by, or endorsed by KX Systems, Inc. "q", "kdb+" and "KDB-X" are
third-party marks used nominatively. Nothing here is a statement about the product's performance —
which is, in part, the point.*
