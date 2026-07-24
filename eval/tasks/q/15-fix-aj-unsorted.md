# Task 15 — fix a silently-wrong as-of join

- **Type:** fix (unidiomatic → idiomatic)   **Touches:** `aj`, sort discipline, `g#`

## Prompt (give verbatim to the model)

> The following as-of join returns silently wrong prevailing quotes because the quote table is
> not sorted by time within sym. Fix it so `aj` is correct, and set the appropriate in-memory
> attribute.
> ```q
> quote:([] sym:`AAPL`AAPL`MSFT; time:09:30:05 09:30:00 09:30:00;
>           bid:99.4 99.0 200.0; ask:99.6 99.2 200.2);
> trade:([] sym:`AAPL`MSFT; time:09:30:03 09:30:02; price:99.1 200.1; size:100 50);
> aj[`sym`time; trade; quote]
> ```

## Reference (for scoring — do not show the model)

- Solution: `15-fix-aj-unsorted.ref.q` · golden: `15-fix-aj-unsorted.expected`
- Cited idiom (checklist item 5): `\`sym\`time xasc quote` then `@[\`quote;\`sym;\`g#]` before
  `aj` — https://code.kx.com/q/ref/aj/ , https://code.kx.com/q/ref/set-attribute/
- Verify: `make verify-eval`. (Missing the sort => wrong result with no error.)
