<!--
LinkedIn post for article 1 (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
Article 1 is live; ready to post.
Canonical URL: https://nandan.me/writing/array-thinking-all-the-way-to-q/ (published 2026-09-25).
Image: attach writings/figures/01/linkedin-card.png (figure 1 at 1200x627).
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
Snippet provenance: `2 * til 5` → 0 2 4 6 8 is lesson 01's line 53, verified by `make verify`.
-->

Array languages ask one thing of an experienced programmer: stop writing the loop. Not the syntax,
which you can pick up in an afternoon, but the reflex of stepping through data one element at a
time with an index and an accumulator.

The whole idea fits in one line of q. Where Python needs a loop, an index and a list to append to,
q writes `2 * til 5` and gets 0 2 4 6 8. The iteration has not disappeared; it has moved into the
operator. Once that clicks, the same move carries from a list to a table, a query and a time-series
join, and the code starts describing the data instead of the steps.

I have been working through that shift deliberately and turning it into a short curriculum: a
brief laboratory in J, where the notation leaves no comfortable place for a loop, then q/kdb+ from
@KX as the destination. Every example in it runs against the real interpreters, and the misses are
published alongside the results. The first of six articles sets out the approach.

https://nandan.me/writing/array-thinking-all-the-way-to-q/

Independent work; not affiliated with KX.

#ArrayProgramming #kdb #SoftwareEngineering #TimeSeries
