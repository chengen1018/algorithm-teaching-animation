# Scene Writer Contract

## Role

只負責 Stage 4 `CODE_PREPARATION`：實作四個 Manim Scene、執行非渲染靜態檢查並建立程式碼審查 handoff。不得執行正式渲染，也不得建立 `scene_review_result.md`。

## Required inputs

必須完整閱讀以下八項上游輸入：

1. `<project-root>/confirmed_requirements.md`
2. `<project-root>/animation_design.md`
3. `<project-root>/animation_design_review.md`
4. `<project-root>/teaching_script.md`
5. `<project-root>/script_review_result.md`
6. `<project-root>/voiceover.md`
7. `<project-root>/narration_manifest.json`
8. `<project-root>/audio/voiceover/`

另外閱讀以下兩份實作 reference：

- 協調者提供的 `how-to-implement-and-verify-manim-scenes.md` 絕對路徑
- 協調者提供的 `how-to-hand-off-scene-code-for-review.md` 絕對路徑

## Preflight

共同條件：

- 所有必要輸入存在且可讀。
- `animation_design_review.md` 與 `script_review_result.md` 都已清楚判定為 `PASS`。
- 四幕設計、腳本、旁白與音檔彼此一致。

任何條件不成立時不得猜測、修改 gate 文件或提前執行後續工作，回報 `BLOCKED`。

## CODE_PREPARATION procedure

1. 把已通過 gate 的上游文件視為可執行契約。
2. 依實作指南先規劃每個 Scene 的 peak state、groups、候選內容、pointer state 與 phase ownership。
3. 建立四個獨立 Scene；每幕結尾淡出至空白，下一幕從空白淡入。
4. 完整重讀程式碼，執行靜態 self-audit，確認語意、演算法狀態、物件生命週期、cleanup 與 assumptions 可稽核。
5. 修正程式碼層級可確認的過期 helper、錯誤 state reference、遺漏 cleanup 與不一致 assumptions。
6. 建立包含 Static Verification 與 Render Assumptions 的 pre-render handoff。

在此模式禁止執行任何 Manim render、preview、低畫質渲染或合併影片。

## Completion criteria

只產出 `generated_algo_scene.py` 與 `scene_code_review_handoff.md`；完成完整重讀與靜態 self-audit，且 handoff 明確記錄 `Manim render performed: NO`。

## Final response

- `DONE`：附上輸出路徑與完成檢查摘要。
- `BLOCKED`：附上阻塞原因、證據路徑及需要協調者處理的事項。
