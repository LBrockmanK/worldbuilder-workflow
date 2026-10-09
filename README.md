# worldbuilder-workflow

[![tests](https://github.com/LBrockmanK/worldbuilder-workflow/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/LBrockmanK/worldbuilder-workflow/actions/workflows/tests.yml)

Claude Code skills for building a game world on the [ainime-games.com](https://ainime-games.com) world builder platform. Install these skills once; run them in Claude Code to get an AI-assisted worldbuilding pipeline from blank page to finished export.

**Requires the scraibe plugin.** Scraibe owns file management — document creation, frontmatter enforcement, status lifecycle, inbox, and audit. This plugin ships the worldbuilding craft skills and an OKF preset; without scraibe installed it does nothing.

---

## What these skills do

The skills guide you through three phases. Each phase is a kind of tracked item: the work runs as items in the world's Anima domain folder, each with an interview, an approved Specification and a final review.

### Foundation phase (Phase 1)

A work item whose builder uses `worldbuilder-world-foundation`. The interview asks the foundational questions — setting, tone, household structure, hidden layer — and the builder produces `project/foundation.md`, a platform-agnostic world proposal that every later phase builds on.

**Key output:** `project/foundation.md`

### Wide phase (Phase 2)

A set of worldbuilder entity items. Each item covers a related group of entities (for example a household and its home). A creative step writes the notes, a critic step checks them, and a revision step applies the mechanical fixes. Concept, story, location, faction, event and character notes are built this way. All creative decisions live here. Nothing in Phase 2 is ainime-specific.

**Key outputs:** character notes, concept notes, story notes, location notes, faction notes, event notes in `notes/`

### Export phase (Phase 3)

A work item whose builder runs `worldbuilder-ainime-export`. Wide-phase notes are packaged into ainime-games.com format. This is the only phase that writes ainime field names.

**Key output:** ainime character cards and supporting JSON fields

---

## Skills

| Skill | When to use |
|---|---|
| `worldbuilder-setup` | Starting a brand-new project — run once; adopts scraibe with the worldbuilder preset |
| `worldbuilder-world-foundation` | Foundation phase — fills `project/foundation.md` and plans the Wide phase |
| `worldbuilder-concept` | Wide phase — writes concept notes |
| `worldbuilder-event` | Wide phase — writes event notes |
| `worldbuilder-story` | Wide phase — writes story notes and the direction document |
| `worldbuilder-location` | Wide phase — writes location notes |
| `worldbuilder-faction` | Wide phase — writes faction notes |
| `worldbuilder-character` | Wide phase — builds individual character notes |
| `worldbuilder-ainime-export` | Export phase — converts character notes to ainime format |

---

## How to start

### New project

Run `worldbuilder-setup` once. It writes the OKF config, installs the vault chrome, creates the project documents, and hands off to `worldbuilder-world-foundation` for the foundation conversation.

### Returning session

Session flow belongs to scraibe: `scraibe:orient` briefs you on where the project stands, `scraibe:triage` processes pending work, and the craft skills fire on demand. Starting from existing material (SillyTavern cards, prior exports, notes)? Run `scraibe:ingest` first, then the craft skills work from the reference documents it produces.

---

## Installing the skills

These skills are distributed as a Claude Code plugin package. Install the plugin through Claude Code's plugin manager — you do not install individual skill files manually. For step-by-step installation instructions, find this plugin's listing in the Claude Code plugin marketplace.

Once installed, invoke any skill using the `/` command prefix in Claude Code (e.g., `/worldbuilder-setup`, `/worldbuilder-character`).

---

## Project vocabulary

The skills use consistent terminology throughout. Key terms:

- **Foundation phase / Wide phase / Export phase** — the three phases, each a kind of tracked item
- **Seed note** — a spin-off tracking note in the world's Anima domain folder
- **`project/foundation.md`** — the foundation document, produced in the Foundation phase
- **Character note** — the comprehensive Wide-phase document for a single character
- **Concept note** — a discrete piece of world knowledge (exported as a lorebook entry)
- **Story note** — a narrative direction document (direction, arc, or intention scope)

Full terminology reference: [`CONTEXT.md`](CONTEXT.md)
