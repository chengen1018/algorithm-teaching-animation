# How to Hand Off Scene Code for Review

這份文件說明 scene-writer 如何在 `CODE_PREPARATION` 中、執行任何 Manim render 之前建立 pre-render `scene_code_review_handoff.md`，交給 `scene_layout_validator` 與獨立 scene-reviewer 使用。

`scene_code_review_handoff.md` 是 pre-render 程式碼交接紀錄，不做程式碼檢查，也不做畫面審查。scene-writer 執行完整重讀與靜態 self-audit；`scene_layout_validator` 另行負責 mobject geometry；獨立 scene-reviewer 另行負責語意與程式碼責任。

## 交接時點

必須先完成整支 `generated_algo_scene.py` 與必要靜態 self-audit，才能建立 handoff。handoff 只屬於 `CODE_PREPARATION`，該模式只產出程式碼與 handoff，並必須記錄 `Manim render performed: NO`。在相同 code hash 的 layout audit 與 reviewer 都產出 `PASS` 前，不得渲染單幕、preview、low-quality 版本或最終影片。

## 交接格式

請使用以下格式：

```markdown
# Scene Code Review Handoff

## Reviewed Source
- Code path: `<generated_algo_scene.py 的路徑>`
- Code SHA-256: `<檔案內容的 SHA-256>`
- Code last-write time: `<最後修改時間>`
- Code size: `<檔案大小>`

## Approved Scene Order
| 核准順序 | Scene class |
| --- | --- |
| 1 | `<Scene class>` |
| 2 | `<Scene class>` |
| 3 | `<Scene class>` |
| 4 | `<Scene class>` |

## Render Profile
- Render Profile path: `<render_profile.json 的絕對路徑>`
- Render Profile SHA-256: `<檔案內容的 SHA-256>`

## Layout Audit Setup
- Registered graph roots: `<逐幕列出顯示期間 identity 穩定的 wrapper 與 optional log name；沒有則填 none；已退場 root 可列為 inactive>`
- Layout exception files by Scene: `<每幕專用 JSON 的絕對路徑；未使用則填 none>`
- Layout exception file SHA-256 values: `<逐檔目前 hash；未使用則填 none>`
- Exception supporting references: `<逐筆 requirement/design reference；未使用則填 none>`

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

`Code SHA-256` 是 Stage 4 審查、layout audit、精確 warning disposition 與後續渲染的程式碼版本身分。`Render Profile SHA-256` 是 layout 與 render 設定的版本身分。scene-reviewer 必須將實際審查的 code hash 寫進 `scene_review_result.md` 的 `Reviewed Code SHA-256`，並同時記錄 layout result 的 `Layout-audited Code SHA-256`；兩者與 handoff 及目前 source hash 必須相同。Layout result 與 render manifest 的 profile hash 也必須等於 handoff 與目前 `render_profile.json`。

每次修改 `generated_algo_scene.py` 或 `render_profile.json` 後，不論變更大小，舊的 `scene_code_review_handoff.md`、`layout_audit_result.md`、完整 visible reports、`scene_review_result.md`、四個 Scene MP4、合併 MP4、`render_manifest.md` 與 `delivery_check_result.md` 全部失效。Source 改變也會讓所有 source-hash-bound exceptions 失效。scene-writer 必須從 Stage 4 `CODE_PREPARATION` 重新執行靜態 audit、建立新 handoff 與新 hash，再依序取得四幕 layout PASS、獨立 scene review PASS、正式 render 與全新的 `DELIVERY_CHECK` PASS。

handoff 不得列出或要求本次程式碼的 MP4；MP4 只會在程式碼審查 PASS 後被產生。

## Render Assumptions 範圍

`Render Assumptions` 只記錄會影響畫面或教學呈現的非平凡解讀。一般配色、間距或程式組織不需要記錄。

遇到這類問題時，先找對應的負責來源：需求檔負責使用者限制；設計檔負責演算法與畫面意義；script 負責 beat 順序與教學焦點；旁白產物負責音訊與同步資料。根據該來源採用對原內容影響最小、最保守的做法，並交給 reviewer 確認。

Layout warning 不能只寫進 `Render Assumptions` 就視為通過。優先調整 layout；只有 confirmed user requirement 或 approved design 明確要求時，才建立 `layout-audit.md` 定義的 machine-readable exact exception，並在本節記錄檔案 hash 與 supporting reference。
