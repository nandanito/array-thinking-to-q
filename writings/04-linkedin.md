<!--
LinkedIn post for article 4, "Unlearn the loop" (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
The article is live at https://nandan.me/writing/unlearn-the-loop/ (published 2026-10-21).
Slot: 2026-10-21 08:30 CEST, as the as-of join post had (2026-10-16).
Image: attach writings/figures/04/linkedin-card.png (1200×627; it is figure 1 rendered with
`rsvg-convert -w 1200`, and the committed PNG is byte-identical to that render, checked 2026-10-17).
Alt text below.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems. J is named in plain
text; no account is tagged for it.
Rewritten 2026-10-21 for a reader who skims: short paragraphs, one idea each, and no word the post
does not explain. The hook (q will let you write the loop, and it works; that is why q cannot
teach you to stop) sits inside the ~210-character preview. Picks up from the as-of join post
(2026-10-16) in one sentence at the top of paragraph 2. The three ideas the detour sends back are
counted, not named (the article names them); "the idiom" became "the one-word version, sum" and
"the array version"; the fork became "a mean written J's way, with no data mentioned"; the eval's
"both arms" became "with and without the plugin".
Every claim is from the article: the loop that works and reads like ordinary q; J allows loops but
makes them feel foreign (five lines of visibly foreign machinery where the alternative is two
characters); three ideas come back and two break; the fork does not parse and cannot ship; the
moving-average windows (four results in J, six in q, two positions early, no error); the eval's
three loop-transliteration tasks, both conditions solved all three, and the article's own caveat
that the eval was underpowered; written for people who have never read q or J; every snippet
copied from a lesson that runs in CI.
No speed or performance wording (Clause 9 caution, same as the article).

Alt text:
Two panels, both summing 1 2 3 4 5 with an explicit loop and printing 15. Left, J: a five-line
explicit definition with its own assignment form and a lone closing parenthesis; the idiom is +/.
Right, q: one ordinary line, do[count x; r+:x i; i+:1]; the idiom is sum. Headline: neither
language forbids the loop, only one makes it feel foreign.
-->

Here is a perfectly good q program. It sums a list with a counter and a loop, and it prints 15. It
will still be correct next year, in production. That is the problem, and it is what article 4 of my
array-thinking series is about.

Last week's article took q's as-of join apart. This one is about a quieter gap. q, the language of
@KX's kdb+, has loops, counters and add-and-assign. Every reflex you bring from Python or Java has
somewhere to land, and the answers come out right. Nothing fails, so nothing ever nudges you toward
the one-word version, sum.

J, the array language the series visits before q, allows loops too. The difference is what a loop
costs you there: you leave J's ordinary notation for five lines of visibly foreign machinery, where
the array version is two characters. That feeling of having wandered off is the whole case for a
short detour through J before q.

The detour sends three habits back with you, and two of them break on the way home. One breaks
loudly: a mean written J's way, with no data mentioned, does not even parse in q, so it can never
ship. One breaks silently: a 3-period moving average of six numbers gives four results in J,
complete windows only, and six in q, which ramps up through partial windows at the start. Both are
right, both are called the same thing, and if you read q's first value as a full window you are two
positions early, with no error.

The article also asks whether the shift actually takes, using my earlier eval of KX's q plugin:
with and without the plugin, all three loop-to-array tasks were solved, and the article explains
why that carries little weight. It is written for people who have never read q or J, and every
snippet is copied from a lesson that runs in CI.

https://nandan.me/writing/unlearn-the-loop/

Independent work; not affiliated with KX or Jsoftware.

#kdb #ArrayProgramming #SoftwareEngineering #FunctionalProgramming
