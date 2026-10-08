---
name: worldbuilder-review
description: Use when a worldbuilder document is drafted and needs adversarial review against its governing format document before it is treated as complete.
---

# Worldbuilder Review

Governed by the spec "2026-08-15-worldbuilder-document-review-gate" in the Anima vault's worldbuilder-workflow domain.

*All prose this skill produces follows `../writing-style.md`. Read it before writing.*

## Inputs

- **Document to review** (required) — path to the worldbuilder document.
- **Governing format document** (required) — path to the format doc (e.g., `card-format.md`).
- **Reference material** (required when the document was produced from Q&A or source ingestion; omitted only when no source material exists) — paths to source documents (behavioral evidence, data profiles, Q&A transcripts, or equivalent).

---

## Process

### Phase 1: Read review criteria

Open the format document's `## Review criteria` section. If it exists, use its Checks, Exempt, and Judgment calls as the review brief. If it does not exist, use the full format document as acceptance criteria — including the format document's own section-scoped rules and exemptions — but without additional review-specific exemptions or judgment-call guidance.

### Phase 2: Review

Read each entry in the document. For each entry, check it against every applicable rule from the Checks list (section-scoped checks filtered by which section the entry belongs to; document-level checks applied across the whole document). Also check against `docs/slop-phrases.md` and `../writing-style.md`. Record each finding with: the rule violated (by name and location in the format doc or shared resource), the entry text, and the specific violation.

### Phase 3: Classify findings

For each finding, apply the two-part test:

1. **Is the violation clear?** The rule text unambiguously matches the entry.
2. **Is the repair safe?** The fix requires only mechanical restructuring (splitting sentences, removing a word, reformatting a bullet to prose) without changing semantic content. Tense changes are not inherently safe — changing past to present can turn a historical event into an ongoing behavior.

Auto-fix applies only when both are true. If either is ambiguous — the rule application is debatable, the repair requires new behavioral content, sourcing from reference material, or a characterization choice — the finding escalates. Check the Judgment calls section of the review criteria for format-specific classification guidance.

### Phase 4: Apply auto-fixes

For each auto-fix finding, rewrite the entry to comply with the rule. Preserve semantic content. When reference material is provided, verify the fix preserves semantic fidelity to the source data. If a fix would require inventing detail not in the source, reclassify as escalated. Check exempt content types before fixing — do not modify exempt sections or content.

### Phase 5: Generate report

Produce a completion report with three sections:

- **Auto-fixed** — for each: rule cited (name and location), before text, after text.
- **Escalated** — for each: rule cited, entry text, why it is ambiguous (which part of the two-part test failed), and a proposed repair when one can be offered without a characterization choice.
- **Scoped out** — for each: rule name, exemption cited (from the Exempt list).

---

## Presenting results

Present the report to the user. The user reviews the diff (this is the quality check on auto-fixes). The user can revert any auto-fix. Each escalated finding requires resolution before the document is marked complete:

- **Fix** — write and apply a repair (the user or agent creates the fix, using the proposed repair as a starting point when one was offered).
- **Reject** — the finding is invalid (record reason).
- **Defer** — acknowledged, not addressing now (record reason).

A second review pass is warranted only when fixes rewrote the document substantially enough that the user would otherwise approve materially unreviewed text.
