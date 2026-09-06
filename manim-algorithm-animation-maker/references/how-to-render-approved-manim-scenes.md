# How to Render Approved Manim Scenes

這份文件是 `scene_final_renderer` 的專業執行權威，只用於 `generated_algo_scene.py` 已通過 Stage 4 layout 與獨立 scene review 的最終渲染、合併、輸出修復與 manifest 建立。Coordinator-owned `DELIVERY_CHECK` 與跨階段回退以 `SKILL.md` 為權威。

## 渲染前資料

Renderer 只處理 Coordinator 依 `scene_final_renderer` Dispatch Profile 交付的 Stage-4-approved inputs 與 dispatch data；資格 gate 與跨階段回退見 `SKILL.md`。

## 渲染與合併

1. 依 `layout_audit_result.md` 所列順序，直接使用目前的 `generated_algo_scene.py` 與 `render_profile.json`，以 profile 的 Python、renderer、解析度與 frame rate 分別渲染五個 Scene，記錄每個實際 command 與 exit code。預設 command 形狀為：

   ```bash
   <profile-python> -m manim --renderer <profile-renderer> -r <profile-width>,<profile-height> --fps <profile-frame-rate> <absolute-scene-file> <SceneClass>
   ```
2. 依 render contract 順序以實際 concat input list 合併五個 Scene MP4，記錄 concat command、input list 與 exit code。
3. 在 manifest 凍結前確認 delivery set 是 six distinct MP4 artifacts：五個 Scene class 互不重複，五個 Scene MP4 的 resolved absolute path 互不重複，combined MP4 的 resolved absolute path 與所有 Scene MP4 都不同。
4. 渲染、concat 或建立 manifest 後不得修改 `generated_algo_scene.py`；任何程式碼變動都會使 Stage 4 與 Stage 5 evidence 失效。
5. 記錄五個 Scene、combined MP4 與所有 commands 後，完整建立並凍結 `render_manifest.md`。只有凍結後才能執行 coordinator-owned `DELIVERY_CHECK`；check 不得補寫或改寫 manifest。
6. 收到 output-only 修復的 `followup_task` 時，只重建訊息指定的受影響輸出，然後以目前六個 MP4 重建並凍結 manifest。若無法在保持 source、render profile 與 Stage 4 gate evidence 不變的前提下完成，回報 `BLOCKED`。

## `render_manifest.md`

五個 Scene 與 combined MP4 均完成後建立 `render_manifest.md`。所有 `<...>` placeholder 必須換成實際值；不可省略欄位、以相對路徑取代絕對路徑，或只記錄部分媒體。五個 Scene class 與六個 resolved MP4 paths 必須符合 six distinct MP4 artifacts 契約。manifest 在 `FINAL_RENDER` 結束前必須完整填妥並凍結，不得包含需要 `DELIVERY_CHECK` 之後回填的結果欄位。

```markdown
# Render Manifest

## Approved Source and Stage 4 Gate
- Code path: `<absolute generated_algo_scene.py path>`
- Layout audit path: `<absolute layout_audit_result.md path>`
- Scene review path: `<absolute scene_review_result.md path>`
- Render Profile path: `<absolute render_profile.json path>`

## Render Profile
- Render command working directory: `<absolute path>`
- Python executable: `<profile python_executable>`
- Manim version: `<profile manim_version>`
- Renderer: `<profile renderer>`
- Resolution: `<profile pixel_width>x<profile pixel_height>`
- Frame rate: `<profile frame_rate>`
- Font: `<profile font>`

## Scene Outputs
| Render order | Scene class | Exact Manim command | Exit code | MP4 path |
| --- | --- | --- | --- | --- |
| 1 | `<Scene class>` | `<actual complete command>` | `<actual exit code>` | `<absolute path>` |
| 2 | `<Scene class>` | `<actual complete command>` | `<actual exit code>` | `<absolute path>` |
| 3 | `<Scene class>` | `<actual complete command>` | `<actual exit code>` | `<absolute path>` |
| 4 | `<Scene class>` | `<actual complete command>` | `<actual exit code>` | `<absolute path>` |
| 5 | `<Scene class>` | `<actual complete command>` | `<actual exit code>` | `<absolute path>` |

## Concat and Combined Output
- Concat input list path: `<absolute path>`
- Concat input list contents: `<five absolute MP4 paths in the approved order>`
- Exact concat command: `<actual complete command>`
- Concat exit code: `0`
- Combined MP4 path: `<absolute path>`
```

`render_manifest.md` 記錄本次使用的 source/profile 路徑、五個 Scene MP4 與 combined MP4。Renderer 回報 `DONE` 時，manifest 必須已凍結；只有 Coordinator 對原本 Renderer 發送 output-only 修復的 `followup_task` 後，Renderer 才能用重建後的媒體替換並重新凍結 manifest。
