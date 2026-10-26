#!/bin/bash
# SPDX-FileCopyrightText: 2026 Justin Douglas
# SPDX-License-Identifier: MIT
#
# Append a typed event to today's daily log.
#
#   memory_append.sh DECISION "Switched to server-side endpointing"
#
# Types: DISCOVERY BLOCKER DECISION ERROR PLAN CONTEXT
#        BREAKTHROUGH FAILURE TASK USER_REQUEST
#
# Creates today's log with the standard section skeleton if it doesn't
# exist yet. Pure append — the log is never rewritten.

set -e

: "${MY_MEMORY_ROOT:=$(cd "$(dirname "$0")/../library" && pwd)}"

TYPES="DISCOVERY BLOCKER DECISION ERROR PLAN CONTEXT BREAKTHROUGH FAILURE TASK USER_REQUEST"

usage() {
    echo "usage: $(basename "$0") TYPE \"message\""
    echo "types: $TYPES"
    exit 1
}

[ $# -lt 2 ] && usage

TYPE="$1"
shift
MSG="$*"

[ -z "$TYPE" ] && usage
[ -z "$MSG" ] && usage

# Validate the type.
VALID=0
for t in $TYPES; do
    [ "$TYPE" = "$t" ] && VALID=1
done
[ "$VALID" -eq 1 ] || {
    echo "error: unknown type '$TYPE'"
    usage
}

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

STAMP=$(date '+%H:%M:%S')
echo "- [$STAMP] [$TYPE] $MSG" >> "$FILE"

echo "[$STAMP] [$TYPE] $MSG"
