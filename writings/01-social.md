<!--
Social posts for article 1 (RELEASE-CHECKLIST: "X + Bluesky: short thread — hook + one snippet +
canonical link"; "Mastodon: single-post summary + link"; Nostr added, same shape as Mastodon).
DRAFT — do not post until article 1 is published at its canonical URL.
The slug in the links is a placeholder: replace it with the real published URL before posting.
Snippet provenance: `2 * til 5  / 0 2 4 6 8` is lesson 01's line 53, verified by `make verify`.
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Image: attach writings/figures/01/linkedin-card.png to the first post on each network, with the
alt text below.
Lengths are checked against each network's limit (X 280 chars, Bluesky 300, Mastodon 500);
links count as 23 characters on X and Mastodon.

Alt text (all networks):
Two panels computing the same result. Left, a Python loop doubles 0 1 2 3 4 in five numbered
steps, one element at a time. Right, the q expression 2 * til 5 applies one operation to the whole
list and produces 0 2 4 6 8.
-->

# X (thread, tag @kxsystems)

**1/5**

Array languages ask one thing of an experienced programmer: stop writing the loop.

I've been working through that shift and turning it into a short, fully executable curriculum: a brief laboratory in J, then q/kdb+ as the destination.

Article 1 of 6 ↓

**2/5**

In Python you write the loop, the index and the accumulator. In q:

2 * til 5                  / 0 2 4 6 8

No index, no loop. The iteration lives in the operator, not in your code.

**3/5**

One constraint runs the project: every example executes. Outputs are captured from the real interpreters and re-checked by make verify; the q suite runs nightly in CI.

**4/5**

The useful finding: every serious defect so far passed a green build. A CI check that verified nothing, stale instructions, an evaluation claim I retracted. Verification covers code. Claims need their own discipline.

**5/5**

The article: https://nandan.me/writing/array-thinking-learning-in-public/

The repo: https://github.com/nandanito/array-thinking-to-q

q runs on @kxsystems' KDB-X Community Edition. Not affiliated.

#kdb #qlang

# Bluesky (thread)

**1/4**

Array languages ask one thing of an experienced programmer: stop writing the loop.

I've been working through that shift and turning it into a short, fully executable curriculum: a brief laboratory in J, then q/kdb+ as the destination. Article 1 of 6 ↓

**2/4**

In Python you write the loop, the index and the accumulator. In q:

2 * til 5                  / 0 2 4 6 8

No index, no loop. The iteration lives in the operator, not in your code.

**3/4**

Every example in the project executes and is re-checked by make verify; q runs nightly in CI.

The useful finding: every serious defect so far passed a green build. Verification covers code. Claims need their own discipline.

**4/4**

The article: https://nandan.me/writing/array-thinking-learning-in-public/

The repo: https://github.com/nandanito/array-thinking-to-q

q runs on KX's KDB-X Community Edition. Not affiliated.

# Mastodon (single post)

Array languages ask one thing of an experienced programmer: stop writing the loop. I've been working through that shift and turning it into a short, fully executable curriculum: a brief laboratory in J, then q/kdb+ (KX) as the destination.

Every example runs under make verify. The more useful finding: every serious defect so far passed a green build, because what was wrong was a claim, not code.

Article 1 of 6: https://nandan.me/writing/array-thinking-learning-in-public/

#ArrayProgramming #kdb #qlang #APL

# Nostr (single note)

Array languages ask one thing of an experienced programmer: stop writing the loop.

I've been working through that shift and turning it into a short, fully executable curriculum: a brief laboratory in J, then q/kdb+ from KX as the destination. Every example runs under make verify, and the q suite runs nightly in CI.

The more useful finding: every serious defect so far passed a green build, because what was wrong was a claim, not code. Verification covers code; claims need their own discipline.

Article 1 of 6: https://nandan.me/writing/array-thinking-learning-in-public/
Repo: https://github.com/nandanito/array-thinking-to-q

#ArrayProgramming #kdb #qlang
