# Creative Step

*Shared by the six entity skills: `worldbuilder-character`, `worldbuilder-location`, `worldbuilder-faction`, `worldbuilder-event`, `worldbuilder-concept` and `worldbuilder-story`. All prose a creative step produces follows `writing-style.md`. Read it before writing.*

A worldbuilder entity item is a tracked item with three middle steps: a creative step, a critic step and a creative revision step. The entity skill is the creative role's instructions. This file says how a creative step starts, how it ends, and how the revision step uses the critic's report. The entity skill says what the notes contain.

The interview does not happen in the creative step. The definer ran it before the item's Specification was approved, and the Specification holds the answers. The interview questions for each entity live in the entity skill's `## Interview` section, which the definer reads.

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

- For each finding whose **Class** is `auto-fix`, replace the **Quoted text** in the entity note with the **Repair text**, exactly as written, without asking. If the **Quoted text** no longer matches the note, return the finding as a question.
- For each finding whose **Class** is `escalate`, change nothing. Return the finding as a question for the human: the **Rule**, the **Quoted text**, the reason it escalated, and the proposed repair when the critic offered one. The orchestrator puts these questions on the answer page. When the human answers, apply the answer.
- Return the list of changes made, so the human sees every change at the item's final review.

## Spin-offs

Every creative step ends by proposing spin-offs: a home, an implied faction, a lore entry, or any other idea the work surfaced that is not part of this item. Do not write the spin-off. Do not create a note for it. Return each proposal with three parts:

- **Idea** — one sentence naming the spin-off.
- **Context** — what in this item implies it, with the paths of the entity notes that mention it.
- **Extends** — the existing seed note on the same idea, if one exists; otherwise "none".

The orchestrator writes each proposal as a seed note in the world's Anima domain folder, or adds it to the existing seed note it extends. A seed note is a tracking note. It is not the world's seed document, `project/seed.md`.

## Hand on

The creative step ends by returning: the paths of the notes it wrote or changed, any questions, and the spin-off proposals. After the first creative step, the critic step runs next (`worldbuilder-review`). After the revision step, the item goes to its final review.
