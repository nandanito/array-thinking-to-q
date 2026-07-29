#!/usr/bin/env python3
"""Check that every output block pasted into a lesson README is real.

`make verify` proves each lesson's q/ijs FILES run. It says nothing about
whether the outputs pasted into the narrative are the ones those files
actually produce — and the repo's whole credibility rests on that claim
(CLAUDE.md rule 3: outputs are captured from the real tools, never typed).

So: run each lesson's sources fresh, then require every *unlabelled* fenced
block in its README to appear as a contiguous run of lines in that capture,
at a position at or after the previous block's. The monotonicity half matters
as much as the membership half — it catches outputs that are individually
genuine but shown in an order the file never executed.

A fenced block with a language tag (```q, ```j, ```python) is SOURCE, not
output, and is not checked here. That is also how the two blocks CLAUDE.md
exempts stay exempt without a special case: the illustrative Python snippet
and the deliberate q parse-error REPL transcript are both tagged.

Usage: check-lesson-outputs.py [lesson_dir ...]     (default: all lessons)
Env:   Q, J — interpreter paths (same knobs the Makefile uses).
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
Q = os.environ.get("Q", "q")
J = os.environ.get("J", "jconsole")

FENCE = re.compile(r"^```(.*)$")


def capture(path: Path) -> list[str]:
    """Run one source file the way `make verify` runs it; return stdout lines.

    Exit code is not sufficient on its own: q can report an error on stderr and
    still exit 0, which would leave a lesson that visibly failed producing
    stdout that still matches its pasted blocks. `verify-eval` already guards
    this exact case ("error masked by exit 0"), so this gate does too.
    """
    if path.suffix == ".q":
        cmd, stdin = [Q, str(path), "-q"], subprocess.DEVNULL
        proc = subprocess.run(cmd, stdin=stdin, capture_output=True, text=True)
    elif path.suffix == ".ijs":
        with path.open() as fh:
            proc = subprocess.run([J], stdin=fh, capture_output=True, text=True)
    else:
        raise ValueError(f"unknown source type: {path}")
    if proc.returncode != 0:
        sys.exit(f"FATAL: {path} exited {proc.returncode}\n{proc.stderr}")
    if proc.stderr.strip():
        sys.exit(
            f"FATAL: {path} exited 0 but wrote to stderr (error masked by exit 0):\n"
            f"{proc.stderr}"
        )
    return [ln.rstrip() for ln in proc.stdout.splitlines()]


def output_blocks(readme: Path) -> list[tuple[int, list[str]]]:
    """Every unlabelled fenced block, as (1-based start line, rstripped lines)."""
    blocks, lines = [], readme.read_text().splitlines()
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        tag, start, body = m.group(1).strip(), i + 1, []
        i += 1
        while i < len(lines) and not FENCE.match(lines[i]):
            body.append(lines[i].rstrip())
            i += 1
        i += 1  # closing fence
        if not tag:
            while body and not body[-1]:
                body.pop()
            if body:
                blocks.append((start, body))
    return blocks


def find(hay: list[str], needle: list[str], start: int) -> int:
    """First index >= start where needle appears contiguously, else -1."""
    n = len(needle)
    for i in range(start, len(hay) - n + 1):
        if hay[i : i + n] == needle:
            return i
    return -1


def check(lesson: Path) -> list[str]:
    readme = lesson / "README.md"
    if not readme.exists():
        return []
    sources = sorted((lesson / "q").glob("*.q")) + sorted((lesson / "j").glob("*.ijs"))
    if not sources:
        return [f"{readme.relative_to(REPO)}: no q/ or j/ sources to verify against"]

    hay: list[str] = []
    for src in sources:
        hay += capture(src)

    failures, cursor = [], 0
    for line_no, block in output_blocks(readme):
        where = f"{readme.relative_to(REPO)}:{line_no}"
        at = find(hay, block, cursor)
        if at >= 0:
            cursor = at + len(block)
            continue
        earlier = find(hay, block, 0)
        if earlier >= 0:
            failures.append(
                f"{where}: OUT OF ORDER — this output exists, but only at capture "
                f"line {earlier + 1}, before a block already matched at {cursor}."
            )
        else:
            failures.append(
                f"{where}: NOT IN CAPTURE — first line {block[0]!r} "
                f"({len(block)} line(s)); no run of the real output matches."
            )
    return failures


def main() -> int:
    args = sys.argv[1:]
    lessons = (
        [Path(a).resolve() for a in args]
        if args
        else sorted(p for p in (REPO / "lessons").iterdir() if p.is_dir())
    )
    failures, checked = [], 0
    for lesson in lessons:
        if not (lesson / "README.md").exists():
            continue
        checked += 1
        failures += check(lesson)
        print(f"-- {lesson.relative_to(REPO)}")
    for f in failures:
        print(f"   {f}")
    if failures:
        print(f"prose outputs: {len(failures)} MISMATCH(es) across {checked} lesson(s)")
        return 1
    print(f"prose outputs: OK ({checked} lesson(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
