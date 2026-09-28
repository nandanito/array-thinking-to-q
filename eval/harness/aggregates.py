#!/usr/bin/env python3
"""aggregates.py <partB-logs-dir> [--lang L] [--check <aggregates.md>]

Derive the Part B aggregates that `verdict.md` and the eval article quote
(output-token totals and ratios, the connector sensitivity, dollar totals,
plugin load and q-skill invocation counts, the session run order) from the
committed session logs. With `--check`, regenerate and diff against the
committed file instead of printing; exit 1 on any difference.

Sibling of mktraces.py: that one derives the per-session table, this one the
numbers built on top of it. Without it, those numbers were prose that happened
to be true on the day (added 2026-09-28, when the eval article's content review
added the dollar and connector figures).
"""
import pathlib, statistics, sys

from sessionlog import load, treatment

logs = pathlib.Path(sys.argv[1])
check = sys.argv[sys.argv.index("--check") + 1] if "--check" in sys.argv else None
# The task language, if the study has one ("q" for M2): only used in wording.
lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None

every = load(logs)
plugin = treatment(every)

# The tools every session was granted. session.sh passes both conditions the
# same --tools, so the baseline is what ALL sessions saw; a pair is excluded
# from the "without extra tools" row when either session's system/init lists
# anything beyond it (in the M2 run: an account connector, verdict.md, Threats
# to validity). Derived per session, never hardcoded. audit.py is the stricter
# gate for new runs: it fails the run outright instead of reporting around it.
INTENDED = set.intersection(*(set(s.init.get("tools", [])) for s in every))


def read(s):
    return {
        "ts": s.first_ts,
        "tokens": s.result["usage"]["output_tokens"],
        "usd": s.result["total_cost_usd"],
        "loaded": plugin in s.plugins,
        "invoked": s.fired(plugin),
        "extra": bool(set(s.init.get("tools", [])) - INTENDED),
    }


sessions = {(s.task, s.cond): read(s) for s in every}
tasks = sorted({t for t, _ in sessions})
unpaired = [t for t in tasks if (t, "A") not in sessions or (t, "B") not in sessions]
if unpaired:
    sys.exit(f"tasks without both an A and a B log: {unpaired}")
CONNECTOR = {t[:2] for t in tasks if sessions[(t, "A")]["extra"] or sessions[(t, "B")]["extra"]}


def total(cond, key, skip=()):
    return sum(sessions[(t, cond)][key] for t in tasks if t[:2] not in skip)


ratios = {t: sessions[(t, "B")]["tokens"] / sessions[(t, "A")]["tokens"] for t in tasks}
wide = max(tasks, key=lambda t: ratios[t])
ta, tb = total("A", "tokens"), total("B", "tokens")
xa, xb = total("A", "tokens", CONNECTOR), total("B", "tokens", CONNECTOR)
ua, ub = total("A", "usd"), total("B", "usd")
ts = {c: sorted(sessions[(t, c)]["ts"] for t in tasks) for c in "AB"}

out = f"""# Part B aggregates

Derived from `{sys.argv[1].rstrip('/')}/` by `{sys.argv[0]}`; `make verify-eval-run`
fails if this file drifts from the logs. Condition A = baseline, B = {plugin} plugin.

| | A | B | B / A |
|---|---:|---:|---:|
| Output tokens, {len(tasks)} tasks | {ta:,} | {tb:,} | {tb / ta:.1f}x |
| Median per-task output-token ratio | | | {statistics.median(ratios.values()):.1f}x |
| Widest single task ({wide[:2]}) | {sessions[(wide, 'A')]['tokens']:,} | {sessions[(wide, 'B')]['tokens']:,} | {ratios[wide]:.1f}x |
| Output tokens without tasks whose sessions saw extra tools ({', '.join(sorted(CONNECTOR)) or 'none'}) | {xa:,} | {xb:,} | {xb / xa:.1f}x |
| Dollars (`total_cost_usd`) | ${ua:.3f} | ${ub:.3f} | {ub / ua:.1f}x |

- Plugin loaded: A {sum(sessions[(t, 'A')]['loaded'] for t in tasks)}/{len(tasks)}, B {sum(sessions[(t, 'B')]['loaded'] for t in tasks)}/{len(tasks)}.
- {lang + ' ' if lang else ''}skill invoked (`Skill` call naming `{plugin}`): A {sum(sessions[(t, 'A')]['invoked'] for t in tasks)}/{len(tasks)}, B {sum(sessions[(t, 'B')]['invoked'] for t in tasks)}/{len(tasks)}.
- Session run order: A {ts['A'][0]} to {ts['A'][-1]}; B {ts['B'][0]} to {ts['B'][-1]}.
"""

if check:
    committed = pathlib.Path(check).read_text()
    if committed != out:
        import difflib
        sys.stdout.writelines(difflib.unified_diff(
            committed.splitlines(True), out.splitlines(True), check, "derived from logs"))
        sys.exit(1)
    print(f"{check}: matches the committed logs")
else:
    sys.stdout.write(out)
