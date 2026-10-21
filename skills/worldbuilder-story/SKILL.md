---
name: worldbuilder-story
description: Use when writing arc or intention notes for an AI-powered narrative game, or producing direction.md in the Foundation phase. Also when output escalates too fast, intensity feels unearned, dark content is handled carelessly, or pacing lacks variation.
---

# Story

*All prose this skill produces follows `../writing-style.md`. Read it before writing. For arc, intention and introduction notes, a creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below. Rules shared by every entity note are in `../creative-step.md`, What every entity note shares.*

## Overview

This skill serves two related purposes:

**The direction document (Foundation phase):** `project/direction.md` is the world's standing creative brief and the story engine's primary guard rail. It is a project document, written by the Foundation item's builder using this skill's section templates as guidance. It is outside the creative step and is not governed by `../creative-step.md`. See the Ongoing Story Direction section below for its complete structure.

**Arc, intention, and introduction notes (Wide phase):** Once the direction document exists, this skill creates the story notes that extend it. Story notes link to their parent via the `up` field. Read the direction document before writing an arc note.

Story note types:

**Arc** (scope: arc) — A major story section. Covers a season, a storyline, or a thematic phase.

**Intention** (scope: intention) — A specific story possibility within an arc. Not a scripted outcome: a soft target the world is set up to enable.

**Introduction** (scope: introduction) — First-contact scene for a specific character. Created during or after character note work, not during the story notes phase.

`note-format.md` is the governing document for the note structure, scope values, the `up` field, the description, section contents, required entries and section-scoped writing rules. Read it before writing any section.

---

## Interview

The definer draws on this section and follows `../creative-step.md`, Interview. The questions for arc, intention and introduction notes follow the order of a narrative arc, from the standing state to what stays open. The arc is the frame; each answer goes to one section of the note, as `note-format.md`, Note structure, sets out.

For the direction document, the questions are the topics under Ongoing Story Direction below.

**Opening question.**
1. Which scope is it (arc, intention, or introduction), and which note is its parent?

**The standing state (goes to Situation).**
2. What is the state of affairs before any player involvement, and what pressure sits in it?
3. Who is involved, what does each want or fear, and which preconditions must hold? See `note-format.md`, Situation.

**What sets it moving (goes to Story Possibilities).**
4. What could set it moving?

**The turns (goes to Story Possibilities).**
5. What turns could it take, and what is the key moment of each? See `note-format.md`, Story Possibilities.

**The directions it could resolve (goes to Story Possibilities).**
6. Which directions could it resolve in? See `note-format.md`, Story Possibilities.
7. How does it connect to other arcs or characters?

**What stays unresolved (goes to Design Notes).**
8. What is unresolved about it, thematically, structurally, or in a specific character's behavior?

**Creative intent (goes to Design Notes).**
9. What is the arc for emotionally, and what should it feel like when it plays out?
10. Which scenes, arcs, or moments from other media does it evoke, and what specifically is drawn from each?
11. Why is it worth building toward?

---

## Writing the Note

Work through the sections in the order `note-format.md` gives. Write Session Notes from the Specification first, then Situation and Story Possibilities, then the rest of Design Notes, which records the creative intent against the arc those two sections hold. Write the description last.

Frontmatter and filename follow `../creative-step.md` (the example name here is `notes/Introduction - Maren.md`).

---

## Self-Check Before Marking Complete (arc, intention, introduction notes)

Mark the note `complete` when every item passes (`../creative-step.md`, Closure).

**Frontmatter**
- [ ] `scope` and `up` set; description written last (`note-format.md`, Frontmatter)

**Design Notes**
- [ ] Present with both subsections; creative intent, inspirations and open questions recorded (`note-format.md`, Design Notes)
- [ ] Not padded

**Situation**
- [ ] State of affairs before player involvement stated; preconditions named (`note-format.md`, Situation)

**Story Possibilities**
- [ ] Every required entry present or waived (`note-format.md`, Required entries)
- [ ] All entries phrased as possibility (`note-format.md`, Story Possibilities)

**Hand on.** When every item passes, hand the note on as `../creative-step.md`, Hand on, says.

---

## Ongoing Story Direction

> Direction notes are operational instructions for the story engine. They do not use the Design Notes / Situation / Story Possibilities structure — that structure applies to arc, intention, and introduction notes only.

### Romance pacing

This section is optional. Include it only when the world weighs in on romance. A world that does not must not mention romance in `project/direction.md`.

The engine by default moves too fast. When the section is present, it is the primary guard rail.

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

When this happens, propose a concept note as a spin-off (see `../creative-step.md`). Use `worldbuilder-concept` for layer classification and writing guidance. Do not leave world knowledge embedded in the story notes — it will either bloat the brief or be invisible to the export layer's lorebook packaging.

---

## Review

None here — arc, intention and introduction notes are reviewed at the critic step of the worldbuilder entity item, and the direction document is reviewed at the review of the Foundation item; no deliverable checks off at this skill.
