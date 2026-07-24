# Task 12 — fix a do-loop sum

- **Type:** fix (unidiomatic → idiomatic)   **Touches:** `sum` / over

## Prompt (give verbatim to the model)

> The following q sums a vector but was transliterated from an imperative loop. Rewrite it
> idiomatically.
> ```q
> x:1 2 3 4 5;
> r:0; i:0;
> do[count x; r+:x i; i+:1];
> r
> ```

## Reference (for scoring — do not show the model)

- Solution: `12-fix-doloop-sum.ref.q` · golden: `12-fix-doloop-sum.expected`
- Cited idiom (checklist item 5): `sum x` (i.e. `+/`) instead of `do[]` — https://code.kx.com/q/ref/sum/
- Verify: `make verify-eval`. (Any surviving `do[]` fails checklist item 1.)
