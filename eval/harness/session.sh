#!/usr/bin/env bash
# session.sh — run ONE subject session, headless, from a fresh NEUTRAL directory.
#
#   session.sh <A|B> <out-basename> <prompt-file>
#
# Condition A = baseline (no plugin).  Condition B = the plugin under test.
# Writes <out-basename>.jsonl (the stream-json session log), .stderr, and .pre
# (what the neutral directory held before the session started).
#
# CONTAMINATION CONTROL. The session's cwd is a directory made by `mktemp -d`
# for this session alone, OUTSIDE any repository, so it has no CLAUDE.md, no
# .claude/, and an auto-memory path no earlier session can have written to.
# Run from inside a working copy instead and condition A silently inherits that
# project's skills and memory. `--setting-sources ""` drops user and project
# settings, account connectors are switched off (below), and the ONLY
# difference between the two conditions is the single --plugin-dir flag.
# audit.py then checks, per session, that this held.
#
# Env:
#   PLUGIN   plugin directory under test, pinned to a commit   (required for B)
#   MODEL    model alias or id                                  (default: opus)
#   TOOLS    tools granted to BOTH conditions                   (default: Skill,Read,Glob)
#   STRICT_MCP  1 = pass --strict-mcp-config (default). Set 0 when the plugin
#            under test ships its own MCP server, which strict mode would drop
#            from condition B; audit.py still fails any run whose sessions saw
#            different non-plugin servers.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="${MODEL:-opus}"
TOOLS="${TOOLS:-Skill,Read,Glob}"
STRICT_MCP="${STRICT_MCP:-1}"

[ $# -eq 3 ] || { echo "usage: session.sh <A|B> <out-basename> <prompt-file>" >&2; exit 2; }
COND="$1"; OUT="$2"; PROMPT_FILE="$3"

# The session runs from the neutral directory, so every caller-supplied path
# must be absolute before that cd happens.
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
case "$PROMPT_FILE" in /*) ;; *) PROMPT_FILE="$PWD/$PROMPT_FILE" ;; esac
[ -f "$PROMPT_FILE" ] || { echo "no such prompt file: $PROMPT_FILE" >&2; exit 2; }
[ -s "$PROMPT_FILE" ] || { echo "empty prompt file: $PROMPT_FILE" >&2; exit 2; }
[ -d "$(dirname "$OUT")" ] || { echo "no such output dir: $(dirname "$OUT")" >&2; exit 2; }

# Read+Glob are granted so a plugin can load its OWN bundled reference files
# (M2's q-knowledge delegates Python->q translation to a sibling file). Both
# conditions get the identical tool policy.
#
# Account connectors (claude.ai MCP servers) are NOT settings, so
# --setting-sources "" does not remove them, and --tools did not stop their
# tools either: in M2 one finished connecting in time for 3 of 15 condition-B
# sessions only. ENABLE_CLAUDEAI_MCP_SERVERS=false keeps them out, and
# --strict-mcp-config with no --mcp-config drops every other MCP source.
COMMON=(
  --model "$MODEL"
  --setting-sources ""
  --tools "$TOOLS"
  --allowedTools "$TOOLS"
  --output-format stream-json --verbose
  --no-session-persistence
)
[ "$STRICT_MCP" = 1 ] && COMMON+=(--strict-mcp-config)

# Condition B differs from A by exactly one flag. Appending to the non-empty
# COMMON array avoids bash 3.2's unbound-variable error on an empty array.
case "$COND" in
  A) ;;
  B) COMMON+=(--plugin-dir "${PLUGIN:?set PLUGIN to the plugin directory under test}") ;;
  *) echo "bad condition: $COND" >&2; exit 2 ;;
esac

# Up to 3 attempts. A transient API error yields a result line with is_error
# true or an "API Error" result string; that must not be scored as a bad answer.
# Every attempt gets its own fresh directory: a failed attempt leaves nothing
# for the next one to find.
for attempt in 1 2 3; do
  NEUTRAL="$(mktemp -d "${TMPDIR:-/tmp}/atq-neutral.XXXXXX")" || exit 2
  NEUTRAL="$(cd "$NEUTRAL" && pwd -P)"     # the path Claude Code will report as cwd
  # Claude Code keys auto-memory on the cwd: non-alphanumerics become '-'.
  MEMORY="$HOME/.claude/projects/$(printf %s "$NEUTRAL" | sed 's/[^A-Za-z0-9-]/-/g')/memory"
  {
    echo "condition: $COND  attempt: $attempt  started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "claude: $(claude --version 2>&1)"
    echo "neutral cwd: $NEUTRAL"
    ls -la "$NEUTRAL"
    echo "auto-memory: $MEMORY"
    if [ -e "$MEMORY" ]; then ls -la "$MEMORY"; else echo "(absent)"; fi
    echo "user CLAUDE.md: $([ -e "$HOME/.claude/CLAUDE.md" ] && echo present || echo absent)"
  } > "$OUT.pre"
  if [ -e "$MEMORY" ] && [ -n "$(ls -A "$MEMORY")" ]; then
    echo "auto-memory for a fresh directory is not empty: $MEMORY" >&2; exit 2
  fi
  # Claude Code also reads CLAUDE.md (and, through its agents-md built-in,
  # AGENTS.md) from every parent of the cwd, and the init record does not list
  # what it read, so a TMPDIR inside a project would leak that project's
  # guidance into both conditions unseen. Refuse to run there.
  # ($HOME/.claude is Claude Code's own config directory, not project guidance.)
  up="$NEUTRAL"; found=""
  while [ "$up" != "/" ]; do
    up="$(dirname "$up")"
    [ -e "$up/CLAUDE.md" ] && found="$found $up/CLAUDE.md"
    [ -e "$up/AGENTS.md" ] && found="$found $up/AGENTS.md"
    [ -e "$up/.claude" ] && [ "$up" != "$HOME" ] && found="$found $up/.claude"
  done
  echo "project guidance above the neutral cwd: ${found:-none}" >> "$OUT.pre"
  if [ -n "$found" ]; then
    rm -rf "$NEUTRAL"
    echo "neutral directory sits under project guidance:$found (set TMPDIR elsewhere)" >&2; exit 2
  fi

  ( cd "$NEUTRAL" && ENABLE_CLAUDEAI_MCP_SERVERS=false \
      claude -p "$(cat "$PROMPT_FILE")" "${COMMON[@]}" \
      < /dev/null > "$OUT.jsonl" 2> "$OUT.stderr" )
  rm -rf "$NEUTRAL"
  if python3 "$HERE/ok.py" "$OUT.jsonl"; then
    exit 0
  fi
  echo "  retry $attempt: $OUT" >&2
  sleep 5
done
echo "FAILED after 3 attempts: $OUT" >&2
exit 1
