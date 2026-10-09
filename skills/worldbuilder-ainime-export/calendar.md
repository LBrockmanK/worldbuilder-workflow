# Calendar Reference

*Reference file for `worldbuilder-ainime-export`. Contains ainime-specific calendar structure, defaults, and design guidance. Read this before building the `calendarConfig`, weather pools, and event calendar sections of the export.*

---

## Default Calendar Structure

ainime uses a structured calendar that feeds seasonal context and day-segment pacing to the engine.

| Field | Default | Notes |
|---|---|---|
| Seasons | 4 (Spring, Summer, Autumn, Winter) | Adjust labels to the world's actual cycle |
| Days per season | 28 | Change only if world design requires it |
| Total year | 112 days | 4 × 28 |
| Day segments | Morning, Afternoon, Evening, Night | Injected as scene context transitions |

Set these in `calendarConfig.seasons`, `calendarConfig.daysPerSeason`, `calendarConfig.daySegments`.

---

## Weather Pools

`calendarConfig.weatherPools` is a nested JSON object: `season → day_segment → string array`.

Each string is a one-line weather description injected when that season and segment are active.

**Counts:** 10–16 entries per season/segment combination.

**Writing weather descriptions:**
- Concrete sensory details, not adjectives alone: "A heavy frost on the grass, melting by midmorning" not "Cold morning"
- Include narrative weight where appropriate — some entries purely atmospheric (clear autumn afternoon), some carrying energy (the first storm of winter, the heat that won't break)
- Vary the register: grounded mundane entries make the setting feel real; not every entry needs to be eventful

```json
{
  "Spring": {
    "Morning": ["Light fog lifting off the fields as the sun climbs...", "..."],
    "Afternoon": ["..."],
    "Evening": ["..."],
    "Night": ["..."]
  }
}
```

Derive weather descriptions from `project/foundation.md` and the world's setting. If the world has no strong seasonal character, use climate-appropriate defaults and vary them for narrative weight.

---

## Festival Calendar Layout

One major festival per season; 4–5 minor observances across the year. Total: 8–9 events.

**Major festivals** define a season's emotional peak. Each has a full atmospheric description and a specific calendar day.

**Minor observances** add texture without requiring full scenes — practical, personal, or commemorative moments.

Suggested layout (adapt to the world's actual calendar):

```
SEASON 1
  Day 8:  Major — communal, renewal, natural introduction opportunity
  Day 20: Minor — trade/market, outsiders in community

SEASON 2
  Day 7:  Minor — leisure, social, relaxed
  Day 21: Major — the night where the hidden layer is most present

SEASON 3
  Day 18: Major — harvest equivalent; abundance + underlying melancholy
  Day 26: Minor — day of remembrance; quiet, grief-adjacent

SEASON 4
  Day 10: Minor — practical market, before deep cold
  Day 22: Major — solstice equivalent; intimate, stories, things said in darkness
```

---

## Mapping Event Notes to storyTriggers

Event notes in `notes/` become `storyTriggers` entries; events whose timing repeats get `recurring: true` in the output.

**Finding the calendar day:** Read the opening of the event note's What Happens section — it states when the event takes place and how often ("early spring," "the darkest night of winter," "midway through harvest"). Assign an absolute calendar day that fits: `(season_number - 1) × days_per_season + day_within_season`. The event note does not specify an exact day — the exporter makes this decision based on the note content and the world's calendar structure.

**Constructing the entry:**
```json
{
  "id": "uuid",
  "name": "Spring Harvest Festival",
  "triggerOnDay": 8,
  "promptInjection": "...",
  "recurring": true
}
```

**Writing `promptInjection`:** Convert the event note's Scene Effects into active direction to the story engine — not a neutral description, but an instruction for how the engine should behave today:

> ❌ "Today is the Spring Harvest Festival. People gather at the village center."
> ✅ "The Spring Harvest Festival transforms every interaction today. Characters are expansive, the usual social distances relax, and introductions that might otherwise take weeks happen naturally. The player should feel the community as a whole for the first time."

**One-time narrative events** from intention story notes that have a concrete calendar day also become `storyTriggers` entries with `recurring: false`.

---

## Scene Structure and Day Segment Pacing

The `arcManagerGuidance` field (derived from `project/direction.md`) contains the pacing guidance for day segments. This is written during the Wide phase by `worldbuilder-story` — verify it is complete before export.

Key items to confirm are present in the direction note:
- Escalation ceiling: at most one emotionally significant beat per day under normal circumstances
- Transition handling: a short narrative acknowledgment between Morning / Afternoon / Evening / Night
- Explicit permission for quiet/atmospheric scenes (required; without it the engine treats every scene as an opportunity for significance)
- Time-of-day social rhythms: who is naturally active and accessible at each segment
