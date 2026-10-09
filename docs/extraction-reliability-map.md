# Extraction Reliability Map

Reference classifying every ainime export field by extraction method.
Maintained alongside the export skill. See spec:
[Export-Standards Review](../.claude/specs/2026-08-10-export-standards-review-keywords-field-and-extraction-reliability-map.md).

## Categories

- **Structural** — deterministic extraction from a known section,
  frontmatter field, or filename. No agent interpretation.
- **Derived** — agent interpretation, constrained by note section
  structure.
- **Constructed** — no source in notes. Configured or generated at
  export time (includes export-time defaults).

## Classification rules

- Every field the export workflow writes appears exactly once.
- Compound fields (storyTriggers[], loreEntries[], characters[],
  calendarConfig.weatherPools, artStyle.*, spriteSets[]) are
  classified at leaf-field granularity — each child gets its own row.
- Categories are mutually exclusive. When a field has a primary path
  and a fallback (e.g., keywords: explicit field or derived from
  body), classify by the primary path and note the fallback in the
  Source column.
- Fields appearing in multiple export sections (e.g., storyTriggers[]
  from both event and intention story notes) are placed in one table
  only — use the primary export section.
- Platform-managed fields (IDs, generated images, UI theme, music,
  custom prompts) are out of scope.

## Setting fields

| Field | Category | Source |
|-------|----------|--------|
| `settingSummary` | Structural | `project/foundation.md` — Setting Summary section (verbatim) |
| `genre` | Structural | `project/foundation.md` — Genre and Tone section (verbatim) |
| `inspirations` | Structural | `project/foundation.md` — Inspirations section (one entry per line item) |
| `tonalInspirations` | Structural | `project/foundation.md` — Tonal Inspirations section (one entry per line item) |
| `keyTropesAndThemes` | Structural | `project/foundation.md` — Key Tropes and Themes section (one entry per line item) |
| `communityDescription` | Structural | `project/foundation.md` — Community section (verbatim) |
| `introText` | Structural | `project/foundation.md` — World Introduction section (verbatim) |

## Adventure fields

| Field | Category | Source |
|-------|----------|--------|
| `initialStoryArc` | Structural | `project/foundation.md` — Opening Situation section (verbatim) |
| `arcManagerGuidance` | Structural | `project/direction.md` (verbatim) |
| `storyTriggers[].id` | Constructed | Export-time generated UUID |
| `storyTriggers[].name` | Structural | Event or intention note title |
| `storyTriggers[].triggerOnDay` | Derived | Agent assigns absolute calendar day from timing language in event note's What Happens section or intention note trigger condition |
| `storyTriggers[].promptInjection` | Derived | Agent converts event note Scene Effects or intention note content into active engine direction |
| `storyTriggers[].recurring` | Derived | Agent determines from event note whether the event repeats annually; intention story triggers default to `false` |

## Calendar fields

| Field | Category | Source |
|-------|----------|--------|
| `calendarConfig.seasons` | Structural | `project/foundation.md` — calendar structure (default: Spring, Summer, Autumn, Winter) |
| `calendarConfig.daysPerSeason` | Structural | `project/foundation.md` — calendar structure (default: 28) |
| `calendarConfig.daysOfWeek` | Structural | `project/foundation.md` — calendar structure (default: standard day names) |
| `calendarConfig.daySegments` | Structural | `project/foundation.md` — calendar structure (default: Morning, Afternoon, Evening, Night) |
| `calendarConfig.eraReminder` | Structural | `project/foundation.md` — era description (one phrase) |
| `calendarConfig.weatherPools[season][segment][]` | Derived | Agent creates weather descriptions from world seasonal tone and `project/foundation.md` |
| `eventCalendarSummary` | Derived | Agent writes prose summary of the full event calendar |

## Lore fields

| Field | Category | Source |
|-------|----------|--------|
| `loreEntries[].id` | Constructed | Export-time generated (`lore_{timestamp}_{random}`) |
| `loreEntries[].keywords[]` | Structural | Concept note `keywords` frontmatter field (when present); fallback: Derived from `aliases` frontmatter + body terms |
| `loreEntries[].content` | Derived | Agent summarizes concept note into dense lore injection |
| `loreEntries[].enabled` | Constructed | Export-time default (`true`) |
| `loreEntries[].availableFromDay` | Structural | Concept note `layer` frontmatter (surface=1, mid=14, deep=56) |

## Character fields

| Field | Category | Source |
|-------|----------|--------|
| `characters[].name` | Structural | Character note filename |
| `characters[].lastName` | Structural | Character note filename |
| `characters[].type` | Structural | Cast plan in `project/plan.md` (Major="main", Supporting="side") |
| `characters[].role` | Derived | Agent derives from character note content (position, relationships, narrative function) |
| `characters[].baseProfile` | Derived | Agent assembles from character note Background, Body, Soul, Relationships, and Story Beats sections per `card-assembly.md`; Story Beats are transformed to possibility-style framing in the Future Storylines subsection |
| `characters[].appearance` | Structural | Character note Body preamble (verbatim or lightly condensed) |
| `characters[].availableFromDay` | Derived | Agent assigns based on narrative logic and introduction note timing |
| `characters[].spriteSets[].name` | Constructed | Export-time convention ("default" for casual, descriptive name for others) |
| `characters[].spriteSets[].description` | Derived | Agent writes art generation context from character note Appearance section |
| `characters[].spriteSets[].expressions.*` | Derived | Agent writes image generation prompts from character note Appearance section |

## Location fields

The `locations` object stores image pools (time-segment-keyed art
assets), not narrative content. It is not produced by the export
workflow. Narrative location descriptions are exported as
`loreEntries[]` (see Lore fields above).

## Art style fields

| Field | Category | Source |
|-------|----------|--------|
| `artStyle.background.style_prefix` | Derived | Agent translates `project/foundation.md` Art style reference into prompt-engineering format |
| `artStyle.background.style_suffix` | Derived | Agent translates `project/foundation.md` Art style reference into prompt-engineering format |
| `artStyle.background.time_contexts` | Derived | Agent creates per-segment lighting descriptions from `project/foundation.md` Art style reference |
| `artStyle.background.negative_prompt` | Derived | Agent creates negative prompt from `project/foundation.md` Art style reference |
| `artStyle.sprite.style_prefix` | Derived | Agent translates `project/foundation.md` Art style reference into prompt-engineering format |
| `artStyle.sprite.style_suffix` | Derived | Agent translates `project/foundation.md` Art style reference into prompt-engineering format |
| `artStyle.sprite.negative_prompt` | Derived | Agent creates negative prompt from `project/foundation.md` Art style reference |

## Multi-target readiness (non-gating)

Additional fields required by non-ainime targets, classified by the
same three categories:

### CCv3 (Character Card V3)

Fields below are V3-specific additions beyond what ainime character
and lore data already covers.

| Field | Category | Candidate source |
|-------|----------|-----------------|
| `personality` | Derived | Character note Foundation and Behavioral Descriptions sections (condensed separately from `description`/baseProfile) |
| `scenario` | Derived | `project/foundation.md` Setting Summary + Opening Situation (combined) |
| `first_mes` | Constructed | No current note source; candidate: character behavior + scenario context |
| `mes_example` | Derived | Character note Influence Thresholds (reformatted as example dialogue) |
| `system_prompt` | Derived | `project/direction.md` (requires target-specific transformation, not verbatim) |
| `post_history_instructions` | Constructed | No current note source |
| `alternate_greetings[]` | Derived | Character note Story Beats scenario prose, adapted to greeting format; trigger conditions degraded to narrative framing when not mechanically enforceable |
| `creator_notes` | Constructed | Export-time metadata |
| `creator` | Constructed | Export-time metadata |
| `character_version` | Constructed | Export-time metadata |
| `nickname` | Structural | Character note `aliases` frontmatter |
| `assets[]` | Structural | `spriteSets[]` mapped to V3 asset schema |
| `character_book` | Structural | `loreEntries[]` mapped to V3 lorebook schema |
| `group_only_greetings[]` | Constructed | No current note source (empty array) |
| `source[]` | Constructed | Export-time metadata |
| `creation_date` | Constructed | Export-time timestamp |
| `modification_date` | Constructed | Export-time timestamp |

### ST WorldInfo

Fields below are ST-specific additions beyond what ainime
`loreEntries[]` already covers.

| Field | Category | Candidate source |
|-------|----------|-----------------|
| `comment` (entry title) | Structural | Concept note title/filename |
| `keysecondary` | Derived | Concept note secondary terms or AND-compound keywords |
| `selectiveLogic` | Constructed | Export-time default (`and_any`) |
| `order` (priority) | Derived | Concept note `layer` frontmatter (surface/mid/deep mapped to priority tiers) |
| `position` | Constructed | Export-time default (`character`) |
| `depth` | Constructed | Export-time default (4) |
| `role` | Constructed | Export-time default (`system`) |
| `constant` | Constructed | Export-time default (`false`) |
| `scanDepth` | Constructed | Export-time default (use lorebook global) |
| `sticky` | Constructed | Export-time default (0) |
| `cooldown` | Constructed | Export-time default (0) |
| `delay` | Constructed | Export-time default (0) |
| `probability` | Constructed | Export-time default (100) |
| `group` | Derived | Concept note type/category frontmatter |
| `displayIndex` | Constructed | Export-time ordering |
| `excludeRecursion` | Constructed | Export-time default (`false`) |
| `preventRecursion` | Constructed | Export-time default (`false`) |
| `name` (lorebook-level) | Structural | Project name |
| `description` (lorebook-level) | Derived | `project/foundation.md` Setting Summary (condensed) |
| `scan_depth` (lorebook-level) | Constructed | Export-time default (100) |
| `token_budget` (lorebook-level) | Constructed | Export-time default |
| `recursive_scanning` (lorebook-level) | Constructed | Export-time default (`false`) |
