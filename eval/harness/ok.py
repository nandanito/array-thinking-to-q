#!/usr/bin/env python3
"""Exit 0 iff the stream-json log ends in a clean, non-empty result."""
import json, sys

def result(path):
    last = None
    try:
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "result":
                last = d
    except FileNotFoundError:
        return None
    return last

d = result(sys.argv[1])
if d is None:
    sys.exit(1)
if d.get("is_error"):
    sys.exit(1)
txt = d.get("result") or ""
if not txt.strip() or txt.lstrip().startswith("API Error"):
    sys.exit(1)
sys.exit(0)
