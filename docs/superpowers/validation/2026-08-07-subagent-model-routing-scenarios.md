# Sub-Agent Model Routing Validation Scenarios

## Repository path convention

The repository's tracked canonical directory is `docs/` (lowercase). This fixture therefore uses `docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md`; the task brief's `Docs/` spelling is not a tracked repository path.

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
- FAIL — `script_writer` and `scene_writer` do not use explicit `gpt-5.6-sol` / `high`; each listed routing field is `Not specified`.
- FAIL — The other six roles do not inherit `gpt-5.6-luna` / `xhigh`; each listed routing field is `Not specified`.
- FAIL — Stage 5 uses `scene_writer` (`FINAL_RENDER`), not `scene_final_renderer`.
- PASS — Only `scene_writer` is permitted to edit `generated_algo_scene.py`; the Stage 5 `scene_writer` entry is not permitted to edit it.
- FAIL — The baseline dispatch plan defines no missing-or-invalid project-config handling and therefore does not produce `BLOCKED` with no fallback.

## Structural Check Evidence

```text
$ rg -n "Scenario prompt|Pass criteria|Baseline Evidence|Forward-Test Evidence|Runtime Reload Boundary" docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
7:## Scenario prompt
13:## Pass criteria
22:## Baseline Evidence
48:## Forward-Test Evidence
50:## Runtime Reload Boundary
[exit 0]

$ git diff --check HEAD^ HEAD -- docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
[no output]
[exit 0]

$ git diff --check -- docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
[no output]
[exit 0]

$ git diff --check --cached
[no output]
[exit 0]
```

## Forward-Test Evidence

Fresh-context evaluator inputs (and no design specification, baseline diagnosis, or answer):

- Skill folder: `/Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker`
- Scenario file: `/Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md`
- Role-spec paths must be literal absolute filesystem paths (spaces must not be URL-encoded).

Raw response:

```text
| Stage | Task name | Role-spec path | Model source | Effective model | Reasoning effort | Source edits permitted |
|---|---|---|---|---|---|---|
| 1 | animation_design_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-animation-design-reviewer.md | project default | gpt-5.6-luna | xhigh | No |
| 2 | script_writer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-script-writer.md | explicit spawn override | gpt-5.6-sol | high | No |
| 2 | script_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-script-reviewer.md | project default | gpt-5.6-luna | xhigh | No |
| 3 | voiceover_generator | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-voiceover-generator.md | project default | gpt-5.6-luna | xhigh | No |
| 4 | scene_writer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-writer.md | explicit spawn override | gpt-5.6-sol | high | Yes |
| 4 | scene_layout_validator | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-layout-validator.md | project default | gpt-5.6-luna | xhigh | No |
| 4 | scene_reviewer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-reviewer.md | project default | gpt-5.6-luna | xhigh | No |
| 5 | scene_final_renderer | /Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md | project default | gpt-5.6-luna | xhigh | No |
```

Forward-test criterion results:

- PASS — Exactly eight task names are present.
- PASS — Only `script_writer` and `scene_writer` use explicit `gpt-5.6-sol` / `high`.
- PASS — The other six roles use project defaults `gpt-5.6-luna` / `xhigh`.
- PASS — Stage 5 uses `scene_final_renderer`, not `scene_writer`.
- PASS — Only `scene_writer` is permitted to edit `generated_algo_scene.py`; `scene_final_renderer` is not.
- PASS — `references/subagent-delegation-protocol.md` requires `BLOCKED` with no fallback when project config is missing or invalid; the valid-config scenario therefore emits the dispatch plan rather than a fallback route.

## Runtime Reload Boundary

This validation task started before `.codex/config.toml` was added. Static checks and the fresh-context planning test above are valid, but actual Luna runtime selection must be verified from a new task started at this project root. Use:

```text
請讀取目前專案的 .codex/config.toml，使用 manim-algorithm-animation-maker 的 subagent delegation protocol，只列出八個角色的 task name、model source、effective model 與 reasoning effort；不要生成影片或修改檔案。
```
