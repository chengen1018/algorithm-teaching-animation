# Teaching Script

本文件定義 `algorithm-teaching-animation` skill 中 `teaching_script.md` 的角色、格式與撰寫原則。

`teaching_script.md` 是教學層文件。  
它的工作不是重新實作演算法，也不是直接描述 Manim 動畫語法，而是把整支動畫拆成一系列可教、可看、可對齊 trace 的教學 beat。

你可以把它理解成：

- `plan.md` 決定「整支動畫要教什麼」
- `teaching_script.md` 決定「每一拍要怎麼教」
- `action_trace.json` 決定「實際發生了哪些演算法事件」
- `generated_algo_scene.py` 決定「這些事件如何被呈現」

## 核心目的

`teaching_script.md` 的存在，是為了避免動畫只有動作，卻沒有教學節奏。

完整 workflow 預設會產出旁白音訊，`teaching_script.md` 也負責提供 `voiceover.md` 收斂前的教學來源。若使用者明確要求字幕，它也可作為 `subtitle_script.md` 的來源。

它的主要目的包括：

- 把 `plan.md` 中的教學目標拆成逐步 beat
- 定義每一拍的畫面焦點
- 指出觀眾在該拍應該理解的重點
- 說明這一拍要修正哪種常見誤解
- 讓 beat 可以對齊到 `action_trace.json`
- 讓 Manim translation 在不違反 trace 的前提下，仍能有清楚的教學呈現
- 讓 `voiceover.md` 能從每個 beat 收斂出自然英文旁白
- 若使用者要求字幕，讓 `subtitle_script.md` 能從每個 beat 收斂出短字幕

## 核心原則

撰寫 `teaching_script.md` 時，應遵守以下原則：

- 教學優先於描述  
  不要只重複畫面上看得到的東西，要指出這一步為什麼重要。

- 一個 beat，一個重點  
  每個 beat 最好只承載一個主要觀念、操作或觀察。

- 先講狀態，再講規則  
  先幫觀眾看到資料結構發生什麼變化，再總結規則或意義。

- 與 trace 對齊  
  每個 beat 都必須能對應到一段 trace 區間或一組 action。

- 與 audience 對齊  
  解釋深度與語氣應符合 `plan.md` 中設定的觀眾程度。

- 不代替 trace  
  教學腳本可以說明意義，但不能自行發明演算法事件。

- 要能收斂成旁白  
  每個 beat 的教學說明都應能被改寫成 1 到 3 句自然口說旁白；若完全無法收斂，通常代表 beat 太滿或說明太散。

## `teaching_script.md` 應包含什麼

一份完整的 `teaching_script.md` 至少應包含：

- 本次動畫的簡短教學目標摘要
- 教學模式或任務類型
- beat list
- 每個 beat 的教學欄位
- 必要時補充全局提醒，例如整支動畫要持續強調的不變量

## 建議格式

建議使用固定的 Markdown 結構，方便人與 agent 一起閱讀。

推薦格式如下：

```md
# Teaching Script

## Summary
- Algorithm:
- Audience:
- Primary teaching goal:
- Primary mode:
- Key invariant(s):

## Beats

### Beat 1: ...
- Visual focus:
- Trace mapping:
- What happens:
- What the viewer should learn:
- Teaching narration:
- Invariant or progress cue:

### Beat 2: ...
- Visual focus:
- Trace mapping:
- What happens:
- What the viewer should learn:
- Teaching narration:
- Invariant or progress cue:
```

這個格式不是唯一合法格式，但若未來沒有特殊需求，建議盡量維持一致。

## 每個 beat 的必要欄位

每個 beat 至少應包含以下資訊。

### 1. Beat title

用途：  
用一句短標題描述這一拍的教學任務。

好例子：

- 比較目前相鄰的兩個元素
- 將較大的值往右推進
- 確認本輪最後一個固定位置
- 計算目前 DP cell 的最佳值

不好的例子：

- Step 7
- 繼續
- 動畫開始

### 2. Visual focus

用途：  
指出這一拍觀眾應先看哪裡。

應明確回答：

- 哪個資料結構是主體
- 哪些元素是焦點
- 哪個 pointer 或區間正在移動

好例子：

- 陣列中索引 `j` 和 `j+1` 的兩個元素
- 二元搜尋目前的 `[left, right]` 區間與 `mid`
- DP 表格中目前正在填寫的 cell 與其依賴格

### 3. Trace mapping

用途：  
將 beat 與 `action_trace.json` 對齊。

可接受的寫法包括：

- 對應單一 action
- 對應一段 action 區間
- 對應一組具名 action

例如：

- `actions 3-5`
- `highlight -> swap -> unhighlight`
- `create_pointer("p_mid") + highlight([mid])`

原則：

- 每個 beat 都必須能回溯到一段 trace
- 重要 trace 區段也應能回溯到某個 beat

### 4. What happens

用途：  
用一到兩句話說明這一拍實際發生的演算法事件。

這裡描述的是事件，不是教學結論。

例如：

- 目前比較相鄰兩個元素，若順序錯誤就交換
- `mid` 指到中間位置後，目標值小於目前值，因此右邊界左移
- 目前 cell 根據上方與左方依賴值計算新結果

### 5. What the viewer should learn

用途：  
指出這一拍的教學目標，也就是觀眾應該理解什麼。

例如：

- 泡沫排序每次比較只會處理局部順序
- 二元搜尋不是逐一檢查，而是透過區間縮減排除不可能的部分
- DP 表格中的每個值都依賴更小子問題的結果

### 6. Teaching narration

用途：  
提供簡短教學說明。這是 `voiceover.md` 的主要來源，但仍可比最終口說旁白更完整；它不是公式推導稿。

它應該回答：

- 現在正在做什麼
- 為什麼這一步重要
- 這一步如何推進整體解題過程

好例子：

- 我們先看這兩個相鄰元素。若左邊比右邊大，就交換它們，讓較大的值逐步往右移動。
- 現在中間位置已經確定不是答案，因此我們可以直接排除一半區間。
- 這個格子的值不是憑空決定的，而是建立在前面已算好的子問題上。

不好的例子：

- 這裡很酷地做了一個交換。
- 接下來動畫會把它移過去。
- 現在我們進入下一步。

補充原則：

- `Teaching narration` 可以比最終 voiceover 完整
- 但它應該能被後續收斂成 `voiceover.md`
- 若一段 narration 長到無法改寫成自然口說旁白，通常應先拆 beat 或重寫說明

### 7. Invariant or progress cue

用途：  
指出這一拍正在強化哪個不變量、進度概念或全局結構。

例如：

- 最右邊的位置在本輪結束後已固定
- `[left, right]` 區間始終包含所有仍可能是答案的位置
- 已填完的 DP cell 可以安全地被後續 cell 依賴

如果沒有明確不變量，也可以寫目前進度標記，例如：

- 已完成第 1 輪比較
- 已確定根到插入點的搜尋路徑

## 教學內容應聚焦什麼

`teaching_script.md` 應優先關注以下面向：

- 狀態變化
- 資料結構操作
- 控制流程
- 不變量
- 指標移動
- 局部決策如何累積成全域結果

這是此 skill 的主要教學取向。

## 教學旁白應怎麼寫

此 skill 中的旁白定位是「教學旁白」，不是「公式推導旁白」。

預設應以以下類型的說明為主：

- 操作說明：這一步做了什麼
- 理由說明：為什麼要這樣做
- 進度說明：目前完成到哪裡
- 結構說明：資料結構如何改變
- 規則說明：這個局部操作遵守什麼規則
- 結果說明：這一步如何幫助得到最終答案

除非演算法本身真的需要，否則不要把旁白預設寫成：

- 高度形式化的證明
- 純公式推導
- 與畫面脫節的抽象敘述

## 與 `plan.md` 的關係

`plan.md` 比 `teaching_script.md` 更高層。

可以理解成：

- `plan.md` 負責決定「教學方向」
- `teaching_script.md` 負責決定「逐拍執行方式」

若兩者衝突，應優先回頭修正 `plan.md`，不要讓 `teaching_script.md` 私自偏離整體教學目標。

## 與 `action_trace.json` 的關係

`teaching_script.md` 不等於 trace，但必須與 trace 對齊。

原則如下：

- 每個 beat 都必須對應到一段 trace 區間或一組 action
- 一個 beat 可以對應多個 action
- 重要 trace 段落不應沒有對應的教學目的
- 若 `teaching_script.md` 的教學重點在 trace 中完全無法表達，應優先檢查：
  - 是否需要修改 beat 設計
  - 是否需要擴充 trace schema

不要在 Manim 層硬補一個 trace 中不存在的重要教學事件。

## 與 `voiceover.md` 的關係

`teaching_script.md` 不等於旁白稿，但它應該是 `voiceover.md` 的主要來源。

建議理解為：

- `teaching_script.md`：較完整的教學說明
- `voiceover.md`：對應 beat 的英文口說旁白

因此：

- 若旁白重點不對，先檢查 `teaching_script.md`
- 若旁白只是太長、太繞或不適合口說，再檢查 `voiceover.md`

## 與 `subtitle_script.md` 的關係

`subtitle_script.md` 是選配產物，只有在使用者明確要求畫面字幕時才產出。若需要字幕，它也應由 `teaching_script.md` 收斂而來，但不得取代預設的 voiceover 音訊 workflow。

## 常見錯誤

### 錯誤 1：把 teaching script 寫成畫面描述稿

錯誤寫法：

- 兩個方塊變黃
- 三角形移到右邊
- 接著有一個交換動畫

問題：

- 這只是在描述畫面，不是在教學

正確方向：

- 說明這些變化代表哪個演算法事件，觀眾應理解什麼

### 錯誤 2：把 teaching script 寫成演算法教科書摘要

錯誤寫法：

- Bubble Sort is a comparison-based sorting algorithm...

問題：

- 它可能正確，但沒有對應到這支動畫的逐拍教學節奏

正確方向：

- 回到每個 beat 的畫面與事件，說明這一步的教學目的

### 錯誤 3：一個 beat 放太多重點

錯誤寫法：

- 同時講比較、交換、指標移動、整輪意義、時間複雜度

問題：

- 觀眾無法在同一拍吸收這麼多資訊

正確方向：

- 把複雜內容拆成多個 beat

### 錯誤 4：旁白只講結果，不講理由

錯誤寫法：

- 我們交換了它們

問題：

- 觀眾看得到交換，但不知道為什麼交換

正確方向：

- 補上比較依據、規則或不變量

## 撰寫流程建議

建議依以下順序撰寫：

1. 先讀 `plan.md`
2. 確認本次主要模式與教學目標
3. 列出核心 beat 順序
4. 為每個 beat 指定 visual focus
5. 為每個 beat 指定 trace mapping
6. 寫出 viewer takeaway
7. 最後補上簡短教學旁白

不要一開始就寫大段旁白，否則容易脫離畫面與 trace。

## 最小範例

以下是一個簡化的 bubble sort `teaching_script.md` 片段：

```md
# Teaching Script

## Summary
- Algorithm: Bubble Sort
- Audience: 初學者
- Primary teaching goal: 理解相鄰比較如何逐步把較大的值推向右側
- Primary mode: algorithm walkthrough
- Key invariant(s): 每完成一輪，最右側一個元素會固定

## Beats

### Beat 1: 建立初始陣列
- Visual focus: 整個陣列
- Trace mapping: `create_array("main")`
- What happens: 顯示輸入陣列的初始順序。
- What the viewer should learn: 演算法的工作對象是一列可逐步調整順序的元素。
- Teaching narration: 我們先從原始陣列開始，接下來的每一步都會在這個排列上逐步修正順序。
- Invariant or progress cue: 尚未有任何位置固定。

### Beat 2: 比較相鄰元素
- Visual focus: 索引 0 和 1 的元素
- Trace mapping: `highlight([0,1])`
- What happens: 目前焦點落在兩個相鄰元素上，準備判斷是否需要交換。
- What the viewer should learn: 泡沫排序一次只處理局部的相鄰順序。
- Teaching narration: 我們一次只比較相鄰的兩個元素，先確認目前這一對的順序是否正確。
- Invariant or progress cue: 目前仍在本輪的局部比較階段。

### Beat 3: 交換順序錯誤的元素
- Visual focus: 被交換的兩個元素
- Trace mapping: `swap(0,1)` + `unhighlight([0,1])`
- What happens: 若左邊比右邊大，兩者交換位置。
- What the viewer should learn: 交換會把較大的值往右推進一格。
- Teaching narration: 因為左邊比右邊大，所以我們交換它們，讓較大的值往右移動一步。
- Invariant or progress cue: 較大的元素正逐步往本輪末端移動。
```

## 與其他文件的關係

- `plan.md`  
  定義教學目標、模式、不變量與 beat 策略

- `teaching_script.md`  
  定義逐拍教學內容、畫面焦點與旁白

- `action_trace.json`  
  定義實際演算法事件與狀態轉移

- `generated_algo_scene.py`  
  忠於 trace，並依據 teaching script 決定如何讓畫面更容易理解

`teaching_script.md` 的責任，是把「正確的事件」轉成「可學習的節奏」。
