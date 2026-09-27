<!--
Social posts for article 3 (RELEASE-CHECKLIST: "X + Bluesky: short thread — hook + one snippet +
canonical link"; "Mastodon: single-post summary + link"; Nostr, same shape as Mastodon).
DRAFT: <URL> is article 3's canonical URL and <URL2> article 2's, both unknown until nandan.me
publishes them.
Snippet provenance: `show sums 1 2 3 4 5` is byte-identical in eval/runs/02-running-total.A.q and
.B.q (line 1), the committed answers the eval scored.
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Article 2 gets only the optional last post of the X and Bluesky threads, not a thread of its own.
Image: attach writings/figures/03/linkedin-card.png to the first post on each network, with the
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

Article 3 of 6 ↓ #kdb

**2/4**

15 paired q tasks, with and without the plugin.

Correct: 14/15 vs 14/15
Idiomatic: 73/75 vs 74/75
Discordant pairs: 1. A sign test needs 6.

Five pairs were identical code. Both arms wrote:

show sums 1 2 3 4 5

**3/4**

The plugin worked: it fired reliably and wrote good q. So did the model without it.

Tasks that are easy to verify are easy to solve. Mine left no headroom.

Measure the baseline's failure rate before you design the comparison.

**4/4**

Also: the control that made the null trustworthy, and a finding I retracted after one more page of KX's docs.

<URL>

Not affiliated with KX.

**5/5 (optional, for article 2)**

Also out: article 2, on reading the KDB-X licence before writing a line of CI.

<URL2>

# Bluesky (thread)

**1/4**

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring.

I ran a controlled eval on KX's official q plugin for Claude Code. The result was a null, and the reason is the finding.

Article 3 of 6 ↓

#kdb

**2/4**

15 paired q tasks, with and without the plugin.

Correct: 14/15 vs 14/15
Idiomatic: 73/75 vs 74/75
Discordant pairs: 1. A sign test needs 6.

Five pairs were identical code. Both arms wrote:

show sums 1 2 3 4 5

**3/4**

The plugin worked: it fired reliably and wrote good q. So did the model without it.

Tasks that are easy to verify are easy to solve. Mine left no headroom.

Measure the baseline's failure rate before you design the comparison.

**4/4**

Also: the control that made the null trustworthy, and a finding I retracted after one more page of KX's docs.

<URL>

Not affiliated with KX.

**5/5 (optional, for article 2)**

Also out: article 2, on reading the KDB-X licence before writing a line of CI.

<URL2>

# Mastodon (single post)

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring.

I ran a controlled eval of KX's official q plugin for Claude Code: 15 paired q tasks. Correct 14/15 in both arms, five pairs byte-identical, one discordant pair where a sign test needs six. The plugin worked; my tasks had no headroom. Check the baseline's failure rate first.

Article 3 of 6: <URL>

#LLM #kdb #ClaudeCode #Evaluation

# Nostr (single note)

When you compare a coding plugin against a frontier model, your task set is part of what you are measuring, and it can settle the result before the plugin gets a chance to.

I ran a controlled eval of KX's official q plugin for Claude Code: 15 paired q tasks, with and without the plugin. Both arms were correct on 14 of 15, five pairs came back as identical code, and there was one discordant pair where a sign test needs six. The plugin fired reliably and wrote good q. So did the model without it. My tasks were easy to verify, which made them easy to solve.

The lesson: measure the baseline's failure rate before you design the comparison.

Article 3 of 6: <URL>
Repo: https://github.com/nandanito/array-thinking-to-q

#LLM #kdb #programming
