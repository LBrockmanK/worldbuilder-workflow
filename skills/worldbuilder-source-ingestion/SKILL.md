---
name: worldbuilder-source-ingestion
description: Use when bringing external source material into the worldbuilder — game assets, existing character cards, fiction excerpts, wiki pages, or any reference material that will feed the character Q&A workflow or other entity skills.
---

# Source Ingestion

*All prose this skill produces follows `../writing-style.md`. Read it
before writing any reference document.*

## Overview

Source ingestion extracts content from external material and organizes
it into reference documents. It does not interpret what the material
means. The Q&A workflow (worldbuilder-character and other entity
skills) handles interpretation when it consumes the references.

**Governing spec:** "2026-08-15-source-ingestion-skill-reference-document-structure-and-extraction-principles" in the Anima vault's worldbuilder-workflow domain.

---

## The No-Inference Principle

Ingestion extracts and organizes. It does not interpret.

**The boundary:** if producing a piece of output requires asking
"what does this mean?" rather than "what does this say?", it belongs
to the Q&A workflow, not this skill.

**What ingestion does:**
- Extracts content verbatim or with structural format conversion
- Records provenance per piece (file path, URL, page, section)
- Follows the source's own organization
- Notes source absences

**What ingestion does not do:**
- Label material thematically
- Identify behavioral patterns or psychological traits
- Propose card-format entries
- Map material to card blocks
- Synthesize across sources
- Rate confidence or importance
- Summarize — selecting what matters is interpretation. (When the
  user directs a narrower extraction depth, that is scoping, not
  summarizing — see Extraction Depth below.)
- Declare one source as correcting another (record discrepancies)

**Permitted structural transformations** (exhaustive — anything else
is interpretation):
- Format conversion (TOML/JSON/XML to markdown)
- Reproducing existing speaker tags from tagged dialogue
- Stripping engine markup while preserving content
- Reproducing file/directory names as section headers
- Reproducing existing metadata labels from filenames, manifests,
  or other source structures

---

## Workflow

1. The user provides source material (files, URLs, documents)
2. Explore the source to map its structure
3. The user confirms scope and depth
4. Extract content following the source's own organization
5. Output one or more reference documents
6. The Q&A workflow consumes the references as source material

### Exploring the source

Before extracting, map the source's structure: directory tree, file
types, file counts, naming conventions. Present this map to the user
and confirm which parts to extract. Large sources (thousands of files)
may need selective extraction — the user decides which directories
or file sets to include.

Explore is iterative, not one-shot. The initial map covers what the
user identified; extraction may reveal adjacent sources worth
including. After each batch, propose newly discovered sources with a
relevance assessment and recommended depth. The user decides whether
to expand scope.

For sources with many independent files (game data dumps, wiki sites),
classify sources by what they contribute to the world presentation
and recommend an extraction depth for each. Independent sources can
be extracted in parallel — identify which sources share no
dependencies so workers do not collide.

### Extraction depth

Three levels, always user-directed:

- **Full** — extract all fields with values. Default for sources
  central to the entity being built (a character's dialogue files,
  a location's primary definition).
- **Structural** — extract the structure (section names, field names,
  categories, relationships) with representative values, but not
  every individual entry. For a list of 200 items, capture the
  list's purpose and a few examples.
- **Broad strokes** — capture what the source is and how it is
  organized without individual entries. One table or paragraph per
  source section.

The agent proposes a depth per source based on size and centrality;
the user confirms. The agent choosing not to extract something it
considers unimportant is interpretation (banned); the user choosing
"broad strokes" for a 60K inventory file is scoping (fine).

Within any depth level, the no-inference principle holds: reproduce
what the source says at the chosen granularity.

### Creating reference documents

Use the scraibe plugin's `new_doc.py` for document creation
(provenance stamping, frontmatter). Do not use scraibe:ingest's
judgment pass (source ranking, contradiction resolution, relevance
extraction) — those conflict with the no-inference principle.

```bash
python "<scraibe-plugin>/scripts/new_doc.py" --type reference \
  --title "<Topic> — <Source Label>" \
  --description "<what this document contains>" \
  --dir <project entity directory>/reference
```

Record source paths in the frontmatter `resources` field.

The date-prefixed filename from `new_doc.py` is the default. Rename
only if the generated filename is misleading.

---

## Source-Path Organization

Reference documents follow the source's own file and directory
structure. The source's directory organization is the partition.

- If a game organizes files under `Conversations/` and `Cutscenes/`,
  those directories become separate documents
- If a novel has no file structure, the document follows chapter/page
  order
- Mixed-content files (dialogue mixed with narration) are reproduced
  as-is without splitting by content type — the file is the unit

**Within a source**, content is ordered by source path (alphabetical
or directory-tree order) or by in-source sequence. No reordering by
perceived importance, narrative arc, or thematic grouping.

**Across sources**, related small files can be combined into one
document (see Granularity below). Each source gets its own H2 section
with a source-path heading. The grouping of sources into documents
is a user or agent decision about document scope — it does not
change the ordering within each source's section.

---

## Reference Document Structure

**Granularity:** one document per source directory or logical source
boundary (a wiki page, a data file, a directory of related files).
When sources are small, multiple related sources can share a document
with section breaks preserving each source's path as headings —
prefer this over creating many tiny documents. The test: if each
document would be under ~50 lines of extracted content, combine them.

**Per-entity vs type-level documents:** character ingestion creates
per-entity directories (`notes/adeline/reference/`) because each
character draws from many sources. Non-character entities often come
from a single source covering many instances (a locations file
defining 60 locations, a festivals file defining 4 events). These
produce type-level reference documents in `notes/<entity-type>/reference/`.

**Entity placement:** when the source doesn't map to an obvious
entity note type:
- Describes a place or space → a location note in `notes/`
- Describes a temporal event or story progression → an event note in `notes/`
- Describes a group identity or social structure → a faction note in `notes/`
- Everything else (systems, ecology, economy, culture) → a concept note in `notes/`
- Tiebreak: where would someone search for it?

**Multi-entity sources:** when a source contains material about
multiple characters or entities (group conversations, ensemble
scenes), store the material once in a shared document. Each entity's
reference set links to the shared document. No per-entity splitting
or duplication.

**Naming:** `<topic> — <source-label-or-summary>.md`

For per-entity documents: `<entity-name> — <source-label>.md`
For type-level documents: `<topic> — <descriptive-label>.md`
For shared multi-entity documents: `<source-label> — <entity-names>.md`

---

## Extraction Guidance

What to capture from each source. Per-piece provenance (source file
path or section) is required for all extraction.

### Structured data

- All fields with values, reproduced as-is
- Field names and structure (nesting, arrays)
- Ambiguous field names: `[field purpose unclear]`
- Units, enums, cross-references preserved
- Source file path

### Text content (dialogue, narration, prose)

- Full text with speaker attribution where tagged
- Trigger/prerequisite conditions
- Expression/portrait/mood tags where present
- Branching choices with response paths
- Refresh/cooldown rates and gameplay mechanics
- Actions triggered (items given, state written, effects)
- Source file path for each block

### Narrative events (cutscenes, quests, story scripts)

- Scene setup: participants, location, preconditions
- Full dialogue/action sequence
- Branching points and outcomes
- State changes
- Follow-up triggers
- Source file path for each event

### Schedule and calendar data

- Timestamped locations and activities
- Day/season/weather conditions
- Scheduled vs. one-time events
- Participation conditions
- Source file path

### Visual assets

- File path and naming convention
- Available variants (expressions, outfits, seasons) reproduced from
  filenames and metadata — not from viewing images
- When images are viewed for physical description, mark every
  observation `[perceptual]` with the source image path
- Discrepancies between visual and text sources noted as
  discrepancies, not corrections

### External references (wiki, community, developer commentary)

- Content reproduced with source attribution (URL, page title,
  access date) — not summarized. If a source is too large to
  reproduce in full, reproduce the sections the user identified
  during source exploration with provenance
- `[official]` or `[community]` marker per source
- Discrepancies with other sources noted with both sides and
  provenance — never declared as corrections

---

## Source Absence Notes

Each reference document ends with a **Source Absences** section
noting what the extracted source does not contain. Absences are
factual observations about the source's coverage, limited to
structural observations: missing fields in structured data, empty
directories, absent file types declared elsewhere in the source.

**Valid:** "The `Schedules/` directory has subdirectories for Spring,
Summer, and Fall but none for Winter."

**Valid:** "This directory contains no `.toml` files for Winter
schedules — only Spring, Summer, and Fall are present."

**Invalid (pipeline-specific):** "No information about core fear or
false belief." (Card-format concepts the source has no obligation to
contain.)

**Invalid (unbounded):** "Does not mention childhood pets." (The
source omits infinitely many facts — note structural gaps in the
source's own coverage only.)

---

## Review

The reference documents are a deliverable of ingestion. The scraibe adversarial-review skill defines this block's shape and runs the loop.

- **Deliverable:** the reference documents this skill writes.
- **Shape:** document — the rounds are capped and the human's approval is the gate.
- **Criteria:** The No-Inference Principle and the Reference Document Structure sections of this skill.
- **Scope:** named files — the reference documents written in this run.
- **Reference inputs:** the source material that was ingested.
- **Stakes default:** durable.
- **Overrides:** none.
