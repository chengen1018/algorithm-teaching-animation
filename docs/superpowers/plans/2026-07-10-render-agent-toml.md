# Render Agent TOML Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 RENDER 的 scene-writer 與 scene-reviewer 遷移為 named custom-agent TOML，並將 `SKILL.md` 限縮為協調流程。

**Architecture:** 兩個 `.codex/agents/scene-*.toml` 是角色唯一指令來源。主 skill 管理 prerequisite、委派、gate 與回退；reference 文件保留可重用的 preflight 與 review 細節。

**Tech Stack:** Markdown、TOML、Python 標準庫 `tomllib`。

## Global Constraints

- TOML 不複製 reference 的逐項檢查表。
- 每次 rerender 仍必須重建 evidence、preflight 與獨立 scene review。
- 不修改既有未追蹤檔案 `TTS_AUDIO_FIX_HANDOFF.md`。

### Task 1: 建立 RENDER custom-agent TOML

**Files:** Create `.codex/agents/scene-writer.toml`、`.codex/agents/scene-reviewer.toml`。

- [ ] 先以 Python 檢查兩份 TOML 不存在，確認測試為失敗。
- [ ] 建立 writer TOML：上游權威來源、必要輸出、preflight 與送審條件；建立 reviewer TOML：獨立性、正式結果、證據與修復路由。
- [ ] 以 `python3.11` 的 `tomllib` 解析兩份 TOML，確認皆含 `name`、`description`、`developer_instructions`。

### Task 2: 精簡協調者流程並刪除平行指令來源

**Files:** Modify `SKILL.md`; delete `agents/scene-writer.md`、`agents/scene-reviewer.md`。

- [ ] 將 RENDER 區段限制於 prerequisite、委派順序、產物、gate、rerender invalidation 與回退路由。
- [ ] 移除只屬於 sub-agent 的閱讀清單、實作規則、交接細節與 Full/delta 判定；由 TOML 要求閱讀 reference。
- [ ] 刪除兩份已被 TOML 取代的 Markdown。

### Task 3: 靜態端到端驗證

**Files:** Test `SKILL.md` 與兩份 scene TOML。

- [ ] 以 `rg` 檢查主 skill 只保留委派與 gate，並確認兩份舊 Markdown 不存在。
- [ ] 以 `python3.11 -c 'import tomllib; ...'` 解析 TOML。
- [ ] 執行 `git diff --check` 及 `git status --short`；預期沒有格式問題，且不含對 `TTS_AUDIO_FIX_HANDOFF.md` 的變更。
