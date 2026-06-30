# Render QA Checklist

This document defines the final QA pass for `algorithm-teaching-animation-v3`.

Scene review asks whether the scene implementation faithfully expresses the contract. Render QA asks whether the rendered output is actually safe to deliver for the chosen tier.

## Required Output

Return `qa_result.md` with:

- `PASS` or `FAIL`
- independent reviewer authorship of the review result
- reviewer ownership of the `QA` gate
- delivery tier under review
- findings with evidence
- repair direction: `RENDER`, `VOICEOVER`, `SCRIPT`, `DESIGN_DEVELOPMENT`, or `CONTRACT`

If `scene_review_result.md` is missing or not `PASS`, `QA` is blocked from starting. In that case, do not emit `qa_result.md`; return an upstream gate-block notice that names the blocking scene-review condition and its repair target. When `scene_review_result.md` is missing entirely, use `RENDER` as the default repair target so the scene-review gate can be completed.

`QA` is an independent review gate. `qa_result.md` must be authored by an independent reviewer rather than any contributing author to the output under review.

Do not start `QA` unless `scene_review_result.md = PASS` exists as the explicit file-backed scene-review result. A failing or missing `scene_review_result.md` blocks `QA` entry and must be honored as an upstream review gate, not converted into an ordinary `QA`-only judgment or a synthetic `qa_result.md`.

## QA Inputs

Review against:

- approved `pre_build_brief.md`
- approved `teaching_script.md`
- `render_preflight.md`
- `scene_review_result.md`
- rendered media output
- approved `voiceover.md`, `narration_manifest.json`, and usable audio assets when the tier includes narration
- overlay output when overlays are enabled

## Delivery-Tier Checks

### No Narration

Verify:

- approved `pre_build_brief.md` explicitly records that narration is not owed and no voiceover assets are required
- the render is visually understandable without narration
- no audio-dependent teaching step is left unexplained
- overlays are absent unless explicitly enabled

### Final Narrated Delivery

Verify:

- all required audio assets are present
- narration language matches the approved brief
- visual focus and voiceover remain aligned beat by beat
- the result is clean enough to deliver, not just debug

## Core Checklist

### Visual Readability

- primary structures remain legible throughout
- active focus is obvious in each beat
- settled or excluded regions remain distinguishable
- labels are readable and non-colliding
- nothing important is cropped or hidden
- final delivery evidence comes from the latest render, not stale review frames

### Contract Fidelity

- the render matches the confirmed semantics
- support structures appear when required
- no new semantics were added during implementation
- overlay behavior matches the brief

### Timing and Audio

- beat pacing gives the viewer time to register the change
- voiceover starts after the visual hook is established
- long holds are justified by teaching value, not by dead air
- narration and visuals do not contradict each other

### Delivery Completeness

- the correct tier was actually produced
- required files for that tier exist and are usable
- no no-narration output is mislabeled as narrated
- no draft-quality narration is mislabeled as final
- `render_preflight.md` and `scene_review_result.md` refer to the same latest-render evidence or clearly explain a later approved rerender

## Repair Direction

Use these paths:

- `stay within RENDER` for layout, spacing, timing, styling, or fidelity repairs that keep the same frozen semantics
- `return to VOICEOVER` when QA discovers missing audio assets, wrong-language narration, narration-text drift, or audio-sync defects rooted in the narration artifacts
- `return to SCRIPT` when QA discovers a beat-structure mismatch that render changes alone cannot fix
- `return to DESIGN_DEVELOPMENT` when the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork; require design repair, review, and reapproval, then brief regeneration and reapproval
- `return to CONTRACT` when the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion; repair and reapprove the brief without redesign

QA may not silently rewrite the contract.
QA may not override a failing scene review by issuing an independent pass or by rerouting the same blocked work as a normal `QA` defect.
QA should not repeat scene review. If `scene_review_result.md = PASS` exists and evidence is fresh, QA checks delivery safety, tier completeness, and final-output readiness.

## PASS Standard

Only pass when all of these are true:

- `scene_review_result.md = PASS` exists as the explicit file-backed scene-review result
- preflight and scene-review evidence are not stale relative to the final rendered media
- the chosen delivery tier is satisfied
- the render is readable
- the contract is implemented faithfully
- no unresolved semantic ambiguity remains visible to the viewer
- `qa_result.md` is written by an independent reviewer rather than any contributing author to the output under review

## Common Failures

- Passing a scene that is semantically correct but visually unreadable.
- Treating missing audio in a narrated tier as a minor note.
- Fixing a contract gap by improvising new semantics inside QA notes.
- Calling a debug-quality preview "final" because the algorithm logic is correct.
