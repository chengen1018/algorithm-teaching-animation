---
name: manim-algorithm-animation-maker
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、製作旁白、實作動畫，並在 `QA` 階段結束。
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
4. `RENDER`
5. `QA`

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
  

## 階段 4：RENDER

### 目標
將已確認需求、已核准動畫設計、已審查腳本與旁白資料實作成場景程式碼；程式碼先通過獨立審查，才能渲染成影片並建立渲染證據。
此階段只能實作已核准的上游內容，不得自行加入新的內容或意思。

### 不得開始直到
`teaching_script.md` 存在且 `script_review_result.md = PASS`。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。
必要的旁白文件與可直接使用的音訊都已存在。
只有在已取得使用 subagent 的明確授權後，才能開始此階段。

### 委派與執行
本階段依委派協定使用兩種角色，並在審查通過後回到原本的 scene-writer subagent 執行最終渲染：

- scene writer 角色規格：`subagent-scene-writer.md` 的絕對路徑
- scene reviewer 角色規格：`subagent-scene-reviewer.md` 的絕對路徑
- 實作與 handoff references：`how-to-implement-and-verify-manim-scenes.md`、`how-to-hand-off-scene-code-for-review.md`
- 程式碼審查 reference：`how-to-review-manim-scene-code.md`
- 最終渲染 reference：`how-to-render-approved-manim-scenes.md`

協調者負責在每次派遣訊息中傳入角色規格要求的所有 project inputs 與上述 skill references 的絕對路徑，安排模式與關卡。

1. 派遣 task name `scene_writer` 的 subagent，明確指定模式 `CODE_PREPARATION`。建立 `generated_algo_scene.py` 與 `scene_code_review_handoff.md`；此時不得執行 Manim render，也不得先產生送審 MP4。
2. `scene-writer` 將已通過 gate 的上游產物視為可執行契約；可合理解讀的細節以最小、保守方式實作，並記錄在 `scene_code_review_handoff.md` 的 `Render Assumptions`。
3. 協調者確認 writer 回報 `DONE`、兩份產物存在且尚未產生本次 MP4 後，派遣 task name `scene_reviewer` 的另一個 subagent。Reviewer 建立 `scene_review_result.md`，審查程式碼與上游契約，不需要 MP4。
4. 若 `scene_review_result.md` 為 `FAIL`，協調者必須將每一項阻塞問題交回 `scene-writer` 修正，然後用最新程式碼重新建立 handoff 並重新審查。本機檢查或預檢都不能取代獨立審查。
5. 只有 reviewer 回報 `DONE` 且實際 `scene_review_result.md` 為 `PASS` 時，才能再次派遣同一個 scene-writer subagent，明確指定模式 `FINAL_RENDER`。此時建立四幕 MP4、合併影片與 `render_manifest.md`。
6. 如果渲染失敗且修復需要改動 `generated_algo_scene.py`，原本的 handoff 與 `scene_review_result.md` 立即失效；必須回到程式碼審查流程取得新 `PASS`，不得直接重新渲染改過的程式碼。
7. 建立 `render_manifest.md` 後，才能完成 `RENDER`。

只有在程式碼審查無法安排或不確定應退回哪個階段時，協調者才閱讀 `references/how-to-review-manim-scene-code.md` 或 `script_review_result.md`。

### 必要輸出
建立：

- `generated_algo_scene.py`
- `scene_code_review_handoff.md`，內含靜態驗證與上游文件對應資訊
- 由獨立審查者產出的 `scene_review_result.md`
- 由通過審查的同一份程式碼產生的四個 Scene MP4 與最終合併 MP4
- `render_manifest.md`

### 通過／離開關卡
僅當 `generated_algo_scene.py`、`scene_code_review_handoff.md`、`scene_review_result.md = PASS`、四個 Scene MP4、最終合併 MP4 與 `render_manifest.md` 均存在，才能進入 `QA`。
`scene_review_result.md` 必須由 `scene-reviewer` 產出，而非 `scene-writer`。
成功完成渲染、本機自行檢查或預檢，都不能取代渲染前的獨立程式碼審查。

### 發生問題時退回
所有程式碼、MP4 產物存在性、實作忠實性或已記錄 assumptions 的問題，都退回 `RENDER` 修正。只要修正涉及程式碼變更，就必須重新通過程式碼審查後才能 render。`RENDER` 不會因上游產物的可合理解讀細節、歧義或衝突而重新啟動上游流程。

## 階段 5：QA

### 目標
使用程式化 layout audit 檢查已渲染版本的可視物件是否超出畫面、互相重疊或形成嚴格包含關係。此階段不以人工播放影片或視覺判斷取代程式檢查。

### 不得開始直到
`RENDER` 的所有必要輸出均已建立。

### 執行事項
依委派協定派遣 task name `layout_auditor` 的 subagent：

- 角色規格：`subagent-layout-auditor.md` 的絕對路徑
- project inputs：`generated_algo_scene.py`、`scene_code_review_handoff.md`、`scene_review_result.md`、`render_manifest.md`
- skill reference：`layout-audit.md` 的絕對路徑
- runner：`run_layout_audit.py` 的絕對路徑

協調者只負責委派、確認必要產物與執行通過／離開關卡。只有 subagent 回報 `DONE`、實際 `layout_audit_result.md` 為 `PASS`，且四幕均已受檢並通過 exit-code 檢查，才能完成工作流程。

開始前完整閱讀 `references/layout-audit.md`。對 `generated_algo_scene.py` 中每一個要交付的 Scene class 執行：

```bash
python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py SceneClass --audit-visible --fail-on-warning --visible-report-level warning
```

使用已通過 RENDER gate 的 `generated_algo_scene.py`，不得為了讓檢查通過而在 QA 中改動程式碼。逐一記錄 Scene class、實際命令、exit code 與完整 audit 輸出。若場景已有明確命名的 layout 群組，依 `references/layout-audit.md` 使用 `scripts/scene_layout_audit.py` 建立場景專用檢查；若需因此修改場景程式碼，先退回 `RENDER`。

### 必要輸出
建立 `layout_audit_result.md`，包含每個交付 Scene class 的命令、exit code、audit 輸出與明確的 `PASS` 或 `FAIL`。

### 通過／離開關卡
僅當所有交付 Scene class 的 audit exit code 都是 `0` 且 `layout_audit_result.md = PASS` 時，才能完成工作流程。不得隱藏、刪除或人工忽略 warning 來取得 PASS。

### 發生問題時退回
任何 audit 執行錯誤、超出畫面或重疊 warning 都使 QA `FAIL`，並退回 `RENDER` 修正。嚴格包含關係在預設 warning 等級下不阻塞；需要調查時可用 `--visible-report-level info` 重新執行並記錄補充資訊。只要修正 `generated_algo_scene.py`，舊 handoff、review result、render manifest 與 layout audit result 全部失效，必須重新完成 `RENDER` 後再執行 QA。

## 不可接受的捷徑
遇到下列說法時，必須視為違反流程，不能當成可以省略步驟的理由：

| 捷徑 | 必要回應 |
| --- | --- |
| 「可以略過 `DESIGN_DEVELOPMENT`，直接把蒐集的需求交給下游。」 | 不得略過；`COLLECT_REQUIREMENTS` 不能取代共同動畫設計與獨立內容審查。 |
| 「reviewer 在聊天中說沒問題，所以不用建立審查檔。」 | 非正式意見不能取代由獨立 `animation-design-reviewer` 產出的 `animation_design_review.md = PASS`。 |
| 「`animation_design.md` 已經夠詳細，所以可以略過 `SCRIPT`。」 | 仍須執行 `SCRIPT`；場景程式碼不能取代 `teaching_script.md`。 |
| 「先渲染再讓 reviewer 看 code，可以更快確認。」 | 不得先渲染；必須先取得獨立 `scene_review_result.md = PASS`。 |
| 「渲染能執行，所以等於已經完成審查。」 | 仍須在渲染前由獨立審查者產出正式的 `scene_review_result.md = PASS`。 |
| 「交接檔已建立，因此獨立場景審查是選用的。」 | 在 `scene_code_review_handoff.md` 存在後執行獨立程式碼審查，且只有 PASS 後才能渲染。 |
| 「PASS 後只修了一個小錯，可以直接重新渲染。」 | 程式碼變更後必須重新審查，才能重新渲染。 |
| 「影片已經渲染完成，所以可以略過 `QA`。」 | 不得略過；必須對所有交付 Scene class 執行程式化 layout audit 並建立 `layout_audit_result.md = PASS`。 |
| 「再做一次本機修補，比追查反覆發生的畫面問題更省事。」 | 如果問題顯示前面階段仍有歧義，應退回對應階段處理。 |
| 「為求保險，我現在應該閱讀所有參考資料。」 | 只讀取目前階段要求的資料；遇到指定情況時，再讀取額外參考資料。 |
| 「我已委派這個階段，所以不再負責該關卡。」 | 協調者仍負責階段順序、產物是否存在與通過條件。 |
| 「這個核心設計缺口很小，可以直接在 `SCRIPT` 或 `RENDER` 中補上。」 | 不得在下游修補核心設計；退回 `DESIGN_DEVELOPMENT`，重新審查與重新核准。 |
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
- `scene_code_review_handoff.md` 存在。
- `scene_review_result.md = PASS`，且由獨立 reviewer 在渲染前產出。
- 四個 Scene MP4、最終合併 MP4 與 `render_manifest.md` 都已建立。
- `layout_audit_result.md = PASS`，涵蓋所有交付 Scene class。
