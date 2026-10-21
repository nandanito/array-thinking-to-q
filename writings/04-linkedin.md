<!--
LinkedIn post for article 4, "Unlearn the loop" (RELEASE-CHECKLIST: "2–3 paragraph professional framing").
The article is live at https://nandan.me/writing/unlearn-the-loop/ (published 2026-10-21).
Slot: 2026-10-21 08:30 CEST, as the as-of join post had (2026-10-16).
Image: attach writings/figures/04/linkedin-card.png (1200×627; it is figure 1 rendered with
`rsvg-convert -w 1200`, and the committed PNG is byte-identical to that render, checked 2026-10-17).
Alt text below.
Tag: type "@KX" and pick the company page linkedin.com/company/kx-systems. J is named in plain
text; no account is tagged for it.
Picks up from the as-of join post (2026-10-16) in paragraph 2, but the hook (q will let you write
the loop, and it works; that is why q cannot teach you to stop) sits inside the ~210-character
preview. Jargon translated for readers of neither language: "a counter and a loop" rather than
do[], "the idiom, sum" rather than sum x, the fork becomes "a mean written with no data in it",
the adverb becomes "something you attach to a function", rank becomes "depth as a number you
choose", and "3-period moving average" stays in English.
Every claim is from the article: the loop that works and reads like ordinary q; J allows loops but
makes them feel foreign (five lines of machinery where the idiom is two characters); the three
ideas; the fork does not parse (loud, cannot ship); the moving-average windows (four results in J,
six in q, two positions early, no error); the eval's three loop-transliteration tasks, both arms
solved them, and the article's own caveat that the eval was underpowered; written for people who
have never read q or J; every snippet copied from a lesson that runs in CI.
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

Last week I took q's as-of join apart and found the part nothing checks: a sort. This article is
about a quieter gap. q, the language of @KX's kdb+, has loops, counters and add-and-assign, so every
reflex you bring from Python or Java has somewhere to land, and the answers come out right. Nothing
fails, so nothing ever pushes you toward the idiom, sum. J, the array language the curriculum visits
first, allows loops too. The difference is what writing one costs you: you leave J's ordinary
notation for five lines of visibly foreign machinery, where the idiom is two characters. That
feeling of having wandered off is the whole case for a short detour through J. Three ideas come
back from it: iteration is something you attach to a function (a moving sum is a running total
with a width), a function can be written with no data in it, and depth is a number you choose.

Two of those ideas break on the way back, and the second is the dangerous one. A mean written J's
way, with no data in it, does not parse in q at all: loud, and it cannot ship. The 3-period moving
average ships. Of six numbers, J returns four averages, complete windows only; q returns six,
ramping up through the partial windows at the start. Neither is wrong, both are called the same
thing, and if you read q's first value as the first full window you are two positions early, with
no error. The article also looks at what my eval of KX's q plugin says about whether the shift
takes (both arms fixed all three loop-transliteration tasks, and why that carries little weight).
It is written for people who have never read q or J, and every snippet is copied from a lesson
that runs in CI.

https://nandan.me/writing/unlearn-the-loop/

Independent work; not affiliated with KX or Jsoftware.

#kdb #ArrayProgramming #SoftwareEngineering #FunctionalProgramming
