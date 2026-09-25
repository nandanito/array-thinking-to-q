#!/usr/bin/env python3
"""Check that every code block in a blog article was copied from running code.

RELEASE-CHECKLIST requires every snippet in an article to come from a RUNNING
lesson file. `make verify-prose` proves the lessons' pasted blocks are real;
this closes the gap between a lesson and the article that quotes it. Three of
the Codex findings on 2026-09-25 were exactly this defect, found by hand: a
block that was only the first lines of a lesson block, and a block written
from memory.

Rule: every fenced block (```q, ```j, ```python, or a bare ``` output block)
in writings/NN-*.md must be
  - IDENTICAL to a fenced block in some lessons/*/README.md, or
  - a contiguous run of whole lines of a committed eval answer
    (eval/runs/*.q), which article 3 quotes.
Whole-block identity is deliberate: a prefix of a lesson block is a different
snippet, and a line-by-line match would miss it (it did, once). Identity
includes the fence's language tag, so relabelling a q block as J fails too;
eval-answer quotes must be fenced ```q.

Only the plain form is supported: a ``` or ```lang fence at column 0. Any
other fence-like line (indented, inside a blockquote, ~~~, or four backticks)
FAILS rather than being skipped, so a snippet cannot slip past unchecked.

Known limitation (Codex, 2026-09-26): a lesson README's *tagged* source blocks
are themselves only partly verified — check-lesson-outputs.py checks output
blocks and inline `/ value` claims, not that each ```q block appears in the
lesson's .q file. This check trusts README membership, so it inherits that gap.

An article may opt out with a visible marker, on its own line:
    <!-- snippet-check: skip — <reason> -->
Skips are printed on every run, so an exemption can never go quiet.
LinkedIn/social drafts (NN-linkedin.md, NN-social.md) are not articles.

Pure text — needs no q or J, so it runs on every PR in j-verify.
Usage: check-article-snippets.py [article.md ...]   (default: all articles)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^```([A-Za-z]*)\n(.*?)^```", re.S | re.M)
# any fence-like line that is NOT the plain column-0 form handled above
ODD_FENCE = re.compile(r"^(?:[ \t]+|(?:>[ \t]*)+)?(?:`{3,}|~{3,})|^````", re.M)
PLAIN_FENCE = re.compile(r"^```[A-Za-z]*$", re.M)
SKIP = re.compile(r"^<!-- snippet-check: skip\s*[—-]\s*(.+?)\s*-->$", re.M)


def lesson_blocks():
    blocks = set()
    for readme in sorted(ROOT.glob("lessons/*/README.md")):
        blocks.update((lang, body) for lang, body in FENCE.findall(readme.read_text()))
    return blocks


def eval_answers():
    return [p.read_text().splitlines() for p in sorted(ROOT.glob("eval/runs/*.q"))]


def is_run_of_lines(block, files):
    want = block.rstrip("\n").splitlines()
    if not want:
        return False
    n = len(want)
    return any(lines[i:i + n] == want for lines in files for i in range(len(lines) - n + 1))


def articles(argv):
    if argv:
        return [Path(a) for a in argv]
    return [p for p in sorted(ROOT.glob("writings/[0-9][0-9]-*.md"))
            if not re.search(r"-(linkedin|social)\.md$", p.name)]


def main(argv):
    lessons, answers = lesson_blocks(), eval_answers()
    failures, checked = 0, 0
    for art in articles(argv):
        text = art.read_text()
        rel = art.relative_to(ROOT) if art.is_absolute() else art
        skip = SKIP.search(text)
        blocks = FENCE.findall(text)
        odd = [m for m in ODD_FENCE.finditer(text) if not PLAIN_FENCE.match(text, m.start())
               or text[m.start():].startswith("````")]
        if skip:
            print(f"-- {rel}  SKIPPED ({len(blocks)} block(s) unchecked): {skip.group(1)}")
            continue
        bad = [f"   {rel}:{text[:m.start()].count(chr(10)) + 1}: UNSUPPORTED FENCE FORM "
               f"(indented, blockquoted, ~~~ or ````) — use a column-0 ``` fence" for m in odd]
        for m in FENCE.finditer(text):
            lang, block = m.group(1), m.group(2)
            if (lang, block) in lessons or (lang == "q" and is_run_of_lines(block, answers)):
                continue
            line = text[:m.start()].count("\n") + 1
            first = block.splitlines()[0] if block.strip() else "(empty)"
            bad.append(f"   {rel}:{line}: NOT FROM A RUNNING FILE — first line {first!r}")
        checked += len(blocks)
        print(f"-- {rel}  ({len(blocks)} block(s))")
        for b in bad:
            print(b)
        failures += len(bad)
    if failures:
        print(f"article snippets: {failures} problem(s) — a block not copied from running code, or an unsupported fence")
        return 1
    print(f"article snippets: OK — {checked} block(s) identical to running lesson/eval code")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
