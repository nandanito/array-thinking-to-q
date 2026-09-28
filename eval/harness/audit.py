#!/usr/bin/env python3
"""audit.py <logs-dir> [--order order.tsv]

Fail a run whose sessions did not see the same world. Reads every
`<task>.<A|B>.jsonl` in <logs-dir> and checks, from each session's own
`system/init` line:

  1. exactly one init per log, and every task has both an A and a B log
     (unless the run was B-only, per order.tsv);
  2. the plugin under test: A sessions loaded no plugin, B sessions loaded
     exactly it (one name across the whole run, read from the logs);
  3. identical NON-TREATMENT context in every session: tools, MCP servers,
     skills and agents, once the plugin's own entries are set aside; plus the
     same model, Claude Code version, permission mode and output style;
  4. no account connector (a `claude.ai ...` MCP server) in any session;
  5. a distinct cwd and auto-memory path per session (a fresh directory each);
  6. with --order, that the sessions ran in the recorded order, by the first
     timestamp in each log.

Exit 0 only if every check passes. Run it before scoring: a run that fails
here measured something other than the plugin, and no number from it should
be published. The M2 logs fail checks 3 to 5, which is how the connector leak
and the shared directory were found (see README.md, "Known gaps").
"""
import collections, pathlib, sys

from sessionlog import load, treatment

logs = pathlib.Path(sys.argv[1])
order_file = sys.argv[sys.argv.index("--order") + 1] if "--order" in sys.argv else None
sessions = load(logs)
if not sessions:
    sys.exit(f"no session logs in {logs}")
plugin = treatment(sessions)
problems = []


def bad(msg):
    problems.append(msg)


# 1. shape
for s in sessions:
    if s.inits != 1:
        bad(f"{s.path.name}: {s.inits} system/init lines, expected 1")
    if s.cond not in ("A", "B"):
        bad(f"{s.path.name}: name is not <task>.<A|B>.jsonl")
sessions = [s for s in sessions if s.init and s.cond in ("A", "B")]
conds = collections.defaultdict(set)
for s in sessions:
    conds[s.task].add(s.cond)
planned = "AB"
if order_file:
    head = pathlib.Path(order_file).read_text().splitlines()[0]
    planned = dict(kv.split("=", 1) for kv in head.lstrip("# ").split()).get("conditions", "AB")
for t, cs in sorted(conds.items()):
    if cs != set(planned):
        bad(f"{t}: conditions {''.join(sorted(cs))}, expected {planned}")

# 2. the treatment
for s in sessions:
    want = [] if s.cond == "A" else [plugin]
    if s.plugins != want:
        bad(f"{s.path.name}: plugins {s.plugins}, expected {want}")


# 3. identical non-treatment context
def own(name):
    """Entries the plugin itself contributes: skills `<plugin>:x`, MCP tools and servers."""
    return (name.startswith(plugin + ":") or name.startswith(f"mcp__plugin_{plugin}_")
            or name.startswith(f"plugin:{plugin}:"))


def context(s):
    i = s.init
    return {
        "tools": sorted(t for t in i.get("tools", []) if not own(t)),
        "mcp_servers": sorted(m.get("name", "") for m in i.get("mcp_servers", [])
                              if not own(m.get("name", ""))),
        "skills": sorted(k for k in i.get("skills", []) if not own(k)),
        "agents": sorted(i.get("agents", [])),
        "model": i.get("model"),
        "claude_code_version": i.get("claude_code_version"),
        "permissionMode": i.get("permissionMode"),
        "output_style": i.get("output_style"),
    }


ctx = {s.path.name: context(s) for s in sessions}
for key in next(iter(ctx.values())):
    seen = collections.Counter(repr(c[key]) for c in ctx.values())
    if len(seen) > 1:
        common = seen.most_common(1)[0][0]
        odd = sorted(n for n, c in ctx.items() if repr(c[key]) != common)
        bad(f"{key} differs between sessions: {len(odd)} of {len(ctx)} depart from the "
            f"most common value ({', '.join(odd[:6])}{' ...' if len(odd) > 6 else ''})")
for s in sessions:
    if s.cond == "B" and not any(own(k) for k in s.init.get("skills", [])):
        bad(f"{s.path.name}: condition B lists no {plugin}: skill")

# 4. account connectors
leaky = sorted(s.path.name for s in sessions
               if any(m.get("name", "").startswith("claude.ai ")
                      for m in s.init.get("mcp_servers", [])))
if leaky:
    bad(f"account connectors present in {len(leaky)} session(s) ({', '.join(leaky[:6])}"
        f"{' ...' if len(leaky) > 6 else ''}); set ENABLE_CLAUDEAI_MCP_SERVERS=false")

# 5. a fresh directory per session
for key, get in (("cwd", lambda i: i.get("cwd")),
                 ("auto-memory path", lambda i: (i.get("memory_paths") or {}).get("auto"))):
    vals = collections.Counter(get(s.init) for s in sessions)
    shared = {v: n for v, n in vals.items() if n > 1}
    if shared:
        bad(f"{key} shared between sessions: {sum(shared.values())} sessions use "
            f"{len(shared)} value(s), e.g. {next(iter(shared))}")

# 6. run order
if order_file:
    rows = [ln.split("\t") for ln in pathlib.Path(order_file).read_text().splitlines()
            if ln and not ln.startswith("#")]
    recorded = [f"{t}.{c}.jsonl" for _, t, c in rows]
    missing_ts = [s.path.name for s in sessions if not s.first_ts]
    if missing_ts:
        bad(f"no timestamp in {missing_ts[:6]}")
    else:
        ran = [s.path.name for s in sorted(sessions, key=lambda s: s.first_ts)]
        if ran != recorded:
            bad(f"sessions did not run in the order recorded in {order_file}")

n = len(sessions)
print(f"{n} sessions, plugin under test: {plugin}")
if problems:
    print(f"AUDIT FAILED ({len(problems)} problem(s)):")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("audit passed: one treatment, identical non-treatment context, no connectors, "
      "a fresh directory per session" + (", recorded order" if order_file else ""))
