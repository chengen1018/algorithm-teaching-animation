# Animation Design Review Checklist

## Review Preconditions

- Review only an `animation_design.md` version that the designer marked `DESIGN_READY` and handed off for independent review.
- Identify the exact design version under review. A prior `animation_design_review.md` does not apply after any edit.
- Read the intake and the design references routed for the algorithm category. Confirm that the reviewer did not author or repair the design.
- Do not request external user approval during review. External approval may be requested only after this exact version receives `PASS`.

## Review Scope Selection

Record `Review Scope: Full` or `Review Scope: Delta` and explain why that scope is valid. When impact is uncertain, use full review.

### Full Review

Use full review for the initial review. Also use it after changes to algorithm semantics, the primary mental model, the core visual metaphor or visual semantics, the teaching arc, scene structure, high-level beats, or any change with cross-cutting or uncertain impact. Inspect the complete document and every `DESIGN_READY` condition.

### Delta Review

Use delta review only for a clearly localized change whose complete effects can be traced. Inspect the changed text, every dependent section, internal consistency, preserved user decisions, and the updated `DESIGN_READY` self-check. Escalate to full review immediately if the change affects or may affect algorithm semantics, the primary mental model, core visual semantics, the teaching arc, scene structure, or high-level beats.

## Teaching Coherence

Require evidence that the design has a clear audience and learning goal, one faithful primary mental model, a teaching sample that exposes meaningful behavior, and a teaching arc in which each high-level beat prepares the next. Confirm that visible evidence supports the intended viewer inference and prevents the named misconceptions.

## Visual Feasibility

Require evidence that the visual metaphor, stable visual semantics, structure presentation, scene regions, information hierarchy, and high-level beats can be implemented without contradictory encodings, hidden teaching-critical state, overloaded focus, or an unexplained layout change. Feasibility does not require low-level Manim choreography.

## Algorithm Semantic Consistency

Require evidence that the algorithm variant, state, invariants, boundary and tie conventions, transitions, termination, sample result, mental model, visual encodings, and beats agree. Presentation choices must not imply behavior or guarantees the algorithm does not have.

## High-Impact Gap Check

Fail if any unresolved question could materially change algorithm semantics, the primary mental model, the core visual metaphor or semantics, the teaching arc, scene structure, or high-level beats. Do not downgrade a core gap into a best-effort note. Confirm that all material user decisions are represented faithfully and that only documented low-impact defaults remain.

## Best-Effort Strengthened Review

When no matching type-specific design reference exists, require the design to mark the category as best-effort and disclose the resulting coverage risk. Strengthen review by checking category-specific semantics, data-structure state, likely misconceptions, and visual feasibility directly against the intake and common design references. Unsupported-category routing is not an automatic failure, but an undisclosed risk or an unresolved high-impact gap is.

## Required Result Schema

Write `animation_design_review.md` using all of these fields and sections:

```markdown
# Animation Design Review

- Reviewed Design Version: <exact version identifier>
- Review Scope: Full | Delta
- Scope Rationale: <why this scope is valid>

## Teaching Coherence Evidence
<specific evidence from animation_design.md>

## Visual Feasibility Evidence
<specific evidence from animation_design.md>

## Algorithm Semantic Consistency Evidence
<specific evidence from animation_design.md>

## Unresolved Issues
<issues, or None>

## Required Repairs
<repairs, or None>

## Rollback Target
<DESIGN_DEVELOPMENT for FAIL, or None for PASS>

## Verdict
PASS | FAIL
```

Emit exactly one verdict: either `PASS` or `FAIL`. Do not emit a mixed, conditional, provisional, or second verdict. The result must state the review scope, evidence for teaching coherence, visual feasibility, and semantic consistency, unresolved issues, required repairs, and rollback target even when a field is `None`.

## PASS Conditions

Return `PASS` only when the selected scope is valid; every applicable `DESIGN_READY` condition is supported by cited evidence; teaching coherence, visual feasibility, and algorithm semantic consistency pass; material user decisions are preserved; no high-impact gap remains; and best-effort coverage risks are disclosed and adequately strengthened. For `PASS`, unresolved issues and required repairs must be `None` and the rollback target must be `None`.

## FAIL and Rollback Rules

Return `FAIL` for any missing evidence, contradiction, regression, unsupported claim, lost user decision, invalid review scope, failed `DESIGN_READY` condition, undisclosed best-effort risk, or unresolved high-impact gap. Name concrete required repairs and set the rollback target to `DESIGN_DEVELOPMENT`.

The reviewer reports defects but must not author or repair `animation_design.md`. After repair, the designer must produce a new `DESIGN_READY` version and request a new independent review. A failed or stale review cannot authorize external approval or conversion to `pre_build_brief.md`.
