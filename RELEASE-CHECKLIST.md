# Release checklist (operational — deliberately NOT in SPEC.md)

## Per article
- [ ] Milestone artifacts verify (`make verify` green for everything the article references)
- [ ] Draft in `writings/` reviewed; every code snippet copied from a RUNNING lesson file
      (enforced: `make verify-writings`, also run by `j-verify` on every PR; an article may opt out
      only with a visible `<!-- snippet-check: skip — reason -->`, which blocks publication)
- [ ] Publish canonical on nandan.me/writing/
- [ ] X + Bluesky: short thread — hook + one snippet + canonical link
- [ ] Mastodon: single-post summary + link
- [ ] LinkedIn: 2–3 paragraph professional framing (strongest for the eval, "Unlearn the loop" and "What compounds")
- [ ] Nostr: note + canonical link (dogfood path: post via Nostr.day / Telenotes when ready)
- [ ] Append what happened to docs/COMPOUND.md (feeds the final article, "What compounds", for free)

## Per milestone
- [ ] Tag the repo
- [ ] Update README status
- [ ] COMPOUND.md entry: what worked, what broke, what transfers

## M5 only (v1 ship)

The marketplace-submission checklist that used to live here is **cut**: the M2 eval authored no
skill, so there is nothing to submit (eval/verdict.md). What ships instead:

Done 2026-09-28 (PRs #43, #44 and the M5-close PR):

- [x] Curriculum complete and `make verify` green end-to-end
- [x] `eval/harness/` packaged as a standalone reusable artifact — README covering the neutral-cwd
      contamination control, mechanical activation detection, and the self-verifying scorer
- [x] Harness works **outside this repo** — verified on a clean checkout against another vendor's
      plugin (`eval/harness/README.md`, "Clean-checkout run"), which found four defects first
- [x] Eval numbers still re-derive: `make verify-eval-run` green
- [x] README status updated
- [x] `v1` tag (annotated, on the merge commit of #45, the M5-close PR)
