# Story Note Format

*Reference document for `worldbuilder-story`. Defines the note structure, scope values, section contents, required entries and section-scoped writing rules for arc, intention and introduction notes. It does not govern the direction document, which `SKILL.md` covers. Style rules: `../writing-style.md`. Rules shared by every entity note: `../creative-step.md`, What every entity note shares.*

---

## Note structure

| Section | Notes |
|---|---|
| Design Notes | Builder record; excluded from exports |
| Situation | State of affairs before player involvement |
| Story Possibilities | What could happen; phrased as possibility, not script |

The story engine acts on Situation and Story Possibilities. A story note has no other section. In particular it has no `## Arc` section: the arc is the frame the questions in `SKILL.md`, Interview, follow, and each answer goes to one of the three sections above.

### Design Notes

`../creative-step.md`, Design Notes, defines the record. For a story note, the arc is the frame the builder writes the creative intent against. Builder Context holds:

- **Creative intent:** what kind of story this is emotionally, what it should feel like when it plays out, and what experience the builder is trying to create for the player.
- **Inspirations:** specific scenes, arcs or moments from other media, with what is drawn from each. Name the quality, not only the source: not "like the opening of Episode 4" but the scale, the stillness before action, the sense of something already in motion.
- **Why this is worth building toward:** what makes the arc or moment interesting, and why it earns space in the world.
- **Open questions:** what stays unresolved about the arc: thematically, structurally, or in a specific character's behavior.

### Frontmatter

The plugin's type roster defines the frontmatter. Set `scope` to one of:

- `arc`: a major story section, linking up to the direction document. It covers a season, a storyline or a thematic phase.
- `intention`: a specific story possibility within an arc, linking up to that arc. It is a soft target the world is set up to enable, not a scripted outcome.
- `introduction`: the first-contact scene for a specific character. It is created during or after character note work, not during the story notes phase.

Set `up` to a markdown link pointing at the parent note. The parent of an arc is the direction document; the parent of an intention is its arc.

The standing creative brief lives in `project/direction.md` (type: direction), not in a story note.

**Description.** 1–2 sentences naming what the note is. For an arc, the emotional territory it covers. For an intention, the story possibility in one sentence. For an introduction, who it introduces and the first impression. Written last (`../../CONTEXT.md`, Properties). Other agents scan this field when planning arcs or building character notes.

---

## Situation

The state of things before any player involvement. Write in present tense.

**Arc and intention notes:**

- The current state of affairs in the world that makes the arc or intention possible, and the pressure in it.
- Who is involved and what each party wants or fears going in.
- Timing constraints or seasonal considerations, if relevant.
- Preconditions: what needs to be true (player trust level, prior events, season) for the arc or intention to be accessible.

**Introduction notes:**

- Where and when the introduction could happen.
- Who else is present.
- The circumstances that make this a natural first meeting.

---

## Story Possibilities

What could happen and how it could develop. Phrase each entry as a possibility, not a script: use "may," "could," "there is a possibility that." Do not script outcomes. Write for robustness: the arc stays interesting whether or not a specific beat fires.

**Arc notes:**

- What could set the arc moving.
- The turns it could take, each with its key moment: the set piece that makes the arc feel real if it fires.
- Resolution directions: natural ways things could go, not scripted outcomes.
- Connection to other arcs or characters.

**Intention notes:** typically shorter. One key possibility, with the moment that would trigger it and the direction it could go. Connection to other arcs or characters.

**Introduction notes:** how the scene plays, what the character does, and what invitation it extends to the player. Connection to other arcs or characters.

---

## Required entries

A note is not finalized until each of these is present or waived (`../creative-step.md`, Required entries and waivers).

1. **A key moment or set piece named** in Story Possibilities.
2. **A connection to other arcs or characters noted** in Story Possibilities.

---

## Section-scoped writing rules

- Style rules (decide, do not hedge; write plainly, no flair) are in `../writing-style.md`. This format adds none.
- Design Notes content stays in Design Notes (see Note structure).
- An arc note develops what the direction document establishes. It does not contradict it.

---

## Review criteria

Rules the critic enforces, organized by scope. Each check names the rule and its source location, then describes the violation pattern. It does not reproduce the rule text.

### Checks

**Document-level:**
- Required entries present or waived (this document, Required entries). Violation: a missing entry with no recorded waiver.
- Temporal scope (`skills/worldbuilder-review/SKILL.md`, Phase 2). Situation is checked.
- Slop-phrase scan (`docs/slop-phrases.md`). Violation: any listed phrase present.
- Writing doctrine compliance (`skills/writing-style.md`). Violation: any failure mode listed there.

**Frontmatter:**
- `scope` and `up` (this document, Note structure — Frontmatter). Violation: `scope` is not arc, intention or introduction, or `up` is not a link to the parent note.
- Description (this document, Note structure — Frontmatter). Violation: more than two sentences, or it does not name the territory, possibility or first impression the scope calls for.

**Situation:**
- Present tense (this document, Situation). Violation: an entry in past or future tense.
- State of affairs before player involvement stated (this document, Situation). Violation: an entry that describes player actions or later outcomes instead.
- Preconditions named for arc and intention notes (this document, Situation). Violation: none stated.

**Story Possibilities:**
- Possibility phrasing (this document, Story Possibilities). Violation: an entry written as a fixed event ("The player meets her at the gate and she hands over the key").
- A key moment named (this document, Required entries). Violation: no set piece or triggering moment.
- A connection noted (this document, Required entries). Violation: no connection to another arc or character.

**Section placement:**
- Design Notes content stays in Design Notes. Violation: creative intent written into Situation or Story Possibilities.

### Exempt

- **Design Notes:** exempt from all review checks (`../creative-step.md`, Design Notes).
- **In-world quoted text:** exempt from the writing-style checks. Text quoted from source material is not prose the author chose.
- **Story-content sections:** Story Possibilities holds story content and is exempt from the temporal-scope check.

### Judgment calls

Classify as `skills/worldbuilder-review/SKILL.md`, Phase 3, sets out. Story-specific guidance:

- A Story Possibilities entry written as a script: auto-fix by rewording as a possibility when the entry keeps its meaning. Escalate when the entry states its outcome as certain and the fix would change what happens.
- A Situation entry in past or future tense: auto-fix to present tense.
- No key moment named: escalate. The moment must be invented.
- No connection noted: escalate. The connection must be sourced.
- Creative intent written into a body section: auto-fix by moving it to Builder Context when the sentence stands alone. Escalate when the section depends on it.
