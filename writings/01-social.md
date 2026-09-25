<!--
Social posts for article 1 (RELEASE-CHECKLIST: "X + Bluesky: short thread — hook + one snippet +
canonical link"; "Mastodon: single-post summary + link"; Nostr added, same shape as Mastodon).
Article 1 is live; ready to post.
Canonical URL: https://nandan.me/writing/array-thinking-all-the-way-to-q/ (published 2026-09-25).
Snippet provenance: `2 * til 5` and its output `0 2 4 6 8` are lesson 01's line 53, verified by
`make verify` (the lesson's alignment spaces are dropped; they read as noise in a social font).
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

**1/4**

Array languages ask one thing of an experienced programmer: stop writing the loop.

Not the syntax, but the reflex of stepping through data one element at a time with an index and an accumulator.

Article 1 of 6 ↓ #kdb #ArrayProgramming

**2/4**

In Python you write the loop, the index and the accumulator. In q:

2 * til 5
→ 0 2 4 6 8

The iteration has not disappeared. It has moved into the operator.

**3/4**

Once that clicks, the same move carries from a list to a table, a query and a time-series join.

The code starts describing the data instead of the steps.

**4/4**

A short curriculum: a brief laboratory in J, then q/kdb+ as the destination. Every example runs against the real interpreters.

https://nandan.me/writing/array-thinking-all-the-way-to-q/

q runs on @kxsystems' KDB-X Community Edition. Not affiliated.

# Bluesky (thread)

**1/4**

Array languages ask one thing of an experienced programmer: stop writing the loop.

Not the syntax, but the reflex of stepping through data one element at a time with an index and an accumulator.

Article 1 of 6 ↓

#kdb #ArrayProgramming

**2/4**

In Python you write the loop, the index and the accumulator. In q:

2 * til 5
→ 0 2 4 6 8

The iteration has not disappeared. It has moved into the operator.

**3/4**

Once that clicks, the same move carries from a list to a table, a query and a time-series join.

The code starts describing the data instead of the steps.

**4/4**

A short curriculum: a brief laboratory in J, then q/kdb+ as the destination. Every example runs against the real interpreters.

https://nandan.me/writing/array-thinking-all-the-way-to-q/

q runs on KX's KDB-X Community Edition. Not affiliated.

# Mastodon (single post)

Array languages ask one thing of an experienced programmer: stop writing the loop.

In q, 2 * til 5 gives 0 2 4 6 8. No index, no accumulator: the iteration has moved into the operator. The same move carries from a list to a table, a query and a time-series join.

A short curriculum: a brief laboratory in J, then q/kdb+ (KX) as the destination. Every example runs against the real interpreters.

Article 1 of 6: https://nandan.me/writing/array-thinking-all-the-way-to-q/

#ArrayProgramming #kdb #APL #FunctionalProgramming

# Nostr (single note)

Array languages ask one thing of an experienced programmer: stop writing the loop. Not the syntax, but the reflex of stepping through data one element at a time with an index and an accumulator.

In q, 2 * til 5 gives 0 2 4 6 8. No index, no accumulator: the iteration has moved into the operator. Once that clicks, the same move carries from a list to a table, a query and a time-series join, and the code starts describing the data instead of the steps.

A short curriculum: a brief laboratory in J, then q/kdb+ from KX as the destination. Every example runs against the real interpreters.

Article 1 of 6: https://nandan.me/writing/array-thinking-all-the-way-to-q/
Repo: https://github.com/nandanito/array-thinking-to-q

#ArrayProgramming #kdb #programming
