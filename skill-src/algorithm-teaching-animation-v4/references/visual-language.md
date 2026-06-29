# Visual Language

Use these viewer-facing rules to keep algorithm state, control, and progress legible.

## Authority Split

`DESIGN_DEVELOPMENT` owns core visual semantics, scene structure, persistent support structures, information hierarchy, and the viewer-facing cause/effect relationships that make algorithm state teachable. Those decisions must be defined in the reviewed and approved `animation_design.md`.

This file supplies higher-level viewer-facing principles for judging whether those design choices are clear, coherent, and semantically stable.

- Use this file to decide whether a default presentation choice is clear enough for the viewer.
- If an approved design or brief conflicts with these clarity or semantic-stability principles, treat the conflict as an upstream contract defect. Downstream agents must not choose precedence or repair the conflict locally.
- Route to CONTRACT when `pre_build_brief.md` mistranslated the approved `animation_design.md`. Route to `DESIGN_DEVELOPMENT` when the approved design itself contains the conflict, then require independent review, exact-version external reapproval, CONTRACT reconversion, and separate brief approval before downstream work resumes.
- `default-visual-semantics.md` is lowest authority and must never resolve a conflict among the approved design, approved brief, and visual-language principles.
- Do not use this file to introduce, repair, or silently complete core semantics that were never fixed upstream.
- A downstream visual-language check that finds missing core semantics, scene structure, persistent support structures, information hierarchy, or cause/effect must route the gap to `DESIGN_DEVELOPMENT`; it must not fix the gap locally.

## Core Principles

- teaching clarity beats decorative motion
- stable semantics beat visual variety
- one dominant focus per beat
- resolved regions should remain understandable without competing with the active action
- layout stability is part of the lesson

## Semantic Stability

Every persistent visual cue should keep one stable meaning inside the animation.

This includes:

- role color
- border or fill emphasis
- pointer style
- support-structure treatment
- excluded-region treatment

If the viewer has to relearn a cue midway through the animation, the visual language failed.

## Focus Control

Each beat should make these things obvious:

- what to look at first
- what matters second
- what is now background context

Common focus tools:

- stronger contrast
- local motion
- temporary enlargement or separation
- quieting non-active regions

Do not highlight everything at once.

## Layout Stability

- keep primary structures anchored
- avoid full-scene reflow for local updates
- keep pointer travel paths easy to track
- introduce new support structures only when the local contract requires them

## Role Differentiation

At minimum, the viewer should be able to distinguish:

- base data
- current focus
- candidate or active comparison target
- settled progress
- excluded region
- support structure

## Support Structures

Queues, stacks, temp slots, helper windows, and similar structures are not neutral decoration.

- If the local contract says the structure matters, keep it visible when the lesson depends on it.
- If the local contract says it is unnecessary, do not add it for flair.
- Style support structures as secondary, but not invisible.

Whether a support structure exists or persists is a core design decision. This reference judges the clarity of the approved choice; it does not invent that choice downstream.

## Text and Labels

- keep labels short and concrete
- prefer naming roles over writing full explanations on screen
- place labels consistently
- use overlay text only when a local artifact opts in

## Motion Rules

- motion should clarify cause and effect
- active motion should match the teaching point of the beat
- use pauses to confirm progress, not to decorate transitions
- if motion hides role distinctions, simplify it

## Mode-Specific Emphasis

### Array Sorting

- separate the active pair from the settled region
- make progress boundaries easy to read
- keep the whole row visible so local actions still feel global

### Binary Search and Interval or Candidate-Region Narrowing Two-Pointer Search

- keep the active interval visually coherent
- distinguish boundary pointers from the active probe
- make elimination visible without deleting context too early

### BFS and DFS

- separate current expansion from already discovered structure
- keep traversal support structures readable when they are part of the lesson
- make ordering cues legible when order affects understanding

## Overlay Safety

- do not reserve overlay space by default
- do not add subtitles or callouts just because room exists
- do not infer overlays from delivery tier alone
- if overlays are enabled, keep them off the teaching-critical region

## Escalation Examples

- A highlight treatment makes `candidate` and `settled` look identical.
- A new support structure is added only to make the frame look fuller.
- An overlay placement covers the active comparison or active interval.
- A downstream phase has to invent a scene region or causal visual cue because the approved design omitted it.

## Common Failures

- Using a style flourish that changes role meaning.
- Hiding teaching-critical structures to make the frame cleaner.
- Treating every active object as equally important.
- Letting overlays crowd the main lesson.
