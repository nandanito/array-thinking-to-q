# Task 07 — total qty by sym

- **Type:** spec (write from English)   **Touches:** qSQL `select … by …`

## Prompt (give verbatim to the model)

> Given this trades table, write a query returning the total `qty` per `sym`, and show the result:
>
> ```q
> t:([] sym:`AAPL`MSFT`AAPL`MSFT`AAPL; qty:100 200 150 50 300)
> ```

## Reference (for scoring — do not show the model)

- Solution: `07-total-qty-by-sym.ref.q` · golden: `07-total-qty-by-sym.expected`
- Cited idiom (checklist item 5): `select sum qty by sym from t` — https://code.kx.com/q/basics/qsql/
- Verify: `make verify-eval`.
