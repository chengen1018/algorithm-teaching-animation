# 本機跨平台 TTS 設計

## 目的

讓 `VOICEOVER` 階段能產生真正可使用的旁白，不需要 API 金鑰，也不會按次向雲端服務付費。方案必須支援 Windows 與 macOS、英文與中文普通話，並阻止靜音 placeholder 被誤判為已完成的旁白。

## 已確認決策

- 使用本機 Kokoro 模型作為主要 TTS provider。
- 在 `/Users/lichengen/Developer/Senior-project/animation/.tts-env/` 建立一套共用 TTS 環境，不隸屬於任何單一動畫專案。
- 每支動畫的旁白資產都保留在該動畫自己的資料夾中。
- 初次設定時下載模型與依賴；之後的旁白生成完全在本機執行，不使用 provider API 金鑰。
- 既有的 Manim 環境保持獨立。TTS 僅負責產生音訊；Manim 與 FFmpeg 仍分別負責畫面渲染與最終混音。
- 英文預設使用 Kokoro 的美式英文聲音 `af_heart`；中文普通話預設使用 `zm_yunxi`。一個旁白 beat 固定使用一種已設定的語言與聲音；單一 beat 的中英混讀不在第一版範圍內。

## 資料夾結構

```text
/Users/lichengen/Developer/Senior-project/animation/
├── .tts-env/                  # 共用的本機 Python 環境與 TTS 依賴
├── tts-samples/               # 可丟棄的英文、中文試聽 WAV
├── binary-search/
│   ├── narration_manifest.json
│   ├── audio/voiceover/       # 僅屬於此動畫的旁白資產
│   └── renders/
└── <其他動畫>/
    ├── narration_manifest.json
    ├── audio/voiceover/
    └── renders/
```

`.tts-env/`、模型快取、試聽 WAV 與渲染媒體都不得提交到 Git。要提交的是固定版本的安裝說明與產生器程式碼，讓 Windows 與 macOS 都能重現相同 provider。

## 元件與資料流

1. 每個動畫自己的 `narration_manifest.json` 提供依序排列的 beat ID、旁白文字、語言、聲音、目標時序與相對輸出路徑。
2. TTS 產生器在合成前驗證 manifest：beat ID 唯一且順序正確、旁白不為空、語言受支援、輸出路徑安全，且 provider／聲音設定已固定。
3. Kokoro 在動畫資料夾的 `audio/voiceover/` 中，為每個 beat 產生 PCM WAV。
4. 驗證器讀取音訊中繼資料與解碼後的取樣值，拒絕遺失、空白、無法解碼或實質靜音的檔案；每個 beat 都記錄時長、取樣率、聲道數、峰值與 RMS 音量。
5. 只有 manifest 中每個 beat 都有通過驗證的非靜音音檔時，此階段才成功；它會寫回包含實際時長的 manifest／報告。否則以非零狀態結束，`VOICEOVER` 仍視為未完成。
6. render／mux 步驟取用這些已驗證的檔案，依排程保留 beat 間的空白，產生完整旁白軌並以 AAC 混入最終 MP4。它必須確認影片仍是 1920x1080、60 fps，且包含非空的音訊串流。

## 失敗處理

- 缺少模型、依賴、語言套件或聲音：以安裝／設定錯誤失敗；絕不產生靜音計時檔。
- 合成失敗、輸出為空、解碼失敗、靜音或時長超出容許範圍：該 beat 與整個 `VOICEOVER` 階段均失敗。
- 旁白比畫面 beat 更長：回報精確的 beat ID 與實際時長。應在 `VOICEOVER` 修正文句或節奏；若該 beat 包含太多教學動作，則退回 `SCRIPT`。
- 不回退至作業系統內建語音：macOS `say` 與 Windows SAPI 在兩個平台會產生不同聲音與品質。
- 不自動回退至雲端：本設計必須免金鑰、免用量費。日後若加入雲端 provider，必須由使用者明確設定，不能暗中選用。

## 試用驗收

在正式整合 workflow 前，先建立共用 TTS 環境，並在 `tts-samples/` 產生一段短英文 WAV 與一段短中文普通話 WAV。確認兩檔都能解碼、不是靜音且有時長資訊。使用者實際聆聽後決定是否接受聲音品質。此試用不會修改既有動畫或 Manim 環境。

## 驗證要求

- 在 macOS 與 Windows 上使用相同、鎖定版本的依賴／模型與產生器指令。
- 每個音訊 beat 在交給 `RENDER` 前都必須通過驗證。
- 最終串流以 FFprobe 驗證：影片是 `1920x1080`、`60/1` fps；音訊存在且為 AAC；最終時長合理。
- 將每支動畫的驗證結果保留在該動畫資料夾，讓 QA 能追溯每段混入音訊的旁白資產與驗證結果。

## 非本次範圍

- 聲音克隆、自訂聲音訓練與自動挑選聲音。
- 單一 beat 內中英混讀。
- 在試用階段取代既有動畫 workflow，或變更任何已核准的視覺內容。
