Work item: Worldbuilder export rework. Objective: carry the export lessons of the Fields of Mistria work into the worldbuilder-ainime-export skill, so every Ainime project exports by one consistent method.

Acceptance criteria (verbatim from the Specification):
1. The Expression Standard (sprite expression tiers) and the Export Procedure Standard (pre-flight check, field map, dead-content detection, adjustment order) are carried into the export skill or its references, from `Projects/Ainime/Fields of Mistria/repo/Fields-of-Mistria/`.
2. The Export Procedure Standard's pre-flight checks are revised or dropped where they fail against the live Fields of Mistria export: a non-empty lastName for every character; every sprite set carrying all 28 availableExpressions; trigger days within one calendar year; no duplicate non-recurring trigger days; recurring triggers within one season. The clothing-rules check is kept.
3. The six mismatches between the export skill and its companions are resolved, each checked against a real .sbworld export: card prose versus headings (target-system.md versus card-assembly.md); Future Storylines optional versus required; artStyle.timeOfDayLighting versus the export's artStyle.background.time_contexts; locations[] versus an object keyed by segment; "six system moods" listing three; notes/ versus the concepts/, events/, story/ and characters/ source folders.
4. Appearance and image-generation fields for long-lived races state the age the character appears to be, never the real age.
5. One standard .sbworld rebuild method serves every Ainime project: world.json, manifest.json and an assets folder packed into the archive.
6. The baseProfile drift is settled: either the card-to-export reconciliation is part of the export procedure, or baseProfile is derived from the cards. The item records which, and why.
7. One background rule for sprite sets is stated in the Expression Standard and never restated in presets or prompt files. (Settled: binds the plugin's own files only.)
8. The plugin's tests and CI pass on the merged change.
9. The derived-output check (`check_coverage.py export`) runs in the export procedure after world.json is written and before the archive is built, only when the world has a reference sheet; a failure blocks the build.

Further binding decisions: the plugin's expression-standard.md is the single source of truth for the expression tiers. Plugin files must not cite paths in the author's private vault (they do not exist on machines receiving the plugin). Out of scope: the foundation rename of the export's input file; the sex property; any change to the Fields of Mistria repository.

The approach, pre-agreed seams and per-criterion verification list are in .scraibe/review/plan.md (reference only). The constraint document is .scraibe/review/constraint-ainime-export-skill-update.md.

Report the Specification check as an explicit split: Missing (asked for, not delivered or partial) and Extra (built without being asked); answer both halves, stating "none" where empty. Apply the repo's documented standards, and the Fowler smell baseline as labelled judgement calls only.

Do all of this review yourself. Never spawn a subagent to review part of the scope, and never spawn another reviewer for a second opinion. This process already provides every review seat the work gets. If the scope feels too large for one pass, review it in passes yourself and say so in your report.
