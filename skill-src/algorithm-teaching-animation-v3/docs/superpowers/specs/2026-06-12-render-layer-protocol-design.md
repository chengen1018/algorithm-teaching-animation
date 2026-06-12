# Render Layer Protocol Design

## Goal

Improve Manim render-layer reliability for algorithm teaching animations by adding reusable render knowledge and wiring it into the `algorithm-teaching-animation-v3` render workflow.

The design targets low-level animation failures such as incorrect cell/header alignment, labels outside containers, stale or duplicated Manim objects, dynamic panel overlap, and semantic coordinate mismatches. It is not limited to dynamic programming tables; the protocol should help future array, pointer/range, graph, tree, and support-panel scenes as well.

## Scope

This change should add a reusable render protocol layer and connect it to `v3` through existing render-phase documents and agents.

In scope:

- Add reusable render-layer knowledge files.
- Strengthen `scene-writer` behavior before Manim code generation.
- Strengthen `scene-reviewer` and review checklist behavior after render evidence exists.
- Update `SKILL.md` and `agents/openai.yaml` so the new references are actually read.
- Preserve the current phase-gated workflow and independent review requirements.

Out of scope:

- Rewriting non-render phases except where render references and handoff requirements must be connected.
- Adding a heavy new formal phase.
- Changing voiceover, script, or QA ownership.
- Fixing any specific generated scene file as part of this design.

## Design Approach

Use a two-layer approach.

Layer A is a reusable render protocol. It contains Manim and animation-layout knowledge that can apply beyond `v3`.

Layer B is the `v3` adapter. It tells `scene-writer`, `manim-guidelines`, `scene-reviewer`, and review checklists how to use the reusable protocol inside the current `v3` phase contract.

The protocol should be concrete enough to prevent common render mistakes, but lightweight enough that it does not turn render work into another expensive phase.

## New Documents

### `references/render-protocol.md`

Purpose: define global render invariants and Manim implementation discipline.

Required content:

- Render contract and global invariants.
- Coordinate systems and anchoring rules.
- Layout composition and reflow rules.
- Mobject identity and update discipline.
- Semantic visual roles.
- Failure taxonomy.
- Local repair versus escalation principles.

Important rules to capture:

- Data values must stay inside their owning cells or containers.
- Header, index, annotation, and data regions must be separated intentionally.
- Semantic coordinate mapping must be explicit before scene code is written.
- Persistent dynamic UI elements must have stable update paths.
- Dynamic panels need wrapping, fixed slots, scaling, or reflow.
- Local render bugs should normally be repaired inside `RENDER`.

### `references/render-structure-patterns.md`

Purpose: organize reusable render knowledge by visual structure type.

Required structure types:

- Linear structures: arrays, stacks, queues, deques, linked lists.
- Tabular structures: DP tables, matrices, grids, prefix tables.
- Pointer/range structures: binary search, two pointers, sliding windows, partitions.
- Graph/tree structures: BFS, DFS, shortest paths, tree traversals, heap/tree operations.
- Support regions: formula panels, legends, current-step panels, side notes, collected-result boxes.

For each structure type, include:

- Standard anchor pattern.
- Label and support zones.
- Common failures.
- Forbidden shortcuts.
- Minimum review questions.

## Modified Documents

### `references/manim-guidelines.md`

Reframe this file as the `v3` render execution adapter.

Changes:

- Require use of `references/render-protocol.md`.
- Require use of `references/render-structure-patterns.md`.
- Add render preflight expectations.
- Require `scene-writer` to choose structure patterns before implementation.
- Define local repair policy for geometry, containment, overlap, reflow, visual role, and update lifecycle defects.
- Define escalation policy for true blockers that require `SCRIPT` or `PRE_BUILD_BRIEF`.

This file should not duplicate the full reusable protocol. It should explain how `v3` render work applies it.

### `agents/scene-writer.md`

Add a concrete render workflow.

Required behavior:

- Read the reusable render protocol and structure patterns.
- Produce a lightweight `Render Mapping Note` or equivalent handoff context.
- Identify structure type.
- Define semantic coordinate mapping.
- Define layout zones and dynamic regions.
- Define visual roles.
- Implement Manim code from the mapping and layout plan.
- Perform a protocol-based self-check before handoff.
- Prefer local repair for render-layer defects.
- Emit a blocker note only for true semantic or beat-structure blockers.

Suggested handoff shape:

```md
## Render Mapping Note
- Structure type:
- Semantic coordinate mapping:
- Layout zones:
- Dynamic regions:
- Visual roles:
- Local repair assumptions:
- Known layout risks:
```

### `references/scene-review-checklist.md`

Add failure-based render review.

Changes:

- Require checking the render mapping note or equivalent context.
- Add review of semantic mapping, geometry, containment, overlap/reflow, visual roles, and structure-specific risks.
- Require findings to include `failure class`, `structure type`, `evidence`, and `repair direction`.
- Clarify repair routing for render defects versus script or brief blockers.

Suggested finding shape:

```md
- Verdict:
- Failure class:
- Structure type:
- Evidence:
- Repair direction:
```

### `agents/scene-reviewer.md`

Align the reviewer role with the protocol.

Required behavior:

- Review render protocol compliance in addition to brief/script fidelity.
- Use failure classes when reporting findings.
- Treat missing render mapping context as a `RENDER` handoff defect.
- Avoid over-escalating local render bugs to upstream phases.
- Route only true semantic blockers to `PRE_BUILD_BRIEF`.
- Route beat-structure blockers to `SCRIPT`.

### `SKILL.md`

Update Phase 6 `RENDER`.

Changes:

- Add `references/render-protocol.md` and `references/render-structure-patterns.md` to executor-required references.
- Add render mapping handoff context to required outputs.
- Add protocol self-check summary to required outputs.
- Keep existing render evidence and independent scene review gates intact.

### `agents/openai.yaml`

Update the default prompt so dispatch instructions require:

- `scene-writer` to read the render protocol and structure patterns before creating `generated_algo_scene.py`.
- `scene-reviewer` to read the render protocol, structure patterns, scene review checklist, and reviewer agent spec before producing `scene_review_result.md`.
- Existing subagent ownership and gate requirements to remain unchanged.

## Failure Taxonomy

The reusable protocol should define these failure classes:

- `geometry/alignment failure`: an object exists but is positioned incorrectly relative to its semantic target.
- `containment failure`: content escapes its owning cell, node, panel, or label zone.
- `overlap/collision failure`: visible objects obscure or crowd each other.
- `semantic-mapping failure`: visual coordinates or visual state contradict the algorithm semantics.
- `visual-role ambiguity`: styles do not make active, referenced, settled, excluded, boundary, support, or result roles distinguishable.
- `update-lifecycle failure`: dynamic Manim updates leave stale objects, duplicates, orphaned references, or broken state tracking.
- `density/readability failure`: the scene contains too much visual load for the chosen layout or beat.

Default repair routing:

- Keep geometry, containment, overlap, role styling, reflow, safe margin, and update lifecycle defects in `RENDER`.
- Return to `SCRIPT` only when beat structure is too coarse or forces hidden sub-beat timing.
- Return to `PRE_BUILD_BRIEF` only when semantic coordinate mapping, support structure persistence, boundary convention, or visual semantics were never frozen.

## Render Preflight

The design adds a lightweight preflight inside `RENDER`, not a new formal phase.

Preflight should answer:

- What is the primary structure type?
- What is the semantic coordinate mapping?
- Which regions are data, header/index, annotation, and support regions?
- Which regions update dynamically?
- Which visual roles are used?
- Which layout risks are expected?
- Which risks are local render repairs and which would block implementation?

This preflight exists to catch expensive render ambiguities before large Manim code is written.

## Implementation Order

1. Add `references/render-protocol.md`.
2. Add `references/render-structure-patterns.md`.
3. Update `references/manim-guidelines.md`.
4. Update `agents/scene-writer.md`.
5. Update `references/scene-review-checklist.md`.
6. Update `agents/scene-reviewer.md`.
7. Update `SKILL.md`.
8. Update `agents/openai.yaml`.
9. Run consistency review.

## Consistency Review

After implementation, verify:

- Every new reference is reachable from `SKILL.md` or agent instructions.
- `scene-writer` and `scene-reviewer` use the same failure vocabulary.
- Repair routing matches existing `v3` rollback rules.
- The preflight remains lightweight and does not become a new expensive gate.
- No unrelated phases were rewritten.
- Existing script, voiceover, review, QA, and delivery gates remain intact.

## Acceptance Criteria

- `scene-writer` cannot go directly from script to ad hoc Manim code without first defining render mapping.
- `scene-writer` must identify structure type, coordinate mapping, layout zones, dynamic regions, and visual roles.
- `scene-reviewer` must classify render findings using failure classes.
- `scene-reviewer` must distinguish local render defects from true `SCRIPT` or `PRE_BUILD_BRIEF` blockers.
- `SKILL.md` Phase 6 must explicitly require the new render protocol references.
- Most geometry, containment, overlap, reflow, visual role, and update lifecycle defects remain repairable inside `RENDER`.
- Rollback is reserved for true semantic mapping gaps, beat-structure blockers, or missing upstream visual semantics.
- The protocol is reusable by future algorithm animation skills without depending on `v3` phase details.

## Risks

- The protocol may become too broad if it tries to cover every algorithm family at once.
- The new preflight could become too costly if it is treated like a full formal phase.
- Reviewers may over-escalate local render failures unless routing rules are explicit.
- Duplicating protocol content inside `manim-guidelines.md` would make future maintenance harder.

Mitigation:

- Keep the first implementation focused on common structures and common failures.
- Keep preflight as short handoff context.
- Put reusable knowledge in the protocol files and keep `v3` files as adapters.
- Make repair routing explicit in both writer and reviewer instructions.
