# Lesson 05 — The as-of join

> **Run it** (from the repo root — the last section reads the showcase's golden file):
> `$HOME/.kx/bin/q lessons/05-asof-join/q/asof.q -q < /dev/null`
> (the tool binaries are not on `PATH` — see the [Part II index](../README.md)).
> Every output below is captured from KDB-X CE 5.0; the J twin from J 9.7.1.
> Files: [`q/asof.q`](q/asof.q), [`j/asof-boundaries.ijs`](j/asof-boundaries.ijs).
> The runnable showcase this lesson explains: [`showcase/aj/`](../../showcase/aj/).

You already know this join. If you have written `merge_asof` in pandas, `join_asof` in Polars,
or an `ASOF JOIN` in DuckDB, QuestDB or ClickHouse, you have asked the question this lesson is
about: *for each trade, what was the quote in force when it happened?* Not a quote at exactly that
time — there usually isn't one — but the most recent quote for the same symbol at or before it.
The as-of join is not rare and it is not q's secret. It exists wherever time series meet.

So this lesson does not introduce `aj` as a feature. It does something more useful: it takes the
join apart and shows that it is made of two things you have already met — lesson 03's `group`,
and one primitive, `bin` — operating on the column lists of lesson 02, over a table whose row
order lesson 04 made **your** responsibility. When those pieces are in place, `aj` is barely a
function at all; it is what the layout was for. That is the honest version of the claim usually
made about q and time series. It is not that q has the join and nobody else does. It is what the
join looks like when the language and its storage were designed around it.

And one practical payoff. The [showcase](../../showcase/aj/) opens with two lines of preamble —
sort the quotes by `` `sym`time ``, then put `` `g# `` on `sym` — that the reference manual
prescribes and most code copies. By the end of this lesson you should be able to *derive* both
lines, and say which half of the join each one serves.

*(As in lesson 04: no timings. The KDB-X Community Edition license restricts publishing
performance figures — see [`docs/licensing-notes.md`](../../docs/licensing-notes.md). Where this
lesson says one shape does less work than another, it means it counts fewer things, which you can
check by reading the code; it does not mean a measurement.)*

---

## 0. The data

The showcase's tables, exactly — with the quotes still in the order they arrived, which is not
time order:

```q
quote:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL;
          time:10:00:02 10:00:04 10:00:00 10:00:01 10:00:05;
          bid :99.1 200.3 99.0 200.0 99.4;
          ask :99.3 200.5 99.2 200.2 99.6 )
```

```
sym  time     bid   ask
-------------------------
AAPL 10:00:02 99.1  99.3
MSFT 10:00:04 200.3 200.5
AAPL 10:00:00 99    99.2
MSFT 10:00:01 200   200.2
AAPL 10:00:05 99.4  99.6
```

```q
trade:([] sym :`AAPL`AAPL`MSFT`AAPL`MSFT;
          time:10:00:01 10:00:03 10:00:02 10:00:06 10:00:06;
          price:99.15 99.25 200.1 99.5 200.4;
          size:100 200 50 150 75 )
```

```
sym  time     price size
------------------------
AAPL 10:00:01 99.15 100
AAPL 10:00:03 99.25 200
MSFT 10:00:02 200.1 50
AAPL 10:00:06 99.5  150
MSFT 10:00:06 200.4 75
```

---

## 1. The join you already know, asked the loop way

The imperative instinct writes the definition down directly. In SQL it is a correlated subquery;
in q it is a function applied to each trade:

```q
prevailing:{[s;t] exec first bid where time=max time from quote where sym=s, time<=t}
prevailing'[trade`sym; trade`time]
```

```
99 99.1 200 99.4 200.3
```

Those are the right answers, and the function deserves credit for something: it does not care
what order the quotes are in. "The one whose time is the greatest among those at or before `t`"
is a statement about *values*, and it stays true however the rows are shuffled. Lesson 04 spent a
whole section on an `aj` that returned 98.5 instead of 99.1 because the rows were in the wrong
order; this version cannot make that mistake.

What it gets wrong is the shape of the work. For every trade it filters the **entire** quote
table by symbol, filters the survivors by time, then scans what is left for a maximum. Five
trades means five full passes; a day of trades against a day of quotes means trades × quotes.
And look at what each pass recomputes. It asks two questions:

1. *Which quotes belong to this symbol?* The answer depends only on the symbol — yet it is
   recomputed for every trade, including the three AAPL trades that ask it about the same `` `AAPL ``.
2. *Of those, which is the latest at or before `t`?* This one genuinely depends on the trade. But
   it is answered by looking at every candidate, as though the quote times had no order at all.

The rest of the lesson answers each question the array way — once, for the whole table.

---

## 2. Question one has a per-table answer: `group`

Lesson 03 already built it:

```q
group quote`sym
```

```
AAPL| 0 2 4
MSFT| 1 3
```

One pass over the `sym` column, and every trade's first question becomes a dictionary lookup.
This dictionary is also exactly what lesson 04's `` `g# `` attribute *keeps*: `` `g# `` is not a
mysterious index, it is `group` of the column, built once and attached to it, so that anything
filtering on `sym` can look the rows up instead of scanning for them.

---

## 3. Question two is a primitive: `bin`

Within one symbol's quotes, "the latest at or before `t`" is a search, and q has a primitive whose
definition is that sentence. `x bin y` returns the index of the **last element of `x` that is at
or before `y`** — provided `x` is sorted. Here are AAPL's three quote times as seconds past
10:00:00, with their bids:

```q
times:0 2 5; bids:99 99.1 99.4
times bin 3                / 1 — index of the last element <= 3
times bin 2                / 1 — a tie counts: <=, not <
times bin -1               / -1 — nothing at or before: off the front
```

Every edge of the as-of question is already decided by the primitive. A trade at exactly a quote's
time gets *that* quote, because the comparison is at-or-before. A trade before any quote gets
`-1` — and `-1` is not a valid position in q, so indexing with it yields a null rather than an
error or a wrapped-around value:

```q
bids times bin 3 2 -1      / 99.1 99.1 0n — and index -1 is null
```

That is a join's worth of boundary semantics — inside, tie, and before-the-first — in one
primitive and one indexing rule, and none of it had to be written.

Now the cost of that convenience, which is lesson 04's cost in a new place. `bin` gets to answer
without looking at every element because it *assumes* `x` is sorted, and it does not check:

```q
2 0 5 bin 3                / 1 — unsorted: a confident, wrong index
```

Position 1 of `2 0 5` holds `0`. The quote at `2` was the right one. No error, no warning — the
same silence as lesson 04's `aj` over an unsorted table, and for the same reason. The search that
makes `bin` worth having is exactly what makes it trust you.

---

## 4. Sort once, and both questions become lookups

So each half of the join needs something from the quote table. The `group` half needs each
symbol's rows to be findable. The `bin` half needs each symbol's times to be **ascending in row
order**. One sort provides both:

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

```q
group sorted`sym
```

```
AAPL| 0 1 2
MSFT| 3 4
```

Compare that with section 2's `0 2 4` / `1 3`. Sorting by `sym` first turned each symbol's rows
into one **contiguous block**; sorting by `time` second made the times inside each block
ascending. Every block is now a ready-made argument for `bin`.

This is the showcase's first preamble line, derived rather than copied, and both of its columns
now have a job:

- **`time` is for correctness.** It is what makes `bin` — and so `aj` — return the right row.
  Leave it out and you get section 3's confident wrong index.
- **`sym` first is for the grouping.** It is what makes each symbol's rows a single block, which
  is the shape the group half can exploit — and the shape lesson 04's `` `p# `` (*parted*) exists
  to claim.

And lesson 04's section 4 lands here with its full weight. `xasc` stamps `` `s# `` on `sym` and
**nothing** on `time`, because "ascending within each block of another column" is not a property
any q attribute can express. The half of the preamble that the join's *correctness* depends on is
precisely the half the language cannot record for you.

---

## 5. `aj`, built by hand from those two pieces

Put them together. Look up each trade's block with `group`, then `bin` the trade time into that
block's times:

```q
g:group sorted`sym
idx:{[r;t] r sorted[`time][r] bin t}'[g trade`sym; trade`time]
idx
```

```
0 1 3 2 4
```

One quote row per trade: `bin` gives a position *within* the block, and `r` translates it back to
a row of `sorted`. Index the quote table with those rows and stitch the columns alongside the
trades — lesson 02's `,'`, joining two tables row by row:

```q
hand:trade,'`bid`ask#sorted idx
```

```
sym  time     price size bid   ask
------------------------------------
AAPL 10:00:01 99.15 100  99    99.2
AAPL 10:00:03 99.25 200  99.1  99.3
MSFT 10:00:02 200.1 50   200   200.2
AAPL 10:00:06 99.5  150  99.4  99.6
MSFT 10:00:06 200.4 75   200.3 200.5
```

```q
hand ~ aj[`sym`time; trade; sorted]   / 1b
```

That is the as-of join. `aj`'s column argument `` `sym`time `` is this same decomposition written
as a spec: every column but the last is matched by **equality** (the `group` half), and the last is
matched **as-of** (the `bin` half). The reference phrases the result as *"the last (in row order)
matching record"* — and now you can see why it says *row order* rather than *greatest time*. It is
describing `bin`. On a table sorted the way section 4 sorted it, the last row in order *is* the
latest in time; on any other table, as lesson 04 showed, it is not, and `aj` returns what `bin`
returns.

Look back at section 1 with this in hand. The loop said "greatest time", which is order-proof and
costs a scan per trade. `aj` says "last in row order", which is a search per trade and costs you a
promise. The difference between those two phrases *is* the co-design: q chose the definition that
the storage can answer directly, and handed you the sort as the price of admission.

(The hand version still walks the trades one at a time with `'`, and it is not how you would write
this join — you would write `aj`. Its job is to make the parts visible. Inside `aj` the same two
questions are answered by the engine, with the attribute telling it how to find each block.)

---

## 6. The edges fall out of `bin`, not out of special cases

Three awkward trades: one before AAPL's first quote, one at *exactly* a quote time, and one for a
symbol that has no quotes at all.

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

Every trade survives — `aj` is a *left* join, so the result always has one row per trade, and
where nothing prevailed you get nulls, not a missing row. The tie gets the quote stamped at the
same second. And the hand-built version produces exactly this, with no code for any of the three
cases:

```q
eidx:{[r;t] r sorted[`time][r] bin t}'[g edge`sym; edge`time]
eidx
```

```
0N 1 0N
```

```q
(edge,'`bid`ask#sorted eidx) ~ aj[`sym`time; edge; sorted]   / 1b
```

The early AAPL trade: `bin` returned `-1`, and row `-1` of the block is null. The IBM trade: `g`
has no `` `IBM `` key, so the lookup returns an empty list, `bin` on an empty list is `-1`, and the
same null follows. The tie: `bin` is at-or-before. The nulls in `aj`'s output are not a policy
someone wrote — they are what indexing does off the front of a list.

---

## 7. The showcase preamble, now every line has a reason

```q
quote:`sym`time xasc quote       / correctness: blocks by sym, time ascending in each
@[`quote;`sym;`g#]               / speed: record the group half, set LAST
res:aj[`sym`time; trade; quote]
```

```
sym  time     price size bid   ask
------------------------------------
AAPL 10:00:01 99.15 100  99    99.2
AAPL 10:00:03 99.25 200  99.1  99.3
MSFT 10:00:02 200.1 50   200   200.2
AAPL 10:00:06 99.5  150  99.4  99.6
MSFT 10:00:06 200.4 75   200.3 200.5
```

That is the showcase, line for line, and the lesson's file checks that `res` renders
line-for-line identical to [`showcase/aj/expected.txt`](../../showcase/aj/expected.txt) — the golden file
`make verify` diffs the showcase against — exiting nonzero if it ever does not:

```
1b
```

Read the preamble back with sections 2–5 in hand:

- **`` `sym`time xasc ``** — the correctness step. `time` ascending within each `sym` is what makes
  "last in row order" mean "latest", i.e. what makes `bin` right. `sym` first makes each symbol one
  contiguous block.
- **`` `g# `` on `sym`** — the speed step. It records the *group* half of the join (section 2's
  dictionary) so the engine can find each symbol's block by lookup. It records nothing about the
  `bin` half; nothing can. It goes **last**, after the data is final, because lesson 04 showed
  attributes are perishable. (And lesson 04's section 6 still stands: on a table already sorted
  this way, `` `p# `` is also available and defensible. `` `g# `` is the default the showcase
  ships, not the single right answer.)
- **`aj[`sym`time; …]`** — equality on every column but the last, `bin` on the last.

Which is to say: the attribute is optional and the sort is not. Drop the `` `g# `` line and the
showcase prints the same table. Drop the sort and it prints a *different* table — mostly right,
wrong for the symbols with several quotes in the window, and silent about it.

---

## What "built around it" actually means

Every as-of join implementation has to solve the same two sub-problems, because they are the
definition of the join: find the matching group, then search it by time. What differs is how much
of that is *native to the data* rather than *done to it*.

In q, nearly all of it is native. A table is a dictionary of column lists (lesson 02), so
`sorted`time` is not an extracted copy or a view — it is the column, a plain list, which `bin`
accepts as-is. The search primitive was defined with as-of semantics — at-or-before, `-1` off the
front, null on indexing — so the boundary cases of the join need no code. The group half is an
attribute the column can carry. And the conventional on-disk layout for this kind of data is the
same shape again: each partition sorted by symbol, with `` `p# `` claiming the blocks — which is why the `aj`
reference's advice for tables on disk is `` `p# `` rather than `` `g# ``. The join, the in-memory
table and the storage all agree about what order the rows are in.

The bill for that agreement is the one lesson 04 itemised. Because the layout is what makes the
search possible, the engine trusts the layout rather than checking it — a check is a full pass,
and the full pass is what the layout exists to avoid. That is a design decision, not a missing
feature: it puts the sort on you, and gives you back a join that is two ideas you can hold in your
head at once.

---

## The J twin: a search, and two edges to get right yourself

J has no as-of join, and its closest primitive answers a subtly different question. `I.` —
*interval index* — returns, for each `y`, the **first** position whose item is at or after `y`.
Step back one and you seem to have "the last item before `y`", which *looks* like `bin`:

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

Right inside, wrong at both edges — and silently. On the tie at `2`, "first at or after" lands on
the tie itself, so stepping back skips *past* the quote that was stamped at exactly the trade
time: `99`, not `99.1`. Before the first quote, stepping back from `0` gives `_1`, and `_1` is a
perfectly legal J index — it means *the last item* — so a trade that should have no quote gets the
day's latest one, `99.4`.

The index can be repaired by asking the as-of question literally, "how many quotes are at or
before `t`, less one":

```j
echo <: +/ times <:/ 3 2 _1
echo bids {~ <: +/ times <:/ 3 2 _1
```

```
1 1 _1
99.1 99.1 99.4
```

`1 1 _1` is exactly what q's `bin` returned in section 3. But the value is still wrong, because
the second edge was never in the search — it is in *indexing*. In q, `-1` is off the end and yields
a null; in J it wraps. So the J programmer writes a guard as well.

None of this is a defect in J. `I.` is a general interval search and negative indices are a
deliberate convenience; both are the right defaults for a general-purpose array language. The
contrast is the lesson's thesis from the other side: q's `bin` and q's out-of-range null were
chosen *together*, for this join, and the join's edge cases were settled in the primitives before
you ever wrote `aj`.

---

## What to carry forward

- **`aj` is `group` plus `bin`.** Every join column but the last is matched by equality (find the
  symbol's rows), the last is matched as-of (search them by time). `aj[`sym`time; …]` spells
  exactly that.
- **The loop's definition is order-proof; `aj`'s is not.** "Greatest time at or before" survives
  any row order and costs a scan per trade. "Last in row order" is a search per trade and is
  correct only on a sorted table. q chose the second on purpose.
- **Derive the preamble, don't copy it.** `` `sym`time xasc `` — `time` for correctness (it makes
  `bin` right), `sym` first for contiguous blocks. `` `g# `` on `sym` — speed only, recording the
  group half, set last. The sort is mandatory; the attribute is not.
- **The half that decides correctness is the half no attribute can record** — time ascending
  *within* each symbol (lesson 04, section 4). Nothing checks it for you.
- **The edges are in the primitives.** Tie → at-or-before; before the first quote or an unknown
  symbol → `bin` gives `-1`, indexing gives null, `aj` gives a null row rather than dropping the
  trade.
- **"Built around it" means agreement, not exclusivity.** Other engines have this join. In q the
  table layout, the search primitive, the attributes and the storage all assume the same row order
  — which is why the join is small, and why the sort is your job.

**This is the last lesson of Part II.** The J laboratory (Part I) and the transition chapter —
what does and does not carry over from J to q — land in a later milestone; see the
[Part II index](../README.md).

---

### References

- `aj` / `aj0`, *"the last (in row order) matching record"*, and the memory/disk attribute table:
  [code.kx.com — aj](https://code.kx.com/q/ref/aj/)
- `bin` / `binr` (binary search, sortedness assumed):
  [code.kx.com — bin](https://code.kx.com/q/ref/bin/)
- `group`: [code.kx.com — group](https://code.kx.com/q/ref/group/)
- `xasc`: [code.kx.com — xasc](https://code.kx.com/q/ref/asc/#xasc)
- Attributes, including `` `p# `` vs `` `g# ``:
  [code.kx.com — Set Attribute](https://code.kx.com/q/ref/set-attribute/)
- J's `I.` interval index:
  [J Dictionary — Indices / Interval Index](https://www.jsoftware.com/help/dictionary/dicapdot.htm)
