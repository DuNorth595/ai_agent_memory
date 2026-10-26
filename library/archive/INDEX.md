# ARCHIVE — chapter index

**Chapter root:** `library/archive/`
**Purpose:** Superseded versions of everything. Never deleted.
**Last updated:** 2026-01-01

---

## Layout

```
archive/
└── YYYY-MM-DD_category/
    ├── <the old file, same name>
    └── RECOVERY_README.md    ← why it was archived, what replaced it
```

## Rules

1. **Never `rm` a memory file.** Archive it.
2. **Archive before a material overwrite** — more than a small addendum.
3. **Every archive directory gets a `RECOVERY_README.md`** explaining
   what changed, why, and what replaced it.
4. **The README is the point.** A directory of orphaned files with no
   explanation is just clutter with extra steps.

## Why archive at all?

A memory file records what was believed *at a time*. When a fact
changes, the interesting question isn't only "what's true now" — it's
"what did we believe before, and why did we change?"

An agent that can answer that is more useful than one that can only
state current truth, because it can reason about *why* decisions were
made.

Deleting the old version destroys that. It also destroys the ability
to recover when a change turns out to be wrong.

---

**Open the file, not this index, when you want the detail.** This is a map.
