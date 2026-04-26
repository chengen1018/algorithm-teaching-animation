# Teaching Script

## Summary
- Algorithm: 0/1 Knapsack DP Table Construction
- Audience: 初學者
- Primary teaching goal: 理解 DP cell 如何在「不選」與「選」兩種候選之間取較佳值
- Primary mode: dynamic programming construction
- Key invariant(s): 已完成的 cell 代表已知子問題結果，可被後續 cell 安全依賴；每個新 cell 都是合法候選中的最佳值

## Beats

### Beat 1: 建立 DP 表格
- Visual focus: 整個矩陣
- Trace mapping: `action 1`
- What happens: 顯示初始化的 DP 表格。
- What the viewer should learn: DP 不是直接算答案，而是先建立一個用來儲存子問題結果的表格。
- Teaching narration: 我們先建立一張表格。DP 的核心，就是把較小子問題的答案先存起來，之後再重用。
- Invariant or progress cue: 初始表格代表尚未處理的狀態。

### Beat 2: 聚焦第一個需要做選擇的 cell
- Visual focus: 當前 cell
- Trace mapping: `actions 2-6`
- What happens: 高亮當前 cell，同時標出「不選」與「選」兩個候選依賴來源，再寫入較佳結果。
- What the viewer should learn: Knapsack 的每個新 cell 都是在兩個合法候選中做最佳選擇。
- Teaching narration: 現在這個格子不是直接抄前一格，而是要比較兩種可能：不選當前物品，或選它之後加上剩餘容量的最佳值。
- Invariant or progress cue: 已完成區域可以作為依賴基礎。

### Beat 3: 計算下一個 cell
- Visual focus: 下一個 cell 與其依賴來源
- Trace mapping: `actions 7-11`
- What happens: 焦點轉到下一格，再次展示兩種候選來源並寫入結果。
- What the viewer should learn: DP 的填表順序保證目前 cell 需要的候選依賴永遠已經可用。
- Teaching narration: 當我們往下一格推進時，前面已算好的結果就成了現成候選，因此可以在固定規則下繼續比較並寫入新值。
- Invariant or progress cue: 已完成區域持續擴大。

### Beat 4: 完成最後答案 cell
- Visual focus: 最終答案 cell
- Trace mapping: `actions 12-16`
- What happens: 最右下角答案 cell 被計算並標記。
- What the viewer should learn: 最終答案來自每個 cell 持續在兩種候選中取最佳值的累積。
- Teaching narration: 當最後這個格子完成時，代表所有必要子問題都已經被比較過，而最後答案正是這些局部最佳選擇累積出的結果。
- Invariant or progress cue: 整張表的計算收束到最終解。
