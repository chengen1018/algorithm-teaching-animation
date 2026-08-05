# Layout Audit

Use this reference when reviewing or hardening `generated_algo_scene.py` for layout problems such as overlapping labels, text outside panels, title collisions, or elements drifting out of frame.

## Purpose

Manim layout bugs are best checked after mobjects exist. Static code review cannot reliably know the size of rendered `Text`, font fallback, transformed objects, or dynamic trace-driven labels.

Use `scripts/scene_layout_audit.py` as a small reusable helper copied into the generated scene project when the scene has explicit layout groups. Use `scripts/run_layout_audit.py` to execute those checks without rendering video.

There are two bundled audit styles:

- `scene_layout_audit.py`: explicit, scene-authored checks over named groups such as labels, nodes, panels, headers, and result text.
- `visible_layout_audit.py`: generic visible-object scan used by `run_layout_audit.py --audit-visible` when no scene-specific adapter exists.

## When to Add It

Use the audit runner during Stage 4 `SCENE_IMPLEMENTATION`, specifically the
pre-render `LAYOUT_VERIFICATION` gate. Add the scene-specific helper during
`CODE_PREPARATION` when:

- the scene contains panels, legends, invariant boxes, dynamic path text, tables, graph labels, or multiple text regions
- generated text comes from `action_trace.json`
- the generic visible-object scan reports crowding or possible overlap
- the user asks to detect layout issues automatically
- CI or repeated generation should fail on obvious visual collisions

Run the generic visible-object scan for every delivered Scene, including tiny
scenes, before any formal Manim render. The required gate command is:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --audit-visible --fail-on-warning --visible-report-level warning
```

Run it once for each of the four approved Scene classes in approved order.
Stage 5 does not repeat this layout gate.

## Install Into a Project

Copy the helper into the same folder as `generated_algo_scene.py`:

```text
<project>/
├── generated_algo_scene.py
└── scene_layout_audit.py
```

Then import it:

```python
import os
from scene_layout_audit import LayoutAudit

LAYOUT_AUDIT_ENABLED = os.getenv("MANIM_LAYOUT_AUDIT", "1").lower() not in {"0", "false", "no"}
LAYOUT_AUDIT_FAIL = os.getenv("MANIM_LAYOUT_AUDIT_FAIL", "0").lower() in {"1", "true", "yes"}
```

## Scene Adapter Pattern

Keep project-specific knowledge in a thin adapter inside the scene. The helper should stay generic.

```python
def _audit_layout(self, context, nodes, labels, panels, header=None, extra_items=None):
    audit = LayoutAudit(context=context, enabled=LAYOUT_AUDIT_ENABLED)
    header = header or []
    extra_items = extra_items or []
    all_items = nodes + labels + panels + header + extra_items

    for name, mob in all_items:
        audit.check_inside_frame(name, mob)

    audit.check_no_internal_overlaps(labels, min_gap=0.05)
    audit.check_no_overlaps_between(labels, nodes, min_gap=0.03)
    audit.check_no_overlaps_between(nodes + labels, panels, min_gap=0.05)
    audit.check_no_overlaps_between(header + extra_items, nodes + labels + panels, min_gap=0.05)
    audit.report(raise_on_issue=LAYOUT_AUDIT_FAIL)
```

Call the adapter after stable states, not just at the beginning:

```python
self._audit_layout("initial", nodes, labels, panels, header=[("title", title)])
self._audit_layout(f"beat:{beat_id}", nodes, labels, panels, header=[("title", title), ("message", message)])
self._audit_layout("final", nodes, labels, panels, extra_items=[("result", result_text)])
```

## Fast Dry-Run Without Rendering

Prefer a dry-run before rendering video:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene
```

The runner imports the scene, patches `Scene.play()` so animations jump to their final state, skips `wait()` and sound playback, and lets layout audit checkpoints print findings. It still creates Manim mobjects, so text metrics and `arrange()` / `next_to()` geometry are real, but it does not write frames or MP4 output.

Use `--fail-on-warning` for CI-like checks:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --fail-on-warning
```

Use `--traceback` when debugging scene construction errors:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --traceback
```

For a deterministic whole-scene pass that does not rely on project-specific `_audit_layout(...)` groups, add `--audit-visible`:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible
```

This pass scans visible scene mobjects after every patched `Scene.play()` and once again after `construct()`:

- error if a visible mobject exceeds the frame
- warning if two visible mobjects partially overlap or fully cover each other
- info if one mobject is strictly inside another smaller-than-outer bounds without touching the outer boundary

Use this pass as a broad safety net. It is deterministic and does not require hand-written groups. By default it prints errors and warnings, while suppressing strict-containment info logs. Messages are deduplicated by level and object/bounds text so repeated stable issues do not flood the log.

Useful controls:

```bash
# only scan the final construct() state
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible --visible-final-only

# cap printed unique messages; errors and warnings still count for --fail-on-warning
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible --visible-max-reports 80

# print only errors
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible --visible-report-level error

# include strict-containment info logs
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible --visible-report-level info

# explicit default: print errors and warnings, suppress strict-containment info logs
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible --visible-report-level warning
```

Limitations:

- It uses axis-aligned bounds rather than pixel-level geometry. Resolve ambiguous warnings with a scene-specific adapter based on named object groups.
- It only checks audit checkpoints that the scene code calls.
- Custom animation logic that depends on real frame-by-frame interpolation is outside the dry-run audit's coverage and must be reported explicitly.
- It does not catch problems visible only between animation endpoints.
- With `--audit-visible`, intentional containment is logged as info; intentional overlap still requires human judgment or a project-specific adapter.

## Common Checks

- `check_inside_frame(name, mob, margin=0.1)` detects out-of-frame objects.
- `check_fits(inner_name, inner, outer_name, outer, padding=0.15)` detects text that does not fit inside a panel or box.
- `check_no_overlap(a_name, a, b_name, b, min_gap=0.05)` detects true overlaps and near misses.
- `check_no_internal_overlaps(items, min_gap=0.05)` checks repeated labels or table cells.
- `check_no_overlaps_between(group_a, group_b, min_gap=0.05)` checks whole categories.

`check_no_overlap` reports true bounding-box intersection as `overlaps`; if objects do not intersect but violate `min_gap`, it reports `is too close to`. Treat these differently in review.

## Review Rules

- Treat generic-scan warnings as candidates that require deterministic scene-specific checks, not as findings that may be ignored.
- Resolve a warning from code-level object semantics and named groups through `scene_layout_audit.py`.
- Ignore transient warnings from in-between animation frames unless they persist in stable frames.
- Verify the audited `generated_algo_scene.py` SHA-256 matches the current
  source and pre-render handoff. The later scene review and formal render must
  consume that exact hash without modifying the source.
- Prefer fixing repeated stable-frame warnings in `generated_algo_scene.py`.
- If the scene cannot express a needed layout state from trace data, fix the trace schema or teaching script first.

## CI Usage

Fast non-rendering check:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene
```

Fast non-rendering check plus deterministic whole-scene scan:

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py AlgorithmScene --audit-visible
```

When Stage 5 later renders the already-approved source, embedded audit hooks
may still print warnings and let render continue:

```bash
manim -ql generated_algo_scene.py AlgorithmScene
```

That diagnostic output is not a second layout gate and cannot replace or amend
the hash-bound Stage 4 `layout_audit_result.md`.

Disable audits:

```bash
MANIM_LAYOUT_AUDIT=0 manim -ql generated_algo_scene.py AlgorithmScene
```

Fail on audit findings:

```bash
MANIM_LAYOUT_AUDIT_FAIL=1 manim -ql generated_algo_scene.py AlgorithmScene
```

On Windows PowerShell:

```powershell
$env:MANIM_LAYOUT_AUDIT_FAIL = "1"
python -m manim -ql .\generated_algo_scene.py AlgorithmScene
```

## Avoid Overreach

Do not rely only on bounding boxes for arrows or curved paths. Arrow bounding boxes often cover large empty triangular regions and can create false positives. Prefer checking labels, nodes, text panels, headers, legends, tables, and result text first. Add line/path-specific checks only when the project has a concrete need.
