# 相容性說明

[返回 README](../README.md)

本文件記錄目前專案明確支援或已驗證的環境。沒有列出的平台不代表一定不能使用，但目前不宣稱已完成驗證。

Manim 與 Kokoro 可以使用不同的 virtual environment；請勿假設兩者必須安裝在同一個環境。

## 必要工具

| 工具 | 用途 | 備註 |
| --- | --- | --- |
| Codex | 載入並執行 Skill | 必須能使用 subagent |
| Manim Community | 建立及渲染 Scene | 實際 Python 路徑會寫入 `render_profile.json` |
| FFmpeg／FFprobe | 合併與驗證影片 | 必須能從命令列執行 |
| Kokoro 0.9.4 | 產生本機旁白 | 詳見 [Kokoro 設置](../KOKORO_SETUP.md) |
| 支援目標語言的字型 | 顯示畫面文字 | 字型必須能被 Manim runtime 解析 |

預設 render profile 為 1920×1080、60 fps、Cairo renderer。使用者可以在需求確認時指定其他輸出規格，但修改 profile 後必須依 Skill 規則重新執行相關驗證。

## 作業系統狀態

- macOS：目前主要開發與本機測試環境。
- Linux：預計可用於 GitHub Actions 的快速測試；正式 Manim／TTS 流程尚未宣稱完整驗證。
- Windows：Kokoro 文件提供 virtual environment 路徑範例；正式完整流程尚未宣稱驗證。

## 快速測試與完整動畫流程

`python3 scripts/check_repository.py` 只執行 Repository contract、Python source compilation 與單元測試。它不需要：

- 下載 Kokoro 模型。
- 呼叫付費 API。
- 執行正式 Manim render。
- 產生音訊或 MP4。

完整動畫流程另外需要 Manim、FFmpeg／FFprobe、可用字型、Kokoro 模型及足夠的本機運算資源。
