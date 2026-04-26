# V2 Ideas

Use this file as a scratchpad for possible improvements to the v2 skill. Ideas here are not committed design decisions yet.

## Candidate Improvements

- Add `subtitle_script.md` to all examples so examples match the current complete workflow.
- Add `review_notes.md` to representative examples to demonstrate expected review output.
- Add a dedicated review rubric reference if repeated evaluations need a runtime-facing checklist.
- Add a data structure state transition example, such as heap insert or union-find.
- Add failure cases that show common bad outputs and why they are bad.
- Clarify when `action_trace.json` should be read from disk versus embedded for a self-contained scene.
- Consider providing a small reusable Manim layout pattern for subtitle-safe area, title, main visualization, and status labels.

## Observed Issues

- Some existing examples may not include every output required by the current workflow.
- DP example synchronization should be checked across `generated_trace_script.py`, `action_trace.json`, `teaching_script.md`, `plan.md`, and `generated_algo_scene.py`.
- BFS frontier and visited transitions may need more visual dwell time.
- Long teaching explanations can accidentally become long on-screen subtitles.

## Questions To Resolve

- Should v2 keep examples inside the runtime skill package, or move larger examples into development-only fixtures?
- Should the skill require `review_notes.md` for every complete workflow, or only for deliverables and benchmark runs?
- Should trace schemas be strict and versioned, or remain flexible for new algorithms?
- Should examples use real generated files only, or include hand-polished golden versions?

## Promising Experiments

- Generate the same algorithm with v1 and v2, then score both using `quality-rubric.md`.
- Test one ambiguous user request and measure whether v2 asks the right clarification or makes a safe assumption.
- Test one complex DP example and inspect whether beat structure, trace events, and subtitles stay aligned.
