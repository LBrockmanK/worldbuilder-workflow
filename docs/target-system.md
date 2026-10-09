# Target System — Field Reference

The ainime-games.com world builder stores all world configuration in a `.sbworld` archive (a ZIP containing `world.json` + image assets). This document is the authoritative map of the `world.json` schema: every field we write, what goes in it, and which skill produces it.

All field names below are the exact JSON keys. These fields are produced by `worldbuilder-ainime-export`, which reads from platform-agnostic Wide-phase notes. The Skill column shows the Wide-phase skill that authors the source content.

**Format version:** 2 (`.sbworld` — current). Earlier `.json` exports may have different or missing fields.

**ZIP format:** The `.sbworld` archive must use `STORED` compression (compress_type 0) for all entries. The platform cannot read deflated entries — assets will appear blank. Structure: `manifest.json` and `world.json` at root, all bundled files under `assets/`, plus an `assets/` directory entry.

---

## Setting Tab

| JSON field | UI label | Type | Source content skill |
|---|---|---|---|
| `worldName` | World Name | string | World configuration |
| `settingSummary` | Setting Summary | string | `worldbuilder-world-foundation` → `foundation.md` |
| `genre` | Genre & Tone | string | `worldbuilder-world-foundation` → `foundation.md` |
| `inspirations` | Inspirations | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `tonalInspirations` | Tonal Inspirations | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `keyTropesAndThemes` | Key Tropes & Themes | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `communityDescription` | Community Description | string | `worldbuilder-world-foundation` → `foundation.md` |
| `introText` | World Introduction | string | `worldbuilder-world-foundation` → `foundation.md` |

### Field notes

**`settingSummary`** — The primary always-active context the engine reads for every scene. Should establish where, when, what the community is like, what the player's situation is, and what the overall tone is. Write it as concrete and specific as possible — this is the context the AI reads constantly.

**`genre`** — Full field label is "Genre & Tone". Not just a genre tag; it is an explicit description for the AI covering primary genre, tonal range (how dark can it go, how light), and content notes.

**`inspirations`** — One string per item. Include what is specifically drawn from each reference, not just the title. `"Stardew Valley — farming life rhythm and community bonds"` not `"Stardew Valley"`.

**`tonalInspirations`** — Same format as `inspirations`. Films, books, music, anime — media that captures the right feel even if it doesn't share the genre.

**`keyTropesAndThemes`** — One string per item. 8–12 entries covering both setting tropes and emotional themes. These shape what the AI treats as thematically available throughout the game.

**`communityDescription`** — The community's social and emotional identity. Not a physical description and not a repeat of `settingSummary` — this is specifically how the community behaves and feels as a social entity. Used as context for how background characters and social dynamics should read.

**`introText`** — Pre-game text the player reads before creating their character. Sets expectations for tone and situation. The player creates only name and appearance — the intro should reflect that. Typically 2–4 short paragraphs.

---

## Adventure Tab

| JSON field | UI label | Type | Source content skill |
|---|---|---|---|
| `initialStoryArc` | Opening Story Arc | string | `worldbuilder-world-foundation` → `foundation.md` |
| `arcManagerGuidance` | Ongoing Story Direction | string | `worldbuilder-story` → `project/direction.md` |
| `storyTriggers` | Story Triggers (Events) | StoryTrigger[ ] | `worldbuilder-story` (intention notes) + `worldbuilder-concept` (recurring event notes) → `notes/` |
| `generateSideCharacterOnNewGame` | AI generate side character | boolean | Builder choice in the platform; no note source |

### Field notes

**`initialStoryArc`** — A brief, evocative description of the situation when the player arrives. Not a scripted sequence — it sets the stage. Drafted in the Foundation phase and refined after the cast exists. See `worldbuilder-story` for content guidance.

**`arcManagerGuidance`** — The engine's standing creative brief throughout the game. The primary guard against escalation, flattening, and inappropriate pacing. Covers: author framing, romance pacing, dark themes, hidden layer handling, seasonal tone, pacing. This is one of the most important fields; a weak brief here degrades every scene the engine generates. See `worldbuilder-story` for the full template.

**`storyTriggers`** — Named events with a day trigger and a narrative injection prompt. When the trigger day is reached (or when a recurring event's anniversary arrives), the `promptInjection` text is injected into the engine's context.

StoryTrigger schema:
```json
{
  "id": "uuid",
  "name": "Event name",
  "triggerOnDay": 8,
  "promptInjection": "Narrative direction text injected on this day.",
  "recurring": false,
  "hiddenFromPlayer": true
}
```

`hiddenFromPlayer` (boolean, optional) marks a trigger as hidden from the player. Exports set it on scripted story beats and introductions and leave public festivals visible; the runtime behavior (the trigger still fires, the player is not shown it in advance) is inferred, not confirmed against the platform.

**`generateSideCharacterOnNewGame`** — When `true`, the platform has the AI generate a side character at New Game (count and basis not yet verified). A builder choice set in the platform; the export preserves the existing value and never derives it from notes. The Adventure tab's other New Game toggles (randomize the opening arc, ignore the opening arc, random NPC romance pair) are app-level settings and never appear in the `.sbworld`.

Set `recurring: true` for annual events (festivals, observances). One-time events use `recurring: false`. Recurrence is yearly only — there is no weekly or monthly repeat. To make a weekly event (e.g., a Saturday market), create a separate `storyTrigger` entry for every instance across the first year, each with its own `triggerOnDay` and `recurring: true` so it repeats in subsequent years.

---

## Calendar Tab

| JSON field / path | UI label | Type | Source content skill |
|---|---|---|---|
| `calendarConfig.seasons` | Seasons | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `calendarConfig.daysPerSeason` | Days per Season | number | `worldbuilder-world-foundation` → `foundation.md` |
| `calendarConfig.daysOfWeek` | Days of Week | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `calendarConfig.daySegments` | Day Segments | string[ ] | `worldbuilder-world-foundation` → `foundation.md` |
| `calendarConfig.eraReminder` | Era | string | `worldbuilder-world-foundation` → `foundation.md` |
| `calendarConfig.weatherPools` | Weather Pools | object | `worldbuilder-calendar` → `notes/` (event notes) |
| `storyTriggers` | Events / Recurring Events | StoryTrigger[ ] | `worldbuilder-calendar` → `notes/` (event notes) |
| `eventCalendarSummary` | Event Calendar Summary | string | `worldbuilder-calendar` → `notes/` (event notes) |
| `calendarConfig.startingYear`, `calendarConfig.baseYear` | Starting Year | integer | Builder choice; both keys present, equal |
| `calendarConfig.dailyInfluenceCapGain` / `dailyInfluenceCapLoss` | Daily Influence Cap (Gain / Loss) | integer | Builder choice (default 5) |
| `calendarConfig.influenceMagnitudeTiers` | Influence Magnitude Ladder | string (one rung per line) | Builder choice, written in the world's terms |
| `calendarConfig.earliestClosePrompts` / `minPromptsBeforeTransition` / `usualMaxPrompts` | Scene Ending Guidance | integer | Builder choice (platform values 6 / 10 / 16) |
| `yearContexts` | Life Stages | object keyed `"0"`, `"1"`, … | `project/direction.md` + arc notes; see the export skill's Life Stages section |

> **`dailyPlannerDirective`** — String field, labelled "Daily Directive" in the platform UI. The scene AI sees it at every scene opening as the standing shape of the day (for example, what each day segment is for). Story-level guidance belongs in `arcManagerGuidance`.

### Field notes

**`calendarConfig.eraReminder`** — One phrase describing the technology and cultural reference point. The engine uses this to calibrate anachronism. Decided in the Foundation phase. Example: `"Contemporary rural — smartphones exist but signal is bad."` or `"Pre-industrial fantasy, no electricity."`

**`calendarConfig.weatherPools`** — Nested object: season → day segment → string array. Each string is a one-line weather description. The AI picks from the pool when generating scenes. Aim for 10–16 entries per season/segment combination.

```json
{
  "Spring": {
    "Morning": ["Light fog lifting...", "Crisp clean air..."],
    "Afternoon": ["..."],
    "Evening": ["..."],
    "Night": ["..."]
  }
}
```

**`storyTriggers`** — The calendar events field. Both recurring annual events (`recurring: true`) and one-time events (`recurring: false`) are stored here. See the Adventure tab section above for the schema.

**`eventCalendarSummary`** — Narrative overview of the full event calendar for LLM reference. A prose summary of the festival calendar and its emotional rhythms — written for the AI, not the player. Produced after all events are written.

**`calendarConfig.seasons`, `daysPerSeason`, `daysOfWeek`, `daySegments`** — Structural configuration. Defaults: 4 seasons, 28 days per season, standard day names, Morning/Afternoon/Evening/Night. Change only if the world needs a different time structure.

---

## Lore Tab

| JSON field path | Type | Skill |
|---|---|---|
| `loreEntries` | LoreEntry[ ] | `worldbuilder-concept` |

### LoreEntry schema

```json
{
  "id": "lore_{timestamp}_{random}",
  "keywords": ["keyword1", "keyword2+keyword3"],
  "content": "Lore text injected when keywords match.",
  "enabled": true
}
```

**`keywords`** — Array of trigger strings. Comma-separated entries are OR (any one triggers). Use `+` between words for AND (both must appear). Keep keywords specific enough that they only fire when the topic is actually relevant.

**`content`** — The lore text injected into context when keywords match. Aim for precision over length — 50 tokens of exact context beats 300 tokens of unfocused description.

**`enabled`** — Boolean. Disabled entries exist but never trigger.

**Date gates** — The UI shows an "Available Day" field for lore entries. This controls when an entry becomes active. Set it to prevent deep lore from surfacing before the player has invested enough time. In the JSON, this field may appear as `availableFromDay` on individual entries. If not present, the entry is active from day 1.

---

## Characters Tab

One object per character in the `characters` array.

| JSON field | UI label | Notes |
|---|---|---|
| `name` | First Name | — |
| `lastName` | Last Name | — |
| `role` | Role | One or two phrases |
| `baseProfile` | Character Card | Main character description — see below |
| `appearance` | Appearance | Physical description for image generation and LLM reference |
| `type` | Type | `"main"` or `"side"` |
| `availableFromDay` | Available Day | Earliest possible introduction day |
| `spriteSets` | Sprite Sets | Visual states for artwork |
| `startingInfluence` | Starting Influence | Integer, may be negative; omit for the platform default ("Auto" in the UI) |
| `color` | Name Color | Tailwind CSS text-color class string, e.g. `"text-pink-400"` |

The character note also carries a `sex` field. It is internal worldbuilder schema, never written to `world.json`: the export reads it to keep pronouns accurate in `appearance`, per-set `appearance` and the card's Future Storylines.

### `baseProfile` — structure

The `baseProfile` field is a single text block: unstructured flowing prose. No JSON sub-fields, no rigid internal format. The card body (personality, background, behavior, relationships, influence thresholds) is written as connected prose followed by a **Future Storylines** section. No internal headers in the card body.

See `worldbuilder-ainime-export/card-assembly.md` for the full assembly guide, register rules, and token targets.

### `appearance` — structure

Physical description for image generation and LLM reference. Cover: species/type and sex (if relevant), age presentation and body type, notable features, clothing style. Should be consistent with `baseProfile`.

### `spriteSets` schema

```json
[
  {
    "name": "default",
    "description": "Casual, at rest — the character's natural state",
    "expressions": {
      "neutral": "image generation prompt for this state"
    },
    "appearance": "Physical-features preamble, then this set's outfit.",
    "baseImage": "asset://sandboxWorldAssets/<uuid>",
    "basePrompt": "image generation prompt for this set's base image"
  }
]
```

Each sprite set is a named visual state (Casual, Working, Formal, etc.). The `description` guides art generation; the `expressions` object maps each expression name to an image — either a generation prompt (at skill output time) or an `asset://` URL (in the final `.sbworld`). Expression keys must be drawn from the world's `availableExpressions` list.

| Sprite set field | Type | Purpose |
|---|---|---|
| `appearance` | string | This set's look: the character's invariant physical-features preamble, then the set's outfit |
| `baseImage` | string (`asset://` URL) | The set's reference image, normally the same asset as `expressions.neutral` |
| `basePrompt` | string | Generation prompt for the set's base image when no `baseImage` is bundled (not yet seen in an inspected export; purpose unverified) |

---

## Expression Configuration

| JSON field | Type | Source |
|---|---|---|
| `availableExpressions` | string[ ] | World configuration |

The `availableExpressions` array defines the palette of emotional expressions available across all characters in the world. Each entry is a snake_case expression name (e.g., `"happy"`, `"eyes_closed"`). Every key in a character's `spriteSets[].expressions` object must appear in this list.

The platform's default set of 26 expressions:

```
amused, angry, annoyed, beaming, blushing, comedic_shock, confident,
crying, embarrassed, emotional, emotional_shock, flirty, happy,
intimate, laughing, nervous, neutral, sad, shy, sleepy_or_tired,
smiling, stoic, surprised, upset, wary, worried_or_concerned
```

Worlds may define a custom set with more or fewer entries. Define `availableExpressions` early when building a world from scratch — it determines how many expression variants each character sprite set needs and how many expression images must be generated per sprite set.

### Expression Tiers

For monolithic AI-generated sprites (one image per expression), three tiers balance cost and coverage: **Essential**, **Standard** (the recommended default) and **Expansive**, each a strict superset of the one before. The names carry no counts, so a change in membership never renames a tier.

This document does not define the tiers. Membership, counts, narrative roles and the cost table live in the Image Gen expression standard, the shared Ainime reference for sprite expressions: `Projects/Ainime/Image Gen/Expression standard.md` in the Anima vault. Until that note is written, the same standard is at `Projects/Ainime/Fields of Mistria/repo/Fields-of-Mistria/Sprite Expression Workflow/Expression Standard.md`.

---

## Locations Tab

The Locations tab manages image pools — sets of location images by time of day. It is NOT the source of narrative location descriptions.

| JSON path | Structure |
|---|---|
| `locations` | `{[timeSegment]: LocationImage[]}` |

```json
{
  "Morning": [{"name": "location_slug_morning", "url": "asset://sandboxWorldAssets/<uuid>", "prompt": "image gen prompt"}],
  "Afternoon": [...],
  "Evening": [...]
}
```

Each entry has three fields:

- **`name`** — Snake-case identifier. Convention for time-variant locations: `{location_slug}_{time_segment}` (e.g., `blacksmith_forge_morning`).
- **`url`** — Either an asset reference (`asset://sandboxWorldAssets/<uuid>`) for a bundled image registered in `manifest.json` with `kind: "location"`, or empty string `""` when no image is provided (the platform can generate one from `prompt`).
- **`prompt`** — Optional. A text description of the location used by the platform's built-in AI image generator. Omit when a bundled image is provided. Prompts describe the empty scene only — no people, characters, or figures unless a specific location is deliberately designed to include them. Each prompt is self-contained: describe the location on its own terms without referencing other locations (no "near the blacksmith" or "across from the inn").

**Narrative location descriptions** belong in `loreEntries`, not the `locations` object. Write a lorebook entry for each major location covering what the place looks like, who uses it, what it means, and one vivid specific detail. The `locations` object is for art assets.

---

## Art Style Tab

The Art Style tab configures image generation prompts for backgrounds and character sprites.

| JSON path | What it contains |
|---|---|
| `artStyle.background.style_prefix` | Prefix prepended to all background generation prompts |
| `artStyle.background.style_suffix` | Suffix appended to all background prompts |
| `artStyle.background.time_contexts` | Per-segment lighting descriptions added to prompts |
| `artStyle.background.negative_prompt` | Negative prompt for backgrounds |
| `artStyle.sprite.style_prefix` | Prefix for all sprite generation prompts |
| `artStyle.sprite.style_suffix` | Suffix for all sprite prompts |
| `artStyle.sprite.negative_prompt` | Negative prompt for sprites |
| `artStyle.sprite.clothingRules` | String array of clothing directives for sprite generation, one rule per entry |

The Foundation phase produces a **plain-language art style reference** describing the desired visual style, color palette, and reference works. This is translated into prompt-engineering format during export.

Do not attempt to write `style_prefix` / `style_suffix` content during the Foundation or Wide phases — these are prompt-engineering outputs produced by `worldbuilder-ainime-export`.

---

## Moods Tab

The `moods` array configures the world's music. Each entry is either a link to an existing audio file (`url` populated, `prompt` empty) or a directive for AI music generation (`prompt` populated, `url` empty).

| JSON field path | Type | Source content skill |
|---|---|---|
| `moods` | Mood[ ] | `worldbuilder-world-foundation` → `foundation.md` (musical reference) + `worldbuilder-character` (character themes) |

### Mood entry schema

```json
{
  "id": "uuid",
  "name": "spring_wake_up_little_seed",
  "description": "Outdoor daytime during Spring. Fresh, optimistic, the season of new growth.",
  "prompt": "",
  "url": "https://example.com/track.ogg",
  "updatedAt": 1787103438769,
  "category": "standard"
}
```

**`id`** — UUID for user-created moods. System moods use `system:{slot_name}` (see below).

**`slot`** — Present only on system moods. Identifies the fixed playback slot.

**`name`** — Snake-case identifier. Convention: `{context}_{descriptive_name}` — e.g. `spring_tenacious_sprout`, `mines_dig_deeper`, `location_bathhouse`, `reina_theme`.

**`description`** — When and where this mood plays, written for the AI music selector. Describes scene context (season, location, activity, weather, emotional state) so the engine can match music to the current game state. This is the most important field for AI-generated music — it is the selection signal.

**`prompt`** — Text prompt for AI music generation. Empty string when `url` provides a direct audio link instead.

**`url`** — Direct link to an audio file (hosted URL or `asset://` reference within the `.sbworld` archive). Empty when `prompt` drives AI generation.

**`updatedAt`** — Millisecond timestamp of last edit.

**`category`** — One of `"standard"`, `"ambient"`, or `"character_theme"`. Absent on system moods.

### System moods

Three fixed-slot entries the engine requires. Use `system:{slot}` as the `id` and include a `slot` field (no `category`):

| slot | Purpose |
|------|---------|
| `main_menu` | Title screen, new-game generation, and endgame / credits |
| `segment_transition` | Brief musical bridge between day segments (Morning → Afternoon, etc.) |
| `day_transition` | End-of-day / going to sleep |

### Standard moods (`category: "standard"`)

General-purpose tracks the engine selects based on scene context. Typical coverage for a full world:

- **Seasonal outdoor** — 2–4 tracks per season for daytime outdoor scenes (farm work, exploration, town activity)
- **Weather** — Rain, storms, overcast, snowfall (cross-season or season-specific)
- **Mines / dungeon** — Per-level-range tracks, rest floors, boss or seal encounters, ambient underground
- **Events** — Festival days, weekly markets, special occasions
- **Story beats** — Revelation moments, milestone achievements, tonal shifts
- **Home** — Morning wake-up, evening wind-down inside the player's house

### Ambient moods (`category: "ambient"`)

Location-specific atmospheric tracks that play when the player enters a named location:

- Shops and services (blacksmith, carpenter, clinic, general store)
- Social spaces (inn daytime vs. evening)
- Special locations (bathhouse, deep woods, underground water features)

Ambient moods layer over or replace standard moods based on location context.

### Character theme moods (`category: "character_theme"`)

Per-character leitmotifs. One entry per major character, with two additional fields:

```json
{
  "id": "uuid",
  "name": "reina_theme",
  "description": "Warm kitchen energy, competitive drive, care expressed through food.",
  "prompt": "",
  "url": "...",
  "updatedAt": 1787103438769,
  "category": "character_theme",
  "characterRef": "character-uuid",
  "referenceImage": "asset://sandboxWorldAssets/uuid"
}
```

**`characterRef`** — UUID of the character entry in the `characters` array.

**`referenceImage`** — Asset URL for the character's reference image, used by the AI music generator for visual-to-audio synthesis.

### Music sourcing

Two paths for populating a mood's audio:

1. **Existing audio** — Set `url` to a hosted link or an `asset://` reference to a file bundled in the `.sbworld` archive. Leave `prompt` as `""`.
2. **AI generation** — Write a `prompt` describing the desired music (genre, tempo, instrumentation, mood, energy). Leave `url` empty. The platform generates audio from the prompt and the mood's `description`.

The Foundation phase produces a **plain-language musical theme reference** (genre, tempo, instrumentation, mood register) that informs mood descriptions across all categories.

### Music style (`musicStyle`)

Global style modifiers for AI-generated music, analogous to `artStyle` for images:

```json
{
  "musicStyle": {
    "prefix": "",
    "suffix": ""
  }
}
```

**`prefix`** — Prepended to every AI music generation prompt. Use for global genre, instrumentation, or production style directions.

**`suffix`** — Appended to every AI music generation prompt. Use for consistent quality tags or stylistic constraints.

---

## Theme Tab

UI color theme. Not part of the worldbuilding workflow. Configure after content is complete.

| JSON field | Content |
|---|---|
| `uiTheme.primaryColor` | Primary accent color |
| `uiTheme.secondaryColor` | Secondary color |
| `uiTheme.textboxGradient1/2/3` | Dialog box gradient colors |

---

## Prompts Tab (formerly Custom Prompts)

Advanced overrides for specific engine prompts, organized into switchable prompt sets. Not part of the standard worldbuilding workflow.

| JSON field | Content |
|---|---|
| `customPrompts` | Object with keys: `dm` (director), `am` (arc manager), `na` (narrator), `td` (translator), and others; holds persona sub-section and World Builder generation-template overrides from a user-created prompt set; empty while the Default prompt set is active |
| `activePromptSet` | Reference to the active prompt set, e.g. `{ "kind": "default" }` |

---

## Phase → Field Mapping

All JSON fields are produced by `worldbuilder-ainime-export` reading from Wide-phase notes. This table shows which notes are the source for each field group.

### Wide-phase sources → ainime export input

```
project/foundation.md  → settingSummary, genre, inspirations, tonalInspirations,
                         keyTropesAndThemes, communityDescription, introText,
                         initialStoryArc, calendarConfig.eraReminder,
                         calendarConfig.seasons/daysPerSeason/daysOfWeek/daySegments
                         [art style reference → artStyle.* prompts]

notes/ (concept)       → loreEntries[]

notes/ (event)         → calendarConfig.weatherPools, storyTriggers[] (events),
                         eventCalendarSummary

project/direction.md   → arcManagerGuidance
notes/ (story, intention scope)
                       → storyTriggers[] (story events, where trigger day exists)

notes/ (character)     → characters[].name, lastName, type, role, availableFromDay,
                         baseProfile, appearance, spriteSets[] (incl. per-set
                         appearance, baseImage, basePrompt); sex is read for
                         pronouns, never exported
                         [Body sections → artStyle.sprite.clothingRules]

project/foundation.md (music ref)
                       → moods[] (system, standard, ambient mood entries),
                         musicStyle.prefix, musicStyle.suffix
notes/ (character)     → moods[] (character_theme entries, linked via characterRef)
project/foundation.md (expressions)
                       → availableExpressions[]
```

### Export skill deliverables

The `worldbuilder-ainime-export` skill produces formatted output ready for entry into the ainime platform. Character cards are the most complex output; see `card-assembly.md` in that skill's directory.

---

## Fields We Do Not Write

These fields are auto-generated or configured by the platform — do not produce content for them:

- `worldId` — UUID assigned by the platform
- `generateSideCharacterOnNewGame` — builder's platform toggle; preserved on re-export, never derived from notes (see the Adventure tab)
- `characters[].image` — generated artwork
- `activePromptSet` — prompt-set reference; prompt sets are builder customization
- `locations[].url` — when platform-generated; bundled location images use `asset://sandboxWorldAssets/<uuid>` and are export-produced
- `artStyle.sprite.same_character_consistency` — platform setting
- `artStyle.sprite.use_tag_style_prompts` — platform setting
- `uiTheme.*` — UI configuration, set after content
- `customPrompts.*` — advanced overrides, not standard workflow
- `mainMenuBackground` / `mainMenuBackgroundThumbnail` — generated images
- `author`, `tags` — publishing metadata
