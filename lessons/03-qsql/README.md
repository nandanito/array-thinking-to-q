# Lesson 03 — qSQL

> **Run it:** `$HOME/.kx/bin/q lessons/03-qsql/q/qsql.q -q < /dev/null`
> (the tool binaries are not on `PATH` — see the [Part II index](../README.md)).
> Every output below is captured from KDB-X CE 5.0; the J twin from J 9.7.1.
> Files: [`q/qsql.q`](q/qsql.q), [`j/group-and-window.ijs`](j/group-and-window.ijs).

You already know SQL, and that is the problem. qSQL looks like SQL and reads like SQL, so the
instinct is to import SQL's *execution model* along with its syntax: a row-processing engine,
aggregates as a special class of function, `GROUP BY` as something the engine does to rows.

None of that is here. `select … by … from` is a readable surface over exactly the two moves from
lesson 02 — **a column is a list, a row is a dictionary** — and nothing else. Every phrase you
write inside a `select` is an ordinary q expression evaluated on whole columns, and `by` hands
back a keyed table, which is to say a dictionary you have already met.

The table for this lesson:

```q
t:([] sym :`AAPL`MSFT`AAPL`MSFT`AAPL`GOOG;
      side:`B`S`S`B`B`S;
      qty :100 200 150 50 300 250;
      px  :187.5 411.2 188.1 410.9 187.9 174.3)
```

```
sym  side qty px
-------------------
AAPL B    100 187.5
MSFT S    200 411.2
AAPL S    150 188.1
MSFT B    50  410.9
AAPL B    300 187.9
GOOG S    250 174.3
```

---

## 1. Every phrase is a whole-column expression

```q
select notional:qty*px from t
```

```
notional
--------
18750
82240
28215
20545
56370
43575
```

Read that the imperative way and you get "for each row, multiply `qty` by `px`". That is not what
happened. `qty` and `px` are two six-element lists, `qty*px` is **one vector multiply** — the very
same operation as lesson 01's `2 * til 5` — and `select`'s entire contribution was to name the
result and wrap it in a table. There is no per-row visit to optimise away, because there was never
a row loop to begin with.

The point sharpens with an aggregate:

```q
select sum qty from t
```

```
qty
----
1050
```

In SQL, `SUM` is a distinguished thing: an *aggregate function*, which the engine treats specially
and which drags along rules about what else may appear in the `SELECT` list. In q, `sum` is the
same `sum` from lesson 01, applied to the same column list. `select` does not know or care that it
is "an aggregate". You got one row back for one reason only: **`sum` of a list is an atom**, and a
one-atom column is a one-row table. Change the function and the shape follows the function.

One practical wrinkle. If you do not name a derived column, q invents a name:

```q
cols select qty*px from t     / ,`qty  — it reused a column name from the expression
cols select 2*qty from t      / ,`x    — and here it fell back to `x
```

(The leading `,` is q showing you a *one-element list* rather than an atom — lesson 01's
distinction, made visible in the display.) The invented name is not worth learning: name your
derived columns.

---

## 2. `where` is a boolean vector

Pull the constraint out of the query and evaluate it on its own:

```q
(t`sym)=`AAPL
```

```
101010b
```

A boolean vector — lesson 01's `(til 5) > 2`, nothing more. There is no predicate being called
once per row; there is one vector comparison producing six booleans, which `select` then uses to
pick rows:

```q
select from t where sym=`AAPL
```

```
sym  side qty px
-------------------
AAPL B    100 187.5
AAPL S    150 188.1
AAPL B    300 187.9
```

Multiple constraints are separated by commas, and this is **not** an `and`. They apply *in
sequence*, each one evaluated only against the rows its predecessor kept:

```q
select from t where sym=`AAPL, qty>100
```

```
sym  side qty px
-------------------
AAPL S    150 188.1
AAPL B    300 187.9
```

`qty>100` never saw the MSFT or GOOG rows. For pure filters the surviving rows are the same
whichever order you write them in, but the *work* is not: put the most selective constraint first
and every later constraint runs on a shorter vector. This is the first place in the lesson where q
gives you a performance lever by exposing its evaluation order rather than hiding it behind a
planner.

---

## 3. `by` gives you back a dictionary

```q
r:select sum qty by sym from t
```

```
sym | qty
----| ---
AAPL| 550
GOOG| 250
MSFT| 250
```

That `|` in the display should be familiar from lesson 02, and so should the type:

```q
type r              / 99h   — a keyed table IS a dictionary
98h~type key r      / 1b    — the key half is a table
98h~type value r    / 1b    — the value half is a table
```

A grouped query result is not a special "result set" object. It is the *same keyed table* you
would get by building a table and calling `` `sym xkey `` on it — so it is a dictionary, so you
index it with a key like any other dictionary:

```q
r[`AAPL]
```

```
qty| 550
```

Lesson 02 ended on the circle **dictionary → (flip) → table → (key it) → dictionary**. `by` is
that last step, performed on the fly by the query. You are not learning a new mechanism here; you
are watching one you already know get a keyword.

---

## 4. `by` does not mean "aggregate by"

Here is the query SQL will not let you write:

```q
select px by sym from t
```

```
sym | px
----| -----------------
AAPL| 187.5 188.1 187.9
GOOG| ,174.3
MSFT| 411.2 410.9
```

`SELECT px FROM t GROUP BY sym` is an error in any standards-respecting SQL, because SQL has no
way to *put* three prices in one row's cell. q does: cells hold lists, and a column of lists is an
ordinary column. So q simply hands back the groups.

This is the definition to take away. **`by` means "cut every selected column into one list per
group."** That is all it means. Aggregation is not part of it — aggregation happened in section 3
only because you wrote `sum`, and `sum` of a list is an atom. Wrote nothing? You get the lists.
Wrote `avg`? You get means. The grouping and the summarising are two separate ideas that SQL welds
together and q leaves apart, which is why `by` is strictly more general than `GROUP BY`.

(`,174.3` is GOOG's group: one trade, so a one-element *list*, and q marks it with the leading
comma so you do not mistake it for an atom. Lesson 01's atom/list distinction, still earning its
keep.)

Aggregates compose freely once you stop treating them as special:

```q
select n:count i, tot:sum qty, avg px by sym from t
```

```
sym | n tot px
----| --------------
AAPL| 3 550 187.8333
GOOG| 1 250 174.3
MSFT| 2 250 411.05
```

`count i` is the row-count idiom: `i` is the virtual index column every table has, so `count i` is
"how many rows in this group".

---

## 5. The grouping behind `by` is a plain function: `group`

`by` is a keyword, but the operation it names is a function you can call yourself:

```q
w:`the`cat`sat`on`the`mat`the
group w
```

```
the| 0 4 6
cat| ,1
sat| ,2
on | ,3
mat| ,5
```

`group` maps each distinct value to the **indices** where it occurs — a dictionary, of course.
That is the same grouping `by` performs, handed to you as an ordinary function: everything a
grouped query does is this dictionary plus something applied to each group's slice.

Which makes word frequency a one-liner, with no table and no query anywhere in sight:

```q
count each group w
```

```
the| 3
cat| 1
sat| 1
on | 1
mat| 1
```

Compare the instinct this replaces: initialise a hash map, loop the words, increment or insert.
Three concepts (a mutable accumulator, iteration, a conditional) for something that is really one
question — *how big is each group?* — asked of a structure q already gave you. `group` supplies
the groups, lesson 01's `each` supplies the "for each of them", and `count` answers. Nothing is
accumulated and nothing is mutated.

The qSQL spelling is the same computation:

```q
exec count i by w from ([] w:w)
```

```
cat| 1
mat| 1
on | 1
sat| 1
the| 3
```

Same counts — **different order**, and this one bites people:

```q
(count each group w) ~ exec count i by w from ([] w:w)   / 0b
attr key exec count i by w from ([] w:w)                 / `s
```

`group` preserves **first-appearance** order; `by` **sorts** its keys. That difference alone is why
`~` says `0b` here, even though every count agrees.

The `` `s `` is a second, separate thing: `by` also stamps its sorted keys with the `` `s# ``
attribute. It is *not* what broke the `~`, because attributes are metadata about a value rather
than part of it, and `~` does not look at them:

```q
(`s#1 2 3) ~ 1 2 3
```

```
1b
```

So choose on ordering alone: `group` when first-appearance order carries meaning, `by` when you
want keys sorted. The attribute rides along for free — and that `` `s `` is lesson 04's whole
subject.

---

## 6. Windows: `mavg`, and the `by` that makes it correct

A moving average is the other thing everyone reaches for a loop to write, and q has it as a verb:

```q
3 mavg 1 2 3 4 5 6f
```

```
1 1.5 2 3 4 5
```

Six inputs, six outputs. The first two windows are **partial** — `1` is the average of just `1`,
`1.5` the average of `1 2` — and from the third element on you get true 3-wide windows. q's
windowed verbs ramp up rather than refusing to answer — the whole `m`-family shares the
convention, so `n` inputs always give you `n` outputs:

```q
3 msum 1 2 3 4 5 6
3 mmax 1 2 3 4 5 6
3 mmin 1 2 3 4 5 6
```

```
1 3 6 9 12 15
1 2 3 4 5 6
1 1 1 2 3 4
```

Now the version that matters, because a real table has more than one instrument in it:

```q
update ma:2 mavg px by sym from t
```

```
sym  side qty px    ma
--------------------------
AAPL B    100 187.5 187.5
MSFT S    200 411.2 411.2
AAPL S    150 188.1 187.8
MSFT B    50  410.9 411.05
AAPL B    300 187.9 188
GOOG S    250 174.3 174.3
```

`by` inside an `update` does something `select … by` does not: it cuts into groups, runs the
window *within each group*, and writes the results **back in the original row order**. The table
keeps its shape — same six rows, same sequence, one new column. AAPL's third trade averages 188.1
and 187.9, its own two most recent prices, and MSFT's rows are untouched by AAPL's.

Drop the `by` and q does not complain:

```q
update ma:2 mavg px from t
```

```
sym  side qty px    ma
--------------------------
AAPL B    100 187.5 187.5
MSFT S    200 411.2 299.35
AAPL S    150 188.1 299.65
MSFT B    50  410.9 299.5
AAPL B    300 187.9 299.4
GOOG S    250 174.3 181.1
```

`299.35` is the average of an AAPL price and an MSFT price. It is not a price of anything. No
error, no warning, a full column of confident nonsense.

This is worth sitting with, because it is the *actual* failure mode of the imperative instinct in
q — and it is not the one you were braced for. Nobody wrote a loop here. The bug is subtler: a
column is **one vector spanning every group**, and any operation with memory (a window, a
difference, a cumulative sum) will happily run straight across the boundary between two
instruments unless you tell it not to. In a row-at-a-time language you would have had to
deliberately write code to mix the symbols. In q, mixing them is the default and separating them
is the thing you must ask for. `by` is how you ask.

---

## 7. `exec` unwraps what `select` wraps

The same question, two keywords, three different shapes. First `select`:

```q
select sum qty by sym from t
```

```
sym | qty
----| ---
AAPL| 550
GOOG| 250
MSFT| 250
```

Now the identical query with `exec`:

```q
exec sum qty by sym from t
```

```
AAPL| 550
GOOG| 250
MSFT| 250
```

No header, no `----` rule: this is a plain dictionary, not a keyed table. And on a single column:

```q
exec qty from t
```

```
100 200 150 50 300 250
```

`select` always returns a table (or a keyed table). `exec` returns the **underlying structure**:
one column becomes the raw list, and `by` becomes a plain key→value dictionary rather than a
keyed table. Use `exec` when you want the data to hand to another q expression, `select` when you
want a table to keep querying. Lesson 02's `exec sym from t` was this rule in miniature.

---

## The J twin: grouping and windows, without names

```j
w =: ;: 'the cat sat on the mat the'   NB. ;: cuts a string into boxed words
#/.~ w                                 NB. /. is "key": group by value, then apply #
~. w                                   NB. the labels are a SEPARATE result
3 (+/ % #)\ 1 2 3 4 5 6                NB. 3-wide windows — COMPLETE ones only
```

```
3 1 1 1 1
┌───┬───┬───┬──┬───┐
│the│cat│sat│on│mat│
└───┴───┴───┴──┴───┘
2 3 4 5
```

J's key adverb `/.` is the same operation as q's `group`: it groups items by value and applies a
verb to each group. So `#/.~ w` — "count each group" in J's spelling — gives `3 1 1 1 1`, the
same five counts q produced.

Look at what J *doesn't* give you. The counts arrive as a bare list. The labels are a second,
independent computation (`~. w`), and the two align only because both are documented to run in
first-appearance order. That is a guarantee you have to know and keep holding — nothing in the
data structure enforces it, and one sort applied to either list breaks the correspondence
silently. q's `by` returns the labels **attached**, as the key half of a keyed table.

That is lesson 02's names-versus-positions contrast again, now with visible consequences. Because
q's groups carry their own labels, a grouped result is still a table: you can key into it, join it,
filter it, group it again. J's grouped result is a list that means something only in the presence of
another list you must keep in step yourself. This is the whole reason `select … by … from` can
exist in q and has no J-native counterpart — there is nothing named to select, and nothing named
to group *by*.

The last line is a translation trap worth memorising. `3 (+/ % #)\` gives **four** results from
six inputs: J's infix `\` yields complete windows only. q's `3 mavg` gave **six**, ramping up
through the partial windows at the start. Neither convention is wrong, but "the 3-period moving
average" is a different-length answer in the two languages, and a translated array idiom that
silently changes the length of its result is exactly the kind of bug that survives review.

---

## What to carry forward

- **Every phrase in a `select` is an ordinary expression over whole columns.** `sum` is not a
  special aggregate class — you get one row because `sum` of a list is an atom.
- **`where` is a boolean vector**, and comma-separated constraints apply *in sequence*, each on
  the rows the previous kept. Most selective first.
- **`select … by` returns a keyed table, which is a dictionary** (`99h`) — lesson 02's circle,
  closed by a keyword.
- **`by` means "cut each column into one list per group"**, not "aggregate". Aggregation is
  whichever function you applied. This is why `by` is more general than `GROUP BY`.
- **`group` is that same grouping as a plain function**, mapping value → indices; `count each
  group w` *is* word frequency. `group` keeps first-appearance order, `by` sorts keys — that
  ordering difference alone is what a `~` comparison catches, since `~` ignores the `` s# ``
  attribute `by` also attaches.
- **`mavg`/`msum` are windows without loops**, with partial windows at the start. Inside `update`,
  **`by` computes per group and writes back in row order** — and omitting it silently averages
  across instruments, the real imperative failure mode in q.
- **`exec` unwraps, `select` wraps.**

**Next:** Lesson 04 — attributes & sort discipline (`` s# ``/`` g# ``/`` p# ``) *(planned)*, where
the `` `s `` that `by` quietly attached to its keys stops being a detail and becomes a correctness
requirement — the one the `aj` showcase depends on.

---

### References

- qSQL `select`/`exec`/`update`, and the sequential `where` phrases:
  [code.kx.com — qSQL query templates](https://code.kx.com/q/basics/qsql/)
- `group` (value → indices): [code.kx.com — group](https://code.kx.com/q/ref/group/)
- `mavg` and the moving-window verbs:
  [code.kx.com — mavg](https://code.kx.com/q/ref/avg/#mavg)
- J's key adverb `/.`:
  [J Dictionary — Oblique / Key](https://www.jsoftware.com/help/dictionary/d421.htm)
- J's infix `\` (complete windows only):
  [J Dictionary — Prefix / Infix](https://www.jsoftware.com/help/dictionary/d430.htm)
