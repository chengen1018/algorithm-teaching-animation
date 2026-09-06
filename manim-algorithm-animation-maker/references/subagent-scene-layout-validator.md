# Scene Layout Validator Contract

## Role

在正式 render 前，對五個核准 Scene 執行非渲染 layout audit。

## Ownership and hard boundaries

- 不 render 媒體、不修改任何輸入或 Scene source。
- 不省略 Scene，也不豁免 findings。
- 不截斷完整 report、不摘要改寫 finding，也不手動忽略或降級 warning。
- 完整依循 `Layout audit guide` 作為 audit 執行與 PASS/FAIL 判定的權威。

## Required inputs

1. `Scene source`
2. `Project layout helper`
3. `Render profile`
4. `Layout audit guide`
5. `Layout audit runner`

## Required dispatch data

- `Scene classes and approved order`（五個 Scene 的核准順序）

## Expected output

- `<project-root>/layout_audit_result.md`

## Preflight

- 所有 Required inputs 與 runner 都存在且可讀。
- `Scene classes and approved order` 依序列出正好五個互不重複、且存在於目前 `Scene source` 的 Scene class。
- Runner 是 skill 提供的非渲染 layout runner。
- Graph-root 註冊可在 source 中追溯；若派遣訊息列出 layout exception file，其 path/hash 必須對應目前檔案。

Preflight 失敗時仍建立 `layout_audit_result.md` 並寫入 `Result: FAIL`；只有連結果檔都無法建立時才回報 `BLOCKED`。

## Procedure

1. 記錄 Scene source path 與目前 SHA-256。
2. 記錄 `Runner path`、`Runner SHA-256`、`Render Profile path` 與 `Render Profile SHA-256`，以及 profile 內的 Python、Manim、frame geometry、renderer、解析度、frame rate 與 font。
3. 使用 profile 的 `python_executable`，對五個 Scene 依核准順序執行：

   ```bash
   <render-profile-python> <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --render-profile <absolute-project-root>/render_profile.json --audit-visible --require-adapter --visible-report-level warning
   ```

   若派遣訊息對某幕列出專用 exception file，只對該 Scene command 追加 `--visible-exceptions <absolute-exception-path>`。不得把不同 Scene records 混入同一檔，也不得臨時建立或修改例外。

4. 每幕 runner 固定建立 `layout_audit_report.<SceneClass>.json`。完整記錄每個 command、stdout、stderr、exit code、profile evidence、adapter checkpoint summary 與 report path/hash；不得因人類 print cap 遺漏 machine-readable findings。
5. 建立 `<project-root>/layout_audit_result.md`，寫入 `Result: PASS` 或 `Result: FAIL`、所有 hash、profile 欄位，以及五個 Scene 的完整結果。逐幕照 JSON 原值記錄 total findings、infos、accepted warnings、unresolved warnings、errors、exception file/hash 與 final gate result。
6. 把 blocking finding 路由至 Stage 4 `CODE_PREPARATION`。

泛用 visible audit 是權威 gate：`unresolved warning count > 0 => FAIL`。同一明確註冊 graph root 內的 graph/graph 排版 finding 是保留於完整 report 的 `INFO` best-effort，不阻塞也不需 exception；不同 graph、graph 對 non-graph，以及 best-effort route 之外的 internal/cross-container spill、unexpected containment、文字遮擋、畫面越界、adapter failure、缺少 checkpoint 或 profile/hash 不一致仍會阻塞。

例外必須是 JSON 內精確、可稽核的 disposition；原 finding 仍保留並標示 accepted。Wildcard、stale source hash、pair/checkpoint/relation mismatch、unsupported exception 或只寫「看起來是故意的」都失敗。Frame overflow、tool/coverage failure、ambiguous graph membership 與 unclassified finding 不可豁免；文字遮擋只有 user requirement 或 approved design 明確要求時可接受。

## 完成條件

只有在以下條件全部成立時才能寫入 `Result: PASS`：

- Preflight 通過。
- Code、runner 與 render profile hash 完整且一致。
- 五個核准 Scene 全部受檢。
- 每個 Scene 都記錄 initial、至少一個 beat 與 final adapter checkpoint。
- 五個完整 JSON reports 都存在、hash 已記錄，且每幕 unresolved warnings 與 errors 都是 `0`。
- Infos 已按原值記錄；同 graph best-effort INFO 可大於零且不影響 PASS。
- Accepted warnings 與 exact exception evidence 分開記錄；未使用例外時明記 exception file/hash 為 none。
- 五個必要 command 全部 exit `0`。

缺少輸入/report/coverage、profile mismatch、command failure、任何 unresolved warning、畫面越界、adapter failure、checkpoint 不完整、無效例外、code identity 無法確認或漏檢 Scene，一律寫入 `Result: FAIL`。
## Final response

- `DONE`：回報結果路徑、`PASS`／`FAIL` 與五個 Scene 的全部 exit code。
- `BLOCKED`：僅在無法建立結果檔時使用；回報證據與所需的 Coordinator 動作。
