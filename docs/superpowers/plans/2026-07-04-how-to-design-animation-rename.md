# How to Design Animation Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將原本的通用動畫設計指南全域重新命名為 `references/how-to-design-animation.md`，不遺留舊檔名。

**Architecture:** 使用保留工作樹內容的檔案 move，確保原檔未提交修改跟隨新路徑。之後對整個儲存庫進行機械式字串替換，包含有效文件與歷史規格／計畫，最後以全域零匹配驗證完成。

**Tech Stack:** Markdown、apply_patch、ripgrep、Git

---

### Task 1: 重新命名指南並更新全部引用

**Files:**
- Move: 原本的通用動畫設計指南 → `references/how-to-design-animation.md`
- Modify: every tracked or untracked text file containing the original filename
- Reference: `docs/superpowers/specs/2026-07-04-how-to-design-animation-rename-design.md`

- [ ] **Step 1: 確認重新命名前狀態**

Run:

```bash
test ! -e references/how-to-design-animation.md
rg -l 'references/[a-z-]*guide\.md' . --hidden --glob '!.git/**'
```

Expected: 舊檔存在、新檔不存在，並列出所有需要更新的文件。

- [ ] **Step 2: 移動檔案並保留內容**

用 `apply_patch` 的 `Move to` 將：

原本的通用動畫設計指南

移至：

```text
references/how-to-design-animation.md
```

不得重建或改寫內容；移動前後除路徑外的 diff 必須保留原檔目前未提交的修改。

- [ ] **Step 3: 全域更新字串**

對 Step 1 列出的每個檔案，將唯一字串：

原檔名字串

替換為：

```text
how-to-design-animation.md
```

新重新命名規格中的描述改以「原本的通用指南檔案」表達舊路徑，避免留下舊檔名字串，同時保持句意正確。

- [ ] **Step 4: 驗證重新命名與全域引用**

Run:

```bash
test -f references/how-to-design-animation.md
! rg -n 'animation-design-''guide\.md' . --hidden --glob '!.git/**'
rg -n 'references/how-to-design-animation\.md' SKILL.md references docs/superpowers
```

Expected: 新檔存在、舊檔不存在、舊檔名全儲存庫零匹配，所有原引用位置使用新路徑。

- [ ] **Step 5: 驗證內容與格式**

Run:

```bash
rg -n 'Scene 1: Problem and Goal|Scene 6: Result and Recap|Teaching Purpose|Explanation Focus|On-Screen Content|Concrete Animation Sequence|animation_design_review\.md = PASS' references/how-to-design-animation.md
git diff --check
```

Expected: 六幕邊界、四個必要欄位與審查 gate 仍存在；格式檢查 exit status `0`。

- [ ] **Step 6: 檢查變更範圍**

Run:

```bash
git status --short
git diff -- references/how-to-design-animation.md SKILL.md references docs/superpowers
```

Expected: 原指南呈現為 rename 或 delete/add，所有其他新增變更只替換檔名字串；本任務前的工作樹修改保持不變。
