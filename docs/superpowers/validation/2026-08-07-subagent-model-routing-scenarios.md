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
- Scenario file: `/Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md`
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

## Static Validation Evidence

The default `/usr/bin/python3` is Python 3.9.6 and lacks both `tomllib` and PyYAML. The following literal commands use installed Python 3.11 and a temporary, non-project PyYAML location at `/private/tmp/task4-model-routing-python-deps`.

```text
$ PYTHONPATH=/private/tmp/task4-model-routing-python-deps python3.11 /Users/lichengen/.codex/skills/.system/skill-creator/scripts/quick_validate.py "/Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker"
Skill is valid!
[exit 0]

$ python3.11 -c 'from pathlib import Path; import tomllib; tomllib.loads(Path(".codex/config.toml").read_text())'
[no output]
[exit 0]

$ rg -n "FINAL_RENDER" manim-algorithm-animation-maker/references/subagent-scene-writer.md
[no output]
[exit 1 — expected: no matches]

$ rg -n "scene_final_renderer" manim-algorithm-animation-maker/SKILL.md manim-algorithm-animation-maker/references/subagent-delegation-protocol.md manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
manim-algorithm-animation-maker/SKILL.md:217:依委派協定派遣 task name `scene_final_renderer` 的 subagent：
manim-algorithm-animation-maker/references/subagent-delegation-protocol.md:33:| 正式場景渲染與合併 | `scene_final_renderer` | `references/subagent-scene-final-renderer.md` | project default | `gpt-5.6-luna` | `xhigh` |
manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md:7:Stage 4 的 `Exit gate` 是唯一的渲染前 gate。協調者將 Stage 4 的四份 gate 證據、已核准的 source version 與 render profile 直接交給 `scene_final_renderer`；本文件不再建立第二份 `Entry gate`，也不要求在第一個 render command 前重做相同的 hash、PASS 或 environment preflight。
[exit 0]

$ git diff --check
[no output]
[exit 0]

$ git status --short
 M manim-algorithm-animation-maker/SKILL.md
 M manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
 M manim-algorithm-animation-maker/references/subagent-scene-writer.md
[exit 0]
```

## Runtime Reload Boundary

This validation task started before `.codex/config.toml` was added. Static checks and the fresh-context planning test above are valid, but actual Luna runtime selection must be verified from a new task started at this project root. Use:

```text
請讀取目前專案的 .codex/config.toml，使用 manim-algorithm-animation-maker 的 subagent delegation protocol，只列出八個角色的 task name、model source、effective model 與 reasoning effort；不要生成影片或修改檔案。
```
