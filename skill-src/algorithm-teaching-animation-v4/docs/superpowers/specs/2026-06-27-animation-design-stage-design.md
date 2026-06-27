# 動畫設計階段規格

## 目的

將目前只處理需求的第一階段，改造成以設計為核心的工作流程。這套流程要能協助使用者把尚未完整的演算法動畫需求，發展成經過審查、可直接編輯且品質良好的動畫設計，之後才開始撰寫腳本或進行實作。

使用者不應被迫自行完成動畫設計。專門的 subagent 必須主動提出心智模型、視覺表達、教學弧線與替代方案；使用者則透過明確的核准關卡保有最終決定權。

## 頂層工作流程

將 `REQUEST_CONTRACT` 改名為 `ANIMATION_DESIGN`，並保留現有的六階段架構：

```text
ANIMATION_DESIGN -> SCRIPT -> VOICEOVER -> RENDER -> QA -> DELIVERY
```

`ANIMATION_DESIGN` 包含三個不可跳過的子階段：

```text
INTAKE -> DESIGN_DEVELOPMENT -> CONTRACT
```

不得跳過任何子階段。如果後續工作發現前面階段存在缺口，必須退回負責該決策的子階段處理。

## 子階段 1：INTAKE

### 目標

準確保留使用者需求，並準備足以開始設計工作的來源資料，但不在此時過早決定動畫設計。

### 負責角色

此子階段由協調者負責。

### 職責

- 保留使用者對需求、限制與禁止事項的原始措辭，特別是會影響演算法語意、教學方向、視覺設計、交付內容或驗收標準的內容。
- 記錄演算法、已知版本、範例輸入或情境、目標觀眾、使用目的、視覺限制、旁白需求與特殊要求。
- 將需求分類為 first-class support 或 best-effort support。
- 記錄尚未解決的設計問題，不得擅自回答。
- 建立 `intake_summary.md`，並交給 `animation-designer`。

### 關卡

只有當 `intake_summary.md` 已包含目前已知的需求、保留的限制、支援類型及開始設計所需的未決問題時，`INTAKE` 才能通過。

## 子階段 2：DESIGN_DEVELOPMENT

### 目標

將使用者需求發展成具體、連貫、可實作且具有教學效果的演算法動畫設計。

此子階段的核心工作是設計動畫如何教學及呈現演算法。需求釐清只是支援設計的手段，不是此子階段的主要目的。

### Animation Designer

新增 `agents/animation-designer.md`。這個 agent 同時負責核心問題規劃與動畫設計。

職責如下：

1. 分析演算法版本、目標觀眾、教學目標、範例情境、觀眾可能產生的誤解，以及原始需求中的風險。
2. 選擇並解釋觀眾看完後應保留的主要心智模型。
3. 設計演算法狀態、資料、指標、邊界、輔助結構、處理進度與排除區域如何出現在畫面上。
4. 定義穩定的視覺語意、資訊層級與主要畫面結構。
5. 選擇或改善範例輸入，使其能呈現預定的教學重點。
6. 設計整體教學弧線與高層次動畫 beats。
7. 定義每個 beat 的主要焦點、狀態變化、因果關係與教學目的。
8. 評估使用者原始構想、找出品質風險、比較合理替代方案，並在必要時明確推薦較好的方案。
9. 只規劃會阻塞良好設計的高影響問題，並為每題提供推薦答案與理由。
10. 建立並修改 `animation_design.md`。
11. 在請求獨立審查前執行 `DESIGN_READY` 自我檢查。

使用者保有最終決定權。Agent 可以挑戰原始構想並推薦不同方案，但不得推翻使用者的明確決定。

### 核心問題互動方式

採用批次交接方式，降低 token 消耗與委派成本：

1. `animation-designer` 一次規劃少量高影響問題。
2. 每個問題都要包含重要性、具體建議與取捨。
3. 協調者一次只向使用者詢問一題，並忠實記錄回答。
4. 協調者不得取代設計師的推薦內容，也不得自行替設計師推導設計結論。
5. 預定問題全部回答後，協調者再將答案整批交回 `animation-designer`。
6. 只有當回答暴露新的阻塞問題時，才能開始下一批問題。

除非使用者明確賦予其語意或契約上的重要性，否則不得詢問一般配色、微小位置、普通轉場、easing 或局部時間調整。

### 動畫設計產物

建立可由使用者直接編輯的 `animation_design.md`。內容必須包括：

- 設計目標與目標觀眾
- 演算法版本與語意
- 主要心智模型
- 預期避免的觀眾誤解
- 範例輸入及選擇理由
- 核心視覺比喻與穩定的視覺語意
- 資料、指標、邊界、處理進度與輔助結構的呈現方式
- 畫面結構與資訊層級
- 整體教學弧線
- 高層次動畫 beats
- 每個 beat 的焦點、狀態變化、因果關係與教學目的
- 推薦設計、重要替代方案、取捨與理由
- 已納入的使用者決策
- 風險與 best-effort 說明
- `DESIGN_READY` 自我檢查結果

使用者可以直接修改此檔案，但直接修改不得繞過獨立審查。

### DESIGN_READY 關卡

只有在以下條件全部成立時，設計才可送交獨立審查：

- 演算法版本、目標觀眾與教學目標均已明確。
- 心智模型、視覺表達與教學弧線均已完整。
- 範例輸入足以支持預定教學內容。
- 高層次 beats 具有明確焦點與因果進程。
- 沒有會改變演算法語意、教學方向、核心版面、beat 結構或交付責任的未決問題。
- 教學連貫性、視覺可行性與語意一致性均已通過自我檢查。
- 設計已包含明確的推薦方案與重要取捨。
- 剩餘風險均已揭露。

達成以上條件後，設計師必須停止探索並請求審查，不得為了最佳化低影響的呈現細節而延後關卡。

### 獨立 Reviewer

新增 `agents/animation-design-reviewer.md`。Reviewer 不得參與受審設計的撰寫。

Reviewer 必須建立 `animation_design_review.md`，內容包括：

- 審查範圍：完整審查或差異審查
- 教學連貫性結果
- 視覺可行性結果
- 演算法語意一致性結果
- 尚未解決的高影響問題
- 必須修正的項目
- 回退目標
- 最終結果：`PASS` 或 `FAIL`

第一次審查一律採完整審查。審查失敗後，普通的局部修正採差異審查；若修改演算法語意、主要心智模型、核心視覺語意或教學弧線，則必須重新進行完整審查。使用者直接修改 `animation_design.md` 後，也適用相同規則。

只有 reviewer 結果為 `PASS` 時，協調者才能請求使用者明確核准 `animation_design.md`。

### 使用者核准設計

只有在獨立審查結果為 `PASS`，且使用者明確核准後，動畫設計才算通過。沉默或只修改檔案不算核准。

## 子階段 3：CONTRACT

### 目標

將已核准的動畫設計轉成供後續階段使用的正式契約，不得重新開啟設計或悄悄改變設計。

### 負責角色

由 `animation-designer` 將已核准的 `animation_design.md` 轉成 `pre_build_brief.md`，不再使用獨立的 `brief-editor`。

### 規則

- 保留所有已核准的核心決策及其來源。
- 明確區分使用者原始要求、使用者核准的決策與 Agent 預設值。
- 為後續階段凍結演算法語意、視覺語意、教學弧線、交付層級、旁白責任與 overlay policy。
- 不得新增未經核准的核心決策。
- 如果轉換過程暴露缺少的核心決策，必須退回 `DESIGN_DEVELOPMENT`；更新、重新審查並再次核准 `animation_design.md` 後，才能重新嘗試。
- 如果設計本身完整，問題只出在契約措辭或來源標示，則留在 `CONTRACT` 修正。

使用者必須分別明確核准 `animation_design.md` 與 `pre_build_brief.md`。只有正式契約取得核准後，`ANIMATION_DESIGN` 才能通過。

## 產物與資料流

```text
使用者需求
    |
    v
intake_summary.md
    |
    v
animation_design.md
    |
    v
animation_design_review.md = PASS
    |
    v
使用者明確核准設計
    |
    v
pre_build_brief.md
    |
    v
使用者明確核准契約
    |
    v
SCRIPT
```

## 回退規則

- 原始需求記錄錯誤：退回 `INTAKE`。
- 設計不完整或審查失敗：退回 `DESIGN_DEVELOPMENT`。
- 契約措辭或來源標示錯誤：留在 `CONTRACT`。
- 契約轉換暴露設計缺口：退回 `DESIGN_DEVELOPMENT`。
- 後續階段發現核心演算法語意、心智模型、視覺語意或教學弧線仍有歧義：退回 `DESIGN_DEVELOPMENT`，不得在 `SCRIPT` 或 `RENDER` 中直接修補。

## Agent 與 Reference 結構

### 新增

- `agents/animation-designer.md`
- `agents/animation-design-reviewer.md`
- `references/animation-design-process.md`
- `references/animation-design-document.md`
- `references/teaching-design.md`
- `references/animation-design-review-checklist.md`
- `references/animation-design-array-sorting.md`
- `references/animation-design-search.md`
- `references/animation-design-graph-traversal.md`

### 沿用或修改

- `references/intake-contract.md`
- `references/high-impact-clarification.md`
- `references/visual-language.md`
- `references/default-visual-semantics.md`
- `references/pre-build-brief.md`

Agent 檔案只定義角色、流程、輸入、輸出、reference 路由、禁止事項與回退責任。詳細設計知識應放在 references 中。

設計師與 reviewer 都必須閱讀通用 references，並且只讀取與目前演算法類型相關的專用 reference。若沒有對應的專用 reference，則使用通用設計方法、將工作標記為 `best-effort`、揭露知識覆蓋風險，並採用更嚴格的審查。

### 移除

- `agents/brief-editor.md`
- `agents/clarification-planner.md`

這兩個角色的必要職責將移入 `animation-designer`。

## 驗證方式

實作後必須確認：

- `SKILL.md`、agent 檔案與 references 中的階段名稱、產物鏈、關卡及回退規則一致。
- 所有已移除角色的引用都已清除。
- 新 agent 均有明確的輸入、輸出、禁止事項與回退規則。
- `animation_design.md` 結構涵蓋所有 `DESIGN_READY` 條件。
- Reviewer checklist 能針對每個關卡條件產生有證據支持的結果。
- 工作流程不能從 `INTAKE` 直接跳到 `CONTRACT`。
- Reviewer 結果為 `FAIL`、設計尚未核准或契約尚未核准時，`SCRIPT` 均不得開始。
- 代表性流程走讀涵蓋 array sorting、binary search、BFS 與一個 best-effort 演算法。
- Sorting 走讀驗證移動語意與 settled progress。
- Search 走讀驗證區間語意與選定的心智模型。
- BFS 走讀驗證 queue visibility、visited timing 與 layer expansion。
- Best-effort 走讀驗證風險揭露與加強審查。

## 成功標準

當使用者可以從不完整的動畫需求開始，取得專業設計協助、直接編輯具體的設計產物、核准通過獨立審查的動畫設計，並在後續製作開始前再次核准忠實轉換而成的正式契約，即代表此變更成功。
