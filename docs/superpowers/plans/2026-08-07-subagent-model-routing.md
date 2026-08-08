# Sub-Agent Model Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** 為 manim-algorithm-animation-maker 提供可複製的 project-level Luna 預設設定、兩個 Sol writer 的顯式覆寫，以及獨立的 Luna scene_final_renderer。

**Architecture:** Repository root 的 .codex/config.toml 提供所有未覆寫 Sub-Agent 的 gpt-5.6-luna／xhigh defaults；references/subagent-delegation-protocol.md 是八個角色模型路由的唯一權威來源，並對 script_writer、scene_writer 指定 gpt-5.6-sol／high。Stage 5 從 scene_writer 拆出 scene_final_renderer，讓程式碼實作與正式渲染維持不同角色與模型設定。

**Tech Stack:** Markdown、TOML、Python 3 標準庫 tomllib、Codex Sub-Agent workflow、Skill validator。

## Global Constraints

- 不修改全域 ~/.codex/config.toml，只建立 repository root 的 .codex/config.toml。
- Luna 角色使用 gpt-5.6-luna／xhigh project defaults；script_writer、scene_writer 顯式使用 gpt-5.6-sol／high。
- Luna 不可用、config 缺失或 config 不符時一律 BLOCKED；不得 fallback 到 Terra、Sol、parent model 或其他模型。
- .codex/config.toml 是會在本 repository 新 task 中生效的實際設定；外部動畫專案使用者應複製整個 .codex/。
- 保留五階段 gate、旁白、layout audit、contract review 與 delivery check 的既有判定標準。
- 保留目前 working tree 中已存在的三份未提交修改：SKILL.md、how-to-render-approved-manim-scenes.md、subagent-scene-writer.md。不得 reset、restore 或以舊版整檔覆寫。
- 因實作會繼續修改上述三份 dirty files，未取得使用者明確同意前，不得把其原有 hunks 一併 stage 或 commit。新檔與原先 clean 的檔案可獨立提交。

## File Map

| File | Responsibility |
| --- | --- |
| .codex/config.toml | Repository-level Luna／xhigh Sub-Agent defaults。 |
| manim-algorithm-animation-maker/SKILL.md | 第一次派遣前的 config preflight，以及 Stage 5 的 scene_final_renderer orchestration。 |
| manim-algorithm-animation-maker/references/subagent-delegation-protocol.md | 八角色 task name、角色規格、model source、model 與 reasoning effort 的唯一對照。 |
| manim-algorithm-animation-maker/references/subagent-scene-writer.md | 只負責 Stage 4 CODE_PREPARATION。 |
| manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md | 只負責 Stage 5 immutable-source render 與 manifest。 |
| manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md | 將正式渲染執行者指向 scene_final_renderer。 |
| Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md | 保存 RED baseline、GREEN forward test 與 runtime reload 邊界。 |

---

### Task 1: 建立 Skill TDD baseline evidence

**Files:**
- Create: Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
- Read: manim-algorithm-animation-maker/SKILL.md
- Read: manim-algorithm-animation-maker/references/subagent-delegation-protocol.md

**Interfaces:**
- Consumes: 尚未加入模型路由的 Skill 與 delegation protocol。
- Produces: 固定情境、判定準則與原始 baseline 回應，供 Task 4 使用同一 prompt 重測。

- [ ] **Step 1: 建立 validation scenario 文件**

文件必須先包含下列固定測試 prompt：

    Use the Manim Algorithm Animation Maker skill from the supplied absolute path. Do not create animation artifacts and do not modify files. Return only the complete Sub-Agent dispatch plan as a table with stage, task name, role-spec path, model source, effective model, reasoning effort, and whether source edits are permitted. Include the final-render agent.

Pass criteria 必須逐項列出：

- Exactly eight task names are present.
- Only script_writer and scene_writer use explicit gpt-5.6-sol / high.
- The other six roles inherit project defaults gpt-5.6-luna / xhigh.
- Stage 5 uses scene_final_renderer, not scene_writer.
- Only scene_writer may edit generated_algo_scene.py; scene_final_renderer may not.
- Missing or invalid project config produces BLOCKED with no fallback.

另外建立 Baseline Evidence、Forward-Test Evidence、Runtime Reload Boundary 三個空 section；evidence 只能填入實際回應。

- [ ] **Step 2: 派遣一個 fresh-context baseline Sub-Agent**

只提供目前 Skill folder 與 scenario 文件的絕對路徑，不提供設計規格、預期模型表或診斷結論。要求 Sub-Agent 不修改任何檔案。

- [ ] **Step 3: 確認 RED failure**

逐欄人工核對回應。預期 delegation protocol 沒有 model／reasoning mapping，而且 Stage 5 仍使用 scene_writer。若 baseline 意外符合全部 criteria，停止並檢查工作樹是否已被提前修改；沒有可觀察的 RED failure 就不得繼續。

- [ ] **Step 4: 保存 baseline evidence**

將原始 Sub-Agent 回應逐字放入 Baseline Evidence 的 fenced text block，再逐項記錄失敗 criteria；不得摘要或改寫回應。

- [ ] **Step 5: 驗證並提交 fixture**

Run:

    rg -n "Scenario prompt|Pass criteria|Baseline Evidence|Forward-Test Evidence|Runtime Reload Boundary" Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
    git diff --check -- Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md

Expected: 五個 section 都存在；format check exit 0。

Commit:

    git add -f Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
    git commit -m "test: capture subagent routing baseline"

---

### Task 2: 將 Stage 5 拆成獨立 final-render Sub-Agent

**Files:**
- Create: manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md
- Modify: manim-algorithm-animation-maker/references/subagent-scene-writer.md:1-72
- Modify: manim-algorithm-animation-maker/references/subagent-delegation-protocol.md:16-26
- Modify: manim-algorithm-animation-maker/SKILL.md:207-219
- Modify: manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md:5-17

**Interfaces:**
- Consumes: Stage 4 immutable source、handoff、layout result、scene review 與 approved render profile。
- Produces: scene_final_renderer role、四個 Scene MP4、combined MP4 與 frozen render_manifest.md。

- [ ] **Step 1: 執行 identity RED check**

Run:

    test -f manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md
    ! rg -n "再次派遣原.*scene_writer" manim-algorithm-animation-maker/SKILL.md

Expected: 第一個命令失敗，第二個命令失敗；新角色尚不存在且舊 Stage 5 dispatch 仍存在。

- [ ] **Step 2: 建立 subagent-scene-final-renderer.md**

角色規格必須依序包含：

1. Role：只負責 Stage 5 FINAL_RENDER；使用 Stage 4 Exit gate 核准的 immutable source 與 profile；不得建立或修改 source、handoff、layout result 或 scene review。
2. Required inputs：generated_algo_scene.py、scene_code_review_handoff.md、layout_audit_result.md、scene_review_result.md、how-to-render-approved-manim-scenes.md 絕對路徑、approved render profile、四個 Scene class 與核准順序。
3. Gate ownership：Stage 4 Exit gate 是唯一渲染前 gate；不重做 hash、PASS 或 environment preflight；輸入無法讀取則 BLOCKED。
4. Procedure：依序渲染四幕、合併影片、建立完整 manifest、在 DELIVERY_CHECK 前凍結 manifest。
5. Failure routing：任何需要修改 source、上游契約或 Stage 4 evidence 的問題立即 BLOCKED，交回 Stage 4 或對應上游 Stage。
6. Completion：四個 Scene MP4、combined MP4 與 frozen render_manifest.md 存在；source 與 gate evidence 未改變。
7. Final response：DONE 回報輸出、commands 與 exit codes；BLOCKED 回報證據與回退路由。

- [ ] **Step 3: 限縮 scene writer**

把 Role 精確改為只負責 Stage 4 CODE_PREPARATION。保留八項上游輸入、兩份實作 reference、既有 CODE_PREPARATION procedure 與禁止渲染規則；移除 FINAL_RENDER inputs、render shared-input 說明、FINAL_RENDER procedure 與 final-render completion criteria。Final response 不再要求模式欄位。

- [ ] **Step 4: 更新 orchestration 與 render guide**

- Delegation table 新增正式場景渲染與合併 → scene_final_renderer → references/subagent-scene-final-renderer.md。
- SKILL Stage 5 改為派遣 scene_final_renderer，提供 Stage 4 四份 evidence、approved profile、四個 Scene class 與順序、render guide 絕對路徑。
- Stage 5 後續稱呼由 Writer 改為 Renderer。
- Render guide 接受 gate evidence 的角色由 scene_writer 改成 scene_final_renderer。
- 保留 dirty files 中既有的 gate 精簡內容。

- [ ] **Step 5: 執行 GREEN checks**

Run:

    test -f manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md
    ! rg -n "FINAL_RENDER" manim-algorithm-animation-maker/references/subagent-scene-writer.md
    rg -n "scene_final_renderer|subagent-scene-final-renderer.md" manim-algorithm-animation-maker/SKILL.md manim-algorithm-animation-maker/references/subagent-delegation-protocol.md manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
    git diff --check

Expected: renderer file 存在；writer spec 不含 FINAL_RENDER；三份流程文件均指向新角色；format check exit 0。

- [ ] **Step 6: 安全提交 clean/new portions**

先檢查完整 diff，確認原有 gate 精簡 hunks 仍存在。只提交新角色與原先 clean 的 delegation protocol：

    git add manim-algorithm-animation-maker/references/subagent-scene-final-renderer.md manim-algorithm-animation-maker/references/subagent-delegation-protocol.md
    git commit -m "feat: add dedicated final render agent"

不要 stage 三份 task 開始前已 dirty 的檔案；將它們保留在 working tree，等待使用者決定如何提交。

---

### Task 3: 加入 Luna defaults、Sol overrides 與 fail-closed preflight

**Files:**
- Create: .codex/config.toml
- Modify: manim-algorithm-animation-maker/references/subagent-delegation-protocol.md:5-43
- Modify: manim-algorithm-animation-maker/SKILL.md:23-45

**Interfaces:**
- Consumes: 動畫 project root 的 .codex/config.toml 與八個 task names。
- Produces: Luna inherited defaults、兩個 writer explicit overrides，以及 BLOCKED preflight contract。

- [ ] **Step 1: 執行 config RED check**

Run:

    python3 -c 'from pathlib import Path; import tomllib; p=Path(".codex/config.toml"); assert p.is_file(); a=tomllib.loads(p.read_text())["agents"]; assert a["enabled"] is True; assert a["default_subagent_model"] == "gpt-5.6-luna"; assert a["default_subagent_reasoning_effort"] == "xhigh"'

Expected: non-zero，因 repository root 尚未提供 config。

- [ ] **Step 2: 建立 repository root config**

Exact content:

    [agents]
    enabled = true
    default_subagent_model = "gpt-5.6-luna"
    default_subagent_reasoning_effort = "xhigh"

- [ ] **Step 3: 在 protocol 加入 preflight**

第一次派遣任何 Sub-Agent 前，要求 coordinator 解析動畫 project root 的 config，確認 enabled 未設為 false、model 為 gpt-5.6-luna、effort 為 xhigh。缺檔、parse error、值不符、runtime 拒絕 Luna 或 config 在目前 task 啟動後才加入時，回報 BLOCKED；不得自行覆寫或 fallback，並要求從正確 project root 建立新 task。

- [ ] **Step 4: 將角色表擴充成唯一模型路由**

Table columns 必須是：

    工作 | task name | 角色規格 | model source | model | reasoning effort

Exact routing:

| task name | model source | model | effort |
| --- | --- | --- | --- |
| animation_design_reviewer | project default | gpt-5.6-luna | xhigh |
| script_writer | explicit spawn override | gpt-5.6-sol | high |
| script_reviewer | project default | gpt-5.6-luna | xhigh |
| voiceover_generator | project default | gpt-5.6-luna | xhigh |
| scene_writer | explicit spawn override | gpt-5.6-sol | high |
| scene_layout_validator | project default | gpt-5.6-luna | xhigh |
| scene_reviewer | project default | gpt-5.6-luna | xhigh |
| scene_final_renderer | project default | gpt-5.6-luna | xhigh |

在表格後要求：project-default roles 呼叫 spawn_agent 時省略 model 與 reasoning_effort；兩個 explicit roles 必須傳入 gpt-5.6-sol 與 high。不得把模型名稱只寫入 message 來假裝已套用。

- [ ] **Step 5: 在 SKILL 串接唯一 preflight**

在 Subagent 委派契約開頭加入：取得授權後、第一次派遣前，coordinator 必須依 protocol 完成 project config preflight；未通過時不得派遣。不要把八角色表複製到 SKILL。

- [ ] **Step 6: 執行 GREEN checks**

Run:

    python3 -c 'from pathlib import Path; import tomllib; a=tomllib.loads(Path(".codex/config.toml").read_text())["agents"]; assert a == {"enabled": True, "default_subagent_model": "gpt-5.6-luna", "default_subagent_reasoning_effort": "xhigh"}'
    python3 -c 'from pathlib import Path; s=Path("manim-algorithm-animation-maker/references/subagent-delegation-protocol.md").read_text(); names=["animation_design_reviewer","script_writer","script_reviewer","voiceover_generator","scene_writer","scene_layout_validator","scene_reviewer","scene_final_renderer"]; table="\n".join(line for line in s.splitlines() if line.startswith("|") and "references/subagent-" in line); assert all(f"| {n} |" in table or f"| `{n}` |" in table for n in names); assert table.count("gpt-5.6-sol") == 2; assert table.count("gpt-5.6-luna") == 6'
    rg -n "project config preflight|Preflight 未通過" manim-algorithm-animation-maker/SKILL.md manim-algorithm-animation-maker/references/subagent-delegation-protocol.md
    git diff --check

Expected: assertions、search 與 format check 全部 exit 0；routing table 內是兩個 Sol rows 與六個 Luna rows。

- [ ] **Step 7: 提交 config 與 routing contract**

    git add .codex/config.toml manim-algorithm-animation-maker/references/subagent-delegation-protocol.md
    git commit -m "feat: route animation subagents by model"

SKILL.md 含 task 開始前既有 hunks；未取得使用者同意前保持 unstaged。

---

### Task 4: GREEN forward test 與整體驗證

**Files:**
- Modify: Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
- Verify: .codex/config.toml
- Verify: manim-algorithm-animation-maker/

**Interfaces:**
- Consumes: Task 1 的相同 scenario、Task 2 的 renderer、Task 3 的 routing。
- Produces: GREEN evidence、Skill 結構驗證，以及 fresh-task runtime check prompt。

- [ ] **Step 1: 使用相同 prompt 執行 fresh-context forward test**

只提供更新後 Skill folder 與 scenario 文件的絕對路徑；不提供設計規格、baseline diagnosis 或答案。要求 Sub-Agent 不修改檔案。

- [ ] **Step 2: 核對 GREEN behavior**

逐項確認 Task 1 六項 pass criteria。任一項失敗時，只針對實際缺口收緊 protocol 或角色規格，再用新的 fresh-context Sub-Agent 重跑；不得把答案加入 prompt。

- [ ] **Step 3: 保存 forward evidence**

把最後一次原始回應逐字放入 Forward-Test Evidence，再逐項標記六項 criteria 為 PASS。保留 baseline，不得覆寫。

- [ ] **Step 4: 執行完整驗證**

Run:

    python3 /Users/lichengen/.codex/skills/.system/skill-creator/scripts/quick_validate.py "/Users/lichengen/Developer/Senior-project/Manim Algorithm Animation Maker/manim-algorithm-animation-maker"
    python3 -c 'from pathlib import Path; import tomllib; tomllib.loads(Path(".codex/config.toml").read_text())'
    ! rg -n "FINAL_RENDER" manim-algorithm-animation-maker/references/subagent-scene-writer.md
    rg -n "scene_final_renderer" manim-algorithm-animation-maker/SKILL.md manim-algorithm-animation-maker/references/subagent-delegation-protocol.md manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
    git diff --check
    git status --short

Expected:

- Skill validator reports valid。
- TOML parse exit 0。
- Scene writer 不含 FINAL_RENDER。
- 三份流程文件都指向 scene_final_renderer。
- git diff --check exit 0。
- Git status 只顯示本計畫產物與 task 開始前已知 dirty files。

- [ ] **Step 5: 提交 validation evidence**

    git add -f Docs/superpowers/validation/2026-08-07-subagent-model-routing-scenarios.md
    git commit -m "test: verify subagent model routing"

- [ ] **Step 6: 回報 runtime reload boundary**

告知使用者：目前 task 在 config 建立前已啟動，靜態與 forward planning tests 可完成，但 Luna 的實際 runtime selection 必須從含有 config 的專案根目錄建立新 task 後驗證。提供以下 prompt：

    請讀取目前專案的 .codex/config.toml，使用 manim-algorithm-animation-maker 的 subagent delegation protocol，只列出八個角色的 task name、model source、effective model 與 reasoning effort；不要生成影片或修改檔案。

## Final Handoff

完成所有任務後交付 config、八角色 routing table、獨立 renderer、RED／GREEN evidence、全部靜態驗證結果，以及仍未提交 dirty files 的精確清單。
