# Sub-Agent Model Routing Validation Scenarios

## Scenario prompt

```text
Use the Manim Algorithm Animation Maker skill from the supplied absolute path. Do not create animation artifacts and do not modify files. Return only the complete Sub-Agent dispatch plan as a table with stage, task name, role-spec path, model source, effective model, reasoning effort, and whether source edits are permitted. Include the final-render agent.
```

## Pass criteria

- Exactly eight task names are present.
- Only `script_writer` and `scene_writer` use explicit `gpt-5.6-sol` / `high`.
- The other six roles inherit project defaults `gpt-5.6-luna` / `xhigh`.
- Stage 5 uses `scene_final_renderer`, not `scene_writer`.
- Only `scene_writer` may edit `generated_algo_scene.py`; `scene_final_renderer` may not.
- Missing or invalid project config produces `BLOCKED` with no fallback.

## Baseline Evidence

```text
| Stage | Task name | Role-spec path | Model source | Effective model | Reasoning effort | Source edits permitted |
|---|---|---|---|---|---|---|
| 1 | animation_design_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-animation-design-reviewer.md | Not specified | Not specified | Not specified | No |
| 2 | script_writer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-script-writer.md | Not specified | Not specified | Not specified | No |
| 2 | script_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-script-reviewer.md | Not specified | Not specified | Not specified | No |
| 3 | voiceover_generator | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-voiceover-generator.md | Not specified | Not specified | Not specified | No |
| 4 | scene_writer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-writer.md | Not specified | Not specified | Not specified | Yes |
| 4 | scene_layout_validator | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-layout-validator.md | Not specified | Not specified | Not specified | No |
| 4 | scene_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-reviewer.md | Not specified | Not specified | Not specified | No |
| 5 | scene_writer (`FINAL_RENDER`) | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-writer.md | Not specified | Not specified | Not specified | No |
```

Baseline criterion results:

- PASS — Exactly eight task names are present.
- FAIL — No role has the required explicit or inherited model/reasoning mapping: every `Model source`, `Effective model`, and `Reasoning effort` value is `Not specified`.
- FAIL — Stage 5 uses `scene_writer` (`FINAL_RENDER`), not `scene_final_renderer`.
- PASS — Only `scene_writer` is permitted to edit `generated_algo_scene.py`; the Stage 5 `scene_writer` entry is not permitted to edit it.
- FAIL — The baseline dispatch plan defines no missing-or-invalid project-config handling and therefore does not produce `BLOCKED` with no fallback.

## Forward-Test Evidence

## Runtime Reload Boundary
