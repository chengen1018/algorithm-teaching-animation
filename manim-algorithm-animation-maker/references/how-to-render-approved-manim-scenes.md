# How to Render Approved Manim Scenes

這份文件只用於 `generated_algo_scene.py` 已通過 Stage 4 layout 與獨立 scene review 的最終渲染。程式碼尚未 PASS 時不得使用本流程產生 preview 或送審 MP4。正式 render、四個 Scene MP4、合併 MP4、`render_manifest.md` 與 `delivery_check_result.md` 全部屬於 Stage 5；不得用它們取代 Stage 4 的 layout gate。

## 渲染前資料

Stage 4 的 `Exit gate` 是唯一的渲染前 gate。協調者將 Stage 4 的四份 gate 證據、已核准的 source version 與 render profile 直接交給 `scene_final_renderer`；本文件不再建立第二份 `Entry gate`，也不要求在第一個 render command 前重做相同的 hash、PASS 或 environment preflight。

Stage 4 PASS 後若已知程式碼、上游契約或 layout-affecting environment/profile 改變，必須依 `SKILL.md` Stage 4 的回退規則重新取得 gate；不能在 Stage 5 以臨時 preflight 取代回退流程。

## 渲染與合併

1. four-scene contract 必須包含四個 Scene；使用上游核准的品質、畫面尺寸與 frame rate，依 render contract 順序分別渲染四個 Scene。記錄每一個實際執行的 Manim command 與 exit code。
2. 依 render contract 順序以實際 concat input list 合併四個 Scene MP4，記錄 concat command、input list 與 exit code。
3. 渲染、concat 或建立 manifest 後不得修改 `generated_algo_scene.py`；任何程式碼變動都會使 Stage 4 與 Stage 5 evidence 失效。
4. 記錄四個 Scene、combined MP4、所有 commands 與核准 code hash 後，完整建立並凍結 `render_manifest.md`。只有凍結後才能執行 coordinator-owned `DELIVERY_CHECK`；check 不得補寫或改寫 manifest。
5. 若問題只涉及輸出、command、concat、manifest 或 media decode，且 code/profile 不變，留在 Stage 5 重建受影響輸出後重跑 `DELIVERY_CHECK`；若 code、profile 或上游契約改變，停止渲染並依 `SKILL.md` 回到對應的 Stage 4 或上游 Stage。

`DELIVERY_CHECK` 使用以下低成本 commands（以實際絕對路徑取代 placeholder）：

```bash
ffprobe -v error -show_format -show_streams -of json <absolute-mp4-path>
ffmpeg -v error -i <absolute-combined-mp4-path> -f null -
shasum -a 256 <absolute-project-root>/generated_algo_scene.py
```

`ffprobe` 對五個 MP4 的 exit status 是主要媒體檢查；它同時隱含檢查檔案存在、非空與可解析性。`ffmpeg` 只對 combined MP4 執行 decode，確認合併成品可讀取；兩者都不得修改或重編碼任何 artifact。

## `render_manifest.md`

四個 Scene 與 combined MP4 均完成後建立 `render_manifest.md`。所有 `<...>` placeholder 必須換成實際值；不可省略欄位、以相對路徑取代絕對路徑，或只記錄部分媒體。manifest 在 `FINAL_RENDER` 結束前必須完整填妥並凍結，不得包含需要 `DELIVERY_CHECK` 之後回填的結果欄位。

```markdown
# Render Manifest

## Approved Source and Stage 4 Gate
- Code path: `<absolute generated_algo_scene.py path>`
- Approved Code SHA-256: `<the single hash approved by the five-way Stage 4 gate>`
- Rendered Source Code SHA-256: `<the same immutable hash supplied by the Stage 4 Exit gate>`
- Handoff path: `<absolute scene_code_review_handoff.md path>`
- Layout audit path: `<absolute layout_audit_result.md path>`
- Scene review path: `<absolute scene_review_result.md path>`
- Render profile: `<approved profile>`

## Render Profile
- Render command working directory: `<absolute path>`
- Render profile/quality: `<approved profile>`

## Scene Outputs
| Render order | Scene | Exact Manim command | MP4 path |
| --- | --- | --- | --- |
| 1 | `<Scene class>` | `<actual complete command>` | `<absolute path>` |
| 2 | `<Scene class>` | `<actual complete command>` | `<absolute path>` |
| 3 | `<Scene class>` | `<actual complete command>` | `<absolute path>` |
| 4 | `<Scene class>` | `<actual complete command>` | `<absolute path>` |

## Concat and Combined Output
- Concat input list path: `<absolute path>`
- Concat input list contents: `<four absolute MP4 paths in the approved order>`
- Exact concat command: `<actual complete command>`
- Concat exit code: `0`
- Combined MP4 path: `<absolute path>`
```

`render_manifest.md` 是唯一已通過 Stage 4 的 source version 與四個 Scene MP4、combined MP4 的版本綁定紀錄。完成後將它視為 immutable input；`DELIVERY_CHECK` 只讀取 manifest 的 source hash 與輸出路徑，不做 Scene 順序的獨立 assertion。manifest 建立後如果程式碼、layout-affecting profile、manifest 本身或任一 MP4 重新產生，舊 delivery result 即失效；依上述 failure routing 重新建立、重新凍結有效 evidence，並執行全新的 `DELIVERY_CHECK`。

## `delivery_check_result.md`

Coordinator 建立一份精簡結果檔，內容包含：

- 五個 MP4 的 `ffprobe` command 與 exit status。
- combined MP4 的 `ffmpeg` decode command 與 exit status。
- 目前 `generated_algo_scene.py` SHA-256、manifest approved/rendered source hash 與 comparison result。
- `Result: PASS` 或 `Result: FAIL`。

不記錄或執行 Scene 順序的獨立檢查，也不派遣額外 media-validator agent。
