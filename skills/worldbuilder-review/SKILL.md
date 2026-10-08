---
name: worldbuilder-review
description: Use when the critic step of a worldbuilder entity item checks drafted entity notes against their governing format document and sorts each finding into auto-fix or escalate.
---

# Worldbuilder Review

This skill is the critic's instructions. The critic is the checking step of a worldbuilder entity item. Governed by the spec "2026-08-15-worldbuilder-document-review-gate" in the Anima vault's worldbuilder-workflow domain.

*All prose this skill produces follows `../writing-style.md`. Read it before writing.*

## How the critic runs

The critic runs read-only on Sol through the codex CLI: `codex exec --sandbox read-only`, as the fleet plugin's codex document describes. It never changes a file. The orchestrator records the critic's report as the critic's callout in the entity item. The creative revision step reads that report and applies it (see `../creative-step.md`).

## Inputs

- **Document to review** (required) — path to the worldbuilder document.
- **Governing format document** (required) — path to the format doc (e.g., `card-format.md`).
- **Reference material** (required when the document was produced from Q&A or source ingestion; omitted only when no source material exists) — paths to source documents (behavioral evidence, data profiles, Q&A transcripts, or equivalent), or the item's Specification when it holds the interview answers.

---

## Process

### Phase 1: Read review criteria

Open the format document's `## Review criteria` section. If it exists, use its Checks, Exempt, and Judgment calls as the review brief. If it does not exist, use the full format document as acceptance criteria — including the format document's own section-scoped rules and exemptions — but without additional review-specific exemptions or judgment-call guidance.

### Phase 2: Review

Read each entry in the document. For each entry, check it against every applicable rule from the Checks list (section-scoped checks filtered by which section the entry belongs to; document-level checks applied across the whole document). Also check against `docs/slop-phrases.md` and `../writing-style.md`. Record each finding with: the rule violated (by name and location in the format doc or shared resource), the entry text, and the specific violation.

### Phase 3: Classify findings

For each finding, apply the two-part test:

1. **Is the violation clear?** The rule text unambiguously matches the entry.
2. **Is the repair mechanical?** The fix requires only mechanical restructuring (splitting sentences, removing a word, reformatting a bullet to prose) without changing semantic content. Tense changes are not inherently safe — changing past to present can turn a historical event into an ongoing behavior.

A finding is `auto-fix` only when both are true. If either is ambiguous — the rule application is debatable, the repair requires new behavioral content, sourcing from reference material, or a characterization choice — the finding is `escalate`. Check the Judgment calls section of the review criteria for format-specific classification guidance. Check exempt content types before classifying — exempt sections and content produce no finding.

When reference material is provided, an `auto-fix` repair must preserve semantic fidelity to the source data. If a repair would need detail the source does not hold, classify the finding as `escalate`.

### Phase 4: Write the report

The report has one section named `## Critic report`. It is a numbered list of findings, and every finding carries exactly these fields, with these labels:

- **Rule** — the rule violated, by name and location.
- **Quoted text** — the entry text, copied word for word.
- **Class** — `auto-fix` or `escalate`.
- **Repair text** — for an `auto-fix`: the exact replacement text for the quoted text, ready to paste. For an `escalate`: the reason the finding failed the two-part test (which part), and a proposed repair when one can be offered without a characterization choice.

After the `## Critic report` section, a `## Scoped out` section lists, for each exempt item, the rule name and the exemption cited. A report with no findings says so under `## Critic report`.

---

## Using the report

The critic does not resolve findings. The creative revision step applies every `auto-fix` finding without asking. The orchestrator puts every `escalate` finding to the human as a question of the revision step. The human sees every change at the item's final review.

## Review

None here — this skill is the critic and produces reviews rather than deliverables; no deliverable checks off at this skill.
