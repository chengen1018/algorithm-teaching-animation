# Algorithm Teaching Animation Skill

Codex skill for turning algorithm explanations into deterministic, teachable animation workflows.

The skill guides Codex through planning, teaching-script design, deterministic trace generation, Manim scene generation, and optional beat-aligned voiceover assets.

## Repository Layout

- `skill-src/algorithm-teaching-animation-v2/` - installable skill package
- `skill-src/algorithm-teaching-animation-v2/SKILL.md` - main skill instructions
- `skill-src/algorithm-teaching-animation-v2/references/` - focused workflow references
- `skill-src/algorithm-teaching-animation-v2/examples/` - example outputs for common algorithm types
- `design-notes/` - design notes, review rubric, and change log
- `quick-sort-animation/` - local quick sort sample workspace
- `SKILL_INDEX.md` - local reading index for development

## Install Locally

Copy or symlink the skill package into your Codex skills directory:

```powershell
Copy-Item -Recurse `
  -LiteralPath ".\skill-src\algorithm-teaching-animation-v2" `
  -Destination "$env:USERPROFILE\.codex\skills\algorithm-teaching-animation-v2"
```

Then restart Codex or reload skills.

## What The Skill Produces

For a complete workflow, the skill expects these artifacts:

- `plan.md`
- `teaching_script.md`
- `voiceover.md`
- `narration_manifest.json`
- `audio/voiceover/*.wav`
- `generated_trace_script.py`
- `action_trace.json`
- `generated_algo_scene.py`

Rendered videos, Manim caches, generated audio, and Python bytecode are intentionally ignored by Git.

