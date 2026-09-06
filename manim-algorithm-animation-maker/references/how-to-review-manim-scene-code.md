# How to Review Manim Scene Code

本文件說明獨立 scene-reviewer 如何在任何 Manim render 之前審查 `generated_algo_scene.py`。這是程式碼語意審查，不是幾何或視覺審查：reviewer 不需要 MP4、不執行 render、不查看影格、不執行 bounding-box 判定，也不根據畫面外觀判定 `PASS` 或 `FAIL`。

## 必要輸出

回傳 `scene_review_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- `Reviewed Code SHA-256`，必須是 reviewer 實際審查的 `generated_algo_scene.py` 內容 hash
- `Layout-audited Code SHA-256`，必須從 `layout_audit_result.md` 取得且與 Reviewed Code SHA-256 相同
- 審查結果必須由獨立 reviewer 撰寫
- reviewer 負責 Stage 4 `SCENE_IMPLEMENTATION` 的 `CONTRACT_REVIEW` gate 程式碼審查
- 分類好的阻塞性 findings
- 指向程式碼位置的 evidence references
- 修復方向：Stage 4 `SCENE_IMPLEMENTATION` 的 `CODE_PREPARATION`

使用以下 finding 類別：

- `implementation fidelity`
- `algorithm/state correctness`
- `lifecycle/ownership and cleanup`
- `source mismatch`

## 審查輸入

審查時應對照：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- 已審查的 `teaching_script.md`
- `generated_algo_scene.py`
- `scene_code_review_handoff.md`
- `layout_audit_result.md`

`scene_code_review_handoff.md` 的 Reviewed Source 用來識別受審程式碼版本；其 Code SHA-256 必須與 reviewer 實際讀取的 `generated_algo_scene.py` 一致。`layout_audit_result.md` 必須為 `PASS`、完整涵蓋四個交付 Scene，且其 `Audited Code SHA-256` 必須與上述 hash 相同。它也必須逐幕引用完整 machine-readable report path/hash，列出 best-effort infos，並顯示 unresolved warnings 與 errors 為零；accepted warnings 必須與 exact exception path/hash 分開記錄。Static Verification 必須明確記錄 `Manim render performed: NO`；如果本次程式碼已被先行渲染，將流程順序違反列為 blocking finding。審查 `Render Assumptions` 時，每一項非平凡解讀都必須最小、保守、可追溯至其負責的來源範圍，且不得新增演算法步驟或教學目標。

## 程式碼審查問題

### Source Fidelity

- 是否有四個 `Scene` 類別，並依 handoff 核准順序忠實實作 `animation_design.md` 中每幕的教學責任與主要 beat？
- 程式碼是否忠實實作已確認需求、已核准設計與已審查 script，而非新增自己的演算法步驟或教學目標？
- 已核准為必要的 support structure、pointer 意義與 state 更新是否在程式碼中可追溯？

### Algorithm, State, Lifecycle, and Cleanup

- `Transform`、`ReplacementTransform` 與可替換物件的 current reference 是否一致？
- helper、label、highlight 與 support structure 是否有明確的建立、更新、淡出或移除時點？
- 各 Scene 是否自行建立與清理物件，並在程式碼中明確淡出至空白後再銜接下一幕？

實際 mobject geometry、bounding box、碰撞、遮擋、safe-frame、文字容量與 magic shift 的判定，完全以 `layout_audit_result.md` 為準；scene-reviewer 不得重做或取代該檢查。

### Assumptions and Maintainability

- 語意常數、builders、groups 與 visibility ownership 是否足以讓演算法與狀態意圖被稽核？
- 是否有 assumptions 過度延伸、無法追溯，或與上游契約不一致？

## 審查範圍

第一次程式碼審查必須檢查完整 `generated_algo_scene.py`。之後只有變更範圍明確、且 reviewer 能從程式碼 diff 確認受影響 Scene、helper 與相鄰 state 的情況下，才可做局部複查；影響不確定時，必須重新檢查完整檔案。

所有 findings 一律回到 Stage 4 `SCENE_IMPLEMENTATION` 的 `CODE_PREPARATION` 修正。scene-reviewer 不得修改 `generated_algo_scene.py`、`scene_code_review_handoff.md` 或任何 render 產物。

## PASS 標準

只有在以下條件成立時才能通過：

- `generated_algo_scene.py` 忠實實作已確認需求、已核准設計與已審查 script
- 程式碼中的演算法狀態、物件生命週期、ownership 與 Scene cleanup 可稽核
- `scene_code_review_handoff.md` 已存在，其 Code SHA-256 與實際受審程式碼一致，且確認尚未執行 Manim render
- `layout_audit_result.md = PASS`、涵蓋所有四個 Scene，且 `Audited Code SHA-256` 與 reviewed code hash 一致
- 四個完整 reports 的 hash、infos 與其他 counts 都已保留，沒有被截斷或摘要取代；任何 accepted warning 皆綁定目前 source hash 與可追溯核准來源
- 每個非平凡 Render Assumption 都最小、保守且可追溯
- `scene_review_result.md` 由獨立 reviewer 撰寫，而非 scene-writer，並記錄實際審查的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256`

## 常見失敗

- 要求先渲染或要求 MP4 才開始程式碼審查。
- 因程式通過語法或靜態檢查就通過，即使它發明了語意或遺漏 script beat。
- 因為沒有影片，就跳過演算法 state、生命週期、ownership 或 cleanup 的程式碼推理。
- scene-reviewer 重做 geometry、bounding-box、碰撞、遮擋或 safe-frame 判定，而不是使用 `layout_audit_result.md` 的 evidence。
- 接受只有人工說明、沒有 exact machine-readable disposition 的 warning，或接受已因 source/profile/hash 改變而失效的 layout evidence。
- 把 assumptions 過度延伸、不可追溯或新增教學內容的問題誤標成 styling。
- 回傳 `FAIL` 卻沒有指向相關程式碼或說明修復方向。
- 用過去的 MP4、截圖或畫面外觀作為渲染前程式碼審查的證據。
- PASS 後程式碼已改動，卻沒有針對新 Code SHA-256 重新審查。
