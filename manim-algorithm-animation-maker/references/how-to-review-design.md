# 動畫設計內容審查

Reviewer 只檢查動畫設計的內容品質，不重新設計動畫。

本文件提供完整的共通審查標準。若 coordinator 另外提供一份與演算法類型相符的專用 reference，再加上其中列出的演算法特有條件。

## 檢查項目

### Algorithm Correctness

確認演算法步驟、狀態更新、範例輸入與最終結果正確。

### Teaching Coherence

確認設計包含正好五個獨立 Scene，並依序完成下列互不重疊的教學責任：

- Scene 1「問題與目標」必須建立具體問題、具實際值的完整代表性輸入，以及本題要求尋找、改變或判定的對象；不得提前介紹演算法機制或追蹤狀態。
- Scene 2「演算法如何運作：決策規則與追蹤狀態」只建立理解 Scene 3 代表性範例所需的概念性運作模型，介紹該範例會使用的重要判斷方向與主要追蹤狀態，並以一次最小局部操作呈現因果；不得完整執行範例或列舉未使用的分支。
- Scene 3「完整演示演算法」必須是唯一一次從完整代表性輸入執行到停止狀態的全程演示，沿著範例實際發生的路徑呈現每個重要觀察或比較、判斷、動作與狀態更新，結尾直接顯示範例答案，並留下 Scene 4 能沿用的工作單位語意。
- Scene 4「複雜度分析」必須從 Scene 3 的 sample cues 一般化為 input-size work count，完整涵蓋已核准的 `Complexity Scope`。
- Scene 5「最終總結」只整理 Scene 3 的答案、核心方法與 Scene 4 已教過的 complexity。

不得有尚未介紹的重要機制、無法解釋的跳躍，或跨 Scene 重複同一段完整因果演示。Scene 2 不必窮舉代表性範例不會使用的分支，也不要求觀眾在完整演示前已能獨立執行演算法。

### Visual and Explanation Consistency

確認畫面、解說重點與動畫動作表達同一件事；原因、動作及結果都可見；相同視覺線索前後含義一致。

### Complexity Analysis

依 `how-to-design-complexity-analysis.md` 獨立檢查：

- Analysis Basis 的 algorithm variant、input variables、assumptions、counted operation、derivation 與 source locator 能支撐每個 claim。
- 至少一個 primary time case 或使用者選定的 replacement time case 已獲明確核准。
- 每個 case label 與分析模型一致，並保持 worst、average、expected 與 amortized 的正確含義。
- 每個已核准 case 的 Visual Derivation 能從工作單位與重複結構推出 expression 與最終 complexity。
- `animation_design.md` 在 Scene 4 前持久化 complete fixed `Complexity Scope` block，且依序包含 `Analysis basis`、`Analysis source`、`Approved primary time case`、`Approved contrast time cases`、`Approved space treatment` 與 `Approval evidence`；contrast 為零時明確記錄 `None — zero approved contrast time cases`。
- `Analysis source` 含可定位來源，且與 derivation basis 分欄保存；六個固定欄位都不可空白。
- Scene 4 完整覆蓋 `Complexity Scope` 的 time cases 與 space treatment。
- Scene 5 只總結 Scene 4 已教內容。
- `Complexity Scope` 與 approval evidence 完整保留使用者核准範圍。

完成條件：以上每項都有可定位的證據；reviewer 已確認完整 scope block 的 topology、位置與內容，任何 blocking complexity finding 使 `Complexity Analysis` 與整體 `Verdict` 為 `FAIL`。

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

## Complexity Analysis
PASS | FAIL — 簡要說明 Analysis Basis、case labels、Visual Derivation、scope coverage 與核准範圍

## Production Readiness
PASS | FAIL — 簡要說明檢查結果

## User Decision Preservation
PASS | FAIL — 簡要說明檢查結果

## Required Repairs
沒有問題時寫 None；有問題時列出具體修正要求

## Verdict
PASS | FAIL
```

任一項失敗，整體判定就是 `FAIL`；任何 blocking complexity finding 也必須使整體 `Verdict` 為 `FAIL`。Reviewer 只報告問題，不得直接修改設計。
