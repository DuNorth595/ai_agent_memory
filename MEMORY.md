# MEMORY.md

**This is the index — a table of contents, not a journal.**

If a fact needs more than one line here, it belongs in a file under
`library/` and this file gets a pointer to it. See `docs/WRITING.md`.

---

## Read order

**Cold-start:** `MEMORY.md` → `library/operating/RULES.md` →
`library/operating/SELF.md` → `library/INDEX.md` → the file inside.

This file is in context every turn. Everything it points at is read on
demand.

## Standing rules

Operating discipline — read before acting. See
`library/operating/RULES.md`.

Archive before overwrite; never `rm` a memory file. See
`library/operating/RULES.md` §2.

Read the target before writing it, every time. See
`library/operating/RULES.md` §1.

If you can't verify something, say so. Don't fabricate. See
`library/operating/RULES.md` §7.

## Identity and environment

Who the agent is, what it values, what it won't do. See
`library/operating/SELF.md`.

Machine-specific facts — paths, ports, quirks, tooling. See
`library/operating/ENVIRONMENT.md`.

The full project map. See `library/operating/PROJECTS_INDEX.md`.

## Current state

Active task, open loops, priorities, breakthroughs. See
`library/state/CURRENT_STATE.md` and `library/state/OPEN_LOOPS.md`.

## History

Daily logs — append-only, one per day, written as the day unfolds. See
`library/log/INDEX.md`.

Significant incidents — postmortems, decisions, security events, dated
and slugged. See `library/events/INDEX.md`.

Chronological log of significant session events. See
`library/operating/SESSION_LOG.md`.

## People

One file per person the agent knows. See `library/people/INDEX.md`.

## Maintenance

Writing memory files that stay useful. See `docs/WRITING.md`.

Naming, headers, frontmatter, layout. See `docs/CONVENTIONS.md`.

Installing the library. See `docs/SETUP.md`.

Health checks and audit cadence. See `docs/ARCHITECTURE.md`.

---

**Budget:** 2,000 chars target, 4,000 hard ceiling. Over target, move
content into `library/` and leave a pointer.
