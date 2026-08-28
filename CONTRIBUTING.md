# 貢獻指南

感謝你協助改善 Manim Algorithm Animation Maker。本文件說明目前能接受的貢獻，以及提交變更前需要完成的檢查。

## 可以貢獻的內容

- 修正安裝、使用或相容性文件。
- 改善既有 Skill workflow、references 或輔助 scripts。
- 補充可以重現問題的單元測試。
- 改善演算法動畫設計指南，但不擴大目前 Skill 的適用範圍。

大型新功能或會改變 Skill contract 的提案，請先建立 Feature Request。這可以避免實作方向與目前維護範圍不一致。

## 開發環境

1. Fork 並 clone Repository。
2. 建立以變更目的命名的 branch。
3. 使用 Python 3.10、3.11 或 3.12。
4. 修改前先執行基線檢查：

```bash
python3 scripts/check_repository.py
```

快速檢查不會下載 TTS 模型，也不會執行 Manim render。

## 修改 Skill 文件

- 保留 `SKILL.md` 的 YAML frontmatter 與 Skill 名稱。
- 修改 workflow 時，同步檢查對應 reference、subagent role 與測試。
- 不要讓 writer 與 reviewer 變成同一個角色。
- 不要以 README 的簡短摘要取代 `SKILL.md` 或 references 中的完整 gate。
- 若改變必要輸入、輸出或 restart rule，Pull Request 必須清楚說明相容性影響。

## 不得提交的檔案

- `.tts-config`、`.env`、API keys 或其他憑證。
- `__pycache__`、virtual environment、cache 或暫存檔。
- Kokoro 產生的音訊。
- Manim `media/`、Scene MP4、合併影片或其他 render output。
- 含有本機絕對路徑或私人動畫專案內容的驗證紀錄。

README 使用的三張輕量 poster 是刻意維護的公開素材，不受上述完整影片限制。

## 測試

提交前執行：

```bash
python3 scripts/check_repository.py
```

若修改完整動畫流程，也應在適當的獨立動畫專案中執行相關 gate。不要將該專案的音訊、影片或私人設定提交到這個 Repository。

## Pull Request

- 一個 Pull Request 只處理一個清楚的目的。
- 說明問題、解法、測試方式與可能的相容性影響。
- 保持變更範圍精簡，不重構無關內容。
- 確認 GitHub Actions 全部通過。
- 回應 review，並在修改後重新執行受影響的測試。

提交 Pull Request 即表示你同意依本專案的 [MIT License](LICENSE) 提供該貢獻，並遵守 [行為準則](CODE_OF_CONDUCT.md)。
