# Algorithm Teaching Animation Skill

這是一個 Codex skill，用來把演算法說明轉成 deterministic、可教學的動畫工作流。

此 skill 會引導 Codex 完成規劃、教學腳本設計、deterministic trace 產生、Manim 場景生成，以及可選的 beat-aligned voiceover 素材。

## Repository Layout（儲存庫結構）

- `skill-src/algorithm-teaching-animation-v2/` - 可安裝的 skill package
- `skill-src/algorithm-teaching-animation-v2/SKILL.md` - 主要 skill 指令
- `skill-src/algorithm-teaching-animation-v2/references/` - 聚焦於各工作階段的參考文件
- `skill-src/algorithm-teaching-animation-v2/examples/` - 常見演算法類型的範例輸出
- `SKILL_INDEX.md` - 開發用的本機閱讀索引

## Install Locally（本機安裝）

將 skill package 複製或建立 symlink 到你的 Codex skills 目錄：

```powershell
Copy-Item -Recurse `
  -LiteralPath ".\skill-src\algorithm-teaching-animation-v2" `
  -Destination "$env:USERPROFILE\.codex\skills\algorithm-teaching-animation-v2"
```

接著重新啟動 Codex，或重新載入 skills。

## What The Skill Produces（輸出內容）

對於完整工作流，此 skill 預期會產生以下 artifacts：

- `plan.md`
- `teaching_script.md`
- `voiceover.md`
- `narration_manifest.json`
- `audio/voiceover/*.wav`
- `generated_trace_script.py`
- `action_trace.json`
- `generated_algo_scene.py`

Rendered videos、Manim caches、generated audio 與 Python bytecode 會刻意被 Git 忽略。
