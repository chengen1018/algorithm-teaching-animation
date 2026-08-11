---
name: manim-algorithm-animation-maker
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、製作旁白、場景實作、最終渲染與交付驗證，並在 `FINAL_RENDER_AND_DELIVERY_CHECK` 階段結束。
主要負責的 agent 必須確保所有步驟依序完成，並確認每個階段都符合要求。

## 必要授權
利用此 skill 完成各階段任務需要使用者核准使用 subagent。
若目前對話中尚未取得明確授權，必須詢問：

```text
此任務會在生成演算法動畫的流程中使用 subagent 分工。你是否同意我在此任務中使用 subagent？請明確回答「同意」或「不同意」(若不同意則無法開始此任務)。
```

只有當使用者明確回答「同意」時，才能開始後續工作。
若使用者回答「不同意」、拒絕授權或未明確表示同意則立即結束工作，不得開始任何後續階段。

## Subagent 委派契約

取得授權後、第一次派遣前，協調者必須依 `references/subagent-delegation-protocol.md` 完成 project config preflight；Preflight 未通過時不得派遣任何 subagent。

每次委派前，協調者必須完整閱讀並遵守本 skill 的 `references/subagent-delegation-protocol.md`。

每次委派時，必須依照協定指定的 task name，並在派遣訊息中清楚提供以下資訊：

- 角色規格的絕對路徑
- 必要參考文件的絕對路徑
- project root 的絕對路徑
- 所有必要輸入的絕對路徑
- 預期產物的絕對路徑


不得只提供角色名稱、假設 subagent 已知道目前對話內容，或要求 subagent 自行尋找角色規則。
如果 subagent 無法讀取派遣訊息提供的角色規格路徑，協調者必須在派遣訊息中完整附上角色規格內容，不得自行摘要、刪減或改寫。

收到 subagent 的回報後，協調者必須確認以下事項：

- 回報狀態為 `DONE` 或 `BLOCKED`
- 必要產物確實存在
- 所有關卡內容都已完成驗證

不得只因 subagent 在對話中聲稱「已完成」就直接進入下一步。

## 工作流程
依序執行以下階段：

1. `ANIMATION_DESIGN`
2. `SCRIPT`
3. `VOICEOVER`
4. `SCENE_IMPLEMENTATION`
5. `FINAL_RENDER_AND_DELIVERY_CHECK`

開始每個階段前確實閱讀完成目前階段需要的參考資料，不得跳過任何階段，也不得合併、提前或補做後續階段的工作來取代目前階段。
請照各階段的描述完成工作，且該階段規定的必要產物、審查與通過條件都已滿足後，才能進入下一個階段。

### 階段 gate 原則

本 skill 每個階段只定義自己的 `Exit gate`。第 N 階段的 `Exit gate` 同時就是第 N+1 階段的開始資格；下一階段不得再另列或重做同一組 `Entry gate` 檢查。只有子階段之間為了確認新產物、回報狀態或失敗路由所需要的局部確認，才保留在該子階段的描述中。

## 階段 1：ANIMATION_DESIGN

### 目標
先記錄使用者需求，再由主要 Agent 與使用者共同設計四個獨立 Manim Scene；動畫設計必須遵守 four-scene contract：問題與目標、演算法如何運作：決策規則與追蹤狀態、完整演示演算法、最終結果與簡短回顧。

### 子階段 1：COLLECT_REQUIREMENTS
此子階段由協調者負責。開始任何行動前，必須完整閱讀並遵循 `references/how-to-collect-requirements.md`，依其要求建立 `confirmed_requirements.md`；不要提前閱讀後續子階段的參考資料。

需求確認後，閱讀 `references/render-profile.md`，找出能成功載入 Manim 的 Python 絕對路徑，並選用支援畫面文字語言的已安裝字型。執行：

```bash
python <absolute-skill-root>/scripts/prepare_render_profile.py --project-root <absolute-project-root> --python <absolute-manim-python> --font <font-name>
```

建立 `<project-root>/render_profile.json`。除非使用者明確指定其他輸出規格，預設必須是 `1920×1080`、`60 fps`、`Cairo`。需求檔只記錄使用者需求；render defaults 只寫入 `render_profile.json`。

只有在需求蒐集的完成條件全部成立，且 `render_profile.json` 已成功建立後，才能進入 `DESIGN_DEVELOPMENT`。

### 子階段 2：DESIGN_DEVELOPMENT
開始前，主要 Agent 必須閱讀 `confirmed_requirements.md` 與 `references/how-to-design-animation.md`，閱讀完後遵循這些文件完成 DESIGN_DEVELOPMENT。

四幕設計完成後，派遣 task name `animation_design_reviewer` subagent 來審查設計。派遣訊息必須傳入：

- 角色規格：`references/subagent-animation-design-reviewer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`
- skill references：`references/how-to-review-design.md`，以及 Designer 本次實際使用的唯一一份專用 reference；若此演算法沒有適用的專用 reference，只傳入 review guide

修正審查問題時，若能在不改變使用者已明確選定的教學呈現、範例、視覺語意或核心動畫動作下完成，應直接修正。若修正會改變任一已選定設計決策，必須先提出具體修正方案並取得使用者同意，才能修改設計。

在 subagent 明確回報 `DONE`、`animation_design_review.md` 存在且清楚判定為 `PASS` 後，下一步請使用者核准設計。若使用者希望對設計進行修改，修改後必須重新派遣新的獨立審查。

只有當使用者明確核准設計後，才能離開 `ANIMATION_DESIGN` 並開始 `SCRIPT`。

## 階段 2：SCRIPT

### 目標
將已確認的需求與已核准動畫設計整理成適合教學的動畫節拍與內容順序。

### 執行事項
依委派協定派遣 task name `script_writer` 的 subagent，完成 `SCRIPT` 階段的教學腳本撰寫工作：

- 角色規格：`references/subagent-script-writer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、 `animation_design.md`、`animation_design_review.md`
- skill reference：`references/how-to-write-teaching-script.md` 的絕對路徑
- 預期產物：`teaching_script.md` 的絕對路徑

當 `script_writer` 回報 `DONE` 且完成 `teaching_script.md` 後，派遣 task name `script_reviewer` 的另一個 subagent，獨立審查教學腳本並建立 `script_review_result.md`：

- 角色規格：`references/subagent-script-reviewer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、 `animation_design.md`、`animation_design_review.md`、`teaching_script.md`
- skill reference：`references/how-to-write-teaching-script.md` 的絕對路徑
- 預期產物：`script_review_result.md` 的絕對路徑

當 `script_reviewer` 回報 `DONE` 且其產出的 `script_review_result.md` 判定為 `PASS` 時，進入下一階段 `VOICEOVER`。

## 階段 3：VOICEOVER

### 目標
根據已通過審查的教學腳本，產生每個 beat 的旁白文字與實際音訊。

### 由誰執行
依委派協定派遣 task name `voiceover_generator` 的 subagent，完成 `VOICEOVER` 階段的旁白文字與音訊生成工作：

- 角色規格：`references/subagent-voiceover-generator.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`、`teaching_script.md`、`.tts-config`
- skill reference：`references/how-to-write-and-generate-voiceover.md` 的絕對路徑
- voiceover helper：`scripts/generate_voiceover_audio.py` 的絕對路徑

### 這個階段要產出什麼
- `voiceover.md`：每個 beat 的旁白文字稿。
- `narration_manifest.json`：包含每個 beat 的音訊驗證數據。
- `audio/voiceover/` 資料夾：每個 beat 已通過驗證的旁白音訊。

### 什麼時候才算完成
subagent 回報 `DONE`，上述三類產物都已建立，manifest 涵蓋所有 beats，且每個音檔驗證均通過後，才能進入下一個階段。
若產生或驗證失敗，必須留在本階段修正；不得以靜音或其他替代方案繞過驗證。


## 階段 4：SCENE_IMPLEMENTATION

### 目標
將已核准的上游內容實作為四個 Scene，並在任何正式 Manim render 之前完成非渲染 layout 驗證與獨立契約審查。此階段只能產生程式碼與 gate 證據；目前版本的 MP4 既不是必要輸出，也不得作為通關證據。

### 子階段 1：CODE_PREPARATION
依委派協定派遣 task name `scene_writer` 的 subagent，明確指定模式 `CODE_PREPARATION`，完成 Stage 4 的場景程式碼實作與 pre-render handoff：

- 角色規格：`references/subagent-scene-writer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`、`animation_design_review.md`、`teaching_script.md`、`script_review_result.md`、`voiceover.md`、`narration_manifest.json`、`audio/voiceover/`、`render_profile.json` 的絕對路徑
- skill references：`references/how-to-implement-and-verify-manim-scenes.md`、`references/how-to-hand-off-scene-code-for-review.md` 的絕對路徑
- layout helper：`scripts/scene_layout_audit.py` 的絕對路徑；複製到 project root，並由每個 Scene 建立 scene-specific adapter
- 預期產物：`generated_algo_scene.py`、`scene_code_review_handoff.md` 的絕對路徑

Writer 把已通過 gate 的上游產物視為可執行契約，以最小、保守方式處理可合理解讀的細節，並在 handoff 記錄 `Render Assumptions`、四個 Scene class 的核准順序、`Code SHA-256`、`Render Profile SHA-256` 與 `Manim render performed: NO`。

Writer 必須完成完整重讀與靜態 self-audit。此子階段不得執行 Manim render、preview、低畫質 render 或合併影片，也不得先建立本版本的送審 MP4。

若上游契約不完整、衝突或必須改變已核准內容，不得由 writer 自行補寫；退回擁有該內容的 Stage 1、2 或 3。

### 子階段 2：LAYOUT_VERIFICATION
協調者確認 `scene_writer` 回報 `DONE`、兩份輸出存在且沒有以本版本 MP4 作為證據後，依委派協定派遣 task name `scene_layout_validator` 的 subagent：

- 角色規格：`references/subagent-scene-layout-validator.md` 的絕對路徑
- project inputs：`generated_algo_scene.py`、`scene_code_review_handoff.md`、`render_profile.json` 的絕對路徑
- skill reference：`references/layout-audit.md` 的絕對路徑
- runner：`scripts/run_layout_audit.py` 的絕對路徑
- 額外派遣資料：handoff 所列四個 Scene class 與核准順序
- 預期產物：`layout_audit_result.md` 的絕對路徑

Validator 對 handoff 所列的四個 Scene class 依核准順序各執行一次以下必要命令，完整保留 stdout、stderr 與 exit code：

```bash
<render-profile-python> <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --render-profile <absolute-project-root>/render_profile.json --audit-visible --require-adapter --visible-report-level warning
```

這是建立真實 Manim mobject geometry、但不寫 frame 或 MP4 的 dry-run。泛用掃描只把超出 frame 視為失敗；overlap 訊息只用來協助除錯。具名物件之間的 fit、collision 與 spacing 由 scene-specific adapter 判定。

`layout_audit_result.md` 必須記錄 `Audited Code SHA-256`、`Runner SHA-256`、`Render Profile path`、`Render Profile SHA-256`、profile 內的 Python／Manim／frame／renderer／font 欄位，以及四個完整命令、輸出、adapter checkpoint 摘要和 exit code。四個命令全部 exit `0`、每幕都執行 initial、至少一個 beat 與 final checkpoint，且 hash 完整一致時才能 `PASS`。

若 adapter 缺少必要 checkpoint、具名檢查失敗、畫面越界、漏檢任一 Scene 或 hash／profile 不一致，留在 Stage 4，先修正 `CODE_PREPARATION`，再重跑全部四幕 layout audit。任何程式碼變更都要建立新 handoff 與新 hash。

### 子階段 3：CONTRACT_REVIEW
只有 `scene_layout_validator` 回報 `DONE`、`layout_audit_result.md = PASS`、完整涵蓋四幕且 audited hash 與目前程式碼及 handoff 相同後，才能依委派協定派遣 task name `scene_reviewer` 的獨立 subagent：

- 角色規格：`references/subagent-scene-reviewer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`、`animation_design_review.md`、`teaching_script.md`、`script_review_result.md`、`generated_algo_scene.py`、`scene_code_review_handoff.md`、`layout_audit_result.md` 的絕對路徑
- skill reference：`references/how-to-review-manim-scene-code.md` 的絕對路徑
- 預期產物：`scene_review_result.md` 的絕對路徑

Reviewer 建立 `scene_review_result.md`，只審查 source fidelity、演算法／state correctness、lifecycle／ownership、cleanup 與 assumptions；實際 mobject geometry、bounding-box、碰撞、遮擋與 safe-frame 判定以 `layout_audit_result.md` 為唯一責任來源，不得重做。Review result 必須記錄相同的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256`。

若 `scene_review_result.md = FAIL`、reviewer 不獨立或 hash 不一致，留在 Stage 4，將 blocking findings 交回 writer；任何程式碼修正都要從 `CODE_PREPARATION` 重新建立 handoff、layout audit 與契約審查。

### 必要輸出
Stage 4 只建立並接受：

- `generated_algo_scene.py`
- `scene_code_review_handoff.md`
- `layout_audit_result.md`
- 由獨立 scene reviewer 產出的 `scene_review_result.md`

四個 Scene MP4、合併 MP4 與 `render_manifest.md` 都屬於 Stage 5，不得用來補足或取代 Stage 4 gate。

### Exit gate
只有以下條件全部成立才能進入 `FINAL_RENDER_AND_DELIVERY_CHECK`：

- `layout_audit_result.md = PASS`，四個核准 Scene 的必要命令都 exit `0`。
- `scene_review_result.md = PASS`，且由未參與程式碼撰寫的獨立 reviewer 產出。
- 目前 `generated_algo_scene.py` SHA-256、handoff 的 `Code SHA-256`、layout result 的 `Audited Code SHA-256`、review result 的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256` 全部一致。
- handoff 與 layout result 記錄的 `Render Profile SHA-256` 都等於目前 `render_profile.json` 的 SHA-256。
- PASS 後程式碼、上游契約、runner 或 `render_profile.json` 都沒有改變。

本機自行檢查、dry-run 可執行、非正式 review 或提早產生的 MP4 都不能取代上述 gate。

Stage 4 `Exit gate` 通過後，若在正式渲染前發現程式碼或 `render_profile.json` 改變，回到 `CODE_PREPARATION`；若 profile 未改變但執行環境或 runner 改變，回到 `LAYOUT_VERIFICATION`；若上游需求、設計、腳本或旁白契約改變，回到擁有該內容的 Stage。

## 階段 5：FINAL_RENDER_AND_DELIVERY_CHECK

### 目標
只用 Stage 4 已通過且 hash 完全一致的單一 source version 完成正式渲染、建立 render evidence，並執行技術性交付檢查。Layout 與演算法語意以 Stage 4 的核准證據為準。

Stage 5 直接承接 Stage 4 的 `Exit gate`，以四份 gate 證據、source hash 與 render profile hash 作為正式渲染的核准輸入。

### 子階段 1：FINAL_RENDER
依委派協定派遣 task name `scene_final_renderer` 的 subagent：

- 角色規格：`references/subagent-scene-final-renderer.md` 的絕對路徑
- Stage 4 gate evidence：`generated_algo_scene.py`、`scene_code_review_handoff.md`、`layout_audit_result.md`、`scene_review_result.md` 的絕對路徑
- `render_profile.json` 的絕對路徑與 Stage 4 核准的 SHA-256
- handoff 所列的四個 Scene class 與核准順序
- render guide：`references/how-to-render-approved-manim-scenes.md` 的絕對路徑
- 預期產物：四個 Scene MP4、combined MP4 與 `render_manifest.md` 的絕對路徑

Renderer 直接使用 Stage 4 `Exit gate` 所核准且未修改的 source 與 `render_profile.json`，並保持 source 與 gate evidence 不變。

若正式渲染前發現 Stage 4 PASS 後程式碼或 `render_profile.json` 改變，回到 Stage 4 `CODE_PREPARATION`；若 profile 未改變但執行環境或 runner 改變，回到 `LAYOUT_VERIFICATION`；若上游需求、設計、腳本或旁白契約改變，回到擁有該內容的 Stage。不得使用舊的 Stage 4 gate 繼續渲染。

依核准順序渲染四個 Scene、合併最終影片並建立 `render_manifest.md`。Manifest 依 handoff 的核准順序記錄實際 render commands、exit codes、輸出路徑與核准 code hash。Renderer 必須在執行 `DELIVERY_CHECK` 前完整填妥並凍結 manifest。

### 子階段 2：DELIVERY_CHECK
`FINAL_RENDER` 完成後，由 coordinator 執行交付檢查。

- project inputs：`generated_algo_scene.py`、`render_profile.json`、`render_manifest.md`、四個 Scene MP4 與合併 MP4
- delivery helper：`scripts/verify_delivery.py` 的絕對路徑
- 預期產物：`delivery_check_result.md`

執行：

```bash
python <absolute-skill-root>/scripts/verify_delivery.py --source <absolute-project-root>/generated_algo_scene.py --profile <absolute-project-root>/render_profile.json --manifest <absolute-project-root>/render_manifest.md --output <absolute-project-root>/delivery_check_result.md
```

Helper 以唯讀方式對五個 MP4 執行 `ffprobe`、解碼 combined MP4，並檢查 video/audio streams、解析度、frame rate、duration、render exit codes、source hash 與 render profile hash。

若任一 `ffprobe` 或 combined decode 失敗，留在 Stage 5 `FINAL_RENDER`，只修復並重新建立受影響的輸出與 manifest，再重跑 `DELIVERY_CHECK`。若 source hash mismatch 或修復時改變 `render_profile.json`，回到 Stage 4 `CODE_PREPARATION`；若 profile 未改變但執行環境改變，回到 Stage 4 `LAYOUT_VERIFICATION`；若上游契約改變，回到擁有該內容的 Stage。只要重新產生任一 MP4 或 manifest，舊的 `delivery_check_result.md` 就不能沿用，必須重新執行 `DELIVERY_CHECK`。

### 必要輸出與 Exit gate
Stage 5 必須建立：

- 依核准順序的四個非空 Scene MP4
- 非空的最終合併 MP4
- `render_manifest.md`
- `delivery_check_result.md = PASS`

Manifest、目前 source 與 Stage 4 gate 必須綁定同一個 code hash 與 render profile hash；delivery result 必須記錄五個 `ffprobe` 結果、combined decode 結果、媒體規格、duration 與兩種 hash comparison。
