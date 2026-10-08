---
name: worldbuilder-world-foundation
description: Use at the start of a new worldbuilding project to establish setting structure and produce the seed document. Also use when auditing an existing world for structural gaps in household design, cast architecture, or thematic grounding.
---

# World Foundation

*All prose this skill produces follows `../writing-style.md`, with two exceptions. The World Introduction and the Opening Situation are written evocatively rather than as specification, and the style reference excludes prose of that kind by its own terms. Every other section of the seed follows it. Read it before writing.*

## Overview

This skill covers two things: the structural decisions that shape the world, and the seed document that captures them. Work through the decisions first; the seed document is the output, not the starting point.

The seed document is a starting point, not a finished world — it will grow in directions it does not anticipate.

This skill is the builder's instruction for the Foundation work item. The definer of that item runs the interview in `## Interview` below and records the answers in the item's Specification. The builder reads the Specification and writes the seed document from it, as the Seed Document section describes. The builder does not ask the human questions: a gap in the Specification is returned as a question.

---

## Interview

The definer draws on the two parts of this section, the opening act and the six foundational questions. The definer's rounds run on the answer page, and the human's answers go into the item's Specification.

### Opening Act: Ingestion

Before asking any questions, check whether the human has reference material to provide.

Ask: "Do you have any existing material for this world — notes, documents, previous writing, URLs, or reference media you want to draw from?"

If yes:
- Run `scraibe:ingest` first — each source becomes a reference document with provenance before anything is extracted from it
- Then extract any decisions already made (setting name, tone, existing characters, world details) from the reference documents
- Note contradictions or gaps to resolve during the questions phase
- Do not discard or override anything the human has already decided

If no: proceed directly to the six foundational questions.

---

### Intimate-dynamics scope

Ask once: does this project include explicit intimate content — all romance-eligible characters, a specific subset, or none? The answer goes into the Specification. The decision is not revisited character by character.

### The Six Foundational Questions

Work through these before the seed document is written. They are not a form to fill in — they are decisions to make. Stop and ask the human at each one. Do not assume or fill in gaps.

#### 1. What is the setting's wound?

Every good setting has something wrong with it — something it lost, something that divided it, something it has been unable to face. This determines what the player's presence means, what the opening arc is, and what long-term healing looks like.

Examples:
- An institution in decline while a hostile outside force moves in
- A guardian or protector who can no longer perform that function
- A founding betrayal the community has never fully reckoned with
- A loss so old it has become local myth

#### 2. What is the community's character?

Not just a name — its personality. Is it proud of its history or embarrassed by it? Tightly knit or full of old grudges? Welcoming to outsiders or suspicious? The community's personality is the default filter every character's behavior runs through.

#### 3. What is the player's connection to this place?

Inherited property? Drawn here by something? Washed up by accident? The connection determines who knew the predecessor, what the player's presence means to different characters, and what stakes the player has from day one.

#### 4. What is the setting's hidden layer?

If the setting includes supernatural elements, the origin shapes tone:
- A catastrophe long ago (the world is in recovery; magic is a relic)
- A choice made by the founders (something was suppressed or traded away)
- A natural cycle (the world breathes in and out; this is an exhale)
- Something ongoing (the change is still happening; something is causing it)

If the setting has no magic, this becomes: what is the setting's concealed depth? Every good setting has something beneath the surface — a secret, a history, a truth the surface doesn't advertise.

#### 5. What is the era?

Approximate technology and cultural reference point. Affects every character's daily life and what kinds of problems are plausible:
- Contemporary with poor infrastructure
- Early modern (electricity and transport, no internet)
- Pastoral (no technology, not medieval)
- Fantasy-modern (technology alongside magic)

#### 6. How many household clusters, and what are they?

Design the setting as 6–8 household clusters before naming any individuals. Characters gain meaning from their relationships with each other, not just with the player.

---

## Household Design

For each household before assigning any characters:

```
HOUSEHOLD NAME / LOCATION
Function: role in the community economy or social structure
Internal tension: what is unresolved or complicated between the members
Inter-household connections: which other households are tied to this one, and how
Narrative hook: what is interesting about this household as a unit
Trajectory: where are they headed if nothing changes — the slow drift of their situation
```

**Every household needs:**
- A physical location
- A primary function in the setting's economy or community
- An internal tension
- At least one connection to another household
- A trajectory — this is what makes household dynamics feel like they exist in time

Characters who exist in isolation from every other household are underwritten. The household structure is what gives the cast its web of meaning.

---

## Cast Architecture

Design the cast structure before naming individuals.

### Romance candidate archetypes

Romance-eligible characters should collectively cover these six slots across gender presentations.

1. **Initially hostile / cold** — earns warmth through player investment; strongest attachment when won
2. **Warm / immediately approachable** — accessible early-game anchor
3. **Quirky / alternative** — operates outside social norms
4. **Ambitious / driven** — has independent goals that don't revolve around the player
5. **Creative / dreamy** — artistic or philosophical orientation
6. **Wild card** — resists easy categorization

**Anti-redundancy check:** If two characters occupy the same slot, verify they differ substantially in execution — different emotional tone, different obstacle, different role in the setting. The same archetype expressed the same way produces redundancy that players notice.

### Non-romance archetypes to place somewhere in the cast

- Authority figure — has own agenda beyond the player; satirizes small-community governance
- Mentor / elder — carries the setting's memory, connects player to local history
- Elderly couple or widow/widower — anchors mortality and long-term commitment
- Child or young teenager — creates stakes for adult characters, multiplies adult complexity
- Outcast / philosopher — lives outside the norm by choice, challenges assumptions about good lives
- Magical practitioner or equivalent — knows more than they say; bridge between surface and hidden layers
- The one who left and came back (or should have left and didn't)
- Someone carrying a secret the surface doesn't reveal

### Negative-track characters

At least 2–3 characters should have meaningful content at low or negative influence — not just distance, but legitimate grievance or opposition. The player should be able to genuinely wrong someone, or encounter someone whose hostility has nothing to do with player behavior.

### Cast size targets

- Default: 8 main / 16 side characters
- Range: 6–10 main, 6–20 side
- The coverage check in Wide Phase Planning below verifies ratio, archetype coverage, and household balance before the roster is confirmed complete

---

## Wide Phase Planning

The Wide phase turns the seed into notes. The planning artifact is `project/plan.md`, created by setup: its Phase Status table tracks where the project is, and its `## Cast Plan` section holds the confirmed roster. Update the table at each phase transition; artifacts are ground truth, not the table — if the table says done but the note is missing or thin, believe the note.

### Cast planning

Build the roster from the household design, with user input, before any character note is written.

The user seeds the cast — names they already have, roles they know they want, characters with personal significance. From each seed, branch through relationships: who is in their household, who do they conflict with, who do they depend on? Fill structural gaps (unfilled archetype slots, households without characters) with proposals for the user to accept, modify, or reject. Never assign a character to a slot without the user's knowledge.

Record the Specification's answer to the intimate-dynamics scope question (asked once, in the Interview) in `project/plan.md`, and flag affected cast entries with `Intimate Dynamics: Yes`. Record the confirmed cast in the `## Cast Plan` section of `project/plan.md`. This is a planning document, not the character notes themselves — each character note is created later and carries the authoritative information.

Cast plan entry format:

```
**[Name]** — [Household] | [Type: Major/Supporting] | [Species/age]
Role: [one or two phrases]
Archetype: [slot from cast architecture]
Key relationships: [named, one per line]
Intimate Dynamics: Yes  ← only if applicable; omit line if not
Summary: [2–3 sentences of behavioral character, not physical description]
```

Coverage check before declaring the cast plan complete — verify against the seed's themes and household structure:
- All 6 romance archetype slots filled across gender presentations
- Non-romance archetypes placed: authority figure, mentor/elder, elderly anchor, child or teen, outcast/philosopher, practitioner, the one who left (or didn't), the secret-carrier
- 2–3 characters with meaningful negative-track content
- Every household has at least one character assigned
- Default count: 8 main / 16 side (range: 6–10 main, 6–20 side)
- Anti-redundancy check: no two romance candidates filling the same slot with the same execution
- The setting's wound from the seed is visible in at least two or three unrelated characters' motivations

### Phase completion criteria

Per-phase "done" definitions. If any item is unresolved, surface it to the user before marking the phase done in `project/plan.md`.

**Seed complete** — `project/seed.md` contains: all six foundational questions answered; Setting Summary; Genre & Tone; Inspirations and Tonal Inspirations with specifics; 8–12 Key Tropes & Themes; Community (social and emotional identity, not physical); World Introduction; Opening Situation; a locations list of 10–14 named locations, one sentence each; art style reference; musical theme; all 6–8 household clusters with function, internal tension, inter-household connections, trajectory, and narrative hook; no individual character names — household types and counts only; every household has at least one named connection to another household.

**Direction complete** — `project/direction.md` has all required sections (romance pacing, hidden layer handling) and the opening arc sketched at a broad level. A brief but complete document beats a detailed stub.

**Concept and event notes complete** — all three layers present (surface, mid, deep); background NPC guidelines concept note written; event notes written for all named recurring events; each note passes its skill's self-check.

**Story notes complete** — opening arc note written (evocative, not scripted); key intention notes written for major story possibilities.

**Location notes complete** — every named location from the seed has a note; each passes the `worldbuilder-location` self-check.

**Faction notes complete** — every household cluster from the seed has a faction note; each passes the `worldbuilder-faction` self-check.

**Cast plan complete** — the coverage check above passes; every entry has household, type, species/age, role, archetype, key relationships, summary; intimate-dynamics flags set where applicable.

**Character notes complete** — per character, the self-check in `worldbuilder-character` is the authoritative gate.

**Relationship review complete** — after all character notes: every character's Relationships section read against the full current cast; entries that no longer reflect the most interesting dynamic updated; this is not a symmetry check — asymmetry is often the most interesting thing.

**Contradiction validation complete** — every note checked against the notes it links to for factual conflicts; every character note checked against its factions; every flagged contradiction resolved with the user, none silently discarded.

**Export** — `worldbuilder-ainime-export` owns its own gate.

### Parallel execution

Once the seed is `complete`, concept, event, story, location, and faction notes are all independent of each other — any can proceed in any order, in parallel. Location and faction notes give character notes context, so run them first where possible.

What blocks on what:
- Everything blocks on the seed.
- The direction document comes before any Wide-phase notes.
- Character notes block on the cast plan. Once the cast plan exists, individual characters are independent of each other — parallelize aggressively; writing a large cast sequentially in one session degrades quality.
- Relationship review blocks on all character notes; contradiction validation blocks on relationship review; export blocks on contradiction validation.

When dispatching parallel character work, each dispatch needs: the relevant household section of the cast plan, the target character's full cast plan entry, which skill to invoke, and an explicit constraint not to modify other characters' notes or the cast plan.

---

## Seed Document

Once the foundational questions and household structure are settled, fill in `project/seed.md`. The document already exists — `worldbuilder-setup` created it — so this skill writes its body, nothing else. When the user confirms the seed is complete, set its status tag to `complete`.

The seed is a platform-agnostic project proposal. Write each section as plain prose under natural headers — this is not an export format, it is the creative document that export skills derive from. The ainime export skill handles field mapping.

### Sections

**Setting Summary**
Time, place, society, and general feel. The always-active context — concrete and specific.

**Genre and Tone**
Primary genre, tonal range (how dark, how light), and any content notes.

**Inspirations**
Source games and media, one per line. Include what specifically is drawn from each rather than just the title ("Stardew Valley — farming life rhythm and community bonds" not just "Stardew Valley").

**Tonal Inspirations**
Other media capturing the right feel — films, books, music, anime. One per line with what's being borrowed tonally.

**Key Tropes and Themes**
8–12 recurring concerns of this world. Both setting tropes and emotional themes.

**Community**
The community's social and emotional identity — not its physical description, not a repeat of the Setting Summary. How the community behaves and feels as a social entity.

**World Introduction**
Pre-game text the player reads before starting. Sets expectations for tone and situation. This section is written evocatively and is exempt from the style reference. No other section of the seed is.

**Opening Situation**
The situation the player arrives into. Evocative, not scripted — establishes the stage rather than dictating what happens. Cover: the setting's visible state on arrival, the immediate invitation for engagement, what the player's arrival means to the community. This section is written evocatively and is exempt from the style reference. No other section of the seed is.

**Story Direction note**
Do not write story direction content into the seed. `project/direction.md` is a separate project document, already created by setup; fill it with `worldbuilder-story` after the seed is confirmed, before any Wide-phase notes.

### Additional seed outputs

**Locations list**
Named locations with one sentence each on function and character. 10–14 locations. Not full location notes — a spatial anchor for the Wide phase. Full location notes come later.

**Art style**
Desired visual aesthetic: overall style (anime, painterly, pixel, etc.), color palette tendencies, reference works if any.

**Musical theme**
Desired audio atmosphere: genre, tempo, instrumentation reference, how mood shifts across emotional registers. Reference tracks or artists if helpful.

---

## Working Principles

**Households before individuals.** Characters gain meaning from their relationships with each other. A character whose card doesn't reference anyone else in the setting is underwritten.

**The setting's wound is structural.** It should be visible in at least two or three unrelated characters' motivations. If the wound only affects one character, it's a personal subplot, not the town's wound.

**The hidden layer is structural, not explained.** The world doesn't owe an explanation. Early encounters hint; later encounters acknowledge; deep lore confirms. Front-loading reveals kills the effect.

**All characters get equal depth.** The main/side toggle is a player-facing engagement setting, not a signal to write a thinner character card.

**Ask at every decision point.** The cost of fixing errors in generated documents is higher than the cost of answering an upfront question. The definer asks during the interview. When the builder finds anything ambiguous in the Specification, it surfaces it as a question and does not fill the gap.

---

## Review

The seed document is a deliverable of the Foundation item. The scraibe adversarial-review skill defines this block's shape and runs the loop.

- **Deliverable:** the seed document, `project/seed.md`, and the direction document, `project/direction.md`.
- **Shape:** document — the rounds are capped and the human's approval is the gate.
- **Criteria:** the "Seed complete" entry under Phase completion criteria in this skill, the Sections and Additional seed outputs lists under Seed Document, and `../writing-style.md` (the World Introduction and the Opening Situation are exempt, as the style note at the top of this skill says).
- **Scope:** named files — `project/seed.md` and `project/direction.md`.
- **Reference inputs:** the source material the human provided and the reference documents made from it; the item's Specification.
- **Stakes default:** durable.
- **Overrides:** none.
