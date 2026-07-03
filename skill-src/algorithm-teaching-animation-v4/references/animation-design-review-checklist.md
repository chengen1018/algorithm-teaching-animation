# 動畫設計審查檢查表

## 審查前提

- 只審查 designer 已標記為 `DESIGN_READY` 且已交接做獨立審查的 `animation_design.md` 版本。
- 明確辨識受審的精確設計版本。只要發生任何編輯，先前的 `animation_design_review.md` 就不再適用。
- 在審查開始時讀取 `animation_design.md` 的精確位元組並計算其 SHA-256 摘要。在最終定稿前立刻重新讀取檔案、重新計算摘要，並確認位元組仍與受審版本一致。若審查過程中版本發生變更，則應以新位元組重新開始，或直接回傳 `FAIL`。
- 讀取 intake 與該演算法類別所路由到的設計參考。確認 reviewer 並非設計的作者或修復者。
- 審查期間不得請求外部使用者核准。只有在這個精確版本獲得 `PASS` 後，才能請求外部核准。
- 以 `references/animation-design-process.md` 作為 `DESIGN_READY` gate 條件的權威來源。證據矩陣必須根據其中每一個 canonical gate condition 建立，不論受審 `animation_design.md` 是否在自己的自檢中重複列出它們。

## 審查範圍選擇

記錄 `Review Scope: Full` 或 `Review Scope: Delta`，並說明為何此範圍有效。若影響不確定，就使用 full review。
若範圍是 `Delta`，在審查繼續前，必須記錄 base reviewed SHA-256 與界定清楚的 reviewed change set / locations；若其中任何一項無法界定，就升級為 `Full`。

### Full Review

第一次審查一律使用 full review。當修改涉及演算法語意、主要心智模型、核心視覺隱喻或視覺語意、教學弧線、場景結構、高層節拍，或任何跨區 / 不確定影響的變更時，也必須使用 full review。需檢查整份文件與每一項 `DESIGN_READY` 條件。

### Delta Review

只有在變更明確局部，且其完整影響可被追蹤時，才可使用 delta review。必須檢查變更文字、每個相依章節、內部一致性、保留的使用者決策，以及更新後的 `DESIGN_READY` 自檢。只要變更影響或可能影響演算法語意、主要心智模型、核心視覺語意、教學弧線、場景結構或高層節拍，就必須立刻升級為 full review。

## 教學一致性

必須有證據證明設計具備清楚的受眾與學習目標、一個忠實的主要心智模型、能暴露重要行為的教學 sample，以及每個高層 beat 都在為下一個 beat 鋪路的教學弧線。還要確認可見證據能支撐預期觀眾推論，並預防已點名的誤解。

## 視覺可行性

必須有證據證明視覺隱喻、穩定視覺語意、結構呈現、場景區域、資訊層級與高層節拍，可以在不產生矛盾編碼、隱藏教學關鍵狀態、焦點過載或無法解釋的版面變化下實作。可行性不要求低層 Manim 編排。

## 演算法語意一致性

必須有證據證明演算法變體、狀態、不變量、邊界與 tie 慣例、轉換、終止條件、sample 結果、心智模型、視覺編碼與節拍彼此一致。呈現選擇不得暗示演算法其實沒有的行為或保證。

## 高影響缺口檢查

若仍有任何未解決問題會實質改變演算法語意、主要心智模型、核心視覺隱喻或語意、教學弧線、場景結構或高層節拍，就必須判定失敗。不要把核心缺口降格成 best-effort 備註。必須確認所有重要使用者決策都被忠實表達，且只剩下有記錄的低影響預設值。

## Best-Effort 強化審查

當沒有相符的型別專用設計參考時，必須要求設計把該類別標示為 best-effort，並揭露因此產生的覆蓋風險。應透過 intake 與通用設計參考，直接檢查該類別專有語意、資料結構狀態、可能誤解與視覺可行性。unsupported-category routing 本身不是自動失敗，但未揭露風險或存在未解決高影響缺口就一定失敗。

## 必要結果格式

請用以下全部欄位與章節撰寫 `animation_design_review.md`：

```markdown
# Animation Design Review

- Reviewed Design Version: <exact version identifier>
- Reviewed Design SHA-256: <64-character lowercase SHA-256 digest of the exact animation_design.md bytes reviewed>
- Review Scope: Full | Delta
- Scope Rationale: <why this scope is valid>
- Base Reviewed SHA-256: <prior reviewed SHA-256 for Delta, or None for Full>
- Reviewed Change Set / Locations: <bounded changed lines/sections for Delta, or None for Full>

## DESIGN_READY Evidence Matrix

| DESIGN_READY Condition | Result | Concrete Evidence and Location | N/A Justification |
|---|---|---|---|
| <one row for every DESIGN_READY condition> | PASS \| FAIL \| N/A | <specific evidence and section/location, or None only for justified N/A> | <required for N/A; otherwise None> |

## Teaching Coherence Evidence
<specific evidence from animation_design.md>

## Visual Feasibility Evidence
<specific evidence from animation_design.md>

## Algorithm Semantic Consistency Evidence
<specific evidence from animation_design.md>

## Unresolved Issues
<issues, or None>

## Required Repairs
<repairs, or None>

## Rollback Target
<DESIGN_DEVELOPMENT for FAIL, or None for PASS>

## Verdict
PASS | FAIL
```

只能輸出一個判定：`PASS` 或 `FAIL`。不要輸出混合式、條件式、暫定式，或第二個判定。結果中必須寫出審查範圍、教學一致性證據、視覺可行性證據、語意一致性證據、未解決問題、必要修復與回退目標，即使某欄位內容是 `None` 也一樣。

證據矩陣必須對 `references/animation-design-process.md` 中每一個 canonical `DESIGN_READY` gate condition 都剛好對應一列或一項。每列都必須說明條件、結果，以及帶有章節或其他精確位置的具體證據。只有在審查明確說明為何不適用，且解釋 governing requirement 仍如何被滿足時，某條件才可標為 `N/A`。若缺列、缺證據、`N/A` 沒解釋，或有失敗條件，都不能 `PASS`。
證據矩陣不能只依賴受審設計中的自檢；若漏掉任何 canonical gate condition、證據或位置，就不得 `PASS`。

## PASS 條件

只有當下列所有條件都成立時才能回傳 `PASS`：所選審查範圍有效；所記錄的 SHA-256 精確對應受審位元組；若為 `Delta`，則 base reviewed SHA-256 與界定清楚的 reviewed change set / locations 已存在且符合審查範圍；若為 `Full`，兩者都必須是 `None`；`references/animation-design-process.md` 中每個 canonical `DESIGN_READY` gate condition 都在證據矩陣中有一列，且要嘛有具體證據與位置而通過，要嘛有明確合理的 `N/A` 處理；教學一致性、視覺可行性與演算法語意一致性都通過；重要使用者決策被保留；沒有高影響缺口；best-effort 覆蓋風險已揭露且審查充分強化。若為 `PASS`，則 `Unresolved Issues` 與 `Required Repairs` 必須是 `None`，且 `Rollback Target` 也必須是 `None`。

`animation_design_review.md = PASS` 只授權請求該精確已審版本的使用者明確核准。在該版本核准前，禁止轉換成 `pre_build_brief.md`；任何設計編輯都會使審查失效，並使設計回到 `DESIGN_DEVELOPMENT`。

## FAIL 與回退規則

若有任何缺少證據、矛盾、回歸、無支撐主張、遺失使用者決策、無效審查範圍、失敗的 `DESIGN_READY` 條件、未揭露的 best-effort 風險，或未解決的高影響缺口，都必須回傳 `FAIL`。要明確指出必要修復，並把回退目標設為 `DESIGN_DEVELOPMENT`。

reviewer 只報告缺陷，不得撰寫或修復 `animation_design.md`。修復後，designer 必須產出新的 `DESIGN_READY` 版本並請求新的獨立審查。失敗或過期的審查都不能授權外部核准或轉換到 `pre_build_brief.md`。
