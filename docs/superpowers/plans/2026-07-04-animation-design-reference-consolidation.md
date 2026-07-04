# Animation Design Reference Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 `DESIGN_DEVELOPMENT` 的四份通用參考整併成單一 `references/how-to-design-animation.md`，並讓有效引用只指向新文件。

**Architecture:** 新 guide 是共同設計流程、六幕產物契約、教學原則與視覺語言的唯一通用權威來源。`confirmed_requirements.md` 維持動態輸入，array sorting、graph traversal 與 narrowing search 參考維持條件式補充；歷史規格與計畫不回寫。

**Tech Stack:** Markdown、ripgrep、Git

---

## File Structure

- Create `references/how-to-design-animation.md` — `DESIGN_DEVELOPMENT` 唯一通用參考。
- Modify `SKILL.md` — 將必讀清單與六幕格式引用改指向新 guide。
- Modify `references/animation-design-array-sorting.md` — 指明它補充新 guide。
- Modify `references/animation-design-graph-traversal.md` — 指明它補充新 guide。
- Modify `references/animation-design-search.md` — 將 fallback 改指向新 guide。
- Delete `references/animation-design-process.md`、`references/animation-design-document.md`、`references/teaching-design.md`、`references/visual-language.md` — 內容併入新 guide。
- Reference only `docs/superpowers/specs/2026-07-04-animation-design-reference-consolidation-design.md` — 已核准整併契約。

目前工作樹在部分目標檔案已有未提交修改。實作者必須以工作樹內容為整併來源，不得用 `HEAD` 覆蓋；提交前只暫存本計畫範圍，並檢查 staged diff 沒有無關檔案。

### Task 1: 建立單一通用參考

**Files:**
- Create: `references/how-to-design-animation.md`
- Reference: `references/animation-design-process.md`
- Reference: `references/animation-design-document.md`
- Reference: `references/teaching-design.md`
- Reference: `references/visual-language.md`

- [ ] **Step 1: 執行存在性測試並確認失敗**

Run: `test -f references/how-to-design-animation.md`

Expected: exit status `1`，因為新 guide 尚不存在。

- [ ] **Step 2: 建立新 guide**

建立 `references/how-to-design-animation.md`，使用以下完整內容：

````markdown
# 動畫共同設計指南

## 目的、責任與開始條件

`DESIGN_DEVELOPMENT` 的工作是讓主要 Agent 與使用者共同決定演算法要如何被解釋與演示，並持續更新 `animation_design.md`。主要 Agent 負責設計思考與面向使用者的互動，不把這項工作委派給其他 Agent。

開始前，讀取 `confirmed_requirements.md`、本指南，以及唯一一份符合演算法類型的專用參考。沒有相符專用參考時，只使用本指南，不得發明不存在的專用語意。

## 六個固定 Scene 與文件格式

`animation_design.md` 必須依序設計六個獨立 Manim `Scene`：

1. 問題與目標
2. 核心觀念
3. 演算法特有的重要資料與狀態
4. 示範一次關鍵動作
5. 完整演示演算法
6. 最終結果與簡短回顧

每個 Scene 都要包含：

- `Teaching Purpose`：這一幕要讓觀眾理解什麼。
- `Explanation Focus`：解說重點，不寫完整旁白台詞。
- `On-Screen Content`：畫面會出現哪些與教學有關的物件、文字與狀態。
- `Concrete Animation Sequence`：依順序描述觀眾實際看到的動作與狀態變化。

動畫順序必須具體，例如先亮起哪些元素、如何比較、哪些內容如何變暗或移動、狀態框如何更新，以及下一個狀態如何出現。不得只寫「演示比較」或「排除不可能區間」。

不要寫 Manim API、精確秒數、完整旁白、方案比較紀錄、風險清單或自我檢查矩陣。

```markdown
# Animation Design: Algorithm Name

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

- 六個 Scene 的教學功能不可合併或省略。
- 第三個 Scene 不解釋一般程式設計與資料結構基礎，只解釋該演算法特有且必要的資料或狀態。
- 第六個 Scene 顯示最終答案並簡短重述演算法如何從輸入得到結果，不加入預測問題或互動要求。
- Scene 之間固定淡出至空白，再淡入下一幕。

## 共同設計流程

按教學順序逐步設計。每次只向使用者詢問一個決定，避免一次要求使用者評估整套場景規劃。

只有當一個教學部分確實有多種不同且合理的呈現方式時才詢問。字體、間距、局部位置、精確秒數、一般淡出時間與其他例行實作細節由主要 Agent 自行決定。

需要詢問時，提出三個完整方案。每個方案都要同時說明：

- 畫面會出現什麼
- 解說重點
- 觀眾實際會看到的動畫動作順序
- 這種方式如何幫助理解
- 主要 Agent 是否推薦，以及推薦理由

方案必須是具體動畫設計，不得只列抽象方向或把視覺、解說與動作拆成不同問題。

使用者可以選擇其中一個方案、混合不同方案、要求修改，或提出自己的設計。只要使用者提出明確設計，就採用並整合。

使用者做出決定後，直接更新 `animation_design.md` 並進入下一個設計決定。不要在對話中重述決定要求二次確認。

若使用者未指定受眾程度，預設觀眾理解基本程式設計、陣列、索引、變數、迴圈、條件判斷與常見資料結構。第三個 Scene 只解釋該演算法特有且理解時必要的資料或狀態。

## 教學設計原則

選擇能展現演算法關鍵判斷與狀態變化的精簡範例。避免使用已經接近答案、只有單一路徑，或避開演算法代表性操作的輸入。

六幕依序先說明問題與輸入輸出，再建立核心觀念、介紹演算法特有狀態、慢速示範一次完整關鍵動作與理由、用具體輸入完整演示，最後顯示結果並簡短回顧。

先讓造成動作的資料、比較或規則可見，再呈現動作，最後呈現結果。保留足夠的前一狀態，讓觀眾能比較變化，不需要記住已消失的資訊。

同一種顏色、位置、框線或動作在六個 Scene 中應維持相同含義。畫面與解說重點不得表達不同狀態或時序。

只有當不同方式會實際改變觀眾如何理解教學內容時，才提出三個方案。不要把配色、字體、間距、局部位置或精確 timing 當成需要使用者決定的教學方案。

## 視覺語言

同一種顏色、框線、位置、標籤或動作在整部影片中只代表一個意思。必須讓觀眾能區分基本資料、目前焦點、候選項目、已完成進度、已排除區域與必要支援結構。

每個動畫動作只保留一個主要焦點。先讓造成動作的資料或判斷可見，再演示動作，最後顯示結果。非目前焦點的內容可以降低存在感，但不要太早移除理解因果所需的脈絡。

主要資料結構的位置應保持穩定。不要為了局部更新重排整個畫面，也不要讓文字或輔助面板與演算法動畫爭奪注意力。

Queue、stack、搜尋範圍、temporary slot 或其他支援結構只有在它們能解釋演算法行為時才顯示。需要顯示時，讓它們保持可讀，但視覺層級低於目前演算法動作。

- 畫面文字保持短而具體。
- 不用畫面長句重複旁白內容。
- 動作必須幫助說明比較、移動、排除、發現或完成等狀態變化。
- 裝飾性動作不得改變或模糊演算法含義。

## 完成與審查交接

六個 Scene 都依文件格式完成後，派遣獨立 `animation-design-reviewer` 進行內容品質審查。

- 不改變使用者選定呈現方式的問題，由主要 Agent 直接修正。
- 會改變使用者選定呈現方式的問題，必須重新提出修正方案並詢問使用者。
- 每次修正後重新審查，直到 `animation_design_review.md = PASS`。
- 審查通過後，請使用者檢查完整 `animation_design.md`。只有明確核准後才能進入 `CONTRACT`。
````

- [ ] **Step 3: 驗證章節與核心契約**

Run:

```bash
rg -n '^## (目的、責任與開始條件|六個固定 Scene 與文件格式|共同設計流程|教學設計原則|視覺語言|完成與審查交接)$' references/how-to-design-animation.md
rg -n 'Scene 1: Problem and Goal|Scene 6: Result and Recap|Teaching Purpose|Explanation Focus|On-Screen Content|Concrete Animation Sequence|三個完整方案|animation_design_review\.md = PASS|CONTRACT' references/how-to-design-animation.md
```

Expected: 依序找到六個章節；找到六幕範本邊界、四個必要欄位、三方案規則與審查 gate。

- [ ] **Step 4: 驗證格式並提交新 guide**

Run:

```bash
git diff --check -- references/how-to-design-animation.md
git add references/how-to-design-animation.md
git diff --cached --check
git commit -m "docs: consolidate animation design guidance"
```

Expected: 格式檢查通過，staged diff 只有新 guide，commit 成功。

### Task 2: 將有效引用切換至新 guide

**Files:**
- Modify: `SKILL.md:47`
- Modify: `SKILL.md:61`
- Modify: `references/animation-design-array-sorting.md:3`
- Modify: `references/animation-design-graph-traversal.md:3`
- Modify: `references/animation-design-search.md:7`

- [ ] **Step 1: 確認舊引用測試目前失敗**

Run:

```bash
rg -n 'references/(animation-design-process|animation-design-document|teaching-design|visual-language)\.md|通用 teaching-design 與 process' SKILL.md references/animation-design-array-sorting.md references/animation-design-graph-traversal.md references/animation-design-search.md
```

Expected: 找到 `SKILL.md` 的舊必讀清單、舊格式引用與 search fallback，證明尚未完成切換。

- [ ] **Step 2: 更新頂層 skill**

將子階段二開始條件改為：

```markdown
此子階段由目前直接與使用者對話的主要 Agent 負責，不另派設計 subagent。開始前，主要 Agent 必須閱讀 `confirmed_requirements.md`、`references/how-to-design-animation.md`，以及唯一一份符合演算法類型的專用參考。
```

將六幕格式句改為：

```markdown
`animation_design.md` 必須依 `references/how-to-design-animation.md` 設計以下六個獨立 Manim Scene：
```

- [ ] **Step 3: 更新三份專用參考**

使用下列確切措辭：

```markdown
在套用 `references/how-to-design-animation.md` 後，對 array-sorting 動畫使用這份參考。它補充如何理解 comparisons 或 updates、movement、identity 與 progress 的專用決策；不會取代通用流程或產物契約。

在套用 `references/how-to-design-animation.md` 後，對 graph traversal 動畫使用這份參考。它規範 traversal 專有的狀態與支援結構，但不會取代通用流程或 `animation_design.md` 契約。

沒有相符專用參考時，只使用 `references/how-to-design-animation.md`，不得發明 interval semantics。
```

前兩段分別取代 array-sorting 與 graph-traversal 的首段；第三句取代 search「適用性」段落的末句。

- [ ] **Step 4: 驗證新入口**

Run:

```bash
rg -n 'confirmed_requirements\.md.*references/animation-design-guide\.md.*唯一一份符合演算法類型的專用參考' SKILL.md
rg -n 'references/animation-design-guide\.md' SKILL.md references/animation-design-array-sorting.md references/animation-design-graph-traversal.md references/animation-design-search.md
```

Expected: `SKILL.md` 明確列出三類輸入；五個目標位置都指向新 guide。

- [ ] **Step 5: 檢查引用修改的範圍**

Run:

```bash
git diff -- SKILL.md references/animation-design-array-sorting.md references/animation-design-graph-traversal.md references/animation-design-search.md
git diff --check -- SKILL.md references/animation-design-array-sorting.md references/animation-design-graph-traversal.md references/animation-design-search.md
```

Expected: 新增的本次變更只有上述五處語意切換，格式檢查通過。若目標檔案還含本任務開始前的修改，先保留未提交，避免把無關內容納入本任務 commit。

### Task 3: 移除舊文件並執行回歸驗證

**Files:**
- Delete: `references/animation-design-process.md`
- Delete: `references/animation-design-document.md`
- Delete: `references/teaching-design.md`
- Delete: `references/visual-language.md`
- Verify: `SKILL.md`
- Verify: `references/how-to-design-animation.md`
- Verify: `references/animation-design-*.md`

- [ ] **Step 1: 用 patch 刪除四份已取代文件**

刪除下列完整檔案：

```text
references/animation-design-process.md
references/animation-design-document.md
references/teaching-design.md
references/visual-language.md
```

- [ ] **Step 2: 驗證舊文件不存在**

Run: `for f in references/animation-design-process.md references/animation-design-document.md references/teaching-design.md references/visual-language.md; do test ! -e "$f" || exit 1; done`

Expected: exit status `0`。

- [ ] **Step 3: 驗證沒有有效的舊引用**

Run:

```bash
rg -n 'references/(animation-design-process|animation-design-document|teaching-design|visual-language)\.md' . --glob '*.md' --glob '*.yaml' --glob '!docs/superpowers/**'
```

Expected: exit status `1`，沒有輸出；歷史 `docs/superpowers/` 明確排除。

- [ ] **Step 4: 驗證內容契約沒有流失**

Run:

```bash
rg -n 'Scene 1: Problem and Goal|Scene 2: Core Concept|Scene 3: Algorithm-Specific Data and State|Scene 4: One Key Action|Scene 5: Full Algorithm Demonstration|Scene 6: Result and Recap' references/how-to-design-animation.md
rg -n 'Teaching Purpose|Explanation Focus|On-Screen Content|Concrete Animation Sequence|三個完整方案|animation-design-reviewer|animation_design_review\.md = PASS|使用者.*明確核准' SKILL.md references/how-to-design-animation.md
```

Expected: 六幕全部存在；四個欄位、三方案、獨立審查、PASS 與使用者核准 gate 全部可定位。

- [ ] **Step 5: 執行整體格式與範圍檢查**

Run:

```bash
git diff --check
git status --short
```

Expected: 格式檢查通過；status 只包含原有工作樹修改與本計畫列出的變更，沒有額外檔案。

- [ ] **Step 6: 提交可安全隔離的剩餘變更**

四份舊文件在本任務開始前已有未提交修改；刪除會取代那些工作樹內容。先確認新 guide 完整吸收其現行內容，再只暫存四份刪除：

```bash
git add references/animation-design-process.md references/animation-design-document.md references/teaching-design.md references/visual-language.md
git diff --cached --check
git commit -m "docs: remove superseded animation design references"
```

Expected: staged diff 只刪除四份已取代文件，commit 成功。`SKILL.md` 與專用參考若混有本任務前修改，維持未提交並在交付時說明。
