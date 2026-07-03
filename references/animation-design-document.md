# 動畫設計文件

## 目的

`animation_design.md` 是定義演算法動畫如何教學與呈現主題的權威設計契約。它在下游製作開始前，記錄已核准的心智模型、視覺系統、教學推進、高層節拍、使用者決策與已知風險。

文件必須足夠具體，能支援設計審查與後續實作，但不能膨脹成場景程式碼或逐格製作腳本。

## 確認規則

使用者必須對 `animation_design.md` 的精確版本給出明確核准，而該版本必須是獨立審查後得到 `animation_design_review.md = PASS` 的版本。使用者可以編輯 `animation_design.md`。每次使用者編輯都會建立新版本、使先前審查失效，且在接受核准前都必須重新審查。編輯影響決定重審是 full 還是 delta；沒有任何編輯可以繞過重新審查。沉默、無回應或僅編輯檔案都不算核准。

核准只適用於精確已審版本。任何後續編輯都會建立另一個新版本，並再次需要審查與明確確認。

orchestrator 必須在工作流程 gate 之外部記錄精確版本的使用者核准。不得修改 `animation_design.md` 來記錄核准、核准狀態、核准參照或審查中繼資料。

## 必要章節

### 設計目標與受眾

說明觀眾在最後應該理解什麼、目標受眾是誰、假設的先備知識，以及期望的深度。請使用可觀察的學習成果，而不是像「解釋這個演算法」這種泛泛目標。

### 演算法變體與語意

說出精確的演算法變體，並定義會影響動畫的行為：狀態、不變量、tie handling、終止條件、索引或邊界慣例，以及預期輸出。區分哪些是必要語意，哪些只是呈現選擇。

### 主要心智模型

描述觀眾應用來推理此演算法的單一主要概念模型。說明它如何映射到實際演算法狀態，以及這個類比或簡化在哪裡停止對應。

### 要預防的觀眾誤解

列出最可能出現的錯誤結論，以及設計用來預防各自誤解的回應。優先處理由隱藏狀態、模糊移動、誤導性視覺殘留，或 heuristic 與 guarantee 混淆所造成的誤解。

### 範例輸入與理由

提供精確的範例輸入與預期結果。說明它為何能暴露出教學所需的重要決策、狀態變化、邊界行為或對比。不要選一個雖然正確卻在視覺上過於平淡的例子。

### 核心視覺隱喻與視覺語意

定義中央視覺隱喻，以及 position、color、shape、labels、highlights、motion、connectors 與 state changes 的穩定含義。每一個被編碼的屬性都只能有一個清楚含義；裝飾性樣式不可暗示演算法狀態。

### 結構呈現

說明演算法的資料結構與控制狀態如何出現、如何在空間上彼此關聯、哪些元素保持持續存在、哪些會變形。要讓觀眾能定位目前項目、active region、candidates、已確定結果，以及相關歷史。

### 場景結構與資訊層級

定義主要場景區域，以及它們之間的資訊優先順序。說明哪些是 primary、supporting、persistent、transient，或刻意省略。避免同時出現的元素彼此爭奪注意力。

### 教學弧線

描述教學推進：動機、鋪陳、第一個具體動作、重複推理模式、關鍵洞見或對比、完成與總結。每一個階段都要連回觀眾正在建立的心智模型。

### 高層動畫節拍

依順序列出主要節拍。每個節拍都要說明教學目的、可見的演算法狀態、重要轉換，以及觀眾應得到的 takeaway。節拍內容應維持在實作時序與 Manim 操作之上。

### 推薦設計與替代方案

提出推薦設計，附上其理由與重要取捨。只列出真正重要的替代方案，並說明各自何時更合適，以及為何這次沒有選它。不要只是列選項卻不做推薦。

### 已納入的使用者決策

忠實記錄使用者決策；若需要脈絡來避免誤解，也應一併保留。區分直接來自使用者的選擇、designer 的預設值，以及由此導出的後果。

### 風險與 Best-Effort 備註

記錄未解決的低影響細節、假設、accessibility 顧慮、視覺密度風險、技術不確定性與簡化處理。說明採用的 best-effort 處理方式，以及某項是否可能因後續證據提升影響而觸發回退。

### DESIGN_READY 自檢

將每個 `DESIGN_READY` 條件標記為 pass 或 fail，並引用支持該結果的章節。自檢必須涵蓋目標與受眾、語意、心智模型、誤解、範例輸入、每一項適用的型別專用要求；若是 unsupported-category，則要檢查 best-effort 分類、具體覆蓋風險與強化獨立審查要求；另外還要檢查視覺隱喻與語意、結構呈現、場景結構與資訊層級、教學弧線、高層節拍、推薦與取捨、已納入決策、已記錄的風險與預設值，以及零個未解決的阻塞性核心問題。

若任何必要章節缺失、內部不一致、存在重大歧義，或仍在等待核心答案，就不可標示為 ready。

## 撰寫規則

- 為 reviewers 與下游實作者而寫；使用精確、可檢驗的設計敘述。
- 分開描述演算法真實狀態、視覺編碼、教學意圖、使用者決策與 best-effort 假設。
- 每個概念使用一個穩定術語；當精確性重要時，保留 code identifiers 或正式記號。
- 描述觀眾看到與學到什麼，不要只寫演算法做了什麼。
- 讓高層節拍遠離低層動畫 API 呼叫與逐格編排。
- 推薦必須明確，並附上理由與取捨。
- 忠實保留使用者答案；不要把它們改寫成不同決策。
- 只有在能澄清映射、層級或順序時，才使用簡潔圖表或表格。
- 即使內容很短，也保留所有必要標題；若某節無內容，請寫 `None` 並附原因，而不是默默省略。

## 失敗條件

若文件有以下情況，審查會失敗：

- 遺漏或重新命名必要章節；
- 讓演算法語意或主要心智模型保持歧義；
- 只描述吸引人的視覺處理，卻沒有穩定視覺語意；
- 只是重述演算法步驟，而沒有設計教學弧線與觀眾體驗；
- 給出的高層節拍隱藏重要狀態變化或因果關係；
- 列出替代方案，卻沒有推薦、理由與取捨；
- 誤述、遺失或默默覆蓋使用者決策；
- 把未解決的低影響細節當 blocker，或把重要不確定性藏成 best-effort 備註；
- 在文件沒有證據時，卻把 `DESIGN_READY` 標成通過；
- 把沉默、無回應、單純編輯檔案，或未經審查的編輯，當成使用者核准。

## 建議範本

```markdown
# Animation Design: <Algorithm and Variant>

## Design Goal and Audience
...

## Algorithm Variant and Semantics
...

## Primary Mental Model
...

## Viewer Misconceptions to Prevent
...

## Sample Input and Rationale
...

## Core Visual Metaphor and Visual Semantics
...

## Structure Presentation
...

## Scene Structure and Information Hierarchy
...

## Teaching Arc
...

## High-Level Animation Beats
...

## Recommended Design and Alternatives
...

## Incorporated User Decisions
...

## Risks and Best-Effort Notes
...

## DESIGN_READY Self-Check
- [ ] Design goal and audience are explicit — evidence: ...
- [ ] Algorithm variant and semantics are unambiguous — evidence: ...
- [ ] Primary mental model is faithful and bounded — evidence: ...
- [ ] Misconceptions and preventions are identified — evidence: ...
- [ ] Sample input and teaching rationale are suitable — evidence: ...
- [ ] Routed type-specific requirements are addressed, or unsupported-category best-effort classification, specific coverage risk, and strengthened independent review requirement are explicit — evidence: ...
- [ ] Visual metaphor and semantics are stable — evidence: ...
- [ ] Structure presentation is defined — evidence: ...
- [ ] Scene structure and information hierarchy are explicit — evidence: ...
- [ ] Teaching arc and high-level beats expose state and causality — evidence: ...
- [ ] Recommendation, alternatives, rationale, and tradeoffs are recorded — evidence: ...
- [ ] User decisions are incorporated faithfully — evidence: ...
- [ ] Risks and best-effort notes are explicit — evidence: ...
- [ ] Zero unresolved blocking core questions remain — evidence: ...
```
