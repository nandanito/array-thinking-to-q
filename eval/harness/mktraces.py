#!/usr/bin/env python3
"""mktraces.py <logs-dir> [--check <traces.md>]

Regenerate `eval/runs/traces.md` from the committed session logs. With
`--check`, regenerate and diff against the committed file instead of printing —
exit 1 on any difference.

This exists so the activation and token claims in `verdict.md` are auditable
from committed artifacts rather than taken on trust: the table is *derived*, and
`make verify` proves it still matches the logs it claims to summarise.
"""
import json, pathlib, sys

logs = pathlib.Path(sys.argv[1])
check = sys.argv[sys.argv.index("--check") + 1] if "--check" in sys.argv else None

# The session log does not echo the prompt back (the `user` entries are tool
# results), so prompt text comes from the committed prompt files — which are the
# exact bytes that were fed to `claude -p`.
PROMPTS = logs.parent / "prompts"

def read(p):
    tools, res = [], None
    for line in p.open():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("type") == "assistant":
            for b in d["message"].get("content", []):
                if b.get("type") == "tool_use":
                    tools.append((b["name"], b.get("input", {})))
        elif d.get("type") == "result":
            res = d
    fired = any(n == "Skill" and str(i.get("skill", "")).startswith("q-knowledge")
                for n, i in tools)
    chain = " → ".join(n for n, _ in tools) or "_(none)_"
    tok = ((res or {}).get("usage") or {}).get("output_tokens", "")
    return chain, fired, tok

out = []
out.append("# Raw session traces — M2 eval")
out.append("")
out.append("**Derived from the committed logs in [`logs/`](logs/)** by "
           "`eval/harness/mktraces.py`, and re-checked by `make verify-eval-run` — so the")
out.append("activation and token numbers in `../verdict.md` can be audited without trusting this")
out.append("table. \"Fired\" means the session actually emitted a `Skill` tool call naming a")
out.append("`q-knowledge` skill, not that the answer *looked* q-flavoured. Condition A has no such")
out.append("skill to call; its logs record `\"plugins\": []`.")
out.append("")
out.append("## Part A — 20 trigger sessions (condition B only)")
out.append("")
out.append("Prompt text is the exact bytes fed to `claude -p`, from [`prompts/`](prompts/).")
out.append("")
out.append("| session | prompt | tool calls in order | fired |")
out.append("|---|---|---|:---:|")
for p in sorted((logs / "partA").glob("*.jsonl")):
    chain, fired, _ = read(p)
    prompt = (PROMPTS / "A" / f"{p.stem}.txt").read_text().strip().replace("|", "\\|")
    out.append(f"| {p.stem} | {prompt} | {chain} | **{'y' if fired else 'n'}** |")
out.append("")
out.append("## Part B — 30 generation sessions")
out.append("")
out.append("| task | cond | tool calls in order | q skill fired | output tokens |")
out.append("|---|:---:|---|:---:|---:|")
for p in sorted((logs / "partB").glob("*.jsonl")):
    task, cond = p.stem.rsplit(".", 1)
    chain, fired, tok = read(p)
    out.append(f"| {task} | {cond} | {chain} | **{'y' if fired else 'n'}** | {tok} |")
text = "\n".join(out) + "\n"

if check:
    have = pathlib.Path(check).read_text()
    if have != text:
        import difflib
        sys.stdout.writelines(difflib.unified_diff(
            have.splitlines(True), text.splitlines(True),
            fromfile=check, tofile="regenerated"))
        sys.exit(f"\n{check} does not match the committed logs")
    print(f"{check}: matches the committed logs")
else:
    sys.stdout.write(text)
