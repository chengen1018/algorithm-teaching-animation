# Teaching Script

## Summary
- Algorithm: Binary Search
- Audience: 初學者
- Primary teaching goal: 理解 `left`、`right`、`mid` 如何控制搜尋區間
- Primary mode: pointer and control-flow explainer
- Key invariant(s): 只要目標值存在，它一定位於當前的 `[left, right]` 區間中

## Beats

### Beat 1: 建立已排序陣列與搜尋目標
- Visual focus: 整個已排序陣列
- Trace mapping: `actions 1-4`
- What happens: 顯示已排序陣列，並建立 `left`、`right` 與 `mid` 三個 pointer。
- What the viewer should learn: 二元搜尋只能用在已排序資料上，而且它一開始就會維護一個明確的搜尋區間。
- Teaching narration: 我們從一個已排序陣列開始。二元搜尋不是逐個檢查，而是維持一個目前仍可能包含答案的區間。
- Invariant or progress cue: 初始有效區間為整個陣列。

### Beat 2: 聚焦目前的中間位置
- Visual focus: `mid` pointer 與索引 `mid`
- Trace mapping: `actions 5-6`
- What happens: 畫面高亮目前的中間元素，作為本輪比較的焦點。
- What the viewer should learn: 每一輪都只拿目標值跟中間位置比較。
- Teaching narration: 這一步我們只看中間位置，因為它能幫我們一次排除半個區間。
- Invariant or progress cue: 決策點永遠從目前區間的中點開始。

### Beat 3: 比較後排除左半邊
- Visual focus: 第一輪的 `mid` 與被排除的左半區
- Trace mapping: `actions 7-12`
- What happens: 目標值大於 `mid` 的值，因此左半邊與 `mid` 本身被排除，`left` 右移。
- What the viewer should learn: 若目標值比中間值大，就不可能在左半邊。
- Teaching narration: 目標值比中間值更大，所以左邊這一半都不可能是答案。我們可以直接把搜尋範圍縮到右半邊。
- Invariant or progress cue: 更新後的 `[left, right]` 仍然包含所有可能答案位置。

### Beat 4: 在縮小後的區間重新選擇中點
- Visual focus: 新的 `left`、`right` 與新的 `mid`
- Trace mapping: `actions 13-16`
- What happens: 在較小的有效區間內重新計算並標示新的中間位置。
- What the viewer should learn: 二元搜尋不是固定看原陣列中點，而是每次看「目前有效區間」的中點。
- Teaching narration: 區間縮小之後，我們重新取這個新區間的中點，而不是回頭看原本的位置。
- Invariant or progress cue: 比較點會跟著有效區間一起更新。

### Beat 5: 比較後排除另一部分區間
- Visual focus: 第二輪的 `mid` 與被排除區域
- Trace mapping: `actions 17-22`
- What happens: 再次比較後，更新邊界並排除另一部分不可能區域。
- What the viewer should learn: 每次比較都會大幅縮小搜尋空間。
- Teaching narration: 這一輪也一樣，根據目標值和中間值的大小關係，我們再排除一批不可能的位置。
- Invariant or progress cue: 有效區間持續縮小。

### Beat 6: 找到答案位置
- Visual focus: 最終 `mid` 與被標記為答案的元素
- Trace mapping: `actions 23-27`
- What happens: 目標值等於目前中間值，該位置被標記為找到答案。
- What the viewer should learn: 當目標值等於 `mid` 的值時，就能直接停止搜尋。
- Teaching narration: 當中間值正好等於目標值時，我們就找到了答案，不需要再繼續縮小區間。
- Invariant or progress cue: 搜尋在有效區間收斂到答案時結束。
