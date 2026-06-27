# Animation Design Stage Design

## Purpose

Replace the current request-only first phase with a design-centered workflow that helps users turn incomplete algorithm-animation requests into reviewed, editable, high-quality animation designs before scripting or implementation begins.

The workflow must not require users to design the animation by themselves. A specialized subagent proposes the teaching model, visual presentation, teaching arc, and recommended alternatives, while the user retains final authority through explicit approval gates.

## Top-Level Workflow

Rename `REQUEST_CONTRACT` to `ANIMATION_DESIGN` while preserving the existing six-phase architecture:

```text
ANIMATION_DESIGN -> SCRIPT -> VOICEOVER -> RENDER -> QA -> DELIVERY
```

`ANIMATION_DESIGN` contains three mandatory subphases:

```text
INTAKE -> DESIGN_DEVELOPMENT -> CONTRACT
```

No subphase may be skipped. A downstream discovery of an upstream gap must return to the subphase that owns the missing decision.

## Subphase 1: INTAKE

### Goal

Preserve the user's request accurately and prepare sufficient source material for design work without prematurely choosing the animation design.

### Owner

The orchestrator owns this subphase.

### Responsibilities

- Preserve the user's original wording for requirements, constraints, and prohibitions that affect semantics, teaching direction, visuals, delivery, or acceptance.
- Record the algorithm, known variant, sample input or scenario, audience, intended use, visual constraints, narration expectations, and special requests.
- Classify the request as first-class or best-effort support.
- Record unresolved design questions without answering them silently.
- Produce `intake_summary.md` and hand it to `animation-designer`.

### Gate

`INTAKE` passes when `intake_summary.md` contains the known request, preserved constraints, support classification, and unresolved design questions needed to begin design development.

## Subphase 2: DESIGN_DEVELOPMENT

### Goal

Develop the user's request into a concrete, coherent, implementable, and teachable algorithm-animation design.

The primary work is designing how the animation teaches and presents the algorithm. Clarification is a supporting mechanism, not the purpose of this subphase.

### Animation Designer

Create `agents/animation-designer.md`. The agent owns both core-question planning and animation design.

Its responsibilities are:

1. Analyze the algorithm variant, audience, teaching goal, sample scenario, likely misconceptions, and risks in the initial request.
2. Select and explain the primary mental model the viewer should retain.
3. Design how algorithm state, data, pointers, boundaries, support structures, progress, and exclusions appear on screen.
4. Define stable visual semantics, information hierarchy, and the main scene structure.
5. Select or improve the sample input so it exposes the intended teaching points.
6. Design the overall teaching arc and high-level animation beats.
7. Define each beat's focus, state change, causal relationship, and teaching purpose.
8. Evaluate the user's initial idea, identify quality risks, compare reasonable alternatives, and clearly recommend a better option when warranted.
9. Plan only the high-impact questions that block a good design, with a recommendation and rationale for each.
10. Produce and revise `animation_design.md`.
11. Run the `DESIGN_READY` self-check before requesting independent review.

The user remains the final decision-maker. The agent may challenge an initial idea and recommend a different design, but may not override an explicit user decision.

### Core-Question Interaction

Use a batched handoff to reduce token and delegation overhead:

1. `animation-designer` plans a small set of high-impact questions.
2. Each question includes why it matters, a concrete recommendation, and its tradeoffs.
3. The orchestrator asks the user one question at a time and records answers faithfully.
4. The orchestrator must not replace the designer's recommendation or infer a design conclusion on its behalf.
5. After the planned questions are answered, the orchestrator returns the answers to `animation-designer` as one batch.
6. Start another question batch only if the answers expose a new blocking issue.

Do not ask about ordinary colors, minor placement, routine transitions, easing, or local timing unless the user made one of those details semantically or contractually important.

### Animation Design Artifact

Create `animation_design.md` as an editable user-facing artifact. It must contain:

- design goal and audience
- algorithm variant and semantics
- primary mental model
- likely viewer misconceptions to prevent
- sample input and selection rationale
- core visual metaphor and stable visual semantics
- presentation of data, pointers, boundaries, progress, and support structures
- scene structure and information hierarchy
- overall teaching arc
- high-level animation beats
- focus, state change, causal relationship, and teaching purpose for each beat
- recommended design, meaningful alternatives, tradeoffs, and rationale
- incorporated user decisions
- risks and best-effort notes
- `DESIGN_READY` self-check result

The user may edit this file directly. A direct edit does not bypass independent review.

### DESIGN_READY Gate

The design is ready for independent review only when all of the following are true:

- The algorithm variant, audience, and teaching goal are explicit.
- The mental model, visual presentation, and teaching arc are complete.
- The sample input supports the intended lesson.
- High-level beats have clear focus and causal progression.
- No unresolved issue would change algorithm semantics, teaching direction, core layout, beat structure, or delivery obligations.
- Teaching coherence, visual feasibility, and semantic consistency pass self-check.
- The design contains a clear recommendation and material tradeoffs.
- Remaining risks are disclosed.

Once these conditions are met, the designer must stop exploratory design and request review. It must not delay the gate to optimize low-impact presentation details.

### Independent Reviewer

Create `agents/animation-design-reviewer.md`. The reviewer must not have authored the design.

The reviewer produces `animation_design_review.md` containing:

- review scope: full or delta
- teaching-coherence result
- visual-feasibility result
- algorithm-semantic-consistency result
- unresolved high-impact issues
- required repairs
- rollback target
- final verdict: `PASS` or `FAIL`

The initial review is always full. After a failure, ordinary localized repairs use delta review. A change to algorithm semantics, the primary mental model, core visual semantics, or the teaching arc requires a new full review. The same rule applies after the user edits `animation_design.md`.

Only `PASS` permits the orchestrator to request explicit user approval of `animation_design.md`.

### User Design Approval

The design passes only after both independent review `PASS` and explicit user approval. Silence and file edits alone do not count as approval.

## Subphase 3: CONTRACT

### Goal

Convert the approved animation design into the formal downstream contract without reopening or silently changing the design.

### Owner

`animation-designer` converts the approved `animation_design.md` into `pre_build_brief.md`. A separate `brief-editor` is not used.

### Rules

- Preserve all approved core decisions and their sources.
- Separate explicit user requests, user-approved decisions, and agent defaults.
- Freeze algorithm semantics, visual semantics, teaching arc, delivery tier, narration obligations, and overlay policy for downstream phases.
- Do not add unapproved core decisions.
- If conversion exposes a missing core decision, return to `DESIGN_DEVELOPMENT`; update, review, and reapprove `animation_design.md` before trying again.
- If the design is complete and only the contract wording or source labeling is wrong, repair it within `CONTRACT`.

The user must explicitly approve `pre_build_brief.md` separately from `animation_design.md`. Only then does `ANIMATION_DESIGN` pass.

## Artifact and Data Flow

```text
user request
    |
    v
intake_summary.md
    |
    v
animation_design.md
    |
    v
animation_design_review.md = PASS
    |
    v
explicit user design approval
    |
    v
pre_build_brief.md
    |
    v
explicit user contract approval
    |
    v
SCRIPT
```

## Rollback Rules

- Incorrectly captured source request: return to `INTAKE`.
- Incomplete or failed design: return to `DESIGN_DEVELOPMENT`.
- Incorrect contract wording or source labeling: remain in `CONTRACT`.
- Contract conversion exposes a design gap: return to `DESIGN_DEVELOPMENT`.
- A later phase exposes ambiguity in core semantics, mental model, visual semantics, or teaching arc: return to `DESIGN_DEVELOPMENT`; do not patch the gap in `SCRIPT` or `RENDER`.

## Agent and Reference Structure

### Add

- `agents/animation-designer.md`
- `agents/animation-design-reviewer.md`
- `references/animation-design-process.md`
- `references/animation-design-document.md`
- `references/teaching-design.md`
- `references/animation-design-review-checklist.md`
- `references/animation-design-array-sorting.md`
- `references/animation-design-search.md`
- `references/animation-design-graph-traversal.md`

### Reuse or Update

- `references/intake-contract.md`
- `references/high-impact-clarification.md`
- `references/visual-language.md`
- `references/default-visual-semantics.md`
- `references/pre-build-brief.md`

The agent files define role, workflow, inputs, outputs, routing, prohibitions, and rollback ownership. Detailed design knowledge belongs in references.

Both designer and reviewer read the common references and only the type-specific reference relevant to the current request. If no type-specific reference exists, use the common design method, label the work `best-effort`, disclose the coverage risk, and apply stricter review.

### Remove

- `agents/brief-editor.md`
- `agents/clarification-planner.md`

Their required responsibilities move into `animation-designer`.

## Verification

Implementation verification must confirm:

- Phase names, artifact chains, gates, and rollback rules agree across `SKILL.md`, agent files, and references.
- No references to removed roles remain.
- New agents have explicit inputs, outputs, prohibitions, and rollback rules.
- The `animation_design.md` schema covers every `DESIGN_READY` condition.
- The reviewer checklist can produce an evidence-backed result for every gate condition.
- The workflow cannot skip from `INTAKE` to `CONTRACT`.
- `SCRIPT` cannot begin after reviewer `FAIL`, missing design approval, or missing contract approval.
- Representative walkthroughs cover array sorting, binary search, BFS, and one best-effort algorithm.
- The sorting walkthrough tests movement semantics and settled progress.
- The search walkthrough tests interval semantics and the chosen mental model.
- The BFS walkthrough tests queue visibility, visited timing, and layer expansion.
- The best-effort walkthrough tests risk disclosure and stricter review.

## Success Criteria

The change succeeds when users can begin with an incomplete animation request, receive expert design assistance, directly edit a concrete design artifact, approve a reviewer-validated animation design, and then approve a faithful formal contract before downstream production begins.
