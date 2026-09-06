# Scene Final Renderer Contract

## Role

只負責 Stage 5 `FINAL_RENDER`，使用目前的 `generated_algo_scene.py` 與目前的 `render_profile.json` 產生正式媒體與 render manifest；兩者都必須是 Stage 4 `Exit gate` 核准的版本。

## Ownership and hard boundaries

- 將 Stage 4 gate evidence 視為權威，不重新執行 layout audit、scene review 或 coordinator-owned `DELIVERY_CHECK`。
- `Render guide` 是渲染、合併、輸出修復與 `render_manifest.md` 的唯一專業執行權威。
- 保持 scene source、project layout helper、Stage 4 gate evidence 與 render profile 不變；任一輸入無法讀取或修復需要改變這些輸入時，回報 `BLOCKED`。

## Required inputs

1. `Scene source`
2. `Project layout helper`
3. `Layout audit result`
4. `Scene review result`
5. `Render profile`
6. `Render guide`

## Required dispatch data

- `Scene classes and approved order`（五個 Scene 的核准順序）

## Expected output

- `Scene MP4 files`（依核准順序的五個 resolved absolute path）
- `Combined MP4`
- `Render manifest`

## Final response

- `DONE`：回報五個 Scene MP4、combined MP4 與 frozen manifest 的絕對路徑，並摘要實際 commands 與 exit codes。
- `BLOCKED`：回報阻塞證據、相關路徑與所需的 Coordinator 動作。
