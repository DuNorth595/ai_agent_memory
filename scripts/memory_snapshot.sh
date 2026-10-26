#!/bin/bash
# SPDX-FileCopyrightText: 2026 Justin Douglas
# SPDX-License-Identifier: MIT
#
# Append a periodic state snapshot to today's daily log.
#
#   memory_snapshot.sh
#
# Creates a fill-in-the-blanks block describing the agent's current
# state. Useful on a timer — it gives a breadcrumb trail of "what was
# the agent thinking at 3pm" without writing a full log entry.
#
# Set MY_MEMORY_ROOT to point at your library.

set -e

: "${MY_MEMORY_ROOT:=$(cd "$(dirname "$0")/../library" && pwd)}"

LOG_DIR="$MY_MEMORY_ROOT/log"
TODAY=$(date +%F)
FILE="$LOG_DIR/$TODAY.md"

mkdir -p "$LOG_DIR"

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

SNAPSHOT="
## Snapshot — $(date '+%Y-%m-%d %H:%M')

### Active Topic
(todo: fill in)

### Current Task
(todo: fill in)

### Unresolved Issue
(todo: fill in)

### Latest Findings
(todo: fill in)

### Current Goals
(todo: fill in)
"

echo "$SNAPSHOT" >> "$FILE"
echo "[SNAPSHOT] Written to $FILE"
