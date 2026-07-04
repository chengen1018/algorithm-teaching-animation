# 移除 Pre-build Brief 設計

## 目標

移除 `ANIMATION_DESIGN` 的 `CONTRACT` 子階段、`pre_build_brief.md` 產物及其參考文件。後續階段直接使用已確認需求與已核准動畫設計，避免維護一份不具權威性且可能失真的摘要。

## 權威輸入

流程只保留兩份動畫設計階段的內容來源：

- `confirmed_requirements.md`：保存演算法或問題、範例輸入或情境、教學目標、配音語言、畫面文字語言，以及使用者主動提出的額外需求。
- `animation_design.md`：保存六個 Scene 的教學目的、解說重點、畫面內容與具體動畫順序。

不新增 Audience、Chosen Visual Rules 或 Delivery Requirements 欄位。視覺一致性仍是設計與審查原則，但不建立獨立欄位；配音仍依需求蒐集規則固定包含在交付中。

## 流程變更

`ANIMATION_DESIGN` 只保留：

1. `COLLECT_REQUIREMENTS`
2. `DESIGN_DEVELOPMENT`
3. 獨立內容審查與使用者最終核准

完成條件為 `confirmed_requirements.md` 存在、六幕 `animation_design.md` 完整、`animation_design_review.md = PASS`，以及使用者已明確核准完整設計。完成後直接進入 `SCRIPT`。

移除所有 `CONTRACT` 回退路徑。下游若發現需求來源錯誤，退回 `COLLECT_REQUIREMENTS`；若發現演算法行為、教學呈現、Scene 結構或動畫設計缺漏，退回 `DESIGN_DEVELOPMENT`；若只是下游產物本身的問題，留在該下游階段修正。

## 下游資料流

- `SCRIPT`：根據 `confirmed_requirements.md` 與已核准 `animation_design.md` 建立並審查 `teaching_script.md`。
- `VOICEOVER`：根據需求、已核准設計與已審查腳本建立旁白；旁白固定為必要產物，不再保留 `no narration` 分支。
- `RENDER`：根據需求、設計、腳本與旁白實作六個 Scene。
- `QA` 與 `DELIVERY`：直接依需求、設計、腳本、旁白及最新渲染證據驗證。

## 檔案範圍

- 刪除 `references/pre-build-brief.md`。
- 修改 `SKILL.md`，移除 `CONTRACT`、`pre_build_brief.md`、delivery tier 與 no-narration 分支。
- 修改 `agents/` 與 `references/` 中所有 `pre_build_brief.md`、`CONTRACT`、已確認 brief、delivery tier 與 no-narration 依賴。
- 更新目前這輪重構的規格與計畫文件中仍指向舊流程的敘述，避免留下失效引用。

## 驗證

完成後必須確認：

- 工作流程檔案中沒有 `pre_build_brief.md`、`CONTRACT`、`no narration` 或 delivery tier 的執行依賴。
- `references/pre-build-brief.md` 已不存在。
- 每個下游角色都能從明確列出的上游產物取得所需資訊。
- `ANIMATION_DESIGN` 的審查與使用者核准關卡仍然存在。
- Markdown 格式檢查沒有錯誤。

## 不在範圍內

- 不新增 Audience、Chosen Visual Rules 或 Delivery Requirements 的替代欄位。
- 不改變六個 Scene 的固定結構。
- 不移除動畫設計的獨立審查或使用者最終核准。
- 不修改與本次資料流簡化無關的 Manim 實作或視覺規則。
