#!/usr/bin/env python3
"""extract.py <log.jsonl> [--field name] [--plugin name]

Reads one subject-session stream-json log and prints one of:
  --field result   the model's final answer, verbatim (default)
  --field code     the first fenced code block in the answer (the candidate script)
  --field tools    one line per tool_use: NAME<TAB>json-input
  --field fired    "y" if the plugin's skill was invoked, else "n"
  --field tokens   output tokens
  --field turns    num_turns

`fired` needs to know the plugin under test. It defaults to the plugin this
log's own system/init loaded, so a condition-A log (no plugin) always prints
"n"; pass --plugin to test an A log against the B plugin's name explicitly.
"""
import json, re, sys

from sessionlog import Session


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


s = Session(sys.argv[1])
field = arg("--field", "result")
txt = s.answer

if field == "result":
    sys.stdout.write(txt)
elif field == "tools":
    for n, i in s.tool_uses:
        print(f"{n}\t{json.dumps(i)}")
elif field == "fired":
    plugin = arg("--plugin", s.plugins[0] if s.plugins else None)
    print("y" if s.fired(plugin) else "n")
elif field == "tokens":
    print(s.output_tokens)
elif field == "turns":
    print((s.result or {}).get("num_turns", ""))
elif field == "code":
    # First fenced block. Contract asks for exactly one; if a model emits more,
    # the first is its answer and the extras are scored as protocol deviation.
    m = re.search(r"```[a-zA-Z]*\n(.*?)```", txt, re.S)
    sys.stdout.write(m.group(1) if m else "")
else:
    sys.exit("unknown field: " + field)
