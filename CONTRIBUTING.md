# 貢獻指南

感謝你協助改善 Manim Algorithm Animation Maker。本文件說明目前能接受的貢獻，以及提交變更時的注意事項。

## 可以貢獻的內容

- 修正安裝、使用或相容性文件。
- 改善既有 Skill workflow、references 或輔助 scripts。
- 改善演算法動畫設計指南，但不擴大目前 Skill 的適用範圍。

大型新功能或會改變 Skill contract 的提案，請先建立 Feature Request。這可以避免實作方向與目前維護範圍不一致。

## 開始修改

1. Fork 並 clone Repository。
2. 建立以變更目的命名的 branch。

## 修改 Skill 文件

- 保留 `SKILL.md` 的 YAML frontmatter 與 Skill 名稱。
- 修改 workflow 時，同步檢查對應 reference、subagent role 與輔助 scripts。
- 不要讓 writer 與 reviewer 變成同一個角色。
- 不要以 README 的簡短摘要取代 `SKILL.md` 或 references 中的完整 gate。
- 若改變必要輸入、輸出或 restart rule，Pull Request 必須清楚說明相容性影響。

## 不得提交的內容

請勿在 Pull Request 中提交憑證、私人設定、cache、TTS 音訊、Manim render output 或其他生成的大型媒體檔案。
