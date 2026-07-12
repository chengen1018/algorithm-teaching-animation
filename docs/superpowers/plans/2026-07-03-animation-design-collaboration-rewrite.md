# Collaborative Animation Design Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `DESIGN_DEVELOPMENT` so the main Agent and user jointly design six concrete Manim Scenes, followed by focused content review without SHA, evidence-matrix, high-impact, or Full/Delta design-review governance.

**Architecture:** The top-level skill owns user interaction and writes `animation_design.md` incrementally. Focused references define the six-Scene template, option format, and reviewer checks. The downstream brief remains a mechanical handoff, while obsolete animation-design governance is removed.

**Tech Stack:** Markdown skill contracts, YAML Agent metadata, `rg` and `git diff` static verification.

---

## File map

- Modify `SKILL.md` and `agents/openai.yaml`: assign collaborative design to the main Agent and simplify the Stage 1 gates.
- Delete `agents/animation-designer.md`: interactive design no longer uses a designer sub-agent.
- Rewrite `references/animation-design-process.md` and `references/animation-design-document.md`: define the interaction loop and six-Scene document.
- Modify `references/teaching-design.md` and `references/animation-design-search.md`: align supporting guidance with the approved flow.
- Delete `references/high-impact-clarification.md`.
- Rewrite `agents/animation-design-reviewer.md` and `references/how-to-review-design.md`: retain only content-quality review.
- Rewrite `references/pre-build-brief.md`: retain a simple downstream handoff without version governance.
- Modify downstream files found by scoped searches: remove stale high-impact and design-SHA dependencies while preserving unrelated script, render, and QA rules.

## Task 1: Capture the failing baseline

**Files:**
- Test: `SKILL.md`
- Test: `agents/*.md`
- Test: `references/*.md`

- [ ] **Step 1: Confirm old designer delegation exists**

Run:

```bash
rg -n "animation-designer|high-impact-clarification" SKILL.md agents/openai.yaml agents references
```

Expected: several matches. This is the RED baseline.

- [ ] **Step 2: Confirm old design-review governance exists**

Run:

```bash
rg -n "SHA-256|證據矩陣|Full Review|Delta Review|DESIGN_READY" SKILL.md agents/animation-design-reviewer.md references/animation-design-process.md references/animation-design-document.md references/how-to-review-design.md references/pre-build-brief.md
```

Expected: several matches.

- [ ] **Step 3: Record and preserve the dirty-worktree boundary**

Run:

```bash
git status --short
git diff -- SKILL.md agents/animation-designer.md agents/openai.yaml references/how-to-collect-requirements.md references/intake-contract.md
```

Expected: existing user-owned changes are visible. Do not discard them or overwrite the affected files wholesale.

## Task 2: Move interactive design to the main Agent

**Files:**
- Modify: `SKILL.md`
- Modify: `agents/openai.yaml`
- Delete: `agents/animation-designer.md`

- [ ] **Step 1: Rewrite `DESIGN_DEVELOPMENT` ownership**

Replace designer delegation with:

```markdown
此子階段由目前直接與使用者對話的主要 Agent 負責，不派遣 `animation-designer`。主要 Agent 讀取已確認需求與動畫設計參考，然後與使用者逐步共同設計並持續更新 `animation_design.md`。
```

- [ ] **Step 2: Implement the option loop**

Add these rules to `SKILL.md`:

```markdown
每次只處理一個設計決定。只有某個教學部分確實存在多種有意義的呈現方式時，才提出三個完整方案。每個方案同時說明畫面內容、解說重點、具體動畫動作順序、如何幫助理解，以及主要 Agent 的推薦與理由。

使用者可以選擇、混合、修改方案，或提出自己的設計。決定後直接更新 `animation_design.md` 並繼續，不重述決定要求二次確認。字體、間距、局部位置與精確秒數等細節由 Agent 自行處理。
```

- [ ] **Step 3: Replace the design-review flow**

Use this order in `SKILL.md`:

```text
joint design → independent content review → repair → repeat review until PASS → final user review and approval → downstream handoff
```

If a repair changes a user-selected presentation, require a new proposal and user decision. Remove exact-byte approval, design SHA checks, DESIGN_READY matrices, and Full/Delta animation-design review.

- [ ] **Step 4: Update `agents/openai.yaml`**

The default prompt must assign the main Agent to joint design, six-Scene document updates, review repair, and final user approval. It must not mention `animation-designer` or design SHA lineage.

- [ ] **Step 5: Delete `agents/animation-designer.md` and verify ownership**

Run:

```bash
rg -n "animation-designer" SKILL.md agents/openai.yaml agents references
```

Expected: no output.

## Task 3: Rewrite collaborative design references

**Files:**
- Rewrite: `references/animation-design-process.md`
- Rewrite: `references/animation-design-document.md`
- Modify: `references/teaching-design.md`
- Modify: `references/animation-design-search.md`
- Delete: `references/high-impact-clarification.md`

- [ ] **Step 1: Rewrite the process document**

Keep these sections:

```markdown
# 動畫共同設計流程
## 目的與責任
## 六個固定 Scene
## 一次處理一個設計決定
## 何時提出三個方案
## 每個方案必須包含什麼
## 如何記錄使用者選擇
## 不詢問的一般實作細節
## 完成與審查交接
```

The fixed sequence is: problem and goal, core concept, algorithm-specific data/state, one key action, full demonstration, and result/recap. Explicitly exclude repeated-pattern and audience-prediction phases.

- [ ] **Step 2: Rewrite the design-document template**

Use these six Scene sections, each with the same four required fields:

```markdown
## Scene 1: Problem and Goal
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 2: Core Concept
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 3: Algorithm-Specific Data and State
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 4: One Key Action
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 5: Full Algorithm Demonstration
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 6: Result and Recap
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence
```

Require visible action order. Prohibit full narration, Manim API calls, timings, risk inventories, alternatives logs, and self-check matrices.

- [ ] **Step 3: Align teaching and type-specific guidance**

Update `references/teaching-design.md` to use the six-part sequence while retaining sample choice, visible cause before effect, stable semantics, and meaningful alternatives. Update `references/animation-design-search.md` to remove best-effort/high-impact escalation while retaining its applicability boundary and search guidance.

- [ ] **Step 4: Delete the high-impact reference**

Delete `references/high-impact-clarification.md` after all useful presentation guidance is represented by the new process.

- [ ] **Step 5: Verify all six Scene headings**

Run:

```bash
rg -n "Scene 1: Problem and Goal|Scene 2: Core Concept|Scene 3: Algorithm-Specific Data and State|Scene 4: One Key Action|Scene 5: Full Algorithm Demonstration|Scene 6: Result and Recap" references/animation-design-document.md
```

Expected: six matches.

## Task 4: Replace design-review governance with content review

**Files:**
- Rewrite: `agents/animation-design-reviewer.md`
- Rewrite: `references/how-to-review-design.md`

- [ ] **Step 1: Rewrite the reviewer role**

Require checks for algorithm correctness, sample/result correctness, six-Scene coherence, visual/explanation/action agreement, visible cause-action-result, consistent visual meaning, production readiness, and preservation of user choices. The reviewer reports problems but never edits or redesigns.

- [ ] **Step 2: Use a concise review artifact**

```markdown
# Animation Design Review
## Algorithm Correctness
PASS | FAIL — 簡要說明演算法、範例與結果的檢查結果
## Teaching Coherence
PASS | FAIL — 簡要說明六個 Scene 的教學連貫性
## Visual and Explanation Consistency
PASS | FAIL — 簡要說明畫面、解說重點與動畫動作是否一致
## Production Readiness
PASS | FAIL — 簡要說明文件是否足以供後續製作
## User Decision Preservation
PASS | FAIL — 簡要說明使用者選定的設計是否完整保留
## Required Repairs
沒有問題時寫 None；有問題時列出具體修正要求
## Verdict
PASS | FAIL
```

Any failed category produces overall `FAIL`.

- [ ] **Step 3: Verify forbidden design-review concepts are absent**

Run:

```bash
rg -n "SHA-256|證據矩陣|Full Review|Delta Review|DESIGN_READY|high-impact|高影響|低影響" agents/animation-design-reviewer.md references/animation-design-process.md references/animation-design-document.md references/how-to-review-design.md
```

Expected: no output.

## Task 5: Simplify the downstream handoff

**Files:**
- Rewrite: `references/pre-build-brief.md`
- Modify: `SKILL.md`
- Modify scoped matches in: `agents/qa-verifier.md`, `agents/scene-reviewer.md`, `agents/scene-writer.md`, `agents/script-reviewer.md`, `agents/script-writer.md`, `agents/voiceover-manifest.md`, `references/manim-guidelines.md`, `references/how-to-hand-off-a-render-for-review.md`, `references/render-qa-checklist.md`, `references/how-to-review-manim-scene-code.md`, `references/script-review-checklist.md`, `references/teaching-script.md`, `references/voiceover.md`

- [ ] **Step 1: Rewrite the brief as a mechanical handoff**

Keep only:

```markdown
# Pre-build Brief
## Algorithm and Audience
## Sample Input
## Confirmed User Requirements
## Six-Scene Outline
## Chosen Visual Rules
## Narration and On-Screen Language
## Delivery Requirements
```

It must faithfully condense reviewed, user-approved `animation_design.md`; it must not add decisions, require SHA lineage, contain high-impact inventory, or require a second approval gate.

- [ ] **Step 2: Remove animation-design SHA prerequisites**

Replace design/brief SHA checks in `SKILL.md` with the plain prerequisite that the current design passed content review, received final user approval, and the brief faithfully reflects it.

- [ ] **Step 3: Rephrase obsolete downstream high-impact language**

Use direct wording such as:

```text
missing or conflicting algorithm behavior, teaching presentation, Scene structure, or user-selected design
```

Preserve unrelated Full/Delta rules for rendered-scene review; only animation-design Full/Delta review is removed.

- [ ] **Step 4: Add the six-Scene implementation rule**

Update `SKILL.md` and `references/manim-guidelines.md`: implement six independent Manim `Scene` classes, render separately, use fade-to-blank/fade-in boundaries, concatenate in order, and do not substitute Manim `Section`.

- [ ] **Step 5: Verify downstream coherence**

Run:

```bash
rg -n "Source Design SHA-256|Reviewed Design SHA-256|Approved Design SHA-256|Approved Brief SHA-256|Resolved High-Impact Clarifications" SKILL.md agents references
```

Expected: no output.

## Task 6: Validate the complete rewrite

**Files:**
- Verify: `SKILL.md`
- Verify: `agents/*.md`
- Verify: `references/*.md`
- Verify: `agents/openai.yaml`

- [ ] **Step 1: Run repository-wide forbidden-term checks**

Run:

```bash
rg -n "animation-designer|high-impact-clarification|Resolved High-Impact Clarifications|Source Design SHA-256|Reviewed Design SHA-256|Approved Design SHA-256|Approved Brief SHA-256" SKILL.md agents references
```

Expected: no output.

- [ ] **Step 2: Verify required concepts**

Run:

```bash
rg -n "三個.*方案|推薦|六個獨立|animation-design-reviewer|使用者.*核准" SKILL.md references/animation-design-process.md references/animation-design-document.md agents/animation-design-reviewer.md
```

Expected: matches for option design, recommendation, six independent Scenes, independent review, and final approval.

- [ ] **Step 3: Check formatting and stale paths**

Run:

```bash
git diff --check
test ! -e agents/animation-designer.md
test ! -e references/high-impact-clarification.md
rg -n "agents/animation-designer.md|references/high-impact-clarification.md" . --glob '*.md' --glob '*.yaml'
```

Expected: the first three checks succeed and the final `rg` prints no output.

- [ ] **Step 4: Review the final diff**

Run:

```bash
git diff --stat
git diff -- SKILL.md agents references
```

Expected: every change maps to collaborative design, six independent Scenes, focused content review, or removal of obsolete design governance. Existing requirement-collection changes remain intact.

- [ ] **Step 5: Commit only safe, intended changes**

Inspect `git status --short` and the baseline diff from Task 1. Do not stage unrelated user-owned changes. If overlapping pre-existing hunks cannot be separated safely, leave implementation unstaged and report the constraint instead of committing them.
