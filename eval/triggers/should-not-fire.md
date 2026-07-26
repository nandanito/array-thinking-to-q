# Part A — adjacent traps that should NOT fire the q skill

Ten prompts that are *adjacent* — array-programming, "query", "group", "asof", or J — but carry
no q/kdb+ context. The skill under test should stay silent on all ten. Each false positive is a
precision failure; a skill that fires on everything is as useless as one that never fires.

**Run 2026-07-26/27**, condition B only, one fresh headless session per prompt, neutral cwd.
"Fired" is decided mechanically from the session's tool calls; traces in
[`../runs/traces.md`](../runs/traces.md).

| # | Prompt | Fired? (y/n) | Why it's a trap |
|---|--------|:---:|-----------------|
| 1 | Vectorize this NumPy loop for speed. | n | array-adjacent, but NumPy not q |
| 2 | Write a SQL query for total sales by region. | n | plain SQL, no q |
| 3 | Explain fork and hook trains in BQN. | n | array-family, but BQN not q |
| 4 | Make this Python function faster. | n | generic perf, no q |
| 5 | Write a query to fetch users by email. | **y** | generic "query", no q context — **false positive** |
| 6 | How do APL trains work? | n | APL not q |
| 7 | Translate this Python loop to idiomatic Rust. | n | different target language |
| 8 | Optimize this pandas `merge_asof` call. | n | as-of keyword trap, pandas not kdb+ |
| 9 | Group a JavaScript array by a key. | n | "group" keyword trap, JS not q |
| 10 | Explain how J's rank operator works. | n | J is cut from skill scope (obj. 3) |

**True negatives:** **9/10.**

The one false positive is #5. Given a bare "write a query to fetch users by email" in an empty
directory, the session loaded `q-knowledge:q` and answered entirely in q — schema, `select from
users where email = `$"…"`, a case-insensitive variant. The answer was *good q*; it was also an
answer to a question nobody asked in q.

Two honest caveats on that single data point, both of which belong in the writeup:

- The harness deliberately strips ambient context (`--setting-sources ""`, empty neutral cwd), so
  `q-knowledge` was the only domain skill in the session. In a real repository the surrounding
  code would supply the missing signal, and this false positive is the kind that would likely not
  survive it. The trap is therefore harder than practice — which is what a trap is for, but it
  caps how much weight one mis-fire can carry.
- The strongest traps were the ones designed to bait a keyword match — `merge_asof` (#8), "group"
  (#9), J's rank (#10) — and the plugin held on every one of them. The mis-fire came from the
  *least* q-flavoured prompt in the set, which reads more like the model reaching for the only
  tool on the bench than like the skill's description over-matching.
