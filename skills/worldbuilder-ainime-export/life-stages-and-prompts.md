# Life Stages and Prompts Reference

*Reference file for `worldbuilder-ainime-export`. Contains the `yearContexts` entry shape and the Prompts tab's structure. Read the Life Stages part before writing `yearContexts`, and the Prompts part before writing any custom prompt.*

---

## Life Stages (`yearContexts`, optional)

Life stages describe how the world changes from one in-game year to the next. `yearContexts` is a top-level object keyed by string numbers (`"0"`, `"1"`, …), one entry per year. Source the content from `project/direction.md` and the arc notes that span years. Each entry is a full creative brief for one year of play:

```json
{
  "name": "Year One — The Rebuilding",
  "transition_warning_days": 7,
  "world_context": "...",
  "player_context": "...",
  "schedule_context": "...",
  "npc_concerns": "...",
  "world_pressures": "...",
  "sprite_set_guidance": "...",
  "transition_context": "...",
  "arc_resolution_guidance": "...",
  "next_year_preview": "..."
}
```

| Field | Purpose |
|---|---|
| `name` | Display name for the stage |
| `transition_warning_days` | Days before the stage ends that the player is warned |
| `world_context` | The state of the world during this stage |
| `player_context` | The player character's situation and constraints |
| `schedule_context` | Scheduling rules for the stage (week structure, work timing) |
| `npc_concerns` | What the characters want and are doing during this stage |
| `world_pressures` | External pressures, deadlines and constraints |
| `sprite_set_guidance` | Which sprite sets characters use during this stage |
| `transition_context` | What happens at the stage boundary |
| `arc_resolution_guidance` | How story arcs resolve at stage end |
| `next_year_preview` | What the next stage holds, for continuity |

A world with no year-over-year change omits `yearContexts`.

---

## Prompts (optional)

Per-AI-persona prompt overrides, on the platform's Prompts tab (formerly Custom Prompts). These inject directly into each AI persona's system prompt and take highest priority, overriding any conflicting built-in instructions. Use to customize how the AI writes, what it focuses on, and how it handles the game.

Available personas: Dungeon Master (scene narration, NPC dialogue, player interactions), Arc Manager, Narrative Architect, Relationship Analyst, Cast Analyst, Novelist, Psychoanalyst, VN Director, Volume Synopsis, Bio Compressor, Character Developer, Canon Archivist, Video Director. The Transition Director persona no longer exists.

Overrides are organized into prompt sets: named, switchable collections, of which one is active. The built-in Default set is read-only. The export records only a reference to the active set (`activePromptSet`, e.g. `{ "kind": "default" }`), and `customPrompts` stays empty while the Default set is active. Prompt sets are the builder's customization, not world content: the export does not produce them and leaves `activePromptSet` as it finds it.

Each persona's override is split into sub-sections (System Prompt, Story Cache, User Prompt, Scene opening + scene plan writing, Every turn). The Prompts tab also exposes the generation templates the World Builder itself uses (setting and lore, arc builder, character fields, expression prompts, time lighting, weather, events, life stages, moods and music style, player appearance, the in-game and World Builder character cards, character appearance, clothing rules). Both the sub-sections and the generation-template overrides are stored in `customPrompts` when a user-created set overrides them.

The AI is already handling complex instructions — keep custom prompts clear and concise. The only hard constraint is the JSON response schema; everything else (NPC behavior, writing style, pacing, tone) is yours to shape.

Most worlds do not need custom prompts. Use them when the world has specific mechanical or narrative needs that the standard fields cannot express — for example, enforcing a particular dialogue style, or adding gameplay mechanics the platform does not natively support.

