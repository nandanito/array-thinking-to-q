<!--
LinkedIn post for article 2, the eval (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
Scheduled: 2026-09-29 08:30 CEST (the article goes live on nandan.me from about 07:15 CEST).
Image: attach writings/figures/02/linkedin-card.png.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
Opens by picking up from the article 1 post (2026-09-25) but puts the hook (KX already ships a q
plugin, so I measured it) inside the ~210-character preview. No article count: the article 1 post
said six and the series is five. Jargon translated for non-q readers (reader test, 2026-09-28).
Every number is from the article / eval/verdict.md: 14/15 correctness in both arms, five
byte-identical pairs, one discordant pair against the six a two-sided exact sign test needs, the
decision rule fixed before any data existed.
Deliberately left out: the 2.8x output-token ratio. It is in the article with its context; stripped
of that context in a post it reads as a knock on the plugin, and the post's claim is about the task
set, not the plugin.
-->

Last week I started a series on array thinking, all the way to q/kdb+. Along the way I had planned
to write a Claude Code skill for q. Then I found that @KX already ships one, as an official plugin,
so I measured theirs instead.

A skill is a short guide the model reads before it answers; this one teaches it to write q the way
q is meant to be written. The setup: fifteen q tasks, each run with and without the plugin,
correctness checked by exact output diff, idiomatic style scored on a five-item checklist, and the
decision rule written down before any data existed.

The plugin did its job: it activated reliably and wrote good q. So did the model without it. Both
were correct on 14 of 15 tasks, five pairs came back as byte-for-byte identical code, and only one
task scored differently between the two, where you would need at least six, all one way, before
calling it a real difference. I had kept verification simple by choosing simple tasks, and they
left no room for any plugin to show a difference. The result says more about my task set than
about KX's plugin, and the check I skipped is the one I would now run first: measure how often the
baseline fails before designing the comparison.

The article also covers the control that kept the comparison clean, and a finding I got wrong and
retracted after reading one more page of KX's documentation. It tests the plugin at a pinned
commit; KX has since added a documentation-search server that this eval did not cover.

https://nandan.me/writing/no-headroom-kx-q-plugin/

Independent work; not affiliated with KX.

#ClaudeCode #AIEvals #kdb #GenerativeAI #ArrayProgramming
