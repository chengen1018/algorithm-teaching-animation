# How to Review Manim Scene Code

本文件說明獨立 scene-reviewer 如何審查 `generated_algo_scene.py`。這是程式碼審查，不是視覺審查：reviewer 不開啟 MP4、不查看影格，也不根據畫面外觀判定 `PASS` 或 `FAIL`。

## 必要輸出

回傳 `scene_review_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- 審查結果必須由獨立 reviewer 撰寫
- reviewer 負責 `RENDER` gate 的程式碼審查
- 分類好的阻塞性 findings
- 指向程式碼位置的 evidence references
- 修復方向：`RENDER`

使用以下 finding 類別：

- `implementation fidelity`
- `state lifecycle`
- `static layout risk`
- `source mismatch`

## 審查輸入

審查時應對照：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- 已審查的 `teaching_script.md`
- `generated_algo_scene.py`
- `render_review_handoff.md`

`render_review_handoff.md` 的 Source Evidence 只用來確認 MP4 產物存在，並識別本次交接版本；不要求 reviewer 開啟或分析該影片。審查 `Render Assumptions` 時，每一項非平凡解讀都必須最小、保守、可追溯至其負責的來源範圍，且不得新增演算法步驟或教學目標。

## 程式碼審查問題

### Source Fidelity

- 六個 `Scene` 類別是否依核准順序實作所需的教學結構與主要 beat？
- 程式碼是否忠實實作已確認需求、已核准設計與已審查 script，而非新增自己的演算法步驟或教學目標？
- 已核准為必要的 support structure、pointer 意義與 state 更新是否在程式碼中可追溯？

### Static Layout and State Safety

- 每個穩定 beat 的定位鏈、群組與最終 bounding box 是否有可追溯的 safe-frame 推理？
- peak state、最長文字、panel 容量與共址 pointer 是否由程式結構處理，而不是依賴未驗證的 magic shift？
- `Transform`、`ReplacementTransform` 與可替換物件的 current reference 是否一致？
- helper、label、highlight 與 support structure 是否有明確的建立、更新、淡出或移除時點？
- 各 Scene 是否自行建立與清理物件，並在程式碼中明確淡出至空白後再銜接下一幕？

### Assumptions and Maintainability

- 語意常數、zones、builders、groups 與 visibility ownership 是否足以讓定位與狀態意圖被稽核？
- 是否有 assumptions 過度延伸、無法追溯，或與上游契約不一致？

## 審查範圍

第一次程式碼審查必須檢查完整 `generated_algo_scene.py`。之後只有變更範圍明確、且 reviewer 能從程式碼 diff 確認受影響 Scene、helper 與相鄰 state 的情況下，才可做局部複查；影響不確定時，必須重新檢查完整檔案。

所有 findings 一律回到 `RENDER` 修正。scene-reviewer 不得修改 `generated_algo_scene.py`、`render_review_handoff.md` 或任何 render 產物。

## PASS 標準

只有在以下條件成立時才能通過：

- `generated_algo_scene.py` 忠實實作已確認需求、已核准設計與已審查 script
- 程式碼中的物件狀態、生命週期、定位推理與 Scene cleanup 可稽核，且沒有未解決的靜態風險
- `render_review_handoff.md` 已存在，且 Source Evidence 指向交接版本的 MP4
- 每個非平凡 Render Assumption 都最小、保守且可追溯
- `scene_review_result.md` 由獨立 reviewer 撰寫，而非 render executor

## 常見失敗

- 因程式可以執行就通過，即使它發明了語意或遺漏 script beat。
- 因為沒有開啟影片，就跳過定位、生命週期、peak state 或 safe-frame 的程式碼推理。
- 把 assumptions 過度延伸、不可追溯或新增教學內容的問題誤標成 styling。
- 回傳 `FAIL` 卻沒有指向相關程式碼或說明修復方向。
- 用 MP4、截圖或畫面外觀作為程式碼審查的證據。
