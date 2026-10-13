# Faction Note Format

*Reference document for `worldbuilder-faction`. Defines the note structure, entry formats, required entries and section-scoped writing rules for faction notes. Style rules: `../writing-style.md`. Rules shared by every entity note: `../creative-step.md`, What every entity note shares.*

---

## Note structure

A faction note holds all its content in one note. There are no sub-files. Work through the sections in order.

| Section | Notes |
|---|---|
| Design Notes | Builder record |
| Origin & Structure | Founding, current holdings, active goals, membership |
| Collective Behavior | Shared tendencies, collective mask, variation layer, inter-faction web |

### Design Notes

`../creative-step.md`, Design Notes, defines the record. For a faction, Builder Context holds the narrative engine the faction runs: not a description of its membership or its history, but what it does to the story, what conflicts it generates or embodies, and what role it fills that no other faction could. A merchant guild and a thieves' guild that produce the same kinds of scenes have the same narrative engine, and that is a problem. Builder Context also holds inspirations with what is drawn from each, design decisions, and open questions about the faction's role.

---

## Origin & Structure

Collective Behavior is the priority section. A note that is mostly Origin & Structure and thin on Collective Behavior documents history without specifying behavior.

Four parts, in this order:

**Founding.** How the faction came to exist and what its original purpose was.

**Current holdings.** What it controls now. Be specific: resources, territory, monopoly, information, relationships, obligations owed to it. "Has influence" is not a holding.

**Active goals.** What the faction is trying to achieve right now. A goal must be specific and active.

> *Controls the grain trade and intends to extend that monopoly to the river docks before the spring thaw.*

"Seeks to grow its power and influence" is not a goal. Specific goals connect the faction to the events layer and make it a story engine.

**Membership.** Deliberately thin on named-member content: named members have their own character notes. Cover:

- **Ranks or tiers**, if they exist (hierarchy only, no personalities here).
- **Acquisition:** how one becomes a member.
- **Loss:** how membership ends or is revoked.
- **Ambiguity cases:** former members, dual loyalties, contested membership, outsiders who function as members without formal standing. These earn their place because characters who straddle faction lines are often the most narratively generative.

### Where the faction operates

Pressure from where the faction operates (territory, climate, geography, neighbors, proximity to danger) is stated under Founding or Current holdings as a pair: [place fact] → [what it made true about the faction and its members].

### Cultural shorthand

The real-world references named in the cultural shorthand answer are written into Origin & Structure. A reference kept only in Design Notes never reaches the model, because Design Notes is excluded from export.

---

## Collective Behavior

This section makes faction members read as members.

**Phrasing rule throughout this section:** instructional, not descriptive. Write what members do, not what they are. Descriptive phrasing tells the engine what to know. Instructional phrasing tells it what to do.

- Fails: "Members are guarded and don't trust outsiders."
- Passes: "When approached by an outsider asking about Brotherhood pricing, members deflect with friendly vagueness — they quote ranges rather than figures, suggest the player talk to the factor, and find a reason to be elsewhere if pressed. Show this."

### Shared behavioral tendencies

**Entry format:** 3-5 entries in When/Behavior/Because form, applied to the group as a whole.

> When [situation], [members do X] because [faction value or principle].

Example:

> When a stranger asks Brotherhood members about their pricing or trade routes, members give friendly, vague answers — ranges rather than figures, references to the factor rather than direct quotes — because the Brotherhood treats price information as proprietary. Show this deflection without making it feel hostile.

Cover recognizable situations: encountering outsiders, handling internal conflict or challenge, interacting with rivals or authority, operating under scrutiny or pressure. A group's default response to a threat to the group is one of these situations.

### The collective mask (Demeanor)

How members present as a group to people who do not know them: what a stranger expects to meet in any member, before individual personality comes through. This is the shared surface that makes members recognizable as members. Write it as a behavioral directive ("members present as...") and not a personality label ("members are...").

### The variation layer (Nature)

The individual underneath the collective mask. Members share the Demeanor without sharing a personality. Name the natural variation axes in terms of observable behavior: how a loyalist acts differently from a cynic in the same situation, not just that one is loyal and one is cynical. Do not write out every possible variation, only the axes that produce meaningfully different characters.

> *Loyalists vs. cynics. True believers vs. pragmatists who joined for the wages. Long-timers who remember the Brotherhood's origins vs. recent recruits who only know its current operation.*

### Inter-Faction Web

Lightweight by design. Direct relationships only: alliances, rivalries, contested territory, historical grievances with active weight. No comprehensive opinion-of-everyone map. Relationships that do not bear on the current project do not go here.

**Entry format:**

```
[[Faction Name]] — allied / neutral / rival / enemy: one sentence on what drives it.
```

---

## Required entries

A note is not finalized until each of these is present or waived (`../creative-step.md`, Required entries and waivers).

1. **Three to five When/Behavior/Because entries** in Shared behavioral tendencies.
2. **Instructional phrasing** in every Collective Behavior entry (the phrasing rule above).
3. **The member test passes.** After completing Collective Behavior, ask: if you wrote an unnamed member of this faction into a scene with no other characterization, would they read as a member? A member who could belong to any faction fails. A member whose behavior only makes sense given this faction's Demeanor and tendencies passes.
   - Fails: a Silt Brotherhood member who "eyes the player with suspicion and asks what they want." Any faction member could do this, and the Brotherhood is invisible.
   - Passes: a Silt Brotherhood member who "quotes the player a price range, suggests they talk to the factor for specifics, and finds a reason to be elsewhere before the player can press further." This behavior only makes sense for the Brotherhood.

---

## Section-scoped writing rules

- Style rules: `../writing-style.md`. This format adds none.
- Design Notes content stays in Design Notes (see Note structure).
- Storylines belong in story notes, not faction notes. When a story possibility is anchored by this faction's existence, propose a story note as a spin-off (`../creative-step.md`, Spin-offs).

---

## Review criteria

Rules the critic enforces, organized by scope. Each check names the rule and its source location, then describes the violation pattern. It does not reproduce the rule text.

### Checks

**Document-level:**
- Required entries present or waived (this document, Required entries). Violation: a missing entry with no recorded waiver.
- Temporal scope (`skills/worldbuilder-review/SKILL.md`, Phase 2). Every section is checked: a faction's active goals are present-state description.
- Slop-phrase scan (`docs/slop-phrases.md`). Violation: any listed phrase present.
- Writing doctrine compliance (`skills/writing-style.md`). Violation: any failure mode listed there.

**Origin & Structure:**
- Current holdings are specific (this document, Origin & Structure). Violation: "influence" or another holding that names nothing.
- Active goals are specific and active (this document, Origin & Structure). Violation: a goal with no concrete target or timing.
- Membership is thin on named members and covers acquisition, loss and ambiguity cases (this document, Origin & Structure — Membership). Violation: member personalities written out, or a part missing.
- Place pressure (this document, Origin & Structure — Where the faction operates). Violation: a place-pressure answer recorded in the Specification is missing from Origin & Structure, or is not written as a [place fact] → [consequence] pair.
- Cultural shorthand placement (this document, Origin & Structure — Cultural shorthand). Violation: a reference recorded in the Specification is missing from Origin & Structure, including one that appears only in Design Notes.

**Collective Behavior:**
- Shared tendencies format (this document, Collective Behavior — Shared behavioral tendencies). Violation: a count outside 3-5, or an entry missing its When, Behavior or Because part.
- Instructional phrasing (this document, Collective Behavior). Violation: an entry that describes what members are.
- Collective mask is a behavioral directive (this document, Collective Behavior — The collective mask). Violation: a personality label.
- Variation axes are observable (this document, Collective Behavior — The variation layer). Violation: an axis named without the behavior that distinguishes its ends.
- Member test (this document, Required entries). Violation: Collective Behavior reads as belonging to any faction.

**Inter-Faction Web:**
- Entry format (this document, Collective Behavior — Inter-Faction Web). Violation: no status, or no one-sentence driver.
- Direct relationships only (same section). Violation: an entry for a relationship that does not bear on the project.

**Section placement:**
- Storylines (this document, Section-scoped writing rules). Violation: story-possibility content in the faction note.
- Design Notes content stays in Design Notes. Violation: narrative engine written into a body section.

### Exempt

- **Design Notes:** exempt from all review checks (`../creative-step.md`, Design Notes).
- **In-world quoted text:** exempt from the writing-style checks. Text quoted from source material is not prose the author chose.
- **Story-content sections:** none. A faction's active goals and variation axes are present-state description and stay subject to the temporal-scope check.

### Judgment calls

Classify as `skills/worldbuilder-review/SKILL.md`, Phase 3, sets out. Faction-specific guidance:

- A Collective Behavior entry in descriptive phrasing: auto-fix when the entry already states the behavior and only the verb form changes ("members tend to deflect" becomes "members deflect"). Escalate when the behavior must be invented ("Members are guarded").
- A vague active goal ("seeks to grow its power"): escalate. The specific goal is a creative choice.
- A holding that names nothing ("has influence"): escalate for the same reason.
- A Demeanor written as a personality label: escalate. The behavior behind the label must be sourced.
- An Inter-Faction Web line missing its status or driver: escalate. The repair is new content.
- A Storylines section or story-possibility content in the note: escalate. The repair is a spin-off proposal, not an edit.
- Narrative engine written into a body section: auto-fix by moving it to Builder Context when the sentence stands alone. Escalate when the section depends on it.
