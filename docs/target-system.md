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

**`communityDescription`** — A one- or two-sentence blurb for the community world list, written for players browsing worlds. With `tags` and `author` it makes up the world's listing. It is not in-game context about the setting's social life: that belongs in `settingSummary`.

**`introText`** — Pre-game text the player reads before creating their character. Sets expectations for tone and situation. The player creates only name and appearance — the intro should reflect that. Typically 2–4 short paragraphs.

---

## Adventure Tab

| JSON field | UI label | Type | Source content skill |
|---|---|---|---|
| `initialStoryArc` | Opening Story Arc | string | `worldbuilder-world-foundation` → `foundation.md` |
| `arcManagerGuidance` | Ongoing Story Direction | string | `worldbuilder-story` → `project/direction.md` |
| `storyTriggers` | Story Triggers (Events) | StoryTrigger[ ] | `worldbuilder-story` (intention notes) + `worldbuilder-concept` (recurring event notes) → `notes/` |
| `generateSideCharacterOnNewGame` | Invent a side character at New Game | boolean | Builder choice in the platform; no note source |
| `randomizedStart` | Randomize the opening arc | object | Builder choice in the platform; no note source |
| `romancePair` | Random NPC romance pair | object | Builder choice in the platform; no note source |
| `quickSlots` | Quick slots | QuickSlot[ ] | Built in the platform from a played save; no note source |
| `choices` | Choices | object | Builder choice in the platform; no note source |

### Field notes

**`initialStoryArc`** — A brief, evocative description of the situation when the player arrives. Not a scripted sequence — it sets the stage. Drafted in the Foundation phase and refined after the cast exists. See `worldbuilder-story` for content guidance.

**`arcManagerGuidance`** — The engine's standing creative brief throughout the game. The primary guard against escalation, flattening, and inappropriate pacing. Covers: author framing, romance pacing, dark themes, hidden layer handling, seasonal tone, pacing. This is one of the most important fields; a weak brief here degrades every scene the engine generates. See `worldbuilder-story` for the full template.

**`storyTriggers`** — Named events with a day trigger and a narrative injection prompt. When the trigger day is reached, or the event repeats on its cadence, the `promptInjection` text is injected into the engine's context. Players see upcoming events on their in-game calendar: the event's `name` and its `playerBlurb`. The `promptInjection` stays private, so a public event can still hold a surprise.

StoryTrigger schema:
```json
{
  "id": "uuid",
  "name": "Event name",
  "kind": "world",
  "triggerOnDay": 8,
  "promptInjection": "Narrative direction text injected on this day.",
  "playerBlurb": "One or two sentences the player reads on the in-game calendar.",
  "recurrence": "once",
  "hiddenFromPlayer": false
}
```

| StoryTrigger field | Type | Purpose |
|---|---|---|
| `promptInjection` | string | Direction for the story AI: what happens, how to stage it, the reveal it builds to |
| `playerBlurb` | string | Text for the player, read on the in-game calendar days ahead. The platform's own event writer requires it on every event, and the Calendar tab offers "Write missing player text" for events without it |
| `recurrence` | string | `once`, `yearly`, `seasonal`, `weekly` or `interval`, counted from `triggerOnDay` |
| `recurrenceIntervalDays` | integer | The cadence in days when `recurrence` is `interval`; without it the platform falls back to a fortnight |
| `recurring` | boolean | The older form of `recurrence`. The platform reads it only when `recurrence` is absent: `true` means `yearly`, `false` or absent means `once` |
| `hiddenFromPlayer` | boolean, optional | Hides the event from the player's calendar entirely |

Prefer a named `recurrence` mode to `interval` when one fits: a named mode stays correct if the calendar is resized later.

A character event returned to the calendar also carries a `justification`:

```json
{
  "id": "uuid",
  "name": "The harbour introduction",
  "kind": "character",
  "justification": "Introduces the harbour guild through this character on a fixed day, which paces the opening days.",
  "triggerOnDay": 3,
  "promptInjection": "Narrative direction text injected on this day.",
  "playerBlurb": "Player-facing calendar text.",
  "recurrence": "once",
  "hiddenFromPlayer": false
}
```

`kind` and `justification` are audit-only keys (standard 2 in `skills/worldbuilder-ainime-export/standards.md`). They live in the tracked `world.json`, and packaging removes both from the shipped file.

`hiddenFromPlayer` (boolean, optional) hides the event from the player's calendar entirely. That the hidden event still fires is inferred from how worlds use it, not confirmed against the platform. Standard 2 in `skills/worldbuilder-ainime-export/standards.md` says which events may use it.

Set `recurrence: "yearly"` for annual events (festivals, observances), `"weekly"` for a market day, `"seasonal"` for an event that returns every season, and `"once"` for a one-time event. A weekly or interval event is one entry, not one entry per occurrence.

**New Game options** — The Adventure tab's New Game options are saved with the world and travel in the `.sbworld`. Each is a builder choice set in the platform: the export preserves the existing value and never derives it from notes.

- **`generateSideCharacterOnNewGame`** (boolean) — "Invent a side character at New Game".
- **`randomizedStart`** (object) — "Randomize the opening arc": dice woven through `initialStoryArc`, which may rewrite it. Holds an NPC `pool`, `threatTypes` and `roles`, among other keys; the full shape is not documented here.
- **`romancePair`** (object) — "Random NPC romance pair": `enabled`, a `pool` and a list of `dynamics`.
- **`choices`** (object) — How many reply choices the AI writes at the end of every reply, with optional labelled, coloured choice slots. The default is four unlabelled choices "in different directions".
- **`quickSlots`** (array) — Quick starts: played saves bundled in the world, which the player picks on the new-game screen instead of starting a new story. Each slot holds an `id`, `title`, `description`, `adventureArc`, the player `persona` (`name`, `backstory`, `appearancePrompt`, `nameColor`), `sourcePlayerName`, the `day` and `segment` the save stands at, any characters the story invented (`emergent`, `alsoEmergent`), and `saveRef`, an `asset://` reference to the save file bundled in the archive.

"Ignore Opening Story Arc" sits on the same tab; no world key for it was found.

---

## Calendar Tab

| JSON field / path | UI label | Type | Source content skill |
|---|---|---|---|
| `calendarConfig.seasons` | Seasons | string[ ] | `worldbuilder-world-foundation` → `project/foundation.md` |
| `calendarConfig.daysPerSeason` | Days per Season | number | `worldbuilder-world-foundation` → `project/foundation.md` |
| `calendarConfig.daysOfWeek` | Days of Week | string[ ] | `worldbuilder-world-foundation` → `project/foundation.md` |
| `calendarConfig.daySegments` | Day Segments | string[ ] | `worldbuilder-world-foundation` → `project/foundation.md` |
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
    "<segment 1>": ["Light fog lifting...", "Crisp clean air..."],
    "<segment 2>": ["..."],
    "<segment 3>": ["..."]
  }
}
```

**`storyTriggers`** — The calendar events field. Repeating events and one-time events are both stored here, told apart by `recurrence`. See the Adventure tab section above for the schema.

**`eventCalendarSummary`** — Narrative overview of the full event calendar for LLM reference. A prose summary of the festival calendar and its emotional rhythms — written for the AI, not the player. Produced after all events are written.

**`calendarConfig.seasons`, `daysPerSeason`, `daysOfWeek`, `daySegments`** — Structural configuration. Season length and the day segments follow standard 1 in `skills/worldbuilder-ainime-export/standards.md`. Seasons and day names follow the world's own cycle.

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

**`availableFromDay`** — Integer, optional. Shown as "Day" in the UI: the entry is held back until that in-game day. Absent means active from the start. Use it to keep deep lore from surfacing before the player has invested enough time.

**`title`** — String, optional. A display name for the entry in the World Builder's list.

**`alwaysOn`** — Boolean, optional. When `true` the entry is sent with every scene, even with no keyword match. It sits in the cached part of the prompt, so use it sparingly.

**`dice`** — Object, optional. Fires the entry on a random roll instead of a keyword: `{ "dieMin": 1, "dieMax": 20, "hitMin": 1, "hitMax": 1 }` fires it on about 1 turn in 20. A roll can also carry several `outcomes`, of which one roll picks at most one text; the outcome shape is not documented here. An entry carries either `alwaysOn` or `dice`, not both. The UI's "Show on hit" lists a hit with the other lore that fired; the story receives the entry either way.

---

## Characters Tab

One object per character in the `characters` array.

| JSON field | UI label | Notes |
|---|---|---|
| `name` | First Name | — |
| `lastName` | Last Name | — |
| `role` | Role | One or two phrases |
| `baseProfile` | Character Card | The character's full description — see below |
| `appearance` | Appearance | Physical description for image generation and LLM reference |
| `type` | Type | `"main"` or `"side"`; see below |
| `futureStorySeeds` | Future story ideas | Possibilities for later arcs, read by the Arc Manager only; see below |
| `availableFromDay` | Available Day | Earliest possible introduction day |
| `spriteSets` | Sprite Sets | Visual states for artwork |
| `startingInfluence` | Starting Influence | Integer, may be negative; omit for the platform default ("Auto" in the UI) |
| `color` | Name Color | Tailwind CSS text-color class string, e.g. `"text-<hue>-<shade>"` |

**`type`** — Mains are optional: a world with only side characters can start. Side characters are written at the same depth as mains. The one difference is that a side character gets no personal story arc until play promotes them: the characters the player spends time with become mains as the game goes on. A main whose `availableFromDay` arrives gets their arc, traits and likes that night.

**`futureStorySeeds`** — String. Labelled "Future story ideas" in the character editor: possibilities the Arc Manager can develop into later arcs, not established facts or instructions for a scene. The Dungeon Master, the AI that plays scenes, does not receive this field. History, motives, relationships and secrets stay in `baseProfile`. The editor's "Find future story notes in profile" button finds a clearly labelled future-story section in `baseProfile` and offers to move it here. Our cards still ship Future Storylines inside `baseProfile` (see below); whether to move them to this field is an open decision.

The character note also carries a `sex` field. It is internal worldbuilder schema, never written to `world.json`: the export reads it to keep pronouns accurate in `appearance`, per-set `appearance` and the card's Future Storylines.

### `baseProfile` — structure

The `baseProfile` field is a single text block with no JSON sub-fields. The character note's sections ship into it in order: an unheaded preamble, then Background, Body, Soul, Relationships, Voice / Dialogue and Future Storylines. Each section after the preamble opens with a plain-text heading line: the heading words on a line of their own, with no markdown heading marks and no `---` dividers. The **Future Storylines** section is required for every character.

See `worldbuilder-ainime-export/card-assembly.md` for the full assembly guide, register rules, and token targets.

### `appearance` — structure

Physical description for image generation and LLM reference. Cover: species/type and sex (if relevant), apparent age and body type, notable features, clothing style. Should be consistent with `baseProfile`.

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
| `framing` | string | The sprite type the set is drawn in: `"bust"` (chest up), `"thigh"` (thigh up), `"ankle"` (head to ankles) or `"full"` (full body). A set without it is a classic sprite from before sprite types existed |
| `versionOf` | string | On a version set only: the `name` of the set (the look) this one redraws in another `framing`. A version set is named `<look>--<framing>`, for example `default--full` |
| `cutouts` | object | See-through copies of the set's pictures: `baseImage`, `expressions` (expression name to `asset://` URL) and the `baseSource` and `sources` they were cut from |
| `expressionPrompts` | object | Expression name to the prompt last used to draw it, kept on version sets |

### Sprite types and versions

A character's look (Casual, Working, a uniform) is one sprite set. The platform can hold the same look in several sprite types: each extra type is a version set with `versionOf` pointing at the look and its own `framing`, outfit `appearance`, `baseImage` and `expressions`. In the Visual novel layout the stage shows each look in the sprite type the world picks under `stage.spriteFraming`, or the nearest version the look has. The Portraits layout always shows chest up; when a look has only a longer sprite, its upper part is used.

A cut-out is a see-through copy of a picture, so the scene shows around the character. A set drawn with a transparent background is already a cut-out. A set drawn on a backdrop can gain cut-outs later, in the `cutouts` object, for the whole cast, one character or one set. Image models that cannot draw transparency (Gemini, for example) paint one flat key colour, which the platform removes; NovelAI and OpenAI GPT Image models draw the transparency themselves.

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

This document does not define the tiers. Membership, counts, narrative roles and the cost table are in `worldbuilder-ainime-export/expression-standard.md`, which is also the one statement of the sprite background rule.

---

## Locations Tab

The Locations tab manages image pools — sets of location images by time of day. It is NOT the source of narrative location descriptions.

| JSON path | Structure |
|---|---|
| `locations` | `{[timeSegment]: LocationImage[]}` |

```json
{
  "<segment 1>": [{"name": "location_slug_<segment 1>", "url": "asset://sandboxWorldAssets/<uuid>", "prompt": "image gen prompt"}],
  "<segment 2>": [...],
  "<segment 3>": [...]
}
```

Each entry has three fields:

- **`name`** — Snake-case identifier, and the only thing the story sees when it picks a background, so it says what the place is. Order: the place, then the time of day, then any version that changes its look: `{location_slug}_{time_segment}` or `{location_slug}_{time_segment}_{version}` (e.g., `cafe_evening`, `cafe_night_rain`). The World Builder's Places view groups names by the part before the time of day; a name with the version before the time of day shows as a separate place.
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
| `artStyle.vnScene` | Object for visual-novel scenes: `enabled` (boolean) and the strings `style_prefix`, `style_suffix`, `negative_prompt`. Standard 10 in `skills/worldbuilder-ainime-export/standards.md` says how to write it |
| `artStyle.{background,sprite,vnScene}.style_reference` | A Style Reference Image for that kind of picture, sent with every picture of that kind the world draws, in the World Builder and in play. The image model is told to copy only how it is drawn |
| `artStyle.{background,sprite,vnScene}.style_reference_enabled` | Boolean switch for the matching reference image, so it can stop being sent without being removed |

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
| `segment_transition` | Brief musical bridge between day segments (one declared segment to the next) |
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

## UI Tab (formerly Theme)

How the game screen looks: the sprite stage, the text box, colours, typography and the main menu picture.

### Sprite stage (`stage`)

The platform shows characters in one of two layouts. **Portraits** puts a chest-up picture of each character above the text box, up to six in two rows. **Visual novel** stands the characters in front of the background, with a one-line text box; cut-outs look best there, and other pictures show as cards. Players can switch layouts in Options, so a world sets both.

| JSON path | UI label | Content |
|---|---|---|
| `stage.mode` | Layout | `"grid"` (Portraits) or `"stage"` (Visual novel): the layout the world starts in. Absent means Portraits |
| `stage.spriteFraming` | Sprite type | `"bust"`, `"thigh"`, `"ankle"` or `"full"`: the sprite type Visual novel shows on desktop. Each look shows that type, or the nearest version it has. New sprites start in this type |
| `stage.phone.*` | Sprite type, phone, and the phone column of each setting below | The phone's own values; phone follows desktop until it has its own |
| `stage.vnReferenceFraming` | VN scene references | The sprite type sent as the character reference when a VN scene picture is drawn. A VN model profile can override it |
| `stage.spriteShape` | Shape | `"square"` (1:1, chest up), `"portrait"` (2:3, thigh up) or `"tall"` (9:16, full body): the shape new sprites are drawn in |
| `stage.cutoutSprites` | Background | `true` for cut-outs (see-through around the character), `false` for a painted backdrop. Absent means on in Visual novel and off in Portraits |
| `stage.keyColor` | Colour to remove | The flat colour a model without transparency paints behind a sprite, which the platform then removes. Automatic picks magenta for a character whose appearance mentions green |
| `stage.maxVisible` | On screen at once | Stage capacity per device (`desktop`, `mobile`); the remaining characters show as small pictures in a corner |
| `stage.floor`, `stage.floorOffset` | Where they stand, Floor position | Feet on `"screen"` (the screen bottom, sprites continue behind the text box) or on `"textBox"`, shifted by a fraction of the play area |
| `stage.spriteHeight` | Base sprite height | One scale for every sprite |
| `stage.slots`, `stage.phoneSlots` | Places | Horizontal positions in percent, one list per number of characters on stage |
| `stage.speakerPortrait` | Speaker portrait | Shows the speaker's chest-up picture beside the text box. Off by default |
| `stage.focus` | Darken everyone but the speaker | `"dim"` (the default) or `"none"` |
| `stage.characters.<name>`, `stage.phone.characters.<name>` | Character adjustments | One character's own `scale` (60% to 140%), vertical offset or facing, per device |

The World Builder's "Convert the cast" redraws every sprite set as a taller sprite type from the pictures the cast has, as version sets (see the Characters tab); the existing pictures stay. The tab also stores the world's default text box size (desktop height and width, phone height), which players can override.

### Colours, typography and menu picture

| JSON field | Content |
|---|---|
| `uiTheme.primaryColor` | Primary accent color |
| `uiTheme.secondaryColor` | Secondary color |
| `uiTheme.textboxGradient1/2/3` | Dialog box gradient colors |
| `uiTheme.fontFamily`, `fontGoogleUrl`, `fontSize`, `fontLineHeight`, `fontLetterSpacing`, `overridePlayerFont` | Typography: a font from the list or any Google Font, and whether the world's font overrides the player's own |
| `mainMenuBackground`, `mainMenuBackgroundThumbnail` | The world's main menu picture |

The colour presets (33, in six groups) and a custom palette both write the `uiTheme` keys above.

---

## Prompts Tab (formerly Custom Prompts)

Advanced overrides for specific engine prompts, organized into switchable prompt sets. Not part of the standard worldbuilding workflow.

| JSON field | Content |
|---|---|
| `customPrompts` | Object with keys: `dm` (director), `am` (arc manager), `na` (narrator), `td` (translator), and others; holds persona sub-section and World Builder generation-template overrides from a user-created prompt set; empty while the Default prompt set is active |
| `activePromptSet` | Reference to the active prompt set, e.g. `{ "kind": "default" }` |
| `worldPromptSet` | A prompt set stored in the world, which travels with its export (marked "world" in the Prompts tab) |

Each prompt set also holds its own Banned Words list, shared by every AI writer in that set.

---

## Builder steering fields

The World Builder's AI builders save the instructions typed into them with the world. They steer the builders, and the export does not write them.

| JSON field | Builder |
|---|---|
| `locationPreferences` | AI Location Builder: which places to write |
| `weatherInstructions` | AI Location Builder: weather and atmosphere for location prompts |
| `moodPreferences` | Music builder |
| `loreBuilderPreferences`, `loreBuilderTopics` | Lorebook Builder |

---

## Phase → Field Mapping

All JSON fields are produced by `worldbuilder-ainime-export` reading from Wide-phase notes. This table shows which notes are the source for each field group.

### Wide-phase sources → ainime export input

All entity notes (character, location, faction, event, concept, story) sit in the project's flat `notes/` folder, told apart by their `type` property. The two named documents are `project/foundation.md` and `project/direction.md`.

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
standard 13 in standards.md
                       → stage.mode, stage.spriteFraming, stage.spriteShape
```

### Export skill deliverables

The `worldbuilder-ainime-export` skill produces formatted output ready for entry into the ainime platform. Character cards are the most complex output; see `card-assembly.md` in that skill's directory.

---

## Fields We Do Not Write

These fields are auto-generated or configured by the platform — do not produce content for them:

- `worldId` — UUID assigned by the platform
- `generateSideCharacterOnNewGame`, `randomizedStart`, `romancePair`, `choices`, `quickSlots` — New Game options set in the platform; preserved on re-export, never derived from notes (see the Adventure tab)
- `characters[].futureStorySeeds` — not written while our cards carry Future Storylines inside `baseProfile` (see the Characters tab)
- `spriteSets[].cutouts`, `expressionPrompts` and platform-made version sets — produced by the platform's own sprite tools; preserved on re-export
- `stage.*` other than the three keys standard 13 sets — stage tuning done in the platform's preview; preserved on re-export
- `artStyle.*.style_reference`, `style_reference_enabled` — reference images imported in the platform
- `locationPreferences`, `weatherInstructions`, `moodPreferences`, `loreBuilderPreferences`, `loreBuilderTopics` — builder steering (see Builder steering fields)
- `worldPromptSet` — prompt-set customization
- `characters[].image` — generated artwork
- `activePromptSet` — prompt-set reference; prompt sets are builder customization
- `locations.<segment>[].url` — when platform-generated; bundled location images use `asset://sandboxWorldAssets/<uuid>` and are export-produced
- `artStyle.sprite.same_character_consistency` — platform setting
- `artStyle.sprite.use_tag_style_prompts` — platform setting
- `uiTheme.*` — UI configuration, set after content
- `customPrompts.*` — advanced overrides, not standard workflow
- `mainMenuBackground` / `mainMenuBackgroundThumbnail` — generated images
- `author`, `tags` — publishing metadata
