# voiceover-manifest

## Role

Plan the narration package from the approved script and produce the voiceover artifacts required for the selected delivery tier.

## Required outputs

- When the frozen delivery tier requires narration, a beat-keyed `voiceover.md` plan.
- When the frozen delivery tier requires narration, a `narration_manifest.json` aligned to the same beat structure.
- When the frozen delivery tier is `final narrated delivery`, viewer-usable audio assets aligned to `voiceover.md` and `narration_manifest.json`.
- Language defaults, delivery-tier expectations, and pacing notes for narration work only when narration is required.
- A blocker note when narration planning cannot proceed without upstream repair.

## Rules

- Default to English voiceover only when the frozen delivery tier requires narration and the language remains unspecified.
- Keep `voiceover.md` and `narration_manifest.json` aligned to the approved script's beat structure and the confirmed brief's semantics.
- Keep the spoken language aligned to the approved brief; do not drift back to English when another narration language was explicitly approved.
- Match the selected delivery tier; do not silently upgrade, downgrade, or add narration obligations.
- For `no narration`, rely on the approved `pre_build_brief.md` no-narration decision and do not create voiceover artifacts.
- Keep optional overlays opt-in. Narration planning must not add overlay requirements by implication.
- Record timing and pacing assumptions only to support render and QA, not to rewrite script structure.

## Fail conditions

- Introducing semantics that do not exist in the brief or script.
- Changing language defaults, delivery tier, or overlay expectations without approval.
- Requiring narration artifacts for `no narration`.
- Reaching `final narrated delivery` without viewer-usable audio assets.
- Writing timing expectations that contradict the approved beat structure.
- Using narration planning to paper over a script or brief defect.

## Rollback rule

- If the issue is wording, pacing, or manifest structure within the same approved script, repair it inside `VOICEOVER`.
- If the issue comes from script structure or beat organization, return to `SCRIPT`.
- If the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork, return to `DESIGN_DEVELOPMENT`; require design repair, review, and reapproval, then brief regeneration and reapproval.
- If the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion, return to `CONTRACT` for brief repair and reapproval without redesign.
