# Script Review 檢查表

## 必要輸出
回傳 `script_review_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- 審查結果必須由獨立 reviewer 撰寫
- 帶有證據的 findings
- 修復方向：`SCRIPT`、`DESIGN_DEVELOPMENT` 或 `CONTRACT`

`script_review_result.md` 必須由獨立 reviewer 撰寫。script writer 的自我審查無效。

## 審查輸入
- 已核准的 `pre_build_brief.md`
- `teaching_script.md`

## 審查問題
### Contract Fidelity

- script 是否留在已核准的 `pre_build_brief.md` 範圍內，而沒有發明新語意？
- beats 是否遵守已凍結的 `Resolved High-Impact Clarifications`、`Overlay Policy` 與 `Delivery Tier`？
- 是否有任何措辭把本該在 brief 中凍結的分歧藏起來，改由 script 自行猜測？

若 script 之所以能繼續，是因為已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上有缺漏或衝突，則回到 `DESIGN_DEVELOPMENT`。必須先設計修復、重新審查與重新核准，再重新產生並重新核准 brief。
若已核准設計清楚，但 script 暴露 brief wording 或 source labels 錯誤，或其他不忠實轉換問題，則回到 `CONTRACT`。修復並重新核准 brief，無需重新設計。

### Teaching Coherence

- 每個 beat 是否都有一個清楚教學目的，而不是混合或漂移的目標？
- 觀眾注意力是否被導向當下最重要的結構或動作？
- progress cues 是否累積成可讀的課程弧線，而不是孤立的局部描述？

若 brief 中已有正確教學邏輯，但 script 解釋太弱或順序錯誤，則修復留在 `SCRIPT`。

### Beat Completeness

- 每個 beat 是否都定義了 viewer goal、algorithm moment、visual focus、teaching note、progress cue 與 voiceover intent？
- 當 brief 說 support structures、pointers、boundaries 與 temporary slots 很重要時，它們是否被清楚命名？
- 下游 scene writer 是否能不靠猜測就實作整個 beat 序列，並知道改變了什麼、為何重要？

若 script 在結構上過薄、缺少 beat 欄位，或太泛泛而無法驅動 render work，則修復留在 `SCRIPT`。

### Beat Atomicity 與 Narration Readiness

- 每個 beat 是否只包含一個可教的局部事件，而不是多個連續局部決策，需要分開口說時序？
- 下游 voiceover 是否能忠於 beat，而不用在單一 beat 內追逐多個不同局部比較、交換或 pointer moves？
- 下游 scene writer 是否能實作 beat timing，而不用自行發明隱藏子節拍或本地決定新重點？

若 brief 清楚，但某個 beat 太粗，不足以支撐忠實同步 narration，則修復留在 `SCRIPT`。

### Voiceover Readiness

- `voiceover.md` 是否能忠於這份 script，而不需要發明新教學邏輯？
- 每個 beat 是否都已包含後續 narration 應壓縮並口語化的 spoken takeaway？
- voiceover writer 是否還需要自行解決時序、重點或語意含義上的歧義，而這些本應已在此文件中明確？

若 script 語意正確，但仍不足以支撐忠實 narration drafting，則修復留在 `SCRIPT`。
若 voiceover readiness 失敗的原因是已核准設計本身缺少或衝突了必要教學或交付決策，則回到 `DESIGN_DEVELOPMENT`。必須先設計修復、重新審查與重新核准，再重新產生並重新核准 brief。
若已核准設計清楚固定了所需的教學或交付決策，但 brief 轉譯錯誤，則回到 `CONTRACT`。修復並重新核准 brief，無需重新設計。

## 修復路由

### 留在 SCRIPT

當已核准 brief 清楚，而問題只限於：

- 較弱的 beat 結構
- 缺少 progress cues
- 模糊的 viewer goals
- 不清楚的 voiceover intent
- beat 尺寸過大，迫使單一 narration segment 跨越多個不同局部狀態轉換
- 不改變已凍結語意的排序或重點問題

### 回到 DESIGN_DEVELOPMENT

當失敗暴露：

- 已核准設計本身在演算法語意上有缺漏或衝突
- 已核准設計本身在主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線或高層節拍上有缺漏或衝突
- 已核准設計本身在交付決策上有缺漏或衝突
- 已核准設計本身在新暴露的高影響分歧上有缺漏或衝突

必須先設計修復、重新審查與重新核准，再重新產生並重新核准 brief。

### 回到 CONTRACT

當已核准設計清楚，但 `pre_build_brief.md` 有錯誤 wording 或 source labels，或是不忠實轉換時，使用此路徑。修復並重新核准 brief，無需重新設計。

## PASS 標準
- script 符合已核准 brief
- 每個 beat 都有具體教學目的
- script 中沒有隱藏未解決的語意歧義
- 下游 voiceover 與 render work 可在不猜測的情況下繼續
- `script_review_result.md` 由獨立 reviewer 撰寫，而非 script writer

## 常見失敗
- 可套用在多種衝突語意上的泛泛 beat prose
- 缺少 progress cues 或 viewer goals
- script 結構迫使 voiceover 發明新教學邏輯
- beat 結構粗到迫使下游推斷隱藏子節拍時序，或把 beat 過大當成 voiceover / render 的方便處理
- 本該升級處理的 brief 歧義，卻在 script 內被偷偷補掉
