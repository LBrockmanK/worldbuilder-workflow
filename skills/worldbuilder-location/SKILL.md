---
name: worldbuilder-location
description: Use when creating or deepening a location note for an AI-powered narrative game — building a named place from scratch, giving depth to a location that feels like a backdrop, or fixing a location that generates repetitive or atmospheric-only output.
---

# Location Blueprint

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below. Rules shared by every entity note are in `../creative-step.md`, What every entity note shares.*

## Overview

A location for an LLM-powered narrative game is not a description — it is a behavioral specification. The engine handles generic scene-setting; the location note supplies the specific: who comes here and why, what the place does to the people in it, how it reads differently at different moments. A location that only answers "what does it look like?" is a backdrop. One that answers "what happens here, and how does this place push back on a scene?" is an actor. The sections that carry this specification are Form & History (physical reality and what the place carries) and Presence (who comes here and how the place behaves across different circumstances).

The location note is the comprehensive Wide-phase single source of truth for a named place. It covers everything true about the location that shapes how the engine writes scenes set there. Export skills derive their output from this note.

`note-format.md` is the governing document for the note structure, entry formats, required entries and section-scoped writing rules. Read it before writing any section.

**Description field:** the world navigation summary — what this place is, what makes it distinctive, and what role it plays in the setting's social and narrative life; not a physical description, which goes in Form & History. 1–2 sentences, written last (`../../CONTEXT.md`, Properties).

---

## Interview

The definer draws on this section and follows `../creative-step.md`, Interview. Questions are grouped by the note's sections, in writing order.

**Opening question.** Which Presence axes (time, observer, circumstances) would produce different scenes here? Skip the axes that would not.

**Design Notes.**
1. What does this place uniquely contribute to the world, and what kinds of scenes can only happen here?

**Form & History.**
2. What kind of place is it: scale, age, condition, environment, and one specific detail?
3. Why does it exist, what does it carry from the past, and what does it imply about the world? Does it hold any secrets?
4. Cultural shorthand: "For a real-world or historically grounded place: what real places, media, or cultural references does it call to mind, and what does each contribute? These references activate existing model associations cheaply. Skip for original-fantasy places where the model has no real-world associations to draw on." The answer lands in Form & History.

**Presence.**
5. Who comes here and why? What do they want that the place does or does not provide?
6. What tension exists between kinds of visitors, between regulars, or between the place and its visitors?
7. For each axis that applies: how does the place change with time, with the observer (insider or stranger), and with circumstances (normal, disrupted, crisis)? Which of those changes alters how a scene plays out?

**Frontmatter.**
8. Which region does it sit in, which characters are primary to it, and which concept notes cover it?

---

## Writing the Note

Work through the sections in the order `note-format.md` gives. Do not skip a section because the location seems simple: every section exists to catch what the others miss. After writing How the Place Behaves, run the push-back test it describes.

Frontmatter and filename follow `../creative-step.md` (the example name here is `notes/Ashen Lantern.md`). `region` and `primary-characters` link to their notes.

---

## Self-Check Before Marking Complete

Mark the note `complete` when every item passes (`../creative-step.md`, Closure).

**Frontmatter**
- [ ] Fields match the type's entry in the plugin's type roster; `region` and `primary-characters` link to their notes

**Description**
- [ ] Written per `../../CONTEXT.md`, Properties; 1–2 sentences; says what makes the location distinctive, not its physical form
- [ ] No design rationale, no export recommendations

**Design Notes**
- [ ] Present with both subsections; narrative function and intended scene types named (`note-format.md`, Design Notes)

**Form & History**
- [ ] Physical Form and History & Meaning meet their entry formats (`note-format.md`, Form & History)
- [ ] Cultural shorthand written here when the place is real-world or historically grounded

**Presence**
- [ ] Who Comes Here is written as who-does-what and holds at least one tension (`note-format.md`, Presence)
- [ ] At least one meaningful variation is specified
- [ ] The required scene-logic axis is present or waived (`note-format.md`, Required entries)

**Hand on.** When every item passes, hand the note on to the critic (`../creative-step.md`, Hand on), with `note-format.md` as the governing format document.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
