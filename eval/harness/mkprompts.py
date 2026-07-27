#!/usr/bin/env python3
"""Build Part B prompt files from the task sheets.

Each prompt = the verbatim blockquote under "## Prompt" in eval/tasks/q/NN-*.md,
de-quoted, plus one fixed OUTPUT CONTRACT appended identically in both
conditions. The contract exists only so a candidate answer can be turned into a
runnable script deterministically; it names no idiom under test.
"""
import pathlib, re, sys, textwrap

TASKS = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

CONTRACT = (
    "Reply with exactly one q code block and nothing else: no prose before or after it, "
    "no alternatives, and no `q)` REPL prompts. The block must be a complete, self-contained "
    "q script that prints the required result to stdout using `show` when run as `q script.q -q`."
)

for md in sorted(TASKS.glob("[0-9][0-9]-*.md")):
    text = md.read_text()
    m = re.search(r"^## Prompt.*?\n\n(.*?)\n\n## ", text, re.S | re.M)
    if not m:
        sys.exit(f"no Prompt block in {md}")
    lines = []
    for ln in m.group(1).splitlines():
        if ln.startswith("> "):
            lines.append(ln[2:])
        elif ln.strip() == ">":
            lines.append("")
        else:
            sys.exit(f"non-blockquote line in {md}: {ln!r}")
    prompt = "\n".join(lines).rstrip()
    dest = OUT / (md.stem + ".txt")
    dest.write_text(prompt + "\n\n" + CONTRACT + "\n")
    print(f"{dest.name}  ({len(prompt.splitlines())} prompt lines)")
