# ARCHITECTURE — why it's shaped this way

This explains the reasoning behind the structure. If you're only
implementing it, read [SETUP.md](SETUP.md) and
[WRITING.md](WRITING.md). If you want to understand why the rules are
the rules, read this.

---

## The problem being solved

An LLM agent has no state between sessions. Every turn starts from
nothing. This creates two failure modes that pull in opposite
directions:

**Failure mode A — forget everything.** The agent doesn't write things
down, so it re-asks the same questions, re-discovers the same facts,
and repeats the same mistakes. On a long-running project this is
exhausting for the user and it makes the agent feel disposable.

**Failure mode B — remember everything, load everything.** The agent
writes everything down and loads the whole thing into every prompt.
Now it's slow, expensive, and the important stuff is drowned in the
noise. Worse, old information sits next to new information with equal
visual weight, and the model treats a stale note as current truth.

The architecture is the balance point between those two.

---

## The core trade: index vs. library

Everything follows from one decision: **separate the index from the
content.**

| | Index (`MEMORY.md`) | Library (`library/`) |
|---|---|---|
| Loaded | Every turn | On demand |
| Size | 2,000 chars target | Unlimited |
| Structure | Flat pointer list | Chapters, files, directories |
| Edited by | The agent, frequently | The agent, selectively |
| Format | Strict | Flexible per type |
| Purpose | Answer "where is it?" | Answer "what is it?" |

If you collapse these into one, you get either a bloated index or a
library that has to be searched every time. Keeping them separate is
what makes both work.

### Why the index size limit is the load-bearing rule

The index is in every prompt. Every character in it is paid for on
every single request, forever. A 2,000-character index costs about 500
tokens — cheap enough to keep always-on, small enough that it doesn't
crowd out the conversation.

The library is free. Reading a 40,000-character file costs 10,000
tokens, but only when you open it.

This asymmetry is the whole design. It means **memory can grow without
cost until someone actually needs to recall it.**

### Why the limit has a hard ceiling

At some point the index is no longer a pointer list — it's a summary,
and summaries are worse than pointers because they drift. The moment
someone writes "RULES §2: archive before overwrite" in the index
*instead of* just pointing at RULES, there are two copies of the rule
and one of them will be wrong.

**The fix for an oversized index is never deletion.** It's moving
content into the library and leaving a pointer.

---

## The four layers

### Layer 1 — the index

Always in context. One pointer per topic. Nothing else.

The test for membership is blunt: *if it needs more than one line here,
it belongs in a file.*

### Layer 2 — the library

The long-form memory. Organized into chapters so that "find the right
file" is a two-step operation (chapter index → file) rather than a
filesystem-wide search.

**Why chapters?** Because a flat directory of 5,000 files is
unsearchable by an agent that doesn't want to list the whole directory.
A chapter index — a table listing each file with a one-line
description — is small enough to read completely, so the agent can
scan it and pick the right file without opening anything else.

That's the same principle as the index itself, applied one level down:
**a map that points at content, at every scale.**

### Layer 3 — transcripts

Raw conversation history. The "I remember bits and pieces from three
weeks ago" layer.

This is deliberately not curated. Curating transcripts is expensive and
usually not worth it — the library's job is to be the *summary* that
makes transcripts findable. When you remember something from a
transcript, it should be because it was important enough to write down
properly.

### Layer 4 — structured facts

Typed, entity-linked facts in SQLite, for queries that span entities:
"everything about project X", "what do we know about person Y."

**This layer is optional and most systems should skip it initially.**
File-based memory handles the common case. Facts earn their place
when you find yourself wanting relational queries over the whole
library, which files are bad at.

It also introduces a real cost: facts become a parallel copy of the
library, and the two drift. If you add facts, decide which is
authoritative. In this design the library is authoritative and facts
are a derived index.

---

## Why chapters map to these specific buckets

### `operating/` — the agent's constitution

Rules, identity, environment, and the project map. These change rarely
and are read on every cold start.

Separated from the rest because it has a different **read frequency**:
`operating/RULES.md` gets read every session; `projects/whatever/` gets
read when relevant. Mixing them means the hot path is buried in cold
files.

### `people/` — one file per person

People are the highest-value, highest-sensitivity memories. One file
per person means:

- A single file to read for "what do you know about X"
- A single file to delete or redact
- No risk of one person's details leaking into another's

### `projects/` — one directory per project

Projects accumulate the most material — plans, decisions, research,
code. A directory per project means a project can be moved, archived,
or deleted as a unit, and a project's history stays together.

### `log/` — append-only daily logs

The texture layer. One file per day, written as the day unfolds.

**Append-only is a feature, not laziness.** A daily log that's edited
after the fact becomes a summary, and summaries lose the details that
make them useful three months later. The append-only constraint
preserves the texture for free.

The format is deliberately loose. `- [14:32] [DECISION] ...` is enough.

### `events/` — significant incidents

The promoted layer. A day produces log entries; some days produce
*events* — postmortems, architecture decisions, security incidents.
These are dated, slugged, and pointed at from the index, because they're
worth finding later by name.

The promotion rule is simple: **if you'd want to find this in six
months, it's an event.**

### `state/` — current state

Where am I right now? Active task, open loops, priorities, recent
breakthroughs.

This is the only chapter that's *rewritten* rather than appended to.
It exists so the agent can orient itself in one file read. It's
deliberately volatile — it's a snapshot, not a record.

### `archive/` — old versions, never deleted

Every material overwrite leaves the old version here.

**Why archiving matters more than it looks.** A memory file records
what was believed *at a time*. When a fact changes, the interesting
question isn't just "what's true now" — it's "what did we believe
before, and why did we change?" An agent that can answer that is
demonstrably more useful than one that can only state current truth,
because it can reason about why decisions were made.

Deleting the old version destroys that. And it destroys the ability to
recover when a change turns out to be wrong.

---

## The three rules, and why each exists

### Rule 1 — the index is a pointer index, not a journal

**Prevents drift.** Every paraphrase in the index is a second copy of a
fact. Copies drift. The index would then contain a stale version of a
rule that the agent still cites while the real file says something
different.

**Prevents bloat.** The one-line test is a hard constraint. It forces
"where do I put this?" to have a real answer.

### Rule 2 — read before write, every time

**Prevents data loss.** You don't know what's in a file you haven't
read. You don't know if it changed since you last looked. An agent that
overwrites from memory loses whatever it forgot to read.

This is the rule agents break most often, because the file *looks*
familiar. Familiarity is not reading.

### Rule 3 — archive before overwrite

**Preserves the history of belief.** See the `archive/` section above.

**Makes changes reversible.** An agent that archives first can always
undo. One that doesn't can only hope.

---

## The write path and why it's shaped that way

```python
# 1. Read the target first. Always.
# 2. If materially changing it, archive the current version.
# 3. Write the new version.
# 4. If it should be findable from the index, add ONE pointer line.
```

**Why step 4 is "add a pointer" and not "update the pointer."** If a
pointer already exists and still points at the right place, there's
nothing to do. Most writes don't change what a pointer says — they
change what's *inside* the file the pointer points at. That's the whole
point of the separation.

**Why "materially changing" and not "any change."** Archiving every
typo fix creates noise in the archive and makes it useless. The
threshold is judgment: if the old version taught something the new one
doesn't, archive it.

---

## The recall path and why order matters

```
1. Index        (already in context — free)
2. Chapter index (small, tells you which file)
3. The file
4. Transcripts  (only if the library doesn't have it)
5. Facts        (only if you need a cross-entity query)
```

Starting at step 4 — grepping the whole library — is the common
mistake. It returns 200 hits and teaches you nothing. Each step down
the chain costs more context and returns less, so you should only
descend when the previous step actually failed.

---

## Scaling

| Library size | Behavior |
|---|---|
| < 100 files | Works as-is. One chapter index per chapter is plenty. |
| 100–1,000 files | Chapter indices become essential. This is where the design starts paying off. |
| 1,000–10,000 files | Consider splitting `projects/` into sub-chapters by domain. |
| > 10,000 files | The index is still fine; you need better chapter indices. Build them from frontmatter. |

**The index never grows with the library.** That's the invariant. A
system where the index grows with the library has failed.

---

## What this design deliberately doesn't do

**No vector database.** Semantic retrieval is genuinely useful for
large document corpora, but it makes memory un-inspectable. You can't
git-diff it, hand-edit it, or explain it. For an agent's own memory —
which is a known, bounded set of facts — structured files with good
indices beat fuzzy similarity.

**No automatic summarization of transcripts.** It produces plausible
prose that drifts from the truth. Humans and agents writing summaries
explicitly is slower and more accurate.

**No timestamps on everything.** Timestamps are useful for logs and
events. Adding them to stable reference files creates noise. The
`Last updated` header is enough.

**No centralized config.** The library root is the config. One
environment variable, one directory, no manifest to drift.

---

## Auditing

Memory libraries rot in predictable ways. The `audit_memory.py` script
detects the mechanical failures; the rest is a human habit.

| Rot | Detection | Fix |
|---|---|---|
| Index bloat | Size check | Move content to library |
| Orphan files | Cross-reference index → files | Add pointer or remove |
| Stale pointers | Link check | Fix or remove |
| Missing archives | Archive dir without a `RECOVERY_README.md` | Archive properly |
| Staleness | `Last updated` header | Review or mark frozen |
| Contradiction | Manual | Pick one, archive the other, note the change |

### Cadence

- **Daily** — nothing. The write path keeps it healthy.
- **Weekly** — run `audit_memory.py`. Read your own rules.
- **Monthly** — read `state/CURRENT_STATE.md` and check it's still true.
- **On any redesign** — write an event file describing what changed and
  why, archive the old structure, update the indices.

**The most valuable audit isn't automated.** Reading your own rules
every few weeks and asking "would I still follow this?" catches the
failures no script can see: rules you stopped believing, values that
drifted, projects that quietly died.

---

## Related

- **[SETUP.md](SETUP.md)** — installing it
- **[WRITING.md](WRITING.md)** — how to write the files
- **[CONVENTIONS.md](CONVENTIONS.md)** — the mechanical details
