---
name: worldbuilder-character
description: Use when building or developing a character for an AI-powered RPG or collaborative fiction — creating from scratch, deepening an existing character note, or fixing a character who feels flat, inconsistent, or generating repetitive LLM output.
---

# Character Blueprint

*All prose this skill produces follows `../writing-style.md`. Read it before writing. A creative step starts and ends as `../creative-step.md` says; the interview answers it works from are in the item's Specification, and the questions behind them are in `## Interview` below.*

## Overview

A character for an LLM-powered game is not a description. It is a behavioral specification. The engine handles generic social warmth and distance; the character note supplies the specific: what this character carries privately, what they do when trust is low or high, what their contradiction is.

`card-format.md` is the governing document for entry format and section-scoped writing rules. Read it before writing any entry.

---

## How the Work Runs

A character is written inside a worldbuilder entity item. The definer interviews the human before the item's Specification is approved, using the questions in `## Interview`. The creative step then writes the character note from the Specification, and the critic checks it (see `../creative-step.md`).

**Batch mode** (`automated-workflow.md`): The human sets the goal and the agents execute to completion from source material. Use when backfilling a section across multiple characters, or any workflow without an interview. The quality standard is the same; the process that reaches it is different.

Source material substitutes for human answers. When the Specification names source material (existing character sheets, fiction excerpts, reference images), extract the behavioral content and translate it into card-format entries the same way you would translate a spoken answer.

### Source isolation

When source material substitutes for the interview answers, the same questions apply. The creative step reads the reference documents, asks itself the questions, and translates the answers into entries. The key difference is source isolation: the creative step works from the reference documents, not from any existing card prose. Pre-written prose (especially Soul entries) creates attractor patterns that cause the output to echo the existing card's phrasing rather than building fresh characterization from the evidence.

Process:
1. Read the reference documents. Do not read the character's existing Core sections.
2. Form your understanding of the character from the raw evidence.
3. Work through the questions section by section, translating your answers into entries.
4. For Relationships specifically: write entries as 1-3 sentence behavioral specifications per `relationships.md`.
5. Complete the Completion Checklist and hand on to the critic.

---

## Source Ingestion

When working from source material (game data, existing character
sheets, fiction, wiki references), reference documents come first.
They are made by a prior `worldbuilder-source-ingestion` run, which is
its own item; the creative step reads them and does not build them. Reference documents organize the raw material
into a reviewable evidence base. They live in a `reference/`
subdirectory alongside the character card.

The reference set depends on what the source material provides, but
typically includes:

- **Data profile** — extracted facts: name, role, relationships,
  gifts, schedules, physical data, anything structured.
- **Behavioral evidence** — dialogue and actions that reveal
  personality, organized by context. What the character says and
  does; what others say about them.
- **Calendar/schedule** — daily and seasonal routines, if the
  source tracks them.
- **Narrative arc** — story progression, relationship milestones,
  key events, thematic analysis.
- **Storylines/greetings** — progression-gated events and
  context-gated dialogue, organized by trigger.

Cross-reference multiple sources (game files, wiki, community
resources) when available. The reference folder is the evidence
base for the card; the review can check card entries against it.

Do not skip ingestion to write the card faster. A card written
directly from raw source material without organized reference
documents is harder to review, harder to verify, and harder for
future sessions to update.

---

## Interview

The definer draws on this section. The definer's rounds run on the answer page, and the human's answers go into the item's Specification, where the creative step reads them. The human can override at any point: write entries directly instead of answering, skip questions, or provide source material (existing character sheets, fiction excerpts, reference images) in place of answers.

Ask one question at a time. Wait for the answer before asking the next. Follow threads: when an answer implies something about a different section, surface it immediately and pursue it before changing topics.

### Opening questions

**Starting world state:** Check whether the project has a starting world state document (a project-level reference listing the timeline boundary, which characters are present at the start, and what has already happened before the story begins). If one exists, read it before asking any questions — it governs what counts as pre-story content for Core sections and Relationships versus story content for Story Seeds. If one does not exist, establish the boundary with the human in this interview; the Specification holds it. If a durable starting-state document is wanted, the creative step proposes it as a spin-off (see `../creative-step.md`) and does not create it.

Before the character questions, determine which addon blocks to include. Record the decision in the Specification.

**Relationships:** Ask whether the character is part of a cast. If yes, include the Relationships block.

**Intimate Dynamics:** Check the project-plan flag. If the flag is set, include the block. If absent, do not raise it or ask about it.

**Voice / Dialogue:** Recommend when the character will be exported to platforms that support example dialogue or when voice distinctiveness matters for the project. The human decides.

**Story Seeds:** Included for every character. Every character has narrative scenarios worth specifying — from source material, from their psychology, or invented to serve their arc.

### Core block questions

Background, then Body, then Soul. Every character card has all three.

Within each section, follow the depth-of-access progression defined in `card-format.md`: immediate (what is apparent on first meeting), then over time (what emerges with familiarity), then hidden/foundational (what is rarely seen or never spoken). This progression guides question order, not document structure.

For the Body section, ask about appearance first (preamble), then physical mannerisms (entries).

**Background guidance:** Alongside the depth-of-access questions, ask these two prompts for the Background section.

- Cultural shorthand: "For real-world or historically grounded characters: what music, media, fashion, food, or subcultures does this character belong to or consume? These references activate existing model associations cheaply — a character who listens to top-40 pop resolves differently from one who listens to jazz or punk. Skip for original-fantasy characters where the model has no real-world associations to draw on."
- Location as pressure: "What about where this character lives or grew up creates pressure on them? Economic conditions, climate, social expectations, isolation, proximity to danger? The connection between place and psychology is a Background entry: [location fact] → [what it made true about this character]."

### Addon block questions

**Relationships:** Target perspective and behavior: "What does this character do differently because that person is in the room?" and "How does this character read that person's behavior?" Avoid event-focused questions ("What happened between them?" or "Tell me about a specific time they...") — these produce scene narrations that must then be generalized back into patterns. See `relationships.md` for the 12-archetype framework and coverage requirements.

**Intimate Dynamics:** Ask about attraction expression, hesitation and limits, and any specific dynamic. Ensure at least one friction point. See `intimate.md` for coverage areas.

**Voice / Dialogue:** The human picks 2-4 situation categories from the list in `card-format.md`.

**Story Seeds:** Ask the growth-trigger prompt: "What experience or evidence could make this character reconsider their false belief, shift their value hierarchy, or change a core behavior?" The answers become Story Seeds. This prompt is not a coverage requirement.

---

## Writing the Note

Work through blocks in order: Core, then the selected addon blocks.

When the Specification carries an answer, reproduce the semantic content of the answer, not the phrasing. The input is the fact; the output is the staged behavior the fact produces. Apply the section-scoped writing rules from `card-format.md`. The rules are overridable defaults; the Specification can override any rule for the project.

### Core block

Background, then Body, then Soul. Within each section, follow the depth-of-access progression. The Body appearance preamble covers static appearance at all depths; the depth-of-access grid guides behavioral entries only. Entries land flat under section headings.

### Addon blocks

Relationships, then Intimate Dynamics, then Voice / Dialogue, then Story Seeds.

**Relationships:** Each entry is a 1-3 sentence behavioral specification stating what this relationship makes the character do, avoid, or become. Entries are written from the character's perspective (swap test: if swappable to the other card, too neutral). No scene narration — entries describe repeatable behavioral patterns, not specific events.

When working from source material, write relationships from the reference documents directly. Do not read the character's existing Core sections while writing relationships. The reference documents are the evidence base; the Core sections are pre-written prose that creates convergence patterns in the output.

**Intimate Dynamics:** Cover the areas in `intimate.md`, with at least one friction point.

**Voice / Dialogue:** For each chosen category, write a composite dialogue snippet showing the character pulling from multiple Core areas at the same time. Include enough scene context to establish the situation.

**Story Seeds:** Work through Story Seeds after Voice / Dialogue (or after the last selected addon block). Draw from three sources: explicit events in source material, implicit scenarios suggested by the character's psychology and relationships, and invented hooks that serve the character's arc. Consolidate multi-step source arcs into single setup beats — describe the premise and the character's stake, not a scripted sequence. Write for freeform play: setups, not outcomes. Aim for the high end of the target range (5-12); thin coverage is a bigger risk than generous coverage. See `card-format.md` for entry format, writing rules, and distinctions from other sections.

---

## Coverage Checking

### After each Core section

Report depth-of-access observations: which columns (immediate, over time, hidden/foundational) have entries, and which are thin or empty. This is advisory, not deterministic. Return follow-up questions for under-represented columns with the step's output.

### After the full Core block

Check for missing required doctrine entries (defined in `card-format.md`). The required entries are:

1. Core want (behavioral, Soul)
2. Core fear (behavioral, Soul)
3. False belief the character acts on (Soul)
4. Value-conflict stance (Soul)
5. At least one unresolved tension or competing pull (Soul)
6. Values with costs (Background or Soul)
7. Protective strategy (behavioral, Soul)

Missing required entries must be addressed before finalization or waived in the Specification with a recorded reason.

---

## Working Document

Entries accumulate in the character note as the creative step writes them. Each section is a markdown heading. Entries are bullet points under their section heading. The Body appearance preamble (prose before the first bullet) and Story Seeds (labeled prose blocks) are recognized exceptions.

The document may carry optional annotations (grid position, coverage area) during creation. These are a working aid; export strips them.

---

## Design Notes

Design Notes is the builder record. It is excluded from all exports. Two H3 subheadings:

### Session Notes

Interview capture: what the human said they wanted this character to be, taken from the Specification. Written before entries are drafted. Raw intent, plain language, bullet points. Future agents revisiting this character read Session Notes first to understand original intent.

### Builder Context

Narrative function, external references, design decisions, open questions. Bullet points. Leave blank if there is nothing worth capturing. Do not pad.

---

## Frontmatter and File Naming

Frontmatter is defined by the project's OKF registry; `new_doc.py` stamps it at creation. The script produces a date-prefixed filename; rename the fresh note to the character's name (e.g. `notes/Maren Holt.md`) before adding content.

**Description field:** the cast navigation summary. Who this character is in the world, their key traits, their place in the social ecosystem. Described, not prescribed: no relationship recommendations, no design rationale. Written last, after the full blueprint is complete.

---

## Story Notes

Story possibilities for this character live in separate story notes, not in the character note. When you have enough clarity on a character's arc, propose a story note with intention scope as a spin-off (see `../creative-step.md`). See `worldbuilder-story` for story note structure.

Story Seeds (the addon block) are character-local scenario sketches —
hooks short enough to live inside the character card. A story note is
a full narrative document with arc structure, scope, and its own
lifecycle. Story Seeds may reference story notes for arcs they
participate in. If a scenario needs more than 2-4 sentences to
describe, it belongs in a story note.

The introduction note is also a story note (introduction scope). Propose it as a spin-off when you have enough character clarity to know where and how the player first meets this character.

---

## Post-Group Sync Pass

After completing a household group or batch of characters, run a relationship sync pass before moving on. Characters develop during the blueprinting sequence. A character written later may shift in ways that make an earlier character's relationship entry inaccurate. Check the group's notes against each other: are named relationships still consistent? Update when the sequence reveals something that changes the picture.

---

## Completion Checklist

The note stays on an open status tag while work is in progress. Mark it `complete` when every item below passes.

- [ ] All required doctrine entries present or explicitly waived with a recorded reason
- [ ] Each Core section (Background, Body, Soul) has at least one entry. Target ranges in `card-format.md` are guidance, not gates
- [ ] Reference documents from a prior ingestion run read when working from source material
- [ ] Story Seeds section present with entries (every character; 5-12 target range)
- [ ] Other selected addon blocks completed (Relationships, Intimate Dynamics, Voice / Dialogue as determined in the Specification)
- [ ] No trait adjectives anywhere in the note. Each replaced by the behavior that earned it
- [ ] Entries follow section-appropriate writing rules per `card-format.md`
- [ ] `### Session Notes` present with the interview capture
- [ ] `### Builder Context` present as applicable; not padded
- [ ] Story notes proposed as spin-offs for any known character arcs
- [ ] `description` field written last and reflects the completed character
- [ ] Handed on to the critic: the critic step runs `worldbuilder-review` with this document, `card-format.md` as the governing format document, and all reference material used to produce the document. The revision step applies the auto-fix findings; escalated findings go to the human.

---

## Review

None here — the entity notes are reviewed at the critic step of the worldbuilder entity item; no deliverable checks off at this skill.
