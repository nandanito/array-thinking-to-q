# docs/ — working notes, not curriculum

**These files are held to a different standard than [`lessons/`](../lessons/).** The lessons are
verified: every q and J example in them is executed by `make verify`, and every printed output is
captured from the real interpreter. Nothing in this directory carries that guarantee. It is the
project's working record — research notes, decisions and their reversals, and what each milestone
taught. Read it as a lab notebook, not as teaching material.

| File | What it is |
|---|---|
| [`toolchain.md`](toolchain.md) | The pinned known-good versions of J and KDB-X, how they were installed, and the gotchas that bite (the macOS `jconsole`/Java name collision; why tool paths are passed to `make` rather than trusted on `PATH`). The one file here that is genuinely reader-facing — start here if you want to reproduce the setup. |
| [`licensing-notes.md`](licensing-notes.md) | The full read of the KDB-X Community Edition license, done because this repo runs q in public and the terms are restrictive. Records what the license actually says (personal / internal-business use only; benchmark publication restricted), what was confirmed against a live install, and which secondary sources turned out to be wrong. |
| [`COMPOUND.md`](COMPOUND.md) | Lessons learned, appended at every milestone: what worked, what broke, and what transfers to other projects. Deliberately candid, including about the author's own wrong guesses — a correction is more useful than a clean narrative. |

Two things follow from "notes, not curriculum":

- **Entries are timestamped and not retroactively tidied.** Where a later finding overturned an
  earlier one, both stay, with the correction marked. The trail is the point; a document that
  silently absorbs its own mistakes teaches nothing about how the work actually went.
- **Excluded from any future documentation site.** If this repo ever grows an mkdocs/Pages build,
  it should be generated from `lessons/`, not from here — publishing a lab notebook as
  documentation would misrepresent both.
