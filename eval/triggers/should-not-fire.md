# Part A — adjacent traps that should NOT fire the q skill

Ten prompts that are *adjacent* — array-programming, "query", "group", "asof", or J — but carry
no q/kdb+ context. The skill under test should stay silent on all ten. Each false positive is a
precision failure; a skill that fires on everything is as useless as one that never fires.

| # | Prompt | Fired? (y/n) | Why it's a trap |
|---|--------|:---:|-----------------|
| 1 | Vectorize this NumPy loop for speed. | | array-adjacent, but NumPy not q |
| 2 | Write a SQL query for total sales by region. | | plain SQL, no q |
| 3 | Explain fork and hook trains in BQN. | | array-family, but BQN not q |
| 4 | Make this Python function faster. | | generic perf, no q |
| 5 | Write a query to fetch users by email. | | generic "query", no q context |
| 6 | How do APL trains work? | | APL not q |
| 7 | Translate this Python loop to idiomatic Rust. | | different target language |
| 8 | Optimize this pandas `merge_asof` call. | | as-of keyword trap, pandas not kdb+ |
| 9 | Group a JavaScript array by a key. | | "group" keyword trap, JS not q |
| 10 | Explain how J's rank operator works. | | J is cut from skill scope (obj. 3) |

**True negatives:** __/10  (target: high precision — no firing on adjacent-but-not-q prompts.)
