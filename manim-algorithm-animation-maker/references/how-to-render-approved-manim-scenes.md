# How to Render Approved Manim Scenes

這份文件只用於 `generated_algo_scene.py` 已通過 Stage 4 layout 與獨立 scene review 的最終渲染。程式碼尚未 PASS 時不得使用本流程產生 preview 或送審 MP4。正式 render、四個 Scene MP4、合併 MP4、`render_manifest.md` 與 `rendered_media_validation_result.md` 全部屬於 Stage 5；不得用它們取代 Stage 4 的 layout gate。

## 渲染前關卡

執行第一個 Manim render command 前，必須全部確認：

- `scene_code_review_handoff.md`、`layout_audit_result.md` 與 `scene_review_result.md` 都存在。
- `layout_audit_result.md = PASS`，完整涵蓋核准順序的四個 Scene。
- `scene_review_result.md = PASS`。
- `generated_algo_scene.py` 的目前 SHA-256，handoff 的 `Code SHA-256`，layout result 的 `Audited Code SHA-256`，以及 review result 的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256` 完全一致。
- Stage 4 PASS 後程式碼、上游契約與 layout-affecting environment/profile（包括 Manim 版本、font、frame geometry、quality/profile）都沒有改變。

使用下列命令取得並保存 preflight evidence；所有路徑都必須是絕對路徑，hash 值以 64 個小寫 hexadecimal 字元記錄：

```bash
shasum -a 256 <absolute-project-root>/generated_algo_scene.py
manim --version
```

任一 hash、PASS status、Scene coverage 或 layout-affecting profile 不一致就停止，回到 Stage 4；不得以舊 PASS 渲染新程式碼或新 layout profile。

## 渲染與合併

1. four-scene contract 必須包含四個 Scene；使用上游核准的品質、畫面尺寸與 frame rate，依核准順序分別渲染四個 Scene。完整記錄每一個實際執行的 Manim command、stdout、stderr 與 exit code。
2. 確認四個 Scene MP4 都存在且非空檔案。每個檔案都取得 SHA-256、size、mtime、duration、resolution、frame rate、container/video/audio stream metadata。
3. 依核准順序以實際 concat input list 合併四個 Scene MP4，完整記錄 concat command、input list 與 stdout、stderr、exit code。
4. 確認最終 MP4 存在且非空檔案，並取得與各 Scene 相同的 hash 和 media metadata。
5. 渲染、concat 或建立 manifest 後不得修改 `generated_algo_scene.py`；任何程式碼變動都會使 Stage 4 與 Stage 5 evidence 失效。

對每個 Scene MP4 與 combined MP4，使用以下具體 evidence commands（以實際絕對 MP4 path 取代 placeholder）：

```bash
shasum -a 256 <absolute-mp4-path>
ffprobe -v error -show_format -show_streams -of json <absolute-mp4-path>
ffmpeg -v error -i <absolute-mp4-path> -f null -
```

`ffprobe` JSON 必須足以記錄 container、video codec、dimensions、frame rate、duration 與所有 audio stream 的 codec、channel/layout、sample rate、duration；`ffmpeg` decode 的完整 stdout、stderr 與 exit code 是 delivery QA evidence。`rendered_media_validator` 依 `subagent-rendered-media-validator.md` 對五個 MP4 重新執行其指定的 `ffprobe`、`ffmpeg` 與 SHA-256 commands，且不得修改或重編碼任何 artifact。

## 渲染失敗時

若問題只涉及輸出路徑、render command、concat、manifest、metadata 或 media decode，且可在不改動 `generated_algo_scene.py`、上游契約或 layout-affecting profile 的情況下修正，可留在 Stage 5。重新建立受影響的 MP4 與完整 `render_manifest.md`，再由 `rendered_media_validator` 對全部五個 MP4 完整執行 DELIVERY_QA。

若修復需要改動 `generated_algo_scene.py`，必須立即停止 Stage 5。任何程式碼變更都會使 handoff、layout result、scene review、render manifest 與 rendered-media result 失效；回到 Stage 4 `CODE_PREPARATION`，建立新 hash 並重新完成 layout audit 和獨立 review 後才能重新渲染。

若修復改變 layout-affecting environment/profile，回到 Stage 4 `LAYOUT_VERIFICATION`，使用相同目前 code hash 取得新的 layout PASS 與 scene review PASS，才可重做 Stage 5。

## `render_manifest.md`

四個 Scene 與 combined MP4 均完成後建立 `render_manifest.md`。所有 `<...>` placeholder 必須換成實際值；不可省略欄位、以相對路徑取代絕對路徑，或只記錄部分媒體。

```markdown
# Render Manifest

## Approved Source and Stage 4 Gate
- Code path: `<absolute generated_algo_scene.py path>`
- Current Code SHA-256: `<64-character hash>`
- Handoff path: `<absolute scene_code_review_handoff.md path>`
- Handoff Code SHA-256: `<64-character hash>`
- Layout audit path: `<absolute layout_audit_result.md path>`
- Layout audit status: `PASS`
- Layout-audited Code SHA-256: `<64-character hash>`
- Layout environment/profile: `<recorded Stage 4 layout-affecting environment and profile>`
- Scene review path: `<absolute scene_review_result.md path>`
- Review status: `PASS`
- Reviewed Code SHA-256: `<64-character hash>`
- Review Layout-audited Code SHA-256: `<64-character hash>`
- Preflight timestamp: `<ISO-8601 timestamp>`

## Render Profile
- Manim version: `<manim --version output>`
- Render profile/quality: `<approved profile>`
- Resolution: `<width>x<height>`
- Frame rate: `<frames per second>`
- Source command working directory: `<absolute path>`

## Scene Outputs
| Order | Scene | Exact Manim command | MP4 path | SHA-256 | Size (bytes) | Mtime (ISO-8601) | Duration (seconds) | Resolution | Frame rate | Container / video stream | Audio stream data |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `<Scene class>` | `<actual complete command>` | `<absolute path>` | `<64-character hash>` | `<integer>` | `<timestamp>` | `<number>` | `<width>x<height>` | `<fps>` | `<format and codec metadata>` | `<all audio stream metadata, or explicitly no audio stream>` |
| 2 | `<Scene class>` | `<actual complete command>` | `<absolute path>` | `<64-character hash>` | `<integer>` | `<timestamp>` | `<number>` | `<width>x<height>` | `<fps>` | `<format and codec metadata>` | `<all audio stream metadata, or explicitly no audio stream>` |
| 3 | `<Scene class>` | `<actual complete command>` | `<absolute path>` | `<64-character hash>` | `<integer>` | `<timestamp>` | `<number>` | `<width>x<height>` | `<fps>` | `<format and codec metadata>` | `<all audio stream metadata, or explicitly no audio stream>` |
| 4 | `<Scene class>` | `<actual complete command>` | `<absolute path>` | `<64-character hash>` | `<integer>` | `<timestamp>` | `<number>` | `<width>x<height>` | `<fps>` | `<format and codec metadata>` | `<all audio stream metadata, or explicitly no audio stream>` |

## Concat and Combined Output
- Approved Scene order: `1: <Scene 1>, 2: <Scene 2>, 3: <Scene 3>, 4: <Scene 4>`
- Concat input list path: `<absolute path>`
- Concat input list contents: `<four absolute MP4 paths in the approved order>`
- Exact concat command: `<actual complete command>`
- Concat stdout: `<complete captured stdout or referenced absolute log path>`
- Concat stderr: `<complete captured stderr or referenced absolute log path>`
- Concat exit code: `0`
- Combined MP4 path: `<absolute path>`
- Combined MP4 SHA-256: `<64-character hash>`
- Combined MP4 size (bytes): `<integer>`
- Combined MP4 mtime (ISO-8601): `<timestamp>`
- Combined MP4 duration (seconds): `<number>`
- Combined MP4 resolution: `<width>x<height>`
- Combined MP4 frame rate: `<fps>`
- Combined MP4 container / video stream: `<format and codec metadata>`
- Combined MP4 audio stream data: `<all audio stream metadata, or explicitly no audio stream>`

## Delivery QA
- Validator contract: `<absolute subagent-rendered-media-validator.md path>`
- Validation result path: `<absolute rendered_media_validation_result.md path>`
- Validation result: `<PASS or FAIL after validator completes>`
```

`render_manifest.md` 是唯一已通過 Stage 4 的 source version 與四個 Scene MP4、combined MP4 的版本綁定證據。manifest 建立後如果程式碼、layout-affecting profile 或任一 MP4 重新產生，舊 manifest 即失效；依上述 failure routing 重新建立有效 evidence，並重新執行 DELIVERY_QA。
