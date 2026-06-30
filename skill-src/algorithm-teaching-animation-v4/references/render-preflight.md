# Render Preflight

This document defines the compact self-check that must happen before independent scene review.

Preflight is not a substitute for review. It prevents obvious render-layer defects from reaching review as the first visual debugging pass.

## Required Output

Write `render_preflight.md` before requesting scene review.

Use this compact format:

```markdown
# Render Preflight

## Source Evidence
- MP4: `<path>`
- MP4 last-write time: `<timestamp>`
- MP4 size: `<bytes or human-readable size>`
- Evidence frames regenerated after latest render: `PASS` or `FAIL`

## Checks
| Check | Result | Evidence |
| --- | --- | --- |
| Intro has no future-phase helper objects | PASS/FAIL/N/A | `<frame or timestamp>` |
| Required base values and labels are visible | PASS/FAIL/N/A | `<frame or timestamp>` |
| One mismatch/update beat shows focus, references, formula/state, and written result | PASS/FAIL/N/A | `<frame or timestamp>` |
| One match/success beat shows focus, references, formula/state, and written result | PASS/FAIL/N/A | `<frame or timestamp>` |
| Completed structure shows all required final values | PASS/FAIL/N/A | `<frame or timestamp>` |
| Traceback/path/reconstruction beat has readable current state and labels | PASS/FAIL/N/A | `<frame or timestamp>` |
| Final frame contains only the intended final-result presentation | PASS/FAIL/N/A | `<frame or timestamp>` |
| No explanatory text is captured mid-transition or visually corrupted | PASS/FAIL/N/A | `<frame or timestamp>` |
```

Each evidence cell must be one short reference, not a paragraph.

## Evidence Freshness

Every rerender invalidates previous extracted review frames.

After each rerender:

- regenerate all review frames from the latest MP4
- update `render_preflight.md`
- record the MP4 path, size, and last-write time
- do not reuse frame evidence older than the MP4

If any frame evidence is older than the MP4, scene review must reject the handoff before judging visual quality.

## First-Pass Correctness Checks

The scene writer must inspect representative settled frames before review:

- opening or intro frame
- at least one ordinary update or mismatch frame when applicable
- at least one match, success, or acceptance frame when applicable
- completed primary structure frame
- traceback, path, reconstruction, or finalization frame when applicable
- final result frame

Use `N/A` only when the algorithm or approved script truly lacks that class of beat.

## Loop Control

After a failed scene review, the next handoff should be a delta handoff unless the repair changed algorithm semantics, beat order, delivery tier, or the approved contract.

A delta handoff must include:

- previous blocking finding ids
- what changed for each finding
- updated evidence references for affected frames
- one adjacent-phase regression check for each changed helper or visibility rule

If two consecutive failures are caused by the same class of Manim visual-state defect, stop local patching and rewrite the scene's phase ownership or visibility plan inside `RENDER` before requesting review again.

If a third scene-review failure occurs after that rewrite, escalate as an architecture issue instead of continuing patch-and-review loops. Route to `RENDER` or `SCRIPT` for defects owned there. Route to `DESIGN_DEVELOPMENT` when the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork; require design repair, review, and reapproval, then brief regeneration and reapproval. Route to `CONTRACT` when the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion; repair and reapprove the brief without redesign.
