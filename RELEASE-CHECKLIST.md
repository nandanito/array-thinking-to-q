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

## M5 only (marketplace submission)
- [ ] Trigger-precision numbers published in the skill README as its quality evidence
- [ ] Skill description/triggers tuned from eval part A, not guessed
- [ ] Marketplace metadata: name, description, when-to-use, example invocations
- [ ] Skill works standalone (installed without the repo) — verify on a clean machine
