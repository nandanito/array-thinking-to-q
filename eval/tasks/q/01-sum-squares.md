# Task 01 — sum of squares

- **Type:** translate (Python → q)   **Touches:** vector arithmetic, `sum`

## Prompt (give verbatim to the model)

> Translate this Python to idiomatic q. Given `n = 10`, compute the sum of the squares of
> `0, 1, …, n-1`, then print the result.
> ```python
> total = 0
> for i in range(n):
>     total += i * i
> ```

## Reference (for scoring — do not show the model)

- Solution: `01-sum-squares.ref.q` · golden: `01-sum-squares.expected`
- Cited idiom (checklist item 5): whole-vector multiply + `sum` — https://code.kx.com/q/ref/sum/
- Verify: `make verify-eval` (or score a candidate per `../../README.md`).
