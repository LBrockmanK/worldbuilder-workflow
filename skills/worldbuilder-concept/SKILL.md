---
name: worldbuilder-concept
description: Use when writing concept notes for an AI-powered narrative game — surface facts, mid-layer history, deep secrets, or background NPC guidelines. Also when a concept note feels too broad or narrow, or when deciding what layer knowledge belongs on.
---

# Lorebook

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below. Rules shared by every entity note are in `../creative-step.md`, What every entity note shares.*

## Overview

World knowledge is organized as concept notes — one note per discrete topic. Export skills read these notes and package them as lorebook entries. This skill covers writing the concept notes well; the export skill handles the packaging.

**Lorebook.** Vault documents say "lorebook" for the world's reference entries. The export platforms (ainime and isekaizero) call the same entries "World Info"; that is the platform's word, kept for exports and not used in vault documents.

Good concept notes give the engine exactly what it needs at the moment a topic arises. The goal is precision: the right information for the right moment. Write notes that are dense and specific rather than broad and atmospheric.

`note-format.md` is the governing document for the note structure, entry formats, required entries and section-scoped writing rules. Read it before writing any section.

**Description field:** the world navigation summary — 1–2 sentences covering what this piece of world knowledge is and when it matters in scenes. Written last (`../../CONTEXT.md`, Properties); a description that does not say when the lore activates is incomplete.

---

## Interview

The definer draws on this section and follows `../creative-step.md`, Interview. Questions are grouped by the note's sections, in writing order.

**Opening question.** Is this a rule-bearing concept: a magic system, institution, cultural practice, belief system, or anything with internal logic that scenes must respect? Skip the costs-and-limits question when it is not.

**Design Notes.**
1. What is this piece of world knowledge, and why does it warrant its own note?
2. What does its existence make impossible, costly, or inevitable in any scene that touches it?
3. At which layer does it sit (surface, mid, deep), and what would be lost one layer higher or lower?

**Lore.**
4. What is true about it? If people believe something different from the truth, what do they believe?

**Implications.**
5. What behavioral and social consequences follow from it?
6. For a rule-bearing concept: what are its costs and limits?
7. When does it matter in a scene: what activation context brings it up?

**Frontmatter.**
8. In what realistic phrasings do characters mention it (the aliases)?

---

## Writing the Note

Work through the sections in the order `note-format.md` gives. Write the narrative purpose in Design Notes before drafting Lore and Implications.

Frontmatter and filename follow `../creative-step.md` (the example name here is `notes/The Old Fire.md`). `layer` is set and `aliases` is complete; other fields follow the concept entry in the plugin's type roster.

Location notes have their own skill, `worldbuilder-location`. Event notes (festivals, seasonal observances, recurring world events) have theirs, `worldbuilder-event`.

---

## Concept Note Lifecycle

World knowledge is a living collection, not a phase that opens and closes. Any stage of the project can produce facts worth capturing: a household design decision, a character backstory detail, an event's implied history, a conversation that clarifies the magic system. When a discrete piece of world knowledge solidifies, propose a concept note as a spin-off (see `../creative-step.md`) — do not wait.

**During active development:** When any working session produces a fact or implication that belongs in the lorebook, propose the concept note as a spin-off, with the fact as the idea and the working session as its context — a sentence or two of Lore is enough to anchor the thought. Flesh it out in a concept item when you have more context.

**At project completion:** Run a validation pass across all concept notes:
- Verify every note has `layer`, `aliases`, and `description` filled in
- Check for contradictions across layers — surface notes should not imply what deep notes are supposed to reveal
- Cross-reference with completed character notes: any implied lore in those notes that has no concept note?
- Check that each note's Implications section includes specific activation context

**Don't front-load.** Writing all concept notes before characters are drafted means writing them before you know what the characters will imply about the world. Let the concept collection grow with the project.

---

## Self-Check Before Marking Complete

Mark the note `complete` when every item passes (`../creative-step.md`, Closure). The note is ready when it can constrain or shape any scene that touches the concept: a scene author reading it knows what is impossible, what costs something, and what is inevitable because this thing exists.

**Frontmatter**
- [ ] `layer` set; `aliases` complete (`note-format.md`, Alias writing); other fields per the concept entry in the plugin's type roster

**Description**
- [ ] Written per `../../CONTEXT.md`, Properties; 1–2 sentences; covers what this knowledge is and when it matters

**Design Notes**
- [ ] Present with both subsections; narrative purpose and layer rationale stated (`note-format.md`, Design Notes)

**Lore**
- [ ] Content written at the correct layer tone; iceberg split present if the belief/truth gap is narratively live (`note-format.md`, Lore)

**Implications**
- [ ] Behavioral and social consequences, not just restrictions; activation context stated (`note-format.md`, Implications)
- [ ] Costs and limits present for rule-bearing concepts, or waived (`note-format.md`, Required entries)

**Hand on.** When every item passes, hand the note on to the critic (`../creative-step.md`, Hand on), with `note-format.md` as the governing format document.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
