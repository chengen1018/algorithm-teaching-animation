# How to Hand Off a Render for Review

這份文件說明 scene-writer 如何建立 `render_review_handoff.md`，交給獨立 scene reviewer 使用。

`render_review_handoff.md` 是簡短交接紀錄，不做程式碼檢查，也不做畫面審查。scene-writer 的程式碼靜態 audit（例如物件碰撞、越界、生命週期與 peak state）依 `references/how-to-implement-and-verify-manim-scenes.md` 執行。實際影片、影格與畫面品質由獨立 scene-reviewer 審查。

請求 scene review 前，請建立 `render_review_handoff.md`，並使用以下格式：

```markdown
# Render Review Handoff

## Source Evidence
- Six Scene MP4s: `<依核准順序列出六個檔案路徑>`
- Combined MP4: `<合併影片路徑>`
- MP4 last-write time: `<最後修改時間>`
- MP4 size: `<檔案大小>`

## Render Assumptions
| 問題或衝突 | 採用的保守做法 | 依據來源 |
| --- | --- | --- |
| `<只有非平凡解讀才填寫；沒有則填 N/A>` | `<對原教學內容影響最小的做法>` | `<requirements/design/script/voiceover 的路徑>` |
```

`Source Evidence` 用來讓 reviewer 確認交接的是哪一版 MP4。每次 rerender 後，都要更新其中的檔案路徑、最後修改時間與檔案大小；舊 handoff 不可用於新版本。

`Render Assumptions` 只記錄會影響畫面或教學呈現的非平凡解讀，例如上游文件有缺口或彼此衝突時所做的選擇。一般配色、間距或程式組織不需要記錄。

遇到這類問題時，先找對應的負責來源：需求檔負責使用者限制；設計檔負責演算法與畫面意義；script 負責 beat 順序與教學焦點；旁白產物負責音訊與同步資料。根據該來源採用對原內容影響最小、最保守的做法，並繼續渲染。
