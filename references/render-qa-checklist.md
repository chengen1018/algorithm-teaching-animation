# Render QA 檢查表

本文件定義 `algorithm-teaching-animation-v4` 的最終 QA 流程。

scene review 要回答的是 scene implementation 是否忠實表達已確認需求、已核准設計與已審查 script。Render QA 要回答的是實際渲染輸出是否已安全可交付。

## 必要輸出

回傳 `qa_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- 審查結果必須由獨立 reviewer 撰寫
- reviewer 負責 `QA` gate
- 帶有證據的 findings
- 修復方向：`RENDER`、`VOICEOVER`、`SCRIPT`、`COLLECT_REQUIREMENTS` 或 `DESIGN_DEVELOPMENT`

若 `scene_review_result.md` 缺失或不是 `PASS`，則 `QA` 無法開始。在這種情況下，不得輸出 `qa_result.md`；必須回傳一份上游 gate-block 通知，指出造成阻塞的 scene-review 條件與其修復目標。若 `scene_review_result.md` 完全缺失，應以 `RENDER` 作為預設修復目標，以便完成 scene-review gate。

`QA` 是獨立 review gate。`qa_result.md` 必須由獨立 reviewer 撰寫，而非受審輸出的任何參與作者。

除非 `scene_review_result.md = PASS` 以明確檔案形式存在，否則不得開始 `QA`。失敗或缺失的 `scene_review_result.md` 會阻塞 `QA` 進入，這必須被當成上游 review gate，而不是轉換成一般 `QA` 判斷或偽造一份 `qa_result.md`。

## QA 輸入

審查時應對照：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- 已審查的 `teaching_script.md`
- `render_preflight.md`
- `scene_review_result.md`
- rendered media output
- 已核准的 `voiceover.md`、`narration_manifest.json` 與可用音訊資產
- 當 overlays 啟用時，對應的 overlay output

只有當 rendered media 是最新最終 render、`render_preflight.md` 的 Source Evidence 指向該 MP4，且 latest-render evidence 與 `scene_review_result.md = PASS` 也都對應該版本時，QA 才能審查並通過。任何 rerender 都會使先前的 preflight、latest-render evidence 與 `scene_review_result.md` 失效；在 QA 開始前，必須更新 preflight、重新準備 reviewer evidence，並讓獨立 scene reviewer 對新 MP4/版本給出新的 `PASS`。

## Narration 檢查

驗證：

- 所有必要音訊資產都存在
- narration language 符合 `confirmed_requirements.md`
- visual focus 與 voiceover 在每個 beat 上都保持對齊
- 結果品質足以交付，而不只是除錯用

## 核心檢查表

### Visual Readability

- 主要結構在整段過程中都可辨識
- 每個 beat 的 active focus 都很明顯
- settled 或 excluded 區域仍可區分
- labels 可讀且不互相碰撞
- 沒有重要內容被裁切或遮住
- 最終交付證據來自最新 render，而不是過期 review frames

### Source Fidelity

- render 符合已確認語意
- 當需要時，support structures 有出現
- 實作過程沒有新增新語意
- overlay 行為符合已核准設計或使用者明確要求

### Timing and Audio

- beat pacing 給觀眾足夠時間理解變化
- voiceover 在 visual hook 建立後才開始
- 長停頓必須有教學價值，而不是空氣時間
- narration 與畫面不互相矛盾

### Delivery Completeness

- 六個獨立 Scene 都已渲染，並依核准順序合併成一支完整影片
- 每個 Scene 邊界皆先淡出至空白，再淡入下一幕
- 所需檔案存在且可用
- 不會把 draft-quality narration 誤標為 final
- rendered media 是最新最終 render，`render_preflight.md` 的 Source Evidence 指向該 MP4，且 latest-render evidence 與 `scene_review_result.md = PASS` 也都對應該版本

## 修復方向

使用以下路徑：

- `stay within RENDER`：用於不改變已凍結語意的版面、間距、時序、樣式或忠實性修復
- `return to VOICEOVER`：當 QA 發現缺少音訊資產、錯誤語言 narration、narration 文字漂移，或根源於 narration 產物的音訊同步缺陷
- `return to SCRIPT`：當 QA 發現 render 無法單獨修正的 beat-structure mismatch
- `return to COLLECT_REQUIREMENTS`：當使用者需求遺漏、來源擷取不準確或語言記錄錯誤；修正後重新送入設計流程
- `return to DESIGN_DEVELOPMENT`：當已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍或使用者選定設計上有缺漏或衝突；必須設計修復、重新審查與重新核准

QA 不可默默重寫需求、設計或 script。
QA 不可透過自行給出通過，或把同一個被阻塞的工作改標成普通 `QA` 缺陷，來推翻失敗的 scene review。
若 `scene_review_result.md = PASS` 存在且證據新鮮，QA 不應重做 scene review；QA 應改為檢查交付安全性、產物完整性與最終輸出是否 ready。

## PASS 標準

只有在以下條件都成立時才能通過：

- `scene_review_result.md = PASS` 以明確檔案形式存在
- rendered media 是最新最終 render，`render_preflight.md` 的 Source Evidence 指向該 MP4，且 latest-render evidence 與 `scene_review_result.md = PASS` 也都對應該版本
- narration 與其他必要產物皆存在且可用
- render 可讀
- 已確認需求、已核准設計與已審查 script 被忠實實作
- 沒有任何仍對觀眾可見的未解決語意歧義
- `qa_result.md` 由獨立 reviewer 撰寫，而非任何參與該輸出的作者

## 常見失敗

- scene 在語意上正確，卻因視覺不可讀仍被通過。
- 把缺少音訊當成小備註。
- 在 QA 備註中即興發明新語意來補上游缺口。
- 因為演算法邏輯正確，就把 debug 品質 render 稱作「final」。
