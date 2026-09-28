#!/usr/bin/env python3
"""aggregates.py <partB-logs-dir> [--check <aggregates.md>]

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
import json, pathlib, statistics, sys

logs = pathlib.Path(sys.argv[1])
check = sys.argv[sys.argv.index("--check") + 1] if "--check" in sys.argv else None

# Tasks whose condition-B session saw an account connector's extra tools
# (verdict.md, Threats to validity).
CONNECTOR = {"03", "04", "06"}


def read(p):
    first_ts, res, loaded, invoked = None, None, False, False
    for line in p.open():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if first_ts is None and d.get("timestamp"):
            first_ts = d["timestamp"]
        if d.get("type") == "system" and d.get("subtype") == "init":
            loaded = any("q-knowledge" in str(pl) for pl in d.get("plugins", []))
        elif d.get("type") == "assistant":
            for b in d["message"].get("content", []):
                if (b.get("type") == "tool_use" and b.get("name") == "Skill"
                        and str(b.get("input", {}).get("skill", "")).startswith("q-knowledge")):
                    invoked = True
        elif d.get("type") == "result":
            res = d
    return {
        "ts": first_ts,
        "tokens": res["usage"]["output_tokens"],
        "usd": res["total_cost_usd"],
        "loaded": loaded,
        "invoked": invoked,
    }


sessions = {}
for p in sorted(logs.glob("*.jsonl")):
    task, cond = p.name.split(".")[0], p.name.split(".")[1]
    sessions[(task, cond)] = read(p)
tasks = sorted({t for t, _ in sessions})


def total(cond, key, skip=()):
    return sum(sessions[(t, cond)][key] for t in tasks if t[:2] not in skip)


ratios = {t: sessions[(t, "B")]["tokens"] / sessions[(t, "A")]["tokens"] for t in tasks}
wide = max(tasks, key=lambda t: ratios[t])
ta, tb = total("A", "tokens"), total("B", "tokens")
xa, xb = total("A", "tokens", CONNECTOR), total("B", "tokens", CONNECTOR)
ua, ub = total("A", "usd"), total("B", "usd")
ts = {c: sorted(sessions[(t, c)]["ts"] for t in tasks) for c in "AB"}

out = f"""# Part B aggregates

Derived from `runs/logs/partB/` by `harness/aggregates.py`; `make verify-eval-run`
fails if this file drifts from the logs. Condition A = baseline, B = q-knowledge plugin.

| | A | B | B / A |
|---|---:|---:|---:|
| Output tokens, {len(tasks)} tasks | {ta:,} | {tb:,} | {tb / ta:.1f}x |
| Median per-task output-token ratio | | | {statistics.median(ratios.values()):.1f}x |
| Widest single task ({wide[:2]}) | {sessions[(wide, 'A')]['tokens']:,} | {sessions[(wide, 'B')]['tokens']:,} | {ratios[wide]:.1f}x |
| Output tokens without tasks {', '.join(sorted(CONNECTOR))} | {xa:,} | {xb:,} | {xb / xa:.1f}x |
| Dollars (`total_cost_usd`) | ${ua:.3f} | ${ub:.3f} | {ub / ua:.1f}x |

- Plugin loaded: A {sum(sessions[(t, 'A')]['loaded'] for t in tasks)}/{len(tasks)}, B {sum(sessions[(t, 'B')]['loaded'] for t in tasks)}/{len(tasks)}.
- q skill invoked (`Skill` call naming `q-knowledge`): A {sum(sessions[(t, 'A')]['invoked'] for t in tasks)}/{len(tasks)}, B {sum(sessions[(t, 'B')]['invoked'] for t in tasks)}/{len(tasks)}.
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
