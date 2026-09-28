# What compounds: notes from a project where everything had to run

*Article 5 of 5, draft. Its milestone, M5 (curriculum v1 and the packaged eval harness), verifies.
Publishes after "Unlearn the loop".*

> **Provenance.** This article packages
> [`docs/COMPOUND.md`](https://github.com/nandanito/array-thinking-to-q/blob/main/docs/COMPOUND.md),
> a log the project appended to at every milestone from July to September 2026: what worked, what
> broke, what transfers. Each lesson below points to the incident it came from, and the incidents
> are dated there. Every q and J snippet is copied from a lesson page in the
> [curriculum](https://github.com/nandanito/array-thinking-to-q/tree/main/lessons/), where
> `make verify` runs it on KDB-X CE 5.0 or J 9.7.1 and diffs every output, and a second check
> requires each block here to be identical to a block on those pages.

---

For three months I built a short curriculum that takes an imperative programmer through the
array-programming paradigm shift, from a J laboratory to q, the language of kdb+. It came with two
rules I did not bend: every example runs, and every milestone appends what it taught to one file.
Along the way it grew an evaluation of KX's official q plugin for Claude Code, four articles, and
a harness for A/B testing plugins that anyone can now run.

This is the fifth article, and the one the rules were for. Almost nothing below is about q. It is
about checking your own work, because that is what kept going wrong, and the file that recorded
each failure turned out to be the most reusable thing the project made.

## q and J in ninety seconds

You need very little of either language to follow the rest.

q applies operations to whole lists. `til 5` is the list `0 1 2 3 4`, and you reduce a list by
naming the reduction, not by walking it (the text after `/` is a comment showing the result, and
`2f` is the float 2.0):

```q
sum til 5          / 10
avg til 5          / 2f
max til 5          / 4
```

Everything in q has a type number, which comes up later. A dictionary maps keys to values:

```q
d:`a`b`c!10 20 30
```

and its type is `99h`:

```q
d[`b]      / 20        — look up by key
key d      / `a`b`c    — get the keys list back
value d    / 10 20 30  — get the values list back
type d     / 99h       — the DICTIONARY type; remember this number
```

A table is a dictionary of columns flipped on its side (here `t:flip cd`, with `cd` mapping
column names to column lists), and its type is `98h`:

```q
type t          / 98h   — "table" is a named type...
t ~ flip cd     / 1b    — ...but t is *literally* flip cd, nothing added
```

(`~` is "match": `1b` means true.) J is the laboratory where the same ideas are harder to avoid.
Its best-known party trick is the fork, a function built from three others with no mention of
data:

```j
mean =: +/ % #     NB. a FORK: (sum) divided-by (count), read as one phrase
mean 0 1 2 3 4
```

```
2
```

That is enough. The rest is about what happens around code like this, not inside it.

## 1. A check you have only seen pass has not been observed

The first rule of the project, "every example runs", was enforced by `make verify`. It proved the
lesson *files* ran. It said nothing about the outputs pasted into the lesson *prose*, which is
where a reader actually looks. So I wrote a checker: re-run each lesson, and require every output
block in the text to appear in a fresh capture. It passed first time.

That was the wrong moment to relax. A check that passes on its first run has told you nothing yet,
so I started planting corruptions. One changed digit was caught. Two genuine blocks swapped out of
order were caught. Then I added a second check for claims written as comments, like the `/ 99h`
above, and planted three wrong claims in it. It caught two.

The one it missed was flipping lesson 02's `type d` comment from `99h` to `98h`. The check asked
whether the claimed value appeared anywhere in the lesson's output, and `98h` does, one block
later, as the type of a table. A wrong claim that collides with a real value is exactly the wrong
claim a reader would believe. The fix was to re-evaluate each claimed expression and compare for
equality instead.

![Two ways to check the comment "type d / 98h" in lesson 02. A membership check searches the lesson's captured output, finds 98h (printed by type t, a table) and passes the wrong claim. An equality check re-evaluates type d, gets 99h, and fails it. Of three planted wrong claims, membership caught two; this was the one it missed.](figures/05/figure-1-membership-is-not-equality.svg)

*Figure 1. A containment check is not an equality check, and it fails exactly where they differ.*

The pattern repeated at every scale. The eval's scoring script first *printed* each answer's
correctness while the committed `results.csv` could have said anything; it only became a check
when it compared the two and exited nonzero. And while I was packaging the eval harness for reuse, it
wrote its own first `results.csv` from a bug (every answer "failed" because a relative path did not
resolve) and then, on the next pass, agreed with it. A self-consistency check cannot see a bug that
both passes share. The only thing that caught it was running the tool somewhere its author had not.

**What transfers:** plant a failure in every new gate before you trust it, and plant more than
one, because a single corruption would have passed the membership check and been called proof.

## 2. Verified outputs do not verify the sentence next to them

"Unlearn the loop" had been executed and captured since July. Every output in it was real. An
adversarial review still found three wrong claims in it, all in prose sitting next to correct
output. The worst: I wrote that J's `for_i.` loop makes you "name an index". It binds each *item*;
the index is a separate name. The captured `15` printed directly under the claim refutes it,
because an index loop over `1 2 3 4 5` would sum `0` to `4` and print `10`. The evidence against
the sentence was on the page, and nobody read it that way, including me.

A subtler version came up in lesson 04, about why an as-of join needs sorted input. I showed four
joins in a grid (sorted or not, with an attribute or not) to prove the sort, not the attribute,
decides correctness. The claim was true. But the "sorted, no attribute" cell used a table sorted
with `xasc`, and q marks what `xasc` sorts:

```q
sorted:`sym`time xasc quote
```

```q
attr sorted`sym
attr sorted`time
```

```
`s
`
```

`` `s `` is the sorted attribute. The cell labelled "no attribute" had one, so the comparison did
not isolate the variable it claimed to. Every output was genuine and `make verify` was green; the
defect was in what the arrangement implied. The lesson now strips the attribute first, and that
cell shows an empty `` ` ``.

**What transfers:** output gates prove the numbers; only a reader can check what the prose says
the numbers mean. Read each verified output as a test of the sentence beside it, and when a
demonstration exists to isolate one variable, check that it does.

## 3. Confirmation is cheapest when you make it yourself

Three times, I stated a confident finding from a partial read of the right source.

The eval's most interesting result was that both conditions used the `` `p# `` attribute on an
in-memory table, where KX's `aj` reference pairs memory with `` `g# ``. It was the one paragraph
that gave a null eval some teeth, so it got the least scrutiny. A sibling page, on setting
attributes, says parted applies in memory as well as on disk, whenever the data can be sorted so
that it can be set, and the models had sorted it. Worse, the repo's own licensing notes had
recorded that exact correction three days before the eval was scored. I retracted the finding.

Later, CI setup needed an install token, or so I inferred from a phrase in my notes. I curled the
install URL, got a 401, and took it as confirmation. The 401 came from my own mistyped URL, missing
one path segment. The real endpoint needs no credential at all.

And the licence. The spec carried a one-line summary of KX's marketing. When I read the licence
itself, the grant in Clause 2.1 looked narrower than that line, so I replaced it with an equally
short line saying the opposite, and carried that into the README and an article. The grant is
"subject to the Usage Restrictions", a link, and Clause 11 makes those restrictions part of the
agreement. I had read the sentence up to the comma. Both one-line summaries turned out to be
wrong, and the repo now quotes the clauses instead of summarising them.

**What transfers:** when a check agrees with what you already believed, check the check before the
conclusion. Cite the source, then look for the page that contradicts it. And give a correction the
same full read as the claim it replaces.

## 4. The test environment must know less than the thing it tests

The eval compared Claude Code sessions with and without KX's q plugin. For that to mean anything,
the sessions' surroundings had to carry none of the help being measured. The single control that
decided it was the working directory. Run from inside this repository, the
"without" sessions would have inherited the repo's own q notes, roughly the thing under test, and
nothing in the results would show it. A contaminated null looks exactly like a clean one.

So the sessions ran from a scratch directory outside the repo, and every log opens with a line
recording what that session loaded. That was the right instinct, and it was still not enough:

- An account connector finished connecting partway through the run and put eight Google Drive tools
  into 3 of the 15 with-plugin sessions. The tool allow-list I had passed did not keep it out. None
  was used, and no score moved, but the two arms had not seen the same tools.
- Redacting the logs for publication surfaced a per-directory memory folder I had never checked.
  It was empty. Had the scratch directory been reused from an earlier q session, stored memory
  would have reached both arms invisibly.
- All fifteen "without" sessions ran before all fifteen "with" ones, which is how a connector that
  arrived mid-run could land on one side only.

Packaging the harness for other people fixed those: a fresh directory per session with a recorded
listing, connectors off, a randomised and recorded run order, and an audit that fails the run
unless every session's own log shows identical context apart from the plugin. Then I ran it from a
clean checkout against somebody else's plugin, and it found four more defects in a harness whose
self-test was green. Claude Code had started loading two built-in plugins into every session,
which broke the audit's assumption that the baseline has none. The seeded shuffle put the
with-plugin session first in every pair. The log redactor rewrote the word "builtin" wherever it
appeared. And there was the scorer bug from section 1.

**What transfers:** the tool allow-list is not the model's context. Assert the context per
session, from the session's own record, instead of trusting the flags you passed. And the claim
"it works outside my repo" can only be tested outside your repo.

## 5. A null result needs a power analysis for its wording

The eval returned no measurable lift: one task out of fifteen where the two conditions disagreed,
correctness 14 of 15 in both. The first draft said "no lift". The honest sentence is narrower. I
kept verification simple by choosing simple tasks, and simple tasks left the baseline near the
ceiling. (Exact-output checking does not require easy tasks; I just did not write any hard ones.)
A task set with that little room cannot express a large effect, so it cannot have failed to detect
one. (The article is
"[No headroom: what a null result on KX's q plugin actually measured](https://nandan.me/writing/no-headroom-kx-q-plugin/)".)

**What transfers:** before you write "no effect", ask what the largest observable effect was. For
any A/B on a frontier model, establish the baseline's failure rate first; a pilot of the baseline
arm alone would have shown this for 15 sessions instead of 50. And when the primary metric hits a
ceiling, record the secondary ones. Quality separated the arms on one task, by one judgement call;
output tokens separated them on every one of the fifteen, at about three times the total for the plugin.

## 6. Documents rot downstream, and in both directions

The recurring defect in this repo was never wrong code. It was documents that were true when
written and silently became false, with nothing failing. Lessons had `make verify`; the plan, the
spec and the checklists had nothing. Three shapes kept recurring.

**The stale text is where the result gets consumed.** When the eval authored no skill, the spec's
section on the eval was still accurate. The milestone list further down still read "skill hardened
from eval findings; marketplace submission", for a skill that would never exist.

**Positions move; names do not.** My licensing notes pinned a benchmark-publication restriction to
"Article 5". The series was renumbered, and a real legal constraint silently pointed at the wrong
article. Docs now name articles instead of numbering them.

**Corrections flow both ways.** One day, a correction to the eval's evidence reached the published
article but not a draft that sat behind a skip marker, until a review flagged it. The next day, it
ran the other way: corrections to the eval article's wording nearly never reached the verdict file
the article cites as its evidence. Each direction needs its own search.

**What transfers:** at every milestone, re-read the governing documents against reality, starting
with whatever was supposed to consume the thing you just finished. Refer to stable names, not
positions. When a claim changes, search every document that cites it, including the ones your
checks skip.

## The model in the loop

I wrote this project with an AI coding assistant, Claude Code, and its failures were mostly one
failure: the confident paraphrase. It drafted a speed claim with the no-speed-claims rule in its
context. It credited a lesson with a point the lesson does not make. The eval writeup we drafted
together reported a skill count taken from a session's description of itself (41) rather than from
that session's log (16).
Each read well and was wrong in a way only opening the source would show. The remedy was the same
as for my own mistakes above: open the cited thing before writing that it says something, and
treat a model's account of its own context as a claim, not a log.

## What did not compound

The log compounds only when it is read. Early on I treated `COMPOUND.md` as something to write at
milestones, and it paid off only at review time: the lesson 03 draft cited documentation URLs that
an earlier entry had already recorded as unfetchable, and the `` `p# `` correction was in the repo
before the finding it corrected. Nothing routed me back to either. A compounding document that
is only ever written is a diary; reading it before starting a class of work, not only after
finishing one, is what makes it an asset.

![Thirteen defects from the project's log, sorted into four columns by the kind of check that found them. A gate that runs (make verify, CI): typed q prompts in lesson 02's outputs; em dashes in figure text, one in a tspan; a missing CI secret that turned main red. An independent review (Codex): a no-attribute grid cell that had one; first bid where aj takes the last; name an index over a loop that binds items; connector tools in 3 of 15 plugin sessions. Preparing to publish (redaction, rendering): an auto-memory folder nobody had checked; a corrected claim left in a figure and its card. Running it elsewhere (a clean checkout, a new plugin): built-in plugins in every session; a seeded order with B first in every pair; a scorer that broke on relative paths; a redactor that rewrote the word builtin.](figures/05/figure-2-where-defects-surfaced.svg)

*Figure 2. Where the defects surfaced. Each kind of check found a different kind.*

---

## What to carry into the next project

- **Test every gate by breaking it**, more than once, and in the ways a reader would believe.
- **Outputs are checkable by machine; claims about them are not.** Budget a reader for the claims.
- **Distrust confirmation you could have manufactured**, and read the whole sentence.
- **Assert the environment per run** from the run's own record, and test portability away from home.
- **Word a null result by its headroom**, not by its headline.
- **Keep one append-only log of what broke, and read it before you start**, not just after.

The curriculum, the eval and the harness are at
[array-thinking-to-q](https://github.com/nandanito/array-thinking-to-q).

---

*Not affiliated with or endorsed by KX Systems, Jsoftware or Anthropic. "q", "kdb+", "KDB-X" and
"J" are used nominatively.*
