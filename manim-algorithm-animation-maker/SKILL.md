---
name: manim-algorithm-animation-maker
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、製作旁白、場景實作、最終渲染與成品 QA，並在 `FINAL_RENDER_AND_QA` 階段結束。
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
5. `FINAL_RENDER_AND_QA`

開始每個階段前確實閱讀完成目前階段需要的參考資料，不得跳過任何階段，也不得合併、提前或補做後續階段的工作來取代目前階段。
請照各階段的描述完成工作，且該階段規定的必要產物、審查與通過條件都已滿足後，才能進入下一個階段。

## 階段 1：ANIMATION_DESIGN

### 目標
先記錄使用者需求，再由主要 Agent 與使用者共同設計四個獨立 Manim Scene；動畫設計必須遵守 four-scene contract：問題與目標、演算法如何運作：決策規則與追蹤狀態、完整演示演算法、最終結果與簡短回顧。

### 子階段 1：COLLECT_REQUIREMENTS
此子階段由協調者負責。開始任何行動前，必須完整閱讀並遵循 `references/how-to-collect-requirements.md`，依其要求建立 `confirmed_requirements.md`；不要提前閱讀後續子階段的參考資料。

只有在需求蒐集的完成條件全部成立後，才能進入 `DESIGN_DEVELOPMENT`。

### 子階段 2：DESIGN_DEVELOPMENT
開始前，主要 Agent 必須閱讀 `confirmed_requirements.md` 與 `references/how-to-design-animation.md`，閱讀完後遵循這些文件完成 DESIGN_DEVELOPMENT。

四幕設計完成後，派遣 task name `animation_design_reviewer` subagent 來審查設計。派遣訊息必須傳入：

- 角色規格：`subagent-animation-design-reviewer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`
- skill references：`how-to-review-design.md`

修正審查問題時，若能在不改變使用者已明確選定的教學呈現、範例、視覺語意或核心動畫動作下完成，應直接修正。若修正會改變任一已選定設計決策，必須先提出具體修正方案並取得使用者同意，才能修改設計。

在 subagent 明確回報 `DONE`、`animation_design_review.md` 存在且清楚判定為 `PASS` 後，下一步請使用者核准設計。若使用者希望對設計進行修改，修改後必須重新派遣新的獨立審查。

只有當使用者明確核准設計後，才能離開 `ANIMATION_DESIGN` 並開始 `SCRIPT`。

## 階段 2：SCRIPT

### 目標
將已確認的需求與已核准動畫設計整理成適合教學的動畫節拍與內容順序。

### 執行事項
依委派協定派遣 task name `script_writer` 的 subagent，完成 `SCRIPT` 階段的教學腳本撰寫工作：

- 角色規格：`subagent-script-writer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、 `animation_design.md`、`animation_design_review.md`
- skill reference：`how-to-write-teaching-script.md` 的絕對路徑
- 預期產物：`teaching_script.md` 的絕對路徑

當 `script_writer` 回報 `DONE` 且完成 `teaching_script.md` 後，派遣 task name `script_reviewer` 的另一個 subagent，獨立審查教學腳本並建立 `script_review_result.md`：

- 角色規格：`subagent-script-reviewer.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、 `animation_design.md`、`animation_design_review.md`、`teaching_script.md`
- skill reference：`how-to-write-teaching-script.md` 的絕對路徑
- 預期產物：`script_review_result.md` 的絕對路徑

當 `script_reviewer` 回報 `DONE` 且其產出的 `script_review_result.md` 判定為 `PASS` 時，進入下一階段 `VOICEOVER`。

## 階段 3：VOICEOVER

### 目標
根據已通過審查的教學腳本，產生每個 beat 的旁白文字與實際音訊。

### 由誰執行
依委派協定派遣 task name `voiceover_generator` 的 subagent，完成 `VOICEOVER` 階段的旁白文字與音訊生成工作：

- 角色規格：`subagent-voiceover-generator.md` 的絕對路徑
- project inputs：`confirmed_requirements.md`、`animation_design.md`、`teaching_script.md`、`.tts-config`
- skill reference：`how-to-write-and-generate-voiceover.md` 的絕對路徑

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

### Entry gate
開始前必須全部成立：

- `animation_design.md` 已通過內容審查並取得使用者明確核准。
- `teaching_script.md` 存在且 `script_review_result.md = PASS`。
- `voiceover.md`、`narration_manifest.json` 與四幕所需的可直接使用音訊都存在且已通過 Stage 3 驗證。
- 已取得使用 subagent 的明確授權。

### 委派契約
協調者依委派協定使用以下三個彼此分離的角色，並在每次派遣中傳入角色規格、必要 project inputs、skill references、runner 與預期產物的絕對路徑：

- scene writer：task name `scene_writer`，角色規格 `subagent-scene-writer.md`，模式 `CODE_PREPARATION`
- layout validator：task name `scene_layout_validator`，角色規格 `subagent-scene-layout-validator.md`
- scene reviewer：task name `scene_reviewer`，角色規格 `subagent-scene-reviewer.md`
- 實作與 handoff references：`how-to-implement-and-verify-manim-scenes.md`、`how-to-hand-off-scene-code-for-review.md`
- layout reference 與 runner：`layout-audit.md`、`run_layout_audit.py`
- 契約審查 reference：`how-to-review-manim-scene-code.md`

### 子階段 1：CODE_PREPARATION
派遣 `scene_writer` 並明確指定 `CODE_PREPARATION`。Writer 把已通過 gate 的上游產物視為可執行契約，以最小、保守方式處理可合理解讀的細節，建立 `generated_algo_scene.py` 與 pre-render `scene_code_review_handoff.md`，並在 handoff 記錄 `Render Assumptions`、四個 Scene class 的核准順序、`Code SHA-256` 與 `Manim render performed: NO`。

Writer 必須完成完整重讀與靜態 self-audit。此子階段不得執行 Manim render、preview、低畫質 render 或合併影片，也不得先建立本版本的送審 MP4。

### 子階段 2：LAYOUT_VERIFICATION
協調者確認 writer 回報 `DONE`、兩份輸出存在且沒有以本版本 MP4 作為證據後，派遣 `scene_layout_validator`。Validator 對 handoff 所列的四個 Scene class 依核准順序各執行一次以下必要命令，完整保留 stdout、stderr 與 exit code：

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --audit-visible --fail-on-warning --visible-report-level warning
```

這是建立真實 Manim mobject geometry、但不寫 frame 或 MP4 的 dry-run。`layout_audit_result.md` 必須記錄 `Audited Code SHA-256`、runner 與 layout-affecting environment/profile metadata、四個完整命令、輸出和 exit code。四個必要命令全部 exit `0` 才能 `PASS`；warning、漏檢、hash 無法核對或環境證據不足一律 `FAIL`，不得人工豁免。

若需要 scene-specific adapter，先退回 `CODE_PREPARATION` 由 writer 依 `layout-audit.md` 實作；任何程式碼變更都要建立新 handoff 與新 hash，再重新執行全部四幕 layout audit。

### 子階段 3：CONTRACT_REVIEW
只有 `scene_layout_validator` 回報 `DONE`、`layout_audit_result.md = PASS`、完整涵蓋四幕且 audited hash 與目前程式碼及 handoff 相同後，才能派遣獨立 `scene_reviewer`。

Reviewer 建立 `scene_review_result.md`，只審查 source fidelity、演算法／state correctness、lifecycle／ownership、cleanup 與 assumptions；實際 mobject geometry、bounding-box、碰撞、遮擋與 safe-frame 判定以 `layout_audit_result.md` 為唯一責任來源，不得重做。Review result 必須記錄相同的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256`。

### 必要輸出
Stage 4 只建立並接受：

- `generated_algo_scene.py`
- `scene_code_review_handoff.md`
- `layout_audit_result.md`
- 由獨立 scene reviewer 產出的 `scene_review_result.md`

四個 Scene MP4、合併 MP4 與 `render_manifest.md` 都屬於 Stage 5，不得用來補足或取代 Stage 4 gate。

### Exit gate
只有以下條件全部成立才能進入 `FINAL_RENDER_AND_QA`：

- `layout_audit_result.md = PASS`，四個核准 Scene 的必要命令都 exit `0`。
- `scene_review_result.md = PASS`，且由未參與程式碼撰寫的獨立 reviewer 產出。
- 目前 `generated_algo_scene.py` SHA-256、handoff 的 `Code SHA-256`、layout result 的 `Audited Code SHA-256`、review result 的 `Reviewed Code SHA-256` 與 `Layout-audited Code SHA-256` 全部一致。
- PASS 後程式碼、上游契約與 layout-affecting environment/profile 沒有改變。

本機自行檢查、dry-run 可執行、非正式 review 或提早產生的 MP4 都不能取代上述 gate。

### 失敗路由
- Layout `FAIL`：留在 Stage 4，交回 `scene_writer` 的 `CODE_PREPARATION` 修正；產生新 hash 後重跑全部四幕 layout audit，再做契約審查。
- Reviewer `FAIL`：留在 Stage 4，將 blocking findings 交回 writer；任何程式碼修正都使舊 handoff 與 layout result 失效，必須從 `CODE_PREPARATION` 重新開始。
- 上游契約不完整、衝突或必須改變已核准內容：退回擁有該內容的 Stage 1、2 或 3，不得由 writer 或 reviewer 自行補寫新意思。

## 階段 5：FINAL_RENDER_AND_QA

### 目標
只用 Stage 4 已通過且 hash 完全一致的單一 source version 完成正式渲染，建立 render evidence，並由獨立 validator 驗證交付媒體的完整性、metadata、音訊、duration、順序與 hashes。Stage 5 不重跑 layout audit，也不得用渲染後觀察取代 Stage 4 的 layout gate。

### Entry gate
Stage 4 的四份必要輸出必須存在，layout 與 scene review 都是目前 source hash 的 `PASS`，四幕 layout audit 完整通過，而且 code、上游契約與 layout-affecting environment/profile 自 Stage 4 PASS 後未改變。任一條件不成立都不得開始正式 Manim render。

### 子階段 1：FINAL_RENDER
再次派遣原 `scene_writer`，明確指定模式 `FINAL_RENDER`，並提供 Stage 4 四份 gate 證據與 `how-to-render-approved-manim-scenes.md` 的絕對路徑。Writer 必須在第一個 render command 前核對目前 code、handoff、layout 與 review hashes 全部一致；gate 通過後不得修改 `generated_algo_scene.py`。

依核准順序渲染四個 Scene、合併最終影片並建立 `render_manifest.md`。四幕與合併 MP4 必須全部存在且非空，manifest 必須把這些輸出綁定到唯一核准的 code hash 與 Stage 4 PASS 證據。

### 子階段 2：DELIVERY_QA
`FINAL_RENDER` 完成後，依委派協定派遣 task name `rendered_media_validator` 的獨立 subagent：

- 角色規格：`subagent-rendered-media-validator.md` 的絕對路徑
- project inputs：`generated_algo_scene.py`、`scene_code_review_handoff.md`、`layout_audit_result.md`、`scene_review_result.md`、`render_manifest.md`、`narration_manifest.json`、依核准順序排列的四個 Scene MP4 與合併 MP4
- 預期產物：`rendered_media_validation_result.md`

Validator 依角色契約對每個 MP4 執行完整的 `ffprobe` metadata、`ffmpeg` decode 與 SHA-256 檢查，核對 source/gate identity、四幕順序、duration 與 audio evidence；不得 render、修改、修補、重編碼或替換媒體。只有 validator 回報 `DONE` 且實際 `rendered_media_validation_result.md = PASS` 才能完成工作流程。

### 必要輸出與 Exit gate
Stage 5 必須建立：

- 依核准順序的四個非空 Scene MP4
- 非空的最終合併 MP4
- `render_manifest.md`
- 由獨立 `rendered_media_validator` 產出的 `rendered_media_validation_result.md = PASS`

Manifest、目前 source 與 Stage 4 gate 必須綁定同一個 code hash；media result 必須涵蓋全部五個 MP4，且所有必要 command、metadata、decode、hash、duration、audio 與順序檢查都通過。

### 失敗路由
- 輸出路徑、渲染命令、concat、manifest 或媒體檢查失敗，且可在不改動 code、上游契約或 layout-affecting profile 的情況下修正：留在 Stage 5，重新建立受影響輸出與 manifest，再完整執行 `DELIVERY_QA`。
- 任何修復需要改動 `generated_algo_scene.py`：立即停止 Stage 5；舊 handoff、layout result、scene review、render manifest 與 media result 全部失效，回到 Stage 4 `CODE_PREPARATION`。
- 任何修復改變 layout-affecting environment/profile：回到 Stage 4 `LAYOUT_VERIFICATION`，取得相同目前 code hash 的新 layout 與 scene review PASS 後，才可重新執行 Stage 5。

## 證據失效矩陣

| 變更或失敗 | 立即失效的證據 | 回復路徑 |
| --- | --- | --- |
| `generated_algo_scene.py` 內容或 SHA-256 改變 | handoff、layout result、scene review、render manifest、rendered-media result | Stage 4 `CODE_PREPARATION`，再依序完成 layout、review 與 Stage 5 |
| Layout runner、Manim 版本、font、frame geometry、quality/profile 或其他影響 layout 的環境改變 | layout result、依賴它的 scene review，以及其後建立的 render manifest 與 rendered-media result | 用目前 code hash 重跑 Stage 4 `LAYOUT_VERIFICATION` 與 `CONTRACT_REVIEW`，再重做 Stage 5 |
| 已核准需求、設計、腳本、旁白、narration manifest 或音訊契約改變 | 變更點之後的所有 Stage gate 與 render/media 證據 | 回到擁有該內容的 Stage，重新通過所有下游 gate |
| `layout_audit_result.md = FAIL`、漏檢任一 Scene 或 hash 不一致 | Stage 4 layout gate 及任何後續證據 | Stage 4 `CODE_PREPARATION` 修正後重跑四幕 layout audit |
| `scene_review_result.md = FAIL`、不獨立或 hash 不一致 | Stage 4 review gate 及任何後續證據 | 交回 writer 修正；若 code 改變，重新建立全部 Stage 4 證據 |
| 任一 Scene／合併 MP4 或 `render_manifest.md` 新建、改寫或重新產生 | 舊 render manifest 與 `rendered_media_validation_result.md` | 保持 code 與 Stage 4 gate 不變，重建 manifest 並重跑 `DELIVERY_QA` |
| `rendered_media_validation_result.md = FAIL` 或媒體輸出檢查失敗 | Stage 5 exit gate | 不改 code/profile 時留在 Stage 5 修復輸出；否則依變更類型回到 Stage 4 |

## 不可接受的捷徑
遇到下列說法時，必須視為違反流程，不能當成可以省略步驟的理由：

| 捷徑 | 必要回應 |
| --- | --- |
| 「可以略過 `DESIGN_DEVELOPMENT`，直接把蒐集的需求交給下游。」 | 不得略過；`COLLECT_REQUIREMENTS` 不能取代共同動畫設計與獨立內容審查。 |
| 「reviewer 在聊天中說沒問題，所以不用建立審查檔。」 | 非正式意見不能取代由獨立 `animation-design-reviewer` 產出的 `animation_design_review.md = PASS`。 |
| 「`animation_design.md` 已經夠詳細，所以可以略過 `SCRIPT`。」 | 仍須執行 `SCRIPT`；場景程式碼不能取代 `teaching_script.md`。 |
| 「先渲染再做 layout 或讓 reviewer 看 code，可以更快確認。」 | 不得先渲染；Stage 4 必須依序取得四幕 `layout_audit_result.md = PASS` 與獨立 `scene_review_result.md = PASS`。 |
| 「渲染能執行，所以等於已經完成審查。」 | 仍須在渲染前由 layout validator 與獨立 scene reviewer 產出同一 code hash 的正式 PASS。 |
| 「交接檔已建立，因此 layout 或獨立場景審查是選用的。」 | Handoff 之後仍須依序完成 `LAYOUT_VERIFICATION` 與 `CONTRACT_REVIEW`，兩者 PASS 後才能渲染。 |
| 「PASS 後只修了一個小錯，可以直接重新渲染。」 | 程式碼變更會使全部 Stage 4 與下游證據失效；必須重建並通過後才能重新渲染。 |
| 「影片已經渲染完成，所以可以略過 `DELIVERY_QA`。」 | 不得略過；必須由獨立 `rendered_media_validator` 建立 `rendered_media_validation_result.md = PASS`。 |
| 「再做一次本機修補，比追查反覆發生的畫面問題更省事。」 | 如果問題顯示前面階段仍有歧義，應退回對應階段處理。 |
| 「為求保險，我現在應該閱讀所有參考資料。」 | 只讀取目前階段要求的資料；遇到指定情況時，再讀取額外參考資料。 |
| 「我已委派這個階段，所以不再負責該關卡。」 | 協調者仍負責階段順序、產物是否存在與通過條件。 |
| 「這個核心設計缺口很小，可以直接在 `SCRIPT` 或 `SCENE_IMPLEMENTATION` 中補上。」 | 不得在下游修補核心設計；退回 `DESIGN_DEVELOPMENT`，重新審查與重新核准。 |
| 「使用者修改設計後，可以沿用舊審查。」 | 不可沿用；更新設計後重新執行內容審查與使用者最終核准。 |

## 完成檢查
在聲稱工作流程完成前，確認：

- `confirmed_requirements.md` 存在，且準確保留使用者來源與來源標籤。
- `animation_design.md` 存在，且完整設計四個獨立 Scene。
- `animation_design_review.md = PASS`，且由獨立的 `animation-design-reviewer` 產出。
- 已取得使用者對完整設計的明確核准。
- `teaching_script.md` 存在。
- `script_review_result.md = PASS`。
- `voiceover.md`、`narration_manifest.json` 與可直接使用的旁白音訊都已完成。
- `generated_algo_scene.py` 存在。
- Stage 4 的 `scene_code_review_handoff.md` 存在，且記錄目前 code hash 與 `Manim render performed: NO`。
- Stage 4 的 `layout_audit_result.md = PASS`，涵蓋依核准順序執行的全部四個 Scene dry-run。
- Stage 4 的 `scene_review_result.md = PASS`，且由獨立 reviewer 在渲染前產出。
- 目前 source、handoff、layout 與 review 的所有 Stage 4 SHA-256 欄位完全一致。
- Stage 5 的四個 Scene MP4、最終合併 MP4 與 `render_manifest.md` 都已建立，且綁定該核准 code hash。
- Stage 5 的 `rendered_media_validation_result.md = PASS`，由獨立 validator 產出並涵蓋全部五個 MP4。
