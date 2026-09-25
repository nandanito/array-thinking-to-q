<!--
LinkedIn post for article 1 (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
DRAFT — do not post until article 1 is published at its canonical URL.
Canonical section is nandan.me/writing/ (singular). The slug below is a placeholder:
replace it with the real published URL before posting.
Image: attach writings/figures/01/linkedin-card.png (figure 1 at 1200x627).
-->

I've started a small learning-in-public project: a short curriculum that takes an imperative
programmer through the array-programming paradigm shift and lands them in q/kdb+, with a brief
stop in J on the way. The premise is that syntax isn't the hard part of array languages; unlearning
the loop is, and a language that lets you stay imperative won't make you stop. So J serves as a
short laboratory where the shift is unavoidable, and q is the destination. The repo has one rule
it won't bend on: every code example runs under `make verify`, and printed outputs are captured
from the real interpreters rather than typed by hand.

What surprised me is that code verification catches the smaller share of the problem. Every
serious defect so far got past a green build, because what was wrong was a claim, not a failing
line of code: a CI check that went green
without checking anything, contributor instructions that had quietly gone stale, and one
published evaluation finding I had to retract, even though my own notes had recorded the
correction days before. The fixes were procedural: re-read the governing documents at every
milestone, and make the evaluation's key numbers recompute from committed artifacts so the
build fails if they drift.

The first article covers the project, the rules it runs under, and what learning in public
costs once you commit to publishing null results and retractions with the same care as
successes. It's the first of six, and each one publishes only once the work it describes
passes verification.

https://nandan.me/writing/array-thinking-learning-in-public/

Not affiliated with KX Systems or Jsoftware; "q", "kdb+", "KDB-X" and "J" are used nominatively.
