#!/usr/bin/env python3
"""No comparative speed wording in the articles, posts, figures or lessons.

The KDB-X Community Edition licence restricts publishing "benchmark, test or
performance information" without KX's written consent (Clause 9). As a
precaution, the author decided on 2026-09-25 to keep q's attributes and joins
semantic in everything published here, and to drop speed wording entirely:
PR #28 removed it from the articles, PR #35 from the lessons. The rule then
lived only in those PR descriptions, and the next piece of writing (the
"What compounds" draft, 2026-09-28) reintroduced a KX "better speedups" quote.
This check is the rule in a form that fails.

It flags the phrase families those two PRs removed: speedups; fast/faster/
slow/slower and the like; outperform; efficient; speed or performance as the
purpose of something ("the speed step", "for speed", "performance lever"); an
operation called cheap ("a cheap local check"); a scan as a cost ("costs a scan
per trade"); complexity claims (O(log n));
timing figures (3 ms); latency and throughput. Saying that there is no speed
claim ("no speed or performance wording", "no benchmark numbers") is fine and
is not matched. Code blocks are checked too: a comment can carry a claim.

ALLOWED lists the exemptions: text already published before the rule. Each
covers exactly one occurrence, so a second copy of an exempted phrase fails.
Each is printed on every run, so an exemption cannot go quiet, and a default
run FAILS if an exempted phrase or its file is gone, so the list cannot go
stale either.

Usage:
  check-speed-wording.py [FILE ...]  check files (default: writings/*.md, the
                                     figures, the lesson READMEs and sources);
                                     exit 1 on any violation
  check-speed-wording.py --hook      Claude Code PostToolUse hook: check the
                                     edited file if in scope; exit 2 with the
                                     matches on stderr
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    (r"\bspeed\s*-?\s*ups?\b", "speedup"),
    (r"\b(?:fast|faster|fastest|slow|slower|slowest|quicker|quickest)\b", "speed adjective"),
    (r"\boutperform\w*", "outperform"),
    (r"\befficien(?:t|tly|cy)\b", "efficiency"),
    # "speed" itself, unless the text is saying there is none: "no speed or
    # performance wording", "no speed claims here". Catches "the speed step",
    # "for speed", "(Speed; ...)" and a "/ speed: ..." comment label.
    (r"(?<!no )(?<!no-)\bspeed\b(?!\s+(?:or\s+performance\s+wording|claims?)\b)",
     "speed as a purpose"),
    # An operation called cheap: "a cheap local check", "cheaply, by comparing".
    # ("Cheapest improvement" in the ordinary sense is not matched.)
    (r"\bcheap(?:ly)?\b", "a cost claim"),
    (r"\bperformance\s+(?:lever|win|gain|boost|benefit)s?\b", "performance as a purpose"),
    (r"\bcosts?\s+(?:a|an|one|you\s+a)\s+(?:full\s+|real\s+)?(?:scan|pass)\b", "a scan as a cost"),
    (r"\bscans?\s+per\b", "a scan as a cost"),
    (r"\bO\((?:1|n|log)", "complexity claim"),
    (r"\b\d+(?:\.\d+)?\s*(?:ms|µs|us|ns|milliseconds?|microseconds?|nanoseconds?)\b",
     "timing figure"),
    (r"\blatenc(?:y|ies)\b|\bthroughput\b", "latency or throughput"),
]
PATTERN = re.compile("|".join(f"(?:{p})" for p, _ in PATTERNS), re.I)

# (file, exact text, reason). Published before the rule; change the live page
# first, then sync the repo copy and delete the entry.
ALLOWED = [
    ("writings/01-array-thinking-all-the-way-to-q.md", "can be *faster*",
     "article 1, live on nandan.me since 2026-09-25, before the speed-wording "
     "decision; edit the site first if it should go"),
]


def rel(path):
    return os.path.relpath(os.path.abspath(path), ROOT)


def in_scope(path):
    r = rel(path).split(os.sep)
    if r[0] == "writings":
        return (len(r) == 2 and r[1].endswith(".md")) or (
            len(r) > 2 and r[1] == "figures" and r[-1].endswith(".svg"))
    if r[0] == "lessons":
        return r[-1] == "README.md" or r[-1].endswith((".q", ".ijs"))
    return False


def label(text):
    for p, name in PATTERNS:
        if re.fullmatch(p, text, re.I):
            return name
    return "speed wording"


def check(path):
    """Return (problems, exempted) for one file."""
    text = open(path, encoding="utf-8").read()
    name = rel(path)
    allowed = [(t, why) for f, t, why in ALLOWED if f == name]
    spans = []
    for t, _ in allowed:
        spans += [(m.start(), m.end()) for m in re.finditer(re.escape(t), text)]
    problems, exempted = [], []
    for m in PATTERN.finditer(text):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        n = text.count("\n", 0, m.start()) + 1
        line = text.split("\n")[n - 1].strip()
        problems.append("line %d (%s): %s" % (n, label(m.group(0)), line[:110]))
    for t, why in allowed:
        n = text.count(t)
        if n == 1:
            exempted.append("%r: %s" % (t, why))
        elif n == 0:
            problems.append("stale exemption: %r is no longer in this file; remove it "
                            "from ALLOWED in tools/check-speed-wording.py" % t)
        else:
            problems.append("exemption %r covers one published occurrence, but the file "
                            "has %d" % (t, n))
    return problems, exempted


def hook():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path or not os.path.exists(path) or not in_scope(path):
        return 0
    problems, _ = check(path)
    if not problems:
        return 0
    sys.stderr.write(
        "Speed wording in %s (Clause 9 caution, PRs #28 and #35):\n- %s\n"
        "Describe what an attribute or join does, not how fast it is. Saying there "
        "is no speed claim is fine.\n" % (rel(path), "\n- ".join(problems)))
    return 2


def default_files():
    return (sorted(glob.glob(os.path.join(ROOT, "writings", "*.md")))
            + sorted(glob.glob(os.path.join(ROOT, "writings", "figures", "**", "*.svg"),
                               recursive=True))
            + [os.path.join(ROOT, "lessons", "README.md")]
            + sorted(glob.glob(os.path.join(ROOT, "lessons", "*", "README.md")))
            + sorted(glob.glob(os.path.join(ROOT, "lessons", "**", "*.q"), recursive=True))
            + sorted(glob.glob(os.path.join(ROOT, "lessons", "**", "*.ijs"), recursive=True)))


def main(argv):
    if argv[:1] == ["--hook"]:
        return hook()
    files = argv or default_files()
    failed = False
    if not argv:
        # An exemption whose file was renamed or deleted would otherwise never be
        # visited, and would outlive the text it was written for.
        for f, t, _ in ALLOWED:
            if not os.path.exists(os.path.join(ROOT, f)):
                failed = True
                print("FAIL stale exemption: %s no longer exists; remove %r from ALLOWED" % (f, t))
    for f in files:
        problems, exempted = check(f)
        for e in exempted:
            print("ALLOWED %s: %s" % (rel(f), e))
        if problems:
            failed = True
            print("FAIL %s:\n- %s" % (rel(f), "\n- ".join(problems)))
    print("speed wording: %s (%d file(s) checked)" % ("FOUND" if failed else "none", len(files)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
