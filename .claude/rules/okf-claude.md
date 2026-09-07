---
paths:
  - ".claude/**"
---

# Scraibe Vault Rules

Files in `.claude/` are OKF knowledge documents (enforcement level: full).

## Universal frontmatter properties

- `type` (text, required)
- `title` (text, required)
- `description` (text, required)
- `tags` (tags, required)
- `created` (date-link, required) — the birth date, machine-stamped at creation as `created: "[[YYYY-MM-DD]]"`
- `modified` (datetime) — maintained automatically by the frontmatter-modified-date plugin; never written by hand, and not required at creation
- `resources` (list, required)
- `output` (list, optional)
- `superseded-by` (list, optional)

Field types: `text`, `number`, `checkbox` (boolean), `date`, `datetime`, `list`, `tags`.

## Types

- **adr**
- **grilling**
- **plan**
- **reference**
- **reflection**
- **research** — Planned investigation of external material: goals, gathered results, consolidation
- **review** — Adversarial review record for one plan or one ad-hoc review: rounds with adjudications, in dispatch order, final pass last
- **spec**

## Status tags (exactly one, in `tags`)

Open: `human-ready`, `agent-ready`
Closed: `complete`, `deprecated`, `abandoned`, `archived`
Behavioral: `priority`, `deferred`

## Reserved names

- `index.md` — auto-generated directory listing. Never hand-edit.
- `log.md` — recognized but unused.
- `inbox.md` — capture buffer, no frontmatter.
- `rules/` (directory) — generated rule files, exempt from vault schema. Never hand-edit; regenerate with generate_rules.py.
- `_templates/` (directory) — generated Templater creation templates, exempt
  from vault schema. Never hand-edit; regenerate with generate_templates.py.
- `_bases/` (directory) — generated Obsidian Bases views, exempt from vault
  schema. Core views are regenerated with generate_bases.py and must not be
  hand-edited; project-specific `.base` files with other names may live here.

## Links

- In document bodies, use relative markdown links (`[title](../specs/target.md)`).
- In frontmatter, any value in wikilink form (`[[filename-stem]]`) is a link edge — on any field, not just `output`/`superseded-by`. Bare names are plain text.
- Illustrative or example links belong in backticks or fenced code blocks — code is excluded from link validation.

## Lifecycle conventions

- **Document creation:** create vault documents with the scraibe plugin's `new_doc.py` — never hand-assemble frontmatter.
- **Write-side linking:** after creating a document or adding substantial body content, run the scraibe plugin's `link_notes.py` on it (forward, then `--reverse`) and review the inserted links — verify the matches and catch references the inventory missed (aliases, indirect phrasings). Ambiguous terms are skipped and reported, not guessed.
- **Renames and moves:** never rename or relocate a vault document by hand — use `rename_doc.py` (`--title` to retitle, `--dest` to move), which renames/moves the file, updates the title, rewrites inbound links (body paths and frontmatter wikilinks), and regenerates the affected directory indexes.
- **Promotion:** when a conversation reaches a design or decision worth keeping, offer to synthesize it into the appropriate doc type via `new_doc.py`. Graduation leaves a link behind: the originating line becomes a link to the new document. Exception: inbox lines are deleted — the document is the graduation.
- **Status transitions:** closing statuses (`complete`, `deprecated`, `abandoned`, `archived`) — propose in the same turn the work finishes; the user confirms (an explicit instruction counts). Never leave a flip for a later audit to find. Open transitions and behavioral tags — apply autonomously and announce.
- **Supersession is mechanical:** when writing `superseded-by` into a document, set that document's status to `deprecated` in the same edit.
- **Session close-out:** when finishing a work session, update the governing document (checkboxes, state, status tag) and flush deferrals to the inbox. No separate handoff documents.

## Presenting for review

- Reviewable content (designs, proposals, decisions) must be written to a vault document before asking for approval — link the file in the ask, not inline text.
- Place the review material and the approval question in the final message block of your turn — mid-turn text can collapse unseen in the desktop app.
- Explain each decision in full sentences in the ask — do not compress the reasoning into one-line option chips.
- Never link a file that is not on disk yet.

## Consuming the vault

- Start at `index.md` and follow links — progressive disclosure, not bulk reading.
- Tolerate incompleteness: open documents are working state, not finished prose.
- Reading creates an obligation: if a document you read is stale or wrong, fix it in place or capture one line to `.claude/inbox.md`.

## Implicit mode

- When creating or editing any document here, apply the type template and populate all required universal properties immediately — do not wait for validation.
- When deferring work or noting something for later, append one line to `.claude/inbox.md` now (`- <YYYY-MM-DDTHH:MM>: <item>`) and move on.
