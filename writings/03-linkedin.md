<!--
LinkedIn post for article 3, the as-of join (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
The article is live at https://nandan.me/writing/the-as-of-join/ (published 2026-10-16).
Suggested slot: a weekday morning, 08:30 CEST, as the eval post had (2026-09-29).
Image: attach writings/figures/03/linkedin-card.png (1200×627; it is figure 1 rendered with
`rsvg-convert -w 1200`, and the committed PNG is byte-identical to that render). Alt text below.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
Picks up from the eval post (2026-09-29) in paragraph 2, but the hook (the join is not q's secret;
what differs is that it comes apart into two primitives on a sort you own) sits inside the
~210-character preview. Jargon translated for non-q readers: "attribute" becomes the flag q keeps
on a column, "null" rather than 0n, and group and bin each get one plain clause.
Every claim is from the article: aj as group plus bin, the three edge cases, the unchecked sort,
the sort as the half no attribute records, attribute optional / sort not, the J contrast, the
reviewer's tie-break find in a lesson that was already green.
Deliberately no speed or performance wording (Clause 9 caution, same as the article): "looks at
less of the data" is not repeated here either, because without the article's framing it reads as
a performance claim.

Alt text:
A time axis for one symbol, AAPL. Three quotes above it at 10:00:00 (bid 99), 10:00:02 (bid 99.1)
and 10:00:05 (bid 99.4). Five trades below it, each with an arrow back to the quote it matches:
10:00:01 takes 99, 10:00:03 takes 99.1, 10:00:06 takes 99.4; a trade at exactly 10:00:02 takes that
quote, 99.1; a trade at 09:59:59, before any quote, gets null and keeps its row.
-->

pandas has merge_asof. Polars has join_asof. DuckDB, QuestDB and ClickHouse all have an ASOF JOIN.
So having the as-of join is not what makes q interesting. What is: in q the join comes apart into
two primitives you already know, standing on a sort you are responsible for.

Last month I measured @KX's q plugin. Article 3 of my array-thinking series takes KX's aj apart
instead. One primitive, group, finds each symbol's rows once, for the whole quote table. The
other, bin, finds the latest quote time at or before each trade. The awkward cases (a trade at
exactly a quote's time, a trade before the first quote, a symbol with no quotes at all) are
settled by those two primitives and one indexing rule, with no special-case code. The price is
that bin assumes the quotes are sorted and never checks. q lets you stamp a column with a flag
that records the grouping; nothing can record the time order inside each symbol, and that is the
half that decides correctness. Drop the flag and you get the same table. Drop the sort and, on
the lesson's data, you get a different one, silently.

The article is written for people who have never read q, and every snippet is copied from a
lesson that runs in CI. It uses J as the control, an excellent array language that was not built
around this join, to show which edge cases a general design leaves to you. It also reports the
bug a reviewer found in a lesson that was already verified green: a verified fixture is not a
verified claim. There are no timings, by choice; the argument does not need them.

https://nandan.me/writing/the-as-of-join/

Independent work; not affiliated with KX.

#kdb #TimeSeries #ArrayProgramming #DataEngineering
