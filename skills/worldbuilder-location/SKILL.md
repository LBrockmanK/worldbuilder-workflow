---
name: worldbuilder-location
description: Use when creating or deepening a location note for an AI-powered narrative game — building a named place from scratch, giving depth to a location that feels like a backdrop, or fixing a location that generates repetitive or atmospheric-only output.
---

# Location Blueprint

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below.*

## Overview

A location for an LLM-powered narrative game is not a description — it is a behavioral specification. The engine handles generic scene-setting; the location note supplies the specific: who comes here and why, what the place does to the people in it, how it reads differently at different moments. A location that only answers "what does it look like?" is a backdrop. One that answers "what happens here, and how does this place push back on a scene?" is an actor. The sections that carry this specification are Form & History (physical reality and what the place carries) and Presence (who comes here and how the place behaves across different circumstances). Presence carries the most weight.

The location note is the comprehensive Wide-phase single source of truth for a named place. It covers everything true about the location that shapes how the engine writes scenes set there. Export skills derive their output from this note.

**Description field:** the world navigation summary — what this place is, what makes it distinctive, and what role it plays in the setting's social and narrative life; not a physical description, which goes in Form & History. 1–2 sentences, written last, after the full note is complete.

---

## Interview

The definer draws on this section. The human's answers go into the item's Specification, where the creative step reads them. Ask one question at a time and follow threads. The human can answer, skip, or provide source material in place of answers.

1. What does this place uniquely contribute to the world, and what kinds of scenes can only happen here?
2. What kind of place is it: scale, age, condition, environment, and one specific detail?
3. Why does it exist, what does it carry from the past, and what does it imply about the world? Does it hold any secrets?
4. Who comes here and why? What do they want that the place does or does not provide?
5. What tension exists between kinds of visitors, between regulars, or between the place and its visitors?
6. How does the place change with time, with the observer (insider or stranger), and with circumstances (normal, disrupted, crisis)? Which change alters scene logic, tone, or friction, not only who is present?
7. Which region does it sit in, which characters are primary to it, and which concept notes cover it?

---

## Location Note Structure

Work through sections in order. Do not skip sections because the location seems simple — every section exists to catch what the others miss.

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| Form & History | Physical reality and what the place carries |
| Presence | Who comes here and how the place behaves |

Location notes do not use sub-files — all content lives in one note. Sub-files are only used in skills where sections are too large for a single document (see `worldbuilder-character` for reference).

Frontmatter is defined by the project's OKF registry; `new_doc.py` stamps it at creation and the generated rules describe it. The script produces a date-prefixed filename; rename the fresh note to the location's name itself (e.g. `notes/Ashen Lantern.md`) before adding content — the filename convention the templates state, and safe while nothing links to the note yet.

---

## Design Notes

> *Excluded from exports. Agent context only.*

The builder record — what drove the design of this location. Narrative function (what does this location uniquely contribute), intended scene types (what kinds of scenes can only happen here), inspirations (real or fictional), design decisions, open questions. Bullet points under plain sub-headers.

Leave blank if nothing warrants capturing — do not pad.

---

## Form & History

### Physical Form

1–3 sentences. Scale, age, condition, environment, one vivid specific detail.

Not a floor plan. The engine needs to know what kind of place this is, not where the furniture is. One concrete detail beats three paragraphs of layout.

> *The mill is a two-storey stone building with a collapsed east wall, open to the sky. The water wheel still turns sometimes when there's no wind.*

A room-by-room layout is not this section.

### History & Meaning

Why this place exists. What it carries from the past. What it implies about the world. Secrets if it has them.

Not required to be long — a sentence or two is often enough — but the "what it implies" question must be answered. A location with no reason to exist generates no scenes worth setting there.

If the location is the subject of concept notes at different knowledge layers, link to those notes here rather than duplicating their content.

---

## Presence

### Who Comes Here

The ecosystem layer. Who comes here and why. What they do when they arrive. What they want that they might not get. What tensions exist between different regular visitors, or between visitors and whoever maintains the place.

Written as who-does-what, not who-is-there. Every fact in this section is a decision — "various locals may visit for various reasons" is not a valid entry.

> *Farmers bring grain in autumn to argue pricing with the factor; the factor holds the only certified scales in the valley, which means he sets the effective price regardless of what anyone negotiates. The itinerant workers who sleep in the granary loft resent both groups and stay out of disputes until someone owes them wages.*

That is a valid entry: three types of visitors, what each wants, and two tensions.

Cover:
- The main types of people who come here and their reasons
- What they want that the place does or doesn't provide
- At least one tension — between visitor types, between regulars, or between the place and its visitors

### How the Place Behaves

The section that turns a backdrop into an actor. How this place reads across variations:

- **Time:** day vs. night, busy periods vs. quiet, seasonal rhythm if relevant
- **Observer:** how an insider or regular experiences it differently from a stranger or first-timer — if that distinction would produce meaningfully different scenes
- **Circumstances:** normal operation vs. disrupted, crisis, or changed state

Not all axes apply to every location. Cover the variations that would produce different scenes; skip those that wouldn't. A remote ruin probably does not need an insider/stranger distinction. A village market square likely needs all three.

**The push-back test:** After writing this section, read it and ask — does this place *do something* to the characters in it, or does it only describe what's there?

An entry that fails: "At night the market is quiet and empty." — This describes absence. The place isn't acting.

An entry that passes: "At night the market belongs to the night-watch, who treat any civilian presence as suspicious until proven otherwise. A player arriving after dark will be questioned before anything else happens." — The place produces a scene logic that doesn't apply in daylight. It acts.

The standard: at least one axis must specify a change in scene logic, tone, or friction — not just a change in who is present or absent.

---

## Key Principles

**Make decisions, don't hedge.** Every fact in the note is a decision. "The mill burned under disputed circumstances" is a decision. "Something may have happened to the mill at some point" is an incomplete note.

**Write plainly. No flair.** "Locals avoid the east wing after dark" is correct. "Shadows cling to its ancient stones like a shroud of forgotten memory" belongs in prose, not here. If a sentence sounds like it belongs in a novel, rewrite it.

**Presence carries more weight than Form & History.** A location note that is mostly physical description and thin on Presence is description masquerading as specification. The behavioral sections are where the location becomes an actor.

**Asymmetry is normal.** Not every location needs every axis of Presence. Write only what is true and useful.

**Design Notes are builder context.** Do not include narrative purpose or creative intent in the note body sections — that goes in Design Notes.

---

## Self-Check Before Marking Complete

The note stays on an open status tag while work is in progress; mark it `complete` when every item below passes.

**Frontmatter**
- [ ] Fields match the generated rules; `region` and `primary-characters` link to their notes

**Description**
- [ ] Written last — after the full note is complete
- [ ] 1–2 sentences; describes what makes this location distinctive, not its physical form
- [ ] No design rationale, no export recommendations

**Design Notes**
- [ ] Narrative function stated
- [ ] Intended scene types named
- [ ] Not padded — blank is acceptable if nothing warrants capturing

**Form & History**
- [ ] Physical Form: 1–3 sentences; one vivid specific detail; no floor plan
- [ ] History & Meaning: states why the place exists and what it implies about the world

**Presence**
- [ ] Names who comes here and why
- [ ] At least one tension in the ecosystem
- [ ] Written as who-does-what, not who-is-there
- [ ] At least one meaningful variation specified
- [ ] At least one axis specifies a change in scene logic, tone, or friction — not just a change in who is present or absent

**Hand on.** When every item passes, hand the note on to the critic: the critic step runs `worldbuilder-review` with this document and its governing format document. The revision step applies the auto-fix findings; escalated findings go to the human.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
