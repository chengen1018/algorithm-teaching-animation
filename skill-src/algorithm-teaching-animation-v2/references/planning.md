# Planning

本文件定義 `algorithm-teaching-animation` skill 中 `plan.md` 的角色、格式與撰寫原則。

`plan.md` 是整個工作流的起點。  
它的工作不是寫程式、不是描述動畫語法，也不是逐拍講稿，而是先決定這支動畫究竟要教什麼、要怎麼教、應該強調哪些結構與不變量。

你可以把它理解成：

- `plan.md` 決定整體教學方向
- `teaching_script.md` 決定逐拍教學節奏
- `generated_trace_script.py` 決定如何把演算法執行轉成 trace
- `generated_algo_scene.py` 決定如何把 trace 呈現成可讀動畫

若 `plan.md` 沒有寫清楚，後面各層通常都會開始漂移。

## 核心目的

`plan.md` 的主要目的包括：

- 定義本次動畫的主要教學目標
- 決定觀眾程度與說明深度
- 選定主要任務模式
- 指出核心資料結構與關鍵狀態
- 找出應被強調的不變量
- 決定教學 beat 的高層順序
- 預先辨識常見誤解與難點
- 為後續 `teaching_script.md`、trace 與 Manim translation 提供共同方向

簡單說，`plan.md` 回答的是：

- 這支動畫想讓觀眾學會什麼？
- 為什麼要這樣切教學節奏？
- 什麼是這支動畫不能講錯、不能漏掉的？

## 核心原則

撰寫 `plan.md` 時，應遵守以下原則：

- 先定義教學目標，再考慮畫面  
  不要一開始就想用什麼 Manim 元件，而應先決定觀眾要理解什麼。

- 一支動畫只應有一個主要教學主軸  
  可以有次要目標，但不要讓主軸模糊。

- 優先決定觀念，而不是細節  
  `plan.md` 應先決定不變量、重點操作、易錯點，而不是旁白逐字稿。

- 讓後續各層有可依循的方向  
  `teaching_script.md`、trace 與 Manim translation 都應能從 `plan.md` 找到依據。

- 只保留必要決策  
  `plan.md` 應聚焦高層教學決策，不要塞入過多實作細節。

## `plan.md` 應包含什麼

一份完整的 `plan.md` 至少應包含以下項目：

- Algorithm / topic
- Audience
- Primary teaching goal
- Primary mode
- Core data structures
- Key states, pointers, or boundaries
- Key invariant(s)
- Common confusion points
- High-level beat outline
- Visual priorities

## 建議格式

建議使用固定的 Markdown 結構，讓後續 agent 能穩定讀取。

推薦格式如下：

```md
# Plan

## Overview
- Algorithm / topic:
- Audience:
- Primary teaching goal:
- Primary mode:

## Core Structures
- Core data structure(s):
- Key state variables / pointers:
- Important boundaries or regions:

## Key Teaching Points
- Key invariant(s):
- Common confusion points:
- Local-to-global story:

## Beat Outline
1. ...
2. ...
3. ...

## Visual Priorities
- Stable semantic roles:
- Required highlights:
- Progress markers:
- Things to avoid:
```

此格式不是唯一合法格式，但若沒有特殊需求，建議維持一致。

## 必填欄位說明

### 1. Algorithm / topic

用途：  
說明本次動畫在講哪個演算法、問題或狀態轉移主題。

例如：

- Bubble Sort
- Binary Search
- BFS Traversal
- 0/1 Knapsack DP Table Construction
- BST Insertion

### 2. Audience

用途：  
定義預期觀眾程度，讓後續解釋深度一致。

常見寫法：

- 初學者
- 已學過基本資料結構的學生
- 需要直觀理解但不追求形式證明的觀眾
- 已理解演算法概念，現在需要視覺化輔助

若未提供明確 audience，預設應採取：

- 可讀、直觀、偏教學導向
- 避免不必要的形式化證明

### 3. Primary teaching goal

用途：  
定義這支動畫最重要的教學目標。

好例子：

- 讓觀眾理解相鄰比較如何逐步把較大元素推向右側
- 讓觀眾理解二元搜尋透過區間縮減排除不可能解
- 讓觀眾理解 DP 表格的值如何依賴較小子問題

不好的例子：

- 介紹這個演算法
- 做一支動畫

### 4. Primary mode

用途：  
從 skill 主檔定義的模式中，選定一個主要模式。

常見模式：

- `algorithm walkthrough`
- `data structure state transition`
- `pointer and control-flow explainer`
- `graph traversal explainer`
- `dynamic programming construction`
- `comparison or intuition explainer`

若任務同時符合多種模式，也應明確指定主要模式，避免後續腳本發散。

### 5. Core data structures

用途：  
指出本次動畫的主要資料結構。

例如：

- 一個主陣列
- 一個 DP 矩陣
- 一棵 BST
- 一張 graph 與一個 queue

原則：

- 只列出真正影響教學的結構
- 不要把所有暫時變數都列進來

### 6. Key states, pointers, or boundaries

用途：  
指出後續應被穩定呈現的重要動態元素。

例如：

- `i`、`j`
- `left`、`right`、`mid`
- frontier / visited
- 當前 row / col
- partition boundary

這一欄的目的是幫後續教學腳本與視覺層決定哪些角色必須持續可見。

### 7. Key invariant(s)

用途：  
定義這支動畫應反覆強化的不變量或穩定規則。

例如：

- 每完成一輪，最右邊的一個元素就固定
- `[left, right]` 區間永遠包含所有仍可能的答案
- 已填寫完成的 DP cell 可以作為後續狀態的依賴

若沒有明確不變量，也可改寫為：

- 本次動畫最需要觀眾持續記住的穩定規則

### 8. Common confusion points

用途：  
提前列出觀眾最容易搞混的地方。

例如：

- 為什麼 bubble sort 每次只比較相鄰元素
- 為什麼 binary search 可以一次排除半個區間
- 為什麼 DP 不是暴力重算，而是重用已知結果

這一欄很重要，因為它直接影響 `teaching_script.md` 的重點安排。

### 9. High-level beat outline

用途：  
先定義高層 beat 順序，之後再由 `teaching_script.md` 展開成逐拍腳本。

例子：

1. 建立初始資料結構與問題情境
2. 顯示第一個關鍵操作
3. 顯示局部操作如何影響狀態
4. 強調一輪或一個子問題完成後的進度
5. 收束成最終結果

原則：

- 這一層不需要逐字旁白
- 這一層只需要決定高層節奏

### 10. Visual priorities

用途：  
定義後續視覺呈現應優先維持的語義。

例如：

- 目前比較中的元素要有穩定 highlight
- 已完成位置應有固定完成色
- pointer 必須易於追蹤
- 不要同時出現太多競爭焦點
- 陣列位置應盡量穩定，不要頻繁重排

這一欄能幫助後續動畫不偏離教學需求。

## 規劃時應回答的問題

在撰寫 `plan.md` 時，至少回答以下問題：

- 觀眾看完後最應該理解哪一件事？
- 哪些狀態變化最值得被視覺化？
- 哪些局部操作最需要被放大呈現？
- 哪些 pointer、邊界或活動區間需要持續可見？
- 哪個不變量是理解核心？
- 哪些地方最容易讓觀眾誤解？
- 這個演算法的局部決策如何累積成最終結果？

如果這些問題答不清楚，後面通常不應急著寫 script 或 trace。

## 與 `teaching_script.md` 的關係

`plan.md` 是高層規劃，`teaching_script.md` 是逐拍執行。

可以理解成：

- `plan.md` 決定「要教什麼」
- `teaching_script.md` 決定「逐拍怎麼教」

因此：

- `teaching_script.md` 不應偏離 `plan.md` 的主要教學目標
- 若 script 寫著寫著發現主要目標改變了，應回頭修 `plan.md`

## 與 `action_trace.json` 的關係

`plan.md` 不直接定義 trace action，但它應影響 trace 的設計方向。

例如：

- 若計畫中強調 pointer movement，就應期待 trace 包含對應 pointer actions
- 若計畫中強調 invariant 的建立與確認，就應期待 trace 能支撐這些關鍵事件

`plan.md` 不等於 `action_trace.json`，但 trace 不應偏離 plan 的教學重點。

## 與 `generated_algo_scene.py` 的關係

`generated_algo_scene.py` 不應只忠於 trace，也應忠於 `plan.md` 所定義的教學目標與視覺優先順序。

具體來說：

- trace 決定事件事實
- `plan.md` 決定教學重點與視覺優先順序

若只看 trace 而忽略 plan，動畫可能會正確但不好教。

## 常見錯誤

### 錯誤 1：把 plan 寫成高層版程式碼註解

錯誤寫法：

- 先建立 array，然後 highlight，然後 swap

問題：

- 這不是 planning，這是在提前寫 trace

正確方向：

- 回到教學目標、不變量、beat 順序與易錯點

### 錯誤 2：目標太寬

錯誤寫法：

- 介紹 bubble sort 的所有重點，包括原理、實作、優化、複雜度、變形版本

問題：

- 單支教學動畫通常承載不了這麼多主軸

正確方向：

- 收斂成一個主要教學主軸

### 錯誤 3：沒有寫不變量

問題：

- 動畫會只剩事件流，而缺乏貫穿的理解線索

正確方向：

- 至少指出一個本次動畫應持續強化的穩定規則

### 錯誤 4：沒有寫觀眾程度

問題：

- 後續 script 可能會忽淺忽深，語氣不一致

正確方向：

- 即使沒有明確 audience，也應先做一個合理假設

## 撰寫流程建議

建議依以下順序撰寫 `plan.md`：

1. 先確認演算法與輸入任務
2. 決定 audience
3. 寫出 primary teaching goal
4. 選定主要 mode
5. 列出核心資料結構與關鍵 pointer / boundary
6. 找出一到兩個最重要的不變量
7. 列出常見 confusion points
8. 排出高層 beat outline
9. 補上 visual priorities

## 最小範例

以下是一個簡化的 bubble sort `plan.md` 片段：

```md
# Plan

## Overview
- Algorithm / topic: Bubble Sort
- Audience: 初學者
- Primary teaching goal: 理解相鄰比較如何逐步把較大元素推向右側
- Primary mode: algorithm walkthrough

## Core Structures
- Core data structure(s): 一個主陣列
- Key state variables / pointers: `j`
- Important boundaries or regions: 本輪未固定區間

## Key Teaching Points
- Key invariant(s): 每完成一輪，最右側一個元素會固定
- Common confusion points: 為什麼只比較相鄰元素也能完成排序
- Local-to-global story: 每次局部交換只修正一對元素，但多次局部修正會把較大值逐步推到正確位置

## Beat Outline
1. 建立初始陣列與排序目標
2. 顯示相鄰比較
3. 顯示必要時的交換
4. 標記本輪固定位置
5. 重複直到整體完成排序

## Visual Priorities
- Stable semantic roles: 比較中元素、已固定元素、活動 pointer
- Required highlights: 當前比較對
- Progress markers: 每輪結束時的固定位置
- Things to avoid: 同時 highlight 過多元素、頻繁重排整個陣列
```

## 與其他文件的關係

- `plan.md`  
  定義高層教學方向

- `teaching_script.md`  
  將高層規劃展開為逐拍教學內容

- `action_trace.json`  
  將演算法執行轉成事件事實

- `generated_algo_scene.py`  
  在忠於 trace 的前提下，依照 plan 的教學優先順序做呈現

`plan.md` 的責任，是先把這支動畫「教什麼、怎麼切重點」定下來。
