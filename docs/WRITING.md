# WRITING — how to write memory that stays useful

Memory files have a shelf life. A good one is still accurate and still
findable six months later. Most aren't. The difference is almost
entirely in how they were written.

---

## The failure mode this prevents

Here's a memory file that will be useless in three months:

```markdown
# Voice Bridge

The voice bridge is a web app that lets you talk to the agent. It uses
FastAPI and runs on port 8770. I set it up because the old PTT version
was annoying. There were some issues with the barge-in detector and we
changed the thresholds a few times. Probably should check on it. The
mobile version needs Tailscale I think? Ask Sam.
```

Every problem with it:

- **No date.** Can't tell if it's current.
- **No structure.** Where's the config? The known bugs? The decision?
- **Vague cross-references.** "Ask Sam" — future-you can't.
- **A summary, not content.** Nothing here tells you *what to do*.
- **Already contradicts itself** ("I think?").

Now the version that survives:

```markdown
---
title: Voice bridge
date: 2026-03-02
type: project
status: live
tags: [voice, duplex, tailscale]
---

# Voice bridge

**Purpose:** Mobile voice UI for the agent. Full-duplex with barge-in.
**Owner:** Sam
**Last updated:** 2026-10-18

## How to reach it

`https://<tailnet-host>:8770/` over Tailscale. Plain HTTP won't work —
iOS Safari requires trusted HTTPS for microphone access.

## What's load-bearing

- One reader owns the WebSocket for the whole duplex session.
  Per-turn readers break barge-in.
- `barge_stop` ends the utterance, not the session.

## Known issues

- Long replies can hit the WebSocket ping timeout. Fixed by
  `ws_ping_timeout=None` + keepalive frames.
- See `library/events/2026-03-14_voice_barge_in_fix.md`.

## Decisions

- 2026-03-02 — Chose server-side endpointing over client-side silence
  detection. Client timers fire early on short utterances.
```

---

## Six rules for writing memory files

### 1. Write for the reader who knows nothing

The reader is an agent with no context, six weeks from now. It knows
the pointer in the index and nothing else.

That means:
- Expand the acronym. "STT" → "speech-to-text (STT)"
- Name the file paths absolutely.
- Say *why*, not just *what*.
- Don't say "as discussed." Nothing was discussed in the reader's
  context.

### 2. Lead with what the reader needs first

Front-load. The reader will often stop reading after the first screen.

```markdown
# Radio stack

**Purpose:** Trunked radio control and monitoring for the local repeater.
**Owner:** Sam
**Last updated:** 2026-10-18

## Current state

Working. Radio in service, FNE healthy. Last incident was the
dvmhost DUID mismatch — see `library/events/2026-10-19_dvmhost_duid.md`.

## How to reach it
...
```

The reader who needs "is it broken right now?" gets their answer in the
first three lines.

### 3. Every fact gets a location

Not the fact itself — the location.

```markdown
The threshold logic is in `barge.py`, function `_BargeState.feed()`.
```

`barge.py` alone is ambiguous in a library with 300 files. The
function name isn't. And a path in a *different* file is a pointer —
the reader opens that file rather than trusting the summary.

### 4. Date-stamp the things that change

Any file with current state needs a date. Without one, a reader can't
tell whether "the bridge is down" means down now or down last March.

Use `**Last updated:**` in the header. For long-lived reference
material that never changes, say so — "Last updated: 2026-01-04 (static
reference)". That tells the reader the old date is fine.

### 5. Write the decision, not just the outcome

This is the highest-value thing you can record, and the thing people
almost never write.

```markdown
## Why server-side endpointing

Chose it over client-side silence detection on 2026-03-02.

Client-side detection fired early on short utterances — it cut
"What time is it?" after "What". Whisper then got a fragment and
returned [BLANK_AUDIO].

Server-side endpointing means the server decides where the utterance
ended, using RMS relative to the peak rather than an absolute floor.
```

Six months later, the *what* is obvious from the code. The *why* is
gone unless you wrote it down, and without it the next agent will
"fix" it back to the broken version.

### 6. Don't record what the code already says

The file listing, the function signatures, the config defaults — those
live in the code. Don't copy them into memory. They'll be wrong in a
month.

Record what the code **can't tell you**: why it's shaped that way, what
breaks it, what was tried and rejected.

---

## Length: how long should a file be?

**As long as it needs to be, and no longer.**

The temptation is to be comprehensive. Resist it. A memory file that
tries to be everything about a topic becomes a file nobody reads
twice, because reading it costs more than it's worth.

Practical guidance:

| File type | Target length | Notes |
|---|---|---|
| Daily log entry | 1–10 lines | Texture, not summary |
| Event file | 50–300 lines | The real record |
| Project file | 100–400 lines | Split into a directory if bigger |
| Rule file | 200–800 lines | Every rule earns its place |
| Chapter index | 20–100 lines | One line per file |
| The index | 20–40 lines | Pointers only, hard limit |

**When a project file outgrows 400 lines, make it a directory.** The
project becomes the chapter; its files become the leaves.

---

## Voice

Write the way you'd want to read it six months later, when you're
tired and trying to remember what happened.

- **Concrete over abstract.** "The detector tripped on playback bleed"
  beats "there were some calibration issues."
- **First person, present tense** for state. "The bridge is running."
- **Past tense for events.** "The gateway restarted 14 times."
- **Include the numbers.** "2.5s" is useful. "A few seconds" isn't.
- **Say what you don't know.** "Not sure why this happens — no error in
  the logs." is genuinely valuable.
- **No hedging stacks.** "It might possibly be related to..." → "Related
  to X, not confirmed."

---

## Frontmatter

Every library file carries frontmatter. It exists so the index builder
can read the file without parsing prose, and so a grep for context
stays possible.

```markdown
---
title: Gateway restart loop
date: 2026-03-14
type: event
status: closed
tags: [hermes, launchd, incident]
---
```

| Field | Required | Values |
|---|---|---|
| `title` | yes | Human-readable title |
| `date` | yes | `YYYY-MM-DD` |
| `type` | yes | `project`, `person`, `event`, `log`, `rule`, `state`, `note` |
| `status` | no | `live`, `active`, `paused`, `closed`, `frozen`, `draft` |
| `tags` | no | Free-form list, lowercase |

**Status is the field that earns its keep.** An index listing shows
which projects are live. `status: closed` on an event means "this is
history, don't act on it."

---

## The header

After frontmatter, every file opens with a three-line header:

```markdown
# Title

**Purpose:** One line — what this file is for.
**Owner:** Who maintains it.
**Last updated:** YYYY-MM-DD
```

The `Last updated` line is what makes staleness visible during an
audit. Update it whenever you materially change the file.

---

## When a fact changes

**Never silently overwrite.** The sequence:

1. Read the file.
2. Archive the old version:
   ```bash
   mkdir -p library/archive/$(date +%F)_<slug>/
   cp library/<path> library/archive/$(date +%F)_<slug>/
   ```
3. Write the new version.
4. If it's a significant change, write an event file saying what
   changed, why, and what the old belief was.

Step 4 is what turns "the file changed" into "the understanding
changed." A reader six months later can ask "why did we switch?" and
get an answer.

**If two files disagree, resolve it explicitly.** Pick one. Archive
the other. Note the conflict and its resolution in an event file.
Leaving both live means the agent will pick whichever it reads last —
which is not a decision, it's a coin flip.

---

## What not to write

| Don't | Why |
|---|---|
| Secrets, keys, tokens | Never. Use environment variables and a secret store. |
| Transient state ("currently running the tests") | Belongs in a daily log. |
| Full file contents | Duplicates the code and drifts. |
| Speculation presented as fact | Label it: "Unconfirmed hypothesis." |
| Apologies or process narration | The file is a record, not a diary. |
| Anything already in the index | The index points; it doesn't summarize. |

**Especially not secrets.** If a memory file contains a credential, the
credential is now in your context every time the file is read, in your
git history, in every backup, and in every export. Reference the
environment variable name instead:

```markdown
The LLM key is in `BRAIN_API_KEY` — see `~/.config/<agent>/.env`.
```

---

## Checklist before you commit a memory file

- [ ] Frontmatter present and correct
- [ ] Three-line header with `Last updated`
- [ ] Leads with what the reader needs first
- [ ] Every cross-reference is a path, not a description
- [ ] The "why" is recorded, not just the "what"
- [ ] No secrets
- [ ] Previous version archived (if this is a material change)
- [ ] A pointer added to the index — **only** if it should be findable
- [ ] The pointer is one line and doesn't summarize

---

## Related

- **[CONVENTIONS.md](CONVENTIONS.md)** — naming and format rules
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — why the structure is this way
- **[SETUP.md](SETUP.md)** — installing it
