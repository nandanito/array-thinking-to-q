# Task 10 — count by (sym, side)

- **Type:** spec (write from English)   **Touches:** qSQL `select count i by …`

## Prompt (give verbatim to the model)

> Given a trades table `t` with columns `sym` and `side`, count the number of trades for each
> `(sym, side)` pair. Build a small `t` and show the result.

## Reference (for scoring — do not show the model)

- Solution: `10-count-by-sym-side.ref.q` · golden: `10-count-by-sym-side.expected`
- Cited idiom (checklist item 5): `select n:count i by sym,side from t` — https://code.kx.com/q/basics/qsql/
- Verify: `make verify-eval`.
