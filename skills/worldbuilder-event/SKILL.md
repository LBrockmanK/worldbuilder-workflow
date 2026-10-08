---
name: worldbuilder-event
description: Use when creating or deepening an event note for an AI-powered narrative game — festivals, calendar events, rituals, commemorations, recurring events. Also when an event note feels thin or generic, or fails to generate distinctive scene behavior.
---

# Event Notes

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below.*

## Overview

An event note is not a schedule entry. It is a behavioral specification for a day. The export skill handles calendar mapping and storyTrigger packaging; this skill covers writing event notes that do real work: making any scene set on this day feel different from any other day.

The event note is the Wide-phase single source of truth for a named event. Export skills derive their output from this note.

**Description field:** the world navigation summary — 1–2 sentences on what this event does to the community, not what it is. Written last, after the full note is complete. Example: "The Spring Harvest Festival: the one day the town's usual distances relax — introductions that normally take weeks happen naturally, and the player meets the community as a whole for the first time."

---

## Interview

The definer draws on this section. The human's answers go into the item's Specification, where the creative step reads them. Ask one question at a time and follow threads. The human can answer, skip, or provide source material in place of answers.

1. What does this event contribute that no other event does, and what kinds of scenes does it enable?
2. When does it take place (season and rough calendar position), and how often?
3. Who participates: everyone, volunteers, a community role, or invited guests?
4. What physically occurs: activities, rituals, traditions?
5. What does it commemorate, or why does it exist?
6. What social distances relax and what tensions tighten? Who talks to whom that normally would not?
7. Who is expected to attend, and what happens socially to someone who does not?
8. What becomes natural on this day, and what becomes unusual or impossible?
9. Does the event touch the hidden layer of the world, and at which knowledge layer (surface, mid, deep) does it sit?
10. In what realistic phrasings do people mention the event in dialogue?

---

## Note Structure

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| What Happens | Factual description of the event |
| Scene Effects | What the event does to scenes and social dynamics |

---

## Event Note Fields

Frontmatter is defined by the project's OKF registry — `new_doc.py` stamps it and the generated rules describe it. The script produces a date-prefixed filename; rename the fresh note to the event's name itself (e.g. `notes/Emberfall Vigil.md`) before adding content — the filename convention the templates state, and safe while nothing links to the note yet. Two writing notes: `aliases` carries every realistic way the event is mentioned in dialogue ("the festival," "harvest time"); the export skill derives keyword triggers from it. Timing — season, day, recurrence — is not a field: open What Happens with when the event takes place and how often.

---

## Design Notes

> **Excluded from exports.**

The Design Notes section is the builder's working record. It is not export content.

Cover:

- What this event contributes that no other event does. What makes it distinctive?
- Inspirations: real festivals, cultural observances, fictional events, what was drawn from each.
- Narrative intent: what kinds of scenes does this event enable?
- Open questions.

---

## What Happens

Factual description of the event.

Cover:

- **Timing:** season and rough calendar position. Exact day is an export decision. Write "early spring," not "day 8."
- **Who participates:** universal, optional, by community role, or by invitation.
- **What physically occurs:** activities, rituals, traditions.
- **Origin:** what the event commemorates or why it exists.

Vague timing is fine. Write for content, not calendar precision. The export skill assigns the specific day.

---

## Scene Effects

What the event does to scenes and social dynamics. This is the section that makes event notes worth having.

Cover:

- **Social dynamics:** what distances relax, what tensions tighten, who talks to whom that normally wouldn't.
- **Obligations and costs:** who is expected to attend, what happens socially if someone doesn't.
- **Scene logic:** what becomes natural on this day, what becomes unusual or impossible.
- **Hidden layer:** how the event touches deeper world elements, if relevant.

**The scene test:** After writing Scene Effects, ask: if the engine generates a scene set on this day with no other context, does it feel different from any other day? If not, Scene Effects is too thin.

Failing example: "It is a day of celebration. People are happy and gather in the town square." This could be any day. The event is invisible.

Passing example: "The usual rules about who approaches whom are suspended today. Characters who normally hold themselves apart from the player will initiate conversation. The player meets the full community for the first time, and relationships that normally require weeks of individual cultivation can begin here." The engine has specific behavioral direction.

---

## Layer Classification

Some events carry layer classification like concept notes. A surface festival is well-known and openly celebrated. A mid-layer observance has old stories behind it. A deep-layer ritual touches the hidden layer. Apply a `layer:` frontmatter field if relevant.

Event notes without a hidden dimension do not need layer classification.

---

## Lifecycle

Event notes can be written at any phase. When work outside an event item names an event, propose it as a spin-off (see `../creative-step.md`); a sentence or two of What Happens is enough to anchor the idea. Flesh out What Happens and Scene Effects once the cast is established; seasonal scenes are richer when you know who is in them. Mark the note `complete` after the self-check passes.

---

## Self-Check Before Marking Complete

**Frontmatter**
- [ ] `aliases` covers every realistic phrasing
- [ ] Fields match the generated rules

**Description**
- [ ] Written last
- [ ] Behavioral: describes what the event does to the community

**Design Notes**
- [ ] Distinctive contribution stated
- [ ] Not padded

**What Happens**
- [ ] Timing stated (approximate is fine)
- [ ] Who participates stated
- [ ] Physical activities described

**Scene Effects**
- [ ] Scene test passes: a scene on this day feels different from any other day
- [ ] At least one social dynamic specified — what relaxes or tightens
- [ ] Obligations and costs stated if the event carries them

**Hand on.** When every item passes, hand the note on to the critic: the critic step runs `worldbuilder-review` with this document and its governing format document. The revision step applies the auto-fix findings; escalated findings go to the human.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
