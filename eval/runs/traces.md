# Raw session traces — M2 eval

**Derived from the committed logs in [`logs/`](logs/)** by `eval/harness/mktraces.py`, and re-checked by `make verify-eval-run` — so the
activation and token numbers in `../verdict.md` can be audited without trusting this
table. "Fired" means the session actually emitted a `Skill` tool call naming a
`q-knowledge` skill, not that the answer *looked* q-flavoured. Condition A has no such
skill to call; its logs record `"plugins": []`.

## Part A — 20 trigger sessions (condition B only)

Prompt text is the exact bytes fed to `claude -p`, from [`prompts/`](prompts/).

| session | prompt | tool calls in order | fired |
|---|---|---|:---:|
| nf01 | Vectorize this NumPy loop for speed. | Glob | **n** |
| nf02 | Write a SQL query for total sales by region. | Glob | **n** |
| nf03 | Explain fork and hook trains in BQN. | _(none)_ | **n** |
| nf04 | Make this Python function faster. | Glob → Glob | **n** |
| nf05 | Write a query to fetch users by email. | Glob → Skill | **y** |
| nf06 | How do APL trains work? | Glob | **n** |
| nf07 | Translate this Python loop to idiomatic Rust. | Glob | **n** |
| nf08 | Optimize this pandas `merge_asof` call. | Glob | **n** |
| nf09 | Group a JavaScript array by a key. | _(none)_ | **n** |
| nf10 | Explain how J's rank operator works. | _(none)_ | **n** |
| sf01 | Write a q function to compute the moving average of a price vector. | Skill | **y** |
| sf02 | Translate this pandas `groupby().sum()` into a kdb+ qSQL `select … by`. | Glob → Skill → Read → Skill | **y** |
| sf03 | Fix this q code — it uses a `do`-loop where a vector op would do. | Glob → Glob | **n** |
| sf04 | How do I do an as-of join in kdb+ to match trades to the prevailing quote? | Skill | **y** |
| sf05 | Write a qSQL query for total volume by symbol from a trades table. | Skill → Skill | **y** |
| sf06 | My `aj` returns wrong quotes — what sort order and attribute do I need? | Skill → Glob → Glob → Glob | **y** |
| sf07 | Convert this Python list comprehension into idiomatic q. | Glob | **n** |
| sf08 | Create a keyed table in q and look up a row by its key. | Skill | **y** |
| sf09 | Rewrite this q `while`-loop accumulator using over/scan. | Glob → Glob → Skill | **y** |
| sf10 | What's the idiomatic q way to count occurrences of each symbol? | Skill | **y** |

## Part B — 30 generation sessions

| task | cond | tool calls in order | q skill fired | output tokens |
|---|:---:|---|:---:|---:|
| 01-sum-squares | A | _(none)_ | **n** | 123 |
| 01-sum-squares | B | Skill | **y** | 548 |
| 02-running-total | A | _(none)_ | **n** | 47 |
| 02-running-total | B | Skill | **y** | 315 |
| 03-word-frequency | A | _(none)_ | **n** | 529 |
| 03-word-frequency | B | Skill → Read → Skill | **y** | 702 |
| 04-square-evens | A | _(none)_ | **n** | 317 |
| 04-square-evens | B | Skill → Skill | **y** | 693 |
| 05-moving-average | A | _(none)_ | **n** | 164 |
| 05-moving-average | B | Skill | **y** | 323 |
| 06-mean-no-avg | A | _(none)_ | **n** | 303 |
| 06-mean-no-avg | B | Skill | **y** | 320 |
| 07-total-qty-by-sym | A | _(none)_ | **n** | 153 |
| 07-total-qty-by-sym | B | Skill | **y** | 619 |
| 08-add-notional | A | _(none)_ | **n** | 111 |
| 08-add-notional | B | Skill | **y** | 436 |
| 09-asof-join | A | _(none)_ | **n** | 610 |
| 09-asof-join | B | Skill | **y** | 615 |
| 10-count-by-sym-side | A | _(none)_ | **n** | 178 |
| 10-count-by-sym-side | B | Skill → Skill | **y** | 679 |
| 11-distinct-syms | A | _(none)_ | **n** | 69 |
| 11-distinct-syms | B | Skill | **y** | 279 |
| 12-fix-doloop-sum | A | _(none)_ | **n** | 20 |
| 12-fix-doloop-sum | B | _(none)_ | **n** | 225 |
| 13-fix-rowwise-notional | A | _(none)_ | **n** | 46 |
| 13-fix-rowwise-notional | B | Skill → Skill | **y** | 328 |
| 14-fix-while-cumsum | A | _(none)_ | **n** | 23 |
| 14-fix-while-cumsum | B | Skill | **y** | 407 |
| 15-fix-aj-unsorted | A | _(none)_ | **n** | 978 |
| 15-fix-aj-unsorted | B | Skill → Glob → Glob → Read | **y** | 3848 |
