# Default Visual Semantics

Use these low-risk defaults for ordinary presentation choices once the upstream semantic choices are already fixed.

## Authority Split

This file owns only low-risk fallback decisions for ordinary presentation after the core design is frozen, such as ordinary colors, minor placement, easing, and local timing.

- Use this file for routine defaults when the brief and higher-level visual principles leave room for an ordinary choice.
- Do not use these defaults to replace missing core design decisions.
- Do not use this file to override the approved `animation_design.md`, the approved `pre_build_brief.md`, or `visual-language.md`.
- Do not use this file to overrule clarity concerns covered by `visual-language.md`; escalate a core gap to `DESIGN_DEVELOPMENT`.

## Scope

Use these defaults for:

- ordinary palette choices for already-defined roles
- minor pointer and label placement
- routine label wording
- routine transitions and easing
- local timing and ordinary beat pacing
- common first-class support layouts

Do not use these defaults to decide:

- movement semantics that change what the viewer learns
- search variant semantics
- pointer meaning
- visited timing
- overlay enablement
- delivery tier
- core visual semantics or role definitions
- scene structure or information hierarchy
- whether a support structure exists or persists
- viewer-facing cause/effect relationships

## Global Defaults

Unless a local artifact says otherwise:

- keep one primary focus cluster per beat
- keep base elements spatially stable across beats
- make focus styling stronger than support styling
- keep settled or resolved regions visible but calmer than the active focus
- dim excluded regions instead of deleting them unless removal is the teaching point
- keep pointer labels consistent with the algorithm's real names such as `left`, `right`, `mid`, `i`, `j`, `front`, or `back`
- place pointer labels near the structure they govern and keep a consistent side
- leave optional overlays off unless a local artifact opts in
- use restrained easing and readable local timing; neither may change the approved causal meaning or beat emphasis

## Default Role Vocabulary

If the project does not define a custom palette, keep this role vocabulary stable:

- `base`: inactive but still relevant data
- `focus`: the main object or region to inspect now
- `candidate`: a value or region under comparison, consideration, or update
- `settled`: a region whose role is already resolved for the lesson
- `excluded`: a region that is no longer active
- `support`: a secondary structure such as a queue, stack, or temp slot

## Ordinary Layout Defaults

### Arrays and Index-Based Structures

- keep the main array horizontal unless vertical layout is clearly better
- place pointer labels above or below the array, not on top of values
- keep index labels small and secondary when they are not the teaching focus
- preserve element spacing even when some elements are lifted, compared, or moved

### Search Windows and Ranges

- keep the active range visually continuous
- dim excluded regions instead of deleting them
- keep range boundaries visible while they matter
- keep the current probe visually distinct from the whole active range

### Graph Traversal

- keep node positions fixed once introduced
- keep edge styling quieter than node state styling unless edge traversal is the current focus
- show the support structure when the local contract says it matters
- let processed regions calm down instead of vanishing

## First-Class Support Defaults

### Array Sorting

- give the active compare pair the strongest focus treatment
- let the currently moved or inserted value rise or separate only when that motion is already part of the chosen semantics
- keep the settled prefix or suffix visibly marked
- keep non-active values visible so local actions still read as part of the whole array

### Binary Search and Two-Pointer Search

- show the active interval as one readable region
- keep active boundary pointers visible for the full beat in which they matter
- make the probe location distinct from both the boundaries and the excluded region
- hold the new interval long enough for shrinkage to register after a boundary update

### BFS and DFS

- separate the current node from discovered-but-not-yet-expanded nodes
- keep the support structure readable when it is part of the lesson
- show frontier emphasis through grouping, border treatment, or support-structure focus
- add neighbor-order cues only when order matters

## Text Defaults

- prefer short labels over sentence-length labels
- let on-screen text name the current rule or observation instead of repeating narration
- use captions or overlay text only when a local artifact opts in
- if a phrase can live in voiceover instead of on screen, prefer voiceover

## Motion Defaults

- move only the objects whose state the viewer needs to track
- prefer direct, legible paths over decorative motion
- remove or calm the old focus before introducing the next one
- preserve the viewer's mental map before adding flourish

## Escalation Examples

- A temp slot appears even though no local artifact confirmed one.
- A range style implies a closed interval even though the interval convention is still unspecified.
- Queue visibility is removed even though the chosen lesson depends on queue semantics.
- A scene region or persistent support structure is missing from the approved design and a default is used to invent it.

## Common Failures

- Using color to invent semantics that were never fixed upstream.
- Hiding an active support structure because the layout looks cleaner.
- Escalating routine label placement even though a normal default is enough.
- Using defaults to avoid a real semantic fork.
- Treating ordinary colors, minor placement, easing, or local timing as core design blockers when they are not explicitly material.
