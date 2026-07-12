# Render Best-Effort Execution 設計

## 目標

將 `RENDER` 定位為已核准上游成果的執行層：scene-writer 必須完成可用的 Manim 程式與渲染成品，而不是因文件中可合理解讀的細節、歧義或衝突重新啟動上游流程。

## 決策

1. 已通過各自 reviewer gate 的上游產物視為可執行契約。
2. scene-writer 遇到可合理解讀的缺口或衝突時，採取最小、保守且不新增演算法步驟或教學目標的解讀，繼續實作與渲染。
3. 每一項非平凡解讀都記錄在 `render_review_handoff.md` 的 `Render Assumptions` 區段，包含：問題、採用解讀、依據的上游檔案。
4. 上游來源各自負責的範圍固定為：需求檔負責使用者限制；設計檔負責演算法與視覺語意；腳本負責 beat 順序與教學焦點；旁白產物負責音訊與同步資料。衝突時以該範圍的負責來源為準。
5. `render_blocker.md` 不再用於上游語意歧義、資料不足或來源衝突，也不再是 RENDER 流程的必要產物或路由機制。
6. scene-reviewer 的每一項 `FAIL` 一律指定修復目標 `RENDER`；reviewer 可要求修正程式、畫面、證據或 assumptions 記錄，但不得把案件退回 `SCRIPT`、`COLLECT_REQUIREMENTS` 或 `DESIGN_DEVELOPMENT`。

## 硬性例外

無法讀取必要檔案、必要音訊不可用、Manim／FFmpeg 無法執行等輸入或環境故障，不屬於上游語意回退。scene-writer 必須回報具體技術阻礙與已嘗試的安全修復，但不得要求上游重新審查或重設計。

## 文件變更範圍

| 檔案 | 修改責任 |
| --- | --- |
| `.codex/agents/scene-writer.toml` | 移除「停止、寫 render_blocker、不得猜測」；加入最小保守解讀、來源職責與 preflight assumptions。 |
| `.codex/agents/scene-reviewer.toml` | 將所有 findings 的修復目標限制為 `RENDER`。 |
| `SKILL.md` | 移除 render_blocker gate 與 RENDER 向上游回退路由；明定 FAIL 回 RENDER。 |
| `references/manim-guidelines.md` | 將上游語意不足時的停止／回退規則改為 best-effort 解讀與 assumptions 記錄。 |
| `references/how-to-hand-off-a-render-for-review.md` | 加入簡潔的 `Render Assumptions` 格式。 |
| `references/how-to-review-manim-scene-code.md` | 將修復路由和 source mismatch 全部收斂為 RENDER，並要求審查已記錄的 assumptions。 |

## 不變條件

- 六個獨立 Scene、最新 render evidence、preflight、獨立 scene review 與 rerender 後重新審查仍然必要。
- scene-writer 不得把個人偏好包裝成上游要求；每個非平凡解讀都必須可追溯。
- reviewer 保持獨立性，且不得修改受審成品。

## 驗證

1. 搜尋確認 RENDER 文件不再要求因上游歧義建立 `render_blocker.md`，也不再將 scene-review findings 路由到上游階段。
2. 搜尋確認 `Render Assumptions` 在 writer、preflight 與 reviewer 規則中一致出現。
3. 用 Python `tomllib` 解析兩個 scene TOML，確認其仍為有效 TOML。
4. 執行 `git diff --check` 確認沒有格式錯誤。
