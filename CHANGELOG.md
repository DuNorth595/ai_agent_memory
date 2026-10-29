# Changelog

All notable changes to **ai_agent_memory** are documented here. Format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); dates
are ISO 8601.

## [0.2.0] — 2026-10-29

Continuous checks on the library.

The library shipped its own health check — `scripts/audit_memory.py` —
and nothing ran it. A structure that rots needs the rot to be caught by
something other than a person remembering to look.

### Added

- **A CI workflow** that runs on every push and every pull request. It
  runs `audit_memory.py --check-links`, so a pointer to a file that has
  been renamed fails the build rather than lingering. It also checks that
  the maintenance scripts still run — a broken audit script is a broken
  product, and nobody notices until they need it — and that every file in
  the tree still carries its SPDX licence header.

### Changed

- The README's Auditing section now says the audit runs on every push,
  and shows the command CI runs.

### Removed

- The `feature/social-preview` branch. It was fully merged into `main`
  and served no open pull request.

## [0.1.0] — 2026-10-27

First tagged release.

### Added

- **The four-layer memory architecture.** A pointer index that stays small
  and always-on, a library of Markdown chapters, a chat transcript log, and
  a structured fact store. The index is a table of contents, not a
  journal.
- **`library/`** — the working structure: `INDEX.md` at the top, one
  pointer per topic, and everything else in plain Markdown files. No
  database required.
- **Conventions** (`docs/CONVENTIONS.md`), **architecture** notes
  (`docs/ARCHITECTURE.md`), **setup** (`docs/SETUP.md`), and **writing**
  guidance (`docs/WRITING.md`).
- **An archive pattern** (`library/archive/`) with a `RECOVERY_README.md`
  per archive, so retired material is kept with version control rather
  than deleted.
- **Event and log templates** — `library/events/EVENT_TEMPLATE.md` and
  `library/log/0.000000.md` — so the structure is obvious to a new reader.
- **A `MEMORY.md`** at the repo root: the pointer index, and the entry
  point for an agent that has never seen this repository before.

### Changed

- The README now opens in plain words rather than jargon, so the project
  is findable by someone searching for what it does.
- The social preview artwork was re-cropped so nothing is cut off.
