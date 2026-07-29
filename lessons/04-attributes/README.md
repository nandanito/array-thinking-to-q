# Lesson 04 — Attributes & sort discipline

> **Run it:** `$HOME/.kx/bin/q lessons/04-attributes/q/attributes.q -q < /dev/null`
> (the tool binaries are not on `PATH` — see the [Part II index](../README.md)).
> Every output below is captured from KDB-X CE 5.0; the J twin from J 9.7.1.
> Files: [`q/attributes.q`](q/attributes.q), [`j/sorted-assumption.ijs`](j/sorted-assumption.ijs).

Lesson 03 ended with a loose thread. `select … by` had quietly stamped `` `s `` onto its sorted
keys, and `~` had refused to care. That `` `s `` is an **attribute**, and this lesson is about the
gap between what you think you are doing when you set one and what q actually does.

If you come from SQL, you already have a model for this and it is wrong in an expensive way.
`CREATE INDEX` is a promise the *engine* keeps: the index is a structure the database owns, it is
maintained through every `INSERT` and `UPDATE`, you cannot desynchronise it from its table, and it
is a pure speed decision — an index can never change an answer, and forgetting one can never make
a query wrong.

q keeps exactly one of those properties. An attribute is a claim **you** make about a vector,
verified once at the moment you make it and never again; q maintains it only where maintenance is
cheap, and where it is not, q *silently withdraws the claim* rather than checking. And the sting
in the tail is the last property — the one you were relying on. It is true that an attribute
cannot change an answer. But the **sort discipline the attribute advertises** absolutely can, and
`aj` is where that bill comes due.

*(A note on what this lesson does not contain: timings. The KDB-X Community Edition license
restricts publishing performance figures — see [`docs/licensing-notes.md`](../../docs/licensing-notes.md).
Everything below is about semantics and what the engine is permitted to assume, which is the more
durable half anyway.)*

---

## 1. An attribute is metadata, not data

`attr` reads the claim attached to a value:

```q
attr 1 2 3                / no claim has been made
attr til 5                / sorted in FACT, but nothing is asserted
attr asc 1 3 2            / asc did the sorting, so asc can vouch for it
attr distinct 1 2 3       / distinct does NOT leave `u# behind
```

```
`
`
`s
`
```

Two of those deserve a second look. `til 5` is `0 1 2 3 4` — sorted by construction, sorted by any
definition you like, and carrying **no** attribute. And `distinct` returns a list whose elements
are unique by definition, also carrying nothing. Attributes are not deduced. q does not scan your
data looking for properties to record; it records the ones a primitive happened to establish on
its way through (`asc` sorts, so `asc` knows) or the ones you assert by hand.

And the claim is genuinely outside the value:

```q
(`s#1 2 3) ~ 1 2 3                                 / ~ compares values
(where (`s#1 2 3 4 5)>2) ~ where 1 2 3 4 5>2       / same answer either way
```

```
1b
1b
```

This is the property to hold onto hardest, because it is the one that survives into the part of
the lesson where things go wrong. **An attribute can never change a result.** A constraint like
`` select from t where sym=`AAPL `` over an attributed column may reach its rows by binary search
or a hash lookup instead of a scan, but it is the *same set of rows*. Any belief of the form "I set
`` `g# ``, so now this query is right" is confused at the root: if the query is right with the
attribute, it was right without it.

---

## 2. q checks the claim when you make it

You cannot simply assert something false:

```q
`s#3 1 2       / not ascending
`u#1 1 2       / not unique
`p#1 2 1       / equal values not adjacent
`g#1 2 1
```

```
"ERROR: s-fail"
"ERROR: u-fail"
"ERROR: u-fail"
`g
```

(The runnable file traps these and prints the message; uncaught at a REPL, the first renders as
`'2026.07.29T12:59:45.680 s-fail` — q stamps the line with a wall-clock time, as lesson 01's parse
error also showed.) So there is a real check, and it costs a real pass over the data. Note the
third one: `` `p# `` — *parted*, meaning equal values occupy contiguous blocks — reports `u-fail`
rather than a `p-fail` of its own.

`` `g# `` is the exception that explains the family. It never fails, because "group this list"
is an operation that succeeds on any list at all: it builds a hash from each distinct value to the
positions where it occurs — precisely lesson 03's `group`, kept as an index. The other three
attributes assert a property the data must *already* have. `` `g# `` asserts nothing; it builds
something.

---

## 3. …and drops it, silently, the moment it might not hold

Here is where the SQL model breaks:

```q
s1:`s#1 2 3; s1,:4;   attr s1
s2:`s#1 2 3; s2,:0;   attr s2
s2
s3:`s#1 2 3; s3[2]:5; attr s3
s4:`s#1 2 3; s4[2]:3; attr s4
p1:`p#`a`a`b`b; p1,:`c; attr p1
u1:`u#1 2 3; u1,:4;   attr u1
u2:`u#1 2 3; u2,:1;   attr u2
```

```
`s
`
1 2 3 0
`
`
`
`u
`
```

Read that column of outputs slowly, because four different things are happening in it.

`s1` appended `4` to `1 2 3` and **kept** `` `s ``: the claim is still true and q could tell
cheaply, by comparing the new element to the last one. `s2` appended `0` and the attribute is
gone — and notice what that is *not*. It is not an error. `s2` is `1 2 3 0`, exactly the data you
asked for; the append succeeded completely. q did not reject your write to protect the index. It
dropped the index to protect the answer.

`s3` is the one that catches people. It assigns `5` at position 2, giving `1 2 5` — which is still
sorted, still perfectly eligible for `` `s ``. The attribute is gone anyway. And `s4` removes the
last possible doubt: it writes `3` at position 2, the value that was *already there*, producing a
vector identical to the one it started with — and still loses the attribute.

q did not re-derive whether the claim survived, because re-deriving it means another full pass,
and the entire point of the attribute is to avoid full passes. **The rule is not "q maintains your
attribute". It is "q keeps the attribute when a cheap local check proves it survived, and abandons
it otherwise."** An append has such a check — compare the new element to the last one. Indexed
assignment does not, so it abandons unconditionally, `s4` included.

`p1` shows the extreme case: the parted attribute is removed by *any* operation on the list, even
an append that visibly preserves partedness. And `u1`/`u2` show the cheap-check rule once more —
appending `4` to `1 2 3` keeps `` `u ``, appending a duplicate `1` drops it.

The practical consequence is the opposite of the SQL habit. There, you create an index once and
forget it. Here, an attribute is a **perishable** property of a particular vector at a particular
moment, and the discipline is to set it *after* you finish building the data, as the last step
before you start querying — which is exactly what the showcase does.

---

## 4. Sort discipline: `xasc` stamps only the first column

The table this lesson has been heading towards, entered deliberately out of order:

```q
quote:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL;
          time:10:00:02 10:00:04 10:00:00 10:00:01 10:00:05;
          bid :99.1 200.3 98.5 200.0 99.4)
```

```
sym  time     bid
-------------------
AAPL 10:00:02 99.1
MSFT 10:00:04 200.3
AAPL 10:00:00 98.5
MSFT 10:00:01 200
AAPL 10:00:05 99.4
```

```q
sorted:`sym`time xasc quote
```

```
sym  time     bid
-------------------
AAPL 10:00:00 98.5
AAPL 10:00:02 99.1
AAPL 10:00:05 99.4
MSFT 10:00:01 200
MSFT 10:00:04 200.3
```

```q
attr sorted`sym
attr sorted`time
```

```
`s
`
```

`xasc` sorted by both columns but attributed only the first, and that is not an oversight — it is
the only honest answer available. Look at the `time` column of the sorted table: `10:00:00`,
`10:00:02`, `10:00:05`, `10:00:01`, `10:00:04`. It is **not** ascending. It ascends *within each
sym* and resets at the boundary. There is no attribute in q that says "ascending within groups of
another column", so `time` gets nothing.

That missing attribute is the whole subject of this lesson. The property that `aj` depends on is
exactly the property q has no way to record.

---

## 5. What `aj` actually depends on

The reference is blunt about the mechanism: `aj` appends **"the last (in row order) matching
record"** from the quote table. Not the record with the greatest time — the *last one it walks
past*. Row order is the semantics.

```q
trade:([] sym:`AAPL`MSFT; time:10:00:03 10:00:02; price:99.25 200.1)
```

```
sym  time     price
-------------------
AAPL 10:00:03 99.25
MSFT 10:00:02 200.1
```

AAPL trades at `10:00:03`. The prevailing quote is the `10:00:02` one, so the correct bid is
**99.1**. Now four joins against the same data in four different states:

```q
aj[`sym`time; trade; quote]                      / unsorted, no attribute
```

```
sym  time     price bid
------------------------
AAPL 10:00:03 99.25 98.5
MSFT 10:00:02 200.1 200
```

**98.5** — wrong, and utterly silent. In the unsorted table AAPL's rows appear in the order
`10:00:02`, `10:00:00`, `10:00:05`; the last one `aj` walks past with a time at or before
`10:00:03` is the `10:00:00` row, so the trade gets matched to a quote three seconds stale.

Now set the attribute the way a SQL reflex would — index the table, then join:

```q
aj[`sym`time; trade; update `g#sym from quote]   / unsorted, WITH `g#
```

```
sym  time     price bid
------------------------
AAPL 10:00:03 99.25 98.5
MSFT 10:00:02 200.1 200
```

Still 98.5. The attribute did not rescue anything, and section 1 already told you it could not:
attributes do not change answers. Setting `` `g# `` on an unsorted quote table buys you a faster
route to the same wrong number.

The converse is just as instructive. Sort the table and set **no** attribute at all:

```q
aj[`sym`time; trade; sorted]                     / sorted, no attribute
```

```
sym  time     price bid
------------------------
AAPL 10:00:03 99.25 99.1
MSFT 10:00:02 200.1 200
```

**99.1** — correct, with nothing indexed. And with both:

```q
aj[`sym`time; trade; update `g#sym from sorted]  / sorted AND attributed
```

```
sym  time     price bid
------------------------
AAPL 10:00:03 99.25 99.1
MSFT 10:00:02 200.1 200
```

Correct, and now also fast. Those four results are the lesson in a box:

|                | no attribute | `` `g#sym `` |
|----------------|--------------|--------------|
| **unsorted**   | 98.5 ✗       | 98.5 ✗       |
| **sorted**     | 99.1 ✓       | 99.1 ✓       |

**The correctness lives entirely in the rows and not at all in the attribute.** The attribute
column changes nothing; the sort row changes everything. If you take one thing from this lesson,
take the shape of that table.

One more probe, to pin down what "sorted" has to mean. It is not enough to group the syms
together — the order *within* each group is the contract:

```q
aj[`sym`time; trade; `sym xasc `time xdesc quote]   / sym-major, time DESCENDING within sym
```

```
sym  time     price bid
------------------------
AAPL 10:00:03 99.25 98.5
MSFT 10:00:02 200.1 200
```

Wrong again. The requirement is precisely "time is non-decreasing within each sym", which
`` `sym`time xasc `` guarantees — and which, as section 4 showed, is the one property no attribute
in the language can express. You maintain it yourself, and nothing checks it for you.

Finally, notice what the MSFT row did through all five joins: nothing. It was `200` every time,
right answer, every state of the table. MSFT has only one quote at or before `10:00:02`, so row
order cannot change which one wins. This is why the bug ships. A wrongly-sorted quote table does
not produce a table of obvious garbage — it produces a table that is *mostly* right, wrong only
for rows whose symbol happened to have several quotes in the window, with no error, no warning,
and no shape change to catch your eye in review.

---

## 6. Which attribute, and the honest answer

The showcase does this, and now every piece of it has a reason:

```q
ready:update `g#sym from `sym`time xasc quote
attr ready`sym
```

```
`g
```

Sort first — that is the correctness step. Attribute second, and last — that is the speed step,
placed after the data is final because section 3 showed attributes are perishable.

Which attribute, though? The `aj` reference gives a table: in memory, `` `g# `` on the first join
column with the rest sorted within it; on disk, `` `p# ``, and it notes that "on disk, the `g#`
attribute does not help". Taken alone that reads like a tidy rule — memory means grouped, disk
means parted — and this repo has already been burned by exactly that reading. The sibling
[set-attribute](https://code.kx.com/q/ref/set-attribute/) page says something the `aj` page does
not: *"If the data can be sorted such that `p` can be set, it effects better speedups than
grouped, both on disk and in memory."*

Both pages are KX's. They are not contradictory — the `aj` page gives a safe default, the
set-attribute page gives the ceiling — but a reader who has only seen one of them will state the
rule too strongly, and a table you have already sorted `` `sym`time xasc `` is exactly a table
where `` `p# `` is available. `` `g# `` is the reasonable default this lesson ships and the
showcase uses; `` `p# `` on an already-sorted table is defensible and may be faster. What is
*not* defensible is claiming either one is the single right answer on the strength of one page.

---

## The J twin: the same discipline, with nowhere to write it down

```j
times =: 0 2 5                NB. one symbol's quote times, ascending
bids  =: 98.5 99.1 99.4
echo times I. 3               NB. insertion point
echo bids {~ <: times I. 3    NB. "prevailing bid at t=3"

utimes =: 2 0 5               NB. same data, rows permuted
ubids  =: 99.1 98.5 99.4
echo utimes I. 3
echo ubids {~ <: utimes I. 3
```

```
2
99.1
2
98.5
```

`I.` is J's interval index: a binary search that **assumes** its left argument is sorted. On
`times` it finds the right slot and the prevailing bid is `99.1`. On the permuted `utimes` it
returns an index with the same confidence and the same absence of complaint, and the answer is
`98.5` — the identical wrong number q produced, for the identical reason, because the two rows
were swapped.

(That the numbers match is constructed, not cosmic: `utimes`/`ubids` are the q quote table's row
order. The point of building it that way is that the failure is genuinely the same failure.)

What J lacks is not the sortedness — `times` is just as sorted as q's column. What J lacks is any
place to *say so*:

```j
echo /: utimes                NB. the grade: how to reorder
echo (/: utimes) { utimes
echo (/: utimes) { ubids
```

```
1 0 2
0 2 5
98.5 99.1 99.4
```

J will sort for you, but `/:` hands back a **permutation** — `1 0 2`, the instruction — and you
must apply it yourself to every parallel list, exactly the `~. w`-alongside-`#/.~ w` problem from
lesson 03 in a new costume. Once applied, the result is an ordinary list that remembers nothing
about how it was made.

So both languages put the sort discipline on the programmer, and neither will catch you breaking
it. q's contribution is narrower than it first appears and more valuable than it sounds: it gives
you a **place to record the claim**, a check that runs when you make it, and the courtesy of
withdrawing it rather than lying when it can no longer vouch for it. `attr` is a question you can
ask. J has no such question.

That is the honest size of the feature. Attributes are not an index that keeps you right. They
are documentation that q occasionally validates.

---

## What to carry forward

- **An attribute is a claim about a vector, not part of its value.** `~` ignores it, and it can
  never change an answer — only how fast q reaches the same one.
- **Attributes are asserted, not deduced.** `til 5` is sorted and carries nothing; `distinct` is
  unique and carries nothing. Only primitives that established the property (`asc`, `xasc`, `by`)
  attach one for free.
- **q checks the claim once, when you set it** (`s-fail`, `u-fail`) — so you cannot lie outright.
  `` `g# `` never fails because it *builds* an index rather than asserting a property.
- **Attributes are perishable and drop silently.** Kept when a cheap local check proves they
  survived (in-order append), abandoned otherwise — even by an indexed assignment that happens to
  preserve the property. `` `p# `` is dropped by any operation at all. Set attributes **last**,
  after the data is final.
- **`xasc` attributes only the first sort column**, because the second is ascending only *within*
  groups of the first — and q has no attribute for that property. The one thing `aj` needs is the
  one thing that cannot be recorded.
- **`aj`'s correctness comes from row order, not from the attribute.** It takes the last matching
  record *in row order*. Sorted-without-attribute is right; attributed-without-sorting is wrong.
  Sort for correctness, attribute for speed, in that order.
- **The wrong-sort bug is partial and silent** — only rows with several quotes in the window go
  wrong, so the output looks mostly fine and passes review.

**Next:** the showcase — [as-of join, end to end](../../showcase/aj/), where a real trade table
meets a real quote table and every line of the sort-then-attribute preamble is now something you
can read rather than copy.

---

### References

- Attributes, the `s`/`u`/`p`/`g` family, and what survives an append:
  [code.kx.com — Set Attribute](https://code.kx.com/q/ref/set-attribute/)
- `attr` (read the attribute of a value): [code.kx.com — attr](https://code.kx.com/q/ref/attr/)
- `aj`, the row-order semantics, and the memory/disk attribute table:
  [code.kx.com — aj](https://code.kx.com/q/ref/aj/)
- `xasc` (sort a table by columns): [code.kx.com — xasc](https://code.kx.com/q/ref/asc/#xasc)
- J's `I.` interval index (binary search, sortedness assumed):
  [J Dictionary — Indices / Interval Index](https://www.jsoftware.com/help/dictionary/dicapdot.htm)
- J's `/:` grade up: [J Dictionary — Grade Up / Sort](https://www.jsoftware.com/help/dictionary/d422.htm)
