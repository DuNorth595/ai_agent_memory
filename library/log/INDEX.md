# LOG — chapter index

**Chapter root:** `library/log/`
**Purpose:** Append-only daily logs. One file per day.
**Last updated:** 2026-01-01

---

## Files

| File | Era | Notes |
|---|---|---|
| `0.000000.md` | Pre-init | Bootstrap placeholder. Leave in place; ignore. |

---

**Append-only.** A daily log that gets edited after the fact becomes a
summary, and summaries lose the texture that makes them useful months
later.

Write the day-of, not the day-after.

Append with:

```bash
scripts/memory_note.sh "what happened"
scripts/memory_append.sh DECISION "the decision and why"
```
