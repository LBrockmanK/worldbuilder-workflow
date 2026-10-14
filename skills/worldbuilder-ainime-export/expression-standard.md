# Expression Standard

*Reference file for `worldbuilder-ainime-export`. It is the source of truth for the sprite expression tiers and the sprite background rule. Read it when choosing the tier at the start of a project and when writing the sprite style text.*

House standard for the expression set of AI-generated sprite sets that use monolithic character portraits: one image per expression, no component layering. Overlay-style consolidations (annoyed as an angry brow layer, shocked as a surprised intensity layer) do not apply to monolithic generation.

---

## Tiers

Three tiers. Each is a strict superset of the one below it. The tier names carry no expression counts on purpose, so a change in membership never renames a tier. The current counts live in the cost table.

### Essential

The minimum viable set. It covers every fundamental emotional beat of a complete narrative. Use it for large casts or projects where generation cost dominates.

| # | Expression | Narrative role |
|---|---|---|
| 1 | neutral | Baseline, listening, exposition |
| 2 | happy | Positive, agreement, warmth |
| 3 | sad | Loss, regret, sympathy |
| 4 | angry | Conflict, hostility, confrontation |
| 5 | annoyed | Frustration, exasperation, mild negative |
| 6 | surprised | Reveals, sudden information, reactive |
| 7 | laughing | Peak delight, open laughter |
| 8 | crying | Grief, sobbing, breakdown |
| 9 | embarrassed | Social misstep, fluster, mortification |
| 10 | nervous | Anxiety, unease, tension |
| 11 | confident | Self-assurance, resolve, authority |
| 12 | flirty | Romance, charm, playful attraction |
| 13 | sleepy-tired | Exhaustion, low energy, morning and late-night scenes |

### Standard (recommended default)

Adds six expressions for richer narrative nuance. Recommended for most new projects.

| # | Expression | What it adds |
|---|---|---|
| 14 | beaming | High-intensity positive; visually distinct from happy (wide smile with teeth visible, against a small smile) |
| 15 | blushing | Romantic self-consciousness; warm and positive, distinct from embarrassed's mortification |
| 16 | emotional | Vulnerability, being moved; no substitute in Essential (open, shining eyes, still posture) |
| 17 | upset | Quiet hurt; fills the space between sad and angry |
| 18 | wary | Suspicion, guardedness; distinct from nervous's self-focused anxiety |
| 19 | worried-concerned | Directed concern for others; outward-facing, against nervous's inward anxiety |

### Expansive

The full 26-expression set. Use it for projects ported from existing media with an established expression library, or when maximum granularity is needed.

| # | Expression | Why it is in the third tier |
|---|---|---|
| 20 | amused | Quiet amusement; subtle, and happy plus confident cover the beat |
| 21 | comedic-shock | Exaggerated comic surprise; specific to anime and comedy genres |
| 22 | emotional-shock | Stunned disbelief; surprised plus emotional cover the beat |
| 23 | intimate | One step past flirty; visually close to it in monolithic sprites |
| 24 | shy | A mild blend of embarrassed and nervous |
| 25 | smiling | Near-identical to happy in monolithic sprites (a gentle closed-mouth smile against a small smile) |
| 26 | stoic | The character's neutral is their stoic in monolithic sprites; the voice carries the distinction |

---

## Cost reference

Images per character per sprite set:

| Tier | Images | Against Expansive |
|---|---|---|
| Essential | 13 | -50% |
| Standard | 19 | -27% |
| Expansive | 26 | baseline |

A project of 20 characters with 2 sprite sets each needs 520, 760 or 1,040 images for the three tiers.

---

## Usage

Standard is the default `availableExpressions` set for new projects. A project overrides to Essential or Expansive based on cast size and narrative needs. The tier choice is made early, because it fixes the generation scope for every character.

Write the chosen tier's expressions to `availableExpressions`. Expression names use hyphen-case in this file and in preset files, and snake_case in the platform's `availableExpressions` array. The mapping is mechanical: hyphens become underscores (`sleepy-tired` becomes `sleepy_tired`).

A world may define its own list instead of a tier. Every sprite set then carries `neutral` plus any subset of that list; the pre-flight check in `export-procedure.md` tests exactly that.

---

## Background

One rule covers the background of every sprite in a set: **every expression of a sprite set uses one fixed two-colour gradient drawn from the character's palette. The gradient is part of the set's visual identity and does not change with emotion.**

Reasons: an emotion-keyed colour clashes with some characters, and a character-specific adjustment per emotion breaks emotion consistency across the cast.

This is the only statement of the rule. A preset or a prompt file points here and does not restate it. The `artStyle.sprite.style_suffix` text in `world.json` is written from this rule: the exported text is a derived copy, not a second statement of it. If the rule changes, change it here and rewrite the exported suffix. The platform's own `maintainConsistency` setting adds a same-character line to each sprite prompt; it does not change this rule.
