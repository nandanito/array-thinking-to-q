# Task 05 — moving average

- **Type:** translate (Python → q)   **Touches:** `mavg`

## Prompt (give verbatim to the model)

> Translate to idiomatic q: the 3-period moving average of `[1, 2, 3, 4, 5, 6]`. Windows shorter
> than 3 at the start average the values available so far. Print the result.

## Reference (for scoring — do not show the model)

- Solution: `05-moving-average.ref.q` · golden: `05-moving-average.expected`
- Cited idiom (checklist item 5): `n mavg x` (moving average) — https://code.kx.com/q/ref/avg/
- Verify: `make verify-eval`.
