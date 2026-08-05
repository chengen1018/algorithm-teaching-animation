# Scene Writer Contract

## Role

負責 Stage 4 `SCENE_IMPLEMENTATION` 與 Stage 5 `FINAL_RENDER_AND_QA` 中的兩次獨立指派：

1. `CODE_PREPARATION`：實作四個 Manim Scene、執行非渲染靜態檢查並建立程式碼審查 handoff。
2. `FINAL_RENDER`：只在 Stage 4 的獨立審查與 layout audit 都為 `PASS` 後，渲染完全相同且未再變更的程式碼。

協調者每次派遣必須明確指定其中一種模式。不得自行同時執行兩種模式，也不得建立 `scene_review_result.md`。

## Required inputs

兩種模式都必須完整閱讀：

1. `<project-root>/confirmed_requirements.md`
2. `<project-root>/animation_design.md`
3. `<project-root>/animation_design_review.md`
4. `<project-root>/teaching_script.md`
5. `<project-root>/script_review_result.md`
6. `<project-root>/voiceover.md`
7. `<project-root>/narration_manifest.json`
8. `<project-root>/audio/voiceover/`

`CODE_PREPARATION` 另外閱讀：

- 協調者提供的 `how-to-implement-and-verify-manim-scenes.md` 絕對路徑
- 協調者提供的 `how-to-hand-off-scene-code-for-review.md` 絕對路徑

`FINAL_RENDER` 另外閱讀：

- `<project-root>/generated_algo_scene.py`
- `<project-root>/scene_code_review_handoff.md`
- `<project-root>/scene_review_result.md`
- `<project-root>/layout_audit_result.md`
- 協調者提供的 `how-to-render-approved-manim-scenes.md` 絕對路徑

## Preflight

共同條件：

- 所有必要輸入存在且可讀。
- `animation_design_review.md` 與 `script_review_result.md` 都已清楚判定為 `PASS`。
- 四幕設計、腳本、旁白與音檔彼此一致。

`FINAL_RENDER` 額外確認：

- `scene_review_result.md` 明確為 `PASS`。
- `layout_audit_result.md` 明確為 `PASS`，並完整涵蓋四個交付 Scene。
- 下列五個程式碼身分完全一致：
  1. 目前 `generated_algo_scene.py` SHA-256。
  2. handoff 的 `Code SHA-256`。
  3. layout result 的 `Audited Code SHA-256`。
  4. scene review 的 `Reviewed Code SHA-256`。
  5. scene review 的 `Layout-audited Code SHA-256`。
- `layout_audit_result.md` 的 `Runner SHA-256`、`Python version`、`Manim version`、`Frame width`、`Frame height`、`Renderer/profile/quality` 與 `Font/font-resolution evidence` 都存在，且逐欄符合目前核准的正式 render environment/profile；無法比對的欄位視為不一致。

任何條件不成立時不得猜測、修改 gate 文件或提前執行後續工作，回報 `BLOCKED`。

## CODE_PREPARATION procedure

1. 把已通過 gate 的上游文件視為可執行契約。
2. 依實作指南先規劃每個 Scene 的 peak state、groups、候選內容、pointer state 與 phase ownership。
3. 建立四個獨立 Scene；每幕結尾淡出至空白，下一幕從空白淡入。
4. 完整重讀程式碼，執行靜態 self-audit，確認語意、演算法狀態、物件生命週期、cleanup 與 assumptions 可稽核。
5. 修正程式碼層級可確認的過期 helper、錯誤 state reference、遺漏 cleanup 與不一致 assumptions。
6. 建立包含 Static Verification 與 Render Assumptions 的 pre-render handoff。

在此模式禁止執行任何 Manim render、preview、低畫質渲染或合併影片。

## FINAL_RENDER procedure

1. 再次確認 Stage 4 的 `scene_review_result.md = PASS` 與 `layout_audit_result.md = PASS`，四個 Scene 都受 layout audit 涵蓋，並重新計算目前 source hash。
2. 在第一個 render command 前，逐一記錄並比較目前 source、handoff、layout result、scene review 的 reviewed identity、scene review 的 layout-audited identity 這五個 SHA-256；任一缺漏或不一致都回報 `BLOCKED`。
3. 逐欄比較 layout result 的 runner、Python、Manim、frame width、frame height、renderer/profile/quality 與 font/font-resolution evidence，確認它們仍與目前核准的 render environment/profile 相容；任一欄位缺漏、改變或無法證明相容都回到 Stage 4 `LAYOUT_VERIFICATION`。
4. Gate 通過後不得再修改 `generated_algo_scene.py`；依渲染指南渲染四個 Scene。
5. 依核准順序合併最終影片。
6. 建立並完整填妥 `render_manifest.md`，記錄渲染輸出；在派遣 `rendered_media_validator` 前凍結 manifest，之後 writer 與 validator 都不得修改它。

若技術修復需要改動 `generated_algo_scene.py`，立即停止，不得繼續渲染；回報 `BLOCKED`，讓舊 PASS 失效並回到 `CODE_PREPARATION` 與獨立審查。

## Completion criteria

- `CODE_PREPARATION`：只產出 `generated_algo_scene.py` 與 `scene_code_review_handoff.md`；完成完整重讀與靜態 self-audit，且 handoff 明確記錄 `Manim render performed: NO`。
- `FINAL_RENDER`：四個 Scene MP4、合併影片與已完整填妥且凍結的 manifest 都存在；manifest 不含尚未產生的 DELIVERY_QA verdict placeholder。

## Final response

- `DONE`：附上模式、輸出路徑與完成檢查摘要。
- `BLOCKED`：附上模式、阻塞原因、證據路徑及需要協調者處理的事項。
