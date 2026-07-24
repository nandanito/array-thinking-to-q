# Task 08 — add a computed column

- **Type:** spec (write from English)   **Touches:** qSQL `update`

## Prompt (give verbatim to the model)

> Given this trades table, add a column `notional` equal to `price * qty`, and show the result:
>
> ```q
> t:([] sym:`AAPL`MSFT`AAPL; price:190.0 410.0 191.0; qty:100 50 200)
> ```

## Reference (for scoring — do not show the model)

- Solution: `08-add-notional.ref.q` · golden: `08-add-notional.expected`
- Cited idiom (checklist item 5): `update notional:price*qty from t` — https://code.kx.com/q/ref/update/
- Verify: `make verify-eval`.
