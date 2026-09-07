---
name: worldbuilder-setup
description: Use when starting a new worldbuilding project. Installs the vault chrome and creation templates onto a scraibe-enabled project and hands off to worldbuilder-world-foundation.
---

# Worldbuilder Setup

## Overview

This skill turns a directory into a worldbuilding project: an Obsidian vault with worldbuilder's creation templates wired in, and the three project documents created. Run it once per project, before any other worldbuilder skill.

Scraibe owns file management from here on — document creation, frontmatter enforcement, status lifecycle, inbox, audit. This skill only installs the chrome and templates, then gets out of the way. It asks no creative questions; genre, tone, cast, and setting belong to `worldbuilder-world-foundation`.

**This skill writes no configuration into the project.** The worldbuilder type roster lives in this plugin, at `defaults/types.json`, and is read from there whenever it is needed. A project does not get a copy. What makes worldbuilder available is that scraibe and this plugin are *enabled for the working tree the session runs in* — see Step 2.

Two directories matter and they are usually different. The **project root** is where the vault content goes: the directory the user names for their world. The **session root** is the working tree the session is running in, whose `.claude/settings.json` carries the live plugin enablement; for a project that lives inside a larger vault, that is the vault root, not the project folder. Steps 3 through 6 all operate on the project root; only Step 2 looks at the session root.

## Steps

### Step 1: Check scraibe

Resolve the scraibe plugin root — the directory containing `scripts/new_doc.py`:

1. Read `~/.claude/plugins/installed_plugins.json` and take the `installPath` of the entry whose key starts with `scraibe@`.
2. If that file or key is missing, fall back to globbing `~/.claude/plugins/marketplaces/*/*/scripts/new_doc.py` — the plugin's directory is not necessarily named `scraibe` (older installs used `okf-enforcement`).

If neither resolves, stop: "This plugin requires the scraibe plugin. Install it first."

Record the resolved root — later steps use its scripts and defaults. Never hardcode this path; resolve it fresh each run.

### Step 2: Check enablement at the working tree root

Adoption is plugin enablement, and fleet:setup is its sole writer.

**Check the working tree the session is running in, not the project directory.** These are usually not the same place. A project inside a vault is not an independent session: the session runs at the vault root, so the vault root's `.claude/settings.json` is the enablement that is actually live. A project folder's own settings are inert in that case, and checking them would fail a correctly-enabled setup.

Determine that root first: it is the directory the session was started in — the working tree containing the `.claude/` whose settings apply. For a vault-homed project this is the vault root, well above `<project>`. If in doubt, ask the user which directory they launched the session from. Call it `<session-root>`.

Resolve the fleet plugin root the same way as Step 1 (the entry whose key starts with `fleet@`), then:

```
python "<fleet>/scripts/plugin_enablement.py" --root "<session-root>" status
python "<fleet>/scripts/plugin_enablement.py" --root "<session-root>" show
```

Both conditions must hold:

- `status` exits 0 — a plugin selection is recorded there. Exit 1 means no selection exists at all: **stop** and tell the user to run `fleet:setup` at `<session-root>`.
- `show` lists both scraibe and this plugin as `enabled`. The marketplace suffix varies by install (`scraibe@<marketplace>`); match on the plugin name before the `@`. If either is missing or reads `disabled`, **stop** and tell the user to run `fleet:setup` at `<session-root>` and enable scraibe and worldbuilder-workflow.

Do not work around a failed check by writing config into the project — there is no config to write, and proceeding would make "adopted" mean nothing.

Then ask: "What is the name of your world or project?"

### Step 3: Install the chrome

- Copy `<scraibe>/defaults/obsidian/` to `<project>/.obsidian/`.
- Overlay this skill's `worldvault/.obsidian/` directory on top (app config, community-plugin registration, and the vendored Templater plugin).
- Copy this skill's `worldvault/Home.md` to the project root, replacing `{{PROJECT_NAME}}` with the project name.
- Copy this skill's `worldvault/_bases/` directory to `<project>/_bases/`.
- Create empty directories: `notes/`, `project/`, `_attachments/`.

Chrome lives at the vault root — `Home.md` and the Bases carry no vault frontmatter, and that is correct. Scraibe's corpus rule excludes reserved spaces (`+/`, `repo/`, `.claude/`, `Imports/`), so nothing there is validated as a vault document.

### Step 4: Create the project documents

From the project root, with this plugin's root recorded as `<worldbuilder>`:

```
python <worldbuilder>/scripts/create_project_docs.py --project-root . --name "<Name>"
```

This creates `project/seed.md`, `project/plan.md`, `project/direction.md` with correct frontmatter (`human-ready` status), body templates from `defaults/types.json`, and `lorebook.md` at the project root — the definition note for the one term the export platforms name differently. The script validates that `plan.md` contains its Phase Status table before exiting.

Verify that all four files exist and that `project/plan.md` contains the `## Phase Status` table and `## Cast Plan` heading.

### Step 5: Generate the creation templates

From the project root, with this plugin's root recorded as `<worldbuilder>`:

    python <worldbuilder>/scripts/generate_templates.py --out . \
      --dir "notes/=character,location,faction,event,concept,story" \
      --dir "project/=seed,plan,direction" \
      --obsidian

The generator reads its type roster from this plugin's own
`defaults/types.json` — there is no `--config`, and nothing is read from
the project.

This writes `_templates/` (one template per type plus a type-picker per
directory) and points the vendored Templater's folder attachments at
them. From here on, a note created in `notes/` or `project/` inside
Obsidian receives compliant frontmatter and its type body at creation —
the type-picker asks one question in mixed directories.

This applies to notes created from here on, and only inside Obsidian. It
does not reach back to the three documents Step 4 already created, which
is why Step 4 applies their bodies itself.

### Step 6: Validate and hand off

```
python <scraibe>/scripts/validate.py project --root . --format human
```

There is no rules-generation step: scraibe retired `generate_rules.py` and the generated-rules mechanism with it. Project conventions live in the project's own agent-conventions file, which `scraibe:setup` maintains.

Report the validation result to the user. Tell them the vault is ready to open in Obsidian ('Open folder as vault' on the project root; Bases and the vendored Templater need Obsidian 1.12.2+ with community plugins enabled for this vault). Then hand off to `worldbuilder-world-foundation` for the seed conversation.

## What this skill does not do

- No creative questions — those belong to `worldbuilder-world-foundation`.
- No migration of pre-scraibe worldbuilder vaults — that is a `scraibe:setup` migration run.
- No plugin enablement — that is `fleet:setup`'s job. This skill only checks it.
- No Obsidian Sync configuration, plugin installation, or cloud integration.
