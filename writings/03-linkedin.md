<!--
LinkedIn post for article 3, the as-of join (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
DRAFT: the canonical URL is not known until nandan.me publishes; <URL> is a placeholder.
Image: attach writings/figures/03/linkedin-card.png.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
Every claim is from the article: aj as group plus bin, the three edge cases, the unchecked sort,
attribute optional / sort not, the J contrast. Deliberately no speed or performance wording
(Clause 9 caution, same as the article): "looks at less of the data" is not repeated here either,
because without the article's framing it reads as a performance claim.
-->

pandas has merge_asof. Polars has join_asof. DuckDB, QuestDB and ClickHouse all have an ASOF JOIN.
The as-of join exists wherever time series meet, because everyone eventually asks the same
question: for each trade, what was the quote in force when it happened?

So having the join is not what makes q interesting. What I wanted to see, building a lesson around
@KX's aj, was what the join looks like when the language and its storage were designed around it.
It comes apart into two primitives: group, which finds each symbol's rows, and bin, which finds the
latest time at or before each trade. The awkward cases (a trade at exactly a quote's time, a trade
before the first quote, a symbol with no quotes) are all settled by those two primitives and one
indexing rule, with no special-case code. The price is that bin trusts your sort and never checks
it. Drop the attribute and you get the same table; drop the sort and you get a different one,
silently.

The article is written for people who have never read q, and every snippet is copied from a lesson
that runs in CI. It contrasts J, an excellent array language that wasn't built around this join, to
show which edge cases a general design leaves to you. There are no timings, by choice: the
argument doesn't need them.

<URL>

Independent work; not affiliated with KX.

#kdb #TimeSeries #ArrayProgramming #DataEngineering
