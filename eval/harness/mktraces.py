#!/usr/bin/env python3
"""mktraces.py <logs-dir> [--title T] [--lang L] [--check <traces.md>]

Regenerate a traces table (`eval/runs/traces.md` for M2) from the committed
session logs. With `--check`, regenerate and diff against the committed file
instead of printing; exit 1 on any difference.

<logs-dir> holds `partB/` (generation sessions, `<task>.<A|B>.jsonl`) and,
optionally, `partA/` (activation sessions). Prompt text for Part A comes from
`<logs-dir>/../prompts/A/`.

This exists so the activation and token claims in a verdict are auditable
from committed artifacts rather than taken on trust: the table is *derived*, and
`make verify` proves it still matches the logs it claims to summarise. Every
count and name in the prose, including which plugin "fired" refers to, is read
from the logs too; none is typed in.
"""
import pathlib, sys

from sessionlog import load, treatment

logs = pathlib.Path(sys.argv[1])
check = sys.argv[sys.argv.index("--check") + 1] if "--check" in sys.argv else None
title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else logs.parent.name
# The task language, if the study has one ("q" for M2): only used in wording.
lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None

# The session log does not echo the prompt back (the `user` entries are tool
# results), so prompt text comes from the committed prompt files — which are the
# exact bytes that were fed to `claude -p`.
PROMPTS = logs.parent / "prompts"

part_a = load(logs / "partA") if (logs / "partA").is_dir() else []
part_b = load(logs / "partB")
plugin = treatment(part_a + part_b)


def chain(s):
    return " → ".join(n for n, _ in s.tool_uses) or "_(none)_"


out = []
out.append(f"# Raw session traces — {title}")
out.append("")
out.append("**Derived from the committed logs in [`logs/`](logs/)** by "
           f"`{sys.argv[0]}`, and re-checked by `make verify-eval-run` — so the")
out.append("activation and token numbers in `../verdict.md` can be audited without trusting this")
out.append("table. \"Fired\" means the session actually emitted a `Skill` tool call naming a")
out.append(f"`{plugin}` skill, not that the answer *looked* "
           + (f"{lang}-flavoured" if lang else "like it used one") + ". Condition A has no such")
out.append("skill to call; its logs record `\"plugins\": []`.")
out.append("")
if part_a:
    # "Condition B only" is a claim about the logs, so it is checked, not typed.
    only_b = all(s.plugins == [plugin] for s in part_a)
    out.append(f"## Part A — {len(part_a)} trigger sessions"
               + (" (condition B only)" if only_b else ""))
    out.append("")
    out.append("Prompt text is the exact bytes fed to `claude -p`, from [`prompts/`](prompts/).")
    out.append("")
    out.append("| session | prompt | tool calls in order | fired |")
    out.append("|---|---|---|:---:|")
    for s in part_a:
        prompt = (PROMPTS / "A" / f"{s.path.stem}.txt").read_text().strip().replace("|", "\\|")
        out.append(f"| {s.path.stem} | {prompt} | {chain(s)} | **{'y' if s.fired(plugin) else 'n'}** |")
    out.append("")
out.append(f"## Part B — {len(part_b)} generation sessions")
out.append("")
out.append(f"| task | cond | tool calls in order | {lang + ' ' if lang else ''}skill fired | output tokens |")
out.append("|---|:---:|---|:---:|---:|")
for s in part_b:
    task, cond = s.path.stem.rsplit(".", 1)
    out.append(f"| {task} | {cond} | {chain(s)} | **{'y' if s.fired(plugin) else 'n'}** | {s.output_tokens} |")
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
