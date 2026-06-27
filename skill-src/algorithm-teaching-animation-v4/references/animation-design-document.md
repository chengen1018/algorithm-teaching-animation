# Animation Design Document

## Purpose

`animation_design.md` is the authoritative design contract for how an algorithm animation teaches and presents its subject. It records the approved mental model, visual system, teaching progression, high-level beats, user decisions, and known risks before downstream production begins.

The document must be specific enough for design review and later implementation without turning into scene code or a frame-by-frame production script.

## Confirmation Rule

The user must explicitly approve the exact version of `animation_design.md` for which independent review produced `animation_design_review.md` with a `PASS` result. The user may edit `animation_design.md`. Every user edit creates a new version, invalidates prior review, and requires re-review before approval can be accepted. Edit impact determines whether re-review is full or delta; no edit bypasses re-review. Silence, inactivity, or editing the file alone does not count as approval.

Approval applies only to the exact reviewed version. Any later edit creates another new version and requires review and explicit confirmation again.

The orchestrator must record exact-version user approval externally in the workflow gate. It must not mutate `animation_design.md` to record approval, approval status, an approval reference, or review metadata.

## Required Sections

### Design Goal and Audience

State what the viewer should understand by the end, the intended audience, assumed prior knowledge, and the desired depth. Use observable learning outcomes rather than a generic goal such as “explain the algorithm.”

### Algorithm Variant and Semantics

Name the exact algorithm variant and define the behavior that affects the animation: state, invariants, tie handling, termination, indexing or boundary conventions, and expected output. Distinguish required semantics from presentation choices.

### Primary Mental Model

Describe the single main conceptual model the viewer should use to reason about the algorithm. Explain how it maps to actual algorithm state and where the analogy or simplification stops being literal.

### Viewer Misconceptions to Prevent

List the most likely incorrect conclusions and the design response that prevents each one. Prioritize misconceptions caused by hidden state, ambiguous motion, misleading visual persistence, or confusion between a heuristic and a guarantee.

### Sample Input and Rationale

Give the exact sample input and expected result. Explain why it exposes the important decisions, state changes, edge behavior, or contrast needed for teaching. Avoid an example that is correct but visually trivial.

### Core Visual Metaphor and Visual Semantics

Define the central visual metaphor and the stable meaning of position, color, shape, labels, highlights, motion, connectors, and state changes. Every encoded property must have one clear meaning; decorative styling must not imply algorithmic state.

### Structure Presentation

Specify how the algorithm's data structures and control state appear, how they relate spatially, what remains persistent, and what transforms. Explain how the viewer can locate the current item, active region, candidates, committed results, and relevant history.

### Scene Structure and Information Hierarchy

Define the major scene regions and the priority of information within them. State what is primary, supporting, persistent, transient, or intentionally omitted. Prevent simultaneous elements from competing for attention.

### Teaching Arc

Describe the instructional progression: motivation, setup, first concrete action, repeated reasoning pattern, pivotal insight or contrast, completion, and takeaway. Connect each phase to the mental model the viewer is building.

### High-Level Animation Beats

List the major beats in order. For each beat, state the teaching purpose, visible algorithm state, meaningful transition, and viewer takeaway. Keep beats above implementation-level timing and Manim operations.

### Recommended Design and Alternatives

Present the recommended design with its rationale and meaningful tradeoffs. Include only material alternatives, explaining when each would be preferable and why it was not selected. Do not list options without making a recommendation.

### Incorporated User Decisions

Record user decisions faithfully, including the question context when needed to prevent reinterpretation. Distinguish direct user choices from designer defaults and derived consequences.

### Risks and Best-Effort Notes

Record unresolved low-impact details, assumptions, accessibility concerns, visual density risks, technical uncertainties, and simplifications. State the chosen best-effort handling and whether any item could trigger rollback if later evidence raises its impact.

### DESIGN_READY Self-Check

Mark each DESIGN_READY condition as pass or fail and cite the section that supports the result. The check must cover goal and audience, semantics, mental model, misconceptions, sample input, visual metaphor and semantics, structure presentation, scene structure and information hierarchy, teaching arc, high-level beats, recommendation and tradeoffs, incorporated decisions, documented risks and defaults, and zero unresolved blocking core questions.

Do not mark the document ready if any required section is missing, internally inconsistent, materially ambiguous, or awaiting a core answer.

## Writing Rules

- Write for reviewers and downstream implementers; use precise, testable design statements.
- Separate algorithm truth, visual encoding, teaching intent, user decisions, and best-effort assumptions.
- Use one stable term for each concept and preserve code identifiers or formal notation where precision matters.
- Describe what the viewer sees and learns, not only what the algorithm does.
- Keep high-level beats free of low-level animation API calls and frame-by-frame choreography.
- Make recommendations explicit and pair each with rationale and tradeoffs.
- Preserve user answers faithfully; do not rewrite them into a different decision.
- Use concise diagrams or tables only when they clarify mappings, hierarchy, or sequence.
- Keep every required heading even when its content is brief; write `None` with a reason instead of silently omitting a section.

## Failure Conditions

The document fails review if it:

- omits or renames a required section;
- leaves algorithm semantics or the primary mental model ambiguous;
- describes an attractive visual treatment without stable visual semantics;
- restates algorithm steps without designing the teaching arc and viewer experience;
- gives high-level beats that hide important state changes or causality;
- lists alternatives without a recommendation, rationale, and tradeoffs;
- misstates, loses, or silently overrides a user decision;
- treats unresolved low-impact details as blockers or hides material uncertainty as a best-effort note;
- marks DESIGN_READY as passed without evidence from the document;
- treats silence, inactivity, editing alone, or an unreviewed edit as user approval.

## Recommended Template

```markdown
# Animation Design: <Algorithm and Variant>

## Design Goal and Audience
...

## Algorithm Variant and Semantics
...

## Primary Mental Model
...

## Viewer Misconceptions to Prevent
...

## Sample Input and Rationale
...

## Core Visual Metaphor and Visual Semantics
...

## Structure Presentation
...

## Scene Structure and Information Hierarchy
...

## Teaching Arc
...

## High-Level Animation Beats
...

## Recommended Design and Alternatives
...

## Incorporated User Decisions
...

## Risks and Best-Effort Notes
...

## DESIGN_READY Self-Check
- [ ] Design goal and audience are explicit — evidence: ...
- [ ] Algorithm variant and semantics are unambiguous — evidence: ...
- [ ] Primary mental model is faithful and bounded — evidence: ...
- [ ] Misconceptions and preventions are identified — evidence: ...
- [ ] Sample input and teaching rationale are suitable — evidence: ...
- [ ] Visual metaphor and semantics are stable — evidence: ...
- [ ] Structure presentation is defined — evidence: ...
- [ ] Scene structure and information hierarchy are explicit — evidence: ...
- [ ] Teaching arc and high-level beats expose state and causality — evidence: ...
- [ ] Recommendation, alternatives, rationale, and tradeoffs are recorded — evidence: ...
- [ ] User decisions are incorporated faithfully — evidence: ...
- [ ] Risks and best-effort notes are explicit — evidence: ...
- [ ] Zero unresolved blocking core questions remain — evidence: ...
```
