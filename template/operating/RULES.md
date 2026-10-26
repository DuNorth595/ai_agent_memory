---
title: Operating rules
date: 2026-01-01
type: rule
status: active
tags: [rules, discipline]
---

# Operating rules

**Purpose:** The durable rules this agent follows. Read on cold start.
**Owner:** <owner>
**Last updated:** 2026-01-01

Replace every `<...>` prompt below. A rules file full of placeholders
is a rules file that teaches nothing.

---

## §1 — Read before write

Read the target file immediately before writing it. Every time.

You don't know what's in a file you haven't read, and it may have
changed since you last looked. Familiarity is not reading.

This includes: files you wrote earlier in this session, files you wrote
in a session three days ago, files you just skimmed.

## §2 — Archive before overwrite

When changing a file materially — more than a small addendum — copy the
current version into `library/archive/<YYYY-MM-DD>_<slug>/` first.

Never `rm` a memory file. Archive it. Memory that's wrong is still
memory: it records what was believed and when.

## §3 — The index is a pointer index

If a fact needs more than one line in the index, it belongs in a file
under `library/` and the index gets a pointer to it.

Pointers don't drift. Summaries do.

## §4 — Never fabricate

If you can't verify something, say so. Don't guess, don't infer from
thin air, don't present a plausible answer as a known one.

A wrong answer delivered confidently is worse than an honest gap.

## §5 — Write down the decision, not just the outcome

The code shows *what*. Only memory shows *why*.

Record what was tried, what was rejected, and what the rejection was
based on. Six months later this is the difference between an agent
that understands the system and one that has to rediscover it.

## §6 — One agent, one job

<Add your own rules here. Number them. Reference them by number from
the index: "See `library/operating/RULES.md` §6.">

## §7 — Put it where it belongs

| The fact is about | It goes in |
|---|---|
| A person | `library/people/<name>.md` |
| A project | `library/projects/<name>/` |
| A durable rule | `library/operating/RULES.md` |
| A specific date or event | `library/events/<date>_<slug>.md` |
| Something that happened today | `library/log/<today>.md` |
| Current state | `library/state/` |
| A small active-context fact | A one-line pointer in `MEMORY.md` |

If you're inventing a new location, stop and re-read this table. The
answer is usually already here.

---

**Adding a rule:** append it with the next number, update the
`Last updated` date, and add a pointer to the index only if it needs
to be findable without reading the whole file.
