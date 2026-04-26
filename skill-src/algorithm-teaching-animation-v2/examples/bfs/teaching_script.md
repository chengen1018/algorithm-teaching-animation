# Teaching Script

## Summary
- Algorithm: BFS
- Audience: 初學者
- Primary teaching goal: 理解 BFS 如何按層擴張 frontier
- Primary mode: graph traversal explainer
- Key invariant(s): visited 集合只增不減；queue 中保留下一批待探索節點

## Beats

### Beat 1: 建立 graph 與起點
- Visual focus: 整張 graph 與起點 `A`
- Trace mapping: `actions 1-2`
- What happens: 顯示 graph，並先聚焦起點節點。
- What the viewer should learn: BFS 會從單一起點開始，逐步向外擴張。
- Teaching narration: 我們從起點 `A` 開始。BFS 的核心不是一路走到底，而是從起點往外一層一層展開。
- Invariant or progress cue: 起點是第一層 frontier。

### Beat 2: 標記起點已訪問
- Visual focus: 起點 `A`
- Trace mapping: `action 3`
- What happens: 起點被標記為已訪問。
- What the viewer should learn: 一旦節點進入 visited，就不會再被重複處理。
- Teaching narration: 起點一旦加入 visited，就表示它已被納入搜尋，不需要再次加入 queue。
- Invariant or progress cue: visited 集合開始建立。

### Beat 3: 展開第一層鄰居
- Visual focus: 當前節點 `A` 與其鄰居 `B`、`C`
- Trace mapping: `actions 4-7`
- What happens: 目前從 `A` 展開，將它的鄰居加入下一層 frontier。
- What the viewer should learn: BFS 會先把當前層可達的鄰居全部找出來。
- Teaching narration: 從 `A` 出發後，我們先看它直接連到哪些節點。這些節點會成為下一層要處理的 frontier。
- Invariant or progress cue: frontier 從起點向外擴張一層。

### Beat 4: 轉移到下一個待探索節點
- Visual focus: 當前節點從 `A` 轉到 `B`
- Trace mapping: `actions 8-10`
- What happens: 焦點移到 `B`，並將其標記為已訪問。
- What the viewer should learn: BFS 依照 queue 順序處理 frontier，而不是任意跳躍。
- Teaching narration: 現在輪到 `B`。這說明 BFS 會按照先進先出的順序，依序處理上一層找到的節點。
- Invariant or progress cue: frontier 依序被消化。

### Beat 5: 從下一層繼續擴張
- Visual focus: `B` 的新鄰居 `D`、`E`
- Trace mapping: `actions 11-16`
- What happens: 從 `B` 找到新的未訪問鄰居並加入 frontier。
- What the viewer should learn: 每次處理一個節點，都可能把 frontier 往外再擴一層。
- Teaching narration: 當我們處理 `B` 時，會把它尚未訪問的鄰居加入下一批待探索節點，於是搜尋範圍繼續往外擴張。
- Invariant or progress cue: visited 持續擴大，且不會回頭重複處理。

### Beat 6: 完成整體遍歷
- Visual focus: 所有已訪問節點
- Trace mapping: `actions 17-24`
- What happens: 餘下節點依序完成訪問，最終整張 graph 的可達節點都被標記。
- What the viewer should learn: BFS 的全域結果來自一連串局部的 queue 展開。
- Teaching narration: 最後，當 queue 清空時，代表所有可達節點都已按層探索完成。這就是 BFS 的完整遍歷結果。
- Invariant or progress cue: frontier 歸零，visited 覆蓋所有可達節點。
