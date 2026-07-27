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

**True positives: 8/10. That is the activation recall for this run — the only one.**

Prompts 3 and 7 are **defective test items**: their text refers to code ("this q code", "this list
comprehension") that the table never supplies, so in an empty directory the model searched, found
nothing, and asked for the input. No q was attempted in either.

That diagnosis explains the two misses; it does **not** license a second, kinder denominator.
Re-scoring 8/8 over "the well-formed prompts" would be choosing the denominator after seeing which
items missed — the same overfitting the protocol forbids when tuning trigger wording against a test
set. The honest position is that this instrument measured **8/10**, and that two of its twenty
items were malformed.

Fixing the two prompts means attaching real snippets, which makes a **different test set**. Any
number from that set has to come from a fresh run, and cannot be reported as this run's result.

