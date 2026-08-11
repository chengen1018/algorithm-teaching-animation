# 動畫設計內容審查

Reviewer 只檢查動畫設計的內容品質，不重新設計動畫。

本文件提供完整的共通審查標準。若 coordinator 另外提供一份與演算法類型相符的專用 reference，再加上其中列出的演算法特有條件。

## 檢查項目

### Algorithm Correctness

確認演算法步驟、狀態更新、範例輸入與最終結果正確。

### Teaching Coherence

確認設計必須包含四個獨立 Scene，並依序完成下列互不重疊的教學責任：

- Scene 1「問題與目標」必須建立具體問題、具實際值的完整代表性輸入，以及本題要求尋找、改變或判定的對象；不得提前介紹演算法機制或追蹤狀態。
- Scene 2「演算法如何運作：決策規則與追蹤狀態」只建立理解 Scene 3 代表性範例所需的概念性運作模型，介紹該範例會使用的重要判斷方向與主要追蹤狀態，並以一次最小局部操作呈現因果；不得完整執行範例或列舉未使用的分支。
- Scene 3「完整演示演算法」必須是唯一一次從完整代表性輸入執行到停止狀態的全程演示，沿著範例實際發生的路徑呈現每個重要觀察或比較、判斷、動作與狀態更新；不得加入 Scene 2 未建立的新機制。
- Scene 4「最終結果與簡短回顧」必須明確標出答案、確認它回應 Scene 1 的問題，並只使用一至三個已演示的核心處理概念進行回顧；不得重播完整範例或引入新內容。

不得有尚未介紹的重要機制、無法解釋的跳躍，或跨 Scene 重複同一段完整因果演示。Scene 2 不必窮舉代表性範例不會使用的分支，也不要求觀眾在完整演示前已能獨立執行演算法。

### Visual and Explanation Consistency

確認畫面、解說重點與動畫動作表達同一件事；原因、動作及結果都可見；相同視覺線索前後含義一致。

### Production Readiness

確認每個 Scene 都有教學目的、解說重點、畫面內容、具體動畫順序、完成條件與責任邊界，且後續腳本與 Manim 實作者不需要猜測教學結構或動畫演法。

### User Decision Preservation

確認所有使用者選定、混合、修改或自行提出的設計都已忠實寫入。

## 結果格式

```markdown
# Animation Design Review

## Algorithm Correctness
PASS | FAIL — 簡要說明檢查結果

## Teaching Coherence
PASS | FAIL — 簡要說明檢查結果

## Visual and Explanation Consistency
PASS | FAIL — 簡要說明檢查結果

## Production Readiness
PASS | FAIL — 簡要說明檢查結果

## User Decision Preservation
PASS | FAIL — 簡要說明檢查結果

## Required Repairs
沒有問題時寫 None；有問題時列出具體修正要求

## Verdict
PASS | FAIL
```

任一項失敗，整體判定就是 `FAIL`。Reviewer 只報告問題，不得直接修改設計。
