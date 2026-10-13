# Concept Note Format

*Reference document for `worldbuilder-concept`. Defines the note structure, entry formats, required entries and section-scoped writing rules for concept notes. Style rules: `../writing-style.md`. Rules shared by every entity note: `../creative-step.md`, What every entity note shares.*

---

## Note structure

| Section | Notes |
|---|---|
| Design Notes | Builder record |
| Lore | What is true about this thing in the world |
| Implications | What follows from this being true; activation context |

### Design Notes

`../creative-step.md`, Design Notes, defines the record. For a concept, Builder Context holds:

- **Narrative purpose:** what the existence of this thing makes impossible, costly or inevitable in any scene that touches it. A note that cannot answer this question is description, not a constraint. Write the answer here before drafting Lore and Implications: it shapes what to include and what to cut.
- **Why this is its own note:** why this knowledge warrants a standalone note and is not embedded in a character, location or faction note.
- **Layer rationale:** why the note is classified surface, mid or deep, and what would be lost one layer higher or lower.
- **Open questions:** unresolved details that may affect how this note is written or how it interacts with other notes.

### Frontmatter

`layer` takes `surface` (freely shareable), `mid` (contextual) or `deep` (revealed late). `aliases` is the most important field of a concept note: the export skill derives keyword triggers from it, and aliases become lorebook keyword candidates at export. See Alias writing below.

---

## Lore

Lore holds what is true about this thing in the world. It is the main exportable content. Imported lorebook entries marked `constant` describe standing setting state: that is foundation material for `project/foundation.md`, not a concept note.

### The three-layer structure

The setting deepens as the player invests. Do not front-load. Surface entries establish a mundane world with texture. Mid-layer entries acknowledge the old stories. Deep entries confirm what the hints implied. Jumping straight to deep lore in early entries kills the effect.

**Surface layer.** What everyone knows: the baseline reality of the setting.

- Geography and physical character of the setting
- Economy: what the place does, how people make a living
- Social texture: close-knit, fractured, proud, struggling
- Common local history: the stories everyone tells
- Practical knowledge relevant to the player's daily activities

Tone: matter-of-fact. No mysticism. These entries establish normalcy so that later disruptions carry weight. A surface entry that hints "but some say this is connected to the old stories" breaks the layer structure.

**Mid layer.** Things people half-remember: old stories told as legend but believed a little.

- The old stories: things the community tells as history but with mythic edges
- Wilderness, ruins, old buildings and what people say about them
- Historical events that left marks: a fire, a founding family's story, something that divided the community
- Hints at what lies beneath the surface

Tone: uncertain and hedged. People who know these stories are not sure they believe them. "They say..." "It's probably nothing, but..." Characters rationalize and deflect.

**Deep layer.** The actual hidden layer: what the hints were pointing toward.

- The supernatural specifics, if the setting has them
- The setting's true history
- The real origin of the wound
- Any non-human or supernatural entities in detail

Tone: confirmed and weighted. These entries feel like the answer to questions the surface layer raised. Do not explain everything: some things can remain permanent mystery.

**Layer classification is authorial intent about pacing.** It is not a reliable mechanism for suppressing information from the engine at runtime, because whether an engine can gate context on conditions varies. Its value is in shaping how the content is written and in what export tools can do with the metadata.

### The iceberg split

Distinct from layer classification. The iceberg split operates within a single note, where what people in the world believe and what is actually true diverge. Where the gap is narratively significant, document both in the same note:

- **Believed:** what characters in the world commonly say, assume or act on: the public version, the legend, the received wisdom.
- **True:** what actually happened, or how the thing actually works underneath the common understanding.

This lets the engine have characters speak and act from belief while the true version constrains what can happen and what specific informed characters know. Use it only when the gap between belief and truth is a live story element.

### Background NPC guidelines

Rather than writing individual unnamed characters, write guidelines for how the engine constructs background figures, as a lorebook entry active from day 1. Cover:

- What kinds of people live here: occupations, ages, social roles
- What personality tendencies fit the setting's character
- How they are incorporated when the player engages with them
- What topics they discuss, what they know and what they do not

This gives the engine a construction kit and not a cast list, which produces more varied and naturalistic background interactions than named extras.

---

## Implications

Implications covers what follows from this thing being true in the world. It is not a description of the concept. It is an account of what the concept does to scenes.

- **Behavioral and social consequences:** what people do differently because this thing exists; what norms, obligations or social structures it produces; what economic consequences it carries.
- **Tensions:** what conflicts, pressures or contradictions this thing creates for characters or communities that encounter it.
- **Costs and limits:** see Required entries.
- **Activation context:** when this lore becomes relevant, and which situations and phrasings bring it into play. Write it as a specific account of the scenes and moments where the concept matters, and not as a one-phrase field.

**The key question.** What would a scene look like differently because this thing exists? If the answer is "nothing specific," Implications is too thin.

---

## Required entries

A note is not finalized until each of these is present or waived (`../creative-step.md`, Required entries and waivers).

1. **Costs and limits, for a rule-bearing concept.** A rule-bearing concept covers a magic system, institution, cultural practice, belief system, or anything with internal logic that scenes must respect. Document what the concept cannot do, what it costs or demands, and what makes it fail, break or produce unexpected results. A concept documented only by what it can do cannot constrain a scene. One documented by its limits and costs can.
   - Does not constrain: "healers can mend wounds and cure illness."
   - Constrains: the same concept plus "healing draws from the healer's own vitality — serious wounds leave the healer bedridden for an equal period, and healing the dying risks the healer's own death."
2. **`layer`, `aliases` and `description` filled.**

---

## Alias writing

The export skill derives keyword triggers from `aliases`, so write them for how topics come up in dialogue.

- **Coverage:** include every realistic phrasing. For a note about the mill, include "the mill," "old mill," "Harrow's mill," "the water wheel." A single overly precise phrase that never appears verbatim never triggers.
- **Plural and possessive forms:** matching is typically exact-string. "mill" does not match "mill's" or "mills." Include the forms that appear in dialogue.
- **Specificity:** short generic terms match too broadly. "inn" fires on "innocent," and "well" on "well-lit." Prefer multi-word aliases where ambiguity exists: "the inn," "the old well."
- **Local names:** characters use the names they know, not the canonical title. Include both.
- **Common mistakes:** a single generic word that fires constantly; forgetting local names or synonyms; so many required terms that the combination almost never matches.

---

## Section-scoped writing rules

- Style rules (decide, do not hedge; write plainly, no flair) are in `../writing-style.md`. This format adds none.
- Design Notes content stays in Design Notes (see Note structure).
- **Short is usually better.** An entry that injects 50 tokens of precise context beats one that injects 300 tokens of unfocused description.
- **Separate entries for separate topics.** Do not pack "the old mill and the mill family and the flood of thirty years ago" into one entry. Split them so each triggers independently and does not bloat context when only one is relevant.
- **Test the trigger mentally.** Read a sample scene where the topic comes up naturally. The alias set should cover the realistic phrasings and avoid unrelated uses of the same word.
- **Over-documented:** any section that adds detail no scene will touch, or duplicates content already in a character, location or faction note. Concept notes are short and dense.

---

## Review criteria

Rules the critic enforces, organized by scope. Each check names the rule and its source location, then describes the violation pattern. It does not reproduce the rule text.

### Checks

**Document-level:**
- Required entries present or waived (this document, Required entries). Violation: a rule-bearing concept with no Costs and limits, or `layer`, `aliases` or `description` empty, with no recorded waiver.
- Temporal scope (`skills/worldbuilder-review/SKILL.md`, Phase 2). Every section is checked.
- Slop-phrase scan (`docs/slop-phrases.md`). Violation: any listed phrase present.
- Writing doctrine compliance (`skills/writing-style.md`). Violation: any failure mode listed there.

**Lore:**
- Content written at the correct layer tone (this document, Lore — The three-layer structure). Violation: a hint of deeper lore in a surface entry, or a confirmed reveal in a mid entry.
- Iceberg split present where the belief/truth gap is live (this document, Lore — The iceberg split). Violation: a gap the note treats as live, with only one side written.

**Implications:**
- Behavioral and social consequences, not only restrictions (this document, Implications). Violation: a list of restrictions with no account of what people do.
- Activation context stated (this document, Implications). Violation: no account of the scenes or phrasings that bring the concept up.
- The key question answered (this document, Implications). Violation: the section names no scene difference.

**Aliases:**
- Alias coverage and specificity (this document, Alias writing). Violation: a single generic word, or no plural or possessive forms for aliases that appear in dialogue.

**Section placement:**
- Design Notes content stays in Design Notes. Violation: narrative purpose written into Lore or Implications.
- Over-documentation (this document, Section-scoped writing rules). Violation: a section that duplicates a character, location or faction note.

### Exempt

- **Design Notes:** exempt from all review checks (`../creative-step.md`, Design Notes).
- **In-world quoted text:** exempt from the writing-style checks, including the hedged mid-layer speech ("They say...") that the layer tone calls for.
- **Story-content sections:** none. Lore and Implications describe the world at the declared starting point, and the temporal-scope check covers both.

### Judgment calls

Classify as `skills/worldbuilder-review/SKILL.md`, Phase 3, sets out. Concept-specific guidance:

- A rule-bearing concept with no costs and limits: escalate. The limits are a creative choice.
- A surface entry that hints at deeper lore: auto-fix when removing the hint sentence leaves the entry whole. Escalate when the hint carries the entry's content.
- An alias list with plural or possessive forms of aliases already present missing: auto-fix. A generic single-word alias: escalate, since the multi-word replacement must be chosen.
- Narrative purpose written into a body section: auto-fix by moving it to Builder Context when the sentence stands alone. Escalate when the section depends on it.
- An Implications section that lists restrictions only: escalate. The behavioral consequences must be sourced.
