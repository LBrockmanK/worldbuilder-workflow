# Location Note Format

*Reference document for `worldbuilder-location`. Defines the note structure, entry formats, required entries and section-scoped writing rules for location notes. Style rules: `../writing-style.md`. Rules shared by every entity note: `../creative-step.md`, What every entity note shares.*

---

## Note structure

A location note holds all its content in one note. There are no sub-files. Work through the sections in order, and do not skip a section because the location seems simple.

| Section | Notes |
|---|---|
| Design Notes | Builder record |
| Form & History | Physical reality and what the place carries |
| Presence | Who comes here and how the place behaves |

### Design Notes

`../creative-step.md`, Design Notes, defines the record. For a location, Builder Context holds the narrative function (what the location uniquely contributes), the intended scene types (what kinds of scenes can only happen here), inspirations (real or fictional) with what is drawn from each, design decisions and open questions. Narrative purpose and creative intent go here and nowhere in the body sections.

---

## Form & History

### Physical Form

**Entry format:** 1-3 sentences. Scale, age, condition, environment, one concrete detail.

Not a floor plan. The engine needs to know what kind of place this is, not where the furniture is. One concrete detail beats three paragraphs of layout.

> *The mill is a two-storey stone building with a collapsed east wall, open to the sky. The water wheel still turns sometimes when there's no wind.*

### History & Meaning

**Entry format:** Why this place exists. What it carries from the past. What it implies about the world. Secrets, if it has them. A sentence or two is often enough, but the "what it implies" question must be answered. A location with no reason to exist generates no scenes worth setting there.

When concept notes at different knowledge layers cover the location, link to them here and do not duplicate their content.

### Cultural shorthand

The real-world references named in the cultural shorthand answer are written into Form & History. A reference kept only in Design Notes never reaches the model, because Design Notes is excluded from export.

---

## Presence

Presence carries more weight than Form & History. A note that is mostly physical description and thin on Presence is description masquerading as specification.

### Who Comes Here

**Entry format:** The ecosystem layer, written as who-does-what, not who-is-there. Who comes here and why, what they do when they arrive, what they want that they might not get, and what tensions exist between regular visitors or between visitors and whoever maintains the place. Every fact is a decision: "various locals may visit for various reasons" is not a valid entry.

> *Farmers bring grain in autumn to argue pricing with the factor; the factor holds the only certified scales in the valley, which means he sets the effective price regardless of what anyone negotiates. The itinerant workers who sleep in the granary loft resent both groups and stay out of disputes until someone owes them wages.*

That entry names three types of visitors, what each wants and two tensions. Cover the main types of people and their reasons, what they want that the place does or does not provide, and at least one tension.

### How the Place Behaves

**Entry format:** How the place reads across the variations that would produce different scenes:

- **Time:** day against night, busy against quiet, seasonal rhythm if relevant.
- **Observer:** how an insider or regular experiences it against a stranger or first-timer.
- **Circumstances:** normal operation against disrupted, crisis or changed state.

Not every axis applies to every location. Cover the axes that would produce different scenes and skip the rest. A remote ruin probably needs no insider/stranger distinction. A village market square likely needs all three. Asymmetry is normal: write only what is true and useful.

**The push-back test.** After writing this section, ask whether the place does something to the characters in it, or only describes what is there.

- Fails: "At night the market is quiet and empty." This describes absence. The place is not acting.
- Passes: "At night the market belongs to the night-watch, who treat any civilian presence as suspicious until proven otherwise. A player arriving after dark will be questioned before anything else happens." The place produces a scene logic that does not apply in daylight.

---

## Required entries

A note is not finalized until each of these is present or waived (`../creative-step.md`, Required entries and waivers).

1. **A scene-logic axis (the push-back standard).** At least one Presence axis specifies a change in scene logic, tone or friction, not only a change in who is present or absent. The push-back test above is how the entry is checked.

---

## Section-scoped writing rules

- Style rules: `../writing-style.md`. This format adds none.
- Design Notes content stays in Design Notes (see Note structure).
- Form & History is physical reality and what the place carries. Behavior belongs in Presence.

---

## Review criteria

Rules the critic enforces, organized by scope. Each check names the rule and its source location, then describes the violation pattern. It does not reproduce the rule text.

### Checks

**Document-level:**
- Required entry present or waived (this document, Required entries). Violation: no Presence axis changes scene logic, tone or friction, and no recorded waiver.
- Temporal scope (`skills/worldbuilder-review/SKILL.md`, Phase 2). Every section is checked: a location's crisis circumstance is present-state description.
- Slop-phrase scan (`docs/slop-phrases.md`). Violation: any listed phrase present.
- Writing doctrine compliance (`skills/writing-style.md`). Violation: any failure mode listed there.

**Form & History:**
- Physical Form entry format (this document, Form & History — Physical Form). Violation: more than 3 sentences, no concrete detail, or a floor plan.
- History & Meaning entry format (this document, Form & History — History & Meaning). Violation: no statement of why the place exists or what it implies.
- Cultural shorthand placement (this document, Form & History — Cultural shorthand). Violation: a reference recorded in the Specification is missing from Form & History, including one that appears only in Design Notes.

**Presence:**
- Who-does-what form (this document, Presence — Who Comes Here). Violation: an entry names who is present without saying what they do or want.
- Tension present (this document, Presence — Who Comes Here). Violation: no tension between visitors, regulars, or the place and its visitors.
- At least one meaningful variation (this document, Presence — How the Place Behaves). Violation: the section describes no variation.
- Push-back test (this document, Presence — How the Place Behaves). Violation: an entry describes absence or presence only and the place does nothing.

**Section placement:**
- Design Notes content stays in Design Notes (this document, Section-scoped writing rules). Violation: narrative purpose or creative intent in a body section.

### Exempt

- **Design Notes:** exempt from all review checks (`../creative-step.md`, Design Notes).
- **In-world quoted text:** exempt from the writing-style checks. Text quoted from source material (signs, in-world documents) is not prose the author chose.
- **Story-content sections:** none. The variations in How the Place Behaves, such as a crisis circumstance, are present-state description and stay subject to the temporal-scope check.

### Judgment calls

Classify as `skills/worldbuilder-review/SKILL.md`, Phase 3, sets out. Location-specific guidance:

- Rewriting an entry that describes absence ("At night the market is quiet and empty"): auto-fix when the note already names who holds or uses the place at that time, so the repair only restructures the entry as an action. Escalate when the scene logic must be invented.
- A Who Comes Here entry that names who is present without what they do or want: escalate. The repair needs new content.
- Cutting a Physical Form entry that runs past 3 sentences: auto-fix when the extra sentences are layout elaboration around one concrete detail. Escalate when cutting would remove the only concrete detail.
- Moving narrative intent from a body section into Builder Context: auto-fix when the sentence stands alone and the section reads whole without it. Escalate when the section depends on it.
- Hedged or incomplete facts ("something may have happened to the mill"): auto-fix when the note decides the fact elsewhere. Escalate when the fact must be invented.
