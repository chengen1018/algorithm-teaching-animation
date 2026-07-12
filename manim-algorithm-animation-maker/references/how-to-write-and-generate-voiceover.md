# Voiceover

本文件定義如何將已審查的教學腳本轉成實際可用的旁白音訊。

spoken language 由 `confirmed_requirements.md` 明確指定。

## 目的

voiceover 應把已核准教學 script 轉成口語引導，並滿足以下要求：

- 聽起來自然
- 能逐 beat 同步
- 忠於 script

Voiceover 不允許靠即興補充新解釋來修補缺失語意。

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
- `animation_design.md`
- `teaching_script.md`
- `script_review_result.md`

## 同步規則

- narration 開始前，visual focus 必須先建立起來
- beat 必須在 narration 結束前保持視覺一致
- verbose wording、壓縮問題、spoken pacing 與 narration-local timing 缺陷都留在 `VOICEOVER`
- 不要用畫面空白時間來掩飾薄弱的 voiceover 撰寫

## Provider 要求

任何 voiceover provider 都必須支援：

- 每個 beat 的 input narration text
- 每個 beat 的 output audio
- 每個 beat 的 duration reporting

不要把 secrets 存進 skill artifacts。

## 常見失敗

- 太字面地照著 script 念，而不是為口說重寫。
- 因需求或設計太薄，就把新的語意解釋偷偷塞進 voiceover。
- 缺少音訊檔卻視為可接受。
- narration timing 漂移過大，導致畫面與語音不再對齊。
