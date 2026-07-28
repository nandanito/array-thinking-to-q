# Array thinking, all the way to q: learning in public

*Article 1 of 6 — draft. The series opener. Repo:
[array-thinking-to-q](https://github.com/nandanito/array-thinking-to-q).*

---

I am writing a short curriculum that takes an imperative programmer through the array-programming
paradigm shift and lands them in **q/kdb+**, with a brief stop in **J** on the way. Every code
example in it runs. I am publishing six articles as I go.

This is the first one, so it owes you three things: what the project is, what rules it runs under
and why those rules turned out to matter more than I expected, and what "learning in public"
actually costs once you commit to it.

## The thesis

Most "learn an array language" material teaches syntax. Syntax is not the hard part. The hard part
is **unlearning the loop** — and the reason that is hard is that nothing forces it.

You can write q for months with `do[]`, `while[]`, an index variable and an accumulator. It works.
The answers are correct. There is no error, no warning, no performance cliff at the sizes you test
on. A language comfortable enough to let you stay imperative will not teach you to stop being
imperative.

So: **J as a short laboratory, then q as the destination.** J is where the shift is unavoidable —
its ordinary notation gives you nowhere comfortable to put a loop. q is where you ship. J is one or
two read-along lessons; you need no J toolchain to read the repo. Everything after the transition
chapter is q: real tables, qSQL, attributes, an as-of join.

I should be honest that J is the laboratory partly for an unglamorous reason: **it is the array
language I already think in**, so that half costs hours instead of weeks. If you have no
destination in mind and just want the paradigm, [BQN](https://mlochbaum.github.io/BQN/) is probably
a gentler on-ramp. The concepts transfer either way.

## Why there is a hierarchy of objectives, and what it bought

The project has four objectives, ordered, with a standing rule that **when they conflict, the
lower-numbered one wins**:

1. **Learning.** I write real running q, and learn skill *evaluation* as a transferable discipline.
2. **Curriculum.** Verified lessons: imperative programmer → array-native.
3. **Skill evaluation.** An independent, published evaluation — authoring something only if that
   evaluation proves a gap.
4. **Blog.** Six articles as a forcing function. Exhaust of the work, never its driver.

That looked like planning ceremony when I wrote it. Then it did real work, twice.

**Once, when the ground moved.** Objective 3 originally read "author a q skill for Claude Code."
Partway through setup I discovered KX already ships official Claude Code plugins for q, PyKX, KDB-X
and KDB.AI, with their own marketplace and a linter integration. Authoring a competing general-purpose
q skill would be redundant.

Without a hierarchy that is a small identity crisis. With one it is a lookup: the *learning*
objective says "authoring **and evaluation**", and evaluation survives the discovery completely
intact. So the deliverable changed from a skill to an independent evaluation of the one that already
exists — and authoring got gated behind that evaluation finding a gap. Ten minutes, not a week of
sulking.

**Once, when it would have been convenient to forget it.** Objective 4 says the blog is exhaust,
never the driver. That is easy to agree with and hard to honour, because "what would make a better
article" is a genuinely seductive input. It has already forced a null result into print (article 3)
and thrown away the framing I wanted for another (see [article 2](02-kdb-x-licensing-maze.md)).
Both were correct calls and neither was comfortable.

## The constraint the whole repo is built around

**Everything executes.** A q or J example does not land in a lesson unless `make verify` runs it.
Printed outputs are captured from the real interpreters and pasted in — never hand-typed, never
reconstructed from memory.

Exactly two blocks are exempt, both marked where they appear: an illustrative Python snippet showing
the instinct being unlearned, and one q expression that *fails to parse on purpose* — which
therefore cannot live in a verify-clean file and is quoted as a real REPL transcript instead.

The cap of two is deliberate. Exemptions are the kind of thing that go from two to nine without
anyone deciding.

That rule sounds like ordinary testing discipline. In a *teaching* repo it does something stronger,
because the output in the prose **is** the lesson. A lesson whose printed result drifts from what
the tool actually prints is not slightly stale, it is teaching something false — with all the
authority of a code block.

## The half that verification doesn't cover

Here is the thing I did not expect, and it is the main reason this article exists.

`make verify` proves my *code* runs. It says nothing about whether my *claims* are true. And every
serious defect in this project so far has been a claim, not a line of code.

Four, in order of discovery:

- A **CI check that went green having verified nothing.** Its install step was a commented TODO
  gated on "when the first J file lands"; the files landed, the gate was never updated, and the
  tick stayed green. A TODO in CI is a time bomb with no alarm.
- **Two rules in my own contributor instructions** that were accurate when written and had since
  become false — one pointing at a directory convention that never existed, one holding a decision
  "pending research" that had concluded weeks earlier. Both read as current.
- A **README status table** advertising work as pending that had already shipped. I fixed that one
  this week, while writing this article.
- And then the one that actually stung, two days ago.

I published [an evaluation](03-evaluating-kx-q-plugin.md) that came back null, and the one genuinely
interesting paragraph in it reported that both test conditions had used the "wrong" attribute on a
kdb+ as-of join, against KX's own documentation. It was the single result with any teeth in an
otherwise flat writeup.

It was wrong. The sibling page of the same reference says the attribute they chose is legitimate
and can be *faster* under exactly the conditions present. Worse: **my own repository had already
recorded that correction, in writing, three days earlier**, in an audit I ran and then never re-read.
I cited one page, drew the opposite conclusion, and shipped it.

Two things I took from that. First, **the claim that flatters your thesis is the one to attack
hardest** — it is precisely the one that gets the least scrutiny, because you want it to be true.
Second, **prior work does not protect you if nothing routes you back to it.** A verified finding
filed in a document nobody re-reads is indistinguishable from a finding never made.

So the repo now has a mandatory per-milestone step to re-read its own governing documents against
reality, and part of the published evaluation has a `make` target that recomputes it from committed
artifacts and **fails if the committed table disagrees** — specifically the pass/fail column and the
per-session activation traces, which are the numbers a reader is most likely to take on trust. The
judgement-based scores it cannot recompute, so those stay defended by writing the scoring rules down
before scoring. Both exist because of specific defects, not because they sounded rigorous.

## What learning in public actually means

It is not "post progress." Progress posts are easy and roughly worthless.

It means the null result gets published with the same effort as a positive one would have. It means
when the interesting paragraph turns out to be wrong, you go back and retract it in the article
that already shipped — which I have now done, and which is a strange feeling I recommend. It means
the repository carries the raw material behind every number: all fifty session logs from that
evaluation, the exact prompts, the scoring rationale, the losing answers.

And it means writing down the mistakes in enough detail that they are useful to someone else, which
is harder than it sounds, because the useful part is usually the reasoning that led you astray
rather than the wrong answer itself.

The upside is straightforward: I am a better q programmer than when I started, and I now have an
evaluation harness I trust — mostly because it has already caught me.

## The six articles

1. **This one** — the project, the rules, and what they cost.
2. **[Running q in a public repo: the KDB-X licensing maze](02-kdb-x-licensing-maze.md)** — reading
   the actual license before writing any CI, and the three findings that changed the build.
3. **[Does KX's official q plugin actually make Claude better at q?](03-evaluating-kx-q-plugin.md)**
   — a controlled evaluation, a null result, and why the null is about my benchmark rather than
   their plugin.
4. **The as-of join** — what changes when the language and the storage engine are designed around
   one primitive. No benchmark numbers, for reasons article 2 explains.
5. **[Unlearn the loop: what J shows that q hides](05-unlearn-the-loop.md)** — the laboratory, and
   the two places it lies to you on the way home.
6. **What compounds** — packaging the lessons-learned file that gets appended at every milestone.

Articles 4 and 5 are drafted or pending against milestones that have not shipped yet. Each publishes
only when the artifacts it describes actually verify — which is the same rule as the code, applied
to the writing.

---

*Not affiliated with, sponsored by, or endorsed by KX Systems, Inc. or Jsoftware, Inc. "q", "kdb+",
"KDB-X" and "J" are third-party marks used nominatively.*
