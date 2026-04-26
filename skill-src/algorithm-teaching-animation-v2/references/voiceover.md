# Voiceover

本文件定義 `algorithm-teaching-animation-v2` skill 中 `voiceover.md`、`narration_manifest.json` 與 beat-level 旁白音訊的角色、格式與撰寫原則。

v2 的完整 workflow 預設產出旁白音訊，而不是畫面字幕。字幕只有在使用者明確要求時才產出。

## 核心目的

旁白層的責任，是把 `teaching_script.md` 中每個教學 beat 轉成自然、可說、可同步的英文講解，並產生可供 Manim 或後製流程使用的音訊對齊資料。

它的主要目的包括：

- 讓完整 workflow 具備實際 voiceover audio
- 讓旁白與 `teaching_script.md` 的 beat 結構對齊
- 讓每段音訊能回對到 trace mapping
- 讓 Manim scene 依照旁白長度安排 beat duration
- 避免把演算法說明臨時塞進 Manim 層

## 產出物

### `voiceover.md`

beat 對齊的英文旁白稿。它是 TTS 或錄音流程的文字來源。

### `narration_manifest.json`

旁白同步 manifest。它是 Manim translation 與 review 階段判斷音訊對齊的結構化輸入。

建議格式：

```json
{
  "language": "en",
  "audio_mode": "voiceover",
  "segments": [
    {
      "beat_id": "beat-001",
      "trace_mapping": "actions 1-3",
      "text": "We start with the original array so every later change has a clear reference point.",
      "audio_path": "audio/voiceover/beat-001.wav",
      "duration_seconds": 3.2
    }
  ]
}
```

### `audio/voiceover/*.wav`

beat-level 旁白音訊。每個 beat 通常對應一個 WAV 檔，檔名應和 `narration_manifest.json` 的 `beat_id` 可穩定對應。

### `tts_config.json`

選配的專案層設定檔，用於記錄本次使用的 TTS provider 名稱、voice id、語速、輸出格式等非機密設定。不要把 API keys、tokens 或 secrets 寫入此檔。

## `voiceover.md` 建議格式

```md
# Voiceover

## Summary
- Language: en
- Voice style: clear teaching voice
- Source: condensed from teaching_script.md
- TTS provider: configurable

## Beats

### beat-001: Establish the input
- Trace mapping: `actions 1-3`
- Narration:
  We start with the original array so every later change has a clear reference point.
- Pacing: 2.5-3.5 seconds
- Pronunciation notes: none

### beat-002: Compare the middle value
- Trace mapping: `actions 4-6`
- Narration:
  The middle value is checked first. This lets binary search decide which half can still contain the target.
- Pacing: 4-5 seconds
- Pronunciation notes: say "binary search" as two words
```

## 每個 beat 的必要欄位

- `beat_id` 或 beat title：必須能穩定回對 `teaching_script.md`
- `Trace mapping`：必須能回對 `action_trace.json` 中的一段 action 或一組 action
- `Narration`：實際要送進 TTS 或錄音的英文旁白文字
- `Pacing`：預期音訊長度或節奏範圍
- `Pronunciation notes`：只有在術語、變數名稱或容易唸錯的內容需要指定時才填

## 撰寫原則

- 旁白必須忠於 `teaching_script.md`
- 旁白不可加入 trace、plan 或 teaching script 沒有支撐的新演算法內容
- 每個 beat 通常 1 到 3 句
- 優先說明「現在發生什麼」與「為什麼這一步重要」
- 避免照讀畫面上看得到的狀態
- 避免公式推導稿、論文式語氣或過長定義
- 若一句話需要太多逗號或子句，通常應拆短
- 若旁白太長到需要畫面停很久，優先回修 `voiceover.md` 或拆分 beat

## TTS Provider Contract

TTS provider 是可插拔的。skill 不綁定特定廠商或本機工具，但完整 narrated delivery 必須有可用 provider。

最小 provider contract：

- 輸入：單一 beat 的英文旁白文字
- 輸入：輸出音訊路徑，例如 `audio/voiceover/beat-001.wav`
- 輸出：一個可播放的 WAV 檔
- 輸出：該音訊檔的 duration，寫入 `narration_manifest.json`

若沒有可用 TTS provider，應停下來要求使用者設定 provider。不要把只有 `voiceover.md` 的結果宣稱為 narrated final delivery。

## 與其他文件的關係

- `plan.md`  
  定義教學目標、觀眾程度、不變量與 beat 策略。

- `teaching_script.md`  
  是旁白的主要來源；若旁白需要新教學內容，先回修這裡。

- `action_trace.json`  
  提供每個 beat 必須能對齊的演算法事件事實。

- `generated_algo_scene.py`  
  依據 `narration_manifest.json` 播放音訊並安排 beat duration。

- `subtitle_script.md`  
  只有使用者明確要求畫面字幕時才產出；字幕不得取代 voiceover。

## 常見錯誤

### 錯誤 1：把 teaching narration 原封不動拿去配音

問題：

- teaching script 可能適合閱讀，但不一定適合口說
- TTS 會顯得冗長、不自然或節奏拖慢

正確方向：

- 將每個 beat 收斂成自然英文口說
- 保留教學意義，刪掉不必要的書面語

### 錯誤 2：旁白補了畫面沒有支撐的新結論

問題：

- 觀眾聽到的內容無法從畫面或 trace 核對
- Manim 層可能被迫硬補不存在的演算法事件

正確方向：

- 回修 `teaching_script.md` 或 trace
- 再重新產生 voiceover

### 錯誤 3：沒有 TTS provider 卻宣稱完成有聲影片

問題：

- 只有文字稿不是 narrated final delivery

正確方向：

- 明確標示目前只完成 voiceover script
- 要求設定 provider 後再產生音訊與 manifest

