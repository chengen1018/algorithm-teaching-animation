# 變更紀錄

本文件記錄使用者可見的重要變更。版本規則以 [Semantic Versioning](https://semver.org/) 為基礎。

## [0.1.0] - 2026-08-28

第一個公開版本。

### 新增

- 五階段 Manim 演算法教學動畫工作流程。
- 動畫設計、腳本、旁白、Scene 實作、版面檢查、正式渲染與交付驗證規格。
- 八種明確分工的 subagent roles 與委派協定。
- Kokoro TTS 本機旁白產生與音訊驗證工具。
- Render profile、非渲染 layout audit 與 MP4 delivery verification scripts。
- Quick Sort、Longest Common Subsequence 與 Johnson Algorithm 三支公開示範影片。
- 繁體中文 README、安裝文件、相容性說明與開源貢獻文件。
- GitHub Actions 快速檢查。

### 已知限制

- 正式 Manim render 與 Kokoro TTS 不在快速 CI 中執行。
- 目前主要在 macOS 開發；Windows 與 Linux 的完整動畫流程尚未宣稱完成驗證。
- 產生動畫需要使用者明確同意使用 subagent。

[0.1.0]: https://github.com/chengen1018/manim-algorithm-animation-maker/releases/tag/v0.1.0
