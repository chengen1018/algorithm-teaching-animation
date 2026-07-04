# Voiceover

本文件定義 `algorithm-teaching-animation-v4` 中的 voiceover 工作。

配音固定包含在成品中，spoken language 由 `confirmed_requirements.md` 明確指定。Optional overlays 仍然是獨立且 opt-in 的。

## 目的

voiceover 應把已核准教學 script 轉成口語引導，並滿足以下要求：

- 聽起來自然
- 能逐 beat 同步
- 忠於已確認需求、已核准設計與已審查 script

Voiceover 不允許靠即興補充新解釋來修補缺失語意。

## 開始 Gate

只有在以下條件成立後，才可開始 narration 工作：

- `confirmed_requirements.md` 已存在且明確記錄配音語言
- 已核准的 `animation_design.md` 已存在
- `teaching_script.md` 已存在
- `script_review_result.md = PASS`

在 script review 通過前，不得開始任何 narration 工作。

## 必要產物

必須產出：

- `voiceover.md` 作為逐 beat 腳本
- `narration_manifest.json` 作為 segment timing 與檔案參照
- `audio/voiceover/` 作為生成或錄製好的音訊檔

voiceover 必須忠於已核准 script 的 beat，而不是在本地自行發明新教學邏輯。

## 建議結構

```md
# Voiceover

## Summary
- Language:
- Source script:

## Beats

### beat-001: ...
- Scene hook:
- Narration:
- Pacing target:
- Pronunciation notes:
```

## Beat 規則

每個 beat-level voiceover 項目都應包含：

- 穩定的 beat id 或 title
- 它對應的 scene hook
- 實際 narration 文字
- pacing target
- 只有在必要時才加入 pronunciation notes

Narration 必須在觀眾即時聽一次時就能理解。

## 撰寫規則

- narration 必須忠於已核准 script
- 解釋這一刻為何重要，而不是只說看到了什麼
- 用已核准 narration language 中自然、簡短、適合口說的句子
- 每個 beat 優先保留一個主要 takeaway
- 若某一句聽起來像教科書段落，就重寫它

## 內容來源

Narration 必須從以下來源導出：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- 已審查的 `teaching_script.md`
- `script_review_result.md`

若 `script_review_result.md` 沒有通過，就應停止，回去修 script，而不是在歧義之上硬寫 narration。

若 narration 工作暴露配音語言等使用者需求記錄不準確，則應回到 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。

若 narration 工作暴露出已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍或使用者選定設計上有缺漏或衝突，則應回到 `DESIGN_DEVELOPMENT`；要求設計修復、重新審查與重新核准。

## 同步規則

- narration 開始前，visual focus 必須先建立起來
- beat 必須在 narration 結束前保持視覺一致
- verbose wording、壓縮問題、spoken pacing 與 narration-local timing 缺陷都留在 `VOICEOVER`
- 若已核准 beat 本身包含太多不同教學動作或決策，無法支撐單一一致 narration segment，則應回到 `SCRIPT`，在上游重構 beat
- 不要用畫面空白時間來掩飾薄弱的 voiceover 撰寫

## Provider 要求

任何 voiceover provider 都必須支援：

- 每個 beat 的 input narration text
- 每個 beat 的 output audio
- 每個 beat 的 duration reporting

不要把 secrets 存進 skill artifacts。

在 `RENDER` 與 `QA` 前，必須先具備可供觀眾使用的音訊資產。不要把真正的音訊檔產出延到 `QA`，也不要只留下規劃文件而沒有實際音訊。

## 常見失敗

- 太字面地照著 script 念，而不是為口說重寫。
- 用尚未審查的 script 就開始 narration，逼 voiceover 自己決定缺失的教學邏輯。
- 因需求或設計太薄，就把新的語意解釋偷偷塞進 voiceover。
- 缺少音訊檔卻視為可接受。
- narration timing 漂移過大，導致畫面與語音不再對齊。
