<!--
LinkedIn post for article 2, the eval (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
DRAFT: the canonical URL is not known until nandan.me publishes; <URL> is a placeholder.
Image: attach writings/figures/02/linkedin-card.png.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems.
Every number is from the article / eval/verdict.md: 14/15 correctness in both arms, 73/75 vs 74/75
idiomaticity, one discordant pair against the six a two-sided exact sign test needs, five
byte-identical pairs, plugin loaded in 14 of 15 Part B runs.
Deliberately left out: the 2.8x output-token ratio. It is in the article with its context; stripped
of that context in a post it reads as a knock on the plugin, and the post's claim is about the task
set, not the plugin.
-->

When you compare a coding plugin against a frontier model, the task set is part of what you are
measuring, and it can settle the result before the plugin gets a chance to.

I ran a controlled evaluation of @KX's official q plugin for Claude Code: fifteen paired q tasks
with and without the plugin, correctness checked by exact output diff, idiomaticity scored on a
five-item binary checklist, and a sign test fixed before any data existed. The plugin did its job:
it activated reliably and wrote good q. So did the model without it. Both conditions were correct
on 14 of 15 tasks, five pairs came back as byte-for-byte identical code, and there was one
discordant pair where the test needs at least six. I kept verification simple by choosing simple
tasks, and they left no room for any plugin to show a difference.

So the finding is not that the plugin does not help. It is that my instrument could not have
detected a small effect and detected no large one. The article covers the control that made the
null trustworthy, a finding I retracted after reading one more page of KX's documentation, and the
check I should have run first: measure the baseline's failure rate before designing the
comparison. It tests the plugin at a pinned commit; KX has since added a documentation-search
server that this eval did not cover.

<URL>

Independent work; not affiliated with KX.

#LLMEvaluation #ClaudeCode #kdb #SoftwareEngineering
