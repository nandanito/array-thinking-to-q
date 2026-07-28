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

## Instrument note — this task is TOO NARROW (added 2026-07-28, deliberately not applied)

The cited idiom names `` `g# `` as though it were the only correct attribute. It is not:
<https://code.kx.com/q/ref/set-attribute/> says parted *"effects better speedups than grouped, both
on disk and in memory"* when the data can be sorted so `p` can be set — which `` `sym`time xasc ``
does. In the M2 run **both** conditions chose `` `p# `` and were marked down for it; that markdown
was later retracted as an instrument defect, not a model error (eval/verdict.md, eval/runs/notes.md).

**The Prompt and cited idiom above are intentionally left UNCHANGED.** `results.csv` was scored
against this exact text, and editing it now would leave the published scores unexplainable by the
committed instrument. Reproducibility beats tidiness.

**Before this task is reused in any future run**, widen item 5 to accept either attribute on a
sorted table — or state why `` `g# `` alone should count — and re-score from scratch. Do not mix
results across the two versions.
