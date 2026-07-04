# 動畫共同設計指南

## 目的、責任與開始條件

`DESIGN_DEVELOPMENT` 的工作是讓主要 Agent 與使用者共同決定演算法要如何被解釋與演示，並持續更新 `animation_design.md`。主要 Agent 負責設計思考與面向使用者的互動，不把這項工作委派給其他 Agent。

## 六個固定 Scene 與文件格式

`animation_design.md` 必須依序設計六個獨立 Manim `Scene`：

1. 問題與目標
2. 核心觀念
3. 演算法特有的重要資料與狀態
4. 示範一次關鍵動作
5. 完整演示演算法
6. 最終結果與簡短回顧

每個 Scene 都要包含：

- `Teaching Purpose`：這一幕要讓觀眾理解什麼。
- `Explanation Focus`：解說重點，不寫完整旁白台詞。
- `On-Screen Content`：畫面會出現哪些與教學有關的物件、文字與狀態。
- `Concrete Animation Sequence`：依順序描述觀眾實際看到的動作與狀態變化。

動畫順序必須具體，例如先亮起哪些元素、如何比較、哪些內容如何變暗或移動、狀態框如何更新，以及下一個狀態如何出現。不得只寫「演示比較」或「排除不可能區間」。

不要寫 Manim API、精確秒數、完整旁白、方案比較紀錄、風險清單或自我檢查矩陣。

```markdown
# Animation Design: Algorithm Name

## Scene 1: Problem and Goal
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 2: Core Concept
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 3: Algorithm-Specific Data and State
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 4: One Key Action
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 5: Full Algorithm Demonstration
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence

## Scene 6: Result and Recap
### Teaching Purpose
### Explanation Focus
### On-Screen Content
### Concrete Animation Sequence
```

- 六個 Scene 的教學功能不可合併或省略。
- 第三個 Scene 不解釋一般程式設計與資料結構基礎，只解釋該演算法特有且必要的資料或狀態。
- 第六個 Scene 顯示最終答案並簡短重述演算法如何從輸入得到結果，不加入預測問題或互動要求。
- Scene 之間固定淡出至空白，再淡入下一幕。

## 共同設計流程

按教學順序逐步設計。每次只向使用者詢問一個決定，避免一次要求使用者評估整套場景規劃。

只有當一個教學部分確實有多種不同且合理的呈現方式時才詢問。字體、間距、局部位置、精確秒數、一般淡出時間與其他例行實作細節由主要 Agent 自行決定。

需要詢問時，提出三個完整方案。每個方案都要同時說明：

- 畫面會出現什麼
- 解說重點
- 觀眾實際會看到的動畫動作順序
- 這種方式如何幫助理解
- 主要 Agent 是否推薦，以及推薦理由

方案必須是具體動畫設計，不得只列抽象方向或把視覺、解說與動作拆成不同問題。

使用者可以選擇其中一個方案、混合不同方案、要求修改，或提出自己的設計。只要使用者提出明確設計，就採用並整合。

使用者做出決定後，直接更新 `animation_design.md` 並進入下一個設計決定。不要在對話中重述決定要求二次確認。

若使用者未指定受眾程度，預設觀眾理解基本程式設計、陣列、索引、變數、迴圈、條件判斷與常見資料結構。第三個 Scene 只解釋該演算法特有且理解時必要的資料或狀態。

## 教學設計原則

選擇能展現演算法關鍵判斷與狀態變化的精簡範例。避免使用已經接近答案、只有單一路徑，或避開演算法代表性操作的輸入。

六幕依序先說明問題與輸入輸出，再建立核心觀念、介紹演算法特有狀態、慢速示範一次完整關鍵動作與理由、用具體輸入完整演示，最後顯示結果並簡短回顧。

先讓造成動作的資料、比較或規則可見，再呈現動作，最後呈現結果。保留足夠的前一狀態，讓觀眾能比較變化，不需要記住已消失的資訊。

同一種顏色、位置、框線或動作在六個 Scene 中應維持相同含義。畫面與解說重點不得表達不同狀態或時序。

只有當不同方式會實際改變觀眾如何理解教學內容時，才提出三個方案。不要把配色、字體、間距、局部位置或精確 timing 當成需要使用者決定的教學方案。

## 視覺語言

同一種顏色、框線、位置、標籤或動作在整部影片中只代表一個意思。必須讓觀眾能區分基本資料、目前焦點、候選項目、已完成進度、已排除區域與必要支援結構。

每個動畫動作只保留一個主要焦點。先讓造成動作的資料或判斷可見，再演示動作，最後顯示結果。非目前焦點的內容可以降低存在感，但不要太早移除理解因果所需的脈絡。

主要資料結構的位置應保持穩定。不要為了局部更新重排整個畫面，也不要讓文字或輔助面板與演算法動畫爭奪注意力。

Queue、stack、搜尋範圍、temporary slot 或其他支援結構只有在它們能解釋演算法行為時才顯示。需要顯示時，讓它們保持可讀，但視覺層級低於目前演算法動作。

- 畫面文字保持短而具體。
- 不用畫面長句重複旁白內容。
- 動作必須幫助說明比較、移動、排除、發現或完成等狀態變化。
- 裝飾性動作不得改變或模糊演算法含義。

## 完成與審查交接

六個 Scene 都依文件格式完成後，派遣獨立 `animation-design-reviewer` 進行內容品質審查。

- 不改變使用者選定呈現方式的問題，由主要 Agent 直接修正。
- 會改變使用者選定呈現方式的問題，必須重新提出修正方案並詢問使用者。
- 每次修正後重新審查，直到 `animation_design_review.md = PASS`。
- 審查通過後，請使用者檢查完整 `animation_design.md`。只有明確核准後才能進入 `SCRIPT`。
