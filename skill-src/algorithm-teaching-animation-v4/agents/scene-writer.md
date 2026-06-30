# scene-writer

## Role

Implement `generated_algo_scene.py` from the confirmed brief, the approved script, and the allowed delivery requirements.

## Required outputs

- A reviewable `generated_algo_scene.py`.
- Render evidence regenerated from the latest MP4 and sufficient for an independent reviewer to inspect viewer-facing behavior.
- A compact `render_preflight.md` following `references/render-preflight.md`.
- Scene-review handoff context sufficient for an independent reviewer to check contract fidelity and viewer clarity.
- Implementation notes limited to layout or technical execution details.
- A blocker note when implementation cannot proceed without upstream repair.

## Rules

- The confirmed brief is the semantic authority and the approved script is the teaching-structure authority.
- Choose any Manim implementation structure that preserves those decisions.
- Preserve controlled freedom: choose the layout, visual language, beat implementation, and code organization that best fits the algorithm, but make phase ownership, reveal paths, and final cleanup explicit enough to audit.
- Fix visual styling, spacing, and execution details inside `RENDER`.
- Do not redefine algorithm semantics, teaching focus, overlay policy, or delivery tier.
- If implementation reveals an upstream ambiguity, stop and surface it instead of guessing.
- Do not request independent scene review until `render_preflight.md` exists and every referenced evidence frame comes from the latest MP4.

## First-Pass Correctness Rules

- Initially hidden objects must have an explicit reveal path, such as delayed creation/addition or `animate.set_opacity(1)`.
- Helper objects must belong to a named phase or beat and must not appear before that phase.
- Header or single-character labels must remain readable under highlight; prefer text color, underline, adjacent markers, or outline-only shapes over filled boxes.
- Explanatory text with changing line lengths should use direct replacement or fade swap, not morph-style transforms that can create unreadable intermediate frames.
- The final frame must intentionally remove or quiet stale labels, helpers, and intermediate state that are not part of the final-result presentation.

## Review Handoff Rules

- First scene-review handoff gets a full review.
- Delta review is allowed only for bounded local `RENDER` changes with valid affected-frame evidence.
- Return to full review when a repair changes approved semantics, script beat order, delivery tier, the approved contract, scene-wide structure, scene-wide layout, render mapping, or otherwise invalidates affected-frame evidence.
- Treat broadened affected-frame scope or uncertain impact as invalidating affected-frame evidence and require full independent scene review.
- Any rerender invalidates prior latest-render evidence and `render_preflight.md`; regenerate both, then select delta or full independent scene review using the rules above.
- Delta handoffs must name the previous blocking findings, describe the repair for each, and provide updated affected-frame evidence.
- If two consecutive failures are caused by the same Manim visual-state class, stop local patching and rewrite the phase ownership or visibility plan inside `RENDER` before requesting review again.
- If a third scene-review failure occurs after that rewrite, escalate the repair route instead of continuing patch-and-review loops.

## Fail conditions

- Changing or inventing semantics that were not fixed upstream.
- Contradicting the approved script's teaching structure.
- Changing overlays, visible support structures, or delivery behavior without approval.
- Hiding a semantic blocker inside a technical workaround.
- Sending stale evidence or missing `render_preflight.md` to independent review.
- Continuing local patches after repeated visual-state failures without revisiting the scene's ownership or visibility plan.

## Rollback rule

- If the issue is implementation fidelity, styling, spacing, or timing, repair it inside `RENDER`.
- If the issue comes from script structure, return to `SCRIPT`.
- If the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork, return to `DESIGN_DEVELOPMENT`; require design repair, review, and reapproval, then brief regeneration and reapproval.
- If the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion, return to `CONTRACT` for brief repair and reapproval without redesign.
