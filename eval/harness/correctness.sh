#!/usr/bin/env bash
# correctness.sh — recompute the `correctness` column of a results.csv from the
# committed candidate answers, and FAIL if the committed value disagrees.
#
#   Q=$HOME/.kx/bin/q eval/harness/correctness.sh            # the M2 study
#   TASKS=my/tasks ANSWERS=my/answers CSV=my/results.csv \
#     EXT=py RUN='python3 {}' eval/harness/correctness.sh    # any other task set
#
# Printing the scores is not enough: a stale or hand-edited results.csv has to
# break something, or the number in the article is only as good as the memory of
# whoever typed it. Exits nonzero on any mismatch, any missing golden or answer,
# and on setup failure.
#
# Applies exactly the rule in eval/README.md: the run must exit 0 AND write
# nothing to stderr AND stdout must match the golden. q exits 0 even after a
# script error (it drops to a prompt, then EOF exits), so the empty-stderr check
# — not the exit status — is what actually catches a failed run.
#
# Env (defaults are the M2 layout inside this repo):
#   TASKS    dir of <task>.expected goldens     (eval/tasks/q)
#   ANSWERS  dir of <task>.<A|B>.<EXT> answers  (eval/runs)
#   CSV      results.csv with task,condition,correctness,...  (eval/results.csv)
#   EXT      answer file extension              (q)
#   RUN      command template; {} is the answer  ("$Q {} -q")
#   INIT=1   write CSV from the recomputed scores instead of checking it, for a
#            new study's first pass (refuses to overwrite). Every later run
#            checks against it, so a hand edit to the column breaks the build.
#
# The candidate set is DERIVED: every golden in TASKS times conditions A and B.
# Nothing here knows how many tasks the study had.
#
# `set -e` is deliberately NOT used: the candidate run below is expected to fail
# for some answers and its status is captured, not fatal.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
Q=${Q:-q}
TASKS="${TASKS:-$REPO/eval/tasks/q}"
ANSWERS="${ANSWERS:-$REPO/eval/runs}"
CSV="${CSV:-$REPO/eval/results.csv}"
EXT="${EXT:-q}"
DEFAULT_RUN="$Q {} -q"          # inline in ${RUN:-...}, the placeholder's } would end it
RUN="${RUN:-$DEFAULT_RUN}"
case "$RUN" in *"{}"*) ;; *) echo "RUN must contain {} (the answer path): $RUN" >&2; exit 2 ;; esac

if [ "${INIT:-0}" = 1 ]; then
  [ -e "$CSV" ] && { echo "INIT=1 will not overwrite $CSV" >&2; exit 2; }
  echo "task,condition,correctness" > "$CSV"
fi
[ -f "$CSV" ] || { echo "missing $CSV" >&2; exit 2; }
[ -d "$TASKS" ] || { echo "missing task dir $TASKS" >&2; exit 2; }
[ -d "$ANSWERS" ] || { echo "missing answers dir $ANSWERS" >&2; exit 2; }
# Each answer runs from its own directory, so a relative path would not resolve
# there: every answer would "fail" with file-not-found, and INIT=1 would record
# those failures as scores (the first outside run did exactly that).
TASKS="$(cd "$TASKS" && pwd)"; ANSWERS="$(cd "$ANSWERS" && pwd)"
CSV="$(cd "$(dirname "$CSV")" && pwd)/$(basename "$CSV")"
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/atq-score.XXXXXX")" || { echo "cannot create a scratch dir" >&2; exit 2; }
trap 'rm -rf "$SCRATCH"' EXIT

# Every answer must have a golden, and every golden an answer per condition.
for cand in "$ANSWERS"/*."$EXT"; do
  [ -e "$cand" ] || continue
  base=$(basename "$cand" ".$EXT"); task=${base%.*}
  [ -f "$TASKS/$task.expected" ] || { echo "missing golden for $task" >&2; exit 2; }
done

n=0; fails=0; mismatches=0; missing=0
printf "%-26s %s %s %s  %s\n" task C ok csv reason
for exp in "$TASKS"/*.expected; do
  [ -e "$exp" ] || { echo "no goldens in $TASKS" >&2; exit 2; }
  task=$(basename "$exp" .expected)
  for cond in A B; do
    cand="$ANSWERS/$task.$cond.$EXT"
    if [ ! -f "$cand" ]; then
      echo "missing answer $task.$cond.$EXT" >&2; missing=$((missing+1)); continue
    fi
    # A fresh directory per answer: a file one answer writes cannot be read by
    # the next, so no answer can pass on another's leftovers.
    work="$(mktemp -d "$SCRATCH/$task.$cond.XXXXXX")"
    out="$work.out"; err="$work.err"
    cmd=(); for w in $RUN; do [ "$w" = "{}" ] && cmd+=("$cand") || cmd+=("$w"); done
    ( cd "$work" && "${cmd[@]}" < /dev/null > "$out" 2> "$err" )
    rc=$?
    if [ $rc -ne 0 ]; then
      reason="exit=$rc: $(head -c 100 "$err" | tr '\n' ' ')"; ok=0
    elif [ -s "$err" ]; then
      reason="stderr: $(head -c 100 "$err" | tr '\n' ' ')"; ok=0
    elif diff -q "$exp" "$out" > /dev/null 2>&1; then
      reason="-"; ok=1
    else
      reason="output differs"; ok=0
    fi

    [ "${INIT:-0}" = 1 ] && echo "$task,$cond,$ok" >> "$CSV"
    # What results.csv claims for this (task, condition).
    csv=$(awk -F, -v t="$task" -v c="$cond" \
          '$1==t && $2==c {print $3; found=1} END{if(!found) print "MISSING"}' "$CSV")
    n=$((n+1))
    [ "$ok" = 0 ] && fails=$((fails+1))
    flag=""
    if [ "$csv" != "$ok" ]; then mismatches=$((mismatches+1)); flag="  <-- MISMATCH"; fi
    printf "%-26s %s %s %s  %s%s\n" "$task" "$cond" "$ok" "$csv" "$reason" "$flag"
  done
done

echo
echo "$n candidates scored; correctness = 0 on $fails"
if [ "$missing" -ne 0 ]; then
  echo "$missing answer(s) missing for tasks that have a golden" >&2; exit 1
fi
if [ "$mismatches" -ne 0 ]; then
  echo "$mismatches row(s) disagree with results.csv" >&2; exit 1
fi
echo "results.csv correctness column matches all $n recomputed scores"
