#!/usr/bin/env python3
"""redact.py <src-dir> <dest-dir>

Copy subject-session stream-json logs for publication in a public repo.

Exactly two changes are made, and they are the only two:

1. **`rate_limit_event` lines are dropped.** They carry the *author's account*
   quota utilisation, which is not eval data and does not belong in a public
   repo. Nothing else reads them.
2. **Machine-specific absolute paths are rewritten** to stable placeholders, so
   the logs do not hard-code one laptop's directory layout. `$PLUGIN` is the
   plugin checkout; `$TMPDIR` is the directory session.sh makes its per-session
   neutral directories in, so each log keeps its own `atq-neutral.XXXXXX` name
   (audit.py checks those stay distinct); `$HOME` catches the rest, notably the
   `memory_paths.auto` directory Claude Code derives from each cwd.

Everything else is byte-for-byte the session output, including the `system/init`
line, which is the per-session proof of the contamination control.

The M2 logs in eval/runs/logs were redacted by the earlier version of this
script (see git history), when every session shared one directory: there, the
whole cwd became `$NEUTRAL` and the plugin path `$KX`.
"""
import json, os, pathlib, re, sys

src, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
HOME = os.path.expanduser("~")


def mangled(path):
    # How Claude Code turns a cwd into a directory name under ~/.claude/projects.
    return re.sub(r"[^A-Za-z0-9-]", "-", path)


dropped = rewritten = kept = 0
learned = set()
for p in sorted(src.rglob("*.jsonl")):
    lines = [ln.rstrip("\n") for ln in p.open() if ln.strip()]
    # Learn this log's own prefixes from its init line, rather than assuming one
    # machine's layout or one directory for the whole run.
    subs = []
    for ln in lines:
        d = json.loads(ln)
        if d.get("type") == "system" and d.get("subtype") == "init":
            for pl in d.get("plugins") or []:
                if pl.get("path"):
                    subs.append((pl["path"], "$PLUGIN"))
            if d.get("cwd"):
                parent = os.path.dirname(d["cwd"])
                subs += [(parent, "$TMPDIR"), (mangled(parent), "$TMPDIR")]
            break
    else:
        sys.exit(f"{p}: no system/init line, is this a stream-json log?")
    subs.append((HOME, "$HOME"))
    learned.update(f"{v} = {k}" for k, v in subs if v != "$HOME")

    out = dest / p.relative_to(src)
    out.parent.mkdir(parents=True, exist_ok=True)
    keep = []
    for line in lines:
        if json.loads(line).get("type") == "rate_limit_event":
            dropped += 1
            continue
        new = line
        for k, v in subs:
            new = new.replace(k, v)
        rewritten += new != line
        kept += 1
        keep.append(new)
    out.write_text("\n".join(keep) + "\n")

print(f"{kept} lines kept, {dropped} rate_limit_event dropped, {rewritten} path-rewritten")
for s in sorted(learned):
    print("  " + s)
# Nothing may survive that names the real home directory.
user = os.path.basename(HOME)
leaked = [p.name for p in dest.rglob("*.jsonl")
          if HOME in p.read_text() or re.search(rf"[/-]{re.escape(user)}[/-]", p.read_text())]
if leaked:
    sys.exit(f"redaction incomplete, the home directory or user name remains in: {leaked[:5]}")
print("no home directory or user name remains")
