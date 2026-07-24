# Task 08 — add a computed column

- **Type:** spec (write from English)   **Touches:** qSQL `update`

## Prompt (give verbatim to the model)

> Given a trades table `t` with columns `sym`, `price`, `qty`, add a column `notional` equal to
> `price * qty`. Build a small `t` and show the result.

## Reference (for scoring — do not show the model)

- Solution: `08-add-notional.ref.q` · golden: `08-add-notional.expected`
- Cited idiom (checklist item 5): `update notional:price*qty from t` — https://code.kx.com/q/ref/update/
- Verify: `make verify-eval`.
