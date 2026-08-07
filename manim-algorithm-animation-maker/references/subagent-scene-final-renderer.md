# Scene Final Renderer Contract

## Role

只負責 Stage 5 `FINAL_RENDER`。只能使用 Stage 4 `Exit gate` 已核准的 immutable source 與 render profile；不得建立或修改 source、handoff、layout result 或 scene review。

## Required inputs

必須完整閱讀：

1. `<project-root>/generated_algo_scene.py`
2. `<project-root>/scene_code_review_handoff.md`
3. `<project-root>/layout_audit_result.md`
4. `<project-root>/scene_review_result.md`
5. 協調者提供的 `how-to-render-approved-manim-scenes.md` 絕對路徑
6. 協調者提供的 approved render profile
7. 協調者提供的四個 Scene class 與核准順序

## Gate ownership

Stage 4 `Exit gate` 是唯一的渲染前 gate。Renderer 直接接受已核准的 source、handoff、layout result、scene review 與 render profile，不重做 hash、`PASS` 或 environment preflight。任一必要輸入無法讀取時，回報 `BLOCKED`。

## Procedure

1. 依核准順序分別渲染四個 Scene，記錄每個實際 command、輸出路徑與 exit code。
2. 依同一核准順序合併四個 Scene MP4，記錄 concat input list、command、combined MP4 路徑與 exit code。
3. 建立完整的 `render_manifest.md`，記錄 Stage 4 提供的 immutable source hash、render profile、所有 commands、exit codes 與五個 MP4 的絕對路徑。
4. 在 coordinator 執行 `DELIVERY_CHECK` 前凍結 `render_manifest.md`；凍結後不得修改。

## Failure routing

任何需要修改 source、上游契約或 Stage 4 evidence 的問題都必須立即回報 `BLOCKED`，不得在 Stage 5 修補。source 或場景程式碼問題交回 Stage 4 `CODE_PREPARATION`；layout-affecting environment/profile 問題交回 Stage 4 `LAYOUT_VERIFICATION`；需求、設計、腳本、旁白或音訊契約問題交回對應的上游 Stage。

## Completion criteria

- 依核准順序渲染的四個 Scene MP4 存在。
- combined MP4 存在。
- 完整且 frozen 的 `render_manifest.md` 存在。
- immutable source 與 Stage 4 gate evidence 都未改變。

## Final response

- `DONE`：回報四個 Scene MP4、combined MP4 與 frozen manifest 的絕對路徑，並列出實際 commands 與 exit codes。
- `BLOCKED`：回報阻塞證據、相關路徑與必須退回的 Stage。
