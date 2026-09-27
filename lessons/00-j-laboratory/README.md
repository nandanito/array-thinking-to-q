# Part I: The J laboratory

> **Read-along.** You do not need J installed to follow this lesson: every J output below is
> captured from J 9.7.1, and the q contrasts from KDB-X CE 5.0. If you want to run them anyway:
> `$HOME/j9.7/bin/jconsole < lessons/00-j-laboratory/j/laboratory.ijs` and
> `$HOME/.kx/bin/q lessons/00-j-laboratory/q/contrasts.q -q < /dev/null`
> (the binaries are not on `PATH`; see the [curriculum index](../README.md)).
> Files: [`j/laboratory.ijs`](j/laboratory.ijs), [`q/contrasts.q`](q/contrasts.q).

This curriculum ends in q, and almost all of it is written in q. So why start somewhere else?

Because q will not make you change. It has loops, and they work. You can write q for a year in the
shape of the language you came from, and nothing in q will push back. This lesson takes a short
trip to J, a language where the imperative habit is still available but visibly out of place, to
see three ideas at full strength: iteration as something you attach to a function, composition
written without data, and depth as a number you choose. Then the [transition
chapter](../00-transition/) brings them back and says plainly which ones survive the trip.

It is one lesson on purpose. J is the laboratory here, not the destination.

---

## 1. The loop that works

Here is a correct q program. It sums a list.

```q
x:1 2 3 4 5;
r:0; i:0;
do[count x; r+:x i; i+:1];
show r
```

```
15
```

It is also exactly the program this curriculum exists to talk you out of. `do[n; ...]` runs its
body `n` times, `x i` indexes, `r+:` adds and reassigns. Every piece has a direct ancestor in
Python or C, and the answer is right. The idiomatic q is `sum x`, and nothing about the loop above
tells you so. q prints no warning and raises no error, and the loop reads like any other line of q.

Keep that in mind while we look at J, because the contrast is not the one you might expect.

## 2. Enough J to read the rest

Four facts cover every J line in this lesson.

```j
2 * 3 + 4      NB. right to left: 3 + 4 first, then 2 * 7
- 5            NB. one argument (monad): negate
10 - 3         NB. two arguments (dyad): subtract
i. 5           NB. monad i.: the first five integers, like q's til
```

```
14
_5
7
0 1 2 3 4
```

J reads right to left with no operator precedence, so `2 * 3 + 4` is `2 * 7`. (q does the same,
which is one thing that does carry over.) Most J primitives have two meanings: one with a single
argument on the right (a *monad*) and one with arguments on both sides (a *dyad*), like `-` above.
J writes negative numbers with an underscore, `_5`, so that `-` is always the verb. `NB.` starts a
comment, and `=:` assigns a name.

## 3. J has loops too

It would be a neat story if J simply forbade loops. It does not:

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

`for_i.`, `while.`, `if.` and local assignment are all there. What differs is what writing the loop
costs you. You leave J's ordinary notation entirely: `3 : 0` opens an explicit definition, `=.`
replaces `=:` for local names, `y` is the argument's fixed name, and the block ends with a lone `)`.
Five lines of visibly separate machinery, in a language where the alternative is two characters:

```j
+/ 1 2 3 4 5   NB. the idiom: + inserted between the items
```

```
15
```

In q, `do[count x; r+:x i; i+:1]` sits on one line with the same texture as the q around it. In J
the loop announces that you have left the language's centre of gravity. That feeling is the whole
reason for the trip.

## 4. Iteration is a modifier

In q you learn a vocabulary of reductions: `sum`, `max`, `prd`, `avg`. Lesson 01 shows the machine
under one of them:

```q
sum til 5          / 10
(+/) til 5         / 10   — the same 10, now with the mechanism showing
```

J has no `sum` to hide behind. You write `+/` every time, and so you learn early that `/` is an
**adverb**: it takes a verb (`+`) and returns a new verb (insert `+` between the items). `\` is
another adverb. With one argument it applies its verb to every prefix of the list:

```j
+/\ 1 2 3 4 5 6
```

```
1 3 6 10 15 21
```

That is a running total: the sums of `1`, `1 2`, `1 2 3`, and so on. Give the same phrase a left
argument and `\` applies the verb to every *window* of that width instead:

```j
3 +/\ 1 2 3 4 5 6
```

```
6 9 12 15
```

A moving sum is the running-total phrase with a number in front. The notation says outright that
a window is a scan with a width. Now the same two results in q:

```q
sums 1 2 3 4 5 6      / 1 3 6 10 15 21
3 msum 1 2 3 4 5 6    / 1 3 6 9 12 15
```

Two names, and nothing in the spelling connects them. q has a whole `m` family (`mavg`, `mmax`,
`mmin`, `mcount`, `mdev`) that you learn one word at a time. The names are good; `3 mavg px` says
what it means to someone who has never heard the word adverb. But they let you use windows for a
long time without noticing that iteration is something you attach to a function. (The two moving
sums also disagree in length, four results against six. Hold that thought until the transition
chapter, where it matters.)

## 5. Composition you can write down

Here is a mean in J:

```j
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), read as one phrase
mean 0 1 2 3 4
```

```
2
```

`#` is count and `%` is divide. The definition never mentions the data. When J sees three verbs in
a row, `(f g h)`, it builds a new verb called a **fork**: apply `f` and `h` to the argument, then
combine the two results with `g`. So `mean` is "sum, divided by, count", a function assembled from
functions.

That changes what a mean *is* in your head. It stops being arithmetic on a particular list and
becomes a shape: a reduction divided by a size. Most of Part II rewards thinking in shapes like
that. The fork itself does not come with you, though: the [transition chapter](../00-transition/)
shows what happens when you type it into q.

## 6. Depth is a parameter

This is the idea q hides most completely. J's `"` (a *conjunction*, which takes a verb and a
number) sets the **rank** a verb works at: the size of the sub-arrays it is handed. Start with a
2×3 matrix (`$` reshapes a list into the shape on its left):

```j
m =: 2 3 $ 1 2 3 4 5 6
+/ m        NB. + inserted between the ITEMS — and a matrix's items are its ROWS
+/"1 m      NB. rank 1: apply to each row instead
```

```
5 7 9
6 15
```

Plain `+/` inserts `+` between the items of its argument, and the items of a matrix are its rows,
so it adds `1 2 3` to `4 5 6`. `+/"1` hands the verb one rank-1 cell (one row) at a time, so each
row is summed on its own. Boxing (`<`) makes the cells visible without arithmetic in the way:

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

Same verb, same matrix. The number chose the depth: `"0` boxes every atom, `"1` every row.

q reaches both sums:

```q
sum (1 2 3; 4 5 6)        / 5 7 9
sum each (1 2 3; 4 5 6)   / 6 15
```

but by a different route. `each` is one fixed move, "one level down", and there is no `each 2`.
Where J turns a dial, q has a word that only ever means one.

Do not push the analogy further than that. q's other iterators are not rank in disguise:

```q
(-':) 1 3 6 10 15   / 1 2 3 4 5     each-prior
```

`each-prior` (`':`) applies `-` to each item and the one before it. That is about neighbours, not
depth, and no rank number expresses it. J files the same job under the infix adverb from §4, with
a window of two (`~` swaps a verb's arguments, so each pair is taken as later minus earlier):

```j
2 -~/\ 1 3 6 10 15
```

```
2 3 4 5
```

Four differences from J where q gave five. J's infix takes complete pairs only; q's each-prior
supplies a starting prior for the first item (here `0`, so the first result is `1-0`). That is
the same four-against-six split as the moving sums in §4, turning up in a second family.

What rank buys you in q is narrower than "it explains the iterators", and still real. Lesson 01
says you never write `each` for the atomic operators (`+`, `*`, `>`) because they already reach the
atoms. After rank, that stops being a rule to memorise and becomes a consequence: `*` already works
at rank 0, so `each` would ask for something it already has.

---

## What to carry forward

- **q lets you write the loop, and it works.** That is why q alone does not teach you to stop.
- **J allows loops too**, but makes them feel foreign, which turns out to be the more useful
  property for a learner.
- **Iteration is a verb modifier.** `+/\` is a running total; `3 +/\` is a moving sum. q spells the
  same pair `sums` and `msum`.
- **A function can be written without its data.** `+/ % #` is a mean as a shape. Feel it here; q
  will not parse it.
- **Depth is a parameter in J.** q's `each` is that idea fixed at one level, and each-prior is a
  different idea (neighbours) that happens to share the word.

**Next:** [the transition chapter](../00-transition/): what crosses into q, what does not, and the
one difference that fails without telling you.

---

### References

- J's vocabulary (every primitive used here): [NuVoc](https://code.jsoftware.com/wiki/NuVoc)
- The fork: [J primer, Forks](https://www.jsoftware.com/help/primer/fork.htm)
- Rank: [NuVoc, `"` (Rank)](https://code.jsoftware.com/wiki/Vocabulary/quote)
- Prefix and infix: [NuVoc, `\`](https://code.jsoftware.com/wiki/Vocabulary/bslash)
- q's iterators, including each-prior: [code.kx.com: Iterators](https://code.kx.com/q/ref/iterators/)
- q's moving windows: [code.kx.com: msum](https://code.kx.com/q/ref/sum/#msum)
