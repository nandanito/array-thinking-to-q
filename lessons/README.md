# Part II — q

> Everything in this directory is **q**. Part I (the J laboratory) is where the array
> *paradigm* is felt; the full transition chapter ("everything after this point is q,
> and here is what does **not** carry over") lands with Part I in a later milestone.
> Until then, each Part II lesson carries its own short J twin so the contrast stays live.

Part I taught the *shift*. Part II is where the paradigm earns its keep: real tables, qSQL,
and an as-of join, in the language people are actually paid to write.

## The contract every lesson keeps

- **Q-first.** The q side is written and *running* before a word of narrative or any J twin.
- **Everything executes.** Every code block below comes from a file under `q/` or `j/` that
  `make verify` runs. The outputs shown in each lesson are **captured from the real tools**
  (KDB-X CE 5.0, J 9.7.1) — never hand-typed, never guessed.
- **Narrative is the product.** A lesson explains *why* an idiom is shaped the way it is and
  what the imperative instinct gets wrong. Two code blocks and a sentence is not a lesson.

## The arc (built one lesson at a time)

| # | Lesson | The core idea | Status |
|---|--------|---------------|--------|
| 01 | [Atoms, lists, and the death of the loop](01-atoms-and-lists/) | the list is the unit of work; `each`/`over`/`scan` replace the loop | ✅ done |
| 02 | [dict → table](02-dict-to-table/) | a table is a flip of a column dictionary; a keyed table *is* a dictionary | ✅ done |
| 03 | [qSQL](03-qsql/) | `select … by … from` is a surface over column-lists; `by` cuts, it does not aggregate | ✅ done |
| 04 | [attributes & sort discipline](04-attributes/) | an attribute is a perishable *claim*, not an index; `aj`'s correctness is the sort, not the `` g# `` | ✅ done |
| — | [showcase: as-of join](../showcase/aj/) | trades matched to prevailing quotes, end-to-end | ✅ gate green |

Atoms and lists are deliberately **half** of lesson 01, not the payload: the payload is
unlearning the loop. The conceptual centre of Part II is lesson 02 (dict → table).

## Run the lessons yourself

The tool binaries are not on a bare `PATH` (see [`docs/toolchain.md`](../docs/toolchain.md)
for why — including the macOS `jconsole`/Java name collision), so pass them to `make`:

```sh
make verify-q Q=$HOME/.kx/bin/q            # run every lesson's q
make verify-j J=$HOME/j9.7/bin/jconsole    # run every lesson's J twin
make verify   Q=$HOME/.kx/bin/q J=$HOME/j9.7/bin/jconsole   # everything, incl. showcase + eval
```

Running the sources is only half of the contract. `make verify-prose` (included in `make verify`)
enforces "captured from the real tools" rather than asserting it, in the two ways a lesson can
state an output:

- **Output blocks** must appear as a contiguous run of a fresh capture, *in execution order*.
- **Trailing `/ 2f` annotations** inside `q` blocks are re-evaluated against the lesson's own q
  source and must equal what they claim.

Or run a single file directly:

```sh
$HOME/.kx/bin/q lessons/01-atoms-and-lists/q/atoms.q -q < /dev/null
$HOME/j9.7/bin/jconsole < lessons/01-atoms-and-lists/j/mean-fork.ijs
```

---

*"q", "kdb+", "KDB-X", and "J" are third-party marks, used nominatively. This project is not
affiliated with or endorsed by KX Systems or Jsoftware. See the repository README.*
