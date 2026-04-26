# Teaching Script

## Summary
- Algorithm: Bubble Sort
- Audience: 初學者
- Primary teaching goal: 理解相鄰比較如何逐步把較大的值推向右側
- Primary mode: algorithm walkthrough
- Key invariant(s): 每完成一輪，最右側的一個元素會固定

## Beats

### Beat 1: 建立初始陣列
- Visual focus: 整個陣列
- Trace mapping: `actions 1`
- What happens: 顯示輸入陣列的初始順序。
- What the viewer should learn: 排序從一個尚未整理的序列開始，後續每一步都只會在這個序列上做局部修正。
- Teaching narration: 我們先從原始陣列開始。Bubble Sort 不會一次看完整列，而是透過一連串局部比較，慢慢把元素推到正確位置。
- Invariant or progress cue: 目前尚未有任何位置固定。

### Beat 2: 開始第一組相鄰比較
- Visual focus: 指標 `j` 與索引 `0, 1` 的元素
- Trace mapping: `actions 2-3`
- What happens: 指標移到起始位置，並高亮目前要比較的兩個相鄰元素。
- What the viewer should learn: Bubble Sort 每次只比較相鄰的一對元素。
- Teaching narration: 現在焦點落在相鄰的兩個元素上。這個演算法每次只處理一對鄰居，先確認它們的順序是否正確。
- Invariant or progress cue: 本輪比較從左往右推進。

### Beat 3: 交換順序錯誤的相鄰元素
- Visual focus: 被交換的兩個元素
- Trace mapping: `actions 4-5`
- What happens: 若左邊元素比右邊大，就交換兩者。
- What the viewer should learn: 一次交換只修正局部順序，但也會把較大的值往右推進一格。
- Teaching narration: 左邊比右邊大，所以這對相鄰元素順序錯了。我們交換它們，讓較大的值向右移動一步。
- Invariant or progress cue: 較大的元素正在逐步往本輪末端移動。

### Beat 4: 持續掃描本輪剩餘位置
- Visual focus: `j` pointer 的推進與新的比較對
- Trace mapping: `actions 6-14`
- What happens: 指標往右移動，依序比較下一組相鄰元素；必要時繼續交換。
- What the viewer should learn: 一輪掃描會持續把目前遇到的較大值往右推。
- Teaching narration: 指標繼續往右移動，重複同樣的規則。每一次局部比較，都可能把較大的值再往右推一步。
- Invariant or progress cue: 本輪尚未固定區域持續縮小。

### Beat 5: 標記本輪已固定的位置
- Visual focus: 最右側元素
- Trace mapping: `action 15`
- What happens: 第一輪結束時，最右側元素被標記為固定。
- What the viewer should learn: 一輪完整掃描後，最大值一定到達最右側，因此該位置不必再比較。
- Teaching narration: 第一輪結束後，最大的值已經被推到最右邊，所以這個位置可以視為已固定。
- Invariant or progress cue: 每完成一輪，最右側新增一個固定位置。

### Beat 6: 重複後續輪次直到整體排序完成
- Visual focus: 比較對、pointer 與逐步擴大的固定區域
- Trace mapping: `actions 16-40`
- What happens: 後續輪次重複相同流程，但每輪的比較範圍都會縮小。
- What the viewer should learn: Bubble Sort 並不是每輪都做一樣多的事，因為右側固定區域會逐步擴大。
- Teaching narration: 後面的每一輪都遵守同樣規則，但因為右邊已有固定元素，所以比較範圍會慢慢縮小。
- Invariant or progress cue: 已固定區域從右往左擴大。

### Beat 7: 顯示排序完成
- Visual focus: 整個陣列
- Trace mapping: `action 41`
- What happens: 全部元素被標記為已完成。
- What the viewer should learn: 一連串局部比較與交換，最終會收斂成全域排序。
- Teaching narration: 當所有輪次完成後，整個陣列就排序好了。這也說明了局部修正如何一步步累積成完整結果。
- Invariant or progress cue: 所有位置都已固定。
