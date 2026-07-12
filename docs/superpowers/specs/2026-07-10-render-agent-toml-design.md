# 階段四 Render Agent TOML 設計

## 目標

讓 `RENDER` 與階段二一樣，使用可被 Codex 載入的 named custom-agent TOML；主 `SKILL.md` 只編排流程與 gate，sub-agent TOML 才是執行與審查角色的唯一指令來源。

## 範圍與權責

| 位置 | 唯一責任 |
| --- | --- |
| `SKILL.md` | RENDER 的前置條件、委派順序、產物、通過 gate 與回退路由。 |
| `.codex/agents/scene-writer.toml` | scene-writer 的權威來源、閱讀清單、可做與不可做的實作、必要產物、preflight 與送審條件。 |
| `.codex/agents/scene-reviewer.toml` | scene-reviewer 的獨立性、閱讀清單、審查產物契約、證據新鮮度、Full/delta 規則與修復路由。 |
| `references/how-to-hand-off-a-render-for-review.md` | writer 使用的交接格式與 assumptions 記錄。 |
| `references/how-to-review-manim-scene-code.md` | reviewer 使用的程式碼審查準則、finding 分類與回退判斷。 |

## 變更

1. 新增 `scene-writer.toml` 和 `scene-reviewer.toml`，格式與階段二的 `script-*.toml` 一致。
2. 將現有 `agents/scene-writer.md`、`agents/scene-reviewer.md` 的角色指令遷入相對應 TOML；刪除這兩份過時的平行指令來源。
3. 精簡 `SKILL.md` 的階段四：保留協調者須判斷的 gate 與委派順序，移除只屬於 writer/reviewer 的閱讀清單、實作細節、preflight 細節與 Full/delta 判定細則。
4. TOML 以「必須閱讀 reference」取代複製 reference 細節，確保每項規則只有一份權威文字。

## 不變條件

- 必須先由 scene-writer 實作與建立最新 evidence、`render_review_handoff.md`，再由獨立 scene-reviewer 審查。
- 所有 rerender 都使 evidence、preflight 與 scene-review 結果失效；重新進入 QA 前必須重新完成這些 gate。
- 第一輪 scene review 為 Full；delta review 僅限 reference 定義的條件。
- 任何需要重新解釋上游需求、設計或 script 的問題仍須依既有流程回退，不能由 RENDER 自行補決策。

## 驗證

- TOML 可由 Python 標準庫 `tomllib` 解析，且具有 `name`、`description`、`developer_instructions`。
- `SKILL.md` 只以 agent 名稱與流程 gate 指向階段四 TOML，不再引用已刪除的 scene agent Markdown。
- 搜尋確認 writer/reviewer 職責沒有同時保留在 SKILL、TOML 與 reference 三個位置。
