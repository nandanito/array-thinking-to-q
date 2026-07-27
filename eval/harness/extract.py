#!/usr/bin/env python3
"""extract.py <log.jsonl> [--field name]

Reads one subject-session stream-json log and prints one of:
  --field result   the model's final answer, verbatim (default)
  --field code     the first fenced code block in the answer (the candidate q script)
  --field tools    one line per tool_use: NAME<TAB>json-input
  --field fired    "y" if the KX q skill was invoked, else "n"
  --field tokens   output tokens
  --field turns    num_turns
"""
import json, re, sys

path = sys.argv[1]
field = "result"
if "--field" in sys.argv:
    field = sys.argv[sys.argv.index("--field") + 1]

tools, res = [], None
for line in open(path):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    if d.get("type") == "assistant":
        for b in d["message"].get("content", []):
            if b.get("type") == "tool_use":
                tools.append((b["name"], b.get("input", {})))
    elif d.get("type") == "result":
        res = d

txt = (res or {}).get("result") or ""

if field == "result":
    sys.stdout.write(txt)
elif field == "tools":
    for n, i in tools:
        print(f"{n}\t{json.dumps(i)}")
elif field == "fired":
    hit = any(
        n == "Skill" and str(i.get("skill", "")).startswith("q-knowledge")
        for n, i in tools
    )
    print("y" if hit else "n")
elif field == "tokens":
    print(((res or {}).get("usage") or {}).get("output_tokens", ""))
elif field == "turns":
    print((res or {}).get("num_turns", ""))
elif field == "code":
    # First fenced block. Contract asks for exactly one; if a model emits more,
    # the first is its answer and the extras are scored as protocol deviation.
    m = re.search(r"```[a-zA-Z]*\n(.*?)```", txt, re.S)
    sys.stdout.write(m.group(1) if m else "")
else:
    sys.exit("unknown field: " + field)
