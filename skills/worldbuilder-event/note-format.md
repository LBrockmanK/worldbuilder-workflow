# Event Note Format

*Reference document for `worldbuilder-event`. Defines the note structure, entry formats, required entries and section-scoped writing rules for event notes. Style rules: `../writing-style.md`. Rules shared by every entity note: `../creative-step.md`, What every entity note shares.*

---

## Note structure

| Section | Notes |
|---|---|
| Design Notes | Builder record |
| What Happens | Factual description of the event |
| Scene Effects | What the event does to scenes and social dynamics |

### Design Notes

`../creative-step.md`, Design Notes, defines the record. For an event, Builder Context holds what this event contributes that no other event does, inspirations (real festivals, cultural observances, fictional events) with what is drawn from each, the narrative intent (what kinds of scenes the event enables), and open questions.

### Frontmatter

`aliases` carries every realistic way the event is mentioned in dialogue ("the festival," "harvest time"). The export skill derives keyword triggers from it. Timing (season, day, recurrence) is not a field: open What Happens with when the event takes place and how often.

Some events carry layer classification like concept notes. A surface festival is well known and openly celebrated. A mid-layer observance has old stories behind it. A deep-layer ritual touches the hidden layer. Apply a `layer:` frontmatter field when the event has a hidden dimension. An event without one needs no layer classification.

---

## What Happens

**Entry format:** a factual description of the event. Write for content, not calendar precision.

- **Timing:** season and rough calendar position. The exact day is an export decision. Write "early spring," not "day 8."
- **Who participates:** universal, optional, by community role, or by invitation.
- **What physically occurs:** activities, rituals, traditions.
- **Origin:** what the event commemorates or why it exists.

### Cultural shorthand

The real-world references named in the cultural shorthand answer are written into What Happens. A reference kept only in Design Notes never reaches the model, because Design Notes is excluded from export.

---

## Scene Effects

This is the section that makes event notes worth having.

**Entry format:** cover these four topics, in whichever order reads best.

- **Social dynamics:** what distances relax, what tensions tighten, who talks to whom that normally would not.
- **Obligations and costs:** who is expected to attend, and what happens socially if someone does not.
- **Scene logic:** what becomes natural on this day, and what becomes unusual or impossible.
- **Hidden layer:** how the event touches deeper world elements, if relevant.

**The scene test.** If the engine generates a scene set on this day with no other context, does it feel different from any other day? If not, Scene Effects is too thin.

- Fails: "It is a day of celebration. People are happy and gather in the town square." This could be any day. The event is invisible.
- Passes: "The usual rules about who approaches whom are suspended today. Characters who normally hold themselves apart from the player will initiate conversation. The player meets the full community for the first time, and relationships that normally require weeks of individual cultivation can begin here." The engine has specific behavioral direction.

---

## Required entries

A note is not finalized until each of these is present or waived (`../creative-step.md`, Required entries and waivers).

1. **A Scene Effects section that passes the scene test.**

---

## Section-scoped writing rules

- Style rules: `../writing-style.md`. This format adds none.
- Design Notes content stays in Design Notes (see Note structure).
- Vague timing is fine. What Happens states the approximate season and does not assign a day.

---

## Review criteria

Rules the critic enforces, organized by scope. Each check names the rule and its source location, then describes the violation pattern. It does not reproduce the rule text.

### Checks

**Document-level:**
- Required entry present or waived (this document, Required entries). Violation: a Scene Effects section that fails the scene test, with no recorded waiver.
- Temporal scope (`skills/worldbuilder-review/SKILL.md`, Phase 2). Every section is checked.
- Slop-phrase scan (`docs/slop-phrases.md`). Violation: any listed phrase present.
- Writing doctrine compliance (`skills/writing-style.md`). Violation: any failure mode listed there.

**Frontmatter:**
- `aliases` covers every realistic phrasing (this document, Note structure — Frontmatter). Violation: a realistic way the event is mentioned in dialogue is missing.
- Layer classification (this document, Note structure — Frontmatter). Violation: Scene Effects touches the hidden layer and no `layer:` is set.

**What Happens:**
- Timing stated, approximately (this document, What Happens). Violation: no timing, or a specific day number.
- Who participates and what physically occurs are stated (this document, What Happens). Violation: either missing.
- Cultural shorthand placement (this document, What Happens). Violation: a reference recorded in the Specification is missing from What Happens, including one that appears only in Design Notes.

**Scene Effects:**
- At least one social dynamic specified (this document, Scene Effects). Violation: no statement of what relaxes or tightens.
- Obligations and costs stated when the event carries them (this document, Scene Effects). Violation: an expected attendance with no stated cost for absence.
- Scene test (this document, Required entries). Violation: a scene on this day would feel the same as any other day.

**Section placement:**
- Design Notes content stays in Design Notes. Violation: narrative intent written into a body section.

### Exempt

- **Design Notes:** exempt from all review checks (`../creative-step.md`, Design Notes).
- **In-world quoted text:** exempt from the writing-style checks. Text quoted from source material is not prose the author chose.
- **Story-content sections:** none. What Happens and Scene Effects describe the event as it stands at the declared starting point, and the temporal-scope check covers both.

### Judgment calls

Classify as `skills/worldbuilder-review/SKILL.md`, Phase 3, sets out. Event-specific guidance:

- A Scene Effects entry that could describe any day ("People are happy and gather in the town square"): escalate. The scene logic must be invented.
- A specific day number in Timing ("day 8"): auto-fix to the approximate season when the same section states the season. Escalate when it does not.
- `aliases` missing a realistic phrasing: escalate. The phrasing must be sourced.
- Narrative intent written into a body section: auto-fix by moving it to Builder Context when the sentence stands alone. Escalate when the section depends on it.
