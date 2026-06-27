# 動畫設計階段實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將第一階段改造成具備 intake、專業動畫設計、獨立審查與雙重使用者核准的 `ANIMATION_DESIGN` 工作流。

**Architecture:** 先建立可獨立閱讀的通用與演算法類型設計 references，再建立 `animation-designer` 與獨立 reviewer，最後更新中英文主契約及入口提示。`animation_design.md` 是可編輯的設計產物，`pre_build_brief.md` 則是經核准設計轉換而成的正式下游契約。

**Tech Stack:** Markdown、Codex Skill/Agent 契約、PowerShell、`rg`、Git

---

## 檔案結構

### 新增

- `references/animation-design-process.md`：設計互動流程、問題批次與 `DESIGN_READY`。
- `references/animation-design-document.md`：`animation_design.md` 的必要結構與寫作規則。
- `references/teaching-design.md`：心智模型、誤解分析、範例選擇與教學弧線。
- `references/animation-design-review-checklist.md`：完整／差異審查與 `PASS` 條件。
- `references/animation-design-array-sorting.md`：排序動畫的類型專用設計知識。
- `references/animation-design-search.md`：搜尋動畫的類型專用設計知識。
- `references/animation-design-graph-traversal.md`：圖形走訪動畫的類型專用設計知識。
- `agents/animation-designer.md`：核心問題規劃、動畫設計、文件修訂與契約轉換。
- `agents/animation-design-reviewer.md`：動畫設計的獨立 reviewer。

### 修改

- `references/intake-contract.md`：改為產出 `intake_summary.md`，不得過早決定設計。
- `references/high-impact-clarification.md`：改為支援 designer 的批次核心問題規劃。
- `references/pre-build-brief.md`：明定只能由已核准的 `animation_design.md` 轉換。
- `references/visual-language.md`：補足設計階段的視覺可行性判準。
- `references/default-visual-semantics.md`：維持低風險預設與核心設計決策的邊界。
- `SKILL.zh-TW.md`：以核准中文規格實作完整流程。
- `SKILL.md`：同步正式可載入 Skill 的英文契約。
- `agents/openai.yaml`：更新入口提示、階段名稱與委派順序。

### 刪除

- `agents/brief-editor.md`：責任併入 `animation-designer`。
- `agents/clarification-planner.md`：責任併入 `animation-designer`。

### 不修改

- `SCRIPT`、`VOICEOVER`、`RENDER`、`QA`、`DELIVERY` 的核心產物與 reviewer 分工保持不變；只更新其上游回退名稱與前置條件。

---

### Task 1：建立設計流程與設計文件契約

**Files:**
- Create: `references/animation-design-process.md`
- Create: `references/animation-design-document.md`

- [ ] **Step 1：確認新 references 尚不存在**

Run:

```powershell
$files = @(
  'references/animation-design-process.md',
  'references/animation-design-document.md'
)
$existing = $files | Where-Object { Test-Path $_ }
if ($existing) { throw "Unexpected existing files: $($existing -join ', ')" }
```

Expected: command exits successfully without output.

- [ ] **Step 2：建立設計流程 reference**

Create `references/animation-design-process.md` with these exact responsibility sections:

```markdown
# Animation Design Process

## Purpose
## Inputs
## Design Responsibilities
## Core-Question Batch Protocol
## Low-Impact Questions That Must Not Block Design
## DESIGN_READY Gate
## User Edit Loop
## Full Review Versus Delta Review
## Rollback Rules
## Failure Conditions
```

The content must require: small question batches; one user-facing question at a time; a recommendation, rationale, and tradeoff per question; faithful answer relay; mandatory design of the mental model, visual presentation, teaching arc, and high-level beats; and stopping once every `DESIGN_READY` condition passes.

- [ ] **Step 3：建立設計文件 reference**

Create `references/animation-design-document.md` with this required schema:

```markdown
# Animation Design Document

## Purpose
## Confirmation Rule
## Required Sections
### Design Goal and Audience
### Algorithm Variant and Semantics
### Primary Mental Model
### Viewer Misconceptions to Prevent
### Sample Input and Rationale
### Core Visual Metaphor and Visual Semantics
### Structure Presentation
### Scene Structure and Information Hierarchy
### Teaching Arc
### High-Level Animation Beats
### Recommended Design and Alternatives
### Incorporated User Decisions
### Risks and Best-Effort Notes
### DESIGN_READY Self-Check
## Writing Rules
## Failure Conditions
## Recommended Template
```

State explicitly that the user may edit `animation_design.md`, edits require re-review, and silence or editing alone does not count as approval.

- [ ] **Step 4：驗證必要章節與關鍵規則**

Run:

```powershell
$checks = @{
  'references/animation-design-process.md' = @('Core-Question Batch Protocol', 'DESIGN_READY Gate', 'Rollback Rules')
  'references/animation-design-document.md' = @('Primary Mental Model', 'Teaching Arc', 'High-Level Animation Beats', 'DESIGN_READY Self-Check')
}
foreach ($file in $checks.Keys) {
  foreach ($text in $checks[$file]) {
    if (-not (Select-String -Path $file -SimpleMatch $text -Quiet)) { throw "$file missing: $text" }
  }
}
```

Expected: command exits successfully without output.

- [ ] **Step 5：提交通用設計流程**

```powershell
git add references/animation-design-process.md references/animation-design-document.md
git commit -m "feat: define animation design workflow"
```

---

### Task 2：建立教學設計與類型專用知識

**Files:**
- Create: `references/teaching-design.md`
- Create: `references/animation-design-array-sorting.md`
- Create: `references/animation-design-search.md`
- Create: `references/animation-design-graph-traversal.md`

- [ ] **Step 1：建立通用教學設計 reference**

Create `references/teaching-design.md` with these sections and rules:

```markdown
# Teaching Design

## Purpose
## Choosing a Mental Model
## Identifying Viewer Misconceptions
## Selecting a Teaching Sample
## Building a Teaching Arc
## Designing High-Level Beats
## Connecting Visual Cause and Effect
## Comparing Alternatives
## Common Failures
```

Require every design to explain what viewers should understand, what visible evidence teaches it, how each beat prepares the next beat, and why the selected sample exposes meaningful behavior.

- [ ] **Step 2：建立 array sorting 設計知識**

Create `references/animation-design-array-sorting.md`. It must cover:

```markdown
## Required Design Decisions
- active comparison unit
- movement model
- settled-progress expression
- temporary holding position
- duplicate-value identity tracking

## Teaching Risks
- movement that hides causality
- settled styling that resembles active styling
- a sample that never demonstrates the defining operation
```

- [ ] **Step 3：建立 search 設計知識**

Create `references/animation-design-search.md`. It must cover:

```markdown
## Required Design Decisions
- interval convention
- pointer meaning
- stopping rule
- elimination logic
- pointer choreography
- excluded-region persistence

## Teaching Risks
- deleting context too early
- visually implying the wrong interval convention
- moving pointers without showing the comparison that caused the move
```

- [ ] **Step 4：建立 graph traversal 設計知識**

Create `references/animation-design-graph-traversal.md`. It must cover:

```markdown
## Required Design Decisions
- queue or stack visibility
- visited timing
- discovery versus processing
- frontier or path emphasis
- neighbor order
- stable graph layout

## Teaching Risks
- conflating discovered and processed states
- moving graph nodes after introduction
- hiding a teaching-critical support structure
```

- [ ] **Step 5：驗證類型路由所需內容**

Run:

```powershell
$checks = @{
  'references/animation-design-array-sorting.md' = @('movement model', 'settled-progress', 'duplicate-value')
  'references/animation-design-search.md' = @('interval convention', 'elimination logic', 'excluded-region')
  'references/animation-design-graph-traversal.md' = @('visited timing', 'neighbor order', 'stable graph layout')
}
foreach ($file in $checks.Keys) {
  foreach ($text in $checks[$file]) {
    if (-not (Select-String -Path $file -SimpleMatch $text -Quiet)) { throw "$file missing: $text" }
  }
}
```

Expected: command exits successfully without output.

- [ ] **Step 6：提交教學與類型知識**

```powershell
git add references/teaching-design.md references/animation-design-array-sorting.md references/animation-design-search.md references/animation-design-graph-traversal.md
git commit -m "feat: add algorithm animation design knowledge"
```

---

### Task 3：建立 designer 與獨立 reviewer

**Files:**
- Create: `references/animation-design-review-checklist.md`
- Create: `agents/animation-designer.md`
- Create: `agents/animation-design-reviewer.md`
- Delete: `agents/brief-editor.md`
- Delete: `agents/clarification-planner.md`

- [ ] **Step 1：建立 reviewer checklist**

Create `references/animation-design-review-checklist.md` with:

```markdown
# Animation Design Review Checklist

## Review Preconditions
## Review Scope Selection
### Full Review
### Delta Review
## Teaching Coherence
## Visual Feasibility
## Algorithm Semantic Consistency
## High-Impact Gap Check
## Best-Effort Strengthened Review
## Required Result Schema
## PASS Conditions
## FAIL and Rollback Rules
```

The result schema must require `Review Scope`, evidence for all three quality dimensions, unresolved issues, required repairs, rollback target, and exactly one verdict: `PASS` or `FAIL`.

- [ ] **Step 2：建立 animation-designer**

Create `agents/animation-designer.md` with:

```markdown
# animation-designer

## Role
## Required Inputs
## Core-Question Batch Output
## Animation Design Responsibilities
## Required Outputs
## Reference Routing
## CONTRACT Conversion Responsibilities
## Rules
## Fail Conditions
## Rollback Rules
```

Require it to read the intake, common design references, `visual-language.md`, `default-visual-semantics.md`, and exactly one matching type reference when available. For unsupported types, require `best-effort` marking and stronger risk disclosure. It may create `pre_build_brief.md` only after reviewed and explicitly approved `animation_design.md` exists.

- [ ] **Step 3：建立 animation-design-reviewer**

Create `agents/animation-design-reviewer.md` with:

```markdown
# animation-design-reviewer

## Role
## Independence Requirement
## Required Inputs
## Reference Routing
## Required Output
## Full and Delta Review Rules
## PASS Conditions
## Fail Conditions
## Rollback Rules
```

Prohibit the reviewer from authoring or silently repairing `animation_design.md`. Require `animation_design_review.md` as the only formal verdict artifact.

- [ ] **Step 4：刪除被取代的角色**

Delete only:

```text
agents/brief-editor.md
agents/clarification-planner.md
```

- [ ] **Step 5：驗證角色邊界與刪除結果**

Run:

```powershell
if (Test-Path 'agents/brief-editor.md') { throw 'brief-editor still exists' }
if (Test-Path 'agents/clarification-planner.md') { throw 'clarification-planner still exists' }
$required = @(
  'agents/animation-designer.md',
  'agents/animation-design-reviewer.md',
  'references/animation-design-review-checklist.md'
)
foreach ($file in $required) { if (-not (Test-Path $file)) { throw "Missing $file" } }
rg -n "DESIGN_READY|animation_design\.md|animation_design_review\.md|pre_build_brief\.md" agents/animation-designer.md agents/animation-design-reviewer.md references/animation-design-review-checklist.md
```

Expected: all three files exist and `rg` shows their required gate and artifact references.

- [ ] **Step 6：提交設計角色與審查關卡**

```powershell
git add agents/animation-designer.md agents/animation-design-reviewer.md references/animation-design-review-checklist.md agents/brief-editor.md agents/clarification-planner.md
git commit -m "feat: add animation design agents"
```

---

### Task 4：更新 intake、契約與視覺 reference 邊界

**Files:**
- Modify: `references/intake-contract.md`
- Modify: `references/high-impact-clarification.md`
- Modify: `references/pre-build-brief.md`
- Modify: `references/visual-language.md`
- Modify: `references/default-visual-semantics.md`

- [ ] **Step 1：先記錄舊 reference 的缺口**

Run:

```powershell
$required = @(
  @{ File='references/intake-contract.md'; Text='intake_summary.md' },
  @{ File='references/pre-build-brief.md'; Text='animation_design.md' }
)
foreach ($item in $required) {
  if (Select-String -Path $item.File -SimpleMatch $item.Text -Quiet) {
    throw "Expected pre-change gap not found: $($item.File) already contains $($item.Text)"
  }
}
```

Expected: command exits successfully, proving the new artifact handoffs are not yet encoded.

- [ ] **Step 2：更新 intake 與核心問題規則**

Modify `references/intake-contract.md` so its formal output is `intake_summary.md`, candidate framing remains non-binding, and unresolved design choices route to `animation-designer`.

Modify `references/high-impact-clarification.md` so it defines the high-impact inventory used by `animation-designer`, requires batched internal planning but one user-facing question at a time, and excludes low-impact presentation details.

- [ ] **Step 3：更新正式契約來源規則**

Modify `references/pre-build-brief.md` to require:

```markdown
- an approved `animation_design.md`
- `animation_design_review.md = PASS`
- faithful conversion rather than new design work
- rollback to `DESIGN_DEVELOPMENT` when a core design gap appears
- separate explicit user approval of `pre_build_brief.md`
```

Preserve all existing downstream contract sections for narration, overlays, semantics, risks, and beats.

- [ ] **Step 4：補足視覺 reference 的設計／實作邊界**

Modify `references/visual-language.md` so `DESIGN_DEVELOPMENT` owns core visual semantics, scene structure, persistent support structures, and information hierarchy.

Modify `references/default-visual-semantics.md` so it continues to own only low-risk defaults such as ordinary colors, minor placement, easing, and local timing. State that defaults cannot replace a missing core design decision.

- [ ] **Step 5：驗證 reference 間沒有權責衝突**

Run:

```powershell
rg -n "intake_summary\.md|animation-designer|DESIGN_DEVELOPMENT|animation_design\.md|animation_design_review\.md" references/intake-contract.md references/high-impact-clarification.md references/pre-build-brief.md references/visual-language.md references/default-visual-semantics.md
rg -n "ordinary colors|minor placement|easing|local timing" references/default-visual-semantics.md
```

Expected: the first command shows the new artifact and rollback routing; the second shows low-risk details remain outside core design.

- [ ] **Step 6：提交 reference 整合變更**

```powershell
git add references/intake-contract.md references/high-impact-clarification.md references/pre-build-brief.md references/visual-language.md references/default-visual-semantics.md
git commit -m "feat: integrate animation design references"
```

---

### Task 5：更新中文主契約

**Files:**
- Modify: `SKILL.zh-TW.md`

- [ ] **Step 1：確認舊階段仍存在**

Run:

```powershell
if (-not (Select-String -Path 'SKILL.zh-TW.md' -SimpleMatch 'REQUEST_CONTRACT' -Quiet)) {
  throw 'Expected old phase name is missing before migration'
}
```

Expected: command exits successfully.

- [ ] **Step 2：更新工作流程、授權與產物鏈**

Replace the first phase name and leading artifacts so the contract states:

```text
1. ANIMATION_DESIGN
2. SCRIPT
3. VOICEOVER
4. RENDER
5. QA
6. DELIVERY

intake_summary.md
animation_design.md
animation_design_review.md
pre_build_brief.md
```

Update subagent authorization language so `animation-designer` and `animation-design-reviewer` are included before downstream content, scene, and QA roles.

- [ ] **Step 3：以三個子階段重寫第一階段**

The new `ANIMATION_DESIGN` section must contain these headings:

```markdown
### 目標
### 委派
### 子階段 1：INTAKE
### 子階段 2：DESIGN_DEVELOPMENT
### 子階段 3：CONTRACT
### 必要輸出
### 通過／離開關卡
### 回退規則
```

Encode the approved role split, question batching, actual animation-design responsibilities, `DESIGN_READY`, independent review, direct user editing, full/delta re-review, and two explicit user approvals.

- [ ] **Step 4：更新所有下游回退名稱與前置條件**

Replace rollback references that currently target `REQUEST_CONTRACT` with the precise owner:

```text
INTAKE — source request capture errors
DESIGN_DEVELOPMENT — semantic, mental-model, visual-semantic, or teaching-arc gaps
CONTRACT — contract wording or source-label errors
ANIMATION_DESIGN — only when referring to the complete top-level phase
```

Preserve downstream behavior and artifact requirements otherwise.

- [ ] **Step 5：更新完成檢查與失敗模式**

Require all of:

```text
intake_summary.md exists
animation_design.md exists
animation_design_review.md = PASS
animation_design.md has explicit user approval
pre_build_brief.md has separate explicit user approval
```

Add failure patterns for skipping `DESIGN_DEVELOPMENT`, treating reviewer comments as a file-backed verdict, and patching core design gaps in `SCRIPT` or `RENDER`.

- [ ] **Step 6：驗證中文主契約**

Run:

```powershell
$required = @('ANIMATION_DESIGN', 'INTAKE', 'DESIGN_DEVELOPMENT', 'CONTRACT', 'DESIGN_READY', 'intake_summary.md', 'animation_design.md', 'animation_design_review.md')
foreach ($text in $required) {
  if (-not (Select-String -Path 'SKILL.zh-TW.md' -SimpleMatch $text -Quiet)) { throw "SKILL.zh-TW.md missing: $text" }
}
if (Select-String -Path 'SKILL.zh-TW.md' -Pattern '階段 1：REQUEST_CONTRACT' -Quiet) { throw 'Old first phase heading remains' }
```

Expected: command exits successfully without output.

- [ ] **Step 7：提交中文主契約**

```powershell
git add SKILL.zh-TW.md
git commit -m "feat: add animation design phase contract"
```

---

### Task 6：同步正式 Skill 與入口提示

**Files:**
- Modify: `SKILL.md`
- Modify: `agents/openai.yaml`

- [ ] **Step 1：同步英文主契約的語意**

Update `SKILL.md` to match every gate and responsibility in `SKILL.zh-TW.md`. Keep English prose, but preserve these identifiers exactly:

```text
ANIMATION_DESIGN
INTAKE
DESIGN_DEVELOPMENT
CONTRACT
DESIGN_READY
intake_summary.md
animation_design.md
animation_design_review.md
pre_build_brief.md
```

Do not alter downstream semantics except for phase numbering, prerequisites, and rollback targets required by the new first phase.

- [ ] **Step 2：重寫入口提示中的第一階段**

Modify `agents/openai.yaml` so `default_prompt` instructs the orchestrator to:

```text
1. run INTAKE and create intake_summary.md
2. dispatch animation-designer for question planning and animation design
3. ask planned questions one at a time and return answers in a batch
4. dispatch animation-design-reviewer after DESIGN_READY
5. request explicit design approval only after PASS
6. dispatch animation-designer to convert the approved design into pre_build_brief.md
7. request separate contract approval before SCRIPT
```

Remove references that describe `INTAKE`, `CLARIFICATION`, and `PRE_BUILD_BRIEF` as the old orchestrator-only phase sequence. Preserve downstream dispatch restrictions.

- [ ] **Step 3：驗證中英文契約的識別字對齊**

Run:

```powershell
$files = @('SKILL.md', 'SKILL.zh-TW.md')
$required = @('ANIMATION_DESIGN', 'INTAKE', 'DESIGN_DEVELOPMENT', 'CONTRACT', 'DESIGN_READY', 'intake_summary.md', 'animation_design.md', 'animation_design_review.md', 'pre_build_brief.md')
foreach ($file in $files) {
  foreach ($text in $required) {
    if (-not (Select-String -Path $file -SimpleMatch $text -Quiet)) { throw "$file missing: $text" }
  }
}
rg -n "animation-designer|animation-design-reviewer|DESIGN_DEVELOPMENT" agents/openai.yaml
```

Expected: both contracts contain every identifier and the prompt names both new agents.

- [ ] **Step 4：確認舊角色及第一階段名稱沒有殘留引用**

Run:

```powershell
$hits = rg -n "clarification-planner|brief-editor|Phase 1: REQUEST_CONTRACT|階段 1：REQUEST_CONTRACT" SKILL.md SKILL.zh-TW.md agents references
if ($LASTEXITCODE -eq 0) { throw "Stale references remain:`n$hits" }
if ($LASTEXITCODE -ne 1) { throw 'rg failed unexpectedly' }
```

Expected: `rg` returns exit code 1 because no stale references remain.

- [ ] **Step 5：提交正式 Skill 與入口提示**

```powershell
git add SKILL.md agents/openai.yaml
git commit -m "feat: activate animation design workflow"
```

---

### Task 7：執行整合驗證與代表性流程走讀

**Files:**
- Verify: `SKILL.md`
- Verify: `SKILL.zh-TW.md`
- Verify: `agents/*.md`
- Verify: `references/*.md`

- [ ] **Step 1：檢查所有必要檔案及已刪除檔案**

Run:

```powershell
$required = @(
  'agents/animation-designer.md',
  'agents/animation-design-reviewer.md',
  'references/animation-design-process.md',
  'references/animation-design-document.md',
  'references/teaching-design.md',
  'references/animation-design-review-checklist.md',
  'references/animation-design-array-sorting.md',
  'references/animation-design-search.md',
  'references/animation-design-graph-traversal.md'
)
foreach ($file in $required) { if (-not (Test-Path $file)) { throw "Missing $file" } }
foreach ($file in @('agents/brief-editor.md', 'agents/clarification-planner.md')) {
  if (Test-Path $file) { throw "Removed role still exists: $file" }
}
```

Expected: command exits successfully without output.

- [ ] **Step 2：檢查關卡完整性與跳階防護**

Run:

```powershell
$gateTerms = @(
  'animation_design_review.md = PASS',
  'explicit user approval',
  'pre_build_brief.md',
  'DESIGN_DEVELOPMENT'
)
foreach ($file in @('SKILL.md', 'references/animation-design-process.md', 'references/animation-design-review-checklist.md')) {
  foreach ($term in $gateTerms) {
    if (-not (Select-String -Path $file -SimpleMatch $term -Quiet)) { throw "$file missing gate term: $term" }
  }
}
```

Expected: every gate term is present in every governing contract.

- [ ] **Step 3：走讀 array sorting 案例**

Use the request `Animate insertion sort on [5, 2, 4, 2] for beginners` and verify the documents force decisions for movement semantics, temporary holding position, settled progress, duplicate identity, mental model, and teaching arc. Record any missing rule as a defect and repair the owning reference before continuing.

- [ ] **Step 4：走讀 binary search 案例**

Use the request `Animate binary search for 23 in [3, 8, 12, 17, 23, 31]` and verify the documents force decisions for interval convention, pointer meaning, stopping rule, elimination logic, excluded-region persistence, mental model, and beat causality.

- [ ] **Step 5：走讀 BFS 案例**

Use the request `Animate BFS from A` and verify the documents force decisions for graph input, queue visibility, visited timing, discovery versus processing, neighbor order, layer-expansion emphasis, and stable graph layout.

- [ ] **Step 6：走讀 best-effort 案例**

Use the request `Animate weighted interval scheduling dynamic programming` and verify the absence of a type-specific reference causes an explicit `best-effort` label, coverage-risk disclosure, use of common teaching-design rules, and strengthened reviewer scrutiny rather than rejection or silent first-class treatment.

- [ ] **Step 7：執行最終靜態檢查**

Run:

```powershell
$stale = rg -n "clarification-planner|brief-editor|Phase 1: REQUEST_CONTRACT|階段 1：REQUEST_CONTRACT" SKILL.md SKILL.zh-TW.md agents references
if ($LASTEXITCODE -eq 0) { throw "Stale references remain:`n$stale" }
if ($LASTEXITCODE -ne 1) { throw 'rg failed unexpectedly' }

$placeholders = rg -n "T[B]D|TO[D]O|implement l[a]ter|fill in d[e]tails" SKILL.md SKILL.zh-TW.md agents references
if ($LASTEXITCODE -eq 0) { throw "Placeholder text remains:`n$placeholders" }
if ($LASTEXITCODE -ne 1) { throw 'rg failed unexpectedly' }

git diff --check
```

Expected: no stale references, no placeholder text, and no whitespace errors.

- [ ] **Step 8：提交走讀修正（只有在 Step 3–6 發現缺口時）**

If walkthroughs required repairs, stage only those repaired contract, agent, or reference files and commit:

```powershell
git add SKILL.md SKILL.zh-TW.md agents references
git commit -m "fix: close animation design workflow gaps"
```

If no walkthrough repair was needed, do not create an empty commit.
