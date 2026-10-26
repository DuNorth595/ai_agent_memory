#!/bin/bash
# SPDX-FileCopyrightText: 2026 Justin Douglas
# SPDX-License-Identifier: MIT
#
# Append a timestamped note to today's daily log.
#
#   memory_note.sh "Fixed the barge-in threshold"
#
# Creates today's log with the standard section skeleton if it doesn't
# exist yet. Pure append — the log is never rewritten.

set -e

: "${MY_MEMORY_ROOT:=$(cd "$(dirname "$0")/../library" && pwd)}"

usage() {
    echo "usage: $(basename "$0") \"your note here\""
    exit 1
}

[ $# -lt 1 ] && usage
[ -z "$1" ] && usage

LOG_DIR="$MY_MEMORY_ROOT/log"
TODAY=$(date +%F)
FILE="$LOG_DIR/$TODAY.md"

mkdir -p "$LOG_DIR"

# First run in a fresh library? Make sure the index exists too.
# The index is normally copied from the repo root; this is a safety net
# so a half-installed library still has a pointer file.
INDEX_FILE="$MY_MEMORY_ROOT/../MEMORY.md"
if [ ! -f "$INDEX_FILE" ] && [ ! -f "$MY_MEMORY_ROOT/MEMORY.md" ]; then
    cat > "$MY_MEMORY_ROOT/MEMORY.md" <<'EOF'
# MEMORY.md

**This is the index — a table of contents, not a journal.**

If a fact needs more than one line here, it belongs in a file under
`library/` and this file gets a pointer to it.

---

## Read order

**Cold-start:** `MEMORY.md` → `library/operating/RULES.md` →
`library/operating/SELF.md` → `library/INDEX.md` → the file inside.

## Standing rules

Operating discipline — read before acting. See
`library/operating/RULES.md`.

---

**Budget:** 2,000 chars target, 4,000 hard ceiling.
EOF
    echo "[bootstrap] created MEMORY.md"
fi

if [ ! -f "$FILE" ]; then
    cat > "$FILE" <<EOF
# $TODAY

## Major Events

## Work Performed

## Findings

## Conversations

## Personal

## Open Loops

## Tomorrow
EOF
fi

echo "" >> "$FILE"
echo "- $(date +%H:%M) $*" >> "$FILE"

echo "[$(date '+%H:%M:%S')] $FILE"
