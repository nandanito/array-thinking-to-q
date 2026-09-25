# The as-of join: what changes when the engine is built around one primitive

*Article 4 of 6 — draft. Gated on M3 (the q core).*

> **Provenance.** Every q and J snippet below is copied from
> [lesson 05](https://github.com/nandanito/array-thinking-to-q/tree/main/lessons/05-asof-join/), whose outputs `make verify` re-captures from KDB-X CE 5.0
> and J 9.7.1 and diffs against the page. No output here was typed by hand. There are no timings
> anywhere in this article, deliberately: the KDB-X Community Edition license bars publishing
> performance figures without KX's written consent ([licensing notes](https://github.com/nandanito/array-thinking-to-q/blob/main/docs/licensing-notes.md)).
> Everything below is about *what* the join does and *why it is shaped that way*, which it turns
> out is the more interesting half anyway.

---

*New to q? It is the language of kdb+, a column-oriented time-series database best known in
finance. Article 1 of this series has a one-minute primer on array languages; nothing here needs
more than that.*

There is a sentence people like to write about q, and it goes something like: *kdb+ has the as-of
join, and that is why trading firms pay for it.*

I don't want to write that sentence, for two reasons. The first is that I can't back it up: the
license I run q under forbids me from publishing the numbers that sentence implies. The second is
better. **It isn't true in the way it sounds.** pandas has `merge_asof`. Polars has `join_asof`.
DuckDB, QuestDB and ClickHouse all have an `ASOF JOIN`. The as-of join is not rare and it is not
q's secret. It exists wherever time series meet, because the question it answers is one every
time-series programmer eventually asks:

*For each trade, what was the quote in force when it happened?*

Not a quote at exactly that time — there usually isn't one — but the most recent quote for the same
symbol at or before it.

![A time axis for one symbol, AAPL. Three quotes above it at 10:00:00 (bid 99), 10:00:02 (bid 99.1) and 10:00:05 (bid 99.4). Five trades below it, each with an arrow back to the quote it matches: 10:00:01 takes 99, 10:00:03 takes 99.1, 10:00:06 takes 99.4; a trade at exactly 10:00:02 takes that quote, 99.1; a trade at 09:59:59, before any quote, gets null and keeps its row.](figures/04/figure-1-trades-meet-quotes.svg)

*Figure 1. The as-of join: same symbol, at or before, most recent. The dashed trades are the edge
cases this article comes back to.*

So if the join isn't the story, what is? After building the lesson around it, my answer is: the
story is what the join looks like **when the language, the table layout and the storage were all
designed around it**. In q, `aj` turns out to be barely a function at all. It is two primitives you
already know, standing on a sort you are responsible for — and every edge case of the join is
settled before you write a line.

## The loop you would write first

Here is the imperative definition, written down directly. In SQL it would be a correlated subquery;
in q it is a function applied to each trade:

```q
prevailing:{[s;t] exec last bid where time=max time from quote where sym=s, time<=t}
prevailing'[trade`sym; trade`time]
```

```
99 99.1 200 99.4 200.3
```

Right answers. And the function deserves credit for something real: it does not care what order the
quote rows are in. "The quote with the greatest time at or before `t`" is a statement about
*values*. Shuffle the table and it stays true — with one exception, which turns out to matter: if
two quotes share a timestamp, "the greatest time" names both, and only row order can break the tie.
That is why it says `last bid`; we will come back to it.

What it gets wrong is the shape of the work. Every trade filters the whole quote table by symbol,
filters again by time, then scans the survivors for a maximum. And inside that, it asks two
different questions and treats them the same way:

1. *Which quotes belong to this symbol?* That depends only on the symbol — yet it's recomputed for
   every trade, including three AAPL trades asking about the same AAPL.
2. *Of those, which is the latest at or before `t`?* This one genuinely depends on the trade. But
   it's answered by looking at every candidate, as though quote times had no order at all.

The array way is to answer each question once, for the whole table.

## Question one is `group`

"Which rows are this symbol" has a per-table answer, and it is one of the first things you learn in
q:

```q
group quote`sym
```

```
AAPL| 0 2 4
MSFT| 1 3
```

One pass, and every trade's first question becomes a dictionary lookup. This is also what q's
`` `g# `` attribute *is*: not a mysterious index, but `group` of the column, built once and kept
attached so anything filtering on `sym` can look the rows up instead of scanning for them.

## Question two is `bin`

"The latest at or before `t`" is a search, and q has a primitive whose definition is that sentence.
`x bin y` returns the index of the last element of `x` that is at or before `y`. Take AAPL's three
quote times as seconds past 10:00, with their bids:

```q
times:0 2 5; bids:99 99.1 99.4
times bin 3                / 1 — index of the last element <= 3
times bin 2                / 1 — a tie counts: <=, not <
times bin -1               / -1 — nothing at or before: off the front
```

This is the part I did not appreciate until I wrote the lesson. **Every boundary case of the as-of
join is already decided by that primitive.** A trade at exactly a quote's time gets *that* quote,
because the comparison is at-or-before. A trade before any quote gets `-1` — and in q, `-1` is not
a position, so indexing with it gives a null instead of an error or a wrapped-around value:

```q
bids times bin 3 2 -1      / 99.1 99.1 0n — and index -1 is null
```

Inside, on a tie, and before the first quote: a join's worth of edge semantics in one primitive and
one indexing rule, none of which anyone had to write.

## The price: `bin` trusts you

`bin` can answer without looking at every element because it assumes `x` is sorted. It doesn't
check:

```q
2 0 5 bin 3                / 1 — unsorted: a confident, wrong index
```

Position 1 of `2 0 5` holds `0`. The right answer was the `2`. No error, no warning.

That silence is the design, not an oversight. A check would be a full pass over the data, and a
full pass is exactly what the sorted layout exists to avoid. So q makes the trade explicitly:
**the search is yours if the sort is yours.**

## Sort once, and both questions become lookups

One sort serves both halves:

```q
sorted:`sym`time xasc quote
```

```
sym  time     bid   ask
-------------------------
AAPL 10:00:00 99    99.2
AAPL 10:00:02 99.1  99.3
AAPL 10:00:05 99.4  99.6
MSFT 10:00:01 200   200.2
MSFT 10:00:04 200.3 200.5
```

Sorting by `sym` first turns each symbol's rows into one contiguous block — the shape the group
half can exploit. Sorting by `time` second makes the times inside each block ascending — the
precondition that makes `bin` correct.

Now put the two primitives together. Look up each trade's block with `group`; `bin` the trade's
time into that block's times:

```q
g:group sorted`sym
idx:{[r;t] r sorted[`time][r] bin t}'[g trade`sym; trade`time]
idx
```

```
0 1 3 2 4
```

Index the quotes with those rows, stitch them beside the trades, and compare with the real thing:

```q
hand:trade,'`bid`ask#sorted idx
```

```q
hand ~ aj[`sym`time; trade; sorted]   / 1b
```

That is the as-of join, built by hand from two primitives, and it matches q's `aj` exactly. And
`aj`'s own column argument, `` `sym`time ``, turns out to be this decomposition written as a spec:
every column but the last is matched by **equality** (the group half), and the last is matched
**as-of** (the bin half).

![One trade, AAPL at 10:00:03, matched in two steps against the quote table sorted by sym then time. Step 1, group: looking up AAPL returns rows 0 1 2, the AAPL block. Step 2, bin: within that block the times are 10:00:00, 10:00:02, 10:00:05, and bin of 10:00:03 returns position 1, row 1, bid 99.1. Below: sym first makes each symbol one contiguous block; time second makes each block ascending so bin is right. aj[`sym`time; trade; quote] is equality on every column but the last, as-of on the last.](figures/04/figure-2-group-plus-bin.svg)

*Figure 2. `aj` is `group` plus `bin`. The sort serves both halves; only one half can be recorded
by an attribute.*

It also explains a phrase in the reference manual that reads oddly the first time: `aj` returns
*"the last (in row order) matching record"*. Row order, not greatest time. The manual is describing
`bin`. On a table sorted the way we just sorted it, the last row in order *is* the latest in time;
on any other table it isn't, and `aj` returns what `bin` returns.

That is the co-design in one sentence. The loop said "greatest time" — order-proof, and a scan per
trade. `aj` says "last in row order" — a search per trade, and it costs you a promise. **q chose the
definition its storage can answer directly, and handed you the sort as the price of admission.**

## The edges, for free

The test of whether a tool is really built around a task isn't the happy path. It's the edges. Here
are three awkward trades: one before AAPL's first quote, one at *exactly* a quote time, and one for
a symbol with no quotes at all:

```q
edge:([] sym:`AAPL`AAPL`IBM; time:09:59:59 10:00:02 10:00:03; price:98.9 99.12 150.0)
aj[`sym`time; edge; sorted]
```

```
sym  time     price bid  ask
-----------------------------
AAPL 09:59:59 98.9
AAPL 10:00:02 99.12 99.1 99.3
IBM  10:00:03 150
```

Every trade survives — `aj` is a *left* join, so there is one row per trade, and where nothing
prevailed you get nulls rather than a missing row. The tie gets the quote stamped at the same
second. The hand-built version produces exactly the same table — with no code for any of
the three cases. The early trade: `bin` said `-1`, and row `-1` is null. The unknown symbol: the
`group` lookup returns an empty list, `bin` on an empty list is `-1`, and the same null follows. The
tie: `bin` is at-or-before. The nulls in `aj`'s output are not a policy someone wrote. They are what
indexing does off the front of a list.

## What the same join costs in a language that wasn't built for it

I use J as a laboratory in this curriculum, and it makes a useful control here because it is an
excellent array language that was *not* designed around this join. J's closest primitive is `I.`,
the interval index: for each `y`, the **first** position whose item is at or after `y`. Step back one
and it *looks* like `bin`:

```j
times =: 0 2 5                NB. AAPL's quotes, seconds past 10:00:00
bids  =: 99 99.1 99.4

echo times I. 3 2 _1          NB. inside, on a tie, before the first quote
echo bids {~ <: times I. 3 2 _1
```

```
2 1 0
99.1 99 99.4
```

Right in the middle, wrong at both edges, and silently. On the tie, "first at or after" lands on the
tied quote itself, so stepping back skips *past* the quote stamped at exactly the trade time. Before
the first quote, stepping back from `0` gives `_1` — and `_1` is a perfectly legal J index meaning
*the last item*. A trade that should have no quote gets the day's latest one.

You can repair the index by asking the as-of question literally:

```j
echo <: +/ times <:/ 3 2 _1
echo bids {~ <: +/ times <:/ 3 2 _1
```

```
1 1 _1
99.1 99.1 99.4
```

`1 1 _1` is exactly what q's `bin` returned. The value is *still* wrong, because the second edge was
never in the search — it's in indexing. In q, `-1` is off the end and yields null; in J it wraps. So
the J programmer writes a guard too.

None of that is a defect in J. A general interval search and wrap-around negative indices are the
right defaults for a general-purpose array language. That is precisely the point: **q's `bin` and
q's out-of-range null were chosen together, for this join**, and J's equally sensible choices were
made for something else. You can see co-design without a single benchmark — just by looking at
which edge cases a tool's primitives settle for free.

## The preamble, derived

The showcase in this repo opens with two lines that most `aj` code on the internet copies without
comment:

```q
quote:`sym`time xasc quote       / correctness: blocks by sym, time ascending in each
@[`quote;`sym;`g#]               / speed: record the group half, set LAST
res:aj[`sym`time; trade; quote]
```

After the above, both lines can be read rather than recited:

- **`` `sym`time xasc ``** is the correctness step. `time` ascending within each `sym` is what makes
  "last in row order" mean "latest" — what makes `bin` right. `sym` first makes each symbol one
  block.
- **`` `g# `` on `sym`** is the speed step. It records the group half of the join so the engine can
  find each block by lookup. It records nothing about the `bin` half. (On a table sorted this way,
  `` `p# `` is a legitimate alternative; `` `g# `` is the default the showcase ships, not the only
  right answer.)

Which gives you the one-line summary I wish someone had given me: **the attribute is optional; the
sort is not.** Drop the attribute and you get the same table. Drop the sort and you get a *different*
table — mostly right, wrong only for the symbols with several quotes in the window, and silent about
it. That failure shape — partial, plausible, unannounced — is what the previous lesson in the
curriculum was written to make you afraid of.

And the half that decides correctness — time ascending *within* each symbol — is exactly the half no
q attribute can record for you. `xasc` stamps a sorted attribute on `sym` and nothing on `time`,
because "ascending within each block of another column" is not a property the language can express.
The engine trusts the layout. The layout is yours.

## What review caught that the green build didn't

One more thing, because this series has a habit of reporting its own misses.

Every snippet in the lesson was verified: `make verify` reruns the q and J and fails if any printed
output drifts. It was green. And an independent Codex review still found a real bug in it.

The first version of the loop above said `first bid`, not `last bid`. On the lesson's data that makes
no difference. But if two quotes for a symbol share a timestamp, "the greatest time" names both, and
*something* has to break the tie. Values can't; only row order can. `first bid` broke it one way;
`bin`, and so `aj`, break it the other. So my sentence "the loop is order-proof" was false on a
perfectly valid input — one my fixture just happened not to contain.

The fix was one word, and it made the lesson better: the loop's order-independence has exactly one
hole, and it's the same hole `aj` fills with "last in row order". But the transferable part is the
failure mode. **A verified fixture is not a verified claim.** `make verify` proves the outputs on the
page are real. It cannot prove that a sentence with "always" in it generalises past the inputs you
chose. When the prose says always, test an input the fixture wasn't built to contain.

## What to carry forward

- **The as-of join is everywhere.** What's distinctive about q isn't having it; it's that the table
  layout, the search primitive, the attributes and the storage all assume the same row order.
- **`aj` is `group` plus `bin`.** Equality on every key but the last, as-of on the last.
  `` aj[`sym`time; …] `` spells exactly that.
- **The edges live in the primitives.** At-or-before settles ties; `-1` plus null-on-index settles
  "before the first quote" and "unknown symbol". Nobody wrote a special case.
- **The sort is mandatory; the attribute is not.** And the sort is the half no attribute can record.
- **You can argue co-design without benchmarks.** Look at which edge cases a tool's primitives
  settle for free, and which ones it leaves to you.

**Next in the series:** the J laboratory, and what it shows about loops that q hides.

---

*Not affiliated with or endorsed by KX Systems or Jsoftware. "q", "kdb+", "KDB-X" and "J" are used
nominatively.*
