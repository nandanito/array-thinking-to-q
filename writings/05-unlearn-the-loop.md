# Unlearn the loop: what J shows that q hides

*Article 5 of 6 — draft. Gated on M4 (the J laboratory).*

> **Publication gate — NOT publishable yet.** Every snippet below was executed against J 9.7.1 and
> KDB-X CE 5.0 and every output is captured, not typed. But RELEASE-CHECKLIST.md requires each
> snippet to come from a **running lesson file**, and by that test the provenance here is mixed:
>
> - **From verified lesson files:** the `sum`/`(+/)` pair, the `mean =: +/ % #` fork and its q
>   parse failure (lesson 01), and the `3 mavg` window convention (lesson 03). The
>   protected-evaluation transcript is stated in lesson 01's prose but not shown there as a block —
>   CLAUDE.md caps verify-exempt blocks at two, and it was not worth spending the third on.
> - **From the eval task set, not a lesson:** the opening `do[]` loop (`eval/tasks/q/12-fix-doloop-sum.md`).
> - **From a scratch directory — no home in the repo yet:** every J rank example, the J explicit
>   loop, the infix/prefix scan pair, and q's `each-prior` / `each-left` / `each-right`.
>
> All three groups have to land in lesson files that `make verify` runs before this publishes.
> Drafted ahead of its milestone deliberately: this is the article the spec flagged as at-risk, and
> banking it early is the mitigation it never got.

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

In q you learn a vocabulary: `sum`, `sums`, `max`, `prd`, `mavg`. Good names, well chosen, and you
can use them for a year without noticing that several of them are the *same construction* wearing
different labels.

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

— but by a different route, and the route is the point. **`each` is not a depth parameter you can
dial.** It is one fixed move — "one level down" — and there is no `each 2`. Where J turns a knob, q
gives you a word that only ever means 1.

Be careful how far you push that, though, because q's other iterators are *not* rank in disguise:

```q
(-':) 1 3 6 10 15   / 1 2 3 4 5     each-prior
```

`each-prior` walks adjacent pairs. That is not a statement about depth at all, and no rank number
expresses it — J puts adjacent pairs in a different family entirely, the **infix** one from §1:

```j
2 -~/\ 1 3 6 10 15
```

```
2 3 4 5
```

Four results where q's `-':` gave five — because J's infix takes complete pairs only, while q's
each-prior supplies a starting prior (here `0`, so the first output is `1-0`). That is the *same*
complete-versus-partial split as the moving-window case, surfacing again in a second family. Worth
noticing now; it is about to cost us.

The practical payoff of rank is narrower than "it explains q's iterators", and real. Lesson 01
makes the point that `each` is about **depth, not looping**, and that the atomic operators (`+`,
`*`, `>`) already reach the atoms by themselves so you never write `each` for those. That is a rule
you can memorise. After rank it stops being a rule and becomes a consequence: `*` already applies
at rank 0, so asking for `each` is asking for something you have.

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
lands in the middle of the fork.

That is a parse-time rejection, not a runtime error, and the distinction has teeth: you cannot
defend against it. Wrapping the fork in protected evaluation does not help, because the wrapper has
to parse too —

```q
q).[{(+/ % #) til 5};();{(`caught;x)}]
'
  [0]  .[{(+/ % #) til 5};();{(`caught;x)}]
             ^        / caret inside the lambda — the guard never got to run
```

(Pedantically: hand that *same text* to `value` as a runtime **string** and it becomes trappable,
because then the parsing happens inside the protected call. That is a different program, and not
one you would write by accident.)

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

What *did* separate both conditions from my reference answer was the one task about attributes and
sort discipline: both applied `` `p# `` where the task sheet called for `` `g# ``. (I originally
wrote that up as both of them getting the attribute *wrong*. They didn't — the
[set-attribute page](https://code.kx.com/q/ref/set-attribute/) says parted "effects better speedups
than grouped, both on disk and in memory" when the data is sorted so it can be set, and both had
sorted first. The narrow instrument was mine.)

I want to be careful about how much weight that split can carry, because my own verdict on that
eval says it was **underpowered** — the fifteen tasks turned out to be easy enough that the
baseline was already at the ceiling, so the study could not have detected a small effect at all.
Three solved loop-fix tasks are three data points from a task set I built badly. They are not
"models have absorbed array thinking".

What they do support is narrower and still worth something. **On the loop-transliteration exercises
I could think of, the failure mode this curriculum exists to prevent did not show up.** And the one
task where the answers diverged from my reference at all was not about loops or reductions or any
other array idea — it was about sortedness, attributes, and what `aj` requires of the table you hand
it. It was even a case where I, not the models, had the documentation wrong.

**J has nothing to say about any of that.** There is no fork that teaches you `` `g# ``, and no
rank that tells you when `` `p# `` is the better call.

That is consistent with a short laboratory, which is what this curriculum already commits to — J
was cut from co-star to one or two illustrative lessons on a reviewer's advice, and I went along
with it at the time without evidence either way. I still do not have strong evidence. I have one
underpowered study pointing the same direction as the architectural argument, which is worth
exactly as much as that sounds.

The errors that will actually cost you live on the q side of the wall. That is where the bulk of
the curriculum has to be, and it is the better reason for keeping the laboratory small.

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
- **Depth is a parameter** — in J. q's `each` is that idea frozen at one level, and q's other
  iterators are *not* rank in disguise: `each-prior` walks adjacent pairs, which is the infix
  family, not a depth. What rank buys you is knowing why you never write `each` for `*`.
- **The thinking transfers; the plumbing does not.** The fork fails loudly. The window convention
  fails silently. Respect the second one more.

**Next:** everything is q.

---

*Not affiliated with or endorsed by KX Systems or Jsoftware. "q", "kdb+", "KDB-X" and "J" are used
nominatively.*
