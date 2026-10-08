---
name: worldbuilder-story
description: Use when writing arc or intention notes for an AI-powered narrative game, or producing direction.md in the Foundation phase. Also when output escalates too fast, intensity feels unearned, dark content is handled carelessly, or pacing lacks variation.
---

# Story

*All prose this skill produces follows `../writing-style.md`. Read it before writing.*

## Overview

This skill serves two related purposes:

**The direction document (Foundation phase):** `project/direction.md` is the world's standing creative brief and the story engine's primary guard rail. It is a project document, produced in the Foundation phase using this skill's section templates as guidance. See the Ongoing Story Direction section below for its complete structure.

**Arc, intention, and introduction notes (Wide phase):** Once the direction document exists, this skill creates the story notes that extend it. Story notes link to their parent via the `up` field.

Story note types:

**Arc** (scope: arc) — A major story section, linking up to the direction document. Covers a season, a storyline, or a thematic phase.

**Intention** (scope: intention) — A specific story possibility within an arc, linking up to that arc. Not scripted outcomes — soft targets the world is set up to enable.

**Introduction** (scope: introduction) — First-contact scene for a specific character. Created during or after character note work, not during the story notes phase.

Frontmatter is defined by the project's OKF registry; `new_doc.py` stamps it at creation and the generated rules describe it. The script produces a date-prefixed filename; rename the fresh note to the story's name itself (e.g. `notes/Introduction - Maren.md`) before adding content — the filename convention the templates state, and safe while nothing links to the note yet. Set `scope` to arc, intention, or introduction, and point `up` at the parent note.

**Description field:** 1–2 sentences naming what this note is — for an arc, the emotional territory it covers; for an intention, the story possibility in one sentence; for an introduction, who it introduces and the first impression. Written last; other agents scan this field when planning arcs or building character notes.

Structure for arc, intention, and introduction notes:

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| Situation | State of affairs before player involvement |
| Story Possibilities | What could happen; phrased as possibility not script |

Read the direction document before creating arc notes. Arc notes develop what the brief establishes — they do not contradict it.

---

## Arc, Intention, and Introduction Notes

### Design Notes

> **Excluded from exports.** The story engine acts on Situation and Story Possibilities. Design Notes are for the builder.

This section captures creative intent — the thinking behind the arc or moment before it becomes structure.

Cover:

- **Creative intent:** What kind of story is this emotionally? What should it feel like when it plays out? What experience is the builder trying to create for the player?
- **Inspirations:** Specific scenes, arcs, or moments from other media being evoked. Name what is being drawn from each — not just "like the opening of Episode 4" but what specifically about that opening: the scale, the stillness before action, the sense of something already in motion.
- **Why this is worth building toward:** What makes this arc or moment interesting? Why does it earn space in the world?
- **Open questions:** What is not yet resolved about this arc — thematic, structural, or about a specific character's behavior in it?

### Situation

This section establishes the state of things before any player involvement. Write in present tense.

**For arc and intention notes:**

- The current state of affairs in the world that makes this arc or intention possible
- Who is involved and what each party wants or fears going in
- Timing constraints or seasonal considerations if relevant
- Preconditions: what needs to be true — player trust level, prior events, season — for this arc or intention to be accessible

**For introduction notes:**

- Where and when the introduction could happen
- Who else is present
- What the circumstances are that make this a natural first meeting

### Story Possibilities

This section covers what could happen and how it could develop. Phrased as possibility, not script: use "may," "could," "there is a possibility that."

Do not script outcomes. Write for robustness — arcs that remain interesting whether or not a specific beat fires.

**For arc notes:**

- What could happen and how it could develop
- Key moments: the set pieces that make the arc feel real if they fire
- Resolution directions: natural ways things could go, not scripted outcomes
- Connection to other arcs or characters

**For intention notes:**

Typically shorter — one key possibility with the moment that would trigger it and the direction it could go.

**For introduction notes:**

How the scene plays, what the character does, what invitation it extends to the player.

---

## Self-Check Before Marking Complete (arc, intention, introduction notes)

The note stays on an open status tag while work is in progress; mark it `complete` when every item below passes.

**Description**
- [ ] Written last
- [ ] 1–2 sentences; navigable summary of what this arc or intention is

**Design Notes**
- [ ] Creative intent stated
- [ ] Inspirations named with what specifically is being drawn
- [ ] Not padded

**Situation**
- [ ] State of affairs before player involvement stated
- [ ] Preconditions named

**Story Possibilities**
- [ ] All entries phrased as possibility, not script
- [ ] At least one key moment or set piece named
- [ ] Connection to other arcs or characters noted

---

## Ongoing Story Direction

> Direction notes are operational instructions for the story engine. They do not use the Design Notes / Situation / Story Possibilities structure — that structure applies to arc, intention, and introduction notes only.

### Romance pacing

The engine by default moves too fast. This section is the primary guard rail.

Adapt this language:

> Romantic relationships develop through accumulated familiarity, genuine emotional connection, and earned trust. Physical and sexual intimacy should not occur until a deep relationship is established — characters are not available simply because the player has been friendly. Romantic interest emerges gradually and should include moments of resistance, uncertainty, or vulnerability before commitment. Early flirtation is fine; it should not rapidly escalate. A relationship that has only had pleasant surface conversation is not ready for intimacy. Let each stage breathe.

Key elements to specify: slow and earned escalation; visible resistance and uncertainty before commitment; escalation that can only follow genuine emotional depth.

### Dark themes

Permission to go there, with guidance on how:

> Difficult material — depression, grief, addiction, family trauma, loss — exists in this world and can surface when context warrants it. Handle it with care and weight, not for shock value. Dark arcs tend toward hope but do not require resolution. A character in recovery is still in recovery; a character who is grieving may always carry some of that grief. The player is a witness and companion, not a therapist or savior. Do not rush toward catharsis.

Key framing: dark material is handled with weight, not shock value; resolution is not required; the player is witness, not savior.

### The hidden layer (if applicable)

For settings with supernatural or concealed depth:

> [The hidden layer] is real in this world but not advertised. Most characters who encounter something genuinely strange will rationalize it, stay quiet about it, or feel unsettled without knowing why. Direct [supernatural] events are rare and carry weight — they should feel significant, not casual. The boundary between mundane and hidden is more permeable near old places, during certain times, and for people who know how to look. The world does not explain itself.

Adapt the bracketed terms to the setting. If the setting has no supernatural element, replace with equivalent guidance on whatever its concealed layer is — mystery, historical truth, institutional corruption, etc.

### NPC relationships (year 2+ guidance)

After the first full year, if characters with strong chemistry have not moved toward formal romantic or close-friendship commitment, the engine should let that natural pull become more visible. Do not force outcomes — let the existing dynamic mature without manufactured escalation.

---

## Common Failure Modes

**Scenes feel samey.** The direction document should explicitly say quiet scenes are valid and desirable — not every scene needs to be emotionally meaningful. If this isn't said, the engine treats every scene as an opportunity for significance.

**Dark content feels gratuitous.** "Handle with care and weight, not for shock value" combined with "the player is a witness, not a savior" addresses the most common failures.

**Characters collapse into positivity.** This is a character note problem, not a story direction problem — see `worldbuilder-character`, particularly the Relationship Behavior section and the negative-track character guidance in `worldbuilder-world-foundation`.

---

## World Knowledge from Story Direction Work

Story direction work regularly surfaces world knowledge that belongs in concept notes rather than the direction brief — historical context implied by the opening arc, background on the hidden layer that shouldn't be in the standing brief, lore that shapes pacing guidance but reads as exposition if left in this document.

When this happens, create a concept note immediately. Use `worldbuilder-concept` for layer classification and writing guidance. Do not leave world knowledge embedded in the story notes — it will either bloat the brief or be invisible to the export layer's lorebook packaging.
