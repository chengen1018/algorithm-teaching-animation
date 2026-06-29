# Pre-build Brief

This document defines `pre_build_brief.md`, the downstream CONTRACT artifact in `algorithm-teaching-animation-v3`.

No CONTRACT conversion may begin until the exact current `animation_design.md` has an independent `animation_design_review.md` verdict of `PASS` and explicit external user approval of that exact reviewed version. No script, voiceover, or scene work may begin until the converted brief receives its own explicit user approval.

## Purpose

`pre_build_brief.md` is the single shared contract for:

- script writing
- script review
- voiceover planning
- scene implementation
- scene review
- render QA

It exists so downstream work can be strict without inventing semantics late. Conversion is a faithful restatement and organization of the approved design, not a new design pass.

## Conversion Preconditions

Before conversion, all of these must be available:

- the current `animation_design.md`;
- `animation_design_review.md = PASS` for that exact design version;
- `Reviewed Design SHA-256` from the passing review;
- an external explicit user approval record with `Approved Design SHA-256` and an approval reference;
- a freshly computed SHA-256 of the current `animation_design.md` bytes.

Require exact convergence immediately before conversion:

```text
Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

Any mismatch means the design is a new or stale version. Do not convert it. Return to `DESIGN_DEVELOPMENT`, obtain the required independent re-review, receive `PASS`, and obtain explicit external user reapproval for the new exact SHA-256.

`Source Design SHA-256` is not required before conversion.

## CONTRACT Conversion Boundary

`pre_build_brief.md` must faithfully convert the approved design's semantics, mental model, visual system, scene structure, teaching arc, high-level beats, user decisions, delivery obligations, and risks. CONTRACT may organize, condense, and source-label those approved decisions, but it must not add, repair, or silently settle a core design choice.

During faithful conversion, record `Source Design SHA-256` in the external CONTRACT lineage record as the exact current `Approved Design SHA-256` used to produce `pre_build_brief.md`. Keep lineage and approval records external; do not mutate `animation_design.md` or `pre_build_brief.md` to store them.

If conversion exposes a missing, conflicting, or materially ambiguous core decision, stop and route the gap to `DESIGN_DEVELOPMENT`. The repaired `animation_design.md` must complete its full required review and approval path before conversion resumes: update and `DESIGN_READY` self-check, appropriate full or delta independent review, `animation_design_review.md = PASS`, exact-version external user approval, and SHA-256 convergence.

A wording, formatting, or source-label issue that does not change approved meaning stays in CONTRACT and may be corrected in `pre_build_brief.md` without reopening design.

Any edit to `animation_design.md` invalidates the derived `pre_build_brief.md`, its `Source Design SHA-256` lineage, and its approval. Return to `DESIGN_DEVELOPMENT`, rerun the impact-appropriate review and exact-version design approval, then regenerate the brief with new external lineage and obtain separate brief approval.

## Separate Brief Approval Gate

Approval of `animation_design.md` does not approve `pre_build_brief.md`. After conversion and before requesting brief approval, recompute the current design SHA-256 and require:

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

Only then may the orchestrator ask for separate explicit user approval of the exact `pre_build_brief.md` before downstream work starts. Record that approval externally with:

- `Approved Brief SHA-256`, computed from the exact approved `pre_build_brief.md` bytes; and
- an explicit user approval reference that identifies the approval event.

Do not write approval status, `Approved Brief SHA-256`, or the approval reference into `pre_build_brief.md`.

Every edit to `pre_build_brief.md` creates a new version and invalidates prior approval, even when the edit appears editorial. Re-review the changed brief for faithful CONTRACT conversion and obtain explicit user reapproval of its new exact SHA-256. If an edit exposes or introduces a core design change, route to `DESIGN_DEVELOPMENT` and complete design review, exact-version design approval, reconversion, and brief approval again.

At the `ANIMATION_DESIGN` exit gate and immediately before SCRIPT or any downstream phase starts, recompute the current design and `pre_build_brief.md` SHA-256 values and require:

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
Approved Brief SHA-256 = current pre_build_brief.md SHA-256
```

A mismatch in `pre_build_brief.md` alone stays in or returns to CONTRACT for brief re-review and exact-version reapproval, but only when the design chain still satisfies `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`. Any mismatch or edit in the design chain itself, whether core or non-core, routes to `DESIGN_DEVELOPMENT` for the required Full or Delta re-review, explicit design reapproval, brief regeneration, and brief reapproval before CONTRACT conversion resumes.

The brief passes the gate only when one of these happens and the external exact-version approval record is complete:

- the user gives explicit approval
- the user requests targeted edits and then approves proceeding

The brief does not pass on:

- silence
- implied agreement
- "looks fine" when unresolved forks remain hidden

## Required Sections

Every brief must include:

- `Algorithm Identity`
- `Teaching Goal`
- `Audience`
- `Sample Input / Scenario`
- `Confirmed User Requests`
- `Source Labels and Decision Provenance`
- `Resolved High-Impact Clarifications`
- `Agent Default Decisions`
- `Chosen Visual Semantics`
- `Scene Structure and Information Hierarchy`
- `Pointer / Boundary / Temp Slot Plan`
- `Beat Outline`
- `Overlay Policy`
- `Delivery Tier`
- `Narration Language`
- `Known Risks / Best-Effort Notes`

If any of these sections would be vague because a high-impact question remains open, the brief is not ready.

## Section Guidance

### Algorithm Identity

State the algorithm or concept plainly. If the request is variant-specific, name the variant.

### Teaching Goal

State the main thing the viewer should understand by the end.

### Audience

Record the user's audience if given. Otherwise state the working assumption.

### Sample Input / Scenario

Use a concrete case the scene can actually build around.

### Confirmed User Requests

List only explicit user asks, not agent guesses.

### Source Labels and Decision Provenance

Distinguish direct user requests, externally approved design decisions, designer defaults, derived consequences, and low-risk CONTRACT wording choices. Preserve source wording where it affects meaning or acceptance.

### Resolved High-Impact Clarifications

List each frozen decision and why it matters. This section is where the workflow proves that clarification was completed.

### Agent Default Decisions

Record only low-risk defaults from `default-visual-semantics.md` or other non-semantic conventions.

### Chosen Visual Semantics

Describe the specific viewer-facing rules the scene must honor.

Examples:

- how active regions are shown
- what counts as settled progress
- how support structures remain visible

This section must convert the approved core visual semantics; it must not invent them.

### Scene Structure and Information Hierarchy

Carry forward the approved major scene regions, persistent support structures, primary and supporting information, and intended viewer-facing cause/effect relationships.

### Pointer / Boundary / Temp Slot Plan

Make pointer meaning explicit. If a temporary holding area is part of the lesson, say so here. If none exists, say that too.

### Beat Outline

Give the high-level lesson arc, not full narration.

### Overlay Policy

State whether overlays are off, optional, or required.

### Delivery Tier

State exactly one of:

- `no narration`
- `final narrated delivery`

### Narration Language

If the delivery tier is `no narration`, state that no narration is owed.

If the delivery tier requires narration, freeze the spoken language explicitly.

If the user did not specify a narration language and the workflow applies the default, record that the language was defaulted to English instead of presenting it as a user instruction.

### Known Risks / Best-Effort Notes

Use this section to document support-tier limits, layout pressure, or remaining non-semantic uncertainty.

## Writing Rules

- write concrete viewer-facing language
- avoid implementation trivia unless it changes the lesson
- do not hide semantic forks behind broad wording
- separate explicit user requests from agent defaults
- preserve approved source labels and user wording when meaning depends on them
- do not add or repair core design decisions during CONTRACT conversion
- keep the brief strong enough that script and scene agents can be audited against it

## Planning Discipline

Before the brief is separately approved:

- verify that the brief faithfully carries the approved algorithm target, scenario, semantics, visual structure, beats, delivery tier, narration language, and overlay policy
- route any newly exposed core semantic, teaching, visual, scene-structure, or delivery fork to `DESIGN_DEVELOPMENT`
- do not keep a parallel "real plan" that silently outranks the brief

Temporary scratch notes are allowed, but any decision that matters downstream must appear in `pre_build_brief.md`.

If the request is best-effort support, say so explicitly in `Known Risks / Best-Effort Notes` instead of weakening the contract language elsewhere.

## Beat Outline Guidance

The beat outline should answer:

- what stable mental model the viewer needs first
- what local action changes that model
- what progress cue should persist after the action
- which support structure is teaching-critical
- where a viewer is most likely to misread the algorithm

## Failure Conditions

The brief fails when:

- a known high-impact issue is missing
- the required design, review, approval record, or exact SHA-256 convergence is unavailable
- `Source Design SHA-256` is required before conversion rather than being created during conversion
- the external CONTRACT lineage record lacks `Source Design SHA-256` or it does not equal the exact approved design SHA-256 used to produce the brief
- semantics are vague enough to support multiple conflicting scenes
- delivery obligations are unstated
- narration language obligations are unstated or hidden inside implied defaults
- overlay policy is unstated
- the beat outline cannot be reconciled with the frozen semantics
- conversion adds or repairs a core design decision
- the brief lacks separate explicit user approval
- the external approval record lacks `Approved Brief SHA-256` or an explicit user approval reference
- the current brief SHA-256 does not equal `Approved Brief SHA-256` immediately before SCRIPT or downstream work
- the design hashes do not satisfy `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256` before brief approval, at `ANIMATION_DESIGN` exit, or immediately before SCRIPT
- approval status or approval metadata is written into `pre_build_brief.md`

## Recommended Template

```md
# Pre-build Brief

## Algorithm Identity

## Teaching Goal

## Audience

## Sample Input / Scenario

## Confirmed User Requests

## Source Labels and Decision Provenance

## Resolved High-Impact Clarifications

## Agent Default Decisions

## Chosen Visual Semantics

## Scene Structure and Information Hierarchy

## Pointer / Boundary / Temp Slot Plan

## Beat Outline

## Overlay Policy

## Delivery Tier

## Narration Language

## Known Risks / Best-Effort Notes
```

## Downstream Rule

After separate confirmation of `pre_build_brief.md`, downstream phases may apply approved low-risk styling and execution defaults, but they may not revise the semantics or design frozen upstream.

If a downstream issue is only CONTRACT wording or source labeling, repair and reapprove the brief in CONTRACT. If it reveals a core design gap, return to `DESIGN_DEVELOPMENT` and complete the required design re-review, exact-version external reapproval, SHA-256 convergence, reconversion, and separate brief approval before continuing.
