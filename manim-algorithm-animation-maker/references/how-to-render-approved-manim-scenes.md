# How to Render Approved Manim Scenes

這份文件只用於 `generated_algo_scene.py` 已通過獨立程式碼審查後的最終渲染。程式碼尚未 PASS 時不得使用本流程產生 preview 或送審 MP4。

## 渲染前關卡

執行任何 Manim render command 前，必須全部確認：

- `scene_code_review_handoff.md` 存在。
- `scene_review_result.md = PASS`。
- `generated_algo_scene.py` 的目前 SHA-256，handoff 的 `Code SHA-256`，以及 review result 的 `Reviewed Code SHA-256` 完全一致。
- 程式碼在 reviewer 產出 PASS 後沒有再被修改。

任一 hash 不一致就停止，回到程式碼送審流程；不得以舊 PASS 渲染新程式碼。

## 渲染與合併

1. 使用上游要求的品質、畫面尺寸與 frame rate，依核准順序分別渲染六個 Scene。
2. 確認六個 Scene MP4 都存在且非空檔案。
3. 依核准順序合併六個 Scene MP4，建立最終合併 MP4。
4. 確認最終 MP4 存在且非空檔案，並記錄輸出資訊。
5. 不得在渲染或合併後偷改 `generated_algo_scene.py`。

## 渲染失敗時

若問題可在不改動 `generated_algo_scene.py` 的情況下解決，例如修正命令、輸出路徑或環境設定，可在保持 code hash 不變的前提下修復並重試。

若修復需要改動 `generated_algo_scene.py`，必須立即停止渲染。任何程式碼變更都會使舊 `scene_code_review_handoff.md` 與 `scene_review_result.md` 失效；必須更新程式碼、重新靜態 audit、建立新 handoff 並取得新 PASS，才能重新渲染。

## `render_manifest.md`

渲染成功後建立：

```markdown
# Render Manifest

## Approved Source
- Code path: `<generated_algo_scene.py 的路徑>`
- Code SHA-256: `<與 handoff 及 review result 一致的 SHA-256>`
- Review result: `<scene_review_result.md 的路徑>`
- Review status: `PASS`

## Render Outputs
| 順序 | Scene | MP4 路徑 | 最後修改時間 | 檔案大小 |
| --- | --- | --- | --- | --- |
| 1 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |
| 2 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |
| 3 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |
| 4 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |
| 5 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |
| 6 | `<Scene class>` | `<path>` | `<mtime>` | `<size>` |

## Combined Output
- Combined MP4: `<path>`
- MP4 last-write time: `<mtime>`
- MP4 size: `<size>`
```

`render_manifest.md` 是「已通過審查的程式碼」與「最終 MP4」之間的版本綁定證據。manifest 建立後如果程式碼或任何 MP4 重新產生，舊 manifest 即失效，必須依目前有效關卡重新建立。
