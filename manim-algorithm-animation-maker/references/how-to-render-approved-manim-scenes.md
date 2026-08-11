# How to Render Approved Manim Scenes

這份文件只用於 `generated_algo_scene.py` 已通過 Stage 4 layout 與獨立 scene review 的最終渲染。程式碼尚未 PASS 時不得使用本流程產生 preview 或送審 MP4。正式 render、四個 Scene MP4、合併 MP4、`render_manifest.md` 與 `delivery_check_result.md` 全部屬於 Stage 5；不得用它們取代 Stage 4 的 layout gate。

## 渲染前資料

Stage 4 的 `Exit gate` 完成渲染前資格判定。協調者將 Stage 4 的四份 gate 證據、已核准的 source version，以及 `render_profile.json` 的絕對路徑與 SHA-256 直接交給 `scene_final_renderer`。

Stage 4 PASS 後若程式碼、上游契約、profile 或執行環境改變，必須依 `SKILL.md` 的回退規則重新取得適用的 Stage 4 gate。

## 渲染與合併

1. Handoff 必須列出四個 Scene class 與核准順序。使用 `render_profile.json` 的 Python、renderer、解析度與 frame rate 分別渲染四個 Scene，記錄每個實際 command 與 exit code。預設 command 形狀為：

   ```bash
   <profile-python> -m manim --renderer cairo -r 1920,1080 --fps 60 <absolute-scene-file> <SceneClass>
   ```
2. 依 render contract 順序以實際 concat input list 合併四個 Scene MP4，記錄 concat command、input list 與 exit code。
3. 渲染、concat 或建立 manifest 後不得修改 `generated_algo_scene.py`；任何程式碼變動都會使 Stage 4 與 Stage 5 evidence 失效。
4. 記錄四個 Scene、combined MP4、所有 commands 與核准 code hash 後，完整建立並凍結 `render_manifest.md`。只有凍結後才能執行 coordinator-owned `DELIVERY_CHECK`；check 不得補寫或改寫 manifest。
5. 若問題只涉及輸出、command、concat、manifest 或 media decode，且 code/profile 不變，留在 Stage 5 重建受影響輸出後重跑 `DELIVERY_CHECK`；若 code、profile 或上游契約改變，停止渲染並依 `SKILL.md` 回到對應的 Stage 4 或上游 Stage。

`DELIVERY_CHECK` 由 bundled helper 執行：

```bash
python <absolute-skill-root>/scripts/verify_delivery.py \
  --source <absolute-project-root>/generated_algo_scene.py \
  --profile <absolute-project-root>/render_profile.json \
  --manifest <absolute-project-root>/render_manifest.md \
  --output <absolute-project-root>/delivery_check_result.md
```

Helper 對五個 MP4 執行 `ffprobe`，對 combined MP4 執行完整 decode，並比對 streams、解析度、frame rate、duration、source hash 與 render profile hash。它只讀取 artifacts，不修改或重新編碼。

## `render_manifest.md`

四個 Scene 與 combined MP4 均完成後建立 `render_manifest.md`。所有 `<...>` placeholder 必須換成實際值；不可省略欄位、以相對路徑取代絕對路徑，或只記錄部分媒體。manifest 在 `FINAL_RENDER` 結束前必須完整填妥並凍結，不得包含需要 `DELIVERY_CHECK` 之後回填的結果欄位。

```markdown
# Render Manifest

## Approved Source and Stage 4 Gate
- Code path: `<absolute generated_algo_scene.py path>`
- Approved Code SHA-256: `<Stage 4 Exit gate 核准的 code hash>`
- Rendered Source Code SHA-256: `<本次實際渲染的相同 code hash>`
- Handoff path: `<absolute scene_code_review_handoff.md path>`
- Layout audit path: `<absolute layout_audit_result.md path>`
- Scene review path: `<absolute scene_review_result.md path>`
- Render Profile path: `<absolute render_profile.json path>`
- Render Profile SHA-256: `<approved profile hash>`

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

## Concat and Combined Output
- Concat input list path: `<absolute path>`
- Concat input list contents: `<four absolute MP4 paths in the approved order>`
- Exact concat command: `<actual complete command>`
- Concat exit code: `0`
- Combined MP4 path: `<absolute path>`
```

`render_manifest.md` 是 Stage 4 核准的 source/profile 與四個 Scene MP4、combined MP4 的版本綁定紀錄。完成後將它視為 immutable input；`DELIVERY_CHECK` 依 manifest 已列出的四個 Scene 與 combined MP4 執行技術檢查。Manifest 建立後如果程式碼、profile、manifest 本身或任一 MP4 重新產生，舊 delivery result 即失效。

## `delivery_check_result.md`

Coordinator 建立一份精簡結果檔，內容包含：

- 五個 MP4 的 `ffprobe` command、exit status、video/audio streams、解析度、frame rate 與 duration。
- combined MP4 的 `ffmpeg` decode command 與 exit status。
- 四個 Scene duration 總和與 combined duration comparison。
- 目前 source/profile SHA-256 與 manifest 記錄值的 comparison result。
- `Result: PASS` 或 `Result: FAIL`。

結果檔只記錄本節列出的技術檢查證據。
