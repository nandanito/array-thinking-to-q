# Task 07 — total qty by sym

- **Type:** spec (write from English)   **Touches:** qSQL `select … by …`

## Prompt (give verbatim to the model)

> Given a trades table `t` with columns `sym` and `qty`, write a query returning the total `qty`
> per `sym`. Build a small `t` and show the result.

## Reference (for scoring — do not show the model)

- Solution: `07-total-qty-by-sym.ref.q` · golden: `07-total-qty-by-sym.expected`
- Cited idiom (checklist item 5): `select sum qty by sym from t` — https://code.kx.com/q/basics/qsql/
- Verify: `make verify-eval`.
