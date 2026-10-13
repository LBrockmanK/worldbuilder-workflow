# Creative Step

*Shared by the six entity skills: `worldbuilder-character`, `worldbuilder-location`, `worldbuilder-faction`, `worldbuilder-event`, `worldbuilder-concept` and `worldbuilder-story`. All prose a creative step produces follows `writing-style.md`. Read it before writing.*

A worldbuilder entity item is a tracked item with three middle steps: a creative step, a critic step and a creative revision step. The entity skill is the creative role's instructions. This file says how a creative step starts, how it ends, and how the revision step uses the critic's report. The entity skill says what the notes contain.

This file covers the entity notes of an entity item only. The Foundation item's documents (the foundation document and `project/direction.md`) are written by that item's builder, outside the creative step.

The interview does not happen in the creative step. The definer ran it in rounds on the answer page before the item's Specification was approved, and the Specification holds the answers. The interview questions for each entity live in the entity skill's `## Interview` section, which the definer reads. `## What every entity note shares` below holds the rules that apply to every entity note and every interview; the entity skills cite it and do not restate it.

---

## How a creative step starts

1. Read the whole item: its Specification, its Work section and the entity notes written so far.
2. Take the interview answers from the Specification. Do not ask the human questions in the creative step. Source material named in the Specification replaces answers: extract the behavioral content from the material and translate it as you would translate an answer.
3. Read the governing format document for each entity type in the item and `writing-style.md`.
4. If the Specification leaves a point open that the notes cannot be written without, stop and return that point as a question. Do not guess.

## First creative step

Write the entity notes of the item. The notes are the item's outputs. Write them into the world's `repo/`, in the folder the project layout gives their type, and return their paths for the item's callout. Write nothing else: the item's entity notes are the only files a creative step creates.

## Revision step

The revision step reads the critic's report. The report is the section named `## Critic report` in the critic's callout (see `worldbuilder-review`). Every finding in it carries four fields: **Rule**, **Quoted text**, **Class** and **Repair text**.

- For each finding whose **Class** is `auto-fix`, replace the **Quoted text** in the entity note with the **Repair text**, exactly as written, without asking. If the **Quoted text** no longer matches the note, return the finding as a question. A **Quoted text** that begins `ABSENT:` names a missing entry or section, not text to replace; it normally has **Class** `escalate`. If one is classed `auto-fix`, insert the **Repair text** under the named heading.
- For each finding whose **Class** is `escalate`, change nothing. Return the finding as a question for the human: the **Rule**, the **Quoted text**, the reason it escalated, and the proposed repair when the critic offered one. The orchestrator puts these questions on the answer page. When the human answers, apply the answer.
- Return the list of changes made, so the human sees every change at the item's final review.

## Spin-offs

Every creative step ends by proposing spin-offs: a home, an implied faction, a lore entry, or any other idea the work surfaced that is not part of this item. Do not write the spin-off. Do not create a note for it. Return each proposal with three parts:

- **Idea** — one sentence naming the spin-off.
- **Context** — what in this item implies it, with the paths of the entity notes that mention it.
- **Extends** — the existing seed note on the same idea, if one exists; otherwise "none".

The orchestrator writes each proposal as a seed note in the world's Anima domain folder, or adds it to the existing seed note it extends.

## Hand on

The creative step ends by returning: the paths of the notes it wrote or changed, any questions, and the spin-off proposals. After the first creative step, the critic step runs next: `worldbuilder-review` with the entity notes, each note's governing format document and all reference material used. The revision step applies the auto-fix findings, and escalated findings go to the human. After the revision step, the item goes to its final review.

---

## What every entity note shares

Each rule in this section is stated here once. The entity skills cite it by heading.

### Interview

The definer asks one question at a time and waits for the answer. Follow threads: when an answer implies something about a different section, surface it and pursue it before changing topics. The human can override at any point: answer, skip questions, write entries directly, or provide source material in place of answers. The definer's rounds run on the answer page, and the human's answers go into the item's Specification.

An interview opens with the question that decides which optional parts of the note apply, then asks per-section questions in the note's writing order. A question asks and does not restate the rule it serves; the rule lives in the format document.

### Frontmatter and filename

The plugin's type roster defines the frontmatter and the generated templates stamp it at creation (scraibe's `new_doc.py` creates the note). The script produces a date-prefixed filename. Rename the fresh note to the entity's own name before adding content: that is the filename convention the templates state, and it is safe while nothing links to the note yet.

### Design Notes

Design Notes is the builder record. It is excluded from all exports and from review. It has two subsections:

- **Session Notes:** the interview capture, taken from the Specification: what the human said they wanted this note to be. Written before the body is drafted. Raw intent, plain language, bullet points. A future agent that revisits the note reads Session Notes first.
- **Builder Context:** narrative function, inspirations and what is drawn from each, design decisions, open questions. Bullet points. Leave it blank when nothing is worth capturing. Do not pad.

The entity skill's format document names what Builder Context holds for that type.

### Required entries and waivers

A format document's required entries are the entries or tests its type treats as mandatory. A note is not finalized until each required entry is present or the item's Specification waives it with a recorded reason.

### Closure

The note is open until it carries a closure tag. Mark it `complete` when the entity skill's self-check passes (`../CONTEXT.md`, Status lifecycle).
