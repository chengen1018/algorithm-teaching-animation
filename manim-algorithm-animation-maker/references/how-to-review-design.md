# 動畫設計內容審查

Reviewer 只檢查動畫設計的內容品質，不重新設計動畫。

## 檢查項目

### Algorithm Correctness

確認演算法步驟、狀態更新、範例輸入與最終結果正確。

### Teaching Coherence

確認六個 Scene 依序完成問題與目標、核心觀念、重要資料與狀態、一次關鍵動作、完整演示，以及結果回顧。不得有尚未介紹的重要概念或無法解釋的跳躍。

### Visual and Explanation Consistency

確認畫面、解說重點與動畫動作表達同一件事；原因、動作及結果都可見；相同視覺線索前後含義一致。

### Production Readiness

確認每個 Scene 都有教學目的、解說重點、畫面內容與具體動畫順序，且後續腳本與 Manim 實作者不需要猜測教學結構或動畫演法。

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
