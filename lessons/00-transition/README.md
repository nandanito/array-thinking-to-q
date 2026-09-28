# Transition: everything after this point is q

> **Run it:** `$HOME/.kx/bin/q lessons/00-transition/q/transition.q -q < /dev/null`
> and `$HOME/j9.7/bin/jconsole < lessons/00-transition/j/windows.ijs`
> (the binaries are not on `PATH`; see the [curriculum index](../README.md)).
> Every output below is captured from KDB-X CE 5.0 and J 9.7.1.
> Files: [`q/transition.q`](q/transition.q), [`j/windows.ijs`](j/windows.ijs).

The [J laboratory](../00-j-laboratory/) showed three ideas at full strength: iteration as a
modifier, composition without data, and depth as a parameter. This chapter is the customs desk.
The thinking crosses into q intact. Much of the notation does not, and one piece of it will
cross, look fine, and hand you a wrong answer.

## What carries over

- **No loop in sight.** A reduction is a function folded across a list; a running total is the same
  fold with every step kept. q spells these `/` (over) and `\` (scan), exactly like J, and names
  the common ones: `sum`, `sums`, `max`, `avg`.
- **Right to left.** q evaluates right to left with no operator precedence, as J does.
- **Shapes over steps.** "A mean is a reduction divided by a size" is as true in q as in J. You
  will say it differently, but thinking in shapes is what Part II keeps rewarding, all the way to
  the as-of join.
- **Depth awareness.** Knowing what level a function works at is why you never write `each` for
  `+` or `*`, and why you do write `count each`.

## What does not

### The fork does not parse

Type `+/ % #` into q and you get no answer at all. Lesson 01 quotes [the real REPL
transcript](../01-atoms-and-lists/#5-the-wall-what-j-shows-and-q-refuses): a blank error message
and a caret in the middle of the fork. That failure happens while q is *parsing* the line, before
anything runs, and the distinction matters more than it looks.

A runtime error can be caught. The usual reflex is to wrap the risky expression in protected
evaluation (q's `.[f; args; handler]`) and handle the failure. That cannot work here, because the
guard is part of the same line, and the line never parses. You can check this directly by handing
the text to q's parser as a string, which turns the parse failure into a value:

```q
parses:{@[{parse x; 1b}; x; 0b]}
parses "(+/ % #) til 5"                        / 0b
parses ".[{(+/ % #) til 5};();{(`caught;x)}]"  / 0b
parses "{(sum x) % count x} til 5"             / 1b
```

`parses` calls `parse` under protected evaluation (`@[f; x; handler]`, the one-argument form) and
returns `0b` if the parser rejects the text. The fork is rejected. So is the fork wrapped in a
guard, because the guard's own text contains it. The same composition written as a lambda parses
fine.

Notice why `parses` itself works: the text arrives as a string at runtime, so the parse happens
*inside* a protected call. That is the only way to trap this error, and it means building the code
as a string on purpose, which is not a mistake anyone makes by accident. In ordinary source, the
fork cannot be defended against. It can only be not written.

**q has no tacit forks or trains.** A parenthesised run of functions is not a new function in q.
What q wants is the composition said out loud, as a built-in or a lambda:

```q
avg til 5                    / 2f
{(sum x) % count x} til 5    / 2f   — the explicit lambda q DOES accept
```

This failure is the kind one. It is loud, and you cannot ship it.

### Rank has no q spelling

There is no `"` in q, and no way to say "apply at rank 2". q's `each` is the one-level move
(`sum each` in the laboratory's §6), and you stack it when you need to go deeper. Beyond that, q
gives you named iterators for specific patterns: each-prior (`':`) for neighbours, each-left
(`\:`) and each-right (`/:`) for pairing one argument against every item of the other. You will
also meet far less nesting than J code has. Part II's data lives in tables, which are
[lists of columns](../02-dict-to-table/), and qSQL works on whole columns at a time. Most of what
rank does in J, a `select ... by` does in q.

### The windows have a different shape, and nothing complains

This one ships.

Here is J's 3-wide moving average of six numbers:

```j
3 (+/ % #)\ 1 2 3 4 5 6
```

```
2 3 4 5
```

Four results. J's infix `\` gives complete windows only, and there is no complete 3-wide window
ending at the first or second item.

The same request in q:

```q
3 mavg 1 2 3 4 5 6f    / 1 1.5 2 3 4 5
```

Six results. q's `m` family ramps up through partial windows: the first output averages one item,
the second averages two, and only from the third is the window full. Six inputs, six outputs,
always.

Neither convention is wrong, and neither announces itself. "The 3-period moving average" describes
both. Carry the J habit into q and anything you line up against that column is off by two rows
(width minus one, in general), with no error and a plausible-looking answer. [Lesson
03](../03-qsql/#6-windows-mavg-and-the-by-that-makes-it-correct) puts `mavg` inside an `update`,
and there the q convention is the useful one: a new column needs one value per row, and `n`
inputs always give `n` outputs.

## The rule

**The thinking transfers. The plumbing does not.** The fork fails loudly and the window convention
fails silently, so trust the silent one less. When a J habit comes up in q, check what q's own
version returns before building on it.

| J laboratory | In q |
|---|---|
| `+/` over, `+/\` scan | `/` and `\` too, usually through a name: `sum`, `sums` |
| `3 +/\` infix window | `3 msum`: a separate name, and partial windows at the start |
| fork `+/ % #` | does not parse; write `avg`, or a lambda |
| rank `"1` | no equivalent; `each` for one level, qSQL for whole columns |
| `2 -~/\` pairs | each-prior `-':`, which also gives a result for the first item |

Everything after this point is q.

**Next:** [Lesson 01: atoms, lists, and the death of the loop](../01-atoms-and-lists/).

---

### References

- `parse` and protected evaluation: [code.kx.com: parse](https://code.kx.com/q/ref/parse/),
  [code.kx.com: Apply, Trap](https://code.kx.com/q/ref/apply/#trap)
- q's iterators: [code.kx.com: Iterators](https://code.kx.com/q/ref/iterators/)
- `mavg`: [code.kx.com: mavg](https://code.kx.com/q/ref/avg/#mavg)
- J's infix: [NuVoc, `\`](https://code.jsoftware.com/wiki/Vocabulary/bslash)
