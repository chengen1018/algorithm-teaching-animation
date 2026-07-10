# 動畫設計：Graph Traversal

在套用 `references/how-to-design-animation.md` 後，對 graph traversal 動畫使用這份參考。它規範 traversal 專有的狀態與支援結構，但不會取代通用流程或 `animation_design.md` 契約。

## 必要設計決策

### queue 或 stack visibility

當 queue 或 stack 的順序會決定未來 traversal 行為時，設計必須顯示它。要顯示 active 端點、保留項目順序，並讓每次 enqueue、dequeue、push 或 pop 與造成它的 graph 事件同步。

### visited timing

設計必須精確定義節點何時變成 visited，例如在 discovery 時，或在取出進行 processing 時。視覺狀態變化必須發生在那個精確時刻，因為不同時機會改變 duplicate frontier entries 是否可能出現。

### discovery 與 processing

設計必須為 discovered 與 processed 狀態賦予不同且持續的含義。要顯示兩者之間的轉換，並讓它與 support structure 連動，避免觀眾誤以為找到一個節點就表示它所有鄰居都已處理完。

### frontier 或 path emphasis

設計必須選定主要教學對象是 frontier、traversal tree，還是 current path。強調方式必須符合演算法與學習目標：breadth-first 行為需要 frontier 順序，而 depth-first 推理則可能需要 stack 或 path 的連續性。

### BFS layer expansion

對 BFS，設計必須決定 layer expansion 是否屬於教學目標。若是，則 current layer 與 next layer 必須有明顯區別，同時 layer membership 仍須與 discovered / processed 狀態分開；一個節點可以在進入 next layer 時就被 discovered，但尚未 processed。若 layer expansion 不是教學目標，就不要加入會與 queue 競爭注意力，或暗示額外演算法狀態的 layer styling。

### sample topology 與 traversal setup

在 traversal 開始前，設計必須明確 graph 的 directedness、起始節點與相關 topology。Sample 只需暴露與教學目標有關的結構：例如 frontier growth 所需的 branching、用於 revisitation 的 cycles 或 cross-edges、會讓 visited timing 變重要的 duplicate-discovery 壓力，或決定 sequencing 的 neighbor-order 影響。不要要求每個 sample 一定包含所有這些結構。

### neighbor order

設計必須說明 neighbor visitation order，並在它影響 queue、stack 或 path 之前，就讓這個順序可見。若有多種順序都合法，則應將選定順序標示為 deterministic teaching choice，而非演算法保證。

### stable graph layout

設計必須在 traversal 開始前固定 node positions，並保持穩定。應透過 highlights、edges 與 support-structure updates 顯示狀態變化；空間移動不應讓人誤以為 graph topology 本身在改變。

## 教學風險

### 混淆 discovered 與 processed 狀態

當這個區分會影響理解時，不可用同一個視覺狀態表示兩者。觀眾必須能在暫停時判斷某節點只是已排入處理，還是已經檢查過其鄰居。

### 引入後又移動 graph nodes

不要為了後面方便而重新排 nodes。節點移動會迫使觀眾重建 graph 的空間地圖，且可能錯誤暗示 adjacency 改變；擁擠問題應在 traversal 開始前解決。

### 隱藏教學關鍵的支援結構

若 queue、stack 或等價的 frontier 表示法能解釋 traversal order，就不要省略它。若空間不足，應先減少裝飾性的 graph 細節，而不是隱藏那個決定下一個節點選擇的結構。
