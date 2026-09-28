<!--
Social posts for article 2 (the eval) (RELEASE-CHECKLIST: X + Bluesky + Mastodon + Nostr). Each is a
single post: the personal X account has Premium (long posts), and Bluesky's 300-character cap is met
by one short post instead of a thread.
Each picks up from the article 1 posts (2026-09-25), but the hook (KX already ships a q plugin, so I
measured it) comes first. Plain language for non-q readers: no "arms", "discordant pair" or "headroom"
(reader test, 2026-09-28). Every post that has room carries the pinned-commit caveat.
Snippet provenance: `show sums 1 2 3 4 5` is byte-identical in eval/runs/02-running-total.A.q and
.B.q (line 1), the committed answers the eval scored; the article introduces it as a running total.
Tagging: KX is @kxsystems on X. KX has no Bluesky, Mastodon or Nostr account (checked
2026-09-25), so those posts name KX in plain text.
Image: attach writings/figures/02/linkedin-card.png to each post, with the alt text below.
Lengths checked 2026-09-28: X long post (Premium, 25,000 limit; about the first 280 characters show
before "Show more", so the opening carries the hook); Bluesky within 300 counting the full URL;
Mastodon within 500 with the link counted as 23.

Alt text (all networks):
Fifteen tiles, one per paired task. Five are byte-for-byte identical q in both conditions; eight
differ in code but score the same; one is a shared miss; one is the only discordant pair. Correct
14/15 in both conditions; idiomatic 73/75 without the plugin, 74/75 with it.
-->

# X (single long post, tag @kxsystems)

I had planned to write a Claude Code skill for q, as part of the array-thinking series I started last week. Then I found that @kxsystems already ships one, as an official plugin. So instead of writing a second, I measured theirs.

Fifteen q tasks, each run with and without the plugin. Correctness checked by exact output diff, idiomatic style scored on a five-item checklist, and the decision rule written down before any data existed.

Correct: 14/15 without the plugin, 14/15 with it
Idiomatic style: 73/75 without, 74/75 with

Only one task scored differently between the two; you would need at least six, all one way, before calling it a real difference. Five tasks came back as identical code. For a running total, both wrote:

show sums 1 2 3 4 5

The plugin did its job: it activated reliably and wrote good q. So did the model without it. I kept verification simple by choosing simple tasks, and they left no room for any plugin to show a difference. The result says more about my task set than about KX's plugin.

The check I would run first next time: measure how often the baseline fails before designing the comparison.

The article also covers the control that kept the comparison clean, and a finding I got wrong and retracted after reading one more page of KX's documentation. It tests the plugin at a pinned commit; KX has since added a documentation-search server that this eval did not cover.

Article 2 of 5: https://nandan.me/writing/no-headroom-kx-q-plugin/

Independent work; not affiliated with KX.

#kdb #AIEvals

# Bluesky (single post)

I measured KX's official q plugin for Claude Code: 15 tasks, with and without it. Both got 14 of 15 right. My tasks were too easy to tell them apart, so check your baseline's failure rate first. (Part 2 of my array-thinking series.)

https://nandan.me/writing/no-headroom-kx-q-plugin/

# Mastodon (single post)

I had planned a Claude Code skill for q in my array-thinking series, then found KX already ships an official plugin, so I measured theirs. 15 q tasks with and without it: both got 14 of 15 right, and five answers were identical code. My tasks were too easy to tell them apart. Check how often your baseline fails first.

Article 2 of 5: https://nandan.me/writing/no-headroom-kx-q-plugin/

#kdb #ClaudeCode #AI #ArrayProgramming

# Nostr (single note)

I had planned to write a Claude Code skill for q, as part of the array-thinking series I started last week. Then I found that KX already ships one as an official plugin, so instead of writing a second, I measured theirs.

15 q tasks, each run with and without the plugin. Both got 14 of 15 right, five tasks came back as identical code, and only one task scored differently between the two, where you would need at least six before calling it a real difference. The plugin activated reliably and wrote good q. So did the model without it. I picked simple tasks to keep verification simple, and they were too easy to tell the two apart.

What I would do first next time: measure how often the baseline fails before designing the comparison. The eval tests the plugin at a pinned commit; KX has since added a documentation-search server that it did not cover.

Article 2 of 5: https://nandan.me/writing/no-headroom-kx-q-plugin/
Repo: https://github.com/nandanito/array-thinking-to-q

#AI #kdb #programming
