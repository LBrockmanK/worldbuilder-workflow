---
name: worldbuilder-ainime-export
description: Use when exporting a completed Wide-phase worldbuilding project to ainime-games.com format. Requires complete character notes, a complete project/seed.md, and Wide-phase concept and story notes.
---

# Ainime Export

## Overview

This skill is the only one in the worldbuilder workflow that knows ainime-games field names. Every skill before this phase writes platform-agnostic notes. This skill reads those notes and packages them into the ainime `world.json` format.

Full JSON schema reference: `../../docs/target-system.md`.

---

## Prerequisites

Before running export, verify:
- [ ] `project/seed.md` tagged `complete` (all sections present)
- [ ] Every character note in `notes/` carries a closed status tag
- [ ] Concept notes in `notes/` written with `layer` set
- [ ] `project/direction.md` and the story notes (arcs, key intentions) in `notes/` tagged `complete`
- [ ] Every character has an Introduction entry in Story Seeds

If any prerequisite is incomplete, return to the relevant Wide-phase skill rather than exporting a partial world.

---

## Field Map

Fields are marked **required** or **optional**. Required fields must be present in every export; optional fields are included when the world needs them.

| Source | ainime JSON field(s) | Req? |
|---|---|---|
| `project/seed.md` — Setting Summary | `settingSummary` | **req** |
| `project/seed.md` — Genre and Tone | `genre` | opt |
| `project/seed.md` — Inspirations | `inspirations[]` | opt |
| `project/seed.md` — Tonal Inspirations | `tonalInspirations[]` | opt |
| `project/seed.md` — Key Tropes and Themes | `keyTropesAndThemes[]` | opt |
| `project/seed.md` — Community | `communityDescription` | opt |
| `project/seed.md` — World Introduction | `introText` | opt |
| `project/seed.md` — Opening Situation | `initialStoryArc` | opt |
| builder-specified | `authorCredit` | opt |
| `project/seed.md` — era (from story direction or seed) | `calendarConfig.eraReminder` | opt |
| builder-specified | `calendarConfig.startingYear`, `calendarConfig.baseYear` | opt |
| builder-specified | `calendarConfig.dailyInfluenceCapGain`, `calendarConfig.dailyInfluenceCapLoss` | opt |
| builder-specified (derived from the world's stakes) | `calendarConfig.influenceMagnitudeTiers` | opt |
| builder-specified | `calendarConfig.earliestClosePrompts`, `minPromptsBeforeTransition`, `usualMaxPrompts` | opt |
| builder-specified | `calendarConfig.dailyPlannerDirective` | opt |
| `project/direction.md` + story arc notes in `notes/` | `yearContexts` | opt |
| builder-specified (set in the platform's Adventure tab) | `generateSideCharacterOnNewGame` | opt |
| `project/direction.md` | `arcManagerGuidance` | opt |
| intention story notes + event notes in `notes/` | `storyTriggers[]` (including `hiddenFromPlayer`) | opt |
| event notes in `notes/` | `calendarConfig.weatherPools`, `eventCalendarSummary` | opt |
| concept notes in `notes/` | `loreEntries[]` | opt |
| character notes in `notes/` | `characters[]` | **req** |
| `project/seed.md` — Art style | `artStyle.background.*`, `artStyle.sprite.*` | opt |
| `project/seed.md` — Art style | `artStyle.timeOfDayLighting.*` | opt |
| character notes (Body sections) | `artStyle.sprite.clothingRules[]` | opt |
| `project/seed.md` — expression tier | `availableExpressions[]` | opt |
| builder-specified | `locations[]` | opt |
| builder-specified | `moods` | opt |
| builder-specified | `theme` | opt |
| builder-specified | `customPrompts` | opt |

---

## Updating an Existing Export

The .sbworld file is the only true export output — it is what the ainime platform consumes. There is no authoritative standalone world.json; the world.json lives inside the .sbworld archive.

An exported .sbworld accumulates manual tweaks — expanded opening arcs, rewritten lore entries, adjusted character cards. A re-export must never overwrite those changes silently.

**Always use the diff workflow.** `scripts/export_diff.py` extracts world.json from the existing .sbworld, generates candidate field values from the source documents (seed.md, direction.md), and diffs them. Only the fields you name are updated, and the .sbworld is repacked in place.

```bash
# show what differs between source docs and the current .sbworld
python scripts/export_diff.py <project-root>

# apply specific fields
python scripts/export_diff.py <project-root> --apply communityDescription arcManagerGuidance

# apply everything (use only when the diff has been reviewed)
python scripts/export_diff.py <project-root> --apply-all
```

Fields not covered by the script (characters, lore entries, calendar events) are updated by extracting world.json from the .sbworld, editing it, and repacking — never by regenerating the whole file.

**Every edit session must end with repacking.** The standalone world.json is a working copy, not the export. After any manual edits to world.json, repack it into the .sbworld before reporting the work as done. An edit that touches world.json but not the .sbworld has changed nothing the platform will see.

---

## Setting and Adventure Fields

Read `project/seed.md` and extract the following. The section names in the seed map directly.

**`settingSummary`** (required) — The AI's primary reference for every scene. Describe the world in detail: where and when the story takes place, technology level and what exists (and what doesn't), cultural norms, social structure, daily life, and the general feel of the world. The more detail, the more consistent and immersive the AI's scenes. Setting Summary section from seed, verbatim.

**`genre`** (optional) — Genre and Tone section verbatim.

**`inspirations`** (optional) — Inspirations section as a string array. One entry per line item.

**`tonalInspirations`** (optional) — Tonal Inspirations section as a string array. One entry per line item.

**`keyTropesAndThemes`** (optional) — Key Tropes and Themes section as a string array. One entry per line item.

**`communityDescription`** (optional) — Short blurb shown in the community world list. This is a description for potential players browsing the ainime community, not an in-game description of the setting's social dynamics. Community section from seed, verbatim.

**`introText`** (optional) — Shown to players when starting a new game. Set the scene: what do they need to know before they step into the world? World Introduction section from seed, verbatim.

**`initialStoryArc`** (optional) — Seeds the main plot at game start — the "global adventure arc," a multi-character web of drama that runs for roughly 14 in-game days. The specific story you want to unfold: who is involved, what's the inciting incident, what's the tension. Can be very specific (naming characters, situations) or thematic. Leave empty for a fully randomized opening arc. Opening Situation section from seed on initial export; commonly expanded manually afterward to include the full scripted opening sequence. The diff workflow preserves those expansions.

**`authorCredit`** (optional) — Your name or Discord handle, shown when sharing your world in the community.

**`calendarConfig.eraReminder`** (optional) — Injected into AI context every day to keep the technology level consistent. Extract from the seed's era description. Leave blank for no restriction.

**`calendarConfig.seasons`, `daysPerSeason`, `daysOfWeek`, `daySegments`** — Structural calendar configuration. Defaults: 4 seasons, 28 days/season, standard day names. Day segments default to Morning/Afternoon/Evening/Night — 4 segments is the recommended sweet spot (the engine is tuned for it), but 3 works fine. Change any of these to fit the world.

**`calendarConfig.startingYear`** / **`calendarConfig.baseYear`** (optional, integer) — The calendar year Day 1 starts in. Use 1400 for medieval, 3025 for sci-fi, etc. Newer platform builds read `baseYear`; current exports carry both keys with the same value. Write both, and keep them equal.

**`generateSideCharacterOnNewGame`** (optional, boolean) — The Adventure tab's "AI generate side character" toggle. When `true`, the platform has the AI generate a side character at New Game (how many, and on what basis, is not yet verified against the platform). This is a builder choice, not world content: no note supplies it, and the export never sets it from the notes. A re-export preserves whatever value the existing `.sbworld` holds. The Adventure tab's other New Game toggles (randomize the opening arc, ignore the opening arc, random NPC romance pair) are app-level settings that never appear in the `.sbworld`.

---

## Calendar Configuration

Read `calendar.md` (this skill's reference file) for design guidance on weather pools, festival layout, and day-segment defaults before building this section.

**`calendarConfig.dailyInfluenceCapGain`** (optional, integer) — Maximum positive influence a character can gain per day. Lower values mean slower relationship growth. Default is 5.

**`calendarConfig.dailyInfluenceCapLoss`** (optional, integer) — Maximum negative influence a character can lose per day. Lower values mean slower relationship decay. Default is 5.

Older exports carry a single `calendarConfig.dailyInfluenceCap` field. Where an existing `.sbworld` still has it alongside the split keys, the split keys take precedence; write the split keys.

**`calendarConfig.influenceMagnitudeTiers`** (optional, multi-line string) — The influence magnitude ladder: one rung per line, value first, each naming the kind of act worth that many points in this world. The highest rung is the ceiling the AI cannot pass, and each rung spends that many points of the daily cap. Write the rungs in the world's own terms:

```
±1: A small daily kindness or friction — a compliment on their work, a careless remark
±2: A meaningful gesture or genuine hurt — a thoughtful gift, a broken confidence
±3: A life-shaping act — saving someone from danger, a deep betrayal of trust
```

**Scene-ending guidance** (optional, integers) — `calendarConfig.earliestClosePrompts` (the earliest prompt count at which a scene may close cleanly), `calendarConfig.minPromptsBeforeTransition` (the usual minimum), and `calendarConfig.usualMaxPrompts` (the usual maximum). Platform values in current exports are 6, 10 and 16. Change them only when the world's scenes should run deliberately shorter or longer.

**`calendarConfig.dailyPlannerDirective`** (optional) — Standing rules about daily structure. The platform UI now labels it "Daily Directive": the scene AI sees it at every scene opening as the standing shape of the day, before any day-specific events. The JSON key is unchanged. Examples: "On weekdays, morning and afternoon MUST be classroom lessons. Evenings are free." / "Every day must include at least one scene in the guild hall." / "Weekend days are fully open for character-driven activities."

**`calendarConfig.weatherPools`** (optional) — Nested object: season → day segment → string array. Each string is a one-line weather description. 10–16 entries per season/segment. The segments must match the project's `daySegments` configuration. Derive from `project/seed.md` and the world's setting; see `calendar.md` for writing guidance.

```json
{
  "Spring": {
    "Morning": ["Light fog lifting...", "Crisp clean air..."],
    "Afternoon": ["..."],
    "Evening": ["..."]
  }
}
```

Note: if the project uses 4 day segments (the platform default), add a `"Night"` key to each season as well.

**`eventCalendarSummary`** (optional) — Prose overview of the event calendar for LLM reference. Summarize the festival calendar and its emotional rhythms after all events are written.

**`storyTriggers[]` (calendar events)** — One entry per event note. Recurring annual events use `recurring: true` in the output. See `calendar.md` for how to derive `triggerOnDay` from the timing language that opens each event note's What Happens section, and how to write effective `promptInjection` content.

```json
{
  "id": "uuid",
  "name": "Event name",
  "triggerOnDay": 8,
  "promptInjection": "Active creative direction injected on this day.",
  "recurring": true,
  "hiddenFromPlayer": false
}
```

`triggerOnDay` is the absolute calendar day (1–112 for the 4×28 default). `promptInjection` is active direction to the story engine, not a neutral description of the event.

**`hiddenFromPlayer`** (optional, boolean) — Marks a trigger as hidden from the player. The intended reading is that the trigger still fires and injects its `promptInjection` while the player is not shown it in advance; that runtime behavior is inferred from the field name and from how existing exports use it, not confirmed against the platform. Set it on scripted story beats and introductions the player should meet in play rather than see announced (an arrival sequence, a character's first appearance, a story gate). Leave it `false` or absent on public festivals and observances the townsfolk would know about.

### Life Stages (`yearContexts`, optional)

Life stages describe how the world changes from one in-game year to the next, as a top-level `yearContexts` object with one entry per year. Read `life-stages-and-prompts.md` (this skill's reference file) for the entry shape and the purpose of each field before writing it. A world with no year-over-year change omits `yearContexts`.

---

## Story Direction and Triggers

**`arcManagerGuidance`** — General creative direction that steers the AI throughout the entire game. Not a specific plot — a creative compass. What kinds of adventures should it create after the opening arc concludes? What themes should it keep coming back to? Read `project/direction.md` and export verbatim; do not summarize. The platform's own examples of what belongs here:

- Keep things grounded — no supernatural elements.
- Romance should always be complicated by external pressures.
- Lean into political intrigue between factions.
- After major arcs, give characters breathing room with slice-of-life moments.
- Lean into moral ambiguity. No clear villains — everyone has reasons.

**`storyTriggers[]` (story events)** — One entry per intention story note where a trigger condition can be expressed as a calendar day or a story moment. Intentions without a concrete trigger day do not produce `storyTriggers` entries; they remain in the `arcManagerGuidance` as ongoing direction instead.

---

## Lorebook Entries

Read all concept notes in `notes/`. Each note produces one `loreEntry`.

```json
{
  "id": "lore_{timestamp}_{random}",
  "keywords": ["keyword1", "keyword2+keyword3"],
  "content": "Lore text injected when keywords match.",
  "enabled": true
}
```

**Entry scope** — A lore entry should provide specific, non-obvious information the AI needs at the moment a topic arises. Do not create entries for concepts self-evident to any player (what calendars are, what fishing means, what weather does). Do not create entries for systems already handled by other fields — homestead setup belongs in the setting summary, town restoration guidance in arc manager direction, weather in calendar config. Prefer seasonal entries naming specific in-world items (crops, forageables, fish, insects by season) over generic activity descriptions.

**Explicit keywords.** If a concept note has a non-empty `keywords`
frontmatter field, use those values directly as the entry's
`keywords[]`. Do not derive from aliases or body terms — the author
has specified the trigger words. When the field is absent or empty,
fall back to the derivation rules below.

**Keywords** — Derive from the note's `aliases` frontmatter and any key terms in the note body. Use `+` between words for AND (both must appear together). Single terms are OR with other array entries. Keep keywords specific enough that they only fire when the topic is actually relevant.

**Content** — Summarize the concept note into a precise, dense lore injection. 50 tokens of exact context beats 300 tokens of vague description. Aim for what the AI most needs to know at the moment the topic arises.

**`availableFromDay`** — Set based on the note's `layer` frontmatter:
- `surface` — active from day 1
- `mid` — active from day 14 (one half-season in)
- `deep` — active from day 56 (two seasons in)
Adjust thresholds based on world pacing if these defaults don't fit.

**Enabled** — All entries default to `true`. Set `false` only for entries that should exist in the export but never activate.

---

## Character Export

For each character note in `notes/`, produce a character record. Process one character at a time; read `card-assembly.md` before writing the card.

| Character note field | ainime JSON field | Req? |
|---|---|---|
| Character name | `name`, `lastName` | **req** / opt |
| Major/Supporting (cast plan entry in `project/plan.md`) | `type`: `"main"` or `"side"` | opt |
| Derived by export skill | `role` | opt |
| Assembled card prose | `baseProfile` | opt |
| Body preamble | `appearance` | opt |
| Sprite sets (see below) | `spriteSets[]` | opt |
| Available Day (see below) | `availableFromDay` | opt |
| Builder-specified | `startingInfluence` | opt |
| Builder-specified (from the character's palette) | `color` | opt |
| `sex` frontmatter field | none — read for pronoun accuracy, never exported | — |

**`name`** (required) / **`lastName`** (optional) — Extract from the character note filename.

**`type`** (optional) — `"main"` for major characters, `"side"` for supporting. Main characters get dedicated story arcs, fully generated personality traits, likes/dislikes, and relationship dynamics. All characters are romanceable. Maps from the character's Major/Supporting designation in the cast plan (`project/plan.md`).

**`role`** (optional) — Not stored in the character note. Derive from the character's function as established by the character note content (their position in the world, their relationship to the player, their narrative role). Write as plain text. Examples: "The player's mysterious neighbor; a hacker with a heart of gold."

**`baseProfile`** (optional) — The character card prose. Include personality, psychology, backstory, motivations, quirks, speech patterns. Optionally add a "Future Storylines" section at the end to guide what happens after the character's initial story arcs conclude. See `card-assembly.md` for full assembly guidance. This is the most complex field; do not attempt it without reading that file.

**`appearance`** (optional) — Used for sprite generation and as context for all in-game AIs. Use the Body section's appearance preamble of the character note verbatim or lightly condensed. Cover species/type and sex if relevant, age presentation and body type, notable features, clothing style.

**`startingInfluence`** (optional, integer) — Initial relationship value for this character, which may be negative (`-10` for a character who starts out hostile to the player). Omit the key to let the platform assign its default; the UI shows the omitted state as "Auto". Never write the string `"Auto"`.

**`color`** (optional, string) — The character's name color in dialogue, as a Tailwind CSS text-color class: `"text-pink-400"`, `"text-emerald-400"`, `"text-rose-700"`. Pick a hue from the character's own palette (hair, signature garment) and keep colors distinct across the main cast so speakers are easy to tell apart. Do not write a hex value or a bare color name.

**`sex`** (internal, character note only) — The character note's `sex` field records the character's sex so every generated text uses the right pronouns. It is worldbuilder schema, not ainime schema: the export never writes a `sex` key to `world.json`. Read it before writing `appearance`, per-set `appearance` and Future Storylines, and check that every pronoun in those fields agrees with it. Where the character's sex matters to how they look, state it in `appearance` in plain words.

**Body preamble → appearance:** The Body appearance preamble provides
the character's physical description for the appearance field.

**Story Seeds → Future Storylines:** Each Story Seed entry maps to
a future storyline. The export transforms definite scenario prose to
possibility-style framing. Trigger conditions that the platform
cannot mechanically enforce are woven into the storyline context as
narrative framing.

---

## Available Day Assignment

`availableFromDay` controls the earliest day the player can encounter this character. Assign based on narrative logic, not the export skill's defaults — the right day varies by world.

Guidelines:
- Day 1–3: characters the player would plausibly meet on arrival
- Day 7–14: characters tied to weekly routines or early story beats
- Day 15–28: characters the player needs to seek out or earn access to
- Day 29+: characters behind story gates or late-world reveals

Check all introduction notes to ensure each character's introduction scene can actually occur before their `availableFromDay`.

---

## Sprite Sets

`spriteSets` are named visual states for artwork — not emotional expressions. Expressions exist within states; states are the costume/context categories.

```json
[
  {
    "name": "default",
    "description": "Casual, at rest — the character's natural default state",
    "expressions": {
      "neutral": "image generation prompt for this state and expression"
    },
    "appearance": "Physical-features preamble, then this set's outfit.",
    "baseImage": "asset://sandboxWorldAssets/<uuid>",
    "basePrompt": "image generation prompt for this set's base image"
  }
]
```

Each sprite set carries three fields beyond `name`, `description` and `expressions`:

- **`appearance`** (optional, string) — What the character looks like in this set. Start with the character's physical-features preamble (hair, eyes, skin, build, species features), written identically in every set, then describe this set's outfit. Only the outfit part varies between sets. No personality, story or pose content. The character-level `appearance` equals the default set's `appearance`.
- **`baseImage`** (optional, string) — The set's reference image: an `asset://sandboxWorldAssets/<uuid>` reference. Set it to the same asset as the set's `expressions.neutral` when that image exists, so the platform generates the other expressions from the same base.
- **`basePrompt`** (optional, string) — The image-generation prompt for the set's base image. Not yet seen in an inspected export: the purpose here is read from the field name and its pairing with `baseImage`, and is unverified. Until it is confirmed, write it from the set's `appearance` only when the platform is to generate the base image, and leave it out when `baseImage` points to a bundled asset.

Every character needs at minimum:
- **Casual** (`name: "default"`) — at rest, natural state
- **Working/Active** — doing their primary activity

Add additional states only where they're meaningfully distinct from the above (Formal for a character who attends ceremonial occasions; Combat for a fighter, etc.). Do not create states for transient emotional conditions.

The `description` drives art generation context; keep it concrete and consistent with the character's Body preamble. The `expressions.neutral` prompt is the base image generation prompt for that state.

### Expression tier

The number of expressions per sprite set depends on the project's chosen expression tier: **Essential**, **Standard** or **Expansive**, each a strict superset of the one before. Standard is the recommended default; Essential suits large casts or tight generation budgets; Expansive gives the full emotional range. The tier names carry no counts on purpose, so a change in membership never renames a tier.

This skill does not hold the tier definitions. Tier membership, expression counts, narrative roles and the cost table live in the Image Gen expression standard, the shared Ainime reference for sprite expressions: `Projects/Ainime/Image Gen/Expression standard.md` in the Anima vault. Until that note is written, the same standard is at `Projects/Ainime/Fields of Mistria/repo/Fields-of-Mistria/Sprite Expression Workflow/Expression Standard.md`. Read it when choosing the tier, then write the chosen tier's expressions to `availableExpressions` (snake_case, as the platform requires).

---

## Art Style Prompts

Read the Art style section of `project/seed.md`. Translate the plain-language reference into prompt-engineering format. These prompts are prepended/appended to every AI-generated image.

### Time-of-Day Lighting (optional)

Per-segment lighting descriptions injected into every background prompt between the scene description and the style suffix. The final prompt is: `prefix + scene + lighting + suffix`. One field per day segment (Morning, Afternoon, Evening, and Night if using 4 segments). Leave empty for segments that don't need specific lighting direction. The platform can AI-generate these from the world's setting.

### Background Generation

**`artStyle.background.style_prefix`** (optional) — Prepended to all background prompts. Should establish the visual style consistently: rendering style, color palette tendencies, era cues. Include ground-level perspective direction (eye-level, first-person viewpoint) — backgrounds are seen from the player's position, not from above.

**`artStyle.background.style_suffix`** (optional) — Appended to background prompts. Typically quality modifiers and technical parameters. Reinforce perspective (ground-level shot) and emptiness (no people, uninhabited).

**`artStyle.background.negative_prompt`** (optional) — Elements to suppress across all backgrounds. SDXL models only (e.g. Nova Anime XL) — ignored by Gemini/Imagen. Always include people/person/figure/crowd/character — location backgrounds are empty scenes with no people unless a specific location is deliberately designed to include them. Suppress aerial perspectives: overhead view, isometric, bird's eye view, top-down, aerial view.

### Sprite Generation

**`artStyle.sprite.style_prefix`** / **`style_suffix`** / **`negative_prompt`** (optional) — Same structure for character sprites. Sprite style should be consistent with background style but may have different technical requirements (transparent background, consistent character proportions). Negative prompt is SDXL only — ignored by Gemini/Imagen.

**`artStyle.sprite.clothingRules`** (optional, string array) — Clothing directives for sprite generation, one rule per array entry (the UI shows one per line). Use them for world-wide costume rules: recognizable silhouettes and color motifs per character, a uniform element a faction always wears, a ban on copying costumes from existing franchises. Derive them from the character notes' Body sections and the seed's art style reference.

**`artStyle.sprite.maintainConsistency`** (optional) — When enabled, appends "Same character, same background." during sprite generation to improve visual consistency across expressions.

Do not attempt to write `artStyle` content during Wide-phase work — this is a prompt-engineering output that belongs here.

---

## Locations

Stock locations are optional — when image generation is enabled in-game, the AI creates locations on the fly. Stock locations are used in hybrid mode (AI picks from stock when a match exists, generates when it doesn't) or when image generation is turned off entirely (stock images are the only backgrounds).

**Naming matters.** The location name is the **only thing the AI sees** when choosing a background — make it descriptive. Use underscores to separate words. Include the place, its vibe or details, and optionally a character owner. Examples: `cafe_cozy_morning`, `hidden_shrine_ruins_mistymorning`, `alex_apartment_livingroom_evening`, `rooftop_bar_cityview_evening`. The more descriptive the name, the better the AI matches scenes to locations.

Locations are organized by day segment (one background image per segment per location). The AI Location Builder can generate location names and image prompts from the world's setting, arcs, characters, and lorebook. It runs iteratively — the first run creates the most essential locations, each subsequent run fills in more niche and atmospheric spots.

---

## Moods

Audio tracks for the world. Two categories:

### System Moods (optional)

Six fixed slots triggered by the game engine (not the AI). Author one audio track per slot — leave any slot empty for silence at that moment. Slots cannot be renamed or removed.

- **Main Menu** (`main_menu`) — plays on the title screen, during new-game generation, and on the endgame/credits screen.
- **Segment Transition** (`segment_transition`) — brief musical transition between day segments (Morning to Afternoon, Afternoon to Evening).
- **Day Transition** (`day_transition`) — plays when the day ends and transitions to the next day (going to sleep).

### Gameplay Moods (optional)

AI-picked moods. The AI chooses the best-fitting mood name each turn from this list. Add as many as you want — more specific moods (signature character themes, locale-specific tracks) give the AI richer choices.

---

## Theme (optional)

Visual customization of the game UI. Not world content — purely presentation.

- **Custom Colors** — Primary Accent (borders, glows), Secondary Accent (UI text, labels), textbox gradient colors.
- **Typography** — custom font for dialogue text. When "Override player font" is on, this font applies to everyone who plays this world.

---

## Prompts (optional)

Per-AI-persona prompt overrides, on the platform's Prompts tab. Most worlds do not need them, and the export does not produce prompt sets: it leaves `activePromptSet` as it finds it. Read `life-stages-and-prompts.md` for the personas, how prompt sets are stored, and when custom prompts are worth writing.
---

## Self-Check Before Export Complete

**Setting fields**
- [ ] `settingSummary` present and detailed (required)
- [ ] `communityDescription` is a player-facing blurb, not an in-game description
- [ ] `introText` sets the scene for a new player
- [ ] `inspirations` and `tonalInspirations` are arrays, one item per source
- [ ] `keyTropesAndThemes` has 8–12 entries

**Calendar**
- [ ] `daySegments` match the project's intended day structure
- [ ] `weatherPools` covers all seasons and all configured day segments
- [ ] All festival and observance events have `storyTriggers` entries
- [ ] Recurring events have `recurring: true`
- [ ] `eventCalendarSummary` written
- [ ] `dailyPlannerDirective` set if the world has standing daily-structure rules
- [ ] No `triggerOnDay` exceeds calendar year length (112 for 4×28)
- [ ] No duplicate non-recurring triggers on the same day
- [ ] `hiddenFromPlayer: true` on scripted beats the player should not see announced; public festivals visible
- [ ] `dailyInfluenceCapGain` / `dailyInfluenceCapLoss` written as split keys; `startingYear` and `baseYear` equal
- [ ] `influenceMagnitudeTiers` rungs written in the world's own terms, if set

**Lorebook**
- [ ] Every major location has a concept note → lore entry
- [ ] Background NPC guidelines entry present
- [ ] `availableFromDay` set on all entries per layer
- [ ] Keywords are specific; no partial-match traps
- [ ] No lore entry has keywords that appear nowhere else in the world (dead content)
- [ ] No multi-word compound keywords requiring unlikely exact matches

**Story direction**
- [ ] `arcManagerGuidance` is creative compass guidance, not a GM prompt
- [ ] Story intention notes with concrete triggers have `storyTriggers` entries

**Characters (per character)**
- [ ] `name` present (required); other fields filled as applicable
- [ ] `baseProfile` prose is complete and in target range (~900 supporting, ~1500 major tokens)
- [ ] All six influence bands present in the card
- [ ] Sprite sets include at minimum Casual and Working/Active
- [ ] Introduction Story Seed present, introduction scenario plausible before `availableFromDay`
- [ ] Expressions match the project's chosen tier (Essential / Standard / Expansive) as the Image Gen expression standard defines it
- [ ] Every sprite set has its own `appearance`, starting with the character's unchanged physical-features preamble
- [ ] `baseImage` matches the set's `expressions.neutral` where both exist
- [ ] `color` is a Tailwind text class (`text-<hue>-<shade>`); `startingInfluence` is an integer or absent
- [ ] Every pronoun in `appearance`, per-set `appearance` and Future Storylines agrees with the note's `sex` field

**Art style**
- [ ] Background and sprite prefix/suffix present if using AI generation
- [ ] Negative prompts are for SDXL models only (Gemini/Imagen ignore them)
- [ ] Time-of-day lighting set if the world needs per-segment atmosphere

---

## Can-This-Ever-Fire Detection

Run after export assembly to identify content that will never reach the player.

**Lore entry keyword analysis.** For each lore entry, check:
- Keywords appearing nowhere else in the world (character cards, other lore, story triggers, setting fields) — the entry will never fire. **CRITICAL.**
- Keywords appearing only in other lore entries — circular dependency, no player-facing trigger. **WARNING.**
- Multi-word compound keywords requiring exact co-occurrence — may be too specific to fire naturally. **WARNING.**
- `availableFromDay` set past when the topic would naturally surface — timing conflict. **WARNING.**

**Story trigger analysis.** For each story trigger, check:
- `triggerOnDay` exceeding calendar year length — will never fire. **CRITICAL.**
- `promptInjection` referencing a character or lore concept not yet introduced by that day — sequencing concern. **WARNING.**
- Two triggers on the same day with conflicting emotional tones — sequencing concern. **WARNING.**

---

## Adjustment Priority Order

When an export needs condensing or reformatting, adjust in this order — lowest-risk first, highest-risk last:

1. **Lore keywords** — tighten or broaden keyword targeting (low risk)
2. **Lore content** — condense entry text (low risk)
3. **Story trigger promptInjection** — condense injection text (medium risk)
4. **Character baseProfile** — condense card prose (medium risk)
5. **settingSummary** — condense setting context (medium risk)
6. **arcManagerGuidance** — condense direction (medium-high risk — this is the primary creative guard)
7. **eventCalendarSummary / weatherPools** — condense calendar prose (low risk, but late in priority because rarely needed)
8. **Art style prompts** — never adjust for size (high risk — prompt changes alter visual output)
