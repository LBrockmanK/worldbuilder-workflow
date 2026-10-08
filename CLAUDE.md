# worldbuilder-workflow

Craft skills and type roster for building player world visions for the
ainime-games.com world builder platform. Runs on the scraibe base plugin
(hard dependency): scraibe owns file management, and its vault
conventions govern this repo's own `.claude/`.

## Working in this repo

- **Domain docs:** `CONTEXT.md` (single-context terminology) and
  the decision notes in the Anima vault's worldbuilder-workflow domain
  (0001 three-phase architecture, 0003 platform decoupling, 0004 action-line
  style model). Use the established vocabulary in issue titles, proposals,
  and test names; if your output contradicts a decision note, surface the
  conflict explicitly instead of silently overriding.
- **Shipped content is model-neutral:** never name a specific AI model
  in templates, stub notes, or skill instructions that reach end users —
  "for future agents", never a product name. Some users run these skills
  with other models.
- **The type roster is plugin-internal:** `defaults/types.json` holds the
  types (their `fields` maps and `template_file` references) and the tag
  vocabulary; type bodies are markdown in `defaults/templates/*.md`. Edit
  both by hand — there is no build step.
  `scripts/generate_templates.py` reads the roster and resolves the
  `template_file` references itself when it emits Templater templates.
  Projects never receive a copy of the roster.
- **Skill prose follows the plugin's own writing doctrine:** plain,
  concrete, no filler — `skills/writing-style.md`; phrase-level review
  checklist in `docs/slop-phrases.md`.

## Agent policies

- **Writing agents operate at the top available tier.** Character cards,
  prose content, and any creative writing that requires characterization
  judgment dispatch at the highest tier, not the default. Tier names
  follow the fleet tier map; the current top tier is opus-class.
- **Adversarial review uses codex.** Pre-completion adversarial review
  runs through `codex exec --sandbox read-only` for cross-provider
  independence. The same model that wrote the content cannot review it.
