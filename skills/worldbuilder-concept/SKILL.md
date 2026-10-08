---
name: worldbuilder-concept
description: Use when writing concept notes for an AI-powered narrative game — surface facts, mid-layer history, deep secrets, or background NPC guidelines. Also when a concept note feels too broad or narrow, or when deciding what layer knowledge belongs on.
---

# Lorebook

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below.*

## Overview

World knowledge is organized as concept notes — one note per discrete topic. Export skills read these notes and package them as lorebook entries. This skill covers writing the concept notes well; the export skill handles the packaging.

Good concept notes give the engine exactly what it needs at the moment a topic arises. The goal is precision: the right information for the right moment. Write notes that are dense and specific rather than broad and atmospheric — 50 tokens of exact context beats 300 tokens of unfocused description.

**Description field:** the world navigation summary — 1–2 sentences covering what this piece of world knowledge is and when it matters in scenes. Written last; a description that does not say when the lore activates is incomplete.

---

## Interview

The definer draws on this section. The definer's rounds run on the answer page, and the human's answers go into the item's Specification, where the creative step reads them. Ask one question at a time and follow threads. The human can answer, skip, or provide source material in place of answers.

1. What is this piece of world knowledge, and why does it warrant its own note?
2. What does its existence make impossible, costly, or inevitable in any scene that touches it?
3. At which layer does it sit (surface, mid, deep), and what would be lost one layer higher or lower?
4. What is true about it? If people believe something different from the truth, what do they believe?
5. What behavioral and social consequences follow from it? For a rule-bearing concept, what are its costs and limits?
6. When does it matter in a scene: what activation context brings it up?
7. In what realistic phrasings do characters mention it (the aliases)?

---

## Note Structure

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| Lore | What is true about this thing in the world |
| Implications | What follows from this being true; activation context |

Frontmatter is defined by the project's OKF registry; `new_doc.py` stamps it at creation and the generated rules describe it. The script produces a date-prefixed filename; rename the fresh note to the concept's name itself (e.g. `notes/The Old Fire.md`) before adding content — the filename convention the templates state, and safe while nothing links to the note yet. `aliases` is the most important field for a concept note — the export skill derives keyword triggers from it; see Alias Writing Guidance below.

---

## Design Notes

> **Excluded from exports.**

The Design Notes section is the builder's working record. It is not lorebook content.

**Narrative purpose:** What does the existence of this thing make impossible, costly, or inevitable in any scene that touches it? A concept note that cannot answer this question is description, not a constraint. Write the answer here before drafting the Lore and Implications sections — it shapes what to include and what to cut.

**Why this is its own note:** Record why this knowledge warrants a standalone note rather than being embedded in a character, location, or faction note.

**Layer rationale:** Why is this classified as surface, mid, or deep? What would be lost if it were placed one layer lower or higher?

**Open questions:** Unresolved details that may affect how this note is written or how it interacts with other notes.

---

## Lore

The Lore section contains what is true about this thing in the world. This is the main exportable content.

Imported lorebook entries marked `constant` describe standing setting state — that is seed/world material for `project/seed.md`, not a concept note.

Write Lore content at the appropriate layer tone:

### The Three-Layer Structure

The setting deepens as the player invests. Do not front-load. Surface entries establish a mundane world with texture; mid-layer entries acknowledge the old stories; deep entries confirm what the hints implied. Jumping straight to deep lore in early entries kills the effect.

**Surface layer** — What everyone knows. The baseline reality of the setting.

- Geography and physical character of the setting
- Economy — what does this place do, how do people make a living
- Social texture — is the community close-knit, fractured, proud, struggling
- Common local history — the stories everyone tells
- Practical knowledge relevant to the player's daily activities

**Tone:** Matter-of-fact. No mysticism. These entries establish normalcy so that later disruptions of normalcy carry weight. If a surface entry contains a hint like "but some say this is connected to the old stories," you've broken the layer structure.

**Mid-layer** — Things people half-remember. Old stories told as legend but believed a little.

- The old stories — things the community tells as history but with mythic edges
- Wilderness, ruins, old buildings and what people say about them
- Historical events that left marks: a fire, a founding family's story, something that divided the community
- Hints at what lies beneath the surface

**Tone:** Uncertain. Hedged. People who know these stories are not sure they believe them. "They say..." "It's probably nothing, but..." Characters rationalize and deflect.

**Deep layer** — The actual hidden layer — what the hints were pointing toward.

- The supernatural specifics (if the setting has them)
- The setting's true history
- The real origin of the wound
- Any non-human or supernatural entities in detail

**Tone:** Confirmed and weighted. These entries feel like the answer to questions the surface layer raised. Don't explain everything — some things can remain permanent mystery.

**Note on layer classification:** The surface/mid/deep layer on a concept note records authorial intent about pacing. It is not a reliable mechanism for suppressing information from the engine at runtime — whether a given engine can actually gate context on conditions varies. Its value is in shaping how the content is written and in what export tools can do with the metadata.

### The Iceberg Split

Distinct from the surface/mid/deep layer classification. The iceberg split operates *within a single note*, for cases where what people in the world believe and what is actually true diverge.

Where the gap between belief and truth is narratively significant, document both explicitly in the same note:

**Believed:** what characters in the world commonly say, assume, or act on — the public version, the legend, the received wisdom.

**True:** what actually happened, or how the thing actually works underneath the common understanding.

This lets the engine have characters speak and act from belief while the true version constrains what can actually happen and what specific informed characters know.

Not every concept note needs this. Use it only when the gap between belief and truth is a live story element.

---

## Implications

The Implications section covers what follows from this thing being true in the world. It is not a description of the concept — it is an account of what the concept does to scenes.

**Behavioral and social consequences:** What do people do differently because this thing exists? What norms, obligations, or social structures does it produce? What economic consequences does it carry?

**Tensions:** What conflicts, pressures, or contradictions does this thing create for characters or communities that encounter it?

**Costs and limits** (required for rule-bearing concepts): For any concept covering a magic system, institution, cultural practice, belief system, or anything with internal logic that scenes must respect — document what the concept cannot do, what it costs or demands, and what makes it fail, break, or produce unexpected results. A concept documented only by what it can do cannot constrain a scene. One documented by its limits and costs can.

**Example:** A healing magic concept note that says "healers can mend wounds and cure illness" does not constrain anything. One that adds "healing draws from the healer's own vitality — serious wounds leave the healer bedridden for an equal period, and healing the dying risks the healer's own death" constrains every scene that touches it.

**Activation context:** When does this lore become relevant? What situations and phrasings bring it into play? This is where the trigger-context purpose lives — write it here as a specific account of the scenes and moments where this concept matters, rather than as a one-phrase field.

**The key question:** What would a scene look like differently because this thing exists? If the answer is "nothing specific," the Implications section is too thin.

---

## Alias Writing Guidance

The export skill derives keyword triggers from the `aliases` field. Writing good aliases requires thinking about how topics actually come up in dialogue.

**Coverage:** Include every realistic phrasing. If the note is about a specific location, include multiple forms: "the mill," "old mill," "Harrow's mill," "the water wheel." A single overly-precise phrase that never appears verbatim will never trigger.

**Plural and possessive forms:** Matching is typically exact-string. "mill" won't match "mill's" or "mills." Include the forms that will actually appear in dialogue.

**Specificity:** Short generic terms match too broadly. "inn" might fire on "innocent." "well" fires on "well-lit." Prefer multi-word aliases where ambiguity exists: "the inn," "the old well."

**Local names:** Players and characters use the names they know, not the canonical names you used in the note title. Include both.

**Common mistakes:** Single generic word that fires constantly; forgetting local names or synonyms; so many required terms that the combination almost never matches in practice.

---

## Location Notes

Location notes have their own dedicated skill: **`worldbuilder-location`**. Use that skill when creating or deepening any named location.

---

## Background NPC Guidelines

Rather than individual unnamed characters, write guidelines for how the engine should construct background figures. Include in a lorebook entry active from day 1.

Cover:
- What kinds of people live here — occupations, ages, social roles
- What personality tendencies fit the setting's character
- How they should be incorporated when the player engages with them
- What topics they discuss, what they know, what they don't

This gives the engine a construction kit rather than a cast list, producing more varied and naturalistic background interactions than a list of named extras.

---

## Recurring World Events

Event notes — festivals, seasonal observances, recurring world events — have their own skill: `worldbuilder-event`. Use that skill for any recurring or calendar event.

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

## Writing Principles

**Short is usually better.** An entry that injects 50 tokens of precise context beats one that injects 300 tokens of unfocused description. The goal is the right thing at the right moment.

**Don't activate on overly common words.** A keyword of "house" or "old" will trigger on nearly every scene. Keywords should be specific enough that they only fire when the topic is actually relevant.

**Separate entries for separate topics.** Don't pack "the old mill AND the mill family AND the flood of thirty years ago" into a single entry. Split them so each triggers independently and doesn't bloat context when only one is relevant.

**Test the trigger mentally.** Read a sample scene where the topic comes up naturally. Does your keyword set cover the realistic phrasings? Does it avoid triggering on unrelated uses of the same word?

---

## Self-Check Before Marking Complete

**Complete when:** the note can constrain or shape any scene that touches this concept — a scene author reading the note knows what is impossible, what costs something, and what is inevitable because this thing exists.

**Frontmatter**
- [ ] `layer` set; `aliases` complete; other fields per the generated rules

**Description**
- [ ] Written last
- [ ] 1–2 sentences; covers what this knowledge is and when it matters

**Design Notes**
- [ ] Narrative purpose stated (what does this make impossible, costly, or inevitable?)
- [ ] Layer rationale present

**Lore**
- [ ] Content written at the correct layer tone
- [ ] Iceberg split present if belief/truth gap is narratively live

**Implications**
- [ ] Covers behavioral and social consequences, not just restrictions
- [ ] Costs and limits present for rule-bearing concepts
- [ ] Activation context stated

**Over-documented when:** any section adds detail no scene will touch, or duplicates content already in a character, location, or faction note. Concept notes are meant to be short and dense — duplication bloats context for no gain.

**Hand on.** When every item passes, hand the note on to the critic: the critic step runs `worldbuilder-review` with this document and its governing format document. The revision step applies the auto-fix findings; escalated findings go to the human.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
