# Toolchain — pinned versions (SKELETON)

> Task Zero requires recording the EXACT downloaded build as the pinned known-good release.
> Both J and q/KDB-X are now PINNED (2026-07-24). Do not fill in a version you have not actually run.

## J  — PINNED (known-good) 2026-07-24

- Interpreter: `jconsole` (J language REPL, jsoftware, GPLv3).
- **Version: J 9.7.1** — banner (`9!:14''`): `j9.7.1/j64arm/darwin/…/2026-04-06/clang-17…`.
  j64arm = Apple Silicon.
- **jconsole path: `~/j9.7/bin/jconsole`.** `~/.zshrc` exports `J=$HOME/j9.7/bin/jconsole`, so
  `make verify` picks it up flag-free in an interactive shell (Makefile uses `J ?=`). CI / non-login
  shells don't source `.zshrc` — there, pass `make J=$HOME/j9.7/bin/jconsole` (or set it in the job).
- Install method (headless, no GUI, CI-friendly — the Homebrew `j` cask is broken on current
  Homebrew, see COMPOUND.md): install via jsoftware's own script, skipping the Jqt IDE and addons:
  `curl -fsSL jsoftware.com/download/j9.7/jinstall.sh | sh -s -- --qt none --no-addons`
  (installs to `~/j9.7`; add `--qt full` / drop `--no-addons` if the IDE or addons are wanted).
- ⚠️ Name collision on macOS: `/usr/bin/jconsole` is Apple's **Java** JConsole shim (dispatches to
  the JDK), NOT the J interpreter — so plain `jconsole` on PATH is the WRONG tool. Always invoke J
  by absolute path or via `make J=$HOME/j9.7/bin/jconsole`. On Ubuntu CI runners `jconsole` is the
  J interpreter, so the collision is local-only.

## q / KDB-X  — PINNED (known-good) 2026-07-24

- Runtime: `q` from **KDB-X Community Edition**.
- **Version: KDB-X 5.0, build `2026.07.23`** (banner: `KDB-X 5.0 2026.07.23 … Kx Systems`).
- Edition: **COMMUNITY**. License: **NONEXPIRE** (the key does not expire — resolves the earlier
  "12-month?" open question).
- Platform verified on: **m64** (macOS 64-bit), author's machine. Native Windows unsupported
  (WSL only); Linux x86_64/ARM + macOS supported — see docs/licensing-notes.md.
- Enforced caps (`.Q.lim[]`, confirmed 2026-07-24): **mem 16384 MB (16 GB) · threads 4 · conns 16 ·
  cores 0W** (no per-process core limit; the 24-core figure is an aggregate *license* cap). The
  banner's 18432 MB is machine RAM, not the cap.
- License terms, phone-home, benchmark clause: docs/licensing-notes.md.
- ⚠️ Deliberately NOT recorded here (repo is public): the license serial, licensed email, and
  hostname from the startup banner. Do not commit those.

## KX Claude Code plugins (eval subject)

- Marketplace: **`KxSystems/kx-skills`** — `/plugin marketplace add KxSystems/kx-skills`.
- **Pinned commit (known-good): `8b7040f769c6653db67b063aa34c944729e8857e`.** The marketplace has
  no version tag, so the SHA is the pin. Eval subject is `q-knowledge@kx-skills` (see eval/PROTOCOL.md).

## Makefile knobs

- `make verify-j J=<path>` overrides the J interpreter (needed on macOS; see collision above).
- `make verify-q Q=<path>` overrides the q binary.
