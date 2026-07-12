# Scene Writer Plain-Language Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 scene-writer 的 TOML 指令改寫為容易理解的中文，同時保留完全相同的行為。

**Architecture:** 保留 TOML 的三個頂層欄位與原本的規則內容。只在 `description` 和多行 `developer_instructions` 中調整語句、段落與條列結構。

**Tech Stack:** TOML、Python 3.11 標準庫 `tomllib`、ripgrep。

## Global Constraints

- 不改變流程路由、必要產物或通過條件。
- 不新增或刪除行為規則。
- 保留六個獨立 Scene、Render Assumptions、最新 evidence 與獨立 reviewer 規則。

---

### Task 1: 白話改寫 Scene Writer TOML

**Files:**
- Modify: `.codex/agents/scene-writer.toml`

**Interfaces:**
- Consumes: 現有 `name`、`description` 和 `developer_instructions`。
- Produces: 可被 Codex 載入、規則不變但更容易閱讀的 scene-writer TOML。

- [ ] **Step 1: 寫入靜態契約檢查**

檢查改寫後仍包含必要規則：

```bash
rg -q '六個獨立.*Scene' .codex/agents/scene-writer.toml
rg -q 'Render Assumptions' .codex/agents/scene-writer.toml
rg -q 'scene-reviewer' .codex/agents/scene-writer.toml
```

- [ ] **Step 2: 執行既有規則檢查**

Run:

```bash
rg -q '六個獨立.*Scene' .codex/agents/scene-writer.toml
rg -q 'Render Assumptions' .codex/agents/scene-writer.toml
rg -q 'scene-reviewer' .codex/agents/scene-writer.toml
```

Expected: 結束碼 0，確認改寫前的必要規則已存在。

- [ ] **Step 3: 進行白話改寫**

將 description 改為：

```toml
description = "依照已確認的設計與腳本，製作 Manim 場景、渲染影片，並準備送審資料。"
```

將 instructions 拆成「你的角色」、「開始前要讀」、「怎麼實作」、「要交付什麼」、「技術問題怎麼辦」與「送審規則」六個白話區塊；只改寫表達，不改變任何規則。

- [ ] **Step 4: 驗證改寫後的 TOML**

Run:

```bash
python3.11 -c 'import tomllib; d=tomllib.load(open(".codex/agents/scene-writer.toml", "rb")); assert set(d) == {"name", "description", "developer_instructions"}'
rg -q '六個獨立.*Scene' .codex/agents/scene-writer.toml
rg -q 'Render Assumptions' .codex/agents/scene-writer.toml
rg -q 'scene-reviewer' .codex/agents/scene-writer.toml
git diff --check
```

Expected: 全部結束碼為 0。
