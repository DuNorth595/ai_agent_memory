# SETUP — standing this up in your own environment

This walks through installing the memory library for an agent, from
nothing to a working system.

**Time:** about 20 minutes. **Difficulty:** copy files and edit two
paths.

---

## Before you start

You need:

- An agent that can **read files** and **run shell commands**
- A place to put the library (any directory on disk)
- A way to get a small file into context on every turn — most agent
  frameworks call this the "memory file", "system memory", or
  "context file"

You do **not** need: a database, an embedding model, a vector store, or
a specific framework.

---

## Step 1 — get the library

```bash
git clone https://github.com/DuNorth595/ai_agent_memory.git
cd ai_agent_memory
```

The repository has three things in it:

| Directory | What it is | Where it goes |
|---|---|---|
| `library/` | The memory structure itself | Wherever you keep memory |
| `scripts/` | Maintenance helpers | Wherever you keep scripts |
| `template/` | Starter files | Copied into `library/` |

---

## Step 2 — place the library

```bash
# Pick your location.
export MY_MEMORY_ROOT=~/my-agent-memory

mkdir -p "$MY_MEMORY_ROOT"
cp -R library/. "$MY_MEMORY_ROOT/"
```

You'll end up with:

```
~/my-agent-memory/
├── INDEX.md
├── operating/
├── people/
├── projects/
├── log/
├── events/
├── state/
├── archive/
└── scripts/
```

**Keep it in one place.** The whole design depends on the index being
able to point at files by relative path.

### If you'd rather keep it in the repo

```bash
cd ai_agent_memory
# just use ./library — it's already there
export MY_MEMORY_ROOT="$PWD/library"
```

That's fine for a single agent. For multiple agents, give each one its
own root — see [Sharing one library between agents](#sharing-one-library-between-agents).

---

## Step 3 — seed the operating files

The `template/` directory has working examples of everything. Copy them
over the empty files:

```bash
cp template/operating/RULES.md         "$MY_MEMORY_ROOT/operating/"
cp template/operating/SELF.md          "$MY_MEMORY_ROOT/operating/"
cp template/operating/ENVIRONMENT.md   "$MY_MEMORY_ROOT/operating/"
cp template/operating/PROJECTS_INDEX.md "$MY_MEMORY_ROOT/operating/"
```

Then **read them and make them yours.** These are the files that define
the agent's behavior, and they only work if they're specific.

`SELF.md` is the one to start with. It has prompts in it:

```markdown
## What I value
<!-- What does this agent care about? What does it find worth doing? -->

## What I won't do
<!-- Hard limits. These are the ones that matter most. -->
```

Fill those in before the first session. An agent with a generic
`SELF.md` behaves generically.

---

## Step 4 — wire up the index

Copy `MEMORY.md` into your agent's always-loaded memory location and
fix the paths.

**The paths in `MEMORY.md` are relative to the library root.** If your
library is at `~/my-agent-memory` and the index lives at
`~/.hermes/memories/MEMORY.md`, then a pointer like:

```markdown
See `library/operating/RULES.md` for operating discipline.
```

should become:

```markdown
See `~/my-agent-memory/operating/RULES.md` for operating discipline.
```

Two options:

**Option A — absolute paths.** Explicit, works everywhere, breaks if
you move the library.

**Option B — a variable the agent resolves.** Cleaner, but only works
if your framework supports variable expansion in the memory file.

Most agents are fine with absolute paths. Use them, and update them
when you move the library.

### What the index should look like when you're done

- A **read order** at the top (3–5 lines)
- One-line pointers grouped by topic
- A **budget note** at the bottom so future-you knows the rule

That's it. If it's longer than ~40 lines, you've started putting content
in the index.

---

## Step 5 — verify the agent can find things

Run one of these:

```bash
# Does the library exist and is the index sized right?
scripts/audit_memory.py --root "$MY_MEMORY_ROOT"

# Does the index point at files that exist?
scripts/audit_memory.py --root "$MY_MEMORY_ROOT" --check-links
```

Then start a session with your agent and ask it something that should
require memory:

> "What are your standing rules?"

If the agent answers from the index alone, it's working. If it says it
can't find them, the paths are wrong.

---

## Step 6 — make it a habit

Memory that's not written down didn't happen. Two habits make the
difference:

**During the session.** Append to the daily log as things happen. Not
at the end of the day — at the end of the day it's a summary, and
summaries lose the texture that makes them useful later.

```bash
scripts/memory_note.sh "Switched to server-side endpointing"
```

**At the end of significant work.** Write an event file, add a pointer
to the index if it's worth finding later.

```bash
cp template/events/EVENT_TEMPLATE.md \
   "$MY_MEMORY_ROOT/events/$(date +%F)_my_event.md"
```

---

## Step 7 — set up the audit

Run it weekly. Make it a cron job, a launchd agent, or just a
calendar reminder. The goal isn't to catch errors — it's to catch
**staleness**.

```bash
scripts/audit_memory.py --root "$MY_MEMORY_ROOT"
```

Exit code is non-zero when something needs attention, so it works as a
CI check too.

---

## Wiring it into specific frameworks

### Hermes

The `memory` tool loads `~/.hermes/memories/MEMORY.md` on every turn.
That's your index.

- Put the **index** in `~/.hermes/memories/MEMORY.md`
- Put the **library** wherever you like — `~/my-agent-memory` works
- Use the `memory` tool only for index pointers; write library files
  with `write_file`
- `fact_store` is the optional facts layer (Layer 4)

**Hermes has a hard limit on the index.** It's a character budget, not a
byte budget. Check the current limit before you fill it:

```bash
grep -r "MAX_SKILL_CONTENT_CHARS\|MEMORY.*LIMIT\|MEMORY_MAX" \
     ~/.hermes/hermes-agent/tools/ 2>/dev/null | head
```

### Claude Code

`CLAUDE.md` is loaded every session. Point it at the index:

```markdown
# Memory

My memory index is at ~/my-agent-memory/MEMORY.md.
Read it first, then follow its read order.
```

Claude Code also has a skills system — that's a natural fit for
*procedures* (how to do things), as opposed to this library's
*content* (what's known).

### OpenAI Agents SDK / any custom framework

1. Load `MEMORY.md` into the system prompt
2. Give the agent a file-read tool scoped to the library root
3. Give it a file-write tool with the same scope
4. Have it shell out to `scripts/memory_note.sh` for daily logs, or
   append directly

---

## Sharing one library between agents

Two agents writing to the same file is a conflict. Two agents *reading*
shared files is fine.

```
~/my-agent-memory/
├── shared/                    ← both agents read
│   ├── operating/
│   └── people/
├── agents/
│   ├── writer/
│   │   ├── MEMORY.md         ← writer's own index
│   │   └── state/
│   └── researcher/
│       ├── MEMORY.md         ← researcher's own index
│       └── state/
```

Each agent gets its own index and its own writable chapters. The
shared chapters are read-only for both.

---

## Troubleshooting

**The agent says it can't find the memory.**
The index is loaded but the paths are wrong. Absolute paths that
include the library root are the fix.

**The index is over budget.**
Move content out of the index into the library. The index should be
pointers only. Run `audit_memory.py` to find the biggest offenders.

**The library feels stale.**
Set `Last updated` in file headers and check it in the audit. If
everything's a year old, either write more often or archive what
you're not using.

**Two files contradict each other.**
Pick one. Archive the other. Write an event file saying which won and
why. Don't leave both live — the agent will pick whichever it reads
last.

**The agent keeps re-asking for things it should remember.**
The fact is in a library file but nothing points to it. Add a pointer
to the index, or fix the chapter index so the file is discoverable.

---

## Next

- **[WRITING.md](WRITING.md)** — how to write memory files that stay useful
- **[CONVENTIONS.md](CONVENTIONS.md)** — naming, headers, frontmatter
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — why it's shaped this way, and how to audit it
