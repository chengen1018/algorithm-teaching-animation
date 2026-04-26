# Quality Rubric

Use this rubric to evaluate outputs produced by the algorithm teaching animation skill. Score each category from 1 to 5.

## Scoring Guide

- `5`: Strong. Clear, correct, and ready to use with only minor polish.
- `4`: Good. Mostly correct with small issues that do not block understanding.
- `3`: Usable. Core idea works, but there are noticeable gaps or rough edges.
- `2`: Weak. Important issues reduce correctness, clarity, or usability.
- `1`: Failing. The output does not satisfy the category.

## Algorithm Correctness

Checks whether the algorithm and state transitions are correct.

- `5`: Final result and intermediate states are correct.
- `3`: Final result is correct, but some intermediate events are incomplete or unclear.
- `1`: Algorithm behavior is wrong or the trace cannot represent the real execution.

## Trace Fidelity

Checks whether rendering follows `action_trace.json` as the source of truth.

- `5`: Manim scene uses trace events without recalculating or inventing algorithm logic.
- `3`: Scene mostly follows the trace, but includes some duplicated or hardcoded logic.
- `1`: Manim layer recomputes the algorithm or contradicts the trace.

## Beat Alignment

Checks whether `plan.md`, `teaching_script.md`, voiceover, narration manifest, and trace events align.

- `5`: Every teaching beat maps clearly to trace actions, voiceover entries, audio segments, and manifest entries.
- `3`: Most beats align, but some trace spans, narration segments, or manifest entries are vague.
- `1`: Beats, trace events, voiceover, and audio segments are disconnected.

## Teaching Clarity

Checks whether the viewer can understand the algorithm step by step.

- `5`: Each beat teaches one clear idea and builds toward the final understanding.
- `3`: Explanation is generally understandable but occasionally too dense or too fragmented.
- `1`: Viewer cannot tell what each step is meant to teach.

## Visual Readability

Checks whether the animation is visually stable and easy to follow.

- `5`: Layout, colors, labels, indicators, and focus states are stable and readable.
- `3`: Mostly readable, but some moments are crowded, ambiguous, or visually unstable.
- `1`: Visual focus is confusing or key states are hard to track.

## Narration / Audio Quality

Checks whether voiceover and beat-level audio support the teaching animation.

- `5`: Voiceover is clear, concise, beat-aligned, natural to hear, and audio timing supports the visual focus.
- `3`: Voiceover is usable, but some segments are too long, too vague, or slightly out of sync.
- `1`: Voiceover is missing, disconnected from the animation, or introduces confusing new information.

## Workflow Completeness

Checks whether the expected files are produced for a complete workflow.

- `5`: All required files are present, audio files exist, and manifest paths/durations are internally consistent.
- `3`: Most files exist, but one or more files, audio segments, or manifest entries are thin, stale, or partially inconsistent.
- `1`: Required outputs are missing or cannot be used together.

## Review Notes Template

```markdown
# Review Notes

## Scores

| Category | Score | Notes |
|---|---:|---|
| Algorithm Correctness |  |  |
| Trace Fidelity |  |  |
| Beat Alignment |  |  |
| Teaching Clarity |  |  |
| Visual Readability |  |  |
| Narration / Audio Quality |  |  |
| Workflow Completeness |  |  |

## Highest Priority Fixes

1. 
2. 
3. 

## Layer To Revise First

- `plan.md` / `teaching_script.md` / `voiceover.md` / `narration_manifest.json` / `generated_trace_script.py` / `action_trace.json` / `generated_algo_scene.py`
```
