# Release checklist (operational — deliberately NOT in SPEC.md)

## Per article
- [ ] Milestone artifacts verify (`make verify` green for everything the article references)
- [ ] Draft in `writings/` reviewed; every code snippet copied from a RUNNING lesson file
- [ ] Publish canonical on nandan.me/writings
- [ ] X + Bluesky: short thread — hook + one snippet + canonical link
- [ ] Mastodon: single-post summary + link
- [ ] LinkedIn: 2–3 paragraph professional framing (strongest for articles 3, 5, 6)
- [ ] Nostr: note + canonical link (dogfood path: post via Nostr.day / Telenotes when ready)
- [ ] Append what happened to docs/COMPOUND.md (feeds article 6 for free)

## Per milestone
- [ ] Tag the repo
- [ ] Update README status
- [ ] COMPOUND.md entry: what worked, what broke, what transfers

## M5 only (v1 ship)

The marketplace-submission checklist that used to live here is **cut**: the M2 eval authored no
skill, so there is nothing to submit (eval/verdict.md). What ships instead:

- [ ] Curriculum complete and `make verify` green end-to-end
- [ ] `eval/harness/` packaged as a standalone reusable artifact — README covering the neutral-cwd
      contamination control, mechanical activation detection, and the self-verifying scorer
- [ ] Harness works **outside this repo** — verify on a clean checkout against some other plugin,
      since "run it from a neutral directory" is the one claim that cannot be tested from in here
- [ ] Eval numbers still re-derive: `make verify-eval-run` green
- [ ] v1 tag; README status updated
