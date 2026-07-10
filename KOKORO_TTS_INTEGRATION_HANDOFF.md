# Kokoro TTS Integration Handoff

## 交接目標

把已驗證的本機 Kokoro TTS 接入 `algorithm-teaching-animation-v4` 的正式 `VOICEOVER` 階段，讓每次動畫流程都產生真實旁白、驗證音檔，並在 `RENDER` 時將音訊混入最終 MP4。此工作尚未整合；目前只有本機 provider 與聲音選擇已完成驗證。

## 已完成

- macOS 已安裝 Homebrew Python 3.11.15，保留原本系統 Python 3.9.6。
- 共用 TTS 虛擬環境：`/Users/lichengen/Developer/Senior-project/animation/.tts-env/`。
- 環境內已安裝：Kokoro 0.9.4、PyTorch、Misaki 英文／中文支援、NumPy、SoundFile。
- Kokoro 英文與中文 pipeline 已實際初始化並生成 WAV。
- 預設聲音已由使用者確認：
  - 英文：`af_heart`，`lang_code='a'`
  - 中文普通話：`zm_yunxi`，`lang_code='z'`
- 所有試聽 WAV 都已驗證為 24,000 Hz、單聲道、16-bit PCM，且不是靜音。

## 現有試聽與工具

```text
/Users/lichengen/Developer/Senior-project/animation/
├── .tts-env/                         # 共用 Python 3.11 + Kokoro 環境
└── tts-samples/
    ├── generate_samples.py            # 英中試聽產生器
    ├── english.wav                    # af_heart
    ├── mandarin.wav                   # 早期中文試聽
    ├── validation.json
    ├── generate_mandarin_voice_samples.py
    └── mandarin-voices/
        ├── zm_yunxi.wav               # 使用者選定的中文預設
        └── validation.json
```

直接呼叫 TTS 環境時，必須使用：

```bash
/Users/lichengen/Developer/Senior-project/animation/.tts-env/bin/python
```

不要使用系統的 `python3`，因為它仍是 Python 3.9.6，而 Kokoro 0.9.4 需要 Python 3.10–3.12。

## 已確認的根因

此前旁白失敗有兩個獨立原因：

1. `VOICEOVER` 只建立了靜音計時 WAV，沒有呼叫任何真實 TTS provider。
2. `RENDER` 只合併視覺 MP4，沒有把 WAV 音軌 mux 到最終 MP4。

不得再把靜音 placeholder 視為完成的旁白。

## 必做整合

1. 在 `VOICEOVER` 實作可重複執行的 Kokoro 產生器：讀取 `narration_manifest.json`，逐 beat 依其語言與文字產生 WAV；英文使用 `af_heart`、中文使用 `zm_yunxi`。
2. 將實際生成結果寫回或另存 manifest 驗證資訊：每段必須包含實際時長、取樣率、聲道、peak 與 RMS。
3. 為每個 beat 強制驗證：檔案存在、可解碼、非空、非靜音、時長合理。任何失敗都讓 `VOICEOVER` 以非零狀態失敗；禁止 fallback 到靜音檔、OS 內建語音或雲端 provider。
4. 在 `RENDER` 建立完整音軌：依 manifest beat 時間保留間隔，將所有已驗證 WAV 排入時間軸；以 FFmpeg 產生 AAC 音軌並 mux 到最終 MP4。
5. 驗證最終 MP4：影像必須維持 1920x1080、60/1 fps；必須存在非空 AAC 音訊串流；總長度合理。
6. 更新 `SKILL.md`、`references/voiceover.md`、`agents/voiceover-manifest.md`，使 provider、預設聲音、驗證與 mux 成為流程的必要條件，而非慣例。
7. 為 Windows 撰寫一次性前置安裝說明：Python 3.11、專案外共用 `.tts-env`、Kokoro/Misaki/SoundFile 安裝；確保後續每次只使用共用環境，不修改 Manim 環境。

## 架構與流程要求

```text
審查通過的 teaching_script.md
  → narration_manifest.json
  → Kokoro 每 beat WAV
  → 音訊驗證報告
  → 合成完整旁白軌
  → FFmpeg AAC mux
  → 最終 MP4 stream 驗證
```

- 每個動畫仍在 `/Users/lichengen/Developer/Senior-project/animation/<animation-name>/` 下擁有自己的 manifest、`audio/voiceover/` 與 render；不要把各動畫的旁白混放於共用根目錄。
- 共用環境及模型只放一份在 `animation/.tts-env/`。
- 同一 beat 不要求中英混讀；一段固定一種語言與聲音。
- Kokoro 是本機推論；首次模型下載或模型快取檢查需要網路，但正式文字不會傳送到雲端 TTS API，也沒有 API 金鑰或按字費用。
- Windows 與 macOS 可能有極小的數值差異；固定 Python、Kokoro、聲音 ID 和輸出格式，並以音訊／串流驗證作為可重現保證。

## 相關文件

- `TTS_AUDIO_FIX_HANDOFF.md`：最初的影音修復問題與既有 Binary Search 產物。
- `docs/superpowers/specs/2026-07-10-local-cross-platform-tts-design.md`：跨平台 TTS 設計與預設聲音。
- `docs/superpowers/plans/2026-07-10-local-tts-pilot.md`：已完成的初始試用計畫；其中原先以系統 Python 建環境的指令已被 Python 3.11 安裝需求取代，請以本 handoff 的路徑為準。
- `docs/superpowers/specs/2026-07-10-mandarin-voice-audition-design.md`：中文聲音選擇與 `zm_yunxi` 決定。
- `docs/superpowers/plans/2026-07-10-mandarin-voice-audition.md`：八個中文聲音試聽的實作紀錄。

## 注意事項

- 目前工作區有使用者的未提交變更，包含 `SKILL.md`、`agents/scene-reviewer.md`、`agents/scene-writer.md`、`.codex/agents/` 與 render agent 文件。不要覆寫、還原或納入無關提交。
- 尚未授權任何雲端 API、付費服務或 API 金鑰。
- 開始整合前，依專案既有的 Superpowers 流程進行設計確認、計畫與驗證；本 handoff 只提供已確認的限制與實測結果。
