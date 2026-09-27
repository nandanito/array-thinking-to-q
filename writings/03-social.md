<!--
Social posts for article 3, the as-of join (RELEASE-CHECKLIST: "X + Bluesky: short thread — hook + one
snippet + canonical link"; "Mastodon: single-post summary + link"; Nostr, same shape as Mastodon).
DRAFT: <URL> is the article's canonical URL, unknown until nandan.me publishes it.
Snippet provenance: `times:0 2 5; bids:99 99.1 99.4` is line 1 of lesson 05's section 3 block,
verbatim; `bids times bin 3 2 -1` is the next block's code with its trailing comment removed, and
that comment is where "99.1 99.1 0n" comes from (make verify-prose checks it).
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Image: attach writings/figures/03/linkedin-card.png to the first post on each network, with the
alt text below.
No speed or performance wording anywhere (Clause 9 caution, as in the article).
Lengths are checked against each network's limit (X 280 chars, Bluesky 300, Mastodon 500);
links count as 23 characters on X and Mastodon.

Alt text (all networks):
One trade, AAPL at 10:00:03, matched in two steps against a quote table sorted by symbol then
time. Step 1, group: AAPL's rows are 0 1 2. Step 2, bin: within those rows, the latest quote at or
before 10:00:03 is row 1, bid 99.1. The as-of join is group plus bin.
-->

# X (thread, tag @kxsystems)

**1/4**

pandas, Polars, DuckDB and ClickHouse all have an as-of join. It isn't q's secret.

What's different in q is what the join looks like when the language and storage were built around it.

Article 3 of 5 ↓ #kdb

**2/4**

q's aj comes apart into two primitives: group finds each symbol's rows, bin finds the latest time at or before each trade.

The edge cases come with bin:

times:0 2 5; bids:99 99.1 99.4
bids times bin 3 2 -1

gives 99.1 99.1 0n. A tie counts; before the first quote is null.

**3/4**

The price: bin trusts your sort and never checks it.

Drop the attribute and aj gives the same table. Drop the sort and it gives a different one, silently.

The attribute is optional. The sort is not.

**4/4**

Also: J as a control, an excellent array language that wasn't built for this join, and the edges it leaves to you.

Every snippet runs in CI. No timings, by choice.

<URL>

Not affiliated with KX.

# Bluesky (thread)

**1/4**

pandas, Polars, DuckDB and ClickHouse all have an as-of join. It isn't q's secret.

What's different in q is what the join looks like when the language and storage were built around it.

Article 3 of 5 ↓

#kdb

**2/4**

q's aj comes apart into two primitives: group finds each symbol's rows, bin finds the latest time at or before each trade.

The edge cases come with bin:

times:0 2 5; bids:99 99.1 99.4
bids times bin 3 2 -1

gives 99.1 99.1 0n. A tie counts; before the first quote is null.

**3/4**

The price: bin trusts your sort and never checks it.

Drop the attribute and aj gives the same table. Drop the sort and it gives a different one, silently.

The attribute is optional. The sort is not.

**4/4**

Also: J as a control, an excellent array language that wasn't built for this join, and the edges it leaves to you.

Every snippet runs in CI. No timings, by choice.

<URL>

Not affiliated with KX.

# Mastodon (single post)

pandas, Polars and DuckDB all have an as-of join; it isn't q's secret. What's different in q is what the join looks like when the language and storage were built around it: aj is two primitives, group and bin, and every edge case (ties, trades before the first quote, unknown symbols) is settled by them. The price is a sort that bin trusts and never checks.

Article 3 of 5: <URL>

#kdb #q #TimeSeries #ArrayProgramming

# Nostr (single note)

pandas, Polars, DuckDB and ClickHouse all have an as-of join, so having one isn't what makes q interesting. What I wanted to see was what the join looks like when the language and its storage were built around it.

In q, aj comes apart into two primitives: group finds each symbol's rows, and bin finds the latest time at or before each trade. The awkward cases (a tie, a trade before the first quote, a symbol with no quotes) are all settled by those primitives, with no special-case code. The price is that bin trusts your sort and never checks it: drop the attribute and you get the same table, drop the sort and you get a different one, silently.

Written for people who have never read q; every snippet runs in CI.

Article 3 of 5: <URL>
Repo: https://github.com/nandanito/array-thinking-to-q

#kdb #programming #TimeSeries
