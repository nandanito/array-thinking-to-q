#!/usr/bin/env bash
# session.sh — run ONE eval subject session, headless, from a NEUTRAL directory.
#
#   session.sh <A|B> <out-basename> <prompt-file>
#
# Condition A = baseline (no plugin).  Condition B = KX q-knowledge plugin.
#
# CONTAMINATION CONTROL (eval/PLAN-M2.md §1). The session's cwd is $NEUTRAL — a
# scratch directory OUTSIDE this repository, with no CLAUDE.md and no .claude/.
# Run from inside the working copy instead and condition A silently inherits
# .claude/skills/idiomatic-q/SKILL.md — approximately the thing under test.
# `--setting-sources ""` additionally drops ~/.claude/settings.json, so the ONLY
# difference between the two conditions is the single --plugin-dir flag.
#
# Env:
#   NEUTRAL  scratch cwd for the session   (default: $TMPDIR/atq-eval-neutral)
#   KX       path to the q-knowledge plugin directory, checked out at the
#            pinned SHA (see eval/verdict.md)   (required for condition B)
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
NEUTRAL="${NEUTRAL:-${TMPDIR:-/tmp}/atq-eval-neutral}"
mkdir -p "$NEUTRAL"

COND="$1"; OUT="$2"; PROMPT_FILE="$3"

# The session runs with cwd = $NEUTRAL, so every caller-supplied path must be
# absolute before that cd happens.
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
[ -f "$PROMPT_FILE" ] || { echo "no such prompt file: $PROMPT_FILE" >&2; exit 2; }
[ -s "$PROMPT_FILE" ] || { echo "empty prompt file: $PROMPT_FILE" >&2; exit 2; }

# Read+Glob are allowed so condition B can load the plugin's OWN bundled
# reference files (skills/q/references/*.md). Without them the plugin is
# handicapped: its SKILL.md delegates Python->q translation to a sibling file.
# Both conditions get the identical tool policy.
COMMON=(
  --model opus
  --setting-sources ""
  --tools Skill,Read,Glob
  --allowedTools Skill Read Glob
  --output-format stream-json --verbose
  --no-session-persistence
)

# Condition B differs from A by exactly one flag. Appending to the non-empty
# COMMON array avoids bash 3.2's unbound-variable error on an empty array.
case "$COND" in
  A) ;;
  B) COMMON+=(--plugin-dir "${KX:?set KX to the q-knowledge plugin directory}") ;;
  *) echo "bad condition: $COND" >&2; exit 2 ;;
esac

cd "$NEUTRAL" || exit 2

# Up to 3 attempts. A transient API error yields a result line with is_error
# true or an "API Error" result string; that must not be scored as a bad answer.
for attempt in 1 2 3; do
  claude -p "$(cat "$PROMPT_FILE")" "${COMMON[@]}" \
    < /dev/null > "$OUT.jsonl" 2> "$OUT.stderr"
  if python3 "$HERE/ok.py" "$OUT.jsonl"; then
    exit 0
  fi
  echo "  retry $attempt: $OUT" >&2
  sleep 5
done
echo "FAILED after 3 attempts: $OUT" >&2
exit 1
