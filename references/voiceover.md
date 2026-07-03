# Voiceover

本文件定義 `algorithm-teaching-animation-v4` 中的 voiceover 工作。

當 narration 為必要且未明確核准其他語言時，預設 spoken language 為 English。Optional overlays 仍然是獨立且 opt-in 的。

## 目的

voiceover 應把已核准教學 script 轉成口語引導，並滿足以下要求：

- 聽起來自然
- 能逐 beat 同步
- 忠於已確認 brief

Voiceover 不允許靠即興補充新解釋來修補缺失語意。

## 開始 Gate

只有在以下條件成立後，才可開始 narration 工作：

- 已核准的 `pre_build_brief.md` 已存在
- `teaching_script.md` 已存在
- `script_review_result.md = PASS`

在 script review 通過前，不得開始任何 narration 工作。

## Delivery-Tier 預期

### No Narration

- 不需要 voiceover
- 保留已核准 `pre_build_brief.md` 中的 no-narration 決策
- 不要假裝一個文字很多的畫面可以取代清楚教學的無音訊版本

### Final Narrated Delivery

- 提供已核准的 spoken segments 與可用的音訊資產
- 最終交付結果必須可直接提供給觀眾播放

## 必要產物

當 tier 包含 voiceover 時，需產出：

- `voiceover.md` 作為逐 beat 腳本
- `narration_manifest.json` 作為 segment timing 與檔案參照
- `audio/voiceover/` 作為生成或錄製好的音訊檔

voiceover 必須忠於已核准 script 的 beat，而不是在本地自行發明新教學邏輯。

對 no-narration tiers，不要產出 `voiceover.md`、`narration_manifest.json`、音訊資產，或額外的狀態檔；請直接依賴已核准 `pre_build_brief.md` 來記錄這個明確 no-narration 決策。

## 建議結構

```md
# Voiceover

## Summary
- Language:
- Delivery tier:
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

## 來源契約

Narration 必須從以下來源導出：

- 已核准 `pre_build_brief.md`
- 已核准 `teaching_script.md`
- `script_review_result.md`

若 `script_review_result.md` 沒有通過，就應停止，回去修 script，而不是在歧義之上硬寫 narration。

若 narration 工作暴露出已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上有缺漏或衝突，則應回到 `DESIGN_DEVELOPMENT`；要求設計修復、重新審查與重新核准，再重新產生並重新核准 brief。

若已核准設計清楚，但 brief 有錯誤文字或來源標籤，或是不忠實轉換，則應回到 `CONTRACT` 做 brief 修復與重新核准，無需重新設計。

## 同步規則

- narration 開始前，visual focus 必須先建立起來
- beat 必須在 narration 結束前保持視覺一致
- verbose wording、壓縮問題、spoken pacing 與 narration-local timing 缺陷都留在 `VOICEOVER`
- 若已核准 beat 本身包含太多不同教學動作或決策，無法支撐單一一致 narration segment，則應回到 `SCRIPT`，在上游重構 beat
- 不要用畫面空白時間來掩飾薄弱的 voiceover 撰寫

## Provider 契約

任何 voiceover provider 都必須支援：

- 每個 beat 的 input narration text
- 每個 beat 的 output audio
- 每個 beat 的 duration reporting

不要把 secrets 存進 skill artifacts。

對 `final narrated delivery`，在 `RENDER` 與 `QA` 前，必須先具備可供觀眾使用的音訊資產。不要把真正的音訊檔產出延到 `QA`，也不要讓 narrated tiers 只剩規劃文件而沒有實際音訊。

## 常見失敗

- 太字面地照著 script 念，而不是為口說重寫。
- 用尚未審查的 script 就開始 narration，逼 voiceover 自己決定缺失的教學邏輯。
- 因 brief 太薄，就把新的語意解釋偷偷塞進 voiceover。
- 對 narrated tier 缺少音訊檔卻視為可接受。
- narration timing 漂移過大，導致畫面與語音不再對齊。
