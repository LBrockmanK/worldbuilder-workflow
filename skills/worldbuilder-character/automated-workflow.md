# Automated Workflow

*Alternate mode for `worldbuilder-character`. Use when writing or revising card sections from source material without interactive Q&A — batch processing multiple characters, backfilling a section across a cast, or any workflow where the human sets the goal and the agents execute to completion.*

The interactive workflow (SKILL.md) assumes one session, one character, with the human answering questions and approving each entry. This workflow replaces the human with source material and adversarial review. The quality standard is the same; the process that reaches it is different.

---

## When to use

- Backfilling a section (e.g., Relationships) across multiple characters
- Writing entries from existing reference material without new Q&A
- Any task where the human says "do all of these" rather than working through one at a time

## When not to use

- First-time character creation with no source material (use interactive)
- Sections that require creative decisions the source material doesn't answer (use interactive for the decisions, then automated for execution)

---

## Required Reading Set

Every agent that writes or reviews card content must read the governing documents. These are relative paths from the skill's base directory — resolve them to absolute paths before dispatching.

### For writing entries

| File | Path from skill base | Purpose |
|------|---------------------|---------|
| Writing style | `../writing-style.md` | Prose rules: plain style, staging test, trait-word ban, tense, Orwell's rules |
| Card format | `card-format.md` | Section-scoped writing rules, depth-of-access grid, review criteria |
| Section guide | `relationships.md`, `intimate.md`, etc. | Section-specific framework, archetypes, coverage requirements, entry format |
| Starting world state | *project-level, path varies* | The declared starting point (`../worldbuilder-review/SKILL.md`, Phase 2) |

### For the character itself

| File | Purpose |
|------|---------|
| Character card | Existing content (Background, Body, Soul) for behavioral context |
| Character reference/ directory | Evidence base: dialogue, behavioral observations, data profile |
| Other cast cards | Pronouns, existing relationship entries for cross-reference |

### For adversarial review

All of the above, plus the review criteria section of `card-format.md`.

---

## Dispatch Brief Template

Every dispatched agent gets a brief containing:

1. **Task:** What section to write, for which character, how many entries expected
2. **Reading list:** Absolute paths to every file in the Required Reading Set. Not descriptions of what the files contain — the actual paths, with the instruction "Read these files before writing."
3. **Exemplars:** 2-3 completed entries from other characters in the same project that represent the target quality. The agent matches the exemplars' style, not a verbal description of it.
4. **Constraints:** Project-specific rules (the declared starting point, dateable vs. supporting character minimums, cast-connectivity requirements)
5. **Acceptance criteria:** What the output must pass before the agent reports done

### What not to put in the brief

Do not restate the content of the governing documents in the brief. The brief points to the documents; the agent reads them. A paraphrased rule in the brief competes with the actual rule in the document, and the paraphrase loses detail.

---

## Process: Relationship Entries

### Phase 1 — Write

One agent per character. Each agent:

1. Reads ALL files from the Required Reading Set (writing)
2. Reads 2-3 exemplar relationship sections from completed cast members
3. Reads the character's own card and reference material
4. Writes entries following `relationships.md` — behavioral engines, not anecdote lists; dual archetypes where the relationship carries competing dynamics; perspective-focus with the card owner as grammatical subject
5. Runs the self-review from `relationships.md` (perspective focus, archetype distribution, coverage validation)
6. Edits the character card
7. Reports: entries written, distribution, uncertainties

### Phase 2 — Adversarial Review

One agent per character, different from the writer. Each agent:

1. Reads ALL files from the Required Reading Set (review)
2. Reads the character's reference material (evidence verification)
3. Checks every entry against every criterion in `card-format.md` review section and `relationships.md` coverage validation
4. Applies mechanical fixes directly (tense, trait words, negative constructions, staging failures, perspective subject)
5. For judgment calls (archetype fit, evidence gaps): applies best fix and flags the reasoning
6. Edits the character card
7. Reports: findings, fixes applied, remaining concerns

### Phase 3 — Verification

One pass across all edited cards:

1. **Pronoun consistency:** For every character mentioned in a relationship entry, verify pronouns match that character's own card. Names do not determine gender — the character's card does.
2. **Distribution legality:** No archetype more than 2x per character. Community Thread max 1x.
3. **Format consistency:** All entries follow the same format within the project (prefix or trailing archetype notation, not a mix).
4. **Cross-character coherence:** Run the cross-card pass and the checker as `../source-extraction-standard.md` sets out.

### Phase 4 — Post-Group Sync

After completing a batch, run the cross-card pass and the checker as `../source-extraction-standard.md` sets out. A character written later in the batch may have shifted in ways that make an earlier character's entry inaccurate.

---

## Failure Modes This Workflow Prevents

These are the specific failures that occurred when the automated workflow was run without this document:

1. **Missing governing documents.** Agents wrote entries without reading `relationships.md`. Entries became anecdote lists instead of behavioral engines because the agents never saw the guidance on what makes an entry generative.

2. **No dual archetypes.** Agents assigned one archetype per entry because the brief didn't include `relationships.md`, which explains that a single relationship can carry more than one archetype and shows when to use them.

3. **Pronoun errors.** Agents assumed gender from character names. Valen (female) was written as he/him in three cards. Dell (female) was written as he/him in one card. The verification phase catches this.

4. **Anecdote lists instead of engines.** Without the generativity hierarchy and the distinction between describing what a character does vs. specifying the dynamic that drives what they do in any scene, agents defaulted to listing specific actions.

5. **Paraphrased rules in briefs.** The dispatcher summarized the rules instead of pointing to the documents. The summaries lost the nuance (e.g., "check perspective focus" without the worked example showing the difference between observable behavior and internal-state claims about the other character).

---

## Exemplar Quality Check

Before dispatching a batch, verify that the exemplar entries (the completed characters used as style targets) pass the same criteria the new entries will be reviewed against. A flawed exemplar propagates its flaws across every character in the batch.
