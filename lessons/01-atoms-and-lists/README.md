# Lesson 01 — Atoms, lists, and the death of the loop

> **Run it:** `q lessons/01-atoms-and-lists/q/atoms.q -q < /dev/null`
> Every output below is captured from KDB-X CE 5.0; the J twin from J 9.7.1.
> Files: [`q/atoms.q`](q/atoms.q), [`j/mean-fork.ijs`](j/mean-fork.ijs).

You already know how to add up a list of numbers. The question this lesson asks is not *how* —
it is *where the iteration lives*. In the language you came from, iteration is something **you**
do: you write the loop, name the index, and step through. In q, iteration is something the
**operator** does, and your job is to stop writing the loop. That is the whole shift, and it
starts with the smallest possible distinction: an atom is not a list of length one.

---

## 1. An atom is not a one-element list

```q
type 42            / -7h    an atom: the type number is NEGATIVE
type til 5         /  7h    a list:  same datatype, POSITIVE
count 42           /  1     an atom still answers `count` — with 1
count til 5        /  5
```

`til 5` is q's `0 1 2 3 4` — "the integers below 5." Notice `type` reports the **same**
underlying datatype for `42` and for `til 5` (`7` is "long"), but flips its **sign**: negative
for an atom, positive for a list. q encodes *shape* in the type itself. That sign is your first
signal that q is tracking structure everywhere, and it is what lets most operators be **atomic** —
they burrow down to the atoms, do their work, and rebuild the surrounding shape for you. Hold on
to that word *atomic*; it is the reason the loop is about to disappear.

The imperative reflex — "a scalar is just an array of length 1" — is exactly wrong here. `42` and
`enlist 42` (a one-item list) both have `count` 1, but they are **different types**: `type 42` is
`-7h`, `type enlist 42` is `7h`. The atom has no length dimension at all; the list has one that
happens to hold a single element. That distinction is load-bearing, and it is carried in the type,
not the count.

---

## 2. The loop you do not write

Here is the instinct we are here to unlearn. To double every element, you reach for:

```python
out = []
for i in range(5):
    out.append(2 * a[i])      # the index i is scaffolding, not the point
```

In q there is no index and no loop — multiplication simply distributes across the list:

```q
2 * til 5                  / 0 2 4 6 8
(til 5) + 10 20 30 40 50   / 10 21 32 43 54
(til 5) > 2                / 00011b
```

`2 * til 5` multiplies the atom `2` into every element. `(til 5) + 10 20 30 40 50` pairs the two
lists elementwise. `(til 5) > 2` compares each element and hands back a **boolean vector** —
`00011b`, where the trailing `b` marks the type and the digits pack together with no separators
(booleans are that compact in q's display).

None of these iterate *in your code*. `+`, `*`, and `>` are **atomic**: given lists, they map
themselves down to the atoms and reassemble the result in the original shape. The index `i` in the
Python version was never the computation — it was bookkeeping the loop needed and you supplied. q
takes the bookkeeping. You write the intent (`2 *`), and the *where-does-the-iteration-live*
question answers itself: inside the operator.

---

## 3. Reductions, and the machine under the built-in

To collapse a list to a single value you name the reduction:

```q
sum til 5          / 10
avg til 5          / 2f
max til 5          / 4
```

These read like English and you will use them constantly. But `sum` is not primitive magic — it is
`+` **inserted between** the elements: `0 + 1 + 2 + 3 + 4`. q spells "insert a binary operator
between the items of a list" with **over**, the `/` adverb:

```q
(+/) til 5         / 10   — the same 10, now with the mechanism showing
```

`(+/)` is `+` folded across the list. `sum`, `max`, `min`, and `prd` (product) are each just one
operator folded this same way — `+`, `|`, `&`, `*` respectively; `avg` goes one step further (that
sum, divided by the `count`). You reach for a raw `+/` almost never, but seeing it once shows there
is **no black box** under the built-in.

Two small things worth pausing on, because a newcomer trips on both:

- **`avg til 5` is `2f`, not `2`.** The mean of integers is generally not an integer, so q promotes
  the result to a float; the `f` suffix says so. A reduction can change type, and q shows you when
  it does.
- **The parentheses around `(+/)` are not decoration.** To apply a `/`-derived function *prefix*
  (in front of its argument), q's grammar wants it isolated: `(+/) til 5` works, bare `+/ til 5`
  does not parse. In day-to-day q you sidestep the whole issue by using the named fold (`sum`) — but
  when you do write a raw over, wrap it.

---

## 4. `each`, `over`, `scan` — the three shapes of iteration

Once the loop lives in the operator, "iteration" splits into three named shapes:

- **over** (`/`) — collapse a list to one value. You just met it as `sum` / `(+/)`.
- **scan** (`\`) — the *running story* of that same fold: keep every intermediate total.

```q
sums til 5         / 0 1 3 6 10   — the cumulative sum
(+\) til 5         / 0 1 3 6 10   — what `sums` is: `+` SCANNED across the list
```

`over` throws away the intermediate steps and keeps the final answer; `scan` keeps them all.
`sums` is to `scan` what `sum` is to `over` — the named convenience over the raw adverb.

- **each** (`'`) — apply a function to every item **one level down**:

```q
count each ("aa"; "bbb"; "c")   / 2 3 1
```

Here is the subtlety that makes `each` click. The atomic operators from §2 already vectorize — they
dive all the way to the atoms on their own. So `each` is not "how you loop"; it is how you **stop
the diving one level early**. `count each` counts *each string* (2, 3, 1) instead of drilling into
the characters. You reach for `each` precisely when the default all-the-way-down behavior is too
deep. That reframing — `each` is about **controlling depth**, not about looping — is the thing to
carry forward.

---

## 5. The wall: what J shows and q refuses

The array *idea* — reduce, scan, don't loop — came from somewhere, and it is worth seeing it in its
purest form once. In J, "the average" is written as a **fork**: three functions glued into a single
wordless phrase.

```j
sum  =: +/         NB. insert + between items
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), as one phrase
sum  0 1 2 3 4     NB. 10
mean 0 1 2 3 4     NB. 2
```

Read `+/ % #` left to right: *sum, divided by, count*. J notices the shape `(f g h)` and builds a
new function that feeds the argument to `f` and `h` and combines with `g` in the middle. The mean is
a **noun-free sentence**. This is the J laboratory's whole seduction, and it runs (output `2`).

Now transliterate that phrase straight into q:

```q
q)(+/ % #) til 5
'
  [0]  (+/ % #) til 5
          ^
```

It does not merely give a wrong answer — **it does not parse.** The caret points into the middle of
the fork, where q's grammar gives up. (Run it non-interactively and q prefixes the error line with a
timestamp; the error *message* itself is empty — the caret is the whole story.) Crucially this is a
*parse-time* rejection, not a runtime type error: protected evaluation cannot catch it, because
there is nothing to evaluate. **q has no tacit trains or forks.** A parenthesized run of functions
is not a new function in q; it is a syntax error.

What q wants instead is that you say the composition out loud — name it, or use the built-in:

```q
avg til 5                    / 2f
(sum til 5) % count til 5    / 2f
{(sum x) % count x} til 5    / 2f   — the explicit lambda q DOES accept
```

This tiny failure is the entire Part II thesis in one line. **The array *thinking* transfers** —
"a mean is a sum reduced against a count, no loop in sight" is true in both languages. **The tacit
*plumbing* does not.** J is where you *feel* the fork; q is where you *ship*, and it makes you be
explicit about the composition J let you leave silent. Every later lesson lives on the q side of
this wall.

---

## What to carry forward

- An **atom** is not a length-1 list — `type`'s sign proves it (`-7h` vs `7h`), even though both
  answer `count` 1. The distinction is load-bearing.
- **Atomic operators vectorize for you.** `2 * til 5` has no loop because `*` maps to the atoms and
  rebuilds the shape. The index you used to write was scaffolding, not computation.
- **A reduction is a binary operator folded across the list:** `sum` is `(+/)`, `sums` is `(+\)`.
  Name the common ones; know the machine underneath.
- **`each` controls *depth*, not iteration** — it stops an operator diving one level too far.
- **q has no forks.** Compose explicitly (`avg`, a named lambda) — the paradigm crosses over from J,
  the syntax does not.

**Next:** [Lesson 02 — dict → table](../02-dict-to-table/) *(planned)*, where a table turns out to
be nothing more than a flip of a dictionary of these lists.

---

### References

- Atoms, lists, types: [code.kx.com — Datatypes](https://code.kx.com/q/basics/datatypes/)
- `over` / `scan` / `each` (adverbs): [code.kx.com — Iterators](https://code.kx.com/q/ref/iterators/)
- `sum`, `avg`, `sums`, `max`: [code.kx.com — Reference](https://code.kx.com/q/ref/)
- Why q has no J-style forks (tacit composition): J's fork is a
  [J primer](https://www.jsoftware.com/help/primer/fork.htm) concept with no q analogue.
