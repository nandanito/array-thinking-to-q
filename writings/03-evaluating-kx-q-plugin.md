# I ran a controlled eval on KX's official q plugin. The result was nothing.

*Article 3 of 6 — draft. Reports the M2 eval result. Evidence: [`eval/verdict.md`](../eval/verdict.md).*

---

I set out to answer a narrow question with an experiment instead of an opinion: **does KX's
official Claude Code plugin for q measurably improve a frontier model's q output?**

The answer, on fifteen paired tasks, is that I could not measure any improvement — and the more
useful finding is *why* I could not. The comparison never got a chance to run. That is a different
and more interesting result than "the plugin doesn't help", and the distance between those two
sentences is most of what this article is about.

## Why this experiment exists at all

I am writing a curriculum that teaches array thinking through q. The original plan included
authoring a q skill for Claude Code. Then I found that KX already ships official plugins for
q, PyKX, KDB-X and KDB.AI, with their own marketplace and a qlint integration.

Writing a competing general-purpose q skill would be redundant. But the *learning* objective was
never "author a skill" — it was "author and evaluate a skill". Evaluation survives the redundancy
intact. So the deliverable changed from a skill to an independent evaluation of the one that
already exists, with authoring gated behind the eval finding a gap.

Which means this article was always going to publish whatever came back. That commitment was made
in the protocol before any data existed, and it is doing real work now.

## The design, in brief

**Subject:** `q-knowledge@kx-skills`, pinned at commit `8b7040f`. There is no version tag upstream,
so the SHA is the pin.

**Conditions:** A = baseline, no plugin. B = that plugin loaded. Identical prompts, identical
model (`claude-opus-5`), identical settings.

**Part A — does it fire?** A skill that never activates is worth zero regardless of content.
20 prompts: 10 that should fire, 10 adjacent traps that should not (NumPy vectorization, plain
SQL, BQN trains, `merge_asof` in pandas, "group a JavaScript array by a key").

**Part B — is the output better?** 15 q tasks — translate from Python, write from an English spec,
fix a deliberately unidiomatic solution — each run under both conditions. Correctness by exact
golden-file diff. Idiomaticity as a **five-item binary checklist**, never a 1–5 "feel" score,
because a feel score drifts upward as my own q taste improves while the benchmark stays fixed.
Every checklist item has to be justifiable against a published source — Q for Mortals or
code.kx.com — rather than against my preferences.

**Decision rule, fixed in advance:** a paired sign test on discordant pairs. Count only the tasks
where the two conditions differ; the effect is real only if one side takes ≥~80% of them.

I want to flag one thing I am *not* claiming. **There is no blind scoring here, and blinding is
impossible in principle.** Idiomatic q identifies its own condition — you cannot un-see which
answer used `sums`. The published-source requirement is the defense against evaluator drift. It is
a weaker defense than blinding. Saying so is the price of using it.

## The control that decided whether any of this meant anything

My repository contains `.claude/skills/idiomatic-q/SKILL.md`. It carries anti-loop rules, "prefer
qSQL over row-wise thinking", and the `aj` sort-discipline gotchas. The root `CLAUDE.md` adds more
q guidance. The `lessons/` directory is full of verified idiomatic q.

Run the eval with Claude Code from inside that working copy and **condition A is not a baseline.**
It silently inherits a q idiom skill — approximately the thing under test. Both arms get treated,
the comparison measures nothing, and — this is the part that should scare you — **the results look
completely normal.** A contaminated null and a clean null are the same numbers.

So every one of the 50 sessions ran from an empty scratch directory outside the repository, with
no `CLAUDE.md` and no `.claude/`, driven headless. I verified it rather than assuming it, by asking
a session in each condition to enumerate what it had loaded. Condition A: 41 skills, none q-related,
no project instructions, and specifically no `idiomatic-q`. Condition B: the same, plus exactly
`q-knowledge:q` and `q-knowledge:qlint-snippet`.

The general form: **when the environment can leak the treatment into the control, that control is a
property of your harness, not of your analysis.** You cannot add it afterwards, and you cannot
detect its absence from the output.

## Part A: it fires

**8/10 on should-fire. 9/10 on the traps.**

The two should-fire misses are my instrument's fault, not the plugin's. Both prompts say "fix
*this* q code" and "convert *this* list comprehension" — and my table supplies no code. In an empty
directory the model searched for a file, found none, and asked me to paste the snippet. It never
attempted q, so there was nothing for a skill to help with.

I wrote "so really it's 8/8 on the well-formed prompts" in the first draft of this article, and an
adversarial reviewer was right to call it. **Choosing your denominator after you have seen which
items missed is the same overfitting my own protocol forbids** when tuning a skill's trigger
against a test set — I would not have accepted it from the plugin's authors, so I do not get to do
it in my own favour. Two of my twenty items were malformed. The recall this instrument measured is
**8/10**. Repairing those prompts makes a *different* test set, and any number off it has to come
from a fresh run.

The single false positive was "Write a query to fetch users by email" — answered entirely in q,
schema and all. Good q; an answer to a question nobody asked in q. Two caveats keep me from making
much of it: my harness deliberately strips all ambient context, so `q-knowledge` was the only
domain skill on the bench, and every trap built to bait a keyword match — `merge_asof`, "group",
J's rank operator — held firm. The mis-fire came from the *least* q-flavoured prompt in the set.

The reason Part A matters is that it forecloses the easy explanation for what comes next. **In Part
B the plugin loaded in 14 of 15 runs.** Whatever follows is a finding about an active plugin.

One methodological note that paid for itself immediately. I decided firing **mechanically** — the
session emitted a `Skill` tool call naming a `q-knowledge` skill, read off the session log — rather
than by judging whether the answer felt q-flavoured. Good thing: one prompt produced fluent,
correct q idioms (`xs where p xs`, `a f' b`) with **no skill loaded at all**, and in Part B one
task matched its plugin-armed twin without ever invoking the plugin. Eyeballing would have scored
both as fires. **If your eval measures activation, measure the tool call.**

## Part B: the ceiling

Generation and scoring were separate sittings — all 30 answers collected and saved verbatim first,
then scored in one pass with both conditions side by side. Scoring an answer right after generating
it means the second condition is read in the light of the first, and the checklist quietly stops
being independent.

Here is what came back.

| | condition A (baseline) | condition B (plugin) |
|---|---:|---:|
| Correctness | 14/15 | 14/15 |
| Idiomaticity | 73/75 | 74/75 |
| **Discordant pairs** | **1** | |
| Wins | 0 | 1 |

The sign test needs roughly five discordant pairs before it can adjudicate anything. I got one.
**The test never engaged.**

And that one pair is thin. It turns entirely on whether writing

```q
t:update notional:price*qty from t
show t
```

instead of

```q
show update notional:price*qty from t
```

counts as an unnecessary binding. Under the rule I fixed *before* scoring — a candidate fails the
"no unnecessary temporaries" item only if it introduces a binding the verified reference solution
does not need — it does. But the task said "add a column `notional` … and show the result", and
mutating the table is a defensible reading of "add". A second scorer could call it a tie without
straining. A margin that flips on one person's reading of one line is not a margin.

Meanwhile **five of the fifteen task pairs came back byte-for-byte identical**. Both conditions
wrote `show sums 1 2 3 4 5`. Both wrote `select n:count i by sym,side from t`. Both threw away the
`do`-loop and wrote `sum x`.

This is a **ceiling**, and it is the honest headline. The tasks cannot discriminate between the
conditions because baseline `claude-opus-5` already solves them. (Pedantically: my protocol defined
the ceiling case as 15/15 in both arms, and I got 14/15 — the one miss being the same task in both
arms, correct join, failed on an extra output line. Substance yes, letter no. Pre-registering your
degenerate cases is worth nothing if you then gesture at them approximately.)

## The mistake I made, stated plainly

I wrote fifteen tasks that were easy to *verify*. Every one has a reference solution that runs and
a golden output that diffs. That discipline is what makes the eval trustworthy — and it is exactly
what broke it, because **tasks that are easy to verify are tasks that are easy to solve.** "Sum of
squares." "Total qty by sym." A frontier model in 2026 does not need help with these from anyone.

The fix costs an hour and I did not spend it: **run the baseline arm alone first, and check that it
fails often enough to leave room for the treatment to show.** Fifteen sessions would have told me
this task set had no headroom, before I spent fifty on a comparison that could not resolve.

So the result I am publishing is not "the plugin doesn't help". It is **"this instrument could not
have detected a small effect, and detected no large one."** Those differ, and only the second is
something I earned. The first would be the cleaner sentence, which is precisely why I have to
resist writing it.

## What did separate the conditions

The tasks could not discriminate on quality. They discriminated cleanly on cost.

| | A | B | ratio |
|---|---:|---:|---:|
| Total output tokens, 15 tasks | 3,671 | 10,337 | **2.8×** |
| Median per-task ratio | | | **3.9×** |
| Widest single task | 23 | 407 | **17.7×** |

Roughly three times the output tokens, for code that scored identically on thirteen of fifteen
tasks and was *literally the same code* on five of them. When your primary metric hits a ceiling,
the secondary metrics are the finding.

## The one genuinely interesting failure — and it belongs to both arms

Task 15 hands the model an as-of join that returns silently wrong quotes because the quote table
is not sorted by time within sym, and asks it to fix the join and *set the appropriate in-memory
attribute*.

Both conditions sorted correctly. Both produced the exactly correct joined table. And both applied
`` `p# `` where my task sheet cites `` `g# ``.

**I first wrote this section up as a finding, and I had it wrong.** The draft said both arms had
reached for "the disk attribute on an in-memory table", citing [the `aj`
page](https://code.kx.com/q/ref/aj/), which frames the pair as memory → `` `g# ``, disk →
`` `p# ``. Then the sibling page: [set-attribute](https://code.kx.com/q/ref/set-attribute/) says of
parted, *"If the data can be sorted such that `p` can be set, it effects better speedups than
grouped, both on disk and in memory."* Both candidates sorted the table first. That is precisely
the precondition. `` `p# `` there is defensible, and possibly faster.

The part that stings: **my own repository already contained that correction.** A licensing-and-docs
audit I ran back at milestone one recorded, in writing, that `p#` "also works in memory and can
outperform `g#` when values are contiguous. It is not useless in memory." I scored the eval months
later, cited the `aj` page, and never opened either the sibling page or my own notes on exactly
this claim.

So the honest version of this section is much smaller than the one I wanted to write. There is no
"KX's plugin failed to correct a deviation from KX's own guidance." There is: both arms diverged
from *my* task sheet, in a direction the documentation supports, and **my task sheet is the thing
that was too narrow.** It names one attribute as though it were the only right answer.

I have left the score at zero, because the scoring rule was fixed before the pass and gets applied
consistently or it is not a rule. But the interpretation is retracted, and since both arms diverged
identically it never touched the comparison anyway.

That is also the end of the one candidate "gap" this eval produced. My protocol permits authoring a
skill only if the eval exposes a gap the plugin does not fill; what it actually exposed was a defect
in my own instrument. No skill, then — and a sharper task set goes in the notebook.

## What I would tell you to steal

- **Establish your baseline's failure rate before designing the comparison.** Otherwise you build
  an instrument with no headroom and find out fifty sessions later.
- **Measure activation as a tool call, not a vibe.** Fluent domain output is not evidence that a
  domain skill loaded.
- **Build the harness so it cannot leak the treatment into the control** — and verify that by
  asking, not by assuming. A contaminated null is indistinguishable from a clean one.
- **Smoke-test the treatment arm's happy path specifically.** My first run had condition B's reads
  of its own bundled reference files being permission-denied — the harness was handicapping the
  plugin against its own design. A harness bug that weakens the treatment reads as a null result.
- **Write down the taste-dependent scoring rules before the scoring pass, and anchor them to an
  artifact.** "No unnecessary temporaries" is pure preference until you tie it to something — for
  me, the verified reference solution. Doing that first is what turned this run's entire margin
  into a documented caveat instead of a headline.
- **Read the sibling page before you call something a deviation from the docs.** My one juicy
  finding evaporated on the second page of the same reference — and my own repo had already written
  the correction down. When a result flatters your thesis, that is the moment to go looking for the
  page that kills it.
- **Publish the null.** It cost the same fifty sessions a positive would have.

## Verdict

No lift, on a task set that could not have shown a small one. KX's `q-knowledge` plugin activates
reliably and writes good q. So does the model without it, on tasks this easy, for a third of the
tokens. No skill authored. The curriculum ships on its own merits.

The eval was underpowered, and that is the finding I actually have. It is worth publishing because
the failure mode generalises far past q: **an A/B against a frontier model is measuring your task
set at least as much as your treatment**, and if you did not check the baseline for headroom first,
a null result is telling you about your benchmark, not about the thing you were testing.

---

*Everything behind this: [`eval/verdict.md`](../eval/verdict.md) for the full writeup and the
threats-to-validity list, [`eval/runs/`](../eval/runs/) for all 30 answers verbatim and the
per-task scoring rationale, [`eval/harness/`](../eval/harness/) for the scripts. The correctness
column recomputes from the committed answers with one command.*

*Not affiliated with or endorsed by KX Systems. "q", "kdb+" and "KDB-X" are used nominatively.*
