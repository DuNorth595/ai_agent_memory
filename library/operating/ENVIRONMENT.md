---
title: Environment
date: 2026-01-01
type: note
status: active
tags: [environment, infrastructure]
---

# Environment

**Purpose:** Machine-specific facts — paths, ports, quirks, tooling.
**Owner:** <owner>
**Last updated:** 2026-01-01

This file is the answer to "how do I actually run things here?" If a
tool has a non-obvious invocation, it goes here.

---

## Machine

- **Host:** <hostname>
- **OS:** <os + version>
- **Shell:** <shell>
- **Home:** `~`

## Paths

| What | Path |
|---|---|
| Memory library | `<absolute path>` |
| Agent config | `<path>` |
| Secrets | `<path>` — never read these into context |
| Logs | `<path>` |

## Ports

| Service | Port | Bind | Notes |
|---|---|---|---|
| `<service>` | `<port>` | `<bind>` | <notes> |

## Tooling

| Tool | How to run it | Gotcha |
|---|---|---|
| `<tool>` | `<command>` | <the thing that bites> |

**Always use the project's own interpreter.** A system Python often
lacks the dependencies and fails in confusing ways.

```bash
# The right way:
<command>

# The wrong way:
<wrong command> — <why>
```

## Gotchas

Things that have already cost time. Write them down the day you learn
them, not the week later.

### <Short title>

**Symptom:** <what you see>

**Cause:** <what's actually happening>

**Fix:** <what to do>

---

**Updating this file:** environment facts change. When one does, update
the `Last updated` date and consider whether anything in `RULES.md` or
the project files needs to change with it.
