---
name: algorithm-teaching-animation-v3
description: Use when an algorithm request must become a complete Manim teaching animation through design, review, rendering, and QA; not for pure-text algorithm explanations, general non-algorithm animations, or requests limited to local edits of an existing scene.
---

# Algorithm Teaching Animation v3

## Overview
This skill turns a user's algorithm request into a complete Manim teaching animation. The workflow covers animation design, teaching-script writing, optional voiceover production, animation implementation, independent review, QA, and delivery.
The orchestrator must ensure that every step is completed in order and that every phase satisfies its requirements.

## Required Authorization
Using this skill to complete the workflow requires the user's approval to use subagents.
If explicit authorization has not already been obtained in the current conversation, ask verbatim:

```text
This task requires subagents: `animation-designer` for animation design, `animation-design-reviewer` for independent animation-design review, and downstream roles for content writing, review, voiceover production, animation implementation, and quality verification. Do you agree to my using subagents for this task? Please answer explicitly with "I agree" or "I do not agree" (if you do not agree, this task cannot begin).
```

Begin subsequent work only if the user explicitly answers `I agree`.
If the user answers `I do not agree`, refuses authorization, or does not explicitly agree, stop immediately and do not begin any subsequent phase.

## Workflow
Run these phases in order:

1. `ANIMATION_DESIGN`
2. `SCRIPT`
3. `VOICEOVER`
4. `RENDER`
5. `QA`
6. `DELIVERY`

Do not skip any phase.
Before starting a phase, confirm that all prerequisites listed for that phase are complete.
Read only the references required by the current phase. Do not read later-phase material early unless a problem occurs and a rule explicitly requires it.
If a later phase reveals that an earlier decision is unclear, wrong, or missing required information, do not patch it in the current phase. Return to the phase that owns the problem, repair it there, and then continue in order.

## Delegation Rules
When a phase requires a specific subagent, that subagent must perform the specified work.
Delegation does not transfer the orchestrator's responsibility for phase order, required artifacts, pass conditions, or rollback routing. When a phase requires independent review, dispatch the named reviewer only after the artifact under review is complete, and the reviewer must not be that artifact's author.

Read required material according to each phase's `Read Before Acting` section.
The orchestrator reads additional references only when an artifact may be defective, a gate fails, or the proper rollback target is unclear.

## Artifact Chain
The normal workflow produces these artifacts in order:

```text
intake_summary.md
animation_design.md
animation_design_review.md
pre_build_brief.md
teaching_script.md
script_review_result.md
voiceover.md
narration_manifest.json
audio/voiceover/
generated_algo_scene.py
render_preflight.md
scene_review_result.md
qa_result.md
```

For the `no narration` delivery tier, the approved `pre_build_brief.md` must explicitly state that narration and voiceover files are not required.
In this tier, `voiceover.md`, `narration_manifest.json`, and files under `audio/voiceover/` are not required.

For the `final narrated delivery` tier, `voiceover.md`, `narration_manifest.json`, and usable narration audio under `audio/voiceover/` must be complete before render and QA can pass.

## Global Rules
These rules apply throughout the workflow:

- This file, `SKILL.md`, is the primary English workflow contract.
- `references/*.md` provide phase-specific execution detail, and `agents/*.md` define role-specific behavior. Neither may override or change this contract.
- `SKILL.md` and `SKILL.zh-TW.md` must remain semantically synchronized.
- A missed supporting-file read, delegated work, successful render, or informal review opinion never permits skipping a phase, artifact, or formal gate required by this contract.
- Do not add explanatory overlays, code panels, or on-screen annotation layers outside the contract unless the user explicitly requests them.
- Every review and QA decision must use the formal gate artifact named by its phase.
- If downstream work discovers inaccurate capture of user source material, roll back to `INTAKE`. If it discovers a gap in core semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, or another core design decision, roll back to `DESIGN_DEVELOPMENT` and repeat review and approval. If the problem is limited to brief wording, source labels, or faithful conversion, roll back to `CONTRACT`. Use `ANIMATION_DESIGN` only when referring to the entire first top-level phase.

## Phase 1: ANIMATION_DESIGN

### Goal
First capture the user's source material accurately, then complete the teaching and visual design, independent review, external approval of an exact version, and faithful conversion into the downstream implementation contract.
Before script, voiceover, or scene production begins, only this phase may define or change core semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, or high-level animation beats.

### Delegation
The orchestrator owns `INTAKE`, user-facing one-at-a-time questions, faithful recording of answers, and every external approval gate.
Dispatch `animation-designer` for `DESIGN_DEVELOPMENT`, creation or revision of `animation_design.md`, and, after exact-version design approval, faithful conversion during `CONTRACT`.
After the designer produces `DESIGN_READY`, separately dispatch an independent `animation-design-reviewer`. The reviewer must not have participated in writing, revising, or repairing that design version.

### Read Before Acting
Before `INTAKE`, the orchestrator reads `references/intake-contract.md`.
Before `DESIGN_DEVELOPMENT`, `animation-designer` reads `references/high-impact-clarification.md`, the common design reference, the visual reference, and exactly one matching type reference when the algorithm type matches, as required by its role contract.
Before design review, `animation-design-reviewer` reads `references/animation-design-review-checklist.md` and follows the same reference routing as the designer.
Before `CONTRACT`, `animation-designer` reads `references/pre-build-brief.md`.
Do not read later-phase references early merely because they might be useful.

### Subphase 1: INTAKE
The orchestrator accurately captures the algorithm, version or scenario, sample input, target audience, teaching goals, animation requirements, delivery tier, constraints, prohibitions, and prior decisions supplied by the user. Preserve original wording and source labels that affect semantics, teaching, delivery, or acceptance.
Create `intake_summary.md` according to `references/intake-contract.md`, clearly separating user-sourced material from agent analysis.
`INTAKE` only records, classifies, and offers non-binding candidate teaching directions. It must not complete the animation design or freeze core visual semantics, scene structure, information hierarchy, teaching arc, or high-level beats.

### Subphase 2: DESIGN_DEVELOPMENT
Dispatch `animation-designer` to plan small batches of closely related core questions and to perform the actual algorithm-animation design. At minimum, the design covers the algorithm version and operational semantics, teaching goals, audience misconceptions to prevent, the primary mental model and its boundaries, the example and its teaching rationale, the core visual metaphor and stable visual semantics, data-structure representation, scene structure, information hierarchy, teaching arc, high-level animation beats, and explicit recommendations, rationales, meaningful alternatives, and tradeoffs.

The orchestrator asks the user only one question at a time, faithfully records and forwards each answer, and does not design the question list or the animation. The designer's recommendation must not replace a user decision. After the entire batch is answered, return the complete batch to `animation-designer` in one faithful consolidated handoff; do not ask the designer to update after each individual answer.
Continue with another small batch while any blocking question could materially change algorithm semantics, the primary mental model, core visual semantics, teaching arc, scene structure, or high-level beats. Low-impact details must not block design; apply a reasonable best-effort default, record the risk, and continue.

`animation-designer` creates `animation_design.md` according to `references/animation-design-document.md`, performs the specified `DESIGN_READY` self-check, and may emit `DESIGN_READY` only when every condition passes and no blocking core question remains.
Then dispatch the independent `animation-design-reviewer`, who creates the sole formal review artifact, `animation_design_review.md`. The review must build a complete evidence matrix against the `DESIGN_READY` conditions specified in `references/animation-design-process.md` and use either `Full` or fully traceable `Delta` routing according to change impact. The initial review, and any change to algorithm semantics, the primary mental model, the core visual metaphor or semantics, teaching arc, scene structure, high-level beats, or a change whose impact is unclear, requires `Full` review.

The reviewer must compute SHA-256 over the exact bytes of the actual `animation_design.md` under review both when review begins and immediately before review ends, and record `Reviewed Design SHA-256` in a `PASS` result. Only after `animation_design_review.md = PASS` may the orchestrator request explicit user approval of that exact reviewed version. The approval record must be stored outside `animation_design.md` and preserve `Approved Design SHA-256` plus an explicit reference to the user's approval.
The user may directly edit `animation_design.md`. Every direct edit creates a new version, invalidates prior review and approval, and triggers `Full` or `Delta` re-review according to change impact. Any existing `pre_build_brief.md`, its `Source Design SHA-256` lineage, and its approval are also invalidated. Every new version must return to `DESIGN_DEVELOPMENT`, undergo the impact-appropriate full or delta review, receive `PASS`, receive the user's renewed explicit approval, and then have `pre_build_brief.md` regenerated with new external lineage and separately reapproved. Silence, no response, the edit itself, or approval of another version does not count as approval.

### Subphase 3: CONTRACT
Dispatch `animation-designer` to convert the design faithfully into `pre_build_brief.md` only when the exact current `animation_design.md` version has received `PASS` from independent review, the user has explicitly approved the same version, and all of these values converge exactly:

```text
Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

`Source Design SHA-256` is not required before conversion. During faithful conversion, record it in the external `CONTRACT` lineage record as the exact current `Approved Design SHA-256` used to produce `pre_build_brief.md`; do not write lineage or approval metadata into `animation_design.md` or `pre_build_brief.md`.
The conversion may organize, condense, and label the sources of approved decisions, but it must not add, repair, or silently decide any core semantics, mental model, core visual semantics, scene structure, teaching arc, or high-level beat.
After conversion and before requesting brief approval, recompute the current design SHA-256 and require `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`. Then the orchestrator must separately request the user's explicit approval of the exact `pre_build_brief.md` version. Design approval cannot substitute for brief approval. The external approval record must preserve `Approved Brief SHA-256` and an explicit reference to the user's approval; do not write approval status or metadata into the brief.
Every edit to `pre_build_brief.md` invalidates prior approval. Recheck faithful conversion and obtain explicit approval of the new version. Immediately before starting `SCRIPT`, recompute SHA-256 for the current design and brief and require:

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
Approved Brief SHA-256 = current pre_build_brief.md SHA-256
```

### Required Outputs
Create:

- `intake_summary.md`
- `animation_design.md`
- `animation_design_review.md`, produced by the independent reviewer with verdict `PASS`
- `pre_build_brief.md`

### Pass / Exit Gate
Leave `ANIMATION_DESIGN` and begin `SCRIPT` only when every condition below is true:

- `intake_summary.md` exists and accurately preserves user-sourced material.
- `animation_design.md` exists and has emitted `DESIGN_READY`.
- `animation_design_review.md = PASS` and was produced by the independent `animation-design-reviewer`.
- `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`.
- The user has explicitly approved the exact reviewed design version in an external record.
- `pre_build_brief.md` exists and is a faithful conversion of that approved design.
- `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.
- The user has separately and explicitly approved that exact brief version in an external record.

Informal reviewer comments, verbal opinions in chat, or the orchestrator's own check cannot replace file-backed `animation_design_review.md = PASS`.

### Rollback Rules
If intake captured source material inaccurately, omitted original user wording, or assigned an incorrect source label, return to `INTAKE`, repair `intake_summary.md`, and feed the corrected source back through the design process.
If there is any gap in core algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, or another core design decision, or if `animation_design.md` changes in any way, return to `DESIGN_DEVELOPMENT`. After repair, repeat `DESIGN_READY`, the appropriate full or delta independent review, file-backed `PASS`, SHA-256 convergence, and exact-version user reapproval. The existing `pre_build_brief.md`, its `Source Design SHA-256` lineage, and its approval are invalid; regenerate the brief with new external lineage and separately reapprove it.
If the problem is limited to brief wording, formatting, source labels, or faithful conversion without changing the meaning of the approved design, stay in or return to `CONTRACT`. Recheck faithful conversion, update `Source Design SHA-256`, and obtain approval for the new SHA-256 of `pre_build_brief.md`.
If `CONTRACT` reveals a missing, conflicting, or materially ambiguous core decision, stop conversion and return to `DESIGN_DEVELOPMENT`. Do not perform design work in the brief.

## Phase 2: SCRIPT

### Goal
Organize the approved `pre_build_brief.md` into teachable animation beats and content order.

### Do Not Start Until
An approved `pre_build_brief.md` exists.
Immediately before starting this phase, recompute SHA-256 for the current design and brief and confirm `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` and `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`, with an external record of explicit approval for that exact `pre_build_brief.md` version.

### Do
Dispatch the `script-writer` subagent to create the teaching script.
Require `script-writer` to read the approved `pre_build_brief.md` and `references/teaching-script.md` before writing.
Then have `script-writer` produce a reviewable teaching script from the approved brief.
The script must make viewer goals, beat order, teaching focus, and content progression explicit without adding meaning absent from the contract.
After `teaching_script.md` exists, dispatch the independent `script-reviewer` subagent to review it against the approved `pre_build_brief.md`.
Require `script-reviewer` to read the approved `pre_build_brief.md`, `teaching_script.md`, and `references/script-review-checklist.md` before reviewing.
The script reviewer must not have written the script.

### Required Outputs
Create `teaching_script.md`.
Provide enough review context for `script-reviewer` to evaluate the script against the approved `pre_build_brief.md`.
Create `script_review_result.md` through the independent reviewer.

### Pass / Exit Gate
Advance only when `teaching_script.md` exists and `script_review_result.md = PASS`.
The review result must be produced by `script-reviewer`, not `script-writer`.

### Rollback When Problems Occur
If the problem is limited to script content order, expression, or adherence to the brief, return to `SCRIPT`.
If the script reveals an error in brief wording, source labels, or faithful conversion, return to `CONTRACT`, repair it, and regain exact-version brief approval.
If the script reveals a gap in core semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, or another core design decision, return to `DESIGN_DEVELOPMENT`; complete redesign, independent review, design reapproval, `CONTRACT` conversion, and separate `pre_build_brief.md` approval before continuing. Do not patch core design in `SCRIPT`.

## Phase 3: VOICEOVER

### Goal
Produce narration artifacts faithful to the approved `pre_build_brief.md` and the reviewed teaching script.
Voiceover is a formal workflow phase, not optional polish added at the end.

### Delegation
If the approved delivery tier includes narration, this phase must use the `voiceover-manifest` subagent.
This phase does not require a separate independent reviewer.

### Read Before Acting
The `voiceover-manifest` subagent must read the approved `pre_build_brief.md`, `teaching_script.md`, `script_review_result.md`, and `references/voiceover.md`.
If voiceover content appears inconsistent with the reviewed script, the orchestrator should read `script_review_result.md`.

### Do Not Start Until
The delivery tier is confirmed and no longer changing.
`teaching_script.md` exists.
`script_review_result.md = PASS`.
Immediately before starting this phase, recompute SHA-256 for the current design and brief and confirm `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` and `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.
If narration is required, do not use an unreviewed or failed script.

### Do
For `no narration`, verify that the approved `pre_build_brief.md` explicitly states that narration and voiceover files are not required.
Do not create purposeless voiceover placeholders merely to fill the artifact chain.

For `final narrated delivery`, dispatch `voiceover-manifest` to produce narration text, manifest data, and usable voiceover files that match the `pre_build_brief.md` and reviewed script.

### Required Outputs
For `no narration`, no additional voiceover artifacts are required.
For `final narrated delivery`, create `voiceover.md`, `narration_manifest.json`, and usable narration audio under `audio/voiceover/`.

### Pass / Exit Gate
For `no narration`, advance only when the approved `pre_build_brief.md` explicitly states that narration and voiceover files are not required.
For `final narrated delivery`, advance only when `voiceover.md`, `narration_manifest.json`, and usable narration audio are complete and ready for downstream render and QA.

### Rollback When Problems Occur
For narration wording or pacing changes, return to `VOICEOVER`.
For animation beat-structure mismatch, return to `SCRIPT`.
If the approved design clearly defines the delivery tier or narration obligations but the brief has a wording, source-label, or faithful-conversion error, return to `CONTRACT`, repair it, and regain exact-version brief approval.
If the delivery tier, core meaning, or teaching design itself is unresolved, conflicting, or incomplete, return to `DESIGN_DEVELOPMENT`; complete redesign, independent review, design reapproval, `CONTRACT` conversion, and separate `pre_build_brief.md` approval before continuing.

## Phase 4: RENDER

### Goal
Implement the approved `pre_build_brief.md`, reviewed script, and required voiceover material as scene code and render evidence.
This phase implements the approved contract and must not invent new content or meaning.

### Delegation
The `scene-writer` subagent must implement the scene and produce render evidence.
After `render_preflight.md` exists, dispatch the independent `scene-reviewer` subagent to review the scene.
The scene reviewer must not have written the scene.

### Read Before Acting
`scene-writer` must read:

- the approved `pre_build_brief.md`
- `teaching_script.md`
- `voiceover.md`, `narration_manifest.json`, and usable audio under `audio/voiceover/` when narration is required
- `references/manim-guidelines.md`
- `references/render-preflight.md`

The orchestrator reads `references/scene-review-checklist.md` or `script_review_result.md` only when render output may be defective, review cannot be routed successfully, or the correct rollback target is unclear.

### Do Not Start Until
`teaching_script.md` exists and `script_review_result.md = PASS`.
Immediately before starting this phase, recompute SHA-256 for the current design and brief and confirm `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` and `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.
For `no narration`, the approved `pre_build_brief.md` explicitly states that narration and voiceover files are not required.
For a delivery tier requiring narration, all required voiceover documents and usable audio exist.
This phase may begin only after explicit authorization to use subagents has been obtained.

### Do
Dispatch `scene-writer` to implement the Manim scene from the approved contract and reviewed script.
Unless the user explicitly requests otherwise, the scene must not add meaning, explanatory overlays, code panels, or annotation layers absent from the contract.
Produce the latest render and corresponding evidence.
Create `render_preflight.md` using evidence verifiably derived from the latest MP4.
Any rerender invalidates all prior latest-render evidence, `render_preflight.md`, and `scene_review_result.md`. Regenerate the evidence and preflight and obtain a new `PASS` from an independent `scene-reviewer` for that same latest MP4/version before `QA`.
Prepare scene-review handoff context, including code-to-render mapping, preflight evidence, and affected-frame information.
After `render_preflight.md` exists, dispatch `scene-reviewer` for independent review.
The first independent scene-review handoff for a scene/render is always `Full`.
Delta review is allowed only for bounded local `RENDER` changes with valid affected-frame evidence.
Affected-frame evidence is valid only while it remains applicable to the bounded change under review.
Return to full review when a repair changes approved semantics, script beat order, delivery tier, the approved contract, scene-wide structure, scene-wide layout, render mapping, or otherwise invalidates affected-frame evidence.
Treat broadened affected-frame scope or uncertain impact as invalidating affected-frame evidence and require full independent scene review.

### Required Outputs
Create:

- `generated_algo_scene.py`
- render evidence regenerated from the latest MP4
- `render_preflight.md`
- a code-to-render mapping or equivalent scene-review handoff context
- `scene_review_result.md` produced by the independent reviewer

### Pass / Exit Gate
Advance only when `generated_algo_scene.py`, latest-render evidence, and `render_preflight.md` exist and `scene_review_result.md = PASS`.
`scene_review_result.md` must be produced by `scene-reviewer`, not `scene-writer`.
A successful render, local self-check, or preflight does not mean the scene passed review.

### Rollback When Problems Occur
If the approved `pre_build_brief.md` and script are clear but the scene violates them in styling, spacing, timing, layout, or implementation content, return to `RENDER`.
If animation beats do not match, or the script is incomplete and forces the scene implementer to guess structure, sequence, or emphasis, return to `SCRIPT`.
If the approved design is clear but brief wording, source labels, or faithful conversion are incomplete, return to `CONTRACT`, repair it, and regain exact-version brief approval.
If a gap remains in core semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, or another core design decision, return to `DESIGN_DEVELOPMENT`; complete redesign, independent review, design reapproval, `CONTRACT` conversion, and separate `pre_build_brief.md` approval before continuing. Do not patch core design in `RENDER`.

## Phase 5: QA

### Goal
Have an independent reviewer verify that the output matches the approved `pre_build_brief.md`, reviewed script, chosen delivery tier, on-screen supplementary-information rules, and narration requirements.
QA verifies contract compliance and delivery readiness, not only whether the video plays.

### Delegation
This phase must use the independent `qa-verifier` subagent.
`qa-verifier` must not have contributed to the output under review.

### Read Before Acting
`qa-verifier` must read:

- the approved `pre_build_brief.md`
- `teaching_script.md`
- rendered media output
- `render_preflight.md`
- `scene_review_result.md`
- `voiceover.md`, `narration_manifest.json`, and usable audio under `audio/voiceover/` when narration is required
- `references/render-qa-checklist.md`

The orchestrator reads `scene_review_result.md` and `references/scene-review-checklist.md` only when QA cannot continue, review results conflict, or the proper rollback target is unclear.

### Do Not Start Until
`scene_review_result.md = PASS` exists as a formal file-backed review result.
Immediately before starting this phase, recompute SHA-256 for the current design and brief and confirm `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` and `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.
QA must be performed by an independent reviewer who did not contribute to the output under review.
If `scene_review_result.md` is missing or is not `PASS`, QA must not begin and `qa_result.md` must not be produced.

If `scene_review_result.md` is entirely absent, return to `RENDER` to complete scene review.
If `scene_review_result.md` exists with `FAIL`, follow that artifact's named repair target instead of inventing a new QA-side route.

### Do
Dispatch `qa-verifier` to inspect the actual rendered output and every required artifact against the approved contract.
QA must check meaning, visual clarity, timing, layout, delivery completeness, compliance with on-screen supplementary-information rules, narration obligations, and audio synchronization when narration exists.
Do not replace formal QA with a basic render test, playback check, or orchestrator self-check.

### Required Outputs
Create `qa_result.md`.

### Pass / Exit Gate
Advance only when `qa_result.md = PASS`.
QA cannot begin without `scene_review_result.md = PASS`.

### Rollback When Problems Occur
For visual, timing, layout, or scene implementation failures against the contract, return to `RENDER`.
For missing audio, wrong-language narration, narration text that drifts from the script, or audio-sync problems rooted in voiceover artifacts, return to `VOICEOVER`.
For animation beat-structure mismatch, return to `SCRIPT`.
If output drift originates in brief wording, source-label, or faithful-conversion errors, return to `CONTRACT`, repair it, and regain exact-version brief approval.
If the output reveals a gap in core semantics, the primary mental model, core visual semantics, teaching arc, or another core design decision, return to `DESIGN_DEVELOPMENT` and complete re-review, reapproval, and the downstream `CONTRACT` gates before continuing.

## Phase 6: DELIVERY

### Goal
Deliver the correct artifacts and summary for the approved delivery tier without overstating what is complete or passed.
Every delivery claim must be supported by passed formal gate artifacts.

### Delegation
The orchestrator handles this phase.
It requires neither a subagent nor an independent reviewer.

### Read Before Acting
Read `qa_result.md`, `scene_review_result.md`, and the approved `pre_build_brief.md`.
Read `references/render-qa-checklist.md` only when delivery evidence is insufficient or tier completeness is unclear.

### Do Not Start Until
`qa_result.md = PASS`.
Immediately before starting this phase, recompute SHA-256 for the current design and brief and confirm `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` and `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.

### Do
Report only artifacts that actually exist and gate status backed by formal files.
The delivery summary must match the approved delivery tier.

### Required Outputs
Produce a delivery summary that matches the actual artifacts and approved delivery tier.

### Pass / Exit Gate
Delivery is complete only when delivered artifacts match the approved delivery tier and are supported by passed formal gate artifacts.
Do not begin `DELIVERY` without `qa_result.md = PASS`.

### Rollback When Problems Occur
For missing delivery evidence or tier-completeness problems, return to `QA`.
If the delivery summary reveals brief wording, source-label, or faithful-conversion errors, return to `CONTRACT`, repair it, and regain exact-version brief approval.
If the delivery summary reveals output drift caused by a core design gap, return to `DESIGN_DEVELOPMENT` and complete re-review, reapproval, and the downstream `CONTRACT` gates before continuing.

## Unacceptable Shortcuts
Treat each statement below as a workflow violation, never as a reason to omit a step:

| Shortcut | Required response |
| --- | --- |
| "I can skip `DESIGN_DEVELOPMENT` and turn intake directly into the brief." | Do not skip it; `INTAKE` cannot replace actual animation design, `DESIGN_READY`, and independent design review. |
| "The reviewer said it was fine in chat, so no review file is needed." | Informal opinion cannot replace `animation_design_review.md = PASS` produced by the independent `animation-design-reviewer`. |
| "`pre_build_brief.md` is detailed enough, so I can skip `SCRIPT`." | Run `SCRIPT`; scene code cannot replace `teaching_script.md`. |
| "The render runs, so review is complete." | Produce formal `scene_review_result.md` through the independent reviewer. |
| "Preflight passed, so independent scene review is optional." | Run scene review after `render_preflight.md` exists. |
| "A basic render test can replace QA." | Run independent QA and produce `qa_result.md`. |
| "One more local patch is cheaper than investigating repeated visual problems." | If failures indicate ambiguity in an earlier phase, return to the owning phase. |
| "I should read every reference now to be safe." | Read only current-phase requirements and additional references when a specified trigger occurs. |
| "I delegated the phase, so I no longer own its gate." | The orchestrator still owns phase order, artifact existence, and pass conditions. |
| "This core design gap is small enough to patch in `SCRIPT` or `RENDER`." | Do not patch core design downstream; return to `DESIGN_DEVELOPMENT`, repeat review and approval, then complete the `CONTRACT` gates. |
| "Only one word changed in `animation_design.md`, so the old review and approval remain valid." | Every edit invalidates old review and approval; use full or delta review according to impact and regain `PASS` and exact-version approval. |
| "The design is approved, so the brief does not need separate approval." | Design and brief are two independent external approval gates; `Approved Brief SHA-256` must equal the current brief SHA-256. |

## Completion Check
Before claiming the workflow is complete, verify:

- `intake_summary.md` exists and accurately preserves user-sourced material and source labels.
- `animation_design.md` exists and passes `DESIGN_READY`.
- `animation_design_review.md = PASS` and was produced by the independent `animation-design-reviewer`.
- `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`.
- The user explicitly approved that exact reviewed design version in an external record.
- `pre_build_brief.md` exists and faithfully converts the approved design.
- `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`.
- The user separately and explicitly approved that exact brief version in an external record.
- `teaching_script.md` exists.
- `script_review_result.md = PASS`.
- Voiceover artifacts match the approved delivery tier.
- `generated_algo_scene.py` exists.
- Latest-render evidence exists and was derived from the latest MP4.
- `render_preflight.md` exists and references latest-render evidence.
- `scene_review_result.md = PASS`.
- `qa_result.md = PASS`.
- The delivery summary matches the approved delivery tier and does not claim any unmet gate is complete.
