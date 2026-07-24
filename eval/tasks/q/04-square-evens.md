# Task 04 — squares of evens

- **Type:** translate (Python → q)   **Touches:** `where` (filter), vector square

## Prompt (give verbatim to the model)

> Translate this Python list comprehension to idiomatic q — the squares of the even numbers
> in `range(10)` — and print the result.
> ```python
> [x * x for x in range(10) if x % 2 == 0]
> ```

## Reference (for scoring — do not show the model)

- Solution: `04-square-evens.ref.q` · golden: `04-square-evens.expected`
- Cited idiom (checklist item 5): `where` to filter, then vector op — https://code.kx.com/q/ref/where/
- Verify: `make verify-eval`.
