# Animation Design Reviewer TOML Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 animation-design-reviewer 遷移為 `.codex/agents` 中的 named custom-agent TOML，並刪除舊 Markdown 定義。

**Architecture:** 新 TOML 是 reviewer 唯一角色指令來源，保留既有 agent 名稱，讓 `SKILL.md` 不需調整。舊 Markdown 檔案刪除，避免角色指令漂移。

**Tech Stack:** TOML、Python 標準庫 `tomllib`、Git 靜態檢查。

## Global Constraints

- TOML 的 `developer_instructions` 必須完整保留舊 reviewer 的角色界線、必要輸入、審查內容、產物與禁止事項。
- `SKILL.md` 必須保留現有 `animation-design-reviewer` 的流程名稱引用。
- 不修改此次遷移無關的既有工作區變更。

---

### Task 1: 建立 custom-agent TOML 並移除舊定義

**Files:**

- Create: `.codex/agents/animation-design-reviewer.toml`
- Delete: `agents/animation-design-reviewer.md`

**Interfaces:**

- Consumes: `agents/animation-design-reviewer.md` 的既有角色指令。
- Produces: 可由 Codex 以名稱 `animation-design-reviewer` 載入的 TOML agent 定義。

- [ ] **Step 1: 建立 TOML 定義**

建立 `.codex/agents/animation-design-reviewer.toml`，其鍵名必須依序為 `name`、`description`、`developer_instructions`，且 `name` 的值必須是 `animation-design-reviewer`。將舊 Markdown 的角色、必要輸入、審查內容、必要輸出及禁止事項完整遷入 `developer_instructions`。

- [ ] **Step 2: 刪除被取代的 Markdown**

刪除 `agents/animation-design-reviewer.md`，使 reviewer 指令只保留在 TOML。

### Task 2: 驗證遷移結果

**Files:**

- Test: `.codex/agents/animation-design-reviewer.toml`
- Test: `SKILL.md`

**Interfaces:**

- Consumes: Task 1 產生的 TOML 和既有流程 skill。
- Produces: 已解析且未破壞流程引用的 agent 定義。

- [ ] **Step 1: 驗證 TOML 結構**

Run:

```bash
python3 -c 'import tomllib; data = tomllib.load(open(".codex/agents/animation-design-reviewer.toml", "rb")); assert set(("name", "description", "developer_instructions")) <= data.keys(); assert data["name"] == "animation-design-reviewer"'
```

Expected: exit code 0。

- [ ] **Step 2: 驗證刪除與流程名稱引用**

Run:

```bash
test ! -e agents/animation-design-reviewer.md
rg -n 'animation-design-reviewer' SKILL.md
```

Expected: 舊 Markdown 不存在，且 `SKILL.md` 仍有 named-agent 引用。

- [ ] **Step 3: 檢查 diff 格式與變更範圍**

Run:

```bash
git diff --check -- .codex/agents/animation-design-reviewer.toml agents/animation-design-reviewer.md
git status --short -- .codex/agents/animation-design-reviewer.toml agents/animation-design-reviewer.md
```

Expected: `git diff --check` 結束碼為 0；狀態只顯示本次兩個 agent 檔案的新增與刪除。
