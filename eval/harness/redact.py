#!/usr/bin/env python3
"""redact.py <src-dir> <dest-dir>

Copy subject-session stream-json logs for publication in a public repo.

Exactly two changes are made, and they are the only two:

1. **`rate_limit_event` lines are dropped.** They carry the *author's account*
   quota utilisation, which is not eval data and does not belong in a public
   repo. Nothing else reads them.
2. **Machine-specific absolute paths are rewritten** to stable placeholders, so
   the logs do not hard-code one laptop's directory layout. `$NEUTRAL` is the
   session cwd (the neutral directory outside the repo); `$KX` is the
   q-knowledge plugin checkout; `$HOME` catches the rest (notably the
   `memory_paths.auto` directory Claude Code derives for any cwd — which was
   **empty** for the neutral directory, so no session loaded any memory).

Everything else is byte-for-byte the session output — including the `system/init`
line, which is the per-session proof of the contamination control: condition A
logs carry `"plugins": []` and no q skill, condition B logs carry exactly
`q-knowledge` 0.1.0 plus `q-knowledge:q` / `q-knowledge:qlint-snippet`.
"""
import json, os, pathlib, re, sys

src, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
HOME = os.path.expanduser("~")

# Learn the two machine-specific prefixes from the logs themselves rather than
# hard-coding one machine's layout.
NEUTRAL = KX = None
for p in sorted(src.rglob("*.jsonl")):
    for line in p.open():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("type") == "system" and d.get("subtype") == "init":
            NEUTRAL = NEUTRAL or d.get("cwd")
            for pl in d.get("plugins") or []:
                KX = KX or pl.get("path")
            break
    if NEUTRAL and KX:
        break
if not NEUTRAL:
    sys.exit("no system/init line found — is this a stream-json log directory?")

dropped = rewritten = kept = 0
for p in sorted(src.rglob("*.jsonl")):
    out = dest / p.relative_to(src)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for line in p.open():
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if json.loads(line).get("type") == "rate_limit_event":
            dropped += 1
            continue
        new = line.replace(KX, "$KX") if KX else line
        new = new.replace(NEUTRAL, "$NEUTRAL").replace(HOME, "$HOME")
        rewritten += new != line
        kept += 1
        lines.append(new)
    out.write_text("\n".join(lines) + "\n")

print(f"{kept} lines kept, {dropped} rate_limit_event dropped, {rewritten} path-rewritten")
print(f"  $NEUTRAL = {NEUTRAL}")
print(f"  $KX      = {KX}")
# Nothing may survive that names the real home directory.
leaked = [p.name for p in dest.rglob("*.jsonl") if re.search(r"/Users/[^/\"]+", p.read_text())]
if leaked:
    sys.exit(f"redaction incomplete, absolute home paths remain in: {leaked[:5]}")
print("no absolute home paths remain")
