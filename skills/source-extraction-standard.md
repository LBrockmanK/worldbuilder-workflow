# Source Extraction Standard

*Shared reference for `worldbuilder-source-ingestion` and `worldbuilder-character`. All prose follows `writing-style.md`. Each rule below is stated here once; the skills cite this file and do not restate it.*

This standard governs how a world's characters are built from a source corpus. It replaces per-character extraction. Per-character extraction lets one character's reference set drift from another's and leaves no record that links a card line to its evidence. The standard runs in two stages, then checks each card against its evidence, then checks the cards against each other.

The no-inference principle in `worldbuilder-source-ingestion` binds stage one: the sweep extracts and organizes, and never says that one source corrects another. Settling a disagreement happens only in stage two.

## Stages

**Stage one, the sweep.** One run of `worldbuilder-source-ingestion` over the whole corpus, for every character at once. Never one pass per character. The sweep writes source-organized reference documents with per-piece provenance, source absences and recorded discrepancies. It also writes the source map and the asset inventory below.

**The sweep is complete.** For a character corpus, the extraction depth levels of `worldbuilder-source-ingestion` (selective, structural, broad strokes) do not apply. The sweep covers every file in the corpus at full depth, so the reference sheets can offer every fact. Only the human can narrow a corpus, and a narrowed corpus is recorded in the source map.

**Stage two, distillation.** Its own step, run by one worker at the builder role, separate from the sweep workers. It reads only the sweep's documents and writes the reference sheets. It is permitted to settle contradictions, as the reference sheets section sets out. The no-inference principle of the ingestion skill covers the sweep only; distillation is not ingestion, and nothing in the sweep settles anything.

**Card writing.** Each card is written from its reference sheet by the creative step, which reads the sheet and does not build it. Each card carries a coverage ledger. A claim the writer infers from the sheet facts and the anime or manga is recorded as inferred in the coverage ledger. After a group of cards is written, the cross-card pass and the checker run.

## Where files live

A world holds all extracted material in `reference/` at the world root, never under `notes/`. The export reads `notes/` whole, so nothing extracted can sit there. Notes in `reference/` use the `reference` type.

- Sweep documents: any name the ingestion skill's naming rule gives, directly in `reference/`.
- The source map: `reference/Source map.md`.
- The reference sheets: `reference/sheets/`, described in the reference sheets section below. The names there are fixed, because the checker finds the sheets by folder and name, so they are the one exception to the ingestion skill's date-prefixed default.
- A character's coverage ledger: the `### Coverage ledger` subsection under `## Design Notes` in the character's note. The export excludes Design Notes, so the ledger never ships.

## The source map

The sweep opens with a complete inventory of the corpus: every file and page, grouped by the source's own structure (folder, site section, data file). The map names every file that sits outside the pattern its neighbours follow. Examples: a loose file beside season folders, a single-variant character beside four-variant ones, a character with no folder of its own. A stray file is recorded before any extraction starts, so no later step has to notice it.

## The asset inventory

For every image or media file the sweep lists, the inventory records the path, the variant the filename or metadata names, and a content hash of the file. The sweep worker computes the hash with a shell hash command. It interprets no image.

Files with identical hashes under different names or variants are one set. The inventory records that set once, with its duplicate names. A character whose four seasonal sets are the same images has one set.

## The reference sheets

The reference sheets are one document per character, plus world files, in `reference/sheets/`. The checker reads the exact headings and table columns shown here, and it reads only the files directly in the folder; a subfolder (for example `checks/` or `entries/`) is ignored.

**The character sheet `reference/sheets/<name>.md`.** One per cast member. A cast member is anyone who has a character sheet. The sheet's canonical name is its file name without the extension and without a leading number and the space after it (`1020 Seiun Sky.md` names Seiun Sky). The frontmatter `aliases` list holds further names of the same cast member (a list of strings). The checker resolves every name through this mapping, case-insensitively: a card's file name, a relationship name on a card, a `From` or `To` value, and an exported character's name. Two sheets that claim one name are a failure. The sheet has these level-2 sections in this order:

- `## Profile`: who the character is, in a few lines.
- `## Facts`: one bullet per fact, grouped under any level-3 headings the sheet needs. Each bullet ends with `(source: <path>)`, where the path is relative to `reference/`. A fact states what the source says, in the source's words. It adds no trait, no card entry and no reading of the source.
- `## Occupations`: a table with the columns `Occupation | Source`. Each occupation is the shortest phrase from the source that names the job (for example `General Store`, `gardener`). A job the source states is never left out of this table.
- `## Connections`: a table with the columns `Kind | From | To | Fact | Source`. Every fact that spans two characters is a row: relationships, ownership, family and sibling order, occupations they share. `Kind` is a short word such as `ownership`, `sibling`, `family` or `friend`. For `ownership`, `From` is the owner and `To` is the owned. A sibling row states the order in `Fact` (for example `Olric is the older brother`). A row sits in one sheet; the checker reads the rows of every sheet together.
- `## Contradictions`: a table with the columns `Fact | Side A | Source A | Side B | Source B | Settled reading | Reason`. Every row keeps both sides with their provenance. A row with fewer than two sources is not a contradiction and fails the check. Distillation settles each contradiction once: it writes the chosen reading and the reason beside it. A contradiction the sources cannot settle is a question to the human, written with `Settled reading` set to `OPEN` until the human answers.
- `## Asset inventory`: one table with the columns `Set | File | Hash`, one row per file, for this character only. Two different sets of one character with the same hashes are a failure: they are one set. Two characters may share hashes.
- `## Provenance`: how the sheet was distilled and from which sweep documents.

A table section with no rows, or a section with no table, counts as empty and is not a failure. Each of the four tables may carry a trailing `Ids` column; the checker ignores it.

**The world file `reference/sheets/world <n> <topic>.md`.** Facts that belong to no one character: places, calendar, rules, catalogues. A world file names no cast member and holds no asset inventory. Its level-2 sections are free-form fact sections (`Facts`, or sections such as `Event stories` and `Support cards`) plus an optional `Connections`, `Contradictions` and `Provenance`, with the same table columns as a character sheet. The checker reads only Connections and Contradictions, and only when present. A name that appears only in a world file does not make a cast member.

The sheets contain nothing else. Distillation reads the sources only to settle the contradictions it lists. It adds no traits, no card entries and no reading beyond collation and those settlements.

## One home for a fact

The reference sheets are the home of every sourced fact. The card states the fact and the export derives it. A correction is made in the sheet first, then carried to every copy the card's ledger row lists. The stale-Body failure came from breaking this rule: the exported appearance was corrected, and the Body kept the old text.

## The coverage ledger

Every character note carries a `### Coverage ledger` subsection under `## Design Notes`. It is a table with the columns `Section | Entry | Claim | Source | Derived copies`, with one row per claim. An entry may hold several claims; each claim gets its own row:

- `Section` is one of `Background`, `Body`, `Soul`, `Relationships`, `Intimate Dynamics`, `Voice / Dialogue`, `Story Seeds`. Intimate Dynamics rows exist only when the note has that section.
- `Entry` is the entry's number, counted as `card-format.md` defines an entry for the section: a top-level bullet in Background, Body, Soul, Relationships and Intimate Dynamics; a labelled block in Story Seeds and Voice / Dialogue, which begins at a bullet, a bold title line or a `####` heading. Several claims in one entry are keyed `1.a`, `1.b`. The Body preamble is prose, so it is split into clauses: one clause is one sentence of the preamble, written `preamble 1`, `preamble 2` and so on. Write one sentence for each feature group (hair, eyes, skin, build, distinguishing features, clothing, hidden features) so each group gets its own row.
- `Claim` is the claim in a few words.
- `Source` lists the reference documents the claim came from, separated by `;`. Each is a path relative to `reference/` that stays inside `reference/`, optionally followed by `#` and a heading. A claim with no source is not written into the card. Its row stays in the ledger with `Entry` set to `unwritten` (`unwritten 1`, `unwritten 2` for several) and `Source` set to `flagged`, so the gap is visible. A flagged row for a claim that is written into the card is an error. The writer returns each flagged row to the human; it never passes silently. A claim the writer inferred from cited evidence is written into the card, and its `Source` cell reads `inferred:` followed by the sheet facts and the anime or manga addresses the claim rests on, all in that one cell. The cell contains no `|` character, because the ledger is a table. The checker accepts the row as a written claim and does not read the evidence as file paths. An `inferred:` cell with nothing after the colon is an error. The writer and the critic read the evidence. The `flagged` state keeps its meaning: the claim is unwritten.
- `Derived copies` lists the export fields that reproduce the fact (`appearance` from the Body preamble, `role` from occupations, `spriteSets[].description` from ownership and appearance), so a correction visits every copy. It is not machine-checked.

The ledger covers every section a card can have, taken from `worldbuilder-character/card-format.md`.

## The gap rule

When the reference sheets lack a fact the card needs, the writer does not guess. The writer follows these steps in order:

1. Re-read the sweep documents for the character.
2. Read the source itself for the character, fresh in the new context, for things the sweep overlooked. Record anything found in the sheet with its provenance.
3. If the fact is still missing, ask the human.

An inference rests on facts a reference document holds or scenes the anime or manga show, and is recorded as `inferred:` in the ledger. A claim with no evidence to rest on is a gap, and the gap rule applies. The writer never fills a gap from invention.

## The evidence readback

After a card is written, the writer re-reads every Background, Soul and Voice / Dialogue entry against the evidence its ledger row cites; an `inferred:` row is read back against the facts and addresses its cell names. The degree of each claim must be the degree the evidence shows. A word of extent or intensity (always, never, expert, obsessive, scientific, savant) stands only where the cited lines show it. An entry that outruns its evidence is rewritten down to the evidence, or returned to the human as a question. This is a reading of meaning. The writer does it as a self-check and the critic does it again. The checker script never does it.

## The cross-card pass

After a group of cards, check every Connections row against each card that carries it:

- A relationship may be one-sided: a card may name a cast member whose own card names it differently or not at all, and a missing entry on the other card is not a discrepancy.
- Where two cards name each other, ownership names the same owner on both cards.
- Where two cards name each other, sibling order, where both cards state it, is the same on both cards and is the order the Connections row states.
- Each character's occupations are complete against the sheet.

Fix every discrepancy in the cards, or return it to the human. The boundary is the cast as the sheets list it. A relationship that names a cast member who has no card yet must appear in the Connections table.

## The derived-output check

The export copies several facts out of the cards: `role`, `appearance`, and each `spriteSets[].description`. The check runs over an exported `world.json` and compares each of these with the sheets and the cards:

- `role` must contain every occupation the character's sheet lists, as a whole word or phrase (`art` is not found in `cartographer`).
- `appearance` must equal the card's Body preamble, ignoring whitespace. Identity is the exported `name` and `lastName` joined with a space, matched to the card and sheet through the name mapping above; an exported character that matches no card is reported.
- A `spriteSets[].description` must not name an owner other than the owners the Connections tables list, whether the name belongs to a cast member or not, and whether or not the tables list any owner. The check reads a name as an owner when the description writes `owned by <Name>`, `belongs to <Name>`, `pet of <Name>` or `companion of <Name>`, or `<Name>'s` followed by the character's own name or one of these pet words: pet, dog, cat, horse, chicken, bird, animal, companion, familiar, mount, puppy, kitten, goat, sheep, cow, pig, rabbit, duck, hen, rooster, donkey, llama, alpaca, fish, turtle, lizard, snake, ferret, hamster, mouse, rat. A name is every capitalised word in a row; a capital letter in any script counts. After `owned by` and the other phrases, a lowercase word counts as a name only when it matches a cast or Connections name, and `anyone`, `no one`, `nobody` and `someone` never count. An exported character with a card but no character sheet is reported.

Every difference is reported. The checker script (`scripts/check_coverage.py`, `export` mode) runs it. The export procedure runs it as its derived-output check (`worldbuilder-ainime-export/export-procedure.md`, section 6), after `world.json` is written and before the archive is built.

## The checker

`scripts/check_coverage.py` checks what a script can check. The writer runs its `world` mode at the end of each group of cards, after the cross-card pass, and fixes every FAIL line or returns it to the human before the group counts as done.

- `world` mode, over a world root: every character note has a ledger; every entry of every card section present (Intimate Dynamics included) and every Body preamble clause has a ledger row; every ledger row names an entry the note has; every named source exists under `reference/`, and flagged rows are listed apart, and `inferred:` rows are accepted as written claims; every Contradictions row of every sheet has two sources; every character note's ledger source stays inside `reference/`; no character sheet has two sets with identical hashes.
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
| Sibling order unstated | March's card said "his brother Olric" without the birth order that Olric's card stated. | The Connections table states the order; the cross-card pass checks that no card contradicts it. |
| Details not derivable from the source | Unsourced details stood in cards: capes in every season, a cabin in the Narrows, a fireplace habit, an invented scene. | The claim-level ledger with flagged rows; the gap rule when the sheet lacks the fact. |
