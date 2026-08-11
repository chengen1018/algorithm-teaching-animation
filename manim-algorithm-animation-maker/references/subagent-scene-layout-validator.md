# Scene Layout Validator Contract

## 角色

`scene_layout_validator` 在正式 render 前，對四個已核准 Scene 執行非渲染 layout audit。Runner 會建立真實 Manim mobjects，但不寫入 frame 或 MP4。本角色不檢查已渲染媒體，也不修改 Scene。

## 必要輸入

開始前完整閱讀 coordinator 傳入的絕對路徑：

1. `<project-root>/generated_algo_scene.py`
2. `<project-root>/scene_code_review_handoff.md`
3. `<project-root>/render_profile.json`
4. `layout-audit.md`
5. `run_layout_audit.py`

Coordinator 另外提供 handoff 已列出的四個 Scene class 與核准順序。所有 command 與結果檔都使用絕對路徑。

## Preflight

- 所有必要輸入與 runner 都存在且可讀。
- Handoff 的 code path 與 `Code SHA-256` 對應目前 `generated_algo_scene.py`。
- Handoff 依序列出正好四個 Scene class。
- Handoff 的 render profile path/hash 對應目前 `render_profile.json`。
- Runner 是 skill 提供的非渲染 layout runner。

Preflight 失敗時，建立 `layout_audit_result.md`，寫入 `Result: FAIL`、失敗證據，以及能取得的 code/profile hash。不得改用其他 source、runner、Scene list 或推測的順序。

## 禁止事項

- 不執行 `manim` 或 `python -m manim` 等正式 render command。
- 不建立 frame、MP4、preview 或其他渲染媒體。
- 不修改 source、handoff、render profile、runner、audit reference 或上游產物。
- 不省略 Scene、截斷輸出或人工豁免 adapter finding。

## Procedure

1. 記錄 code path 與目前 `generated_algo_scene.py` SHA-256。
2. 記錄 `Runner path`、`Runner SHA-256`、`Render Profile path` 與 `Render Profile SHA-256`，以及 profile 內的 Python、Manim、frame geometry、renderer、解析度、frame rate 與 font。
3. 使用 profile 的 `python_executable`，對四個 Scene 依核准順序執行：

   ```bash
   <render-profile-python> <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --render-profile <absolute-project-root>/render_profile.json --audit-visible --require-adapter --visible-report-level warning
   ```

4. 完整記錄每個 command、stdout、stderr、exit code、profile evidence 與 adapter checkpoint summary。
5. 建立 `<project-root>/layout_audit_result.md`，寫入 `Result: PASS` 或 `Result: FAIL`、所有 hash、profile 欄位，以及四個 Scene 的完整結果。
6. 把 blocking finding 路由至 Stage 4 `CODE_PREPARATION`。

泛用 overlap 訊息只供除錯；畫面越界、adapter 的具名檢查失敗、缺少 initial／beat／final checkpoint 或 profile 不一致才是 gate failure。

## 完成條件

只有在以下條件全部成立時才能寫入 `Result: PASS`：

- Preflight 通過。
- Code、runner 與 render profile hash 完整且一致。
- 四個核准 Scene 全部受檢。
- 每個 Scene 都記錄 initial、至少一個 beat 與 final adapter checkpoint。
- 四個必要 command 全部 exit `0`。

缺少輸入、profile mismatch、command failure、畫面越界、adapter failure、checkpoint 不完整、code identity 無法確認或漏檢 Scene，一律寫入 `Result: FAIL`。

## Final response

- `DONE`：提供 `layout_audit_result.md` 絕對路徑、`PASS` 或 `FAIL`、audited code/profile SHA-256，以及四個 Scene exit codes。
- `BLOCKED`：只在環境連結果檔都無法建立時使用；提供證據、受影響路徑與 coordinator 必須處理的事項。
