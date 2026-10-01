# Card Assembly — ainime `baseProfile`

*Sub-file for `worldbuilder-ainime-export`. Read this when assembling the `baseProfile` field for a character.*

---

## Overview

The `baseProfile` field carries the character's complete profile — everything the engine reads as "who this character is." The character note's sections ship directly into the `baseProfile`, separated by `---` dividers: the preamble, Background, Body, Soul, Relationships, Voice / Dialogue, then Future Storylines. Everything from the character note ships except Design Notes.

Do not rewrite, paraphrase, weave into prose, or otherwise transform the source content. The character note is the card.

Source material: the character note in `notes/`.

---

## Sections

Each section from the character note ships as-is with its heading. Preserve the content — every fact, every behavioral detail, every "because" clause, every archetype label, every dialogue line. Do not summarize, merge, drop entries, or reword.

**Preamble** — the opening text before the first heading. Ships without a heading.

**Background** — ships with heading.

**Body** — ships with heading.

**Soul** — ships with heading. Every psychological driver and its internal logic must survive intact.

**Relationships** — ships with heading. Every named relationship with its archetype label and full behavioral description.

**Voice / Dialogue** — ships with heading. Every dialogue situation with its label, scene context, and full dialogue lines. Engine format applies to dialogue and narration within scenes.

**Story Seeds → Future Storylines** — the one transformation. Story Seeds are reframed as Future Storylines: the title becomes the storyline label, and the scenario prose is reframed from definite to possibility-style ("may", "could", "might"). Do not script outcomes — give the engine material to work from. Do not drop lines or sentences from source seeds.

**Design Notes** — excluded. Does not ship.

---

## Engine format

Used in Voice / Dialogue and Future Storylines:

- Speech: plain text
- Narration/action that appears in play: `_asterisks_`
- Context for the reader (does not appear in play): `(parentheses)`
- Internal thought: `` `backticks` ``

---

## Register rules

These apply to the one section that is rewritten (Future Storylines) and to any minor cleanup of source text:

- **Write plainly. No flair.** The card's prose style becomes the engine's narration style.
- **No literary flair or metaphor** in descriptive text — that register belongs in dialogue.
- **Numbers as numerals.** 27, not twenty-seven.
- **Pronouns follow the `sex` field.** The character note's `sex` frontmatter field is internal worldbuilder schema and never ships in the card. Read it before reframing Story Seeds, and keep every pronoun for the character in agreement with it.

---

## Self-Check

- [ ] Preamble present
- [ ] Background section present — every fact from source
- [ ] Body section present — physical description and every behavioral tic from source
- [ ] Soul section present — every psychological driver with its full internal logic
- [ ] Relationships section present — every named entry with archetype label and full description
- [ ] Voice / Dialogue section present — every dialogue situation with all lines
- [ ] Future Storylines present — every Story Seed accounted for, phrased as possibility, no lines dropped
- [ ] Introduction storyline present
- [ ] Design Notes excluded
- [ ] No content rewritten, paraphrased, or summarized beyond the Story Seeds → Future Storylines reframing
- [ ] Factual accuracy — no reversed attributions, no invented details
- [ ] Pronouns agree with the character note's `sex` field
