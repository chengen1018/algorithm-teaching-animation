# Scene Writer 白話改寫設計

## 目標

讓 `.codex/agents/scene-writer.toml` 更容易讀懂，同時完全保留現有 Agent 的行為規則。

## 改寫方式

- `description` 改為直接說明工作內容的白話中文。
- `developer_instructions` 改成短句與有標題的條列：角色、開始前、工作方式、交付內容、技術阻礙、送審規則。
- 保留所有檔案名稱、六個獨立 Scene、最新 MP4 證據、Render Assumptions、最小保守解讀、技術阻礙回報與獨立 reviewer 規則。

## 不變條件

- 不改變任何流程路由、必要產物或通過條件。
- 不加入新規則，也不移除既有規則。
- TOML 結構仍只包含 `name`、`description` 和 `developer_instructions`。

## 驗證

1. 使用 Python 3.11 的 `tomllib` 解析 TOML。
2. 搜尋確認必要檔名、`Render Assumptions`、六個 Scene 與 `scene-reviewer` 規則仍存在。
3. 執行 `git diff --check`。
