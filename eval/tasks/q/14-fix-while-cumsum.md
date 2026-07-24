# Task 14 — fix a while-loop cumulative sum

- **Type:** fix (unidiomatic → idiomatic)   **Touches:** scan, `sums`

## Prompt (give verbatim to the model)

> The following q builds cumulative sums with a while loop. Rewrite it idiomatically.
> ```q
> x:5 3 8 1;
> out:(); run:0; i:0;
> while[i<count x; run+:x i; out,:run; i+:1];
> out
> ```

## Reference (for scoring — do not show the model)

- Solution: `14-fix-while-cumsum.ref.q` · golden: `14-fix-while-cumsum.expected`
- Cited idiom (checklist item 5): `sums x` (a scan) instead of `while[]` — https://code.kx.com/q/ref/sum/
- Verify: `make verify-eval`.
