# Unlearn the loop: what J shows that q hides

*Article 5 of 6 — draft. Gated on M4 (the J laboratory).*

> **Publication gate.** Every snippet below was executed against J 9.7.1 and KDB-X CE 5.0 and the
> outputs are captured, not typed — but the q-side ones come from verified lesson files while the
> J-side ones currently live only in a scratch directory, because Part I does not exist yet. Per
> RELEASE-CHECKLIST.md, this cannot publish until those J snippets sit in lesson files that
> `make verify` runs. Drafted ahead of its milestone deliberately: this is the article the spec
> flagged as at-risk, and banking it early was the mitigation it never got.

---

Here is a perfectly good q program. It sums a list.

```q
x:1 2 3 4 5;
r:0; i:0;
do[count x; r+:x i; i+:1];
show r
```

```
15
```

Fifteen. Correct. It will still be correct next year, on a bigger list, in production.

That is the problem.

## The language will not tell you

q has `do[]`. It has `while[]`. It has `x i` for indexed access, `r+:…` for add-and-reassign, and a
perfectly ordinary notion of a counter you increment yourself. Every reflex you brought from
Python or Java or C has somewhere to land, and the answers come out right.

So you can write q for months — shipping, passing tests, reviewing other people's code — and never
once make the shift the language was built around. Nothing fails. There is no error, no warning, no
performance cliff at the sizes you are testing on. The loop is *right there*, and it works.

I want to be precise about the contrast, because the easy version of this argument is wrong. **It
is not that J forbids loops.** It doesn't:

```j
sumloop =: 3 : 0
r =. 0
for_i. y do. r =. r + i end.
r
)
sumloop 1 2 3 4 5
```

```
15
```

Same fifteen. J has `for_i.`, `while.`, `if.`, local assignment — the whole imperative apparatus.

The difference is what it *costs you in feel*. To write that loop I had to leave J's ordinary
notation entirely: open an explicit definition with `3 : 0`, switch from `=:` to `=.`, name a
variable, name an index, and close the block with a lone `)` on its own line. That is a five-line
block of visibly foreign machinery, in a language where the alternative is `+/`. Nothing stops you.
Everything about it says *you have wandered off*.

The q version says nothing of the kind. `do[count x; r+:x i; i+:1]` is one line of ordinary q,
indistinguishable in texture from the q around it. It doesn't look like a detour. It looks like
Tuesday.

**That is the whole case for the laboratory.** Not that J is stricter, but that J makes the
imperative path *feel* like what it is, and q makes it feel like home. A language that lets you
stay comfortable will not teach you a paradigm shift; you have to go somewhere the shift is
unavoidable, feel it, and come back.

Three things become visible over there — and two of them will betray you on the way back.

---

## 1. Iteration is a modifier, not a statement

In q you learn a vocabulary: `sum`, `sums`, `max`, `group`, `mavg`. Good names, well chosen, and
you can use them for a year without noticing they are instances of anything.

They are. `sum` is `+` inserted between the items — q spells that with the `over` adverb, and
lesson 01 shows the machine under the built-in:

```q
sum til 5          / 10
(+/) til 5         / 10   — the same 10, now with the mechanism showing
```

J never lets the machine out of sight, because J has no `sum` to hide behind. You write `+/` and
you write it every time. `/` is an **adverb**: it takes a verb and returns a modified verb. So is
`\` (scan). So is `/.` (key — group by value, then apply).

Which is a tidy observation until you see what it buys. In J, this is a running total:

```j
+/\ 1 2 3 4 5 6
```

```
1 3 6 10 15 21
```

and this — the *same three characters*, with a left argument in front — is a 3-wide moving sum:

```j
3 +/\ 1 2 3 4 5 6
```

```
6 9 12 15
```

One phrase. Supply a left argument and "scan the prefixes" becomes "scan the windows." The
relationship is right there in the notation: a window is a scan with a width.

Now q:

```q
sums 1 2 3 4 5 6      / 1 3 6 10 15 21
3 msum 1 2 3 4 5 6    / 1 3 6 9 12 15
```

Two names. `sums` and `msum`. Nothing in either spelling suggests they are the same idea with a
parameter — and there is a whole `m`-family (`mavg`, `mmax`, `mmin`, `mcount`, `mdev`) that you
learn as vocabulary rather than derive as a consequence.

q's names are genuinely better for getting work done. `3 mavg px` says what it means to a reader
who has never heard of an adverb. But you can hold that vocabulary completely and still not know
that iteration in this language is a *thing you modify a verb with*, because q never made you say
so out loud.

## 2. Composition is something you can write down

This is J's party trick, and lesson 01 already walks into it:

```j
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), read as one phrase
mean 0 1 2 3 4
```

```
2
```

Read it left to right: *sum, divided by, count*. There is no argument anywhere in that definition.
J sees the shape `(f g h)` and builds a new verb that feeds its argument to `f` and to `h` and
combines the two with `g`. The mean is a **noun-free sentence** — a function assembled out of
functions, with the data never mentioned.

Once you have seen that, "a mean is a sum reduced against a count" stops being a sentence about
arithmetic and becomes a sentence about *structure*. That reframing is the single most valuable
thing the laboratory hands you.

And it is also the first thing that will betray you.

## 3. Depth is a parameter

Here is the one I think q hides most completely.

J has a conjunction, `"`, that sets the **rank** at which a verb applies — the depth of the
sub-arrays it sees. Take a 2×3 matrix:

```j
m =: 2 3 $ 1 2 3 4 5 6
+/ m        NB. + inserted between the ITEMS — and a matrix's items are its ROWS
+/"1 m      NB. rank 1: apply to each row instead
```

```
5 7 9
6 15
```

The first result is `1 2 3 + 4 5 6`, because "insert `+` between the items" means exactly that and
a matrix's items are its rows. The second is one conjunction and a number: `"1` says *apply to each
rank-1 cell*, so each row is summed on its own. `"0` would say each atom; `"2` the whole matrix.
Boxing makes the difference visible without any arithmetic in the way:

```j
<"0 m
<"1 m
```

```
┌─┬─┬─┐
│1│2│3│
├─┼─┼─┤
│4│5│6│
└─┴─┴─┘
┌─────┬─────┐
│1 2 3│4 5 6│
└─────┴─────┘
```

Same verb, same argument; the number chose the depth.

q reaches the same two answers:

```q
sum (1 2 3; 4 5 6)        / 5 7 9
sum each (1 2 3; 4 5 6)   / 6 15
```

— but by a different route, and the route is the point. `each` is not a depth parameter you dial;
it is one specific move, "one level down," and when you need a *different* iteration shape you
reach for a different glyph entirely:

```q
(-':) 1 3 6 10 15   / 1 2 3 4 5     each-prior
1 2 3 ,\: `a        / each-left
`a ,/: 1 2 3        / each-right
```

Four separate iterators — `'`, `':`, `\:`, `/:` — for cases J covers with one conjunction and a
number. Learn them as four facts and you will use them correctly and never notice they are one
concept wearing four hats.

The practical payoff of noticing is immediate. Lesson 01 makes the point that `each` is about
**depth, not looping**, and that the atomic operators (`+`, `*`, `>`) already reach the atoms by
themselves so you never write `each` for those. That is a rule you can memorise. After rank it
isn't a rule any more — it is the obvious consequence of the fact that `*` already applies at rank
0, so asking for `each` is asking for something you already have.

---

## Where the laboratory lies to you

Everything above is why the trip is worth taking. Here is the return fare. Both of these are real,
both are already flagged in the lessons, and the second is by far the more dangerous.

### The fork does not survive the flight

Take `+/ % #` — the phrase that made composition feel like a first-class thing — and type it into q:

```q
q)(+/ % #) til 5
'                     / the error MESSAGE is empty (q also stamps the line with a wall-clock time)
  [0]  (+/ % #) til 5
          ^           / the caret lands mid-fork — where the parser gives up
```

It does not return the wrong answer. **It does not parse.** The message is empty and the caret
lands in the middle of the fork. This is a parse-time rejection, not a runtime error — there is
nothing to evaluate, so protected evaluation cannot catch it either.

**q has no tacit forks or trains.** A parenthesised run of functions is not a new function; it is a
syntax error. What q wants is for you to say the composition out loud:

```q
avg til 5                    / 2f
{(sum x) % count x} til 5    / 2f   — the explicit lambda q DOES accept
```

As betrayals go this one is kind, because it is *loud*. You cannot ship it.

### The windows have a different shape, and nothing complains

This one ships fine.

J's moving average of six numbers, three wide:

```j
3 (+/ % #)\ 1 2 3 4 5 6
```

```
2 3 4 5
```

Four results. J's infix `\` gives you **complete windows only** — there is no 3-wide window ending
at the first or second element, so there is no output for them.

q, same request:

```q
3 mavg 1 2 3 4 5 6f    / 1 1.5 2 3 4 5
```

Six results. q's `m`-family **ramps up through the partial windows**: the first output is the
average of one element, the second of two, and only from the third does a full window exist. Six
inputs, six outputs, always.

Neither convention is wrong. They are different, they are silent about it, and *"the 3-period
moving average"* names both. Carry the J habit into q and anything you align against that column is
shifted — by two rows here, by *width − 1* in general — with no error and a perfectly plausible
answer. That is the exact failure shape this curriculum's `aj` showcase exists to teach.

**The thinking transfers. The plumbing does not.** That is the rule, and both examples above are
just the rule with the volume turned up and down.

---

## Does the shift actually take? Some evidence I did not expect

I ran a controlled evaluation a couple of days ago for a different purpose — [testing whether KX's
official q plugin improves a frontier model's q](03-evaluating-kx-q-plugin.md) — and three of its
fifteen tasks are exactly this article's thesis stated as an exercise: *here is q that was
transliterated from an imperative loop; make it idiomatic.* A `do`-loop accumulating a sum. A
`while` loop building a running total. Row-index iteration over a table. Several of the
Python-to-q translation tasks probe the same instinct from the other side.

Both conditions solved all three, immediately, correctly. `do[]` → `sum`. `while[]` → `sums`.
Row-walk → one vectorised `update`. The loop-transliteration failure mode this whole curriculum is
built to prevent did not appear at all.

What *did* break both conditions was the one task about attributes and sort discipline — applying
`` `p# `` to an in-memory table where [KX's own documentation](https://code.kx.com/q/ref/aj/) calls
for `` `g# ``. Correct rows, wrong attribute, no error.

I find that split genuinely clarifying, and it retroactively justifies a decision I originally made
for much weaker reasons. J started this project as a co-star and got cut to a short laboratory on a
reviewer's advice; I went along with it without real evidence either way. This is the evidence.
**The array-thinking half is the learnable half.** Reduce-don't-loop, scan,
group, "iteration lives in the operator" — that material is well-represented, well-documented, and
apparently well-absorbed. It is also precisely the half J teaches, which is an argument for the
laboratory being *short*: one or two lessons, felt and left behind.

The half that broke is q-engine-specific — sortedness, attributes, what `aj` requires of the table
you hand it — and **J has nothing to say about any of it.** There is no fork that teaches you
`` `g# ``. That part only exists on the q side of the wall, it is where the real errors live, and
it is where the bulk of the curriculum has to be.

The laboratory earns its keep by being small.

---

## Why J, and not APL or BQN

Because it is the array language I already think in, and honesty about that is worth more than a
constructed justification.

If you are arriving with no destination in mind, [BQN](https://mlochbaum.github.io/BQN/) is
probably the better first array language — the glyphs are more regular, the documentation is
friendlier, and it was designed with hindsight about what APL got awkward. J's advantages here are
narrower and specific to this project: it is pure ASCII, so it survives any editor and any blog
renderer; it is GPLv3 and needs no license key, which makes it the one green check in this repo's
CI that does not depend on a vendor; and its fork and its rank are the two ideas I most wanted to
put in front of you.

The concepts are the same wherever you meet them. Meet them somewhere.

---

## What to carry across the wall

- **q will let you write the loop, and it will work.** That is why q cannot teach you to stop.
- **J does not forbid loops either** — it makes them feel foreign, which turns out to be the more
  useful property.
- **Iteration is a verb modifier**, and a window is a scan with a width. q gives you `sums` and
  `msum` as separate vocabulary; J shows them as one phrase with an argument.
- **Composition can be written down without mentioning data.** Feel the fork once. Then leave it —
  it does not parse in q.
- **Depth is a parameter.** After rank, q's `each` / `each-prior` / `each-left` / `each-right` stop
  being four facts and become one idea, and you stop reaching for `each` where the operator already
  vectorises.
- **The thinking transfers; the plumbing does not.** The fork fails loudly. The window convention
  fails silently. Respect the second one more.

**Next:** everything is q.

---

*Not affiliated with or endorsed by KX Systems or Jsoftware. "q", "kdb+", "KDB-X" and "J" are used
nominatively.*
