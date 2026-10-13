---
name: worldbuilder-faction
description: Use when creating or deepening a faction note for an AI-powered narrative game — any named group (noble household, guild, religious order, criminal network). Also when members feel interchangeable or faction identity is invisible in scenes.
---

# Faction Blueprint

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below. Rules shared by every entity note are in `../creative-step.md`, What every entity note shares.*

## Overview

A faction note is not a roster — it is a shared behavioral specification. The engine handles generic social roles; the faction note supplies the specific: how this group acts as a collective, what its members do when they encounter strangers, how they present to outsiders, and how individuals vary beneath that shared surface.

When a faction is underspecified, the engine defaults to making every member a generic instance of their surface role — every guard gruff, every merchant greedy, faction identity invisible across scenes. The faction note exists to prevent this. The section that carries the specification is Collective Behavior. Origin & Structure is supporting context.

The faction note is the comprehensive Wide-phase single source of truth for any named group. Export skills derive their output from this note.

`note-format.md` is the governing document for the note structure, entry formats, required entries and section-scoped writing rules. Read it before writing any section.

**Description field:** the world navigation summary — what this group is, what it does to scenes, and what a player can expect from any member they encounter. 1–2 sentences, behavioral rather than descriptive, written last (`../../CONTEXT.md`, Properties): a reader who sees only this field should know what to expect when the faction enters a scene.

---

## Interview

The definer draws on this section and follows `../creative-step.md`, Interview. Questions are grouped by the note's sections, in writing order.

**Opening question.** Does an Inter-Faction Web apply to this project, or does the faction deal with no other faction directly? Skip the web questions when it does not apply.

**Design Notes.**
1. What does this faction do to the story: what conflicts does it generate, and what role does it fill that no other faction could?

**Origin & Structure.**
2. How did it come to exist, and what was its original purpose?
3. What does it control now? Name specific resources, territory, monopolies, information, relationships, or obligations owed to it.
4. What is it trying to achieve right now? The goal must be specific and active.
5. Location as pressure: "What about where this faction operates creates pressure on its members? Territory, climate, geography, neighbors, proximity to danger? State the connection as a pair: [place fact] → [what it made true about the faction]." The answer lands in Origin & Structure.
6. Cultural shorthand: "For a faction modeled on real-world or historically grounded groups: what real organizations, movements, or subcultures does it resemble, and what does each contribute? These references activate existing model associations cheaply. Skip for original-fantasy factions where the model has no real-world associations to draw on." The answer lands in Origin & Structure.
7. How does one become a member, how does membership end, and which ranks or tiers exist?
8. Which cases are ambiguous: former members, dual loyalties, contested membership, outsiders who function as members?

**Collective Behavior.**
9. What do members do as a group when they meet a stranger, when a member is challenged from inside, when they deal with rivals or authority, and when they operate under scrutiny or pressure? Why?
10. What is the collective mask members present, and along which axes do individual members vary beneath it?
11. When the web applies: which other factions does it deal with directly, what is the status of each relationship, and what drives it?

**Frontmatter.**
12. Which characters are its members?

---

## Writing the Note

Work through the sections in the order `note-format.md` gives. After completing Collective Behavior, run the member test it describes.

Frontmatter and filename follow `../creative-step.md` (the example name here is `notes/Lantern Guild.md`). `members` links to member character notes.

---

## Self-Check Before Marking Complete

Mark the note `complete` when every item passes (`../creative-step.md`, Closure).

**Frontmatter**
- [ ] Fields match the type's entry in the plugin's type roster; `members` links to member character notes

**Description**
- [ ] Written per `../../CONTEXT.md`, Properties; 1–2 sentences; behavioral, describing what a player encounters with any member, not what the faction is in the abstract

**Design Notes**
- [ ] Present with both subsections; narrative engine stated (`note-format.md`, Design Notes)

**Origin & Structure**
- [ ] Founding, Current holdings, Active goals and Membership meet their formats (`note-format.md`, Origin & Structure)
- [ ] Place pressure and cultural shorthand written here when they apply

**Collective Behavior**
- [ ] The required entries are present or waived (`note-format.md`, Required entries)
- [ ] Demeanor and the variation layer are written as `note-format.md` describes

**Inter-Faction Web**
- [ ] Present only when the web applies; entries meet their format (`note-format.md`, Inter-Faction Web)

**Hand on.** When every item passes, hand the note on to the critic (`../creative-step.md`, Hand on), with `note-format.md` as the governing format document.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
