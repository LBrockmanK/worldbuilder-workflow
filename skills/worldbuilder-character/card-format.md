# Card Format Definition

*Reference document for `worldbuilder-character`. Defines the block model, entry structure, and section-scoped writing rules for character cards.*

---

## Core block

Three sections organized by information type. Every character card has all three.

### Background

Facts and formative events. What is true about the character. No behavioral framing.

**Entry format:** Fact pairs. A formative fact and what it made true.

**Target range:** 4-8 entries.

**Example entries:**
- Grew up working-class in a trade city, left at 18 → never returned to the neighborhood, never explained why
- Trained as a scribe for 6 years → can read legal documents but has never written one for pay

### Body

Physical presence and habits. What you see and experience physically.

**Appearance preamble:** Body opens with short descriptive prose
(sentences or descriptive clauses) covering the character's static
physical appearance. The preamble is exempt from the staging test.
Orwell co-anchor and trait-word ban apply. No meta-vocabulary from
the builder abstraction layer. Content: hair, eyes, skin, build,
distinguishing physical features, default or seasonal clothing, and
hidden static features (scars, marks, tattoos) when relevant —
everything about what this person looks like, regardless of
depth-of-access.

**Entry format:** One stageable sentence per entry. Describes
physical behavior that can be observed.

**Target range:** 3-5 entries. Thin Body sections are acceptable when nothing about the character's physicality is distinctive. Do not force entries.

**Example entries:**
- When she enters a room she does not know, she finds a wall or corner first. She positions herself to watch before anyone watches her.
- He talks with his hands when he is confident and folds his arms when he is not.

### Soul

Psychological and social behavior. How they think, feel, and act.

**Entry format:** Prose sentences following the When/Behavior/Because structure embedded naturally. The formula is a construction guide, not a labeling scheme.

> When [trigger], they [behavior], because [underlying reason].

**Target range:** 5-8 entries.

**Example entries:**
- When challenged, she responds with certainty, treating doubt as a personal insult rather than a reasonable position, because the last time she showed uncertainty, someone took her job.
- When someone is struggling, he drops everything to help, partly because he cares, partly because being needed is the only time he feels valuable.

---

## Depth-of-access grid

A 3x3 grid crossing the three information-type rows with a depth-of-access progression. This is a Q&A coverage tool, not a document structure. Entries land in flat sections (Background, Body, Soul). The Q&A process uses the grid to guide question order, and a coverage check flags under-represented columns. The grid maps to how roleplay unfolds over time: column 1 early, column 2 as the relationship develops, column 3 in moments of depth.

| | Immediate | Over time | Hidden / foundational |
|---|---|---|---|
| **Background** | Known history, visible circumstances | Things they let slip, stories that emerge | Formative wound, what they never tell |
| **Body** | Surface features, first impression, obvious mannerisms | Subtle habits noticed with familiarity | Physical tells revealed with familiarity — the preamble holds static hidden features (scars, marks) |
| **Soul** | Social persona, default behavior with strangers | True self that emerges with trust | Motivational engine. Core want, fear, false belief, value-conflict stance |

---

## Required doctrine entries

A card is not finalized until all of the following are present or the user explicitly waives specific entries with a recorded reason.

1. **Core want** (behavioral, Soul). How the want shows in action, not a label. Provenance: Character Builder v3's Core slot; community consensus on motivational engine.

2. **Core fear** (behavioral, Soul). What the character does when the feared outcome approaches. Observable action, not internal dread. Provenance: same as core want; fear and desire form the motivational axis.

3. **False belief the character acts on** (Soul). A belief held wrongly and acted on with confidence. The belief and the resulting behavior must both be specific. Provenance: Character Builder v3; described as "a scene generator" in the Hoplight review.

4. **Value-conflict stance** (Soul). Which way they go when values collide with morality, the lever that tips them, how guilt manifests. Provenance: Character Builder v3; graduated in convergence retest (behavioral influence 3/4 scenarios, the only functionally validated doctrine entry).

5. **At least one unresolved tension or competing pull** (Soul). Resolved states become shortcuts models can collapse to. Provenance: community sources in causal character writing research.

6. **Values with costs** (Background or Soul). At least one top value with its stated price. A value without a cost is decoration. Provenance: Character Builder v3 via Hoplight review.

7. **Protective strategy** (behavioral, Soul). The habitual first response to any perceived threat — what the character does before they identify what they are afraid of. Observable action, not a coping label. Provenance: Writer's Workbench 'protective strategy' field; Character Codex 'override specification'; community consensus on default defensive behavior.

**Finalization gate:** the card is not finalized until every required entry above is present or explicitly waived.

---

## Addon blocks

### Relationships

Named dynamics with specific other characters. One entry per relationship. Relevant for cast-based worldbuilding; not needed for standalone characters. Only characters already in the character's life before the story begins get entries; characters who arrive during the story are narrative events, not standing relationships, and belong in Story Seeds. The 12-archetype framework and coverage requirements are defined in `relationships.md`.

### Intimate Dynamics

Optional. The user decides at project planning whether a character includes this block. Entries are behavioral prose in the same format as Soul (When/Behavior/Because embedded naturally). Three coverage areas with 1-2 entries each:

- Attraction expression: how they show interest
- Hesitation and limits: what makes them slow down or hold a boundary
- Specific dynamic (if applicable): behavioral signature and the emotional need it serves

Mandatory friction point: one internal contradiction in intimate behavior. Full reference in `intimate.md`.

### Voice / Dialogue

Recommended when the character will be exported to platforms that support example dialogue or when voice distinctiveness matters for the project. 2-4 composite dialogue snippets, each showing the character pulling from multiple Core areas at the same time.

**Situation categories** (the user picks 2-4 relevant to their character):
- Casual / social
- Conflict / pressure
- Vulnerability / intimacy
- Authority / power dynamic
- Alone / internal

Each snippet includes enough scene context to establish the situation. The working sheet notes which Core areas each example exercises as a coverage sanity check. Include this block when voice distinctiveness matters for the project or when the target platform supports example dialogue.

### Story Seeds

Every character should have Story Seeds — narrative setups the target
platform can grow in any direction.
They provide the character's stake in a scenario and the conditions
that could trigger it, not a scripted outcome. Labeled prose blocks:
each entry has a short title, a trigger/condition note, and 2-4
sentences of scenario prose describing the setup (where and when),
the key action or exchange, and what the event reveals about the
character. Prose follows the action-line convention. Staging test
applies. Orwell co-anchor applies. No meta-vocabulary. Condition
notes are factual, not prose-styled.

**Target range:** 5-12 entries. Err on the side of more rather
than fewer — entries can be pared down later, but gaps in coverage
leave the platform with nothing to work from. A thin Story Seeds
section is a bigger problem than a generous one.

**Required entry — Introduction:** Every character's Story Seeds
must include an Introduction entry describing the character's first
meeting with the player. The trigger/condition states when and where
the player would plausibly encounter the character for the first
time. The scenario prose describes what the player sees, what the
character does, and the first impression the character makes. Source
material for introductions includes first-time greeting text,
opening cutscenes, and the character's daily routine and location.
Characters who arrive mid-story describe the circumstances of their
arrival. Characters who are not physically present (off-screen
family, referenced figures) describe how the player first learns
about them — through another character's mention, a letter, or a
photograph.

**Sources for Story Seeds:**
- **Explicit:** events defined in source material (heart events,
  quest progressions, story milestones).
- **Implicit:** scenarios implied by the character's psychology,
  relationships, or role but not scripted in source material
  (a gossip-lover trying to set up a romance in town, a reluctant
  leader being forced to delegate, a daydreamer missing something
  important).
- **Invented:** scenarios that serve the character's arc even when
  no source material exists. Every character has developmental
  potential; Story Seeds make it available to the platform.

**Writing for freeform play:** The target platform is freeform —
events can diverge from any scripted path. Write Story Seeds as
setups, not outcomes. Describe the situation that could arise and
what the character would do, not the resolution. A multi-step arc
from source material (e.g. a five-event quest chain) becomes one
Story Seed that establishes the premise and the character's stake
in it, not a sequence of scripted events.

**Relationship to lorebook:** Story Seeds provide the character's
stake in a scenario. Factual context that supports the scenario
(lore, mechanics, history) belongs in lorebook entries (location,
concept, or event documents), not in the Story Seed itself. A Story
Beat can reference lorebook by name without reproducing it.

When a Story Seed requires lorebook that does not yet exist,
create a stub entry in the character's folder (e.g. a concept or
location note alongside the card) to be merged into the project's
main lorebook set later. This avoids blocking card completion on
the full lorebook pipeline. Note the stub in the character's
Design Notes so the merge is not forgotten.

**Distinction from other sections:**
- vs. Relationships: Relationships describe standing dynamics with
  characters already present before the story begins. Interactions
  with characters who arrive during the story are Story Seeds.
- vs. Voice/Dialogue: Voice/Dialogue shows speech patterns. Story
  Beats describe specific events that could unfold.
- vs. calendar events: calendar events are scheduled
  occurrences. Story Seeds are one-time or progression-gated.
  A dated one-time event with character-specific narrative (e.g. a
  festival date at a milestone) is a Story Seed referencing the
  calendar context.
- vs. story notes: Story Seeds are character-local hooks inside the
  card. Story notes are full arc documents outside it.

---

## Section-scoped writing rules

These are overridable defaults. The user can override any rule for their project.

### Background entries

Background is factual, not behavioral. The following rules apply:
- **Orwell co-anchor:** shortest word, active voice, cut waste
- **No meta-vocabulary** from the builder abstraction layer

The staging test, action-line convention, and fact-to-manifestation transformation do not apply to Background. Background states what is true; other sections handle how that truth manifests as behavior.

### Body and Soul entries

Body and Soul are behavioral. The following rules apply:
- **Action-line convention:** present tense, only what can be seen or heard in a scene
- **Staging test:** "Can a director stage this?" The Because clause in Soul entries is exempt. It may name an internal state if the state is specific.
- **Trait-word ban:** no adjective labels. Behavior earns the word. Replace the label with what happens that makes people reach for it.
- **Orwell co-anchor:** shortest word, active voice, cut waste
- **Fact-to-manifestation:** reproduce semantic content from the user's answer, never reproduce the phrasing. The input is the fact; the output is the staged behavior the fact produces.

For the full writing doctrine, see `../writing-style.md`.

---

## Starting world state

Core sections (Background, Body, Soul) and Relationships describe
who the character is at the project's declared starting point — the
moment the story begins. Events, outcomes, and characters that
arrive after that point are story content and belong in Story Seeds.

The starting world state is a project-level document, not part of
the card format. When a project declares one, it is the authority on
what counts as pre-story. When no starting state is declared, the
card author applies their best judgment and the reviewer flags
entries that appear to reference progression-gated events.

Voice / Dialogue scenes are composites illustrating the character's
voice. They should depict situations plausible at the starting
state, not scenes from specific story events.

## Player references

The player (the user interacting with the character on the target
platform) is not referenced in Core sections or Relationships. These
sections describe who the character is independent of any specific
interlocutor.

Story Seeds may reference the player — these are progression-gated
events that involve the player by design. Voice / Dialogue may
reference the player — these are composite scenes showing how the
character talks to the person in front of them.

In dialogue lines, use `{{user}}` for the player's name. In stage
directions and Story Seeds prose, use "the player." Do not use
source-specific or project-specific player names.

## Working document conventions

Entries accumulate under section headings as bullet points. The document may carry optional annotations (grid position, coverage area, relationship archetype) during creation; export strips these. Annotations are a working aid, not part of the card's final content.

Two recognized exceptions to the all-bullets convention: the Body
appearance preamble (prose before the first bullet point) and Story
Beats entries (labeled prose blocks with bold title, em-dash
condition, and scenario prose). Export strips working annotations
but preserves both formats.

---

## Review criteria

Rules the pre-completion review enforces, organized by scope. Each
check names the rule and its source location, then describes the
violation pattern — it does not reproduce the full rule text.

### Checks

**Document-level:**
- Required doctrine entries present or waived (this document,
  Required doctrine entries section). Violation: missing entry with
  no recorded waiver.
- Each Core section has at least one entry (this document, Core block
  section). Violation: empty section.
- Slop-phrase scan (`docs/slop-phrases.md`, full checklist).
  Violation: any listed phrase present in card prose.
- Writing doctrine compliance (`skills/writing-style.md`;
  `.claude/adr/0004-action-line-style-model.md`). Violation: any
  failure mode listed in those documents.
- Starting-state scope (this document, Starting world state section).
  Violation: entry in Background, Body, Soul, or Relationships
  references an event, outcome, or character that does not exist at
  the project's declared starting point. Story Seeds and Voice /
  Dialogue are exempt. When no starting state is declared, flag
  entries that appear to reference progression-gated events and
  escalate for confirmation.
- Player reference scope (this document, Player references section).
  Violation: the player is referenced by name or role in Background,
  Body, Soul, or Relationships. Story Seeds and Voice / Dialogue may
  reference the player. Dialogue uses `{{user}}`; stage directions
  use "the player." Source-specific player names are violations.

**Background entries:**
- Fact-pair format (this document, Background section). Violation:
  result half contains behavioral framing instead of a concrete fact.
- No meta-vocabulary (this document, Section-scoped writing rules —
  Background).
- Orwell co-anchor (this document, Section-scoped writing rules —
  Background).
- Trait-word ban (`skills/writing-style.md`, trait-word ban).
  Violation: trait adjective anywhere in a Background entry.

**Body preamble:**
- Short descriptive prose before the first bullet (this document,
  Body section — Appearance preamble). Violation: preamble formatted
  as a bullet entry.
- Staging test exempt (this document, Body section — Appearance
  preamble).
- Orwell co-anchor and trait-word ban apply.

**Body entries:**
- Entry format (this document, Body section) and action-line
  convention (Section-scoped writing rules). Violation:
  multi-sentence entries, past tense, internal states.
- Staging test (this document, Section-scoped writing rules — Body
  and Soul). Violation: entries a director cannot stage.
- Trait-word ban. Violation: adjective labels instead of behavior.

**Soul entries:**
- Entry format (this document, Soul section). Violation: missing
  When trigger, missing Behavior, missing Because reason.
- Action-line convention (Section-scoped writing rules — Body and
  Soul). Violation: internal states outside the Because clause.
- Staging test; Because clause exempt.
- Trait-word ban.

**Relationship entries:**
- Behavioral claim (`relationships.md`, What an entry is). Violation:
  entry states the relationship rather than what the relationship
  makes this character do, avoid, or become.
- Scene-narration ban (`relationships.md`, What an entry is not).
  Violation: entry recounts specific exchanges, quotes dialogue, or
  narrates events instead of describing repeatable behavioral
  patterns.
- Perspective-focus and swap test (`relationships.md`, per-entry
  self-review). Violation: entry reads as a neutral account that
  could appear on either character's card, or describes the other
  character's internal states.
- Archetype annotation present (`relationships.md`, Writing
  Relationship Entries section). Violation: missing archetype
  working annotation.
- Pre-story characters only (this document, Addon blocks —
  Relationships). Violation: entry for a character who arrives
  during the story.
- Trait-word ban. Violation: trait adjective describing a related
  character.
- Coverage requirements (`relationships.md`, Coverage Requirements
  section). Violation: count below the minimum for the character's
  role.

**Intimate Dynamics entries (when included):**
- When/Behavior/Because format, same as Soul (this document, Addon
  blocks — Intimate Dynamics; `intimate.md`).
- Three coverage areas present with 1-2 entries each
  (`intimate.md`).
- Mandatory friction point present (`intimate.md`). Violation:
  no internal contradiction in intimate behavior.

**Voice / Dialogue (when included):**
- 2-4 composite snippets (this document, Addon blocks — Voice /
  Dialogue). Violation: count outside range.
- Each snippet pulls from multiple Core areas (this document, Addon
  blocks — Voice / Dialogue). Violation: snippet exercises only one
  area.
- Sufficient scene context to establish the situation.
- Scene situations are plausible at the starting state (this
  document, Starting world state section). Violation: scene depicts
  a specific progression-gated story event rather than a
  starting-state situation.

**Story Seeds entries (when included):**
- Action-line convention, staging test, Orwell co-anchor (this
  document, Addon blocks — Story Seeds).
- No meta-vocabulary.
- Condition notes are factual, not prose-styled.

### Exempt

- **Design Notes:** exempt from all review checks. Design Notes are
  excluded from all exports and exist as a builder record.
- **Working annotations** (doctrine labels like `*(core want)*`,
  `*(false belief)*`): stripped at export; drafting aids, not
  meta-vocabulary violations.
- **In-world quoted text:** exempt from the trait-word ban. Text
  quoted from the source material (game dialogue, in-world documents)
  is not prose the card author chose.
- **Voice / Dialogue speech lines:** in-character dialogue follows
  the character's speech patterns, not the card-body writing rules.
  Stage directions and situation descriptions within Voice / Dialogue
  are not exempt.

### Judgment calls

The general rule (D4 of the governing spec): auto-fix when the
violation is clear AND the repair is safe (mechanical restructuring
only). Escalate when either is ambiguous.

Character-card-specific guidance:
- Splitting a multi-sentence Body entry into one sentence: auto-fix
  when the entry contains one core behavior and the extra sentences
  are elaboration. Escalate when the entry contains multiple distinct
  behaviors that each need their own entry.
- Removing an internal state from a Soul entry: auto-fix when the
  internal state can be replaced by the observable behavior already
  described in the entry. Escalate when removing it would lose the
  entry's meaning and a replacement behavior must be sourced from
  reference material.
- Reformatting a bullet preamble to prose: always auto-fix (purely
  mechanical).
- Adding a missing relationship archetype annotation: always escalate
  (requires a characterization choice about which archetype fits).
- Rewriting a Background fact-pair result: escalate when the current
  result is a trait label or abstract interpretation and a concrete
  replacement must be sourced from reference material.
