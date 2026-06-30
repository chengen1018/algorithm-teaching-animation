# Manim Guidelines

This document defines how `generated_algo_scene.py` should implement a `v3` teaching design.

The scene is a renderer of the confirmed brief and approved teaching script. It may choose implementation structure, but it may not invent new semantics.

## Core Principle

The scene layer owns:

- layout execution
- styling
- timing
- beat staging
- audio and overlay synchronization

The scene layer does not own:

- semantic fork decisions
- delivery-tier changes
- new support-structure requirements
- reinterpretation of the teaching goal

## Required Inputs

Build the scene from:

- confirmed `pre_build_brief.md`
- approved `teaching_script.md`
- algorithm code or pseudocode when needed for execution fidelity
- approved `voiceover.md`, `narration_manifest.json`, and required audio assets when the delivery tier includes narration

If the scene cannot state what frozen decision it is implementing, it is not ready to render.

## Recommended File Structure

Keep scene code explicit and inspectable without forcing every algorithm into the same template.

Recommended sections:

1. constants and styling roles
2. scene-state structures
3. layout builders
4. beat helpers
5. `construct()`

Suggested helper groups:

- `build_primary_layout()`
- `build_support_layout()`
- `apply_role_style()`
- `play_beat()`
- `sync_voiceover()`
- `show_overlay_if_enabled()`

These are organizational expectations, not fill-in-the-blank templates. The scene writer may choose a different structure when the algorithm needs it, as long as style roles, layout setup, beat execution, visibility ownership, and final cleanup remain easy to audit.

## State Management

Maintain explicit semantic state instead of inferring meaning from current appearance.

Typical state structures:

```python
self.role_state = {}
self.pointer_state = {}
self.layout_state = {}
self.beat_state = {}
```

Track at least:

- semantic role for each visible object
- active pointers and their meaning
- support-structure visibility
- current beat id

This keeps repair work deterministic and prevents accidental drift when styles change.

## Manim Visibility Guardrails

These rules target common render-layer failures while preserving freedom in visual design.

### Hidden Objects

- Avoid pre-adding important objects with `opacity=0` unless they have an explicit reveal path.
- Prefer delayed creation/addition for objects that should not exist yet.
- If an object is already present but hidden, reveal it with an explicit state change such as `mobject.animate.set_opacity(1)`.
- Do not rely on `FadeIn` to restore visibility for an already-present hidden object without verifying the settled frame.

### Phase Ownership

- Every helper object should belong to a named phase, beat, or mode.
- Intro frames must not show traceback, future-iteration, or finalization helpers.
- Fill/update helpers must not leak into reconstruction or final-result frames unless the script says they remain meaningful.
- Traceback, path, or reconstruction helpers must not appear before that mode is introduced.

### Label Highlighting

- Do not place filled highlight boxes over single-character labels, prefix labels, row headers, or column headers.
- Prefer text color changes, underlines, adjacent markers, or outline-only shapes with verified transparent fill.
- Evidence must include at least one settled frame where active row/column, pointer, or state labels remain readable under highlight.

### Explanatory Text

- Avoid morph-style transforms for multi-line explanatory text when line lengths or wording change substantially.
- Prefer direct replacement, short fade swap, or stable panel sections.
- Do not use transition frames as review evidence for text clarity; capture settled frames after the text has resolved.

### Final Cleanup

- The final frame should intentionally remove, fade, or quiet stale labels, helper marks, temporary formula text, and intermediate indicators.
- Keep only the final-result presentation and any context the approved script requires.
- If a support structure remains in the final frame, it must still carry teaching value rather than leftover implementation state.

## Beat-Oriented Implementation

`v3` scenes should be organized around teaching beats, not only raw loop mechanics.

Each beat implementation should make these things easy to answer:

- what the viewer is supposed to inspect
- which objects carry the focus
- what progress cue remains visible after the beat

Loop-oriented code is acceptable, but the resulting motion still has to read as beat-oriented teaching.

## Visual Stability Rules

- keep primary structures spatially stable
- move only what the viewer needs to track
- keep pointer origins and destinations legible
- calm resolved regions instead of deleting them unless disappearance is part of the lesson
- keep support structures present when the brief says they are semantically important

## Render-Layer Fix Policy

Allowed fixes inside `RENDER`:

- color styling
- label micro-placement
- spacing
- safe-margin tuning
- animation pacing
- implementation-fidelity repairs that do not change frozen semantics

Disallowed fixes inside `RENDER`:

- changing movement semantics
- changing pointer meaning
- changing visited timing
- changing the lesson's active support structure
- changing delivery-tier obligations

If implementation reveals script incompleteness or beat-structure mismatch, stop and return to `SCRIPT`.

If implementation reveals that the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork, stop and return to `DESIGN_DEVELOPMENT`; require design repair, review, and reapproval, then brief regeneration and reapproval.

If the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion, stop and return to `CONTRACT` for brief repair and reapproval without redesign.

## Voiceover and Overlay Sync

When the delivery tier includes voiceover:

- sync one voiceover segment per approved beat
- make sure the visual focus is established before the corresponding narration begins
- keep the beat visually coherent until the segment finishes
- shorten narration or split beats upstream instead of hiding long audio with dead time

When overlays are disabled:

- do not reserve overlay-only layout space by default

When overlays are enabled:

- keep them in a stable, non-colliding region
- avoid covering the primary teaching structure

## Constants and Styling

Prefer clear semantic names over ad hoc style values.

Examples:

- `ROLE_BASE`
- `ROLE_FOCUS`
- `ROLE_CANDIDATE`
- `ROLE_SETTLED`
- `ROLE_EXCLUDED`
- `ROLE_SUPPORT`
- `MIN_BEAT_HOLD`
- `POINTER_LABEL_BUFF`

The exact numbers may change per project, but the semantic naming should stay stable.

## Common Scene Patterns

### Arrays

- isolate the active compare or update region
- keep the rest of the row readable
- mark settled progress without stealing focus from the active operation

### Search Windows

- show the active window as a coherent region
- distinguish boundary pointers from the current probe
- hold the updated window after elimination

### Graph Traversal

- keep node layout fixed
- visually separate current expansion from already discovered structure
- keep the queue or stack readable when it is part of the brief

## Review Readiness

Before handing the scene to review, verify that:

- every major beat can be traced back to the brief and script
- no semantic meaning depends on an unstated styling convention
- support structures appear only when justified by the brief
- audio behavior and required voiceover artifacts match the selected delivery tier
- overlay behavior matches the brief's frozen overlay policy or explicit user opt-in
- `render_preflight.md` exists and references evidence extracted from the latest render
- representative settled frames prove visibility, label readability, phase isolation, and final cleanup

## Common Failures

- Cleaning up the layout by deleting a semantically required support structure.
- Compensating for a vague brief by choosing semantics inside scene code.
- Letting animation polish override focus clarity.
- Treating implementation convenience as permission to reinterpret the lesson.
- Revealing already-added hidden objects without a reliable opacity or creation path.
- Letting helper objects appear before their teaching phase.
- Covering labels with filled highlight shapes.
- Judging explanatory text from an unreadable transition frame.
