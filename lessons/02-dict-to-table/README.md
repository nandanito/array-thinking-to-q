# Lesson 02 — dict → table

> **Run it:** `$HOME/.kx/bin/q lessons/02-dict-to-table/q/dict-to-table.q -q < /dev/null`
> (the tool binaries are not on `PATH` — see the [Part II index](../README.md)).
> Every output below is captured from KDB-X CE 5.0; the J twin from J 9.7.1.
> Files: [`q/dict-to-table.q`](q/dict-to-table.q), [`j/transpose.ijs`](j/transpose.ijs).

You have already used q tables — the `aj` showcase and the eval tasks are full of `([] … )`.
This lesson is the one that makes them stop being magic. There is no "table" primitive to
memorise. **A table is a dictionary you flipped, and a keyed table is a dictionary again.** Two
things you already have — dictionaries and lists — compose into everything q calls a table, and
once you see the seam, qSQL reads as sugar over two ordinary moves.

This is the conceptual centre of Part II. Take it slowly.

---

## 1. A dictionary is two lists

A dictionary maps a list of keys to a list of values — that is the whole definition. `!` builds one:

```q
d:`a`b`c!10 20 30
```

```
q)d
a| 10
b| 20
c| 30
```

`d` is not a new kind of thing hiding a hash table you cannot see; it is the keys list and the
values list, associated. Everything a dictionary does follows from that:

```q
d[`b]      / 20        — look up by key
key d      / `a`b`c    — get the keys list back
value d    / 10 20 30  — get the values list back
type d     / 99h       — the DICTIONARY type; remember this number
```

Hold on to `99h`. It is going to reappear somewhere surprising.

---

## 2. A column dictionary

Nothing said the values had to be atoms. Make each value an **equal-length list**:

```q
cd:`sym`px!(`AAPL`MSFT`GOOG; 100 200 300)
```

```
q)cd
sym| AAPL MSFT GOOG
px | 100  200  300
```

This is still just `keys!values` — but now each key names a whole **column**. `cd` is a
*dictionary of columns*: it already holds tabular data, merely oriented column-wise. It is one
transpose away from looking like a table, and q spells transpose `flip`.

---

## 3. `flip` is transpose — and a *named* flip is a table

`flip` is the ordinary array transpose. On plain lists it swaps rows and columns:

```q
flip (1 2 3; 4 5 6)
```

```
1 4
2 5
3 6
```

(That is exactly what J's `|:` does — see the twin at the end.) Now apply the *same* `flip` to the
column dictionary:

```q
t:flip cd
```

```
q)t
sym  px
--------
AAPL 100
MSFT 200
GOOG 300
```

There is your table — header, rows, the shape you have been writing all along. q even gives it its
own type:

```q
type t          / 98h   — "table" is a named type...
t ~ flip cd     / 1b    — ...but t is *literally* flip cd, nothing added
```

So a table earns its own type number (`98h`) for convenience, but structurally it is **the flip of
a column dictionary and not one atom more.** The names are the entire difference between q's `flip`
and J's `|:`: J transposes anonymous *positions* and gets another matrix; q transposes *named*
columns and gets a thing you can query by name. Names are why q has qSQL and J does not.

---

## 4. The `([] … )` literal is just sugar for that flip

Every table literal you have written is this same flipped dictionary with friendlier syntax:

```q
t ~ ([] sym:`AAPL`MSFT`GOOG; px:100 200 300)     / 1b
```

`([] … )` lets you write the columns in the natural top-to-bottom order and flips for you. The
`aj` showcase's `([] sym:…; time:…; price:… )` was never special syntax — it was `flip` of a
column dictionary, wearing a nicer coat.

---

## 5. Rows are dictionaries, columns are lists — both views free

Because a table is a flipped column-dict, the two ways you might want to slice it are both already
sitting there. Index by row number and you un-flip one slice back into a **dictionary**:

```q
t 0
```

```
sym| `AAPL
px | 100
```

Index by column name and you get the underlying **list** straight out of the dict:

```q
t[`px]              / 100 200 300
exec sym from t     / `AAPL`MSFT`GOOG   — the same list, via qSQL
```

This is the payoff. A **row is a dictionary**, a **column is a list**, and you paid nothing extra
for either — they are the two axes of the same flipped structure. qSQL's `select`/`exec` are a
readable surface over exactly these two moves; there is no third hidden mechanism underneath.

---

## 6. A keyed table *is* a dictionary

Key the table on `sym` — promote a column to the row label:

```q
kt:`sym xkey t
```

```
q)kt
sym | px
----| ---
AAPL| 100
MSFT| 200
GOOG| 300
```

The `|` in the display is the tell. Ask its type:

```q
type kt     / 99h
```

`99h` — the **dictionary** type from step 1. A keyed table is not a fourth new thing; it is a
dictionary whose keys and values are *both tables*:

```q
98h ~ type key kt       / 1b   — the key half is a table
98h ~ type value kt     / 1b   — the value half is a table
```

So look-up works exactly as it did for `d` in step 1 — hand it a key, get back the matching value.
Here the "value" is a one-row record, i.e. a dictionary:

```q
kt[`AAPL]
```

```
px| 100
```

And the circle closes: **dictionary → (flip) → table → (key it) → dictionary.** There was never a
tower of four independent data types to memorise. It is dictionaries and lists, composed two ways.

---

## The J twin: transpose without names

```j
m =: 2 3 $ 1 2 3 4 5 6    NB. a 2x3 matrix, built by reshape ($)
m                         NB. two rows of three
|: m                      NB. |: transposes it: three rows of two
```

```
1 2 3
4 5 6
1 4
2 5
3 6
```

`|: m` gives `1 4 / 2 5 / 3 6` — byte-for-byte what q's `flip (1 2 3; 4 5 6)` produced in step 3.
The *transpose* is shared; the array instinct carries straight over. What does **not** carry over is
naming. J's matrix has rank and position but no column names, so its transpose is just another
matrix — there is no J-native `select … from` because there is nothing named to select. q trades
J's rank machinery for **named columns**, and that trade is the whole reason a q `flip` produces a
*table* while a J `|:` produces a *matrix*. (This is the flip side of lesson 01's wall: J has the
tacit array plumbing q lacks; q has the named, queryable structure J lacks.)

---

## What to carry forward

- **A dictionary is `keys!values`** — two lists, associated. `key`/`value` recover them; `type` is
  `99h`.
- **A table is `flip` of a column dictionary** (`type` `98h`), and `([] … )` is just sugar for it.
  No new primitive.
- **A row is a dictionary; a column is a list.** Both fall out of the flip for free, and qSQL is a
  surface over those two moves.
- **A keyed table is a dictionary** (`type` `99h` again) mapping a key-table to a value-table.
- The entire model is **dictionaries and lists, composed** — `flip` to get a table, key it to get a
  dictionary back. Names are what q buys with the rank it gives up (the J twin).

**Next:** Lesson 03 — qSQL (`select … by … from`) *(planned)*, where `select`, `exec`, and `update`
turn out to be readable surface over the row-dict / column-list views you just met.

---

### References

- Dictionaries & tables ("Flip it and we see a table"):
  [code.kx.com — Dictionaries](https://code.kx.com/q/basics/dictsandtables/)
- `keys` / `xkey` (keyed tables): [code.kx.com — keys, xkey](https://code.kx.com/q/ref/keys/)
- Why J's transpose carries positions, not names — J's rank model:
  [Learning J, Ch 7: Ranks](https://www.jsoftware.com/help/learning/07.htm)
