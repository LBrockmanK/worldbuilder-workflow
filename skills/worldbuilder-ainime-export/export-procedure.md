# Export Procedure

*Reference file for `worldbuilder-ainime-export`. It holds the checks and steps that run after `world.json` is written and before the `.sbworld` archive is built. The skill's field sections say what to write; this file says how to prove the result is sound. It carries the lessons of the Fields of Mistria export.*

---

## Order of the steps

1. Write or edit the project's versioned `exports/ainime/world.json` (see "Updating an Existing Export" in the skill).
2. Reconcile each character's `baseProfile` with its card (section 5).
3. Run the pre-flight check (section 1). Every line is pass or fail. A failure blocks the export until resolved.
4. Run the can-this-ever-fire detection (section 3). It runs only after the pre-flight check passes.
5. Run the derived-output check (section 6) when the world has a reference sheet.
6. Build the archive (section 7).

When the export needs condensing, use the adjustment order in section 4, then repeat from step 2.

**Calendar year length.** In every check below, the calendar year is `len(calendarConfig.seasons) × calendarConfig.daysPerSeason` for the world's own `calendarConfig`. Never assume a fixed number of days.

---

## 1. Pre-flight check

### Structural completeness

- [ ] `worldName`, `settingSummary`, `genre`, `inspirations`, `tonalInspirations`, `keyTropesAndThemes`, `communityDescription`, `introText`, `initialStoryArc`, `arcManagerGuidance` and `availableExpressions` are non-empty. A world that deliberately omits an optional field records that in the Export item, and the check passes for that field.
- [ ] `settingSummary` is detailed. `communityDescription` is a player-facing blurb, not an in-game description. `introText` sets the scene for a new player.
- [ ] `inspirations` and `tonalInspirations` are arrays, one item per source. `keyTropesAndThemes` has 8–12 entries.
- [ ] `calendarConfig` has `seasons`, `daysPerSeason`, `daysOfWeek` and `daySegments`. `eraReminder` is populated, or blank on purpose for a world with no technology restriction.
- [ ] `daySegments` match the project's intended day structure.
- [ ] `weatherPools` covers every season × segment combination, with no missing cell.
- [ ] `eventCalendarSummary` is populated and matches the story triggers and calendar events.
- [ ] `dailyPlannerDirective` is set if the world has standing daily-structure rules.
- [ ] `dailyInfluenceCapGain` and `dailyInfluenceCapLoss` are written as split keys. `startingYear` and `baseYear` are equal.
- [ ] `influenceMagnitudeTiers` rungs are written in the world's own terms, if set.

### Characters

- [ ] Every character has a non-empty `name`. `lastName` is optional: the live Fields of Mistria export leaves it empty for all 38 characters, and the platform does not need it.
- [ ] Every character has `role`, `baseProfile`, `appearance`, `type` and `availableFromDay`.
- [ ] Sprite sets include at minimum Casual and Working/Active.
- [ ] Every sprite set carries a `neutral` expression, and every expression key in every sprite set is named in `availableExpressions`. A set need not carry all of them: the live Fields of Mistria export has no set with all 28 names, and the most any set carries is 18. The tier a project chooses at the start sets how many expressions to generate (`expression-standard.md`); it is not a pre-flight check, because an existing list may predate the tiers.
- [ ] No character has `availableFromDay` greater than the calendar year length.
- [ ] Each character's introduction scenario is plausible before that character's `availableFromDay`.
- [ ] `appearance` contains physical description only, with no story content and no personality, and states the apparent age (the age they appear to be, never the real age; rule in `../worldbuilder-character/card-format.md`).
- [ ] Every sprite set has its own `appearance`, starting with the character's unchanged physical-features preamble.
- [ ] `baseImage` matches the set's `expressions.neutral` where both exist.
- [ ] `color` is a Tailwind text class (`text-<hue>-<shade>`). `startingInfluence` is an integer or absent.
- [ ] Every pronoun in `appearance`, per-set `appearance` and Future Storylines agrees with the note's `sex` field.
- [ ] `baseProfile` prose is complete and in the target range (about 900 tokens supporting, about 1500 major), and all six influence bands are present in it.
- [ ] Each `baseProfile` passes the reconciliation comparison in section 5.

### Story triggers and events

- [ ] Every non-recurring trigger has `triggerOnDay` of at most twice the calendar year length. A day past one year is a second-year scene: it is allowed and listed in section 3. The same ceiling applies to lore entries.
- [ ] Two non-recurring triggers may share a day. The tone-conflict check in section 3 covers them. The live Fields of Mistria export has four such days, including two arrival-day scenes.
- [ ] Every recurring trigger is one entry per occurrence, with an absolute `triggerOnDay` inside the calendar year. A weekly market gets one entry per week, each with its own day.
- [ ] Every trigger has a non-empty `promptInjection`.
- [ ] All festival and observance events have `storyTriggers` entries. Recurring events have `recurring: true`.
- [ ] `hiddenFromPlayer: true` is set on scripted beats the player should not see announced. Public festivals are visible.
- [ ] Story intention notes with concrete triggers have `storyTriggers` entries.
- [ ] `arcManagerGuidance` is creative compass guidance, not a game-master prompt.

### Lore entries

- [ ] Every major location has a concept note and a lore entry. The Background NPC guidelines entry is present.
- [ ] Every lore entry has at least one keyword and non-empty `content`.
- [ ] `enabled` is explicitly set on every entry.
- [ ] `availableFromDay` is set on every entry per layer and is at most twice the calendar year length.
- [ ] Keywords are specific, with no partial-match traps and no multi-word compound keywords that need an unlikely exact match.

### Locations

- [ ] `locations` is an object keyed by day segment. Each segment named in `daySegments` has at least one location image.
- [ ] Location prompts describe a ground-level perspective, not an aerial or establishing shot.
- [ ] Location names use the slug format.

### Art style

- [ ] `artStyle.background` has `style_prefix`, `style_suffix`, `negative_prompt` and a `time_contexts` entry for every day segment.
- [ ] `artStyle.sprite` has `style_prefix`, `style_suffix` and `negative_prompt`.
- [ ] `artStyle.sprite.clothingRules`, when the world has world-wide costume rules, is a string array with one rule per entry.
- [ ] Negative prompts are for SDXL models only (Gemini and Imagen ignore them).
- [ ] Sprite prompts do not reference other characters, and location prompts do not reference other locations.

---

## 2. Asset preservation (re-export only)

An existing `.sbworld` holds generated assets (location images, character sprites). A re-export must carry forward every existing asset that is not being deliberately replaced. The archive's `manifest.json` lists every bundled asset by `id`, `path`, `mime` and `kind`.

- [ ] Inventory the existing assets before rebuilding: `python scripts/sbworld_tool.py extract <archive>` unpacks `world.json`, `manifest.json` and `assets/` into a new folder.
- [ ] Carry forward all `location`-kind assets unless the location was removed or its image is being regenerated.
- [ ] Carry forward all `character_sprite`-kind assets unless the sprite is being replaced.
- [ ] Verify the asset count in the rebuilt `manifest.json`: old count, minus removals, plus additions.
- [ ] Use the project's versioned `world.json` as the source of truth, never the copy inside an old archive.

---

## 3. Can-this-ever-fire detection

Run after the pre-flight check passes. It finds content that will never reach the player.

**Lore entry keyword analysis.** Search the keywords in every character's `baseProfile`, `settingSummary`, `introText`, `arcManagerGuidance`, `initialStoryArc` and every trigger's `promptInjection`.

*Will never fire (CRITICAL):*
- Keywords that appear nowhere else in the export. If no in-world content would naturally mention the term, the player never meets it and the entry is dead content.

*Unlikely to fire (WARNING):*
- Keywords that appear only in other lore entries. This is a circular dependency: entry A fires only if entry B fires first, and B may be gated too.
- Multi-word compound keywords that need an exact phrase match in conversation.
- Proper nouns that are not character names, location names or terms introduced in the opening arc.

*Fires too often (WARNING):*
- Keywords that are common English words or substrings of common words (for example, "art" matches "start", "heart" and "part").
- Keywords shorter than 4 characters.

*Timing conflicts (WARNING):*
- An `availableFromDay` that delays a lore entry past the point where its keywords would come up in the story (for example, festival lore gated to after the festival's trigger day).

**Story trigger analysis.**

*Will never fire (CRITICAL):*
- A non-recurring `triggerOnDay` greater than twice the calendar year length. This is the same ceiling as the pre-flight check.

*Listed, not failed:*
- A non-recurring trigger between one and two calendar years is a second-year scene. List each one so the human sees that it fires only in the second year of play.

*Sequencing concerns (WARNING):*
- A trigger's `promptInjection` references a character whose `availableFromDay` is after the trigger day. The character is not introduced yet.
- A trigger references content from a lore entry whose `availableFromDay` is after the trigger day.
- Two triggers on the same day whose prompt injections conflict in tone or plot direction.

---

## 4. Adjustment priority order

When the export needs condensing or tuning, adjust in this order. Earlier items are cheaper to change.

| Priority | Target | Adjustment type | Risk of degradation |
|---|---|---|---|
| 1 | Lore entry keywords | Add synonyms, broaden terms, remove overly specific phrases | Low: keywords are metadata, not prose |
| 2 | Lore entry content | Condense, clarify, remove redundancy with `settingSummary` | Low: lore is supplementary context |
| 3 | Story trigger `promptInjection` | Condense injection text, tighten narrative focus | Medium: injections shape plot direction |
| 4 | Character `baseProfile` | Condense the character note's sections, then re-export. Never edit the profile alone. | Medium: profiles are the AI's primary character knowledge |
| 5 | `settingSummary` | Condense, move detailed lore to lore entries | Medium: always-active context, core to AI behavior |
| 6 | `arcManagerGuidance` | Tighten creative direction, remove redundancy with `settingSummary` | Medium-high: guides the whole narrative engine |
| 7 | `eventCalendarSummary` / `weatherPools` | Condense prose descriptions | Low: supplementary atmosphere, rarely needed |
| 8 | Art style prompts | Do not adjust unless generation quality requires it | High: generation quality is sensitive to prompt changes |

The general principle: adjust metadata and supplementary content first (keywords, lore, weather). Adjust core narrative content (profiles, summary, guidance) only when supplementary adjustments are insufficient. Never adjust art prompts for size reasons.

---

## 5. `baseProfile` reconciliation

**Decision, recorded here:** the export settles `baseProfile` drift by reconciliation, not by derivation. The profile is not a mechanical copy of the card: Future Storylines is writing, not a transform, so a generator would need a new card-to-profile contract. Reconciliation keeps the card-assembly contract and makes the export prove it.

**The contract** is `card-assembly.md`:

- Verbatim from the character note: the preamble (no heading), Background, Body, Soul, Relationships and Voice / Dialogue.
- Transformed: Future Storylines, rewritten from Story Seeds. Rewrite it when Story Seeds changed since the last export. Keep the exported section otherwise.
- Never shipped: Intimate Dynamics and Design Notes.

**At every export, first or repeat:**

1. Re-assemble each character's `baseProfile` from the current card under the contract.
2. Diff the result against the exported `baseProfile` and apply the differences to the versioned `world.json`.
3. Pre-flight comparison: for each profile, compare the preamble and each of the five verbatim sections with the card's, after whitespace normalisation. Require a Future Storylines section.

**Condensing is made in the card.** If a profile must be shorter (adjustment order, item 4), shorten the character note and re-export. The next export then reproduces the change. A profile edited alone is overwritten by the next export.

**Consequence.** A profile that abbreviates Relationships or condenses Voice / Dialogue by hand deviates from the contract. The next export replaces those sections with the card's. If the abbreviations are wanted, make them in the card first.

---

## 6. Derived-output check

When the world has `reference/Reference sheet.md`, run the checker after `world.json` is written and reconciled, and before the archive is built:

```bash
python scripts/check_coverage.py export --world-root <project-root> --world-json <project-root>/exports/ainime/world.json
```

A FAIL line (or a non-zero exit) blocks the build. Fix the card or the export and run the check again. List any FLAGGED and PENDING lines in the Export item's record so the human sees them.

A world with no reference sheet skips this step. The step is not a pre-flight line, because the check needs the sheet and the checker stops at once without one.

---

## 7. Build

Build the archive from the three versioned inputs: `world.json`, `manifest.json` and the `assets/` folder.

```bash
python scripts/sbworld_tool.py build --world exports/ainime/world.json --manifest exports/ainime/manifest.json --assets exports/ainime/assets
```

The tool refuses to overwrite an existing archive, writes the stored (uncompressed) form the platform requires, and checks the manifest against the asset files. Read `--help` for the flags that record recomputed counts.
