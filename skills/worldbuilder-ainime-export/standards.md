# Ainime Export Standards

*Reference file for `worldbuilder-ainime-export`. These standards apply to every world exported to ainime-games.com, whether it is a full world built through the Wide phase or a quick world assembled from existing character cards. Other files in this skill point here for the values below and restate none of them.*

Each standard has a short rule, then the reasons and details. Standard 11 describes the audit that checks them before packaging.

---

## 1. Calendar defaults

- A season has **14 days**.
- A day has **three segments**. The default names are **Morning, Afternoon and Evening**.
- A world may rename its segments to fit its game. A world about nightlife can use Day, Evening and Night. The count stays at three.
- Every world declares its segment names. The declaration is the single list that the calendar, the weather pools, the background time contexts and the location images all key on.

Where the declaration lives:

- **Full world:** the exported world file's `calendarConfig.daySegments` is the declaration. The audit is given those names with `--segments`.
- **Quick world:** `config.json` holds a `segments` list of the three names.

Every field that names a segment uses exactly the declared names: `calendarConfig.daySegments`, each season in `calendarConfig.weatherPools`, `artStyle.background.time_contexts`, and the `locations` object. A world that renames its segments keeps all of these in step with the declaration.

Compute the year from the world's own values: seasons × 14. With four seasons the year is 56 days. Trigger days, lore days and `availableFromDay` values are written for that year.

### Worked example: festival layout for 14-day seasons

One major festival per season and 4 to 5 minor observances across the year. A four-season year has 8 to 9 events. The absolute day is `(season number - 1) × 14 + day within the season`.

```
SEASON 1 (days 1-14)
  Day 4:   Major. Communal, renewal, a natural introduction opportunity.   Absolute day 4
  Day 11:  Minor. Trade or market, outsiders in the community.             Absolute day 11

SEASON 2 (days 15-28)
  Day 3:   Minor. Leisure, social, relaxed.                                Absolute day 17
  Day 10:  Major. The night when the hidden layer is most present.         Absolute day 24

SEASON 3 (days 29-42)
  Day 9:   Major. Harvest equivalent, abundance with underlying loss.      Absolute day 37
  Day 13:  Minor. A day of remembrance, quiet.                             Absolute day 41

SEASON 4 (days 43-56)
  Day 5:   Minor. Practical market before deep cold.                       Absolute day 47
  Day 11:  Major. Solstice equivalent, intimate, stories told in darkness. Absolute day 53
```

Adapt the layout to the world's own calendar. A festival that lands on day 15 or later of a season is outside a 14-day season and is a fault.

---

## 2. What may sit on a calendar

The calendar holds events that happen whatever the player has done:

- holidays, festivals and observances
- recurring venues and market days
- quest postings
- world events
- quests that open after an earlier calendar event

Every **character event** leaves the calendar by default. A character event is a scene that exists to move one character's story: a meeting, a visit, a confession, a conflict. That beat belongs in the character's Future Storylines section, where it fires when the story reaches it.

### Returning a character event

A character event returns to the calendar only with a written justification. The justification states why the event belongs on a fixed day rather than in that character's future storylines. A justification passes when it names one of these reasons:

- the event introduces a factor of the world or the story through the character, such as a place, a faction, a custom or a threat, and the world needs it on a set day (a first-meeting sequence that paces the opening days is this case);
- the event involves several characters, so it belongs to no single storyline;
- the day is part of the world's schedule, such as a ceremony that fixes when two characters must meet.

A justification that says only that the scene is important fails. Write the justification beside the event: in a quick world as a `justification` note on the trigger, in a full world in the event's note and in the export item's record. The script check cannot judge a reason. It enforces only a valid `kind` and, on a character event, a non-empty `justification`. The reader of the pre-flight check confirms that each justification names one of the reasons above and that any other exception carries one.

### Declaring each event

Every story trigger in the world file declares a `kind`: one of `opening`, `world`, `quest` or `character`. A trigger of kind `character` also carries a non-empty `justification`. The audit fails any trigger that lacks a valid `kind`, and any character trigger without a justification.

`kind` and `justification` are audit-only keys. They live in the tracked world file, and packaging strips them from the shipped one.

### Hidden events

`hiddenFromPlayer: true` is kept only for **player-independent surprises**: events that happen in the world whatever the player does, which the player should discover in play rather than see announced. A hidden event that exists to stage a character beat leaves the calendar under the character-event rule above, or returns with its written justification.

Scripted story beats, arrival sequences and a character's first appearance are not hidden events by default. They follow the character-event rule.

### Other exceptions

Any other event that does not fit the lists above needs a written justification in the same place and form.

### Ignore conditions

An event may carry a condition under which it is ignored. State the condition in the event's `promptInjection` as a plain sentence that opens the injection ("Ignore this event if the player has already ..."). Use it for events that make no sense after a particular choice, such as a quest the player has already finished.

---

## 3. Opening blurb and player choices

The opening blurb (`introText`) covers everything the player needs to know about the world and their immediate situation.

A choice the player is expected to make at the start is described in the blurb, together with every way of making it. No character asks the player for that choice in play. If the world sorts the player into a House, faction or path, the blurb lists the options and says how the player chooses (for example in the background description, by narrating the result, or by already being a member in the opening scene).

Check: read the `initialStoryArc` and the first story trigger. Neither may contain a character prompting the player for a choice the blurb already hands to the player.

---

## 4. Card text that only lets a card stand alone

Fan character cards carry text so that each card works on its own. Examples are genre lines such as `[Genre: Dark Fantasy, Political Intrigue]` and world-information blocks that repeat what the world data already holds. In an Ainime world that text duplicates the world data and pulls the narrator toward the card's own genre.

- Strip this text from every card and every lore entry in the exported world.
- Genre lives in the world's `genre` field only.
- A world-information block is removed when the world data already holds the same facts. Facts the world data lacks are rewritten as plain setting or lore text (see standard 5).

The form of this text differs for every source, so each world names what to strip in its own fix list. The tooling has no generic strip. Quick worlds name each exact string, the cards or entries it applies to, and the expected number of removals in the world's fix list.

---

## 5. Folded cards give facts, not instructions

A folded card is a card whose content joins the world as setting or lore text instead of becoming a character. Its text must read as facts about the world.

Prompt wording addressed to a narrator is removed. Example: `[Respond as the Gamemaster overseeing a single player game ...]`. Any world fact that wording held is kept as plain setting or lore text through the world's rewrite files. State each fact once.

---

## 6. No working-document text

No exported field refers to:

- the source cards or their greetings
- the export documents themselves
- the other game of a pair
- variants
- build steps

Known examples:

- "Play the scene as her alternate greeting sets it"
- "Play the opening exactly as the opening arc sets it"
- "The cards set the tone"
- "This document is exported verbatim as `arcManagerGuidance`"

Rewrite such a line as text about the world. Fix the line in the source (the world's rewrite files for a quick world, the direction note for a full world) so the next export carries the fix. A word that is also part of the setting (a "card" in a card game) is allowed. Record it as an exemption in the world's audit configuration.

---

## 7. Character colours

Every character `color` is a Tailwind text class `text-<hue>-<shade>` with a **mid-tone shade from 400 to 600**. A shade in that range reads on both light and dark backgrounds.

- Take the hue from the character's own palette.
- Every colour is unique within its world. Two characters may share a hue only with different shades.
- In a world shared by two games, uniqueness holds across the whole cast. The quick-world audit reads the world's configuration, which holds the cast of every game, so its colour check covers both games. A full world is one game.
- Every colour is a class the platform's stylesheet defines. A class the stylesheet lacks (for example `text-blue-500` or `text-yellow-500`) renders black. The defined set, with its source and read date, is kept in one data file the audit reads.

---

## 8. Location images across times of day

Each location gets one image per time of day. The first image generated for a location is the reference for the rest: every later time-of-day image of that location is drawn with the first image as its reference image. The prompt tells the model to keep the place in the reference and change only the lighting.

This keeps the images of one place consistent. A rerun draws only the missing later images and reuses the existing reference.

---

## 9. Emergent-character art guidance

Ainime draws characters it invents during play from the world's art guidelines. These characters have no canon portrait. Each world's character style guide (`artStyle.sprite`) is therefore tuned to the image model the platform uses for emergent characters. The project's own records name that model. The standard names no model, because the model changes with the platform.

Tune the guide to that model:

- Use reference-free wording. The model has no canon sprite to copy, so the guide alone carries proportions, line, palette, backdrop treatment and clothing rules.
- Put the things the model over-does into the guide as explicit limits.

The guide passes when the world's owner approves a comparison sheet: four invented characters generated from the guide alone, set beside four canon sprites. The guide gets at most two revisions. If the sheet is still not approved after the second revision, stop and ask the owner.

---

## 10. Visual-novel scene style

Ainime has a separate art-style field for visual-novel scenes, apart from the background and sprite guidance. Scenes show characters inside a location, so this style describes the look of a composed scene.

Every world sets this field; the field map marks it required. The value is written from the world's sprite style guide and its canon sprites: the same line weight, rendering, palette and backdrop treatment, written for a full scene with figures instead of a lone sprite.

The field is `artStyle.vnScene`:

| Key | Shape | Meaning |
|---|---|---|
| `enabled` | boolean | The "VN Scene Generation" switch in the world editor, which shows the other keys only while it is `true`. Set `true` whenever the other keys hold a value. |
| `style_prefix` | string | The look the scene director uses for the scene. |
| `style_suffix` | string | Rendering notes the scene director uses for the scene. |
| `negative_prompt` | string | Only image models that take a negative prompt use it; the others ignore it. |

The world editor's help text says that while `style_prefix` and `style_suffix` are both empty, the scene director uses the background and sprite styles, and once either holds text it uses `vnScene` instead. The platform's script does not show what a filled prefix does when `enabled` is `false`, so that case is not relied on.

The value passes when the owner sees one generated scene beside two canon sprites and approves that the scene matches the sprites. It follows the same two-revision limit as standard 9.

---

## 11. The audit

Every export passes two audit parts before packaging. This applies to full worlds and quick worlds alike. A failure in either part blocks the export.

Run the audit on the world file (`world.json`) that will be packaged.

### Part 1. Script check

A script reads the world file and reports each of these as pass or fail, naming the field and the offending text:

1. **Genre lines outside the genre field.** Bracketed meta lines (`[Genre:`, `[Genre/Writing style`, `[World Info:`, `[Instructions:`, `[Respond as`) anywhere but `genre`, and every exact string the world's own strip list names.
2. **Working-document wording** (standard 6), from a default phrase list plus the world's own additions and exemptions.
3. **Names with no matching entry.** Capitalised names in any text field that match no character, no lore keyword and no name on the world's known-names list. This check reports for the operator to read. Exempt a name by adding it to the known-names list.
4. **Colours** outside the 400 to 600 range, outside the classes the platform's stylesheet defines, or repeated across the world's whole cast (standard 7).
5. **Calendar settings** that differ from 14-day seasons or from the three declared segment names, fields that name segments with any other keys, and trigger days beyond twice the year length (standards 1 and 2).
   Also in this check: every story trigger declares a valid `kind`, and every `character` trigger carries a non-empty `justification` (standard 2).

Pass condition: the script report shows every check passed, with no failure. The name check (check 3) is report-only: it never fails, and its report is read before packaging.

### Part 2. Model read

A model reads the whole world file and reports, without editing anything:

- every contradiction within the file
- every reference to information the file does not hold

The report is a numbered list. Each item gives the field and the quoted text.

Pass condition:

- A model report exists for the current world file. Each report records the digest of the file it read. A report for any other digest is stale and does not count.
- Every finding is either fixed (the fix changes the file, so a fresh read follows) or carries a recorded disposition: one sentence, kept with the export record, saying why the text stands.

The two parts are independent. A clean script report does not replace the model read, and the model read does not replace the script.
