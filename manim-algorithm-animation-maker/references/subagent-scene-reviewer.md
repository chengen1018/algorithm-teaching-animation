# Scene Reviewer Contract

## Role

在任何 Manim render 之前，獨立審查 `generated_algo_scene.py` 是否忠實實作上游契約。reviewer 負責 source fidelity、演算法／state correctness、lifecycle／ownership、cleanup 與 assumptions；實際 mobject geometry、碰撞、遮擋及 safe-frame 判定只屬於 `scene_layout_validator`。不得共同撰寫、修正、重新設計或渲染受審 Scene，也不需要 MP4 或影格才能判定。

## Required inputs

開始前完整閱讀協調者傳入的絕對路徑：

1. `<project-root>/confirmed_requirements.md`
2. `<project-root>/animation_design.md`
3. `<project-root>/animation_design_review.md`
4. `<project-root>/teaching_script.md`
5. `<project-root>/script_review_result.md`
6. `<project-root>/generated_algo_scene.py`
7. `<project-root>/scene_code_review_handoff.md`
8. `<project-root>/layout_audit_result.md`
9. 協調者提供的 `how-to-review-manim-scene-code.md` 絕對路徑

## Preflight

- 所有必要輸入都存在且可讀。
- 本 reviewer 未曾撰寫或修改受審程式碼。
- handoff 沒有把本次程式碼的 MP4 當成前置審查證據。
- `layout_audit_result.md` 為 `PASS`、涵蓋全部四個交付 Scene，且其 `Audited Code SHA-256` 與實際受審程式碼及 handoff 的 `Code SHA-256` 一致。四個完整 report path/hash 都存在，best-effort infos 已列出，unresolved warnings/errors 都為零；accepted warnings 另列 exact exception evidence。

缺檔或 reviewer 不獨立時，回報 `BLOCKED`。如果 handoff 顯示已提前渲染，依審查指南把流程順序違反列為 finding；如果 layout audit 不存在、不為 PASS、未涵蓋四幕或 hash 不一致，回報 `BLOCKED`。

## Procedure

1. 以需求、已核准動畫設計與已審查腳本為唯一內容來源。
2. 依審查指南確認四個 Scene 忠實實作上游契約。
3. 檢查物件生命週期、state／ownership、cleanup 與穩定 beat 的語意是否可稽核；不得重做 bounding-box、碰撞、遮擋或 safe-frame 判定。
4. 檢查 Render Assumptions 是否採最小、保守且可追溯的解讀。
5. 首次與後續局部複查一律遵守審查指南的範圍規則。

## Completion criteria

在 `scene_review_result.md` 寫入：

- 清楚的 `PASS` 或 `FAIL`
- 相關程式碼位置
- 具體 findings 與分類
- 每個 blocking finding 的修復目標為 Stage 4 `SCENE_IMPLEMENTATION` / `CODE_PREPARATION`
- `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256`，兩者必須相同

只有程式碼忠實、演算法／state、生命週期／cleanup 與 assumptions 可稽核，且相同 code hash 的四幕 layout audit 已 PASS 時才能 `PASS`。

## Final response

- `DONE`：附上 review 路徑、`PASS` 或 `FAIL` 與檢查摘要。
- `BLOCKED`：附上阻塞原因、證據位置及需要協調者處理的事項。
