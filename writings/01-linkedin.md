<!--
LinkedIn post for article 1 (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
DRAFT — do not post until article 1 is published at its canonical URL.
Canonical section is nandan.me/writing/ (singular). The slug below is a placeholder:
replace it with the real published URL before posting.
Image: attach writings/figures/01/linkedin-card.png (figure 1 at 1200x627).
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
-->

Array languages ask one thing of an experienced programmer: stop writing the loop. Not the syntax,
which is learnable in an afternoon, but the reflex of stepping through data one element at a time
with an index and an accumulator. I have been working through that shift deliberately, and turning
it into a short curriculum: a brief laboratory in J, where the notation leaves no comfortable place
for a loop, and then q/kdb+ from @KX as the destination, where the same ideas carry real tables,
queries and an as-of join.

The project runs on one constraint: every example executes. Printed outputs are captured from the
real interpreters and re-checked by `make verify`, and the q suite runs nightly in CI against a
licensed KDB-X Community Edition build. The more useful finding came from what that constraint does
not cover. Every serious defect so far passed a green build, because what was wrong was a claim
rather than a line of code: a CI check that verified nothing, contributor instructions that had
drifted out of date, and one evaluation finding I retracted even though the correction was already
in the repository. The remedies were procedural: re-read the governing documents at every
milestone, and have the evaluation's key numbers recompute from committed artifacts so the build
fails if they drift.

The first of six articles sets out the approach, the rules it runs under, and why claims deserve
the same discipline as code. Each article is published only once the work it describes verifies.

https://nandan.me/writing/array-thinking-learning-in-public/

Not affiliated with KX or Jsoftware; "q", "kdb+", "KDB-X" and "J" are used nominatively.
