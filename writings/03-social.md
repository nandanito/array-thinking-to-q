<!--
Social posts for article 3, the as-of join (RELEASE-CHECKLIST: X + Bluesky + Mastodon + Nostr). Each is
a single post, the shape the eval posts settled on: the personal X account has Premium (long posts),
and Bluesky's 300-character cap is met by one short post instead of a thread.
The article is live at https://nandan.me/writing/the-as-of-join/ (published 2026-10-16).
Each picks up from the eval posts (2026-09-29), but the hook (the join is not q's secret; what differs
is that it comes apart into two primitives on a sort you own) comes first. Plain language for non-q
readers: group and bin each get one clause, "null" is spelled out next to 0n, and q's attribute is
"a flag q keeps on a column".
Snippet provenance: `times:0 2 5; bids:99 99.1 99.4` is line 1 of lesson 05's section 3 block,
verbatim; `bids times bin 3 2 -1` is the next block's code with its trailing comment removed, and
that comment is where "99.1 99.1 0n" comes from (make verify-prose checks it).
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Images: attach writings/figures/03/linkedin-card.png (1200×627, figure 1 rendered with
`rsvg-convert -w 1200`) to every post, with the card alt text below. Figure 2 goes in an optional
self-reply on X and Mastodon as writings/figures/03/figure-2-group-plus-bin.png (1800×1000, figure 2
at 2x) with the figure 2 alt text; as a second attachment it would be cropped into a grid, as the
only image of a reply it shows whole. Bluesky gets the card only.
No speed or performance wording anywhere (Clause 9 caution, as in the article).
Lengths checked 2026-10-16: X long post (Premium, 25,000 limit; about the first 280 characters show
before "Show more", so the opening carries the hook); Bluesky within 300 counting the full URL;
Mastodon within 500 with the link counted as 23.

Card alt text (all networks):
A time axis for one symbol, AAPL. Three quotes above it at 10:00:00 (bid 99), 10:00:02 (bid 99.1)
and 10:00:05 (bid 99.4). Five trades below it, each with an arrow back to the quote it matches:
10:00:01 takes 99, 10:00:03 takes 99.1, 10:00:06 takes 99.4; a trade at exactly 10:00:02 takes that
quote, 99.1; a trade at 09:59:59, before any quote, gets null and keeps its row.

Figure 2 alt text (the self-reply):
One trade, AAPL at 10:00:03, matched in two steps against a quote table sorted by symbol then
time. Step 1, group: AAPL's rows are 0 1 2. Step 2, bin: within those rows, the latest quote at or
before 10:00:03 is row 1, bid 99.1. The as-of join is group plus bin; the sort serves both steps,
and only the group half can be recorded by an attribute.
-->

# X (single long post, tag @kxsystems)

pandas has merge_asof, Polars has join_asof, DuckDB and ClickHouse have an ASOF JOIN. The as-of join isn't q's secret. What's different in q is that @kxsystems' aj comes apart into two primitives you already know, standing on a sort you're responsible for. Article 3 of my array-thinking series.

group finds each symbol's rows once, for the whole quote table. bin finds the latest quote time at or before each trade. The edge cases come with bin. Three quote times and their bids:

times:0 2 5; bids:99 99.1 99.4
bids times bin 3 2 -1

gives 99.1 99.1 0n. A trade at 3 takes the quote at 2. A trade at exactly 2 takes that quote: a tie counts. A trade at -1, before any quote, gets 0n, q's null. Nobody wrote a special case.

The price: bin assumes the quotes are sorted and never checks. q can stamp a column with a flag that records the grouping; nothing records the time order inside each symbol, and that is the half that decides correctness. Drop the flag and you get the same table. Drop the sort and, on the lesson's data, you get a different one, silently.

Also in the article: J as the control, an excellent array language that wasn't built for this join, and the bug a reviewer found in a lesson that was already verified green. Every snippet runs in CI. No timings, by choice.

Article 3 of 5: https://nandan.me/writing/the-as-of-join/

Independent work; not affiliated with KX.

#kdb #TimeSeries

# Bluesky (single post)

The as-of join isn't q's secret: pandas, Polars and DuckDB have one too. What differs in q is that aj comes apart into two primitives, group and bin, standing on a sort that bin trusts and never checks. (Part 3 of my array-thinking series.)

https://nandan.me/writing/the-as-of-join/

# Mastodon (single post)

pandas, Polars and DuckDB all have an as-of join; it isn't q's secret. What's different in q: aj is two primitives you already know. group finds each symbol's rows once; bin finds the latest quote at or before each trade. Ties, early trades and unknown symbols all fall out of those two. The price is a sort that bin trusts and never checks: drop it and, on the lesson's data, you get a different table, silently.

Article 3 of 5: https://nandan.me/writing/the-as-of-join/

#kdb #q #TimeSeries #ArrayProgramming

# Nostr (single note)

pandas, Polars, DuckDB and ClickHouse all have an as-of join, so having one isn't what makes q interesting. Article 3 of my array-thinking series is about what the join looks like when the language and its storage were built around it.

In q, aj comes apart into two primitives: group finds each symbol's rows once, for the whole quote table, and bin finds the latest quote time at or before each trade. The awkward cases (a tie, a trade before the first quote, a symbol with no quotes) are all settled by those primitives and one indexing rule, with no special-case code. The price is that bin assumes the quotes are sorted and never checks. q can stamp a column with a flag that records the grouping; nothing records the time order inside each symbol, and that is the half that decides correctness. Drop the flag and you get the same table. Drop the sort and, on the lesson's data, you get a different one, silently.

Written for people who have never read q; every snippet runs in CI. J serves as the control, and the article reports the bug a reviewer found in a lesson that was already verified green. No timings, by choice.

Article 3 of 5: https://nandan.me/writing/the-as-of-join/
Repo: https://github.com/nandanito/array-thinking-to-q

#kdb #programming #TimeSeries

# Self-reply with figure 2 (X and Mastodon, optional)

The two primitives in one picture. group finds the symbol's block of rows; bin finds the position inside it. Sorting by symbol first makes the block, sorting by time second makes bin right, and only the first half can be recorded by a flag.
