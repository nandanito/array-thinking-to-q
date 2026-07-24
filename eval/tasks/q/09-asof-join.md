# Task 09 — as-of join

- **Type:** spec (write from English)   **Touches:** `aj`, sort discipline

## Prompt (give verbatim to the model)

> You have a `trade` table and a `quote` table, each with `sym` and `time`. Match every trade to
> the prevailing quote — the most recent quote at or before the trade's time, for the same sym —
> using an as-of join. Build small tables and show the joined result (trade columns plus bid/ask).

## Reference (for scoring — do not show the model)

- Solution: `09-asof-join.ref.q` · golden: `09-asof-join.expected`
- Cited idiom (checklist item 5): `aj[\`sym\`time; trade; quote]` on a quote table sorted by
  time within sym — https://code.kx.com/q/ref/aj/
- Verify: `make verify-eval`.
