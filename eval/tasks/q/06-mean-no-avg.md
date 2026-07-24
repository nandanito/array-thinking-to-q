# Task 06 — mean without avg

- **Type:** spec (write from English)   **Touches:** `sum`, `count`, no tacit fork in q

## Prompt (give verbatim to the model)

> Write a q function `mean` that returns the arithmetic mean of a numeric list. Do NOT use the
> built-in `avg`. Demonstrate it on `1 2 3 4 5`.

## Reference (for scoring — do not show the model)

- Solution: `06-mean-no-avg.ref.q` · golden: `06-mean-no-avg.expected`
- Cited idiom (checklist item 5): `{(sum x) % count x}` — q has NO tacit fork, so the J-style
  `(+/ % #)` train is wrong here — https://code.kx.com/q/ref/sum/ , https://code.kx.com/q/ref/count/
- Verify: `make verify-eval`. (A loop or a J-style train fails checklist item 1/5.)
