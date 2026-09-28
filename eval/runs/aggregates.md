# Part B aggregates

Derived from `runs/logs/partB/` by `harness/aggregates.py`; `make verify-eval-run`
fails if this file drifts from the logs. Condition A = baseline, B = q-knowledge plugin.

| | A | B | B / A |
|---|---:|---:|---:|
| Output tokens, 15 tasks | 3,671 | 10,337 | 2.8x |
| Median per-task output-token ratio | | | 3.9x |
| Widest single task (14) | 23 | 407 | 17.7x |
| Output tokens without tasks whose sessions saw extra tools (03, 04, 06) | 2,522 | 8,622 | 3.4x |
| Dollars (`total_cost_usd`) | $0.469 | $2.104 | 4.5x |

- Plugin loaded: A 0/15, B 15/15.
- q skill invoked (`Skill` call naming `q-knowledge`): A 0/15, B 14/15.
- Session run order: A 2026-07-26T14:42:20.599Z to 2026-07-26T14:43:14.934Z; B 2026-07-26T14:43:23.422Z to 2026-07-26T14:44:20.952Z.
