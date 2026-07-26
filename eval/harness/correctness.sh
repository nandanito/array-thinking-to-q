#!/usr/bin/env bash
# correctness.sh — score every candidate in eval/runs/ against its golden.
#
#   Q=$HOME/.kx/bin/q eval/harness/correctness.sh
#
# Applies exactly the rule in eval/README.md: q must exit 0 AND write nothing to
# stderr AND stdout must match the golden. q exits 0 even after a script error
# (it drops to a prompt, then EOF exits), so the empty-stderr check — not the
# exit status — is what actually catches a failed run.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
Q=${Q:-q}
WORK="${WORK:-${TMPDIR:-/tmp}/atq-eval-score}"
mkdir -p "$WORK"

fails=0
printf "%-26s %s %s  %s\n" task C ok reason
for cand in "$REPO"/eval/runs/*.q; do
  base=$(basename "$cand" .q)          # NN-name.A
  task=${base%.*}; cond=${base##*.}
  exp="$REPO/eval/tasks/q/$task.expected"
  out="$WORK/$base.out"; err="$WORK/$base.err"
  ( cd "$WORK" && "$Q" "$cand" -q < /dev/null > "$out" 2> "$err" )
  rc=$?
  if [ $rc -ne 0 ]; then
    reason="exit=$rc: $(head -c 120 "$err" | tr '\n' ' ')"; ok=0
  elif [ -s "$err" ]; then
    reason="stderr: $(head -c 120 "$err" | tr '\n' ' ')"; ok=0
  elif diff -q "$exp" "$out" > /dev/null 2>&1; then
    reason="-"; ok=1
  else
    reason="output differs"; ok=0
  fi
  [ "$ok" = 0 ] && fails=$((fails+1))
  printf "%-26s %s %s  %s\n" "$task" "$cond" "$ok" "$reason"
done
echo "correctness = 0 on $fails of $(ls "$REPO"/eval/runs/*.q | wc -l | tr -d ' ') candidates"
