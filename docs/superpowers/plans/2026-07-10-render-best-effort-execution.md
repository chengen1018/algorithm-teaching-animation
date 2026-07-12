# Render Best-Effort Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 RENDER 改為以已審查上游產物為契約的 best-effort 執行層，移除向上游回退的 `render_blocker.md` 機制。

**Architecture:** `scene-writer` 以最小、保守解讀完成程式與渲染，並把非平凡解讀記入 preflight。`scene-reviewer` 繼續獨立審查，但所有 FAIL 都在 RENDER 內修正；主 skill、agent TOML 與 references 採用相同語意。

**Tech Stack:** Markdown、TOML、Python 標準庫 `tomllib`、ripgrep。

## Global Constraints

- 不修改六個獨立 Scene、rerender evidence freshness 或獨立 scene review 的既有 gate。
- 不使用 `render_blocker.md` 處理上游歧義、資料不足或來源衝突。
- 不新增演算法步驟、教學目標或未記錄的上游需求。
- 每個非平凡解讀都寫入 `render_review_handoff.md` 的 `Render Assumptions`。
- scene-review 的修復目標一律是 `RENDER`。

---

### Task 1: 統一 Render best-effort 契約與 review 路由

**Files:**
- Modify: `.codex/agents/scene-writer.toml`
- Modify: `.codex/agents/scene-reviewer.toml`
- Modify: `SKILL.md`
- Modify: `references/manim-guidelines.md`
- Modify: `references/how-to-hand-off-a-render-for-review.md`
- Modify: `references/how-to-review-manim-scene-code.md`

**Interfaces:**
- Consumes: 已通過 gate 的 `confirmed_requirements.md`、`animation_design.md`、`teaching_script.md` 與 voiceover 產物。
- Produces: `generated_algo_scene.py`、最新 evidence、含 `Render Assumptions` 的 `render_review_handoff.md`，以及只路由回 `RENDER` 的 `scene_review_result.md`。

- [x] **Step 1: 寫入失敗的靜態契約檢查**

建立暫存檢查，要求三項尚未存在的行為：

```bash
rg -q "Render Assumptions" .codex/agents/scene-writer.toml references/how-to-hand-off-a-render-for-review.md references/how-to-review-manim-scene-code.md
! rg -q "上游有歧義或不足時，停止並建立 render_blocker.md" .codex/agents/scene-writer.toml
! rg -q "修復目標 SCRIPT、COLLECT_REQUIREMENTS 或 DESIGN_DEVELOPMENT" .codex/agents/scene-writer.toml
```

- [x] **Step 2: 執行檢查，確認目前失敗**

Run:

```bash
rg -q "Render Assumptions" .codex/agents/scene-writer.toml references/how-to-hand-off-a-render-for-review.md references/how-to-review-manim-scene-code.md
```

Expected: 非零結束碼，因為目前三份檔案尚未全部定義 assumptions 規則。

- [x] **Step 3: 以最小文字變更實作契約**

在 writer TOML 將停止／回退規則換成以下內容：

```text
上游已通過 gate 的產物是可執行契約。遇到可合理解讀的缺口或衝突時，採取最小、保守且不新增演算法步驟或教學目標的解讀，繼續實作與渲染；每項非平凡解讀都記錄到 render_review_handoff.md 的 Render Assumptions。
```

在 reviewer TOML、主 skill 與 checklist 將所有 scene-review FAIL 路由收斂為 `RENDER`；移除 `render_blocker.md` 的上游回退 gate。更新 Manim 指引與 preflight，使 assumptions 的格式、來源職責、review 檢查一致。

- [x] **Step 4: 執行靜態契約檢查，確認通過**

Run:

```bash
rg -q "Render Assumptions" .codex/agents/scene-writer.toml references/how-to-hand-off-a-render-for-review.md references/how-to-review-manim-scene-code.md
! rg -q "上游有歧義或不足時，停止並建立 render_blocker.md" .codex/agents/scene-writer.toml
! rg -q "修復目標 SCRIPT、COLLECT_REQUIREMENTS 或 DESIGN_DEVELOPMENT" .codex/agents/scene-writer.toml
```

Expected: 結束碼 0。

- [x] **Step 5: 驗證所有受影響契約**

Run:

```bash
python3 -c 'import tomllib; [tomllib.load(open(p, "rb")) for p in (".codex/agents/scene-writer.toml", ".codex/agents/scene-reviewer.toml")]'
rg -n -i "render_blocker|回到 SCRIPT|回到 COLLECT_REQUIREMENTS|回到 DESIGN_DEVELOPMENT|修復目標.*SCRIPT|修復目標.*COLLECT_REQUIREMENTS|修復目標.*DESIGN_DEVELOPMENT" SKILL.md .codex/agents/scene-*.toml references/manim-guidelines.md references/how-to-hand-off-a-render-for-review.md references/how-to-review-manim-scene-code.md
git diff --check
```

Expected: TOML 解析成功；搜尋結果不包含 RENDER 的上游回退規則；`git diff --check` 結束碼 0。

- [x] **Step 6: 提供可審閱的變更摘要**

Run:

```bash
git diff -- SKILL.md .codex/agents/scene-writer.toml .codex/agents/scene-reviewer.toml references/manim-guidelines.md references/how-to-hand-off-a-render-for-review.md references/how-to-review-manim-scene-code.md
```

Expected: 僅顯示 best-effort、assumptions 與 RENDER-only routing 的文字變更。
