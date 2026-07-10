# Specialized Design Reference Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `DESIGN_DEVELOPMENT` explicitly select the one applicable specialized animation-design reference.

**Architecture:** `references/how-to-design-animation.md` is the single authority for the algorithm-category-to-reference mapping. `SKILL.md` requires the main Agent to follow that mapping before design begins, without duplicating the table. No downstream agent configuration changes.

**Tech Stack:** Markdown, ripgrep, Git.

## Global Constraints

- Preserve the pre-existing unstaged `SKILL.md` script-writer wording change.
- Do not alter any custom-agent TOML files.
- Read only one specialized reference; no matching category means only the shared guide applies.

---

### Task 1: Add the shared-guide selection table

**Files:**
- Modify: `references/how-to-design-animation.md:5-7`
- Test: repository text assertions

- [ ] **Step 1: Verify the selection table is absent**

Run: `rg -n 'animation-design-(array-sorting|graph-traversal|search)\.md|專用參考選擇' references/how-to-design-animation.md`

Expected: exit status `1` because the shared guide does not yet name the specialized references.

- [ ] **Step 2: Add the start condition and mapping**

Immediately after the purpose paragraph, add a `## 專用參考選擇` section that requires reading `confirmed_requirements.md` and this guide, then provides this table:

```markdown
| 演算法類型 | 必讀的專用參考 |
| --- | --- |
| Array sorting | `references/animation-design-array-sorting.md` |
| Graph traversal | `references/animation-design-graph-traversal.md` |
| 區間或候選區域收縮型 search | `references/animation-design-search.md` |
| 其他演算法類型 | 無；只使用本指南。 |
```

State that exactly one matching reference may be read, and that unmatched algorithms must not inherit specialized sorting, traversal, or interval semantics.

- [ ] **Step 3: Verify all selection outcomes**

Run: `rg -n 'confirmed_requirements\.md|animation-design-array-sorting\.md|animation-design-graph-traversal\.md|animation-design-search\.md|只使用本指南|唯一.*專用參考' references/how-to-design-animation.md`

Expected: one output set covering the prerequisite, three mappings, fallback, and one-reference rule.

### Task 2: Link the workflow entry to the selection rule

**Files:**
- Modify: `SKILL.md:47`
- Test: repository text assertions and diff scope review

- [ ] **Step 1: Confirm the existing generic wording**

Run: `rg -n '唯一一份符合演算法類型的專用參考' SKILL.md`

Expected: one match at the `DESIGN_DEVELOPMENT` start condition.

- [ ] **Step 2: Replace only the design-stage sentence**

Replace the line at `SKILL.md:47` with:

```markdown
開始前，主要 Agent 必須閱讀 `confirmed_requirements.md` 與 `references/how-to-design-animation.md`，並依該指南的「專用參考選擇」讀取唯一一份相符的專用參考；若沒有相符類型，則只使用共通指南。完整遵循這些文件完成 DESIGN_DEVELOPMENT。
```

- [ ] **Step 3: Verify the link and preserve user changes**

Run: `rg -n '專用參考選擇|若沒有相符類型，則只使用共通指南' SKILL.md && git diff -- SKILL.md`

Expected: the new entrypoint wording is present, and the diff retains the pre-existing script-writer wording change without modifying it.

### Task 3: Run final document verification

**Files:**
- Verify: `SKILL.md`
- Verify: `references/how-to-design-animation.md`

- [ ] **Step 1: Run formatting and cross-reference checks**

Run:

```bash
git diff --check -- SKILL.md references/how-to-design-animation.md
rg -n 'animation-design-(array-sorting|graph-traversal|search)\.md|其他演算法類型|只使用本指南' references/how-to-design-animation.md
rg -n '專用參考選擇|若沒有相符類型，則只使用共通指南' SKILL.md
```

Expected: formatting exits `0`; the guide names all three references and its fallback; `SKILL.md` links to the selection rule and fallback.

- [ ] **Step 2: Review change ownership**

Run: `git diff --name-only && git diff -- SKILL.md references/how-to-design-animation.md`

Expected: only the planned guide addition and `SKILL.md:47` change are introduced by this task; the existing script-writer edit remains visibly separate and unstaged.
