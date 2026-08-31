# How to Review Manim Scene Code

本文件說明獨立 scene-reviewer 如何在任何 Manim render 之前審查 `generated_algo_scene.py`。這是程式碼語意審查，不是幾何或視覺審查：reviewer 不需要 MP4、不執行 render、不查看影格、不執行 bounding-box 判定，也不根據畫面外觀判定 `PASS` 或 `FAIL`。

## 必要輸出

回傳 `scene_review_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- 審查結果必須由獨立 reviewer 撰寫
- reviewer 負責 Stage 4 `SCENE_IMPLEMENTATION` 的 `CONTRACT_REVIEW` gate 程式碼審查
- 分類好的阻塞性 findings
- 指向程式碼位置的 evidence references
- 修復方向：Stage 4 `SCENE_IMPLEMENTATION` 的 `CODE_PREPARATION`

使用以下 finding 類別：

- `implementation fidelity`
- `algorithm/state correctness`
- `lifecycle/ownership and cleanup`

## 審查輸入

審查時必須讀取派遣訊息中的每個 `Required inputs`，並以角色定義的輸入標籤指稱它們。Preflight 要求所有 `Required inputs` 都存在且可讀，且 `Layout audit result` 為 `PASS` 並完整涵蓋五個交付 Scene；否則回報 `BLOCKED`。Reviewer 直接審查目前的 `Scene source`。

## 程式碼審查問題

### Source Fidelity

- 是否有五個 `Scene` 類別，並依 `animation_design.md` 的 Scene 1–5 核准順序忠實實作每幕的教學責任與主要 beat？
- 程式碼是否忠實實作已確認需求、已核准設計與已審查 script，而非新增自己的演算法步驟或教學目標？
- 已核准為必要的 support structure、pointer 意義與 state 更新是否在程式碼中可追溯？
- Scene 4 的 case labels、assumptions、工作單位與逐 beat 呈現是否和已核准 derivation 一致？Complexity claim 的數學正確性由 design review 擁有，scene-reviewer 只檢查 source fidelity，不重做該數學審查。

### Algorithm, State, Lifecycle, and Cleanup

- `Transform`、`ReplacementTransform` 與可替換物件的 current reference 是否一致？
- helper、label、highlight 與 support structure 是否有明確的建立、更新、淡出或移除時點？
- 各 Scene 是否自行建立與清理物件，並在程式碼中明確淡出至空白後再銜接下一幕？

實際 mobject geometry、bounding box、碰撞、遮擋、safe-frame、文字容量與 magic shift 的判定，完全以 `layout_audit_result.md` 為準；scene-reviewer 不得重做或取代該檢查。

### Maintainability

- 語意常數、builders、groups 與 visibility ownership 是否足以讓演算法與狀態意圖被稽核？
- 是否存在無法追溯至上游契約的演算法或教學解讀？

## 審查範圍

第一次程式碼審查必須檢查完整 `generated_algo_scene.py`。之後只有變更範圍明確、且 reviewer 能從程式碼 diff 確認受影響 Scene、helper 與相鄰 state 的情況下，才可做局部複查；影響不確定時，必須重新檢查完整檔案。

每個 finding 的修正目標為 Stage 4 `SCENE_IMPLEMENTATION` 的 `CODE_PREPARATION`。scene-reviewer 不得修改 `generated_algo_scene.py` 或任何 render 產物。

## PASS 標準

只有在以下條件成立時才能通過：

- `generated_algo_scene.py` 忠實實作已確認需求、已核准設計與已審查 script
- 程式碼中的演算法狀態、物件生命週期、ownership 與 Scene cleanup 可稽核
- `layout_audit_result.md = PASS` 且涵蓋所有五個 Scene
- `scene_review_result.md` 由獨立 reviewer 撰寫，而非 scene-writer

## 常見失敗

- 要求先渲染或要求 MP4 才開始程式碼審查。
- 因程式通過語法或靜態檢查就通過，即使它發明了語意或遺漏 script beat。
- 因為沒有影片，就跳過演算法 state、生命週期、ownership 或 cleanup 的程式碼推理。
- scene-reviewer 重做 geometry、bounding-box、碰撞、遮擋或 safe-frame 判定，而不是使用 `layout_audit_result.md` 的 evidence。
- 把不可追溯或新增教學內容的問題誤標成 styling。
- 回傳 `FAIL` 卻沒有指向相關程式碼或說明修復方向。
- 用過去的 MP4、截圖或畫面外觀作為渲染前程式碼審查的證據。
