# Task 02 — running total

- **Type:** translate (Python → q)   **Touches:** scan, `sums`

## Prompt (give verbatim to the model)

> Translate this Python to idiomatic q: given `[1, 2, 3, 4, 5]`, produce the running
> (cumulative) totals, then print them.
> ```python
> out, run = [], 0
> for x in [1, 2, 3, 4, 5]:
>     run += x
>     out.append(run)
> ```

## Reference (for scoring — do not show the model)

- Solution: `02-running-total.ref.q` · golden: `02-running-total.expected`
- Cited idiom (checklist item 5): `sums` (running sum, a scan) — https://code.kx.com/q/ref/sum/
- Verify: `make verify-eval`.
