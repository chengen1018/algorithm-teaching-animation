# Dijkstra Algorithm Animation Package

本資料夾整理本次 Dijkstra 演算法教學動畫的製作檔案與最終影片。

## 最終影片

- 路徑：`video/dijkstra_algorithm_animation_1080p60.mp4`
- 規格：1920×1080、60 fps、H.264 + AAC、英文旁白
- 長度：316.55 秒
- SHA-256：`96aee3731a8177809c50a72ec0c8dfeaba7bf4c115d44c4124b60e819cfc7336`

## 資料夾內容

- `docs/`：需求、動畫設計、教學腳本、旁白、manifest、渲染預檢及審查結果。
- `source/`：Manim 場景程式與影片合併清單。
- `audio/voiceover/`：44 個英文旁白 AIFF 音訊。
- `video/scenes/`：六個獨立高品質 Scene 影片。
- `video/`：最終合併影片。
- `evidence/`：由最終高品質影片抽取的 17 張渲染證據；`archive/` 保存修復過程中的舊版影格，避免與正式證據混用。

## 審查狀態

- Animation design review：PASS
- Script review：PASS
- Scene review：PASS
- Final QA：未執行（依使用者要求）

相關原始產物已直接移入此資料夾，工作區根目錄不保留重複副本。Manim partial movie cache 不屬於交付產物，因此未納入。
