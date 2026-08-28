# 安全政策

## 支援範圍

安全修正會套用到目前 `main` 與最新發布版本。早期版本不保證收到回溯修正。

## 私密回報漏洞

請使用 GitHub 的 [Private Vulnerability Reporting](https://github.com/chengen1018/manim-algorithm-animation-maker/security/advisories/new) 提交安全問題。

請勿在公開 Issue、Discussion 或 Pull Request 中揭露尚未修正的漏洞、憑證、私人路徑或敏感資料。

回報內容請包含：

- 受影響的版本或 commit。
- 問題的影響與可行的攻擊情境。
- 最小重現步驟或概念驗證。
- 已知的緩解方式。
- 是否已經對外公開相關資訊。

維護者的目標是在 7 個工作天內確認收到回報。後續修正與公開時間會依問題影響，和回報者協調。

## 安全邊界

本專案會執行本機 Python、Manim、FFmpeg 與 TTS 工具。使用者仍需自行審查動畫專案中的程式碼與第三方依賴，不應對不受信任的檔案直接執行 render 或 scripts。
