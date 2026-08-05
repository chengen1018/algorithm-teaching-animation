# How to Hand Off Scene Code for Review

這份文件說明 scene-writer 如何在執行任何 Manim render 之前建立 `scene_code_review_handoff.md`，交給獨立 scene-reviewer 進行程式碼審查。

`scene_code_review_handoff.md` 是程式碼交接紀錄，不做程式碼檢查，也不做畫面審查。scene-writer 的靜態 audit（例如物件碰撞、越界、生命週期與 peak state）依 `references/how-to-implement-and-verify-manim-scenes.md` 執行；獨立 scene-reviewer 另行審查程式碼。

## 交接時點

必須先完成整支 `generated_algo_scene.py` 與必要靜態 audit，才能建立 handoff。在 reviewer 對目前 code hash 產出 `scene_review_result.md = PASS` 之前，不得渲染單幕、preview、low-quality 版本或最終影片。

## 交接格式

請使用以下格式：

```markdown
# Scene Code Review Handoff

## Reviewed Source
- Code path: `<generated_algo_scene.py 的路徑>`
- Code SHA-256: `<檔案內容的 SHA-256>`
- Code last-write time: `<最後修改時間>`
- Code size: `<檔案大小>`

## Static Verification
- Full-file reread: `COMPLETE`
- Four-Scene stable-beat audit: `COMPLETE`
- Non-render checks: `<已執行的語法／靜態檢查與結果；沒有則填 N/A>`
- Manim render performed: `NO`

## Render Assumptions
| 問題或衝突 | 採用的保守做法 | 依據來源 |
| --- | --- | --- |
| `<只有非平凡解讀才填寫；沒有則填 N/A>` | `<對原教學內容影響最小的做法>` | `<requirements/design/script/voiceover 的路徑>` |
```

## 版本與失效規則

`Code SHA-256` 是程式碼審查與後續渲染的版本身分。scene-reviewer 必須將實際審查的 hash 寫進 `scene_review_result.md` 的 `Reviewed Code SHA-256`。

每次修改 `generated_algo_scene.py` 後，舊的 `scene_code_review_handoff.md` 與 `scene_review_result.md` 都失效，不論變更大小。scene-writer 必須重新執行受影響範圍的靜態 audit、更新 handoff 並取得新 PASS。

handoff 不得列出或要求本次程式碼的 MP4；MP4 只會在程式碼審查 PASS 後被產生。

## Render Assumptions 範圍

`Render Assumptions` 只記錄會影響畫面或教學呈現的非平凡解讀。一般配色、間距或程式組織不需要記錄。

遇到這類問題時，先找對應的負責來源：需求檔負責使用者限制；設計檔負責演算法與畫面意義；script 負責 beat 順序與教學焦點；旁白產物負責音訊與同步資料。根據該來源採用對原內容影響最小、最保守的做法，並交給 reviewer 確認。
