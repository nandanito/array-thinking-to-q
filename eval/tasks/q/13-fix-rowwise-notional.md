# Task 13 — fix row-wise table iteration

- **Type:** fix (unidiomatic → idiomatic)   **Touches:** qSQL `update`

## Prompt (give verbatim to the model)

> The following q computes per-row notional by iterating row indices. Rewrite it idiomatically
> using qSQL.
> ```q
> t:([] price:190.0 410.0 191.0; qty:100 50 200);
> n:count t;
> res:();
> i:0; do[n; res,:t[i;`price]*t[i;`qty]; i+:1];
> update notional:res from t
> ```

## Reference (for scoring — do not show the model)

- Solution: `13-fix-rowwise-notional.ref.q` · golden: `13-fix-rowwise-notional.expected`
- Cited idiom (checklist item 5): `update notional:price*qty from t` — https://code.kx.com/q/ref/update/
- Verify: `make verify-eval`. (Row-index iteration fails checklist items 1–2.)
