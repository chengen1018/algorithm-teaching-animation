# How to Write Teaching Script

請依照以下順序，把已確認需求與已核准動畫設計整理成 `teaching_script.md`。完成的腳本必須讓後續的 voiceover writer 與 scene writer 不必猜測教學順序、畫面焦點或語意。

## 1. 先理解腳本的職責

`teaching_script.md` 是動畫設計與實際製作之間的教學結構層。它把已核准的內容拆成一連串可教、可說、可實作的 Beat。

腳本必須回答三個問題：

1. 每個 Beat 要讓觀眾理解什麼？
2. 當下要引導觀眾看哪個結構或動作？
3. 每個局部動作如何累積成完整的教學進程？

不要用腳本補做下列工作：

- 不要代替需求澄清。
- 不要自行決定尚未核准的演算法語意或視覺設計。
- 不要寫成 Manim 動畫指令、版面座標或逐行場景實作。

## 2. 確認可以開始

開始撰寫前，完整閱讀：

- `confirmed_requirements.md`
- `animation_design.md`

只有在忠實描述演算法流程所必需時，才查閱 `confirmed_requirements.md` 內保存的使用者 code 或 pseudocode。它們只能協助確認流程，不能覆蓋已確認需求或已核准設計。

## 3. 建立整體教學主線

先用摘要固定整份腳本的方向，再拆分 Beat。摘要必須包含：

- `Algorithm`：本次示範的演算法。
- `Teaching goal`：觀眾看完後應理解的核心內容。
- `Key semantics`：所有 Beat 都必須遵守的關鍵演算法語意與視覺含義。
- `Complexity scope`：逐項列出 `animation_design.md` 的 `Complexity Scope` 中已核准的 time cases 與 space treatment；不得加入 scope 外的 case。

接著依已核准的 Scene 順序與 sample input 的實際執行過程，列出演算法狀態如何逐步改變。不要先寫口語旁白；先確認教學事件的順序完整且沒有跳步。

## 4. 將教學主線拆成 Beat

一個 Beat 只承擔一個主要教學點與一個主要局部事件。好的 Beat 通常依序完成：

1. 建立當前局部狀態。
2. 顯示一個局部決策或狀態轉換。
3. 說明這次改變留下的進度線索或不變量。

Beat 不必等同一次 loop iteration，但必須能在單一 voiceover segment 中維持一致的視覺焦點。遇到下列事件時，通常應拆成不同 Beat：

- 在兩個 active candidates 之間進行 compare-then-choose。
- 會改變局部狀態的 swap 或 pointer move。
- 被移動的 candidate 在新位置上需要重新檢查。

若解說必須連續使用多個「然後」才能跨過多次比較、交換或 pointer move，表示 Beat 太粗，應繼續拆分。只有在已核准教學目標明確要求摘要重複工作時，才可用一個 Beat 概括多次相同操作。

Scene 4 的每個已核准 complexity case 都要用足夠數量的原子 Beat，依序建立：input variables、工作單位、一般化的重複／分層／phase 結構、expression，以及最終 case label。Beat 數量依推導需要決定，不固定壓成單一 Beat。只承接 `Complexity Scope` 已核准的 case。

## 5. 完整填寫每個 Beat

每個 Beat 都必須包含下列六個欄位：

- `Viewer goal`：觀眾在這個 Beat 結束時應理解什麼。
- `Algorithm moment`：對應演算法流程中的哪個明確時刻，以及狀態如何改變。
- `Visual focus`：觀眾當下應看哪個結構、元素或動作。
- `Teaching note`：這個時刻為何重要，以及它如何支撐整體理解。
- `Progress cue`：Beat 結束後已確立的進度、不變量或仍成立的狀態。
- `Voiceover intent`：後續旁白必須口語化傳達的單一 takeaway；不要在此撰寫完整旁白稿。

使用具體、面向觀眾的語言。直接寫出比較對象、選擇結果、pointer 位置或區間邊界，不要用「正常步驟」、「照常處理」等泛稱掩蓋細節。

若 support structure 對理解當前事件很重要，請在 `Visual focus` 或 `Progress cue` 明確說明它為何必須保持可見。

## 6. 使用固定輸出格式

建立 `teaching_script.md`，至少使用以下結構：

```md
# Teaching Script

## Summary
- Algorithm:
- Teaching goal:
- Key semantics:
- Complexity scope:

## Beats

### Beat 1: <簡短且具體的教學事件名稱>
- Viewer goal:
- Algorithm moment:
- Visual focus:
- Teaching note:
- Progress cue:
- Voiceover intent:

### Beat 2: <簡短且具體的教學事件名稱>
- Viewer goal:
- Algorithm moment:
- Visual focus:
- Teaching note:
- Progress cue:
- Voiceover intent:
```

可以依已核准設計加入 Scene 標題來分組 Beat，但不要刪除或改變上述必要欄位。每個 Beat 必須能對應到已核准設計中的內容，不能加入上游來源沒有的新意思。

## 7. 完成寫作後自我檢查

交付審查前，從頭讀一次 `teaching_script.md`，逐項確認：

- 摘要與所有 Beat 都符合 `confirmed_requirements.md` 及已核准的 `animation_design.md`。
- Beat 順序忠於 sample input 的演算法流程與已核准 Scene 順序。
- 每個 Beat 只有一個主要教學事件，並完整填寫六個必要欄位。
- Scene 4 的每個已核准 complexity case 都依序覆蓋 input variables、工作單位、一般化結構、expression 與 case label，且沒有未核准 case。
- 觀眾注意力、狀態改變及 progress cue 能前後銜接成清楚的教學弧線。
- 重要的 support structures、pointers、boundaries 與 temporary slots 已在需要時明確命名。
- Voiceover writer 能直接把 `Voiceover intent` 口語化，不必發明新教學邏輯。
- Scene writer 能判斷畫面焦點、必須保持可見的結構及進度何時出現，不必猜測隱藏子節拍。
