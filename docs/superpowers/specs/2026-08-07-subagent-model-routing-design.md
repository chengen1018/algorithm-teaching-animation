# Sub-Agent 模型路由設計

## 目標

讓 `manim-algorithm-animation-maker` 在每次派遣 Sub-Agent 時，依角色穩定使用指定的 GPT-5.6 模型與推理強度，同時保留為可從 GitHub 取得並套用到其他動畫專案的配置。

指定策略如下：

| 階段 | Sub-Agent | 模型 | 推理強度 |
| --- | --- | --- | --- |
| 1 | `animation_design_reviewer` | `gpt-5.6-luna` | `xhigh` |
| 2 | `script_writer` | `gpt-5.6-sol` | `high` |
| 2 | `script_reviewer` | `gpt-5.6-luna` | `xhigh` |
| 3 | `voiceover_generator` | `gpt-5.6-luna` | `xhigh` |
| 4 | `scene_writer` | `gpt-5.6-sol` | `high` |
| 4 | `scene_layout_validator` | `gpt-5.6-luna` | `xhigh` |
| 4 | `scene_reviewer` | `gpt-5.6-luna` | `xhigh` |
| 5 | `scene_final_renderer` | `gpt-5.6-luna` | `xhigh` |

## 核心決策

在 repository root 建立可追蹤的 `.codex/config.toml`，與 `manim-algorithm-animation-maker/`、`kokoro setup/`、`Docs/` 同層。它是動畫專案的 Codex runtime 設定範本，不是 Skill 內部資源，也不放在 `manim-algorithm-animation-maker/.codex/`。

```text
Manim Algorithm Animation Maker/
├── .codex/
│   └── config.toml
├── manim-algorithm-animation-maker/
├── kokoro setup/
└── Docs/
```

設定內容：

```toml
[agents]
enabled = true
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "xhigh"
```

Repository 使用者要在另一個目錄產生動畫時，應將 `.codex/` **複製**到該動畫專案的根目錄，再從該根目錄開啟新的 Codex task。若直接移動 Git 所追蹤的範本，原 repository 會出現刪除變更，因此只有在不需要保留本地範本時才移動。

`.codex/config.toml` 只影響以其所在專案為根目錄或位於其子目錄中的 Codex task；它不會因 Skill 安裝而自動套用到任意專案，也不會在既有 task 中保證熱載入。

因為 repository root 的設定本身會生效，未來若從本 repository 開啟新的 Codex task，該 task 派遣的所有未顯式覆寫 Sub-Agent 也會繼承 Luna／xhigh；這不只影響動畫生成流程。這是使用可直接複製之實際 `config.toml`（而非停用的 example 檔）所接受的 repository-wide 行為。

## 模型解析與派遣契約

目前派遣介面能明確傳入 `gpt-5.6-sol`，但未在本次 runtime 的顯式 model override 清單中提供 `gpt-5.6-luna`。因此採用兩層解析：

1. Luna 角色派遣時不傳 `model` 或 `reasoning_effort`，由目標專案 `.codex/config.toml` 繼承 `gpt-5.6-luna` 與 `xhigh`。
2. `script_writer` 與 `scene_writer` 派遣時明確傳入 `model = "gpt-5.6-sol"`、`reasoning_effort = "high"`，覆寫專案預設值。

`references/subagent-delegation-protocol.md` 成為模型路由的唯一權威來源。角色對應表增加 `model source`、`model` 與 `reasoning effort`，並要求協調者在每次派遣前依表設定。`SKILL.md` 的各階段只指出 task name、角色與必要輸入，不重複整張模型表。

派遣訊息不宣稱或模擬模型選擇；模型與推理強度必須由真正的派遣參數或 project config 決定。

## Project config preflight

在第一次派遣任何 Sub-Agent 前，協調者必須確認本次動畫 project root 下存在 `.codex/config.toml`，且 `[agents]` 至少包含：

- `default_subagent_model = "gpt-5.6-luna"`
- `default_subagent_reasoning_effort = "xhigh"`
- `enabled` 未被設為 `false`

如果設定不存在、無法解析或值不同，流程回報 `BLOCKED`，說明必須把 repository 提供的 `.codex/` 複製到動畫 project root，並從該目錄建立新的 Codex task。協調者不得在動畫工作流程中自行覆寫使用者既有的 project config。

若 runtime、登入身分或 Workspace policy 不允許 Luna，派遣失敗時同樣回報 `BLOCKED`。不得靜默改用 Terra、Sol、parent model 或其他 fallback。

## Stage 5 角色分離

目前 Stage 5 再次派遣 `scene_writer` 的設計與模型表衝突，因為 `scene_writer` 在 Stage 4 必須使用 Sol／high，而正式渲染必須使用 Luna／xhigh。

新增獨立 task name `scene_final_renderer` 與角色規格 `references/subagent-scene-final-renderer.md`：

- 只接收 Stage 4 已通過的 immutable source、gate evidence、render profile 與正式渲染指南。
- 渲染四個 Scene、合併影片並建立及凍結 `render_manifest.md`。
- 不得修改 `generated_algo_scene.py`、上游契約或 Stage 4 gate evidence。
- 任何需要修改 source 的問題回報 `BLOCKED`，交回 Stage 4 `CODE_PREPARATION`。

`references/subagent-scene-writer.md` 移除 `FINAL_RENDER` 模式，只保留 Stage 4 `CODE_PREPARATION`。既有使用者尚未提交的 Stage 4／Stage 5 gate 精簡修改必須保留，模型路由改動只在必要位置疊加。

## 資料流

1. 使用者將 repository 的 `.codex/` 複製到動畫 project root。
2. 使用者從該 project root 建立新的 Codex task 並啟用 Skill。
3. 協調者在取得 Sub-Agent 授權後執行 project config preflight。
4. 協調者依 delegation protocol 派遣角色：Luna 角色繼承 project defaults；兩個 writer 角色顯式覆寫為 Sol／high。
5. 每個角色仍遵守既有輸入、產物、`DONE`／`BLOCKED`、PASS gate 與 writer／reviewer 獨立性規則。
6. Stage 5 使用新的 `scene_final_renderer`，不再重新派遣 `scene_writer`。

## 失敗處理

| 問題 | 結果 |
| --- | --- |
| 動畫 project root 缺少 `.codex/config.toml` | `BLOCKED`，要求複製範本並開啟新 task |
| TOML 無法解析或 Luna／xhigh defaults 不符 | `BLOCKED`，列出不符欄位，不自動覆寫 |
| `agents.enabled = false` | `BLOCKED` |
| Luna 不受目前 surface、帳號或 Workspace 支援 | `BLOCKED`，不 fallback |
| Sol writer 未顯式指定 Sol／high | 不得派遣；先修正派遣參數 |
| Stage 5 發現必須修改 source | renderer 回報 `BLOCKED`，回到 Stage 4 |

## 驗證策略

### Skill TDD baseline

在修改 Skill 前，用目前版本進行最小派遣規劃測試，確認它不能產生完整且一致的八角色模型映射，且 Stage 5 仍把正式渲染交給 `scene_writer`。保存實際缺口作為 RED 證據。

### 靜態驗證

- 使用 Python `tomllib` 解析 repository root 的 `.codex/config.toml`。
- 確認 `[agents]` 的 Luna／xhigh defaults 與 `enabled` 值。
- 搜尋所有派遣點，確認 task name 與 delegation protocol 的八個角色一致。
- 確認只有 `script_writer`、`scene_writer` 要求顯式 Sol／high。
- 確認 Stage 5 只派遣 `scene_final_renderer`，且 `scene_writer` 角色規格不再包含 `FINAL_RENDER`。
- 執行 Skill 的 `quick_validate.py` 與 `git diff --check`。

### Forward test

以新 task 從含有目標 `.codex/config.toml` 的測試專案啟動，要求協調者只建立八個角色的派遣計畫，不實際生成影片。驗證 Luna 角色走 project defaults、Sol 角色走 explicit override，以及缺少／錯誤 config 時 fail closed。

本次既有 task 在建立 config 前已啟動，因此只能完成檔案與靜態驗證；實際 Luna runtime 載入必須在重新開啟的 task 中驗證。

## 不在範圍內

- 不修改使用者的全域 `~/.codex/config.toml`。
- 不修改 Codex runtime 的工具 schema 或模型白名單。
- 不自動授予帳號或 Workspace 的 Luna 模型權限。
- 不改變既有五階段 gate、動畫內容契約、旁白流程、layout audit 或 delivery check 的判定標準。
- 不以 Terra 作為 Luna 的 fallback。

## 完成條件

- Repository root 提供可解析且可複製的 `.codex/config.toml`。
- Delegation protocol 對八個角色只有一份明確模型路由。
- Skill 在第一次派遣前執行 project config preflight。
- `scene_final_renderer` 是獨立 Luna／xhigh 角色，`scene_writer` 只負責 Sol／high 的 code preparation。
- 所有不支援或設定不一致情況都 fail closed，不發生靜默模型替換。
- 靜態驗證、Skill validator 與 forward-test 規劃情境均通過。
