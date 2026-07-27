# Part B — per-run notes and scoring rationale

Raw answers: `NN-name.A.q` (baseline) and `NN-name.B.q` (KX `q-knowledge` plugin). Every one of
the 30 answers obeyed the output contract exactly — one fenced q block, zero prose — so the `.q`
files are the model's replies **verbatim**, minus the fences. Tool traces and token counts:
[`traces.md`](traces.md). Scores: [`../results.csv`](../results.csv).

## Two scoring rules fixed before the pass, applied mechanically

**`idiom_no_temps` (item 4) is scored against the task's own reference solution.** A candidate
fails only if it introduces a binding the verified `NN-name.ref.q` does not need. Naming input
data the prompt supplies (`t:([]…)`, `x:1 2 3 4 5`, `n:10`) never counts — the item exists to catch
loop-transliteration scratch state (`r:0; i:0; res:()`), not to tax readable code. Without this
anchor the item is the author's taste, which is precisely what PROTOCOL.md's binary checklist is
there to prevent.

**`idiom_cited` (item 5) is scored against the cited idiom in that task's own sheet**, not against
q idiom in general. A candidate that goes beyond the cited idiom in ways the task did not ask about
is not penalised under item 5 (see task 09).

## Per task

| # | task | A | B | note |
|---|---|:---:|:---:|---|
| 01 | sum-squares | 6 | 6 | Both vectorise. A inlines the assignment (`sum x*x:til n`), B names it (`i:til n; sum i*i`) — same binding count as the reference either way. Tie. |
| 02 | running-total | 6 | 6 | Byte-identical: `show sums 1 2 3 4 5`. |
| 03 | word-frequency | 6 | 6 | Both `count each group`. A derived the word list by splitting a string (`` `$(" " vs "…") ``), B typed the symbol vector. Both are one binding, same as the reference. Tie. |
| 04 | square-evens | 6 | 6 | Both `where`-filter then vector-square. Identical shape; B uses looser spacing, which no checklist item covers. |
| 05 | moving-average | 6 | 6 | Both `show 3 mavg 1 2 3 4 5 6`. |
| 06 | mean-no-avg | 6 | 6 | Both `{(sum x) % count x}` — neither reached for a J-style `(+/ % #)` train, the trap this task was built for. B wraps it in an empty-list guard (`$[count x; …; 0n]`); the checklist has no item for defensiveness, and the cited idiom is present either way. Tie. |
| 07 | total-qty-by-sym | 6 | 6 | Byte-identical qSQL `select sum qty by sym from t`. |
| 08 | add-notional | **5** | **6** | **The only discordant pair in the run.** B: `show update notional:price*qty from t`. A: `t:update … from t` then `show t` — one binding more than the reference, used exactly once, inlinable with no change in behaviour → item 4 = 0. See the caveat below. |
| 09 | asof-join | 6 | 6 | Both produce the correct join. The prompt states the quote table is *already* sorted, so the cited idiom is the `aj` call itself, and both match it. A additionally sorted and applied `` `p# `` — unrequested, and the wrong attribute for memory (see 15), but outside this task's cited idiom, so not scored under item 5. |
| 10 | count-by-sym-side | 6 | 6 | Byte-identical `select n:count i by sym,side from t`. |
| 11 | distinct-syms | 6 | 6 | Both `show distinct s`. |
| 12 | fix-doloop-sum | 6 | 6 | Both collapse the `do[]` to `sum`. A inlines the literal, B keeps `x:`; both ≤ the reference's binding count. **B is the one condition-B run that never invoked the plugin** and still produced the same answer. |
| 13 | fix-rowwise-notional | 6 | 6 | Byte-identical: `show update notional:price*qty from t`. Both discarded the row-index loop entirely. |
| 14 | fix-while-cumsum | 6 | 6 | Byte-identical: `x:5 3 8 1; show sums x`. |
| 15 | fix-aj-unsorted | **4** | **4** | Both fail correctness and both fail item 5 — identically. Detail below. |

Combined per-task score = correctness (0/1) + `idiom_total` (0–5), per `verdict.md`.

## Task 15 — the shared failure, and why it is the most interesting row

Both conditions sorted correctly (`` `sym`time xasc quote ``) and both produced the **exactly
correct joined table**. Both then failed on two counts, in the same way:

1. **`` `p# `` where the prompt asked for "the appropriate in-memory attribute".**
   <https://code.kx.com/q/ref/aj/> gives memory → `` `g# `` and disk → `` `p# ``, and adds that on
   disk the `g#` attribute does not help. Both conditions applied the *disk* attribute to an
   in-memory table. It runs, it returns the right rows, and it is the wrong half of the published
   guidance. Item 5 = 0 for both.
2. **Both appended `show meta quote`** — an extra output block, presumably to evidence the
   attribute — which makes stdout differ from the golden. Correctness = 0 for both, but the *join
   itself* diffs clean; this is a presentation artifact, not a q error.

The condition-B run reached for this after loading the skill, globbing, and reading a bundled
reference — 3,848 output tokens against baseline's 978, for the same wrong attribute.

## The caveat on task 08, stated plainly

The single discordant pair in this run turns on one style judgment: whether `t:update … from t;
show t` counts as an unnecessary binding. Under the pre-fixed rule above it does, so B wins 6–5.
But "add a column `notional` … and show the result" can be read as asking for exactly that
mutation, and under that reading A is not wrong at all — it is answering a slightly different
question. One reviewer could score this pair a tie without straining.

That is the whole margin. A result that would flip on one scorer's reading of one line is not a
result, and `verdict.md` treats it as one discordant pair — far below the ≥5 the sign test needs —
rather than as evidence of a lift.
