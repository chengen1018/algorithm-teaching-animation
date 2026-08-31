# 動畫共同設計指南

## 目的、責任與開始條件

`DESIGN_DEVELOPMENT` 的工作是讓主要 Agent 與使用者共同決定演算法要如何被解釋與演示，並持續更新 `animation_design.md`。

## 參考路由與專用參考選擇

開始前，主要 Agent 必須閱讀 `confirmed_requirements.md`、本指南與 `references/how-to-design-complexity-analysis.md`。使用者提供的 algorithm variant、code 或 pseudocode 以 `confirmed_requirements.md` 內保存的內容為準。Complexity reference 定義每次設計都要執行的分析與核准 gate。

此外，依演算法類型最多讀取下表中唯一一份適用的專用參考：

| 演算法類型 | 必讀的專用參考 |
| --- | --- |
| Array sorting | `references/how-to-design-array-sorting-animation.md` |
| Graph traversal | `references/how-to-design-graph-traversal-animation.md` |
| 區間或候選區域收縮型 search | `references/how-to-design-narrowing-search-animation.md` |
| 其他演算法類型 | 無；只使用本指南。 |

## 五幕契約

`animation_design.md` 必須依序設計五個獨立 Manim `Scene`：

1. Scene 1 問題與目標
2. Scene 2 演算法如何運作：決策規則與追蹤狀態
3. Scene 3 完整演示演算法，結尾直接顯示範例答案
4. Scene 4 複雜度分析，完整涵蓋已核准 `Complexity Scope`
5. Scene 5 最終總結，只整理答案、核心方法與已教 complexity

## DESIGN_DEVELOPMENT 執行流程

### 共同設計流程

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

### Complexity Scope Gate

設計 Scene 4 前，依 `references/how-to-design-complexity-analysis.md` 完成下列步驟：

1. 以 `confirmed_requirements.md` 內保存的 algorithm variant、code 或 pseudocode 建立 Analysis Basis，選擇代表性 cases，並依 reference 的固定格式提出 `Complexity Analysis Proposal`。完成條件：每個 proposal claim 都有可審查的 assumptions、counted operation、derivation 與 source locator。
2. 取得使用者對 time cases 與 space treatment 的明確決定。完成條件：至少一個 primary time case 或使用者選定的 replacement time case 已獲明確核准；只有明確核准的項目進入 scope，optional case 不會自動加入。
3. 將核准結果寫入 `animation_design.md` 中 Scene 3 與 Scene 4 之間的固定 `Complexity Scope` topology。Analysis basis 與 Analysis source 必須是不同欄位；contrast 為零時仍寫出 `None — zero approved contrast time cases`。所有六個欄位都必須有值。

Persistence gate：使用者核准後，先寫入 complete fixed `Complexity Scope` block before any Scene 4/5 design。`Complexity Scope` 核准是局部 scope gate；核准前或完整 block 尚未持久化時保持在 `DESIGN_DEVELOPMENT`。Design reviewer `PASS` 之後，仍須把完整 `animation_design.md` 交給使用者取得整體設計核准，才完成本階段。

## 全片設計原則

### 教學設計原則

若使用者未指定受眾程度，預設觀眾理解基本程式設計、陣列、索引、變數、迴圈、條件判斷與常見資料結構。

選擇能展現演算法關鍵判斷與狀態變化的精簡範例。避免使用已經接近答案、只有單一路徑，或避開演算法代表性操作的輸入。

先讓造成動作的資料、比較或規則可見，再呈現動作，最後呈現結果。保留足夠的前一狀態，讓觀眾能比較變化，不需要記住已消失的資訊。

同一種顏色、位置、框線或動作在五個 Scene 中應維持相同含義。畫面與解說重點不得表達不同狀態或時序。

只有當不同方式會實際改變觀眾如何理解教學內容時，才提出三個方案。不要把配色、字體、間距、局部位置或精確 timing 當成需要使用者決定的教學方案。

### 視覺語言

同一種顏色、框線、位置、標籤或動作在整部影片中只代表一個意思。必須讓觀眾能區分基本資料、目前焦點、候選項目、已完成進度、已排除區域與必要支援結構。

每個動畫動作只保留一個主要焦點。先讓造成動作的資料或判斷可見，再演示動作，最後顯示結果。非目前焦點的內容可以降低存在感，但不要太早移除理解因果所需的脈絡。

主要資料結構的位置應保持穩定。不要為了局部更新重排整個畫面，也不要讓文字或輔助面板與演算法動畫爭奪注意力。

Queue、stack、搜尋範圍、temporary slot 或其他支援結構只有在它們能解釋演算法行為時才顯示。需要顯示時，讓它們保持可讀，但視覺層級低於目前演算法動作。

- 畫面文字保持短而具體。
- 不用畫面長句重複旁白內容。
- 動作必須幫助說明比較、移動、排除、發現或完成等狀態變化。
- 裝飾性動作不得改變或模糊演算法含義。

## animation_design.md 固定格式

每個 Scene 都要包含：

- `Teaching Purpose`：這一幕要讓觀眾理解什麼。
- `Explanation Focus`：解說重點，不寫完整旁白台詞。
- `On-Screen Content`：畫面會出現哪些與教學有關的物件、文字與狀態。
- `Concrete Animation Sequence`：依順序描述觀眾實際看到的動作與狀態變化。
- `Completion Criteria`：列出本幕結束前，觀眾必須已能理解或辨認的內容。
- `Boundary`：指出本幕不得提前教授或重複演示的內容。

動畫順序必須具體，例如先亮起哪些元素、如何比較、哪些內容如何變暗或移動、狀態框如何更新，以及下一個狀態如何出現。不得只寫「演示比較」或「排除不可能區間」。

```markdown
# Animation Design: Algorithm Name

## Scene 1: 問題與目標
### Teaching Purpose
- 讓觀眾理解要解決的具體問題、完整代表性輸入，以及本題要求尋找、改變或判定的對象。

### Explanation Focus
- 說明問題與輸入本身，不解釋演算法將如何操作輸入。
- 明確指出本題要求尋找、改變或判定的對象。

### On-Screen Content
- 顯示具實際值的完整代表性輸入，不以抽象符號或不完整片段代替。
- 以直接可辨認的方式標出本題要求尋找、改變或判定的對象。

### Concrete Animation Sequence
1. 呈現要解決的具體問題。
2. 顯示一份完整的代表性輸入，並標出本題要求尋找、改變或判定的對象。
3. 確認問題與輸入都已清楚可辨後結束本幕。

### Completion Criteria
- 即使尚未知道演算法如何運作，觀眾也能指出問題、完整輸入與待處理對象。

### Boundary
- 不介紹指標、候選範圍、比較角色、支援結構、追蹤狀態、更新規則或終止條件；這些內容留到 Scene 2。

## Scene 2: 演算法如何運作：決策規則與追蹤狀態
### Teaching Purpose
- 讓觀眾對演算法如何逐步處理問題建立概念性理解。
- 讓觀眾認得 Scene 3 代表性範例會使用的主要追蹤狀態與動作。

### Explanation Focus
- 說明演算法反覆進行的核心行為，以及每一步大致會觀察或比較什麼。
- 只介紹 Scene 3 代表性範例實際會使用的重要判斷方向與主要追蹤狀態。
- 說明主要追蹤狀態的概念性用途，不要求觀眾在本幕掌握所有分支或精確執行細節。

### On-Screen Content
- 顯示能代表演算法核心概念的簡化資料狀態。
- 顯示 Scene 3 會使用的主要追蹤狀態，並以簡短標籤說明其概念性用途。
- 顯示一次最小的「觀察或比較 → 做出判斷 → 改變狀態」因果關係。

### Concrete Animation Sequence
1. 以簡化畫面說明演算法會如何逐步處理問題。
2. 引入 Scene 3 需要理解的主要追蹤狀態，並說明其概念性用途。
3. 使用一次最小的局部動作，呈現演算法如何根據觀察或比較改變狀態。
4. 只說明 Scene 3 代表性範例實際會遇到的重要判斷方向，不延伸介紹未使用的分支。
5. 確認本幕使用的狀態標記、顏色與動作含義；Scene 3 必須沿用相同含義。

### Completion Criteria
- 觀眾能概略說明演算法如何逐步處理問題、主要追蹤狀態各代表什麼，以及一次觀察或比較如何造成下一個狀態。
- 不要求觀眾記住全部分支、精確更新規則或自行執行整個演算法；Scene 3 可以跟著代表性範例逐步補足實際執行細節。

### Boundary
- 只能使用靜態狀態或一次最小的局部操作建立概念，不得從完整輸入一路執行到答案。
- 不得為了完整列舉演算法而介紹 Scene 3 代表性範例不會使用的分支。

## Scene 3: 完整演示演算法
### Teaching Purpose
- 讓觀眾跟著同一個代表性範例，看到演算法如何從初始輸入逐步得到結果。
- 將 Scene 2 的概念性理解轉化成可觀察的實際執行過程。
- 為 Scene 4 留下可沿用的 comparison、scan、level、phase、augmentation 或 table-update 操作語意。

### Explanation Focus
- 使用 Scene 1 的完整代表性輸入，按照演算法的真實執行順序推進。
- 每一步都說明目前觀察或比較的具體資料、得到的判斷，以及接著採取的動作。
- 將 Scene 2 的概念套用到範例中的具體數值與狀態，只沿著這個範例實際發生的執行路徑前進。
- 可以解釋某次判斷為何導致某個更新，但不得加入 Scene 2 完全未建立的新機制。

### On-Screen Content
- 顯示完整代表性輸入、目前焦點，以及 Scene 2 已介紹的主要追蹤狀態。
- 清楚區分目前焦點、待處理、已處理與已排除的內容。
- 保留理解目前決策所需的資料與前一狀態，直到動作及更新結果清楚可辨。
- 讓 Scene 4 需要一般化的工作單位保持可辨認，但在本幕只服務 sample execution。

### Concrete Animation Sequence
1. 重新呈現 Scene 1 的完整代表性輸入，並套用 Scene 2 已建立的狀態標記。
2. 顯示演算法的初始追蹤狀態。
3. 聚焦目前要觀察、比較或處理的具體資料。
4. 先呈現造成決策的資料或比較結果，再說明這次判斷在目前範例中的意義。
5. 動畫化相應的資料動作或狀態更新，並保留更新前後的關聯。
6. 重複「觀察或比較 → 判斷 → 動作或更新」，直到範例符合停止條件。
7. 顯示停止時的完整資料與最終狀態，直接標出這個範例的答案。

### Completion Criteria
- 範例已從初始輸入完整執行到停止狀態，且沒有省略任何會影響結果的步驟。
- 每個重要動作都能回溯到造成它的觀察、比較或判斷；每次重要更新都有可見的更新前後關係。
- Scene 2 建立的視覺含義保持一致，觀眾不需要猜測任何會影響結果的步驟。
- 範例答案已清楚顯示，Scene 4 所需的一般化入口已有可見的操作語意。

### Boundary
- 負責執行範例與呈現因果，不重新進行 Scene 2 的概念介紹。
- 不介紹代表性範例沒有使用的其他分支，也不臨時加入新的追蹤狀態或決策機制。
- 不進行漸近推導；sample 的工作單位與次數由 Scene 4 一般化到 input-size work count。

## Complexity Scope
- Analysis basis: <algorithm variant, input variables, implementation or representation assumptions, counted operation, and derivation basis>
- Analysis source: <source type and precise source locator for the algorithm variant and derivation evidence>
- Approved primary time case: <case and complexity>
- Approved contrast time cases: <None — zero approved contrast time cases, or every approved case and complexity>
- Approved space treatment: <omit, one-line summary, or visual derivation>
- Approval evidence: <the user's explicit decision>

## Scene 4: 複雜度分析
### Teaching Purpose
- 讓觀眾看見已核准 complexity claims 如何從演算法的工作結構形成。

### Explanation Focus
- 完整涵蓋 `Complexity Scope` 中每個已核准 time case 與 space treatment。
- 從 Scene 3 的 sample cues 出發，依 complexity reference 的 `Visual Derivation` 一般化到 input-size work count。

### On-Screen Content
- 顯示 input variables、counted operation、重複結構或 aggregation、expression，以及完整 case label。
- 空間內容依已核准的 omit、one-line summary 或 visual derivation 處理。

### Concrete Animation Sequence
1. 沿用 Scene 3 已建立的工作單位語意。
2. 定義 input size，顯示工作單位如何隨規模重複、分層、分 phase 或求和。
3. 將次數與單次成本組成 expression，化簡後標示 case 與 complexity。
4. 對每個已核准 case 完成同樣的可見鏈條，並完成已核准的 space treatment。

### Completion Criteria
- `Complexity Scope` 的每個已核准 case 都有完整 `Visual Derivation`，且 assumptions、expression 與 case label 一致。
- Scene 3 的 sample cues 已一般化到輸入規模，而非作為 complexity proof。

### Boundary
- 只教授使用者已核准的 scope；新增或改變 case 時回到 complexity proposal 與 approval gate。

## Scene 5: 最終總結
### Teaching Purpose
- 收束答案、核心方法與前四幕已教過的 complexity。

### Explanation Focus
- 再次指出 Scene 3 的範例答案，概括核心方法，並整理 Scene 4 已教過的主要 time complexity。
- 只有 Scene 4 已涵蓋或明確簡短標示的 space complexity 與 contrast cases 才進入總結。

### On-Screen Content
- 顯示最終答案、最重要的演算法概念，以及 Scene 4 已標示的 complexity labels。

### Concrete Animation Sequence
1. 重新聚焦 Scene 3 已得到的範例答案。
2. 以已出現的視覺語意概括核心方法。
3. 顯示 Scene 4 已教過的主要 time complexity，以及 scope 內適用的 contrast 或 space 結論。
4. 收束畫面，只留下答案、核心方法與已教 complexity。

### Completion Criteria
- 觀眾能指出範例答案、核心方法與已教的 complexity，所有總結內容都能回溯到前四幕。

### Boundary
- 總結已建立的內容。答案驗證與正確性證明不屬於整部動畫的任何 Scene；新推導與新的 complexity cases 回到 `Complexity Scope Gate` 與 Scene 4 設計。
```

- Scene 之間固定淡出至空白，再淡入下一幕。
