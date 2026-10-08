---
name: worldbuilder-faction
description: Use when creating or deepening a faction note for an AI-powered narrative game — any named group (noble household, guild, religious order, criminal network). Also when members feel interchangeable or faction identity is invisible in scenes.
---

# Faction Blueprint

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below.*

## Overview

A faction note is not a roster — it is a shared behavioral specification. The engine handles generic social roles; the faction note supplies the specific: how this group acts as a collective, what its members do when they encounter strangers, how they present to outsiders, and how individuals vary beneath that shared surface.

When a faction is underspecified, the engine defaults to making every member a generic instance of their surface role — every guard gruff, every merchant greedy, faction identity invisible across scenes. The faction note exists to prevent this. The section that carries the specification is Collective Behavior. Origin & Structure is supporting context.

The faction note is the comprehensive Wide-phase single source of truth for any named group. Export skills derive their output from this note.

**Description field:** the world navigation summary — what this group is, what it does to scenes, and what a player can expect from any member they encounter. 1–2 sentences, behavioral rather than descriptive, written last: a reader who sees only this field should know what to expect when the faction enters a scene.

---

## Interview

The definer draws on this section. The definer's rounds run on the answer page, and the human's answers go into the item's Specification, where the creative step reads them. Ask one question at a time and follow threads. The human can answer, skip, or provide source material in place of answers.

1. What does this faction do to the story: what conflicts does it generate, and what role does it fill that no other faction could?
2. How did it come to exist, and what was its original purpose?
3. What does it control now? Name specific resources, territory, monopolies, information, relationships, or obligations owed to it.
4. What is it trying to achieve right now? The goal must be specific and active.
5. How does one become a member, how does membership end, and which ranks or tiers exist?
6. Which cases are ambiguous: former members, dual loyalties, contested membership, outsiders who function as members?
7. What do members do as a group when they meet a stranger, and why (three to five When, Behavior, Because entries)?
8. What is the collective mask members present, and along which axes do individual members vary beneath it?
9. Which other factions does it deal with directly, what is the status of each relationship, and what drives it?
10. Which characters are its members?

---

## Faction Note Structure

Work through sections in order.

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| Origin & Structure | Founding, holdings, membership |
| Collective Behavior | Behavioral entries, mask, variation, inter-faction |

Faction notes do not use sub-files — all content lives in one note.

Frontmatter is defined by the project's OKF registry; `new_doc.py` stamps it at creation and the generated rules describe it. The script produces a date-prefixed filename; rename the fresh note to the faction's name itself (e.g. `notes/Lantern Guild.md`) before adding content — the filename convention the templates state, and safe while nothing links to the note yet.

---

## Design Notes

> **Builder record — excluded from exports.**

The narrative engine this faction runs. Not a description of its membership or its history — what does it *do* to the story? What conflicts does it generate or embody? What role does it fill that no other faction could?

A merchant guild and a thieves' guild that produce the same kinds of scenes have the same narrative engine. That is a problem.

Also record here: inspirations, design decisions, and open questions about the faction's role.

---

## Origin & Structure

Three things, in order, then membership:

**Founding** — how the faction came to exist and what its original purpose was.

**Current holdings** — what it controls now. Be specific: resources, territory, monopoly, information, relationships, obligations owed to it. "Has influence" is not a holding.

**Active goal(s)** — what the faction is trying to achieve right now. Goals must be specific and active.

> *Controls the grain trade and intends to extend that monopoly to the river docks before the spring thaw.*

"Seeks to grow its power and influence" is not a goal.

Specific goals connect the faction to the events layer and make it a story engine.

**Membership** — Deliberately thin on named-member content — named members have their own character notes. Covers:

- **Ranks or tiers** if they exist (hierarchy only — no personalities here)
- **Acquisition** — how one becomes a member
- **Loss** — how membership ends or is revoked
- **Ambiguity cases** — former members, dual loyalties, contested membership, outsiders who function as members without formal standing

Ambiguity cases earn their place because characters who straddle faction lines are often the most narratively generative.

---

## Collective Behavior

The key section. This is what makes faction members read as members.

**Phrasing rule throughout this section:** instructional, not descriptive. Write what members DO, not what they ARE.

Failing example:
> "Members are guarded and don't trust outsiders."

Passing example:
> "When approached by an outsider asking about Brotherhood pricing, members deflect with friendly vagueness — they quote ranges rather than figures, suggest the player talk to the factor, and find a reason to be elsewhere if pressed. Show this."

Descriptive phrasing tells the engine what to know. Instructional phrasing tells it what to do. Every entry in this section must be instructional.

### Shared behavioral tendencies

3–5 entries in When/Behavior/Because form, applied to the group as a whole:

> When [situation], [members do X] because [faction value or principle].

Example:
> When a stranger asks Brotherhood members about their pricing or trade routes, members give friendly, vague answers — ranges rather than figures, references to the factor rather than direct quotes — because the Brotherhood treats price information as proprietary. Show this deflection without making it feel hostile.

Cover recognizable situations: encountering outsiders, handling internal conflict or challenge, interacting with rivals or authority, operating under scrutiny or pressure.

### The collective mask (Demeanor)

How members present as a group to people who don't know them. What a stranger interacting with any member of this faction expects to encounter — before individual personality comes through.

This is the shared surface: the thing that makes members recognizable as members. Write it as a behavioral directive, not a personality label — "members present as..." not "members are...".

### The variation layer (Nature)

The individual underneath the collective mask. Members share the Demeanor without sharing the same personality. Name the natural variation axes — do not write out every possible variation, just the axes that produce meaningfully different characters.

> *Loyalists vs. cynics. True believers vs. pragmatists who joined for the wages. Long-timers who remember the Brotherhood's origins vs. recent recruits who only know its current operation.*

This is what prevents members from being interchangeable. They wear the same mask; who they are underneath differs. Name the axes in terms of observable behavior — how a loyalist acts differently from a cynic in the same situation, not just that one is loyal and one is cynical.

### Inter-Faction Web

Lightweight by design. Direct relationships only — alliances, rivalries, contested territory, historical grievances with active weight. No comprehensive opinion-of-everyone map.

Each entry:
```
[[Faction Name]] — allied / neutral / rival / enemy: one sentence on what drives it.
```

Relationships that don't bear on the current project do not go here.

---

## Key Principles

**The member test.** After completing Collective Behavior, read it and ask: if you wrote an unnamed member of this faction into a scene with no other characterization, would they read as a member?

Failing example: a Silt Brotherhood member in a scene where they "eye the player with suspicion and ask what they want." Any faction member could do this. The Brotherhood is invisible.

Passing example: a Silt Brotherhood member who "quotes the player a price range, suggests they talk to the factor for specifics, and finds a reason to be elsewhere before the player can press further." This behavior only makes sense for the Brotherhood.

The standard: a member who could belong to any faction fails the test. A member whose behavior only makes sense given this faction's Demeanor and behavioral tendencies passes it.

**Make decisions, don't hedge.** An active goal that is vague is not a goal. A Demeanor that could belong to any group is not a Demeanor.

**Collective Behavior is the priority section.** A faction note that is mostly Origin & Structure and thin on Collective Behavior documents history without specifying behavior. History is less important than what the faction does.

**Instructional phrasing is not optional.** Descriptive phrasing in Collective Behavior will not produce behavioral consistency in output. Every entry must specify what members do.

**Write plainly. No flair.** This applies to every section, not just Collective Behavior. "The Brotherhood controls the valley's grain pricing" is correct. "The Brotherhood's iron grip on commerce has shaped the valley's soul for generations" is not.

**Storylines belong in story notes, not faction notes.** If a story possibility is anchored by this faction's existence, propose a story note as a spin-off (see `../creative-step.md`).

---

## Self-Check Before Marking Complete

The note stays on an open status tag while work is in progress; mark it `complete` when every item below passes.

**Frontmatter**
- [ ] Fields match the generated rules; `members` links to member character notes

**Description**
- [ ] Written last
- [ ] 1–2 sentences; behavioral — describes what a player encounters with any member, not what the faction is in the abstract

**Design Notes**
- [ ] Narrative engine stated
- [ ] Not padded

**Origin & Structure**
- [ ] Has a specific active goal (not "seeks power" or similar)
- [ ] Names what the faction currently controls (specific, not "influence")
- [ ] How membership is acquired and lost is stated
- [ ] Ambiguity cases addressed

**Collective Behavior**
- [ ] 3–5 When/Behavior/Because entries for the group
- [ ] Demeanor (collective mask) described
- [ ] Variation layer (Nature axes) named
- [ ] All entries phrased as instructional directives, not description
- [ ] Member test passes: Demeanor entry specifies at least one concrete behavior, not a personality label; a member behaving per this note could not belong to a different faction without rewriting their behavior

**Inter-Faction Web**
- [ ] Direct relationships only
- [ ] Each entry has status + one sentence on what drives it

**Hand on.** When every item passes, hand the note on to the critic: the critic step runs `worldbuilder-review` with this document and its governing format document. The revision step applies the auto-fix findings; escalated findings go to the human.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
