# Source Extraction Standard

*Shared reference for `worldbuilder-source-ingestion` and `worldbuilder-character`. All prose follows `writing-style.md`. Each rule below is stated here once; the skills cite this file and do not restate it.*

This standard governs how a world's characters are built from a source corpus. It replaces per-character extraction. Per-character extraction lets one character's reference set drift from another's and leaves no record that links a card line to its evidence. The standard runs in two stages, then checks each card against its evidence, then checks the cards against each other.

The no-inference principle in `worldbuilder-source-ingestion` binds stage one: the sweep extracts and organizes, and never says that one source corrects another. Settling a disagreement happens only in stage two.

## Stages

**Stage one, the sweep.** One run of `worldbuilder-source-ingestion` over the whole corpus, for every character at once. Never one pass per character. The sweep writes source-organized reference documents with per-piece provenance, source absences and recorded discrepancies. It also writes the source map and the asset inventory below.

**Stage two, distillation.** One pass that reads only the sweep's documents and writes the reference sheet. The sheet collects each character's facts, the connections between characters, and the contradictions between sources, and settles each contradiction once.

**Card writing.** Each card is written from the reference sheet. Each card carries a coverage ledger. After a group of cards is written, the cross-card pass runs.

## Where files live

A world holds all extracted material in `reference/` at the world root, never under `notes/`. The export reads `notes/` whole, so nothing extracted can sit there. Notes in `reference/` use the `reference` type.

- Sweep documents: any name the ingestion skill's naming rule gives, directly in `reference/`.
- The source map: `reference/Source map.md`.
- The reference sheet: `reference/Reference sheet.md`.
- A character's coverage ledger: the `### Coverage ledger` subsection under `## Design Notes` in the character's note. The export excludes Design Notes, so the ledger never ships.

## The source map

The sweep opens with a complete inventory of the corpus: every file and page, grouped by the source's own structure (folder, site section, data file). The map names every file that sits outside the pattern its neighbours follow. Examples: a loose file beside season folders, a single-variant character beside four-variant ones, a character with no folder of its own. A stray file is recorded before any extraction starts, so no later step has to notice it.

## The asset inventory

For every image or media file the sweep lists, the inventory records the path, the variant the filename or metadata names, and a content hash of the file. The sweep worker computes the hash with a shell hash command. It interprets no image.

Files with identical hashes under different names or variants are one set. The inventory records that set once, with its duplicate names. A character whose four seasonal sets are the same images has one set.

## The reference sheet

One document for the whole cast, with these sections in this order. The checker reads the exact headings and table columns shown here.

**`## Characters`.** One `### <Name>` subsection per cast member. A cast member is anyone the sheet lists here. Each subsection has:

- `#### Facts`: one bullet per fact. Each bullet ends with `(source: <path>)`, where the path is relative to `reference/`. A fact states what the source says, in the source's words. It adds no trait, no card entry and no reading of the source.
- `#### Occupations`: a table with the columns `Occupation | Source`. Each occupation is the shortest phrase from the source that names the job (for example `General Store`, `gardener`). A job the source states is never left out of this table.

**`## Connections`.** One table with the columns `Kind | From | To | Fact | Source`. Every fact that spans two characters is a row: relationships, ownership, family and sibling order, occupations they share. `Kind` is a short word such as `ownership`, `sibling`, `family` or `friend`. For `ownership`, `From` is the owner and `To` is the owned. A sibling row states the order in `Fact` (for example `Olric is the older brother`).

**`## Contradictions`.** One table with the columns `Fact | Side A | Source A | Side B | Source B | Settled reading | Reason`. Every row keeps both sides with their provenance. A row with fewer than two sources is not a contradiction and fails the check. Distillation settles each contradiction once: it writes the chosen reading and the reason beside it. A contradiction the sources cannot settle is a question to the human, written with `Settled reading` set to `OPEN` until the human answers.

**`## Asset inventory`.** One `### <Name>` subsection per cast member who has assets, holding a table with the columns `Set | File | Hash`. One row per file. Two different sets of one character with the same hashes are a failure: they are one set.

The sheet contains nothing else: no traits, no card entries, no reading beyond collation.

## One home for a fact

The reference sheet is the home of every sourced fact. The card states the fact and the export derives it. A correction is made in the sheet first, then carried to every copy the card's ledger row lists. The stale-Body failure came from breaking this rule: the exported appearance was corrected, and the Body kept the old text.

## The coverage ledger

Every character note carries a `### Coverage ledger` subsection under `## Design Notes`. It is a table with the columns `Section | Entry | Source | Derived copies`, with one row per claim:

- `Section` is one of `Background`, `Body`, `Soul`, `Relationships`, `Intimate Dynamics`, `Voice / Dialogue`, `Story Seeds`. Intimate Dynamics rows exist only when the note has that section.
- `Entry` is the entry's number, counting the section's top-level bullets from 1. The Body preamble is prose, so it is split into clauses: one clause is one sentence of the preamble, written `preamble 1`, `preamble 2` and so on. Write one sentence for each feature group (hair, eyes, skin, build, distinguishing features, clothing, hidden features) so each group gets its own row.
- `Source` lists the reference documents the claim came from, separated by `;`. Each is a path relative to `reference/`, optionally followed by `#` and a heading. A claim with no source is not written into the card. Its row stays in the ledger with `Source` set to `flagged`, so the gap is visible. A flagged row is a gap the writer returns to the human; it never passes silently.
- `Derived copies` lists the export fields that reproduce the fact (`appearance` from the Body preamble, `role` from occupations, `spriteSets[].description` from ownership and appearance), so a correction visits every copy. It is not machine-checked.

The ledger covers every section a card can have, taken from `worldbuilder-character/card-format.md`.

## The gap rule

When the reference sheet lacks a fact the card needs, the writer does not guess. The writer follows these steps in order:

1. Re-read the sweep documents for the character.
2. Read the source itself for the character, fresh in the new context, for things the sweep overlooked. Record anything found in the sheet with its provenance.
3. If the fact is still missing, ask the human.

The writer never fills a gap from invention.

## The evidence readback

After a card is written, the writer re-reads every Background, Soul and Voice / Dialogue entry against the evidence its ledger row cites. The degree of each claim must be the degree the evidence shows. A word of extent or intensity (always, never, expert, obsessive, scientific, savant) stands only where the cited lines show it. An entry that outruns its evidence is rewritten down to the evidence, or returned to the human as a question. This is a reading of meaning. The writer does it as a self-check and the critic does it again. The checker script never does it.

## The cross-card pass

After a group of cards, check every Connections row against each card that carries it:

- A relationship is mirrored on both cards.
- Ownership is named the same on both cards.
- Sibling order is stated on both cards.
- Each character's occupations are complete against the sheet.

Fix every discrepancy in the cards, or return it to the human. The boundary is the cast as the sheet lists it. A relationship that names a cast member who has no card yet must appear in the Connections table, and is recorded as a pending mirror, not a failure. It becomes a failure when that character's card exists without the mirror entry.

## The derived-output check

The export copies several facts out of the cards: `role`, `appearance`, and each `spriteSets[].description`. The check runs over an exported `world.json` and compares each of these with the sheet and the cards:

- `role` must contain every occupation the sheet lists for the character.
- `appearance` must equal the card's Body preamble, ignoring whitespace. A character with no card is not compared.
- A `spriteSets[].description` must not name an owner for an owned character other than the owners the Connections table lists. The check reads a name as an owner when the description writes `<Name>'s`, `owned by <Name>`, `belongs to <Name>` or `pet of <Name>`.

Every difference is reported. The checker script (`scripts/check_coverage.py`, `export` mode) runs it. Wiring it into the export procedure belongs to the export rework item; until then, someone runs it after an export.

## The checker

`scripts/check_coverage.py` checks what a script can check:

- `world` mode, over a world root: every character note has a ledger; every entry of every card section present (Intimate Dynamics included) and every Body preamble clause has a ledger row; every ledger row names an entry the note has; every named source exists under `reference/`, and flagged rows are listed apart; every Contradictions row has two sources; no character has two sets with identical hashes; every Relationships entry that names a cast member with a note is mirrored on that note, and those that name a cast member with no note are listed as pending.
- `export` mode, over a world root and a `world.json`: the derived-output check.

The checker does not read meaning. The evidence readback and the judgement that a source supports a claim stay with the writer and the critic.

## The Fields of Mistria failures

Each failure from the Fields of Mistria world, and the component here that catches it:

| Failure | What happened | Caught by |
|---|---|---|
| Seasonal sprite set skipped | Merri's winter set was missing because eight winter files sat loose in her folder instead of in a `Winter/` folder. | The source map's stray-file rule records the loose files before extraction. |
| Four identical sets | Dozy and Henrietta were exported with four sprite sets that pointed at identical images under different asset ids. | The asset inventory's content hashes record identical files as one set; the checker's `world` mode fails two sets with the same hashes. |
| Stale appearance in card bodies | The appearance fields were corrected and the Body sections kept the old text and wrong details. 13 of 38 exported `baseProfile` Body paragraphs were an older variant. | One home for a fact, with the ledger row's derived copies; the derived-output check compares `appearance` with the Body preamble. |
| Wrong pet ownership | Sprite-set descriptions named Holt as the owner of Dozy and Henrietta; the cards were right. | The Connections table holds the ownership; the derived-output check reads the descriptions against it. |
| Job omitted from a role field | Celine's General Store job was in the extraction and dropped when the export wrote `role`. | The sheet's Occupations table lists every job the source states; the derived-output check requires `role` to contain them. |
| Savant instead of hobbyist | Celine was written as an autistic savant where the source gives a hobbyist, with lecture-shaped voice samples. | The evidence readback compares each claim's degree with the cited lines. |
| Sibling order unstated | March's card said "his brother Olric" without the birth order that Olric's card stated. | The Connections table states the order; the cross-card pass checks both cards state it. |
| Details not derivable from the source | Unsourced details stood in cards: capes in every season, a cabin in the Narrows, a fireplace habit, an invented scene. | The claim-level ledger with flagged rows; the gap rule when the sheet lacks the fact. |
