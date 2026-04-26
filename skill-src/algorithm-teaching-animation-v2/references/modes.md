# Modes

本文件定義 `algorithm-teaching-animation` skill 中各種主要任務模式的教學重點、規劃重點、trace 重點與視覺重點。

主 skill 已定義以下主要模式：

- `algorithm walkthrough`
- `data structure state transition`
- `pointer and control-flow explainer`
- `graph traversal explainer`
- `dynamic programming construction`
- `comparison or intuition explainer`

本文件的目的，是幫助 agent 在不同任務下，不要用同一套教法硬套所有演算法。

## 使用方式

當使用者需求進入本 skill 時：

1. 先判斷最接近哪一種主要模式
2. 以該模式作為主要規劃方向
3. 若任務同時涉及多種模式，可保留次要模式，但只能有一個主要模式
4. `plan.md`、`teaching_script.md`、trace 與視覺設計都應圍繞主要模式展開

若模式選錯，通常整支動畫雖然正確，卻不好教。

## 1. `algorithm walkthrough`

### 適用情境

適合：

- 需要從輸入一路講到輸出的完整流程
- 使用者希望看見逐步執行過程
- 初學者導向的教學動畫

常見任務：

- Bubble Sort
- Insertion Sort
- Binary Search
- BFS / DFS 的完整遍歷過程

### 教學重點

應優先讓觀眾理解：

- 演算法每一步在做什麼
- 為什麼這一步會發生
- 整體流程如何逐步推進
- 局部操作如何累積成最終結果

### 規劃重點

`plan.md` 應特別明確：

- 主要教學目標
- 高層 beat 順序
- 哪些局部步驟值得放大
- 觀眾最容易在哪裡掉線

### Trace 重點

trace 應完整支撐：

- 結構建立
- 焦點轉移
- 關鍵比較或更新
- 進度標記
- 收束成結果的關鍵段落

### 視覺重點

應優先讓觀眾看見：

- 現在的主焦點
- 當前正在發生的局部操作
- 目前已完成到哪裡

### 常見錯誤

- 每一步都記錄，但沒有教學節奏
- 教學太像逐行 debug，而不是教學 walkthrough

## 2. `data structure state transition`

### 適用情境

適合：

- 主要重點在資料結構本身如何變化
- 演算法邏輯可視化的核心是狀態改變

常見任務：

- Heap insert / heapify
- BST insertion
- Queue / stack 狀態演化
- Linked structure 的節點變動

### 教學重點

應優先讓觀眾理解：

- 哪些結構部分發生了變化
- 哪些部分保持不變
- 每次更新對整體結構有什麼影響

### 規劃重點

`plan.md` 應特別明確：

- 核心資料結構
- 重要結構關係
- 結構中哪些位置、節點或區域值得持續追蹤

### Trace 重點

trace 應清楚表達：

- 結構建立
- 局部更新
- 值覆寫或節點移動
- 關鍵位置的狀態變更

### 視覺重點

應優先讓觀眾看見：

- 結構布局的穩定性
- 局部變化如何改變整體結構
- 哪些節點或元素是目前活動區域

### 常見錯誤

- 為了呈現變化而頻繁重排整個結構
- 結構關係變動太快，觀眾看不清

## 3. `pointer and control-flow explainer`

### 適用情境

適合：

- 演算法的理解重點在 pointer、index、boundary 或控制流程

常見任務：

- Binary Search
- Two Pointers
- Sliding Window
- Partition 類演算法
- 某些 recursion interval 解說

### 教學重點

應優先讓觀眾理解：

- pointer 為什麼移動
- 邊界如何更新
- 哪些區域仍有效、哪些已被排除
- 控制流程如何導向下一步決策

### 規劃重點

`plan.md` 應特別明確：

- 哪些 pointer 是關鍵角色
- 每個 pointer 的語義
- 哪些區間、邊界或 active range 需要持續可見

### Trace 重點

trace 應清楚支撐：

- pointer create / move / remove
- 邊界變動
- 焦點對象改變
- 當前有效範圍
- 被排除區間

### 視覺重點

應優先讓觀眾看見：

- `left` / `right` / `mid` 等角色差異
- 區間縮減或邊界推進
- pointer 的移動原因，而不只是移動結果

### 常見錯誤

- pointer 很多，但沒有角色區分
- pointer 位置有動，但觀眾不知道為什麼

## 4. `graph traversal explainer`

### 適用情境

適合：

- 主要重點是圖上的探索順序、visited 狀態與 frontier 行為

常見任務：

- BFS
- DFS
- 簡化版 shortest path explainer

### 教學重點

應優先讓觀眾理解：

- 現在正在探索哪個節點
- 哪些節點已訪問
- frontier 如何擴張或收縮
- queue / stack 如何影響遍歷順序

### 規劃重點

`plan.md` 應特別明確：

- traversal 的主要故事線
- queue / stack 是否要可視化
- visited / frontier / current node 的角色分工

### Trace 重點

trace 應清楚表達：

- 當前焦點節點
- visited 狀態切換
- frontier 進出
- 必要的 queue / stack 操作

### 視覺重點

應優先讓觀眾看見：

- current node
- visited vs unvisited
- frontier
- 探索順序

### 常見錯誤

- 只看到節點亮起來，但不知道 traversal story
- graph 太亂，節點狀態難以區分

## 5. `dynamic programming construction`

### 適用情境

適合：

- 核心教學目標是理解表格如何建立
- 重點在狀態定義、依賴關係與填表順序

常見任務：

- 0/1 Knapsack
- LCS
- Edit Distance

### 教學重點

應優先讓觀眾理解：

- 每個 cell 代表什麼
- 當前 cell 依賴哪些已知子問題
- 表格如何逐步被建立
- 為什麼填表順序合理

### 規劃重點

`plan.md` 應特別明確：

- state definition
- row / col 的意義
- 依賴方向
- 哪些 cell 需要被明確標示為來源

### Trace 重點

trace 應清楚支撐：

- create_matrix
- highlight_cell / unhighlight_cell
- set_cell
- mark_cell

必要時應能讓教學腳本對應到依賴來源區域。

### 視覺重點

應優先讓觀眾看見：

- 當前 cell
- 依賴 cell
- 已完成區域
- 填表順序

### 常見錯誤

- 只看到格子被填值，卻不知道依賴從哪裡來
- 表格狀態雖正確，但沒有顯示為什麼要這樣更新

## 6. `comparison or intuition explainer`

### 適用情境

適合：

- 使用者想理解為什麼某演算法成立
- 想比較兩種策略
- 想強調局部決策與全域結果之間的關係

常見任務：

- Bubble Sort 為什麼只靠相鄰比較也能完成排序
- 為什麼 Binary Search 可以排除半區間
- Greedy vs DP 的直觀差異

### 教學重點

應優先讓觀眾理解：

- 核心直觀
- 為什麼這套規則有效
- 局部操作與全域結果之間的連結

### 規劃重點

`plan.md` 應特別明確：

- 要強調的核心直觀是什麼
- 哪些對比最值得呈現
- 哪種誤解最需要被拆解

### Trace 重點

trace 仍然重要，但不一定需要像 walkthrough 那樣逐步完整。

這類任務可接受：

- 只選最能支持直觀的關鍵事件
- 用較少但高教學價值的 action 支撐說明

### 視覺重點

應優先讓觀眾看見：

- 關鍵對比
- 重複出現的局部規則
- 最後如何收束成整體效果

### 常見錯誤

- 只講抽象結論，沒有事件支撐
- 動畫存在，但沒有真正幫助 intuition

## 模式選擇建議

若同一任務可以落在多種模式，優先問自己：

- 這支動畫最主要是在教「完整流程」嗎？
- 還是在教「結構如何變」？
- 還是在教「pointer / boundary 如何控制流程」？
- 還是在教「表格如何建立」？
- 還是在教「為什麼這種做法有效」？

哪個答案最強，就選哪個模式當主模式。

## 多模式任務的處理原則

有些任務會同時含有多種模式，例如：

- Binary Search 既是 walkthrough，也是 pointer-heavy
- Knapsack 既是 walkthrough，也是 DP construction
- BFS 既是 walkthrough，也是 graph traversal

處理方式：

- 先選一個主模式
- 次要模式只作為輔助視角
- 不要讓每個 beat 都切換教學主軸

## 常見錯誤

### 錯誤 1：把所有演算法都當 walkthrough 講

問題：

- 對 pointer-heavy 或 DP 任務來說，會失去真正的重點

### 錯誤 2：模式選得太抽象

問題：

- `plan.md` 與 `teaching_script.md` 無法聚焦

### 錯誤 3：主模式和教學目標不一致

問題：

- 整支動畫會像是在做一件事，但嘴上說在教另一件事

## 與其他文件的關係

- `planning.md`  
  使用本文件選定主要 mode，並據此決定高層教學方向

- `teaching-script.md`  
  依 mode 決定每個 beat 的重點與講法

- `trace-schema.md`  
  依 mode 決定哪些事件最值得被記錄

- `visual-language.md`  
  依 mode 決定焦點、顏色、標記與版面優先順序

本文件的責任，是幫這個 skill 在不同類型任務中維持正確教學重心。
