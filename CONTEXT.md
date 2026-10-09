# RPG World Builder Skills

Craft skills plus a type roster, running on the scraibe base plugin. This plugin defines the worldbuilding types and deliverables for the ainime-games.com world builder platform; scraibe owns all file management — document creation (`new_doc.py`), frontmatter enforcement, status lifecycle, inbox, triage, audit. No skill in this plugin creates files by hand or specifies frontmatter; the roster and the generated Templater templates do that.

Phases 1 and 2 are platform-agnostic. Only the Export phase produces ainime-specific output.

## Vault layout

A player project after `worldbuilder-setup`:

```
<project>/
  .claude/inbox.md
  .obsidian/            ← scraibe defaults + app.json overlay (attachmentFolderPath)
  _templates/           ← generated (generate_templates.py)
  Home.md  _bases/  _attachments/   ← chrome
  lorebook.md           ← definition note: the platforms' "world info" is this project's lorebook
  project/              ← foundation.md, plan.md, direction.md
  notes/                ← all entity notes, flat
```

No configuration file is written into the project: the project is a worldbuilder project because scraibe and this plugin are enabled for it, which `fleet:setup` records. Scraibe's corpus rule excludes reserved spaces (`+/`, `repo/`, `.claude/`, `Imports/`); everything else is a vault document. Chrome at the root — `Home.md` and the Bases — carries no frontmatter, and that is fine.

## Types

Defined in `defaults/types.json`, this plugin's internal roster. Entity types live in `notes/`; project types live in `project/`.

**character** — the comprehensive Wide-phase behavioral specification for one character; the source every export card derives from. _Avoid_: blueprint, draft card.

**location** — a named place as behavioral specification: who comes here, how the place pushes back on scenes.

**faction** — a named group's shared behavioral specification: collective mask, variation axes, inter-faction web.

**event** — a recurring world event (festival, observance, ritual) and what it does to scenes. Timing lives in the opening of its What Happens section, not in frontmatter.

**concept** — a discrete piece of world knowledge, layer-tagged (surface, mid, deep); packaged as a lorebook entry at export. _Avoid_: lorebook entry (for the Wide-phase artifact).

**story** — a narrative note with a `scope` of arc, intention, or introduction, linked to its parent via `up`.

**foundation** — the world foundation document (`project/foundation.md`), produced by `worldbuilder-world-foundation` in the Foundation phase.

**plan** — the project plan (`project/plan.md`): phase status table and cast plan.

**direction** — the standing creative brief (`project/direction.md`); the story engine's primary guard rail, exported verbatim as `arcManagerGuidance`.

**reference** — ingested external material with provenance, created by `scraibe:ingest`.

## Status lifecycle

A typed document is open while it carries no status tag, and born open with an empty `tags` list. It carries at most one status tag, and that tag closes it: `complete`, `deprecated`, `abandoned` or `archived` (`priority` and `deferred` are behavioral, not statuses).

For creative notes: a note stays open (no status tag) while it is being built and takes `complete` when its skill's self-check passes. Export gates on this — `project/foundation.md` must be tagged `complete`, and every exported character note must carry a closed status.

## Phases

The three phases are kinds of tracked item, not a mechanical lock. A tracked item is a note in the world's Anima domain folder that records one unit of work from its approved Specification to its final review.

- **Foundation phase** — a work item whose builder uses `worldbuilder-world-foundation` to produce the foundation document; `worldbuilder-story` fills the direction document. The plan.md Phase Status table calls this the Foundation phase. _Avoid_: setup phase.
- **Wide phase** — a set of entity items, one per related group of entities. All creative decisions live here. _Avoid_: development phase, building phase.
- **Export phase** — a work item whose builder runs `worldbuilder-ainime-export` to package Wide-phase notes into ainime format; the only phase that writes ainime field names. _Avoid_: deliverables phase, finalization phase.

No further item type exists. The Phase Status table in `project/plan.md` is the tracker; the export skill gates itself via its status-tag preflight. Session flow belongs to scraibe: `scraibe:orient` for briefings, `scraibe:triage` for pending work, `scraibe:audit` for health checks.

## Terms

- **foundation document** — the world's founding file, `project/foundation.md`, produced by `worldbuilder-world-foundation`.
- **seed note** — a spin-off tracking note in the world's Anima domain folder, born from a creative step's proposal (a home, an implied faction, a lore entry). It tracks an idea to explore;
- **entity item** — a tracked item that writes, checks and revises the entity notes of a related group of entities (for example a household and its home). The definer sets its size per item. Its steps are a creative step, a critic step (`worldbuilder-review`) and a creative revision step.
- **Foundation item** — the work item of the Foundation phase.
- **Export item** — the work item of the Export phase.

## Pointers

- Spec for this architecture: the note "2026-07-04-retool-worldbuilder-skills-on-scraibe-base" in the Anima vault's worldbuilder-workflow domain
- Type roster: `defaults/types.json`, with type bodies in `defaults/templates/*.md`; both hand-edited, no build step. `scripts/generate_templates.py` reads them to emit a project's Templater templates.
- Target platform field reference: `docs/target-system.md`
