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
import tempfile
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
Q = os.environ.get("Q", "q")
J = os.environ.get("J", "jconsole")

FENCE = re.compile(r"^```(.*)$")

# A q literal as it appears in captured output: symbol(s), number(s)/vectors with
# an optional type suffix, a boolean vector, or a type code. `,` prefixes a
# one-element list, which q's display uses and the lessons lean on.
Q_LITERAL = r"(?:,?`[\w`]*|-?[\d.]+[a-z]?(?: -?[\d.]+[a-z]?)*|[01]+b|-?\d+h)"
CLAIM = re.compile(rf"^({Q_LITERAL})(?:\s*—.*|\s{{2,}}.*)?$")


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


def fenced_blocks(readme: Path) -> list[tuple[str, int, list[str]]]:
    """Every fenced block, as (language tag, 1-based start line, rstripped lines)."""
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
        blocks.append((tag, start, body))
    return blocks


def output_blocks(readme: Path) -> list[tuple[int, list[str]]]:
    """Every unlabelled fenced block — these are captured OUTPUT."""
    out = []
    for tag, start, body in fenced_blocks(readme):
        if tag:
            continue
        while body and not body[-1]:
            body.pop()
        if body:
            out.append((start, body))
    return out


def inline_claims(readme: Path) -> list[tuple[int, str, str]]:
    """Value claims made in trailing `/ ...` comments inside ```q blocks.

    Lesson 01 is written almost entirely this way (`avg til 5   / 2f`), so
    without this the block check barely covers it. A comment counts as a claim
    only when it OPENS with something shaped like a q literal -- `2f`, `-7h`,
    `00011b`, `` `a`b`c ``, `0 1 3 6 10`, ``,`qty`` -- optionally followed by
    prose after an em-dash or a two-space gap. Prose-only comments ("the
    idiom", "not ascending") assert nothing and are skipped.
    """
    claims = []
    for tag, start, body in fenced_blocks(readme):
        if tag != "q":
            continue
        for offset, line in enumerate(body):
            m = re.search(r"^(.*?)\s/\s(.+)$", line)
            if not m or not m.group(1).strip():
                continue
            c = CLAIM.match(m.group(2).strip())
            if c:
                claims.append((start + offset, m.group(1).strip(), c.group(1).strip()))
    return claims


def find(hay: list[str], needle: list[str], start: int) -> int:
    """First index >= start where needle appears contiguously, else -1."""
    n = len(needle)
    for i in range(start, len(hay) - n + 1):
        if hay[i : i + n] == needle:
            return i
    return -1


def check(lesson: Path) -> tuple[list[str], int, int]:
    readme = lesson / "README.md"
    if not readme.exists():
        return [], 0, 0
    sources = sorted((lesson / "q").glob("*.q")) + sorted((lesson / "j").glob("*.ijs"))
    if not sources:
        return [f"{readme.relative_to(REPO)}: no q/ or j/ sources to verify against"], 0, 0

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

    claims = inline_claims(readme)
    failures += check_claims(lesson, readme, claims)
    return failures, len(output_blocks(readme)), len(claims)


def check_claims(
    lesson: Path, readme: Path, claims: list[tuple[int, str, str]]
) -> list[str]:
    """Evaluate each claimed expression and compare to what it is annotated with.

    Mere membership in the capture is too weak: swapping lesson 02's ``type d``
    annotation from `99h` to `98h` passes a membership test, because `98h` is a
    real value elsewhere in that same lesson. So each expression is re-evaluated
    instead -- appended to the lesson's own (verify-clean) q source, which has
    already built the state the narrative refers to (`d`, `t`, `kt`, `r`, `w`).
    Only value-bearing lines are appended, so the deliberate error demos, whose
    comments are prose, are never executed here.
    """
    qsrc = sorted((lesson / "q").glob("*.q"))
    if not claims or not qsrc:
        return []
    prog = [qsrc[0].read_text()]
    for i, (_, code, _) in enumerate(claims):
        prog.append(f'-1"@@{i}@@";')
        prog.append(f"show({code.rstrip(';')});")

    with tempfile.TemporaryDirectory() as tmp:  # never inside the repo
        gen = Path(tmp) / "claims.q"
        gen.write_text("\n".join(prog) + "\n")
        proc = subprocess.run(
            [Q, str(gen), "-q"], stdin=subprocess.DEVNULL, capture_output=True, text=True
        )
    if proc.returncode != 0:
        return [
            f"{readme.relative_to(REPO)}: could not evaluate inline claims "
            f"(q exited {proc.returncode}):\n{proc.stderr.strip()}"
        ]

    parts = re.split(r"@@(\d+)@@\n", proc.stdout)
    actual = {int(parts[i]): parts[i + 1].strip() for i in range(1, len(parts), 2)}
    out = []
    for i, (line_no, code, claim) in enumerate(claims):
        got = actual.get(i)
        if got != claim:
            out.append(
                f"{readme.relative_to(REPO)}:{line_no}: WRONG CLAIM — "
                f"`{code}` is annotated {claim!r} but evaluates to {got!r}."
            )
    return out


def main() -> int:
    args = sys.argv[1:]
    lessons = (
        [Path(a).resolve() for a in args]
        if args
        else sorted(p for p in (REPO / "lessons").iterdir() if p.is_dir())
    )
    failures, checked, tot_b, tot_c = [], 0, 0, 0
    for lesson in lessons:
        if not (lesson / "README.md").exists():
            continue
        checked += 1
        f, nb, nc = check(lesson)
        failures += f
        tot_b, tot_c = tot_b + nb, tot_c + nc
        print(f"-- {lesson.relative_to(REPO)}  ({nb} block(s), {nc} inline claim(s))")
    for f in failures:
        print(f"   {f}")
    if failures:
        print(f"prose outputs: {len(failures)} MISMATCH(es) across {checked} lesson(s)")
        return 1
    print(
        f"prose outputs: OK — {tot_b} block(s) and {tot_c} inline claim(s) "
        f"across {checked} lesson(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
