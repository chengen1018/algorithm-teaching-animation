# Scene Review Checklist

This document defines the `RENDER` gate review for `algorithm-teaching-animation-v3`.

The reviewer checks scene fidelity and viewer clarity. The reviewer does not invent or repair semantics.

## Required Output

Return `scene_review_result.md` with:

- `PASS` or `FAIL`
- independent reviewer authorship of the review result
- reviewer ownership of the `RENDER` gate
- categorized blocking findings
- evidence references
- repair direction: `RENDER`, `SCRIPT`, `DESIGN_DEVELOPMENT`, or `CONTRACT`

Use these finding categories:

- `styling`
- `layout`
- `semantic ambiguity`
- `contract mismatch`

## Review Inputs

Review against:

- approved `pre_build_brief.md`
- approved `teaching_script.md`
- `generated_algo_scene.py`
- `render_preflight.md`
- rendered preview or render evidence

Before judging visual quality, verify that `render_preflight.md` and latest-render evidence exist, match each other, and were regenerated after the latest MP4. Missing, stale, incomplete, or mismatched preflight or latest-render evidence is a blocked or invalid review handoff and an evidence/process defect routed to `RENDER`, not a `layout` finding. Do not proceed or return `PASS` until `RENDER` regenerates matching evidence and preflight for the latest MP4. Classify actual visual layout findings as `layout`.

## Review Questions

### Contract Fidelity

- Does the scene implement the frozen semantics rather than a new interpretation?
- Does each major beat match the teaching purpose in the approved script?
- Are support structures present when the brief says they matter?

### Visual Clarity

- Is the current focus obvious?
- Are pointers, boundaries, and temporary structures readable?
- Do resolved regions remain understandable without stealing focus?
- Are active prefix, header, pointer, or state labels readable under highlight?
- Are explanatory text panels judged in settled frames rather than unreadable transition frames?

### Layout Safety

- Are labels and structures free of collisions?
- Is important content kept inside safe margins?
- If overlays are enabled, do they avoid the teaching-critical area?
- Does the intro avoid future-phase helper objects?
- Does the final frame contain only the intended final-result presentation?

### Semantic Safety

- Does any styling choice force the viewer to infer a rule the brief never froze?
- Does any implementation convenience change what the viewer learns?
- Does any mismatch reveal unresolved semantic ambiguity, a semantic mismatch, or a missing upstream decision?

## Repair Routing

### Stay Within RENDER

Use this when the problem is limited to:

- styling
- spacing
- layout execution
- implementation fidelity without semantic ambiguity

The repaired scene must keep the same confirmed semantics.

### Return to SCRIPT

Use this when:

- the scene exposes a beat-structure mismatch against the approved script
- the approved brief is clear, but the script did not give scene work enough faithful beat guidance
- the approved brief is clear, but script-layer incompleteness forced the scene to guess structure, sequencing, or emphasis

Do not patch beat logic locally inside `RENDER` just because the implementation is already in motion.

### Return to DESIGN_DEVELOPMENT

Use this when the issue is:

- the approved design itself lacks or conflicts on algorithm semantics
- the approved design itself lacks or conflicts on the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, or high-level beats
- the approved design itself lacks or conflicts on the delivery decision
- the approved design itself lacks or conflicts on a newly surfaced high-impact fork

Require design repair, review, and reapproval, then brief regeneration and reapproval before resuming scene work.

### Return to CONTRACT

Use this when the approved design is clear but `pre_build_brief.md` has wrong wording or source labels, or otherwise failed faithful conversion. Repair and reapprove the brief without redesign.

## Contract Mismatch Rule

Use `contract mismatch` when the scene conflicts with the confirmed brief or approved script.

Default handling:

- keep it inside `RENDER` when the brief and script are clear and the scene simply violated them
- return to `SCRIPT` when the brief is clear but the approved script is the layer that mismatched the intended beat structure or otherwise left scene work with script-layer incompleteness
- return to `DESIGN_DEVELOPMENT` when the mismatch proves that the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork; require design repair, review, and reapproval, then brief regeneration and reapproval
- return to `CONTRACT` when the approved design is clear but the mismatch comes from wrong brief wording or source labels, or another failure of faithful conversion; repair and reapprove the brief without redesign

## Delta Review

Delta review is allowed only for bounded local `RENDER` changes with valid affected-frame evidence.

A delta review checks only:

- previous blocking findings
- changed frames and directly adjacent phases
- new visual regressions caused by the repair
- evidence freshness

Return to full review when a repair changes approved semantics, script beat order, delivery tier, the approved contract, scene-wide structure, scene-wide layout, render mapping, or otherwise invalidates affected-frame evidence.

Treat broadened affected-frame scope or uncertain impact as invalidating affected-frame evidence and require full independent scene review.

If two consecutive failures share the same Manim visual-state class, require the scene writer to rewrite phase ownership or visibility planning before another review. If a third failure occurs after that rewrite, route according to the failed artifact's repair target instead of continuing local patch loops.

## PASS Standard

Pass only when:

- the scene is faithful to the contract
- the scene is visually readable
- layout is safe
- `render_preflight.md` exists and references latest-render evidence
- no unresolved semantic question remains visible to the reviewer
- `scene_review_result.md` is written by an independent reviewer rather than the render executor
- `scene_review_result.md` exists as the explicit review artifact; implicit passes, waivers, or undocumented substitutes do not count

## Common Failures

- Approving a scene because it runs, even though it invented semantics.
- Mislabeling a semantic problem as styling to avoid rollback.
- Returning `FAIL` without evidence or without naming the repair level.
- Treating support-structure removal as harmless cleanup when it changes the lesson.
- Reviewing stale frames after a rerender.
- Repeating full review when the handoff only needs delta review.
