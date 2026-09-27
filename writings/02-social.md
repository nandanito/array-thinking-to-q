<!--
Social posts for article 2 (the eval) (RELEASE-CHECKLIST: "X + Bluesky: short thread — hook + one snippet +
canonical link"; "Mastodon: single-post summary + link"; Nostr, same shape as Mastodon).
DRAFT: <URL> is the article's canonical URL, unknown until nandan.me publishes it.
Snippet provenance: `show sums 1 2 3 4 5` is byte-identical in eval/runs/02-running-total.A.q and
.B.q (line 1), the committed answers the eval scored.
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Image: attach writings/figures/02/linkedin-card.png to the first post on each network, with the
alt text below.
Lengths are checked against each network's limit (X 280 chars, Bluesky 300, Mastodon 500);
links count as 23 characters on X and Mastodon.

Alt text (all networks):
Fifteen tiles, one per paired task. Five are byte-for-byte identical q in both conditions; eight
differ in code but score the same; one is a shared miss; one is the only discordant pair. Correct
14/15 in both conditions; idiomatic 73/75 without the plugin, 74/75 with it.
-->

# X (thread, tag @kxsystems)

**1/4**

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring.

I ran a controlled eval on @kxsystems' official q plugin for Claude Code. The result was a null, and the reason is the finding.

Article 2 of 5 ↓ #kdb

**2/4**

15 paired q tasks, with and without the plugin.

Correct: 14/15 vs 14/15
Idiomatic: 73/75 vs 74/75
Discordant pairs: 1. A sign test needs 6.

Five pairs were identical code. Both arms wrote:

show sums 1 2 3 4 5

A running total, no loop.

**3/4**

The plugin worked: it fired reliably and wrote good q. So did the model without it.

I picked simple tasks to keep verification simple. They left no headroom.

Measure the baseline's failure rate before you design the comparison.

**4/4**

Also: the control that made the null trustworthy, and a finding I retracted after one more page of KX's docs.

<URL>

Not affiliated with KX.

# Bluesky (thread)

**1/4**

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring.

I ran a controlled eval on KX's official q plugin for Claude Code. The result was a null, and the reason is the finding.

Article 2 of 5 ↓

#kdb

**2/4**

15 paired q tasks, with and without the plugin.

Correct: 14/15 vs 14/15
Idiomatic: 73/75 vs 74/75
Discordant pairs: 1. A sign test needs 6.

Five pairs were identical code. Both arms wrote:

show sums 1 2 3 4 5

A running total, no loop.

**3/4**

The plugin worked: it fired reliably and wrote good q. So did the model without it.

I picked simple tasks to keep verification simple. They left no headroom.

Measure the baseline's failure rate before you design the comparison.

**4/4**

Also: the control that made the null trustworthy, and a finding I retracted after one more page of KX's docs.

<URL>

Not affiliated with KX.

# Mastodon (single post)

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring.

I ran a controlled eval of KX's official q plugin for Claude Code: 15 paired q tasks. Correct 14/15 in both arms, five pairs byte-identical, one discordant pair where a sign test needs six. The plugin worked; my tasks had no headroom. Check the baseline's failure rate first.

Article 2 of 5: <URL>

#LLM #kdb #ClaudeCode #Evaluation

# Nostr (single note)

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring, and it can settle the result before the plugin gets a chance to.

I ran a controlled eval of KX's official q plugin for Claude Code: 15 paired q tasks, with and without the plugin. Both arms were correct on 14 of 15, five pairs came back as identical code, and there was one discordant pair where a sign test needs six. The plugin fired reliably and wrote good q. So did the model without it. I picked simple tasks to keep verification simple, and they left no headroom.

The lesson: measure the baseline's failure rate before you design the comparison.

Article 2 of 5: <URL>
Repo: https://github.com/nandanito/array-thinking-to-q

#LLM #kdb #programming
