#!/usr/bin/env bash
# correctness.sh — recompute the `correctness` column of eval/results.csv from
# the committed candidate answers, and FAIL if the committed value disagrees.
#
#   Q=$HOME/.kx/bin/q eval/harness/correctness.sh
#
# Printing the scores is not enough: a stale or hand-edited results.csv has to
# break something, or the number in the article is only as good as the memory of
# whoever typed it. Exits nonzero on any mismatch, any missing golden, and on
# setup failure.
#
# Applies exactly the rule in eval/README.md: q must exit 0 AND write nothing to
# stderr AND stdout must match the golden. q exits 0 even after a script error
# (it drops to a prompt, then EOF exits), so the empty-stderr check — not the
# exit status — is what actually catches a failed run.
#
# `set -e` is deliberately NOT used: the q invocation below is expected to fail
# for some candidates and its status is captured, not fatal.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
Q=${Q:-q}
WORK="${WORK:-${TMPDIR:-/tmp}/atq-eval-score}"
mkdir -p "$WORK" || { echo "cannot create work dir $WORK" >&2; exit 2; }

CSV="$REPO/eval/results.csv"
[ -f "$CSV" ] || { echo "missing $CSV" >&2; exit 2; }

n=0; fails=0; mismatches=0
printf "%-26s %s %s %s  %s\n" task C ok csv reason
for cand in "$REPO"/eval/runs/*.q; do
  base=$(basename "$cand" .q)          # NN-name.A
  task=${base%.*}; cond=${base##*.}
  exp="$REPO/eval/tasks/q/$task.expected"
  [ -f "$exp" ] || { echo "missing golden for $task" >&2; exit 2; }
  out="$WORK/$base.out"; err="$WORK/$base.err"
  ( cd "$WORK" && "$Q" "$cand" -q < /dev/null > "$out" 2> "$err" )
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

  # What results.csv claims for this (task, condition).
  csv=$(awk -F, -v t="$task" -v c="$cond" \
        '$1==t && $2==c {print $3; found=1} END{if(!found) print "MISSING"}' "$CSV")
  n=$((n+1))
  [ "$ok" = 0 ] && fails=$((fails+1))
  flag=""
  if [ "$csv" != "$ok" ]; then mismatches=$((mismatches+1)); flag="  <-- MISMATCH"; fi
  printf "%-26s %s %s %s  %s%s\n" "$task" "$cond" "$ok" "$csv" "$reason" "$flag"
done

echo
echo "$n candidates scored; correctness = 0 on $fails"
if [ "$n" -ne 30 ]; then
  echo "expected 30 candidates (15 tasks x 2 conditions), found $n" >&2; exit 1
fi
if [ "$mismatches" -ne 0 ]; then
  echo "$mismatches row(s) disagree with results.csv" >&2; exit 1
fi
echo "results.csv correctness column matches all $n recomputed scores"
