# array-thinking-to-q

**Learn array thinking in a short J laboratory, then go where the industry actually pays for it: q/kdb+.**

Most "learn an array language" material teaches syntax. The hard part isn't syntax — it's
unlearning the loop. This repo takes an imperative programmer through that shift using **J as a
compact laboratory** for the paradigm, then spends the overwhelming majority of its pages on **q**:
real tables, qSQL, attributes, and an as-of join.

Every code block in every lesson is executed by `make verify`. The outputs printed in the prose are
captured from the real interpreters — never hand-typed, never guessed.

---

## Status

A learning-in-public project, built one verified lesson at a time. Honest state of play:

| Area | State |
|---|---|
| Part II — q lessons | **3 of ~4 written**: [atoms & lists](lessons/01-atoms-and-lists/), [dict → table](lessons/02-dict-to-table/), [qSQL](lessons/03-qsql/). Attributes & sort discipline next. |
| Showcase — as-of join | [Runs end-to-end](showcase/aj/), golden-filed |
| Part I — J laboratory | Not yet written (1–2 illustrative, read-along lessons) |
| Transition chapter | Not yet written |
| Eval of KX's official q plugin | Harness + 15 tasks + 20 trigger prompts built; **the run itself is pending** ([plan](eval/PLAN-M2.md)) |
| `idiomatic-q` skill | Conditional stub — authored **only** if the eval proves a gap |
| CI | `j-verify` blocking on every PR; q verification is author-side only (license-gated) |

## Start here

- **[`lessons/`](lessons/)** — the curriculum, in order. Start with the [Part II index](lessons/README.md).
- **[`showcase/aj/`](showcase/aj/)** — trades matched to prevailing quotes, end-to-end.
- **[`SPEC.md`](SPEC.md)** — what this project is and is not, including its non-goals.
- **[`docs/COMPOUND.md`](docs/COMPOUND.md)** — lessons learned at each milestone, kept continuously.

## Run it yourself

**You do not need a J toolchain to read this repo.** Part I is read-along: J snippets with their
captured outputs. J stays executable in CI because it costs nothing to run, but no reader is
asked to install it.

To run the q lessons you need your **own** KDB-X Community Edition install and license key (see
[licensing](#licensing-the-honest-version) below — the terms are restrictive, read them).

```sh
# everything: q lessons + J twins + the aj golden file + the eval reference solutions
make verify Q=/path/to/q J=/path/to/jconsole

# or one leg at a time
make verify-q Q=/path/to/q
make verify-j J=/path/to/jconsole
```

The tool paths are explicit because neither binary is reliably on `PATH` — and on macOS
`/usr/bin/jconsole` is **Apple's Java console**, not J. Pinned known-good versions and the full
story are in [`docs/toolchain.md`](docs/toolchain.md).

**Windows:** KDB-X is not supported natively — use WSL.

## Everything executes

This is the constraint the whole repo is built around:

- No code block lands in a lesson unless `make verify` runs it.
- Printed outputs are captured from the real tools, then pasted into the prose. Hand-computed
  "expected" output drifts from what q and J actually display.
- A lesson whose q side does not run stays in `drafts/` and out of `lessons/`.
- Golden files exist for the showcase and the eval references, so silent rot in a toolchain
  upgrade fails a check instead of quietly changing the teaching.

## Why J, and why not BQN

J is the laboratory here for an honest and unglamorous reason: **it is the author's native array
language**, so the J half costs hours instead of weeks and the writing can be opinionated rather
than tentative.

If you have no particular destination and just want the array paradigm with the gentlest possible
on-ramp, **[BQN](https://mlochbaum.github.io/BQN/) is probably the better first stop** — better
error messages, better documentation for newcomers, a friendlier community on-ramp. The concepts
transfer either way; nothing in the paradigm is J-specific.

What J uniquely contributes here is the *contrast*. Its rank machinery and tacit forks are exactly
the parts that **do not** carry into q, and seeing them fail in q is a sharper lesson than never
having met them. Each q lesson carries a short J twin for that reason.

## Prior art and better books

This repo is a narrow, opinionated path, not a reference. These are the things it stands on:

- **[Q for Mortals](https://code.kx.com/q4m3/)** — the standard q book. If you want one
  comprehensive q text, it is this, not this repo.
- **[code.kx.com/q/ref](https://code.kx.com/q/ref/)** — the q reference; every idiom claim in these
  lessons is checked against it.
- **[J for C Programmers](https://www.jsoftware.com/help/jforc/contents.htm)** and
  **[Learning J](https://www.jsoftware.com/help/learning/contents.htm)** — the J texts.
- **Jim Pivarski's ["Thinking in Arrays"](https://github.com/jpivarski-talks/2023-07-11-scipy2023-tutorial-thinking-in-arrays)**
  (SciPy 2023) — adjacent in name and spirit, different lane: NumPy/Awkward Array in Python rather
  than J and q. Credited explicitly because the phrase "array thinking" is his territory too.
- **[Rosetta Code](https://rosettacode.org/wiki/Category:J)** — for seeing the same task in many
  languages at once.

## Licensing (the honest version)

**q / KDB-X Community Edition is not a permissive free-software license — do not assume it is.**
Per the [KX Community Edition License Agreement](https://kx.com/legal/community-edition-license-agreement-08-27/)
(v1.1, 27 Aug 2025), as read in full for this project:

- Use is granted for **personal or internal-business purposes only**. It is not a grant to
  distribute, sell, or monetise the software, or to build a competing product.
- **Publishing benchmark or performance figures requires KX's prior written consent** (Clause 9).
  This project therefore makes **no performance claims about KDB-X anywhere** — the as-of join
  material argues design and semantics, never speed.
- A license key is required, and license validation involves a periodic call home.

Full notes, with the caps confirmed against `.Q.lim` on a real install, are in
[`docs/licensing-notes.md`](docs/licensing-notes.md). Get your own build and key from
[KX](https://developer.kx.com/products/kdb-x); this repo distributes lessons, never the software.

**J** is GPLv3 and free to run, which is why it is the one green check in CI that depends on
nobody's commercial terms.

### This repo's own content

Copyright 2026 Nandan. Licensed by content type, because a curriculum is two different things:

| What | License |
|---|---|
| **Code** — the Makefile, CI workflows, and every q/J code sample, **including the snippets embedded in lesson prose** | [Apache-2.0](LICENSE) |
| **Prose** — lesson narrative, `docs/`, articles in `writings/` | [CC-BY-4.0](LICENSE-CC-BY-4.0.txt) |

The boundary is deliberate: **lift any q or J snippet from a lesson into your own work under
Apache-2.0**, with no attribution obligation attaching to your source file. The idioms are the
point; they should travel freely. Attribution under CC-BY applies when you reuse the *writing* —
the explanations, the arguments, a lesson as a whole.

Apache-2.0 rather than MIT for the code, for two reasons specific to this repo: it carries an
express patent grant, and its §6 explicitly withholds any trademark license — which matters when
the material is saturated with third-party marks (see below). See [`NOTICE`](NOTICE).

## Disclaimer

"q", "kdb+", "KDB-X", and "J" are third-party marks, used **nominatively** to identify the
technologies this material teaches. This project is **not affiliated with, sponsored by, or
endorsed by KX Systems, Inc. or Jsoftware, Inc.** All opinions are the author's. Nothing here is a
statement about either product's performance.

---

<sub>**Keywords:** array programming · kdb+ · q language · qSQL · J language · APL family · vector
programming · as-of join · array thinking · learning in public · verified curriculum</sub>
