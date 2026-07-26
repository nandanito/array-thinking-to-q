# Part A — prompts that SHOULD fire the q skill

Ten prompts with explicit q / kdb+ / qSQL / aj context. The skill under test (KX's
`q-knowledge@kx-skills`) should activate on all ten. Run each in a fresh context, record
fire / no-fire, then compute the true-positive rate. After any trigger tuning of a *self-authored*
skill, re-run on FRESH prompts (SPEC.md) — do not report tuning-set numbers.

**Run 2026-07-26/27**, condition B only (see `../README.md` — "fire/no-fire" is undefined for
condition A, which has no plugin to activate). One fresh headless session per prompt, neutral cwd.
"Fired" is decided mechanically: the session emitted a `Skill` tool call naming a `q-knowledge`
skill. Per-session tool traces: [`../runs/traces.md`](../runs/traces.md).

| # | Prompt | Fired? (y/n) | Notes |
|---|--------|:---:|-------|
| 1 | Write a q function to compute the moving average of a price vector. | y | `Skill(q-knowledge:q)` first call, no other tools. |
| 2 | Translate this pandas `groupby().sum()` into a kdb+ qSQL `select … by`. | y | Fired, then read its own `python-q-mapping.md`, then re-entered the skill. |
| 3 | Fix this q code — it uses a `do`-loop where a vector op would do. | **n** | **Instrument artifact, not a trigger miss** — the prompt says "this q code" but the table carries no code, and the cwd is empty. The model globbed for `**/*.q`, found nothing, and replied "paste the snippet and I'll vectorize it". No q work was attempted, so there was nothing for a skill to assist with. |
| 4 | How do I do an as-of join in kdb+ to match trades to the prevailing quote? | y | Fired immediately. |
| 5 | Write a qSQL query for total volume by symbol from a trades table. | y | Fired twice (re-entered the skill mid-answer). |
| 6 | My `aj` returns wrong quotes — what sort order and attribute do I need? | y | Fired, then globbed for a local table definition. |
| 7 | Convert this Python list comprehension into idiomatic q. | **n** | **Same artifact as #3** — no comprehension in the prompt. Model asked for it. (It did volunteer correct q idioms in passing — `xs where p xs`, `a f' b` — without loading the skill.) |
| 8 | Create a keyed table in q and look up a row by its key. | y | Fired immediately. |
| 9 | Rewrite this q `while`-loop accumulator using over/scan. | y | Globbed twice, then fired. |
| 10 | What's the idiomatic q way to count occurrences of each symbol? | y | Fired immediately. |

**True positives:** **8/10** as measured.

Read with the artifact in mind: prompts 3 and 7 are the two whose text refers to code that the
table never supplies, and in both the model correctly declined to invent the input rather than
doing q work. On the **8 prompts that actually presented a q task, activation was 8/8.** Both
numbers belong in the writeup — 8/10 is what the pre-registered instrument measured, 8/8 is what
it measured *about the plugin*. The fix for a future re-test is to attach real snippets to those
two prompts; that is a change to the test set, so it cannot be applied retroactively to this run.
