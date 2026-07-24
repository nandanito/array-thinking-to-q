# Part A — prompts that SHOULD fire the q skill

Ten prompts with explicit q / kdb+ / qSQL / aj context. The skill under test (KX's
`q-knowledge@kx-skills`) should activate on all ten. Run each in a fresh context, record
fire / no-fire, then compute the true-positive rate. After any trigger tuning of a *self-authored*
skill, re-run on FRESH prompts (SPEC.md) — do not report tuning-set numbers.

| # | Prompt | Fired? (y/n) | Notes |
|---|--------|:---:|-------|
| 1 | Write a q function to compute the moving average of a price vector. | | |
| 2 | Translate this pandas `groupby().sum()` into a kdb+ qSQL `select … by`. | | |
| 3 | Fix this q code — it uses a `do`-loop where a vector op would do. | | |
| 4 | How do I do an as-of join in kdb+ to match trades to the prevailing quote? | | |
| 5 | Write a qSQL query for total volume by symbol from a trades table. | | |
| 6 | My `aj` returns wrong quotes — what sort order and attribute do I need? | | |
| 7 | Convert this Python list comprehension into idiomatic q. | | |
| 8 | Create a keyed table in q and look up a row by its key. | | |
| 9 | Rewrite this q `while`-loop accumulator using over/scan. | | |
| 10 | What's the idiomatic q way to count occurrences of each symbol? | | |

**True positives:** __/10  (target: high recall — a skill that never fires is worth zero.)
