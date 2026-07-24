# Task 09 — as-of join

- **Type:** spec (write from English)   **Touches:** `aj`, sort discipline

## Prompt (give verbatim to the model)

> Using these tables (the quote table is already sorted by time within sym), match every trade to
> the prevailing quote — the most recent quote at or before the trade's time, for the same sym —
> with an as-of join, and show the joined result (trade columns plus bid/ask):
>
> ```q
> quote:([] sym:`AAPL`AAPL`MSFT`MSFT; time:09:30:00 09:30:04 09:30:01 09:30:05;
>           bid:99.0 99.2 200.0 200.3; ask:99.2 99.4 200.2 200.5);
> trade:([] sym:`AAPL`MSFT`AAPL; time:09:30:02 09:30:03 09:30:06;
>           price:99.1 200.1 99.3; size:100 50 150)
> ```

## Reference (for scoring — do not show the model)

- Solution: `09-asof-join.ref.q` · golden: `09-asof-join.expected`
- Cited idiom (checklist item 5): `aj[\`sym\`time; trade; quote]` on a quote table sorted by
  time within sym — https://code.kx.com/q/ref/aj/
- Verify: `make verify-eval`.
