#!/usr/bin/env python3
"""Em-dash budget for the blog articles and their posts in writings/.

Heavy em-dash use reads as machine-generated prose, and nandan.me (where these
articles are published, and which is canonical) enforces a budget on import.
Keeping the same rule here means the site sync is a no-op instead of a rewrite
that then has to be copied back. The rule matches nandan.me's
_tools/check_em_dashes.py:

  - at most 2 em dashes per 1,000 words of prose, with a floor of 2 per file;
  - none in the title, headings or figure captions (the *Figure N. ...* lines).

Code (fenced blocks and inline code) and HTML tags/attributes are not counted.
En dashes in ranges ("2–4") are fine. Rewrite with commas, colons, parentheses
or full stops; keep an em dash only where it carries a deliberate beat.

LEGACY lists articles written before the rule that have not had their pass
yet. They are reported on every run (so the exemption cannot go quiet) and
come off the list when they are next edited for publication.

Usage:
  check-em-dashes.py [FILE ...]   check files (default: all writings/*.md);
                                  exit 1 on any violation
  check-em-dashes.py --hook       Claude Code PostToolUse hook: read the hook
                                  JSON on stdin, check the edited file if it is
                                  under writings/, exit 2 with the violations
                                  on stderr
"""

import glob
import json
import os
import re
import sys

EM = "\u2014"
PER_1000 = 2
FLOOR = 2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY = {
    "writings/04-unlearn-the-loop.md",
}


def rel(path):
    return os.path.relpath(os.path.abspath(path), ROOT)


def in_scope(path):
    r = rel(path)
    return (r.startswith("writings" + os.sep) and r.endswith(".md")
            and os.sep not in r[len("writings") + 1:])


def prose(text):
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    text = re.sub(r"`[^`\n]*`", "", text)
    return re.sub(r"<[^>]+>", "", text)


def check(path):
    """Return (problems, count, words) for one file."""
    text = open(path, encoding="utf-8").read()
    p = prose(text)
    problems = []
    for line in p.split("\n"):
        s = line.strip()
        if EM not in s:
            continue
        if re.match(r"#{1,6} ", s):
            problems.append("heading has an em dash: %s" % s[:90])
        elif re.match(r"\*Figure \d", s):
            problems.append("figure caption has an em dash: %s" % s[:90])
    count = p.count(EM)
    words = len(p.split())
    budget = max(FLOOR, words * PER_1000 // 1000)
    if count > budget:
        problems.append("%d em dashes in %d words of prose; budget is %d "
                        "(%d per 1,000 words, minimum %d)"
                        % (count, words, budget, PER_1000, FLOOR))
    return problems, count, words


def lines_with_dashes(path):
    out, in_code = [], False
    for n, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and EM in re.sub(r"`[^`\n]*`|<[^>]+>", "", line):
            out.append("  line %d: %s" % (n, line.strip()[:110]))
    return out


def hook():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path or not os.path.exists(path) or not in_scope(path):
        return 0
    if rel(path) in LEGACY:
        return 0
    problems, _, _ = check(path)
    if not problems:
        return 0
    sys.stderr.write(
        "Em-dash budget exceeded in %s (CLAUDE.md, Voice):\n- %s\n"
        "Rewrite with commas, colons, parentheses or full stops. Keep an em dash "
        "only where it carries a deliberate beat. Don't touch code blocks, and "
        "keep article text identical to nandan.me once published.\n"
        "Lines with em dashes:\n%s\n"
        % (rel(path), "\n- ".join(problems), "\n".join(lines_with_dashes(path))))
    return 2


def main(argv):
    if argv[:1] == ["--hook"]:
        return hook()
    files = argv or sorted(glob.glob(os.path.join(ROOT, "writings", "*.md")))
    failed = False
    for f in files:
        problems, count, words = check(f)
        name = rel(f)
        if name in LEGACY:
            print("LEGACY %s: %d em dashes, %d words (not enforced until its pass)"
                  % (name, count, words))
        elif problems:
            failed = True
            print("FAIL %s:\n- %s" % (name, "\n- ".join(problems)))
        else:
            print("ok   %s (%d em dashes, %d words)" % (name, count, words))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
