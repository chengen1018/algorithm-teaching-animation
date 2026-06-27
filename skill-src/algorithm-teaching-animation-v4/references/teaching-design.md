# Teaching Design

## Purpose

Use this reference to decide how an algorithm animation will teach, not to redefine the design process or the `animation_design.md` contract. Every design must explain:

- what viewers should understand;
- what visible evidence teaches it;
- how each beat prepares the next beat;
- why the selected sample exposes meaningful behavior.

These explanations must be specific to the stated audience, algorithm variant, and learning goal. A sequence of correct algorithm steps is not yet a teaching design unless the viewer can use the visible evidence to form and revise a faithful mental model.

## Choosing a Mental Model

Choose one primary mental model that lets the viewer predict the algorithm's next meaningful action. State the algorithm state represented by the model, the invariant it helps explain, and the point where any analogy stops being literal. Prefer a model that remains valid across the full sample instead of changing metaphors when the algorithm becomes difficult to show.

Test the choice by asking what a viewer could correctly infer from the screen without narration. If the model makes a heuristic look guaranteed, hides required state, or depends on unexplained motion, revise it.

## Identifying Viewer Misconceptions

Identify likely misconceptions before choosing highlights or motion. For each misconception, state the incorrect conclusion a viewer might draw, the visual condition that could cause it, and the concrete evidence that will prevent or correct it.

Prioritize confusion about state boundaries, identity, ordering, commitment, and the difference between considering an item and finishing it. Do not rely on narration to repair a contradiction created by the visuals.

## Selecting a Teaching Sample

Select the smallest sample that still forces the algorithm to exhibit its defining decisions. Explain why the selected sample exposes meaningful behavior, including the operation, state transition, contrast, or edge condition that would remain hidden in an easier sample.

Avoid samples that are already solved, take only one undifferentiated path, or accidentally remove the need for the algorithm's defining operation. Include duplicates, failed comparisons, reversals, or branching only when they teach behavior required by the learning goal.

## Building a Teaching Arc

Build the arc as a progression in viewer capability: establish the problem, introduce the state that matters, demonstrate one complete reasoning cycle, vary or challenge that cycle, then consolidate the invariant and result. Each phase must add a question or piece of evidence that the next phase resolves.

State how each beat prepares the next beat. If two beats can be swapped without changing what the viewer knows, their instructional dependency is probably missing or the beats should be combined.

## Designing High-Level Beats

Define each beat by its teaching purpose, starting state, visible change, and intended viewer inference. Keep beats above camera timing and animation-library operations. A beat must expose a meaningful decision or state transition rather than merely announce that an algorithm step occurred.

For every beat, explain what viewers should understand and what visible evidence teaches it. Preserve enough prior state for viewers to compare before and after without holding hidden facts in memory.

## Connecting Visual Cause and Effect

Show cause before or with effect. First make the relevant operands, condition, or frontier visible; then show the comparison or rule; only then animate the resulting movement, elimination, discovery, or commitment. Keep the causal evidence visible long enough to connect it to the result.

Use stable visual semantics so the same color, position, connector, or motion does not change meaning between beats. When an effect changes several regions, sequence or group those changes so viewers can identify the single algorithmic cause.

## Comparing Alternatives

Compare only alternatives that materially change the mental model, visible evidence, teaching arc, or interpretation of state. Recommend one approach and explain why it better serves the audience and learning goal. For each rejected alternative, state its genuine advantage, its teaching cost, and the condition under which it would become preferable.

Do not treat cosmetic variations as competing teaching designs, and do not list options without deciding which one makes causality and state easiest to understand.

## Common Failures

- Restating pseudocode without explaining the viewer inference produced by each beat.
- Selecting a convenient sample that never reveals the algorithm's defining behavior.
- Introducing a visual state after the viewer needed it to interpret an earlier action.
- Using motion as decoration, so an effect appears without its comparison or rule.
- Removing history before it can serve as evidence for progress, exclusion, or commitment.
- Letting narration and visuals assert different state or timing.
- Adding alternatives that differ only in style and provide no teaching tradeoff.
- Repeating process gates or document schemas instead of supplying design reasoning.
