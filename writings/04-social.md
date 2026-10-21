<!--
Social posts for article 4, "Unlearn the loop" (RELEASE-CHECKLIST: X + Bluesky + Mastodon + Nostr).
Each is a single post, the shape the eval and as-of join posts settled on: the personal X account
has Premium (long posts), and Bluesky's 300-character cap is met by one short post instead of a
thread.
The article is live at https://nandan.me/writing/unlearn-the-loop/ (published 2026-10-21).
Rewritten 2026-10-21 for readers who skim: short sentences, one idea each, and no word a post does
not explain. The hook (q will let you write the loop, and it works; that is why q cannot teach you
to stop) comes first everywhere. The X and Nostr posts pick up from the as-of join posts
(2026-10-16) in one sentence. The three ideas the detour sends back are counted, not named (the
article names them). Glosses: "a counter, a loop, an accumulator" rather than do[]; "the one-word
version, sum" rather than "the idiom"; the fork is "a mean written J's way" or, where the X post
quotes it, "sum divided by count, with no data mentioned"; "the array version is two characters"
rather than "the idiom is +/"; the eval's "both arms" is "with and without the plugin"; the q
comment marker is explained where a snippet carries one.
Snippet provenance (X post only): `3 (+/ % #)\ 1 2 3 4 5 6` and its output `2 3 4 5` are the
transition chapter's two blocks under "The windows have a different shape, and nothing complains",
verbatim; `3 mavg 1 2 3 4 5 6f    / 1 1.5 2 3 4 5` is the next block, verbatim including its
trailing comment, which is the output make verify-prose checks. All three are byte-identical to
lessons/00-transition/README.md (checked 2026-10-21).
Tagging: KX is @kxsystems on X, inside the first 280 characters as in the eval and as-of join
posts. KX has no Bluesky, Mastodon or Nostr account (checked 2026-09-25), so those posts name KX in
plain text. J is named in plain text everywhere; no account is tagged for it.
Images: attach writings/figures/04/linkedin-card.png (1200×627, figure 1 rendered with
`rsvg-convert -w 1200`) to every post, with the card alt text below. Figure 3 goes in an optional
self-reply on X and Mastodon as writings/figures/04/figure-3-where-the-laboratory-lies.png
(1800×940, figure 3 at 2x) with the figure 3 alt text; as a second attachment it would be cropped
into a grid, as the only image of a reply it shows whole. Bluesky gets the card only.
No speed or performance wording anywhere (Clause 9 caution, as in the article).
Lengths checked 2026-10-21: X long post (Premium, 25,000 limit; about the first 280 characters show
before "Show more", so the opening carries the hook and the tag); Bluesky within 300 counting the
full URL; Mastodon within 500 with the link counted as 23.

Card alt text (all networks):
Two panels, both summing 1 2 3 4 5 with an explicit loop and printing 15. Left, J: a five-line
explicit definition with its own assignment form and a lone closing parenthesis; the idiom is +/.
Right, q: one ordinary line, do[count x; r+:x i; i+:1]; the idiom is sum. Headline: neither
language forbids the loop, only one makes it feel foreign.

Figure 3 alt text (the self-reply):
Two panels about J habits that break in q. Left, the fork fails loudly: +/ % # is a mean written
with no data; the same text typed into q is shown with the blank error message q prints and the
note "does not parse", so you cannot ship it; q wants avg or a lambda instead. Right, the windows
fail silently: the 3-period moving average of 1 to 6 gives four results in J (2 3 4 5) and six in
q (1 1.5 2 3 4 5), drawn as two rows of boxes aligned by position, so J's first value sits above
q's first; an arrow from J's first value to q's third shows where it belongs, two slots to the
right. Read q's first value as a full window and you are two slots early, with no error. Footer:
the thinking transfers, the plumbing does not; respect the silent one more.
-->

# X (single long post, tag @kxsystems)

Here is a perfectly good q program: a counter, a loop, an accumulator, and it prints 15. It will still be correct next year, in production. That is the problem. @kxsystems' q has every reflex you brought from Python or Java, and the answers come out right, so nothing ever nudges you toward the one-word version, sum. Article 4 of my array-thinking series.

J does not forbid loops either. But to write one you step outside J's ordinary notation: a definition block, a different assignment, a lone ) to close it. Five lines of visibly foreign machinery, where the array version is two characters. In q the loop is one ordinary line. That feeling of having wandered off is the whole case for a short detour through J before q.

The detour sends three habits back with you, and two of them break on the way home. One breaks loudly. J writes a mean as +/ % # (sum divided by count, with no data mentioned); the same text does not parse in q at all, so it can never ship. One breaks silently, and ships. The 3-period moving average of six numbers in J:

3 (+/ % #)\ 1 2 3 4 5 6

gives 2 3 4 5: complete windows only. The same request in q (in q, / starts a comment, and this one shows what the line returns):

3 mavg 1 2 3 4 5 6f    / 1 1.5 2 3 4 5

Six results, ramping up through partial windows. Neither is wrong. Both are called "the 3-period moving average". Read q's first value as a full window, the way J's would be, and you are two positions early, with no error.

Last week's article took q's as-of join apart; this one is about a quieter gap. Also in it: whether the shift actually takes, using my earlier eval of KX's q plugin (with and without the plugin, all three loop-to-array tasks were solved, and why that carries little weight), and why J rather than APL or BQN. Every snippet is copied from a lesson that runs in CI, on KDB-X Community Edition and J 9.7.1.

Article 4 of 5: https://nandan.me/writing/unlearn-the-loop/

Independent work; not affiliated with KX or Jsoftware.

#kdb #ArrayProgramming

# Bluesky (single post)

q has loops, and they work, so q alone will never make you stop writing them. J has loops too, but writing one means leaving its normal notation. That feeling is the case for a short detour through J before q. Article 4 of my array-thinking series:

https://nandan.me/writing/unlearn-the-loop/

# Mastodon (single post)

q has loops, and they work. You can write q for months and nothing pushes back. J has loops too, but writing one means leaving its notation, and that feeling is the case for a short detour through J before q. Two J habits then break on the way back. A mean written J's way, with no data in it, does not parse in q at all. A 3-period moving average of six numbers gives four results in J and six in q, and nothing complains.

Article 4 of 5: https://nandan.me/writing/unlearn-the-loop/

#kdb #q #ArrayProgramming

# Nostr (single note)

Here is a perfectly good q program: a counter, a loop, an accumulator, and it prints 15. It will still be correct next year, in production. That is the problem. Every reflex you bring from Python or Java has somewhere to land in q, the answers come out right, and nothing ever nudges you toward the one-word version, sum. Article 4 of my array-thinking series is about why a language that lets you stay comfortable cannot teach you a paradigm shift.

Last week's article took q's as-of join apart. This one is about a quieter gap. J does not forbid loops either. What differs is what writing one costs you: you leave J's ordinary notation for five lines of visibly foreign machinery, where the array version is two characters. That feeling of having wandered off is the whole case for a short detour through J before q.

The detour sends three habits back with you, and two of them break on the way home. One breaks loudly: a mean written J's way, with no data in it, does not parse in q at all, so it can never ship. One breaks silently: a 3-period moving average of six numbers gives four results in J, complete windows only, and six in q, which ramps up through partial windows at the start. Both are right, both are called the same thing, and reading q's first value as a full window puts you two positions early with no error.

Also in the article: whether the shift actually takes, using my earlier eval of KX's q plugin, and why J rather than APL or BQN. Written for people who have never read q or J; every snippet is copied from a lesson that runs in CI.

Article 4 of 5: https://nandan.me/writing/unlearn-the-loop/
Repo: https://github.com/nandanito/array-thinking-to-q

#kdb #programming #ArrayProgramming

# Self-reply with figure 3 (X and Mastodon, optional)

The two places the J detour misleads you, in one picture. The mean written with no data in it fails to parse in q, so it can never reach production. The moving-average windows can: J's first result is q's third, and nothing complains. Respect the silent one more.
