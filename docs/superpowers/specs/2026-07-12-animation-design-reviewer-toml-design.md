# Animation Design Reviewer TOML 設計

## 目標

將 animation-design-reviewer 從舊的 Markdown agent 定義遷移為 Codex 可載入的 named custom-agent TOML，並移除舊定義，避免兩份角色指令來源並存。

## 範圍與權責

| 位置 | 責任 |
| --- | --- |
| `.codex/agents/animation-design-reviewer.toml` | animation-design-reviewer 的唯一角色指令來源。 |
| `agents/animation-design-reviewer.md` | 已被 TOML 取代後刪除。 |
| `SKILL.md` | 維持既有流程與 `animation-design-reviewer` 名稱引用，不承載此 reviewer 的詳細角色指令。 |

## 設計

新增 TOML 檔案，格式與 `.codex/agents` 內既有 custom agents 一致：

- `name = "animation-design-reviewer"`
- 簡短 `description`
- 三引號字串 `developer_instructions`

`developer_instructions` 忠實遷移舊 Markdown 中的角色、必要輸入、審查內容、必要輸出與禁止事項。Reviewer 仍只審查 `animation_design.md`，不參與共同設計，也不得修改該檔案。

## 不變條件

- 必須閱讀 `confirmed_requirements.md`、`animation_design.md`、`references/how-to-review-design.md` 與相符演算法的教學及類型參考。
- 產出 `animation_design_review.md`，清楚給出 PASS 或 FAIL；FAIL 時列出具體問題與必要修正。
- 不得以個人偏好推翻或取代使用者選定的設計。
- `SKILL.md` 的既有 named-agent 引用不變。

## 驗證

- 以 Python 標準庫 `tomllib` 解析 TOML，並確認具備 `name`、`description`、`developer_instructions`。
- 確認 `agents/animation-design-reviewer.md` 不存在。
- 確認 `SKILL.md` 仍引用 `animation-design-reviewer`，且不引用已刪除的 Markdown 路徑。
- 執行 `git diff --check`。
