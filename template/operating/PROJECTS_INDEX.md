---
title: Projects index
date: 2026-01-01
type: note
status: active
tags: [projects, map]
---

# Projects index

**Purpose:** The map of every project, its state, and where its files live.
**Owner:** <owner>
**Last updated:** 2026-01-01

One row per project. The detail lives in the project's own directory.

---

## Active

| Project | What it is | State | Files |
|---|---|---|---|
| `<name>` | <one line> | live | `library/projects/<name>/` |

## Paused

| Project | What it is | State | Files |
|---|---|---|---|
| `<name>` | <one line> | paused | `library/projects/<name>/` |

## Closed

| Project | What it is | Closed | Files |
|---|---|---|---|
| `<name>` | <one line> | 2026-01-01 | `library/projects/<name>/` |

---

**Keeping this honest.** A project row should be removed or moved to
"Closed" when the work ends. A map full of dead entries is a map
nobody trusts.

**When a project becomes big enough to need its own directory**, make
it one — a directory per project, with `README.md` at its root.
