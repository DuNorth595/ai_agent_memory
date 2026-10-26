# Library — master index

**Purpose:** The long-form memory library. Organized into chapters.
**Owner:** <owner>
**Last updated:** 2026-01-01

---

## Cold-start read order

1. `MEMORY.md` (outside the library) — the always-on pointer index
2. `library/operating/RULES.md` — how to behave
3. `library/operating/SELF.md` — who the agent is
4. `library/state/CURRENT_STATE.md` — where things stand
5. The chapter index below for whatever the task touches
6. The file inside that chapter

**Steps 5 and 6 are the point of the chapter indices.** An agent should
answer "what do I know about X?" by reading one chapter index and one
file — not by grepping the library.

## Chapters

Each chapter has an `INDEX.md` listing every file with a one-line
description and status. **Open the chapter index when you want a map.**
Open the file inside when you want the content.

| Chapter | Path | What it is |
|---|---|---|
| **operating** | `operating/` | Rules, identity, environment, the project map, session log. Read on cold start. |
| **people** | `people/` | One file per person the agent knows. |
| **projects** | `projects/` | One directory per project — plans, decisions, research. |
| **log** | `log/` | Append-only daily logs, one per day. |
| **events** | `events/` | Significant incidents and decisions, dated and slugged. |
| **state** | `state/` | Current state, open loops, priorities, breakthroughs. |
| **archive** | `archive/` | Superseded versions. Never deleted. |
| **scripts** | `scripts/` | Maintenance helpers. |

## Where does a new file go?

| The fact is about | It goes in |
|---|---|
| A person | `people/<name>.md` |
| A project | `projects/<name>/` |
| A durable rule | `operating/RULES.md` |
| The agent's identity | `operating/SELF.md` |
| The machine | `operating/ENVIRONMENT.md` |
| A specific date or event | `events/<date>_<slug>.md` |
| Something that happened today | `log/<today>.md` |
| Where things stand right now | `state/` |
| A small active-context fact | A one-line pointer in `MEMORY.md` |

**If you're inventing a new location, stop.** The answer is usually
already here. See `docs/CONVENTIONS.md` for the full rules.

## Standing rules

- **Read before write.** Every time. Familiarity is not reading.
- **Archive before overwrite.** Never `rm` a memory file.
- **The index is a pointer index.** If it needs more than one line
  there, it belongs in a file.
- **Never fabricate.** If you can't verify it, say so.

Full text: `operating/RULES.md`.

## Audit cadence

- **Daily** — nothing. The write path keeps it healthy.
- **Weekly** — `scripts/audit_memory.py`, and re-read `operating/RULES.md`.
- **Monthly** — check `state/CURRENT_STATE.md` is still true.
- **On any redesign** — write an event file, archive the old structure,
  update the indices.

## Related

- `../MEMORY.md` — the always-on pointer index
- `../docs/WRITING.md` — how to write memory files
- `../docs/CONVENTIONS.md` — naming, headers, frontmatter
- `../docs/SETUP.md` — installing this in your own environment
- `../docs/ARCHITECTURE.md` — why it's shaped this way
