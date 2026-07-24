# Task 03 — word frequency

- **Type:** translate (Python → q)   **Touches:** `group`, `count each`

## Prompt (give verbatim to the model)

> Translate this Python to idiomatic q: count how many times each word appears in the list
> `the cat sat on the mat the`, then print the per-word counts.
> ```python
> from collections import Counter
> Counter(words)
> ```

## Reference (for scoring — do not show the model)

- Solution: `03-word-frequency.ref.q` · golden: `03-word-frequency.expected`
- Cited idiom (checklist item 5): `count each group x` — https://code.kx.com/q/ref/group/
- Verify: `make verify-eval`.
