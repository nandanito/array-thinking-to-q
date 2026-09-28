#!/usr/bin/env python3
"""schedule.py --prompts DIR --out DIR --seed N [--conditions AB] [--dry-run]

Run one session per (task, condition) in a seeded random, interleaved order,
and record that order BEFORE the first session starts.

  --prompts DIR     one <task>.txt per task (mkprompts.py writes these)
  --out DIR         where the logs go: <task>.<cond>.jsonl/.stderr/.pre, plus
                    order.tsv; must not already hold logs
  --seed N          the shuffle seed; recorded in order.tsv
  --conditions AB   which conditions to run (B alone for activation-only runs)
  --dry-run         write and print order.tsv, run nothing

Why: in M2 every condition-A session ran before every condition-B one, so
anything that changed during the run (an account connector finishing its
connection, a rate limit, a model-side deploy) lands on one condition only.
Here the tasks are shuffled and each task's conditions run back to back, with
A first in half the pairs and B first in the other half (which half is random),
so drift within the run is spread across both conditions and a
pair's two sessions are minutes apart, not a whole run apart. audit.py --order
checks afterwards that the logs' own timestamps follow the recorded order.
"""
import argparse, pathlib, random, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("--prompts", required=True, type=pathlib.Path)
ap.add_argument("--out", required=True, type=pathlib.Path)
ap.add_argument("--seed", required=True, type=int)
ap.add_argument("--conditions", default="AB")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

if set(a.conditions) - {"A", "B"} or not a.conditions:
    sys.exit(f"--conditions must be drawn from A and B, got {a.conditions!r}")
tasks = sorted(p.stem for p in a.prompts.glob("*.txt"))
if not tasks:
    sys.exit(f"no <task>.txt prompts in {a.prompts}")
a.out.mkdir(parents=True, exist_ok=True)
if any(a.out.glob("*.jsonl")) or (a.out / "order.tsv").exists():
    sys.exit(f"{a.out} already holds a run; use a new --out")

rng = random.Random(a.seed)
rng.shuffle(tasks)
# Which condition goes first in each pair is BALANCED, then shuffled: an
# independent coin per task can put B first in every pair (the first run of
# this script, seed 20260928 on three tasks, drew exactly that).
firsts = [a.conditions, a.conditions[::-1]] * ((len(tasks) + 1) // 2)
firsts = firsts[:len(tasks)]
rng.shuffle(firsts)
order = [(t, c) for t, f in zip(tasks, firsts) for c in f]

lines = [f"# seed={a.seed} conditions={a.conditions} prompts={a.prompts}"]
lines += [f"{i}\t{t}\t{c}" for i, (t, c) in enumerate(order, 1)]
(a.out / "order.tsv").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
if a.dry_run:
    sys.exit(0)

failed = []
for i, (t, c) in enumerate(order, 1):
    print(f"[{i}/{len(order)}] {t} {c}", flush=True)
    rc = subprocess.call([str(HERE / "session.sh"), c,
                          str(a.out.resolve() / f"{t}.{c}"),
                          str((a.prompts / f"{t}.txt").resolve())])
    if rc:
        failed.append(f"{t}.{c}")
if failed:
    sys.exit(f"{len(failed)} session(s) failed: {failed}")
