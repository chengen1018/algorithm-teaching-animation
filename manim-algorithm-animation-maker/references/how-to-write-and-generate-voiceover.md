# 旁白撰寫與音訊生成

本文件用來把已通過審查的 `teaching_script.md` 轉成逐 beat 旁白與 Kokoro TTS 音訊。旁白語言以 `confirmed_requirements.md` 為準。

## 內容原則

- 忠於教學腳本的 beat、教學重點與順序，不新增教學邏輯。
- 使用自然、簡短、適合口說的句子；不要逐字朗讀像教科書的段落。
- 每個 beat 聚焦一個主要重點，並說明這一刻為什麼重要。
- 畫面焦點要先建立，旁白才開始；該 beat 的畫面狀態至少保留到旁白結束。
- 每個 Scene 4 complexity 結論都明確說出其對應 teaching script 的 case label，不以未核准 case 補充或替換結論。
- 旁白先說明分析模型，再說結論，例如「最壞情況時間複雜度為 O(n log n)」或「每次 append 的 amortized time complexity 為 O(1)」。
- 旁白依 Scene 4 beats 口語化 input size、主要工作與 work count，不能只念 O(...)。
- worst、average、expected 與 amortized 保持各自含義，不把 average 當成 expected，也不把單次 worst cost 當成 amortized cost。

旁白內容只從以下檔案導出：

- `confirmed_requirements.md`
- `animation_design.md`
- `teaching_script.md`

## 必要產物

- `voiceover.md`：逐 beat 的旁白文字。
- `narration_manifest.json`：beat、文字、音檔路徑與驗證結果。
- `audio/voiceover/`：Kokoro 生成的逐 beat WAV。

`voiceover.md` 使用以下結構：

```markdown
# Voiceover

## Summary
- Language:
- Source script:

## Beats

### beat-001: <beat title>
- Scene hook:
- Narration:
- Pacing target:
- Pronunciation notes: <只有需要時才填寫>
```

每個 beat id 必須與 `teaching_script.md` 對應，並在 `voiceover.md`、manifest 與音檔名稱中保持一致。

## Narration manifest

生成音訊前先建立：

```json
{
  "language": "zh",
  "beats": [
    {
      "id": "beat-001",
      "text": "<實際旁白>",
      "audio_path": "<absolute-project-root>/audio/voiceover/beat-001.wav"
    }
  ]
}
```

中文使用 `language: zh`，英文使用 `language: en`。`audio_path` 必須是絕對路徑。

## 生成與驗證

執行：

```bash
python <absolute-skill-root>/scripts/generate_voiceover_audio.py \
  --project-root <absolute-project-root> \
  --manifest <absolute-project-root>/narration_manifest.json
```

Helper 讀取 `<project-root>/.tts-config` 的 `TTS_PYTHON`，在該環境中呼叫 Kokoro：

- 中文：`zm_yunxi`，語言代碼 `z`
- 英文：`af_heart`，語言代碼 `a`

每個 WAV 必須可解碼、非空、非靜音，且時長合理。Helper 會把 duration、sample rate、channels、peak、RMS 與 validation result 寫回 manifest；任何 beat 驗證失敗時，整個命令都必須失敗。

## 常見問題

- 旁白逐字照念書面 script，聽起來不自然。
- 在旁白階段加入需求、設計或教學腳本沒有的解釋。
- beat id、manifest 項目與音檔名稱無法對應。
- 旁白開始時畫面焦點尚未建立，或音訊結束前畫面已切換。
- 音檔缺失、靜音或驗證失敗，卻仍把階段標記為完成。
