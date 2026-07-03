# Animation Design Process Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 `references/animation-design-process.md` 重整為容易閱讀、可直接執行的流程文件，同時完整保留既有契約語意。

**Architecture:** 只修改一份權威流程文件。先將分散的規則重新排列為「範圍、步驟、提問判準、設計內容、通過條件、審查核准、修改回退、禁止事項」，再逐項比對原始契約與相依 reviewer 規則，避免可讀性改寫意外改變 gate。

**Tech Stack:** Markdown、Git diff、ripgrep

---

## File Structure

- Modify: `references/animation-design-process.md` — `DESIGN_DEVELOPMENT` 與 canonical `DESIGN_READY` gate 的權威流程文件。
- Reference only: `docs/superpowers/specs/2026-07-03-animation-design-process-rewrite-design.md` — 已核准的改寫範圍與結構。
- Reference only: `references/animation-design-review-checklist.md` — 確認 reviewer 對 canonical gate、Full Review、Delta Review 及 `PASS` 的依賴沒有被破壞。

### Task 1: 依核准結構改寫流程文件

**Files:**
- Modify: `references/animation-design-process.md`
- Reference: `docs/superpowers/specs/2026-07-03-animation-design-process-rewrite-design.md`

- [x] **Step 1: 保存改寫前的契約檢查基準**

執行：

```bash
git diff -- references/animation-design-process.md
rg -n "^## |DESIGN_READY|Full Review|Delta Review|使用者編輯|回退|失敗條件" references/animation-design-process.md
```

預期：目標檔案尚無未提交修改，並列出原有九個主要章節、`DESIGN_READY` 條件、審查範圍與回退規則。

- [x] **Step 2: 將內容重整為八個執行導向章節**

使用以下固定章節順序完整改寫 `references/animation-design-process.md`：

```markdown
# 動畫設計流程

## 1. 這份文件管什麼
## 2. 整體流程
## 3. 哪些問題需要詢問使用者
## 4. 動畫設計必須完成什麼
## 5. DESIGN_READY 通過清單
## 6. 通過後：獨立審查與使用者核准
## 7. 文件修改、重新審查與回退
## 8. 禁止事項
```

改寫時必須做到：

- 使用「設計者」「協調者」「獨立審查者」作為角色名稱。
- 保留 `DESIGN_DEVELOPMENT`、`DESIGN_READY`、Full Review、Delta Review、`animation_design.md`、`animation_design_review.md`、`PASS`、`CONTRACT` 等正式名稱。
- 將整體流程寫成六個有順序的步驟。
- 在第三節明確區分阻塞性的核心問題與使用 best-effort 預設值處理的低影響細節。
- 保留「小批問題、一次只問一題、整批答案一次交回設計者」的批次協定。
- 將審查範圍、文件修改與回退方式整理成決策表。
- 將重複失敗說明收斂到第八節，不刪除任何實質禁止行為。

- [x] **Step 3: 原樣保留十五項 canonical DESIGN_READY conditions 的個別可審查性**

第五節必須逐條保留以下十五項條件，不得合併成較少項目：

1. 設計目標與受眾明確。
2. 演算法變體與操作語意沒有歧義。
3. 主要心智模型明確且技術正確。
4. 已辨識觀眾誤解與預防方式。
5. 範例輸入適合且有教學理由。
6. 型別專用要求已處理；無相符參考時記錄 best-effort 分類、具體覆蓋風險與強化審查要求。
7. 核心視覺隱喻與視覺語意已定義。
8. 結構呈現、場景結構與資訊層級已定義。
9. 教學弧線一致。
10. 高階動畫節拍能呈現重要狀態轉換與因果關係。
11. 推薦設計與重要替代方案都有理由與取捨。
12. 所有重要使用者決策已忠實納入。
13. 沒有未解決的阻塞性核心問題。
14. 剩餘低影響項目均記錄風險及 best-effort 預設值。
15. 設計文件符合必要契約與自檢要求。

- [x] **Step 4: 明確寫出不可顛倒的 gate 順序**

第六節必須包含：

```text
DESIGN_READY
  → 獨立審查 animation_design.md
  → animation_design_review.md = PASS
  → 使用者核准同一精確版本
  → 進入 CONTRACT
```

並明確說明：`PASS` 不能取代使用者核准；使用者核准不能取代獨立審查；沉默、未回覆或只編輯檔案都不是核准。

### Task 2: 驗證改寫沒有改變契約

**Files:**
- Verify: `references/animation-design-process.md`
- Reference: `references/animation-design-review-checklist.md`
- Reference: `docs/superpowers/specs/2026-07-03-animation-design-process-rewrite-design.md`

- [x] **Step 1: 執行格式與占位文字檢查**

執行：

```bash
git diff --check -- references/animation-design-process.md
rg -n "TBD|TODO|待定|placeholder" references/animation-design-process.md
```

預期：`git diff --check` 無輸出；占位文字搜尋無結果。

- [x] **Step 2: 驗證必要流程名稱與關卡仍存在**

執行：

```bash
rg -n "DESIGN_DEVELOPMENT|DESIGN_READY|Full Review|Delta Review|animation_design_review\.md|PASS|CONTRACT|best-effort" references/animation-design-process.md
```

預期：每個正式名稱至少出現一次，且位於對應的設計、通過、審查或回退章節。

- [x] **Step 3: 逐項核對 reviewer 的權威依賴**

對照 `references/animation-design-review-checklist.md`，確認改寫後文件仍明確要求：

- reviewer 對每個 canonical `DESIGN_READY` condition 提供證據；
- 初次審查一律使用 Full Review；
- 核心語意或跨區／不確定影響的修改使用 Full Review；
- Delta Review 只適用於範圍明確且影響可完整追蹤的局部修改；
- Delta 發現跨區影響時升級為 Full Review；
- 審查失敗或下游發現核心缺口時回到 `DESIGN_DEVELOPMENT` 並停止下游工作。

預期：六項全部能在改寫後文件中找到明確句子，沒有靠推論才能成立的規則。

- [x] **Step 4: 檢視完整差異**

執行：

```bash
git diff --word-diff=plain -- references/animation-design-process.md
```

預期：差異只涉及重排、簡化措辭、加入流程與決策表；沒有刪除角色限制、gate、審查範圍、精確版本核准或回退義務。

- [ ] **Step 5: 提交改寫**

```bash
git add references/animation-design-process.md docs/superpowers/plans/2026-07-03-animation-design-process-rewrite.md
git commit -m "docs: clarify animation design process"
```

預期：只提交目標流程文件與本執行計畫，不包含工作樹中既有的其他修改。
