---
name: idiomatic-q
description: >
  Write idiomatic q (kdb+) instead of loop-transliterated imperative code. Use when writing,
  reviewing, translating, or fixing q code, qSQL queries, kdb+ tables, or as-of joins.
---

# Writing idiomatic q

STATUS: CONDITIONAL STUB. Do not build this out until the M2 eval shows a GAP that KX's official
q plugin does not already fill. KX ships first-party Claude Code plugins for q/PyKX/KDB-X/KDB.AI
(with qlint integration); a general q skill from us would be redundant. If a gap exists it is
likely LEARNER-facing (coaching out of imperative habits), not practitioner-facing. J is out of
scope for any skill — the J-asking user does not exist.

All technical claims below are FLAGGED FOR VERIFICATION against code.kx.com at M1. They are not
yet sourced; do not ship them to a public skill on model authority alone.

## Core principle

Loops are a smell. Reach for whole-array operations first. q *has* `do`/`while` — they are
unidiomatic, not absent.

## q gotchas (expand from eval failures)

- `til n` is 0..n-1. q evaluates RIGHT-TO-LEFT with no operator precedence: `2*3+1` is 8, not 7.
- Idiomatic iteration: `each`, `over` (/), `scan` (\), and vector ops.
- Tables are column dictionaries; a table is a flip of a column dict, a keyed table IS a dict.
  Prefer qSQL (`select … by … from t`) over row-wise thinking.
- **`aj` (verify all of this at M1):** join columns are the columns COMMON to both tables — not
  necessarily the leading ones; all but the last match on equality, the last matches as-of (≤),
  taking the prevailing value. Attributes: `g#` on sym is the standard IN-MEMORY prescription (time
  sorted within sym) and `p#` the on-disk one — but `p#` also works in memory and can OUTPERFORM
  `g#` where values are contiguous (code.kx.com/q/ref/set-attribute/). It is NOT useless in memory;
  an earlier draft of this line said so and was wrong. Only the attribute on the first join column
  is used.
- **THE GOTCHA THAT MATTERS MOST:** `aj` takes the last matching record in ROW ORDER. If the quote
  table is not sorted by time within sym, aj returns SILENTLY WRONG prevailing quotes — no error,
  no warning. Sort discipline is a correctness requirement, not an optimization.
- `aj0` returns the time from the quote side rather than the trade side.
- Symbols `` `x `` vs strings `"x"` are different types; qSQL column refs are symbols.

## Anti-patterns to refuse

- Transliterating Python loops into q do-loops.
- Using deprecated k-style syntax unless the user asks for k.
- Writing J-style tacit constructions in q: **q has no tacit trains**. Composition exists but is
  explicit (`'[f;g]`, projections). Related and deeper: **q has no true multidimensional arrays** —
  nested lists, not rectangular arrays with rank. This is why J's rank machinery has no q analogue.

## References (load lazily)

- ../../lessons/ — verified examples; ground truth for idiom style.
- q reference: https://code.kx.com/q/ref/
