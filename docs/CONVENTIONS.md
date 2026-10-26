# CONVENTIONS — naming, headers, format

The mechanical details. [WRITING.md](WRITING.md) covers *how* to write;
this covers *what the files look like*.

---

## File naming

| Kind | Pattern | Example |
|---|---|---|
| Daily log | `YYYY-MM-DD.md` | `2026-03-15.md` |
| Daily log (multiple per day) | `YYYY-MM-DD-slug.md` | `2026-03-15-what-changed.md` |
| Event | `YYYY-MM-DD_snake_slug.md` | `2026-03-15_gateway_restart.md` |
| Project directory | `snake_case/` | `voice_bridge/` |
| Project file | `snake_case.md` | `voice_bridge/architecture.md` |
| Person | `lowercase.md` | `justin.md` |
| State file | `UPPER_SNAKE.md` | `CURRENT_STATE.md` |
| Archive directory | `YYYY-MM-DD_snake_slug/` | `2026-03-15_memory-redesign/` |
| Rule | `UPPER_SNAKE.md` | `RULES.md` |

**Rules:**

- Dates are `YYYY-MM-DD`. Always. No `March 15` or `03/15`.
- Slugs are `snake_case` — lowercase, underscores, no spaces.
- The date prefix sorts correctly with `ls` and `glob`.
- No version numbers in filenames. Versioning is a frontmatter field
  and an archive directory, not a filename suffix.

---

## Directory layout

```
library/
├── INDEX.md                 ← master index, points at each chapter
├── operating/
│   ├── INDEX.md
│   ├── RULES.md             ← durable operating discipline
│   ├── SELF.md              ← identity
│   ├── ENVIRONMENT.md       ← machine facts
│   ├── PROJECTS_INDEX.md    ← the project map
│   ├── learning/            ← notes on what's been learned
│   │   └── INDEX.md
│   ├── research/            ← open research threads
│   │   └── INDEX.md
│   └── reflections/         ← the agent's own thinking
│       └── INDEX.md
├── people/
│   └── INDEX.md
├── projects/
│   └── INDEX.md
├── log/
│   └── INDEX.md
├── events/
│   └── INDEX.md
├── state/
│   └── INDEX.md
├── archive/
│   └── INDEX.md
└── scripts/
    └── INDEX.md
```

**Every directory has an `INDEX.md`.** Not every *file* directory —
every *chapter* directory. The chapter index is what makes the library
navigable without a filesystem search.

---

## Frontmatter

Every library file (not the index, not the chapter indices) carries it.

```yaml
---
title: Gateway restart loop
date: 2026-03-15
type: event
status: closed
tags: [hermes, launchd, incident]
---
```

### Fields

| Field | Required | Type | Notes |
|---|---|---|---|
| `title` | yes | string | Human-readable, sentence case |
| `date` | yes | date | `YYYY-MM-DD` — creation or last material change |
| `type` | yes | enum | See below |
| `status` | no | enum | See below |
| `tags` | no | list | Lowercase, free-form |

### `type` values

`project` · `person` · `event` · `log` · `rule` · `state` · `note`

### `status` values

| Value | Meaning |
|---|---|
| `live` | Actively running / in production |
| `active` | Being worked on right now |
| `paused` | Intentionally stopped, may resume |
| `closed` | Finished. Historical record. |
| `frozen` | Kept for reference, not changing |
| `draft` | Work in progress |

**`closed` on an event means "history, don't act on this."** It's the
field that stops an agent from trying to fix a bug that was already
fixed.

### Tag rules

- Lowercase
- No spaces — use hyphens
- Reuse tags. A tag that appears once is noise; a tag that appears
  across eight files is a category.

---

## The file header

After frontmatter:

```markdown
# Gateway restart loop

**Purpose:** Postmortem of the 2026-03-14 gateway restart loop.
**Owner:** Sam
**Last updated:** 2026-03-15
```

Three lines, always in that order. The `Last updated` line is what the
audit reads to find stale files — update it whenever you materially
change the file.

For files that never change, say so:

```markdown
**Last updated:** 2026-01-04 (static reference)
```

---

## Chapter index format

```markdown
# PROJECTS — chapter index

**Chapter root:** `library/projects/`
**Purpose:** One directory per project.
**Last updated:** 2026-10-18

---

## Files

| Project | What it is | Status |
|---|---|---|
| `voice_bridge/` | Mobile full-duplex voice UI | live |
| `radio_stack/` | Trunked radio control and monitoring | active |

---

**Open the project directory, not this file, when you want the
detail.** This is a map.
```

**Rules for chapter indices:**

- One line per entry
- The description is a *label*, not a summary
- Include the status column — it makes the map scannable
- End with a line saying it's a map, so the reader doesn't mistake it
  for the content

---

## The index (`MEMORY.md`)

The always-loaded pointer file. Three sections:

```markdown
# MEMORY.md

**This is the index. It is a table of contents, not a journal.**

## Read order
...

## <topic group>
See `path/to/file.md`.

---

**Budget:** 2,000 chars target, 4,000 hard ceiling.
```

**Rules:**

- One line per pointer
- No summaries — if you can say it in the pointer, it belongs in the
  file
- Group by topic with `##` headers
- Always include the read order at the top
- Always include the budget note at the bottom

---

## Cross-reference style

**Always a path. Never a description.**

```markdown
✅ See `library/operating/RULES.md` §2.
✅ See `library/events/2026-03-15_gateway_restart.md`.
❌ See the rules file for the archiving policy.
❌ See my notes about what went wrong last month.
```

A path is unambiguous and clickable. A description is a guess you hope
resolves.

When referencing a specific part of a file, name the section or
function:

```markdown
✅ `library/projects/voice_bridge/architecture.md` § "What's load-bearing"
✅ `barge.py` → `_BargeState.feed()`
```

---

## Dates and times

- **Dates:** `YYYY-MM-DD`. Always.
- **Times:** `HH:MM` local, with the timezone when it matters:
  `2026-03-15 14:32 CDT`
- **Relative dates** ("yesterday", "last week") are fine in a daily log.
  **Not** fine in an event file or a project file — by the time anyone
  reads it, "yesterday" is meaningless.
- **Never estimate a date.** If you're not sure when something happened,
  say "date unknown" or check. A wrong date in an archive directory name
  breaks the chronological ordering the whole system depends on.

---

## Markdown style

- **Headings** start at `#` for the title, `##` for sections.
- **Bold** for emphasis, sparingly.
- **Code fences** with a language tag for anything a reader might copy.
- **Tables** for genuinely tabular data. Not for prose.
- **Lists** `-` for unordered, `1.` for ordered.
- **Line length:** no hard limit. Wrap at ~80 for prose, not for code
  blocks, tables, or URLs.

---

## Shell scripts

In `library/scripts/` and `scripts/`:

- Start with `#!/bin/bash` (or `#!/usr/bin/env python3`)
- `set -e` in bash, unless there's a reason not to
- **Never hardcode an absolute path.** Use an environment variable with
  a sensible default:
  ```bash
  : "${MY_MEMORY_ROOT:=$(cd "$(dirname "$0")/.." && pwd)/library}"
  ```
- Quote every variable expansion
- `usage()` function for anything that takes arguments
- No `rm -rf` without a confirmation path

---

## Python scripts

- `#!/usr/bin/env python3`
- Standard library only, unless a dependency is documented in the README
- `argparse` for arguments
- Exit non-zero on failure — makes it CI-friendly
- Docstring at the top explaining what it does and how to run it

---

## Git conventions

- One logical change per commit
- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Never commit secrets
- `.env` and credential files are gitignored

---

## Related

- **[WRITING.md](WRITING.md)** — how to write the content
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — why the structure exists
- **[SETUP.md](SETUP.md)** — installing it
