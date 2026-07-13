---
name: manim-algorithm-animation-maker
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫 v4

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、製作旁白、實作動畫，並在 `RENDER` 階段結束。
主要負責的 agent 必須確保所有步驟依序完成，並確認每個階段都符合要求。

## 必要授權
利用此 skill 完成各階段任務需要使用者核准使用 subagent。
若目前對話中尚未取得明確授權，必須詢問：

```text
此任務會在動畫設計完成後使用 `animation-design-reviewer` 執行獨立內容審查，並在後續階段使用 subagent 處理腳本、旁白、動畫實作及場景審查。你是否同意我在此任務中使用 subagent？請明確回答「同意」或「不同意」(若不同意則無法開始此任務)。
```

只有當使用者明確回答「同意」時，才能開始後續工作。
若使用者回答「不同意」、拒絕授權或未明確表示同意則立即結束工作，不得開始任何後續階段。

## 工作流程
依序執行以下階段：

1. `ANIMATION_DESIGN`
2. `SCRIPT`
3. `VOICEOVER`
4. `RENDER`

開始每個階段前確實閱讀完成目前階段需要的參考資料，不得跳過任何階段，也不得合併、提前或補做後續階段的工作來取代目前階段。
請照各階段的描述完成工作，且該階段規定的必要產物、審查與通過條件都已滿足後，才能進入下一個階段；`RENDER` 是最後一個階段。

## 階段 1：ANIMATION_DESIGN

### 目標
先記錄使用者需求，再由主要 Agent 與使用者共同設計六個獨立 Manim Scene。完成內容審查與使用者最終核准後，直接進入 `SCRIPT`。

### 子階段 1：COLLECT_REQUIREMENTS
此子階段由協調者負責。開始任何行動前，必須完整閱讀並遵循 `references/how-to-collect-requirements.md`，依其要求建立 `confirmed_requirements.md`；不要提前閱讀後續子階段的參考資料。

只有在需求蒐集的完成條件全部成立後，才能進入 `DESIGN_DEVELOPMENT`。

### 子階段 2：DESIGN_DEVELOPMENT
開始前，主要 Agent 必須閱讀 `confirmed_requirements.md` 與 `references/how-to-design-animation.md`，並依該指南的「專用參考選擇」讀取唯一一份相符的專用參考；若沒有相符類型，則只使用共通指南。完整遵循這些文件完成 DESIGN_DEVELOPMENT。

只有當 `references/how-to-design-animation.md` 定義的完成條件全部成立後，才能離開 `ANIMATION_DESIGN` 並開始 `SCRIPT`。

### 回退規則
遇到問題時，依下列規則回退：

- 若來源擷取不準確、遺漏使用者原始措辭，或來源標籤錯誤發生在需求蒐集，退回 `COLLECT_REQUIREMENTS` 修正 `confirmed_requirements.md`，再把修正後的來源重新送回設計流程。
- 若演算法行為、教學呈現、Scene 結構或使用者選定的設計有缺漏或衝突，退回 `DESIGN_DEVELOPMENT`，重新執行該子階段。

## 階段 2：SCRIPT

### 目標
將已確認的需求與已核准動畫設計整理成適合教學的動畫節拍與內容順序。

### 不得開始直到
`confirmed_requirements.md` 已存在。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。

### 執行事項
派遣 custom agent `script-writer` 建立教學腳本。
要求 `script-writer` 在寫作前閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md` 與 `references/how-to-write-teaching-script.md`。
接著讓 `script-writer` 撰寫可供審查的教學腳本。
腳本必須清楚說明觀眾應學到什麼、各節拍的順序、教學重點與內容如何逐步推進，而且不得加入上游來源中沒有的新意思。
完成 `teaching_script.md` 後，派遣獨立的 custom agent `script-reviewer`，依已確認需求與已核准設計審查腳本。
要求 `script-reviewer` 在審查前閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md` 與 `teaching_script.md`。
腳本審查者不得撰寫該腳本。

### 必要輸出
建立 `teaching_script.md`。
提供足夠的審查資訊，讓 `script-reviewer` 能依已確認需求與已核准設計評估腳本。
透過獨立審查者建立 `script_review_result.md`。

### 通過／離開關卡
僅當 `teaching_script.md` 存在且 `script_review_result.md = PASS` 時，才能前進。
審查結果必須由 `script-reviewer` 產出，而非 `script-writer`。

### 發生問題時退回
若問題只在腳本的內容順序、表達或對上游來源的遵循，退回 `SCRIPT`。
若腳本暴露使用者需求記錄不準確，退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
若腳本暴露演算法行為、教學呈現、Scene 結構或使用者選定的設計有缺口，退回 `DESIGN_DEVELOPMENT`，完成共同設計、獨立內容審查與使用者重新核准後再繼續。不得在 `SCRIPT` 直接修補設計。

## 階段 3：VOICEOVER

### 目標
根據已通過審查的教學腳本，產生每個 beat 的旁白文字與實際音訊。

### 由誰執行
此階段交給 `voiceover-generator` custom agent 處理，詳細工作規則以 `.codex/agents/voiceover-generator.toml` 為準。
協調者只負責安排流程與確認關卡，不得更改其規則。

### 這個階段要產出什麼
- `voiceover.md`：每個 beat 的旁白文字稿。
- `narration_manifest.json`：包含每個 beat 的音訊驗證數據。
- `audio/voiceover/` 資料夾：每個 beat 已通過驗證的旁白音訊。

### 什麼時候才算完成
以上三樣產物都存在，且每個音檔都已通過驗證，才能進入下一個階段。
若有任何音檔生成失敗或驗證不通過，必須在此階段修正，不能以靜音或其他替代方案過關，直到所有音檔都已通過驗證，本階段才算完成。
  

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
本階段依序交給兩個 custom agent 處理，並在審查通過後再回到 `scene-writer` 執行最終渲染：`scene-writer` 負責寫程式碼與渲染已通過審查的版本，`scene-reviewer` 負責獨立程式碼審查。兩者的詳細工作規則以 `.codex/agents/scene-writer.toml` 與 `.codex/agents/scene-reviewer.toml` 為準；協調者負責安排流程、核對程式碼版本與確認關卡。

1. 先交由 `scene-writer` 建立 `generated_algo_scene.py`，完成靜態 audit，並建立 `scene_code_review_handoff.md`。此時不得執行 Manim render，也不得先產生送審 MP4。
2. `scene-writer` 將已通過 gate 的上游產物視為可執行契約；可合理解讀的細節以最小、保守方式實作，並記錄在 `scene_code_review_handoff.md` 的 `Render Assumptions`。
3. 只有在 `generated_algo_scene.py`、`scene_code_review_handoff.md` 與程式碼審查交接資料都已完成後，才能交由獨立的 `scene-reviewer` 審查。Reviewer 審查程式碼與上游契約，不需要 MP4。
4. 若 `scene_review_result.md` 為 `FAIL`，協調者必須將每一項阻塞問題交回 `scene-writer` 修正，然後用最新程式碼重新建立 handoff 並重新審查。本機檢查或預檢都不能取代獨立審查。
5. 只有當 `scene_review_result.md = PASS`，且其 Reviewed Code SHA-256 與目前 `generated_algo_scene.py` 完全一致時，才能再交由 `scene-writer` 依 `references/how-to-render-approved-manim-scenes.md` 執行六幕渲染、合併影片與建立 `render_manifest.md`。
6. 如果渲染失敗且修復需要改動 `generated_algo_scene.py`，原本的 handoff 與 `scene_review_result.md` 立即失效；必須回到程式碼審查流程取得新 `PASS`，不得直接重新渲染改過的程式碼。
7. 建立 `render_manifest.md` 後不得再改動程式碼；manifest、handoff 與 review result 的 Code SHA-256 必須一致，才能完成 `RENDER`。

只有在程式碼審查無法安排或不確定應退回哪個階段時，協調者才閱讀 `references/how-to-review-manim-scene-code.md` 或 `script_review_result.md`。

### 必要輸出
建立：

- `generated_algo_scene.py`
- `scene_code_review_handoff.md`，內含受審程式碼的 SHA-256、靜態驗證與上游文件對應資訊
- 由獨立審查者產出的 `scene_review_result.md`
- 由通過審查的同一份程式碼產生的六個 Scene MP4 與最終合併 MP4
- `render_manifest.md`

### 通過／離開關卡
僅當 `generated_algo_scene.py`、`scene_code_review_handoff.md`、`scene_review_result.md = PASS`、六個 Scene MP4、最終合併 MP4 與 `render_manifest.md` 均存在，且三份紀錄的 Code SHA-256 完全一致時，才算完成工作流程。
`scene_review_result.md` 必須由 `scene-reviewer` 產出，而非 `scene-writer`。
成功完成渲染、本機自行檢查或預檢，都不能取代渲染前的獨立程式碼審查。

### 發生問題時退回
所有程式碼、MP4 產物存在性、實作忠實性或已記錄 assumptions 的問題，都退回 `RENDER` 修正。只要修正涉及程式碼變更，就必須重新通過程式碼審查後才能 render。`RENDER` 不會因上游產物的可合理解讀細節、歧義或衝突而重新啟動上游流程。

## 不可接受的捷徑
遇到下列說法時，必須視為違反流程，不能當成可以省略步驟的理由：

| 捷徑 | 必要回應 |
| --- | --- |
| 「可以略過 `DESIGN_DEVELOPMENT`，直接把蒐集的需求交給下游。」 | 不得略過；`COLLECT_REQUIREMENTS` 不能取代共同動畫設計與獨立內容審查。 |
| 「reviewer 在聊天中說沒問題，所以不用建立審查檔。」 | 非正式意見不能取代由獨立 `animation-design-reviewer` 產出的 `animation_design_review.md = PASS`。 |
| 「`animation_design.md` 已經夠詳細，所以可以略過 `SCRIPT`。」 | 仍須執行 `SCRIPT`；場景程式碼不能取代 `teaching_script.md`。 |
| 「先渲染再讓 reviewer 看 code，可以更快確認。」 | 不得先渲染；必須先取得與目前 code hash 一致的 `scene_review_result.md = PASS`。 |
| 「渲染能執行，所以等於已經完成審查。」 | 仍須在渲染前由獨立審查者產出正式的 `scene_review_result.md = PASS`。 |
| 「交接檔已建立，因此獨立場景審查是選用的。」 | 在 `scene_code_review_handoff.md` 存在後執行獨立程式碼審查，且只有 PASS 後才能渲染。 |
| 「PASS 後只修了一個小錯，可以直接重新渲染。」 | 任何程式碼變更都會使舊 PASS 失效；必須對新 hash 重新審查。 |
| 「再做一次本機修補，比追查反覆發生的畫面問題更省事。」 | 如果問題顯示前面階段仍有歧義，應退回對應階段處理。 |
| 「為求保險，我現在應該閱讀所有參考資料。」 | 只讀取目前階段要求的資料；遇到指定情況時，再讀取額外參考資料。 |
| 「我已委派這個階段，所以不再負責該關卡。」 | 協調者仍負責階段順序、產物是否存在與通過條件。 |
| 「這個核心設計缺口很小，可以直接在 `SCRIPT` 或 `RENDER` 中補上。」 | 不得在下游修補核心設計；退回 `DESIGN_DEVELOPMENT`，重新審查與重新核准。 |
| 「使用者修改設計後，可以沿用舊審查。」 | 不可沿用；更新設計後重新執行內容審查與使用者最終核准。 |

## 完成檢查
在聲稱工作流程完成前，確認：

- `confirmed_requirements.md` 存在，且準確保留使用者來源與來源標籤。
- `animation_design.md` 存在，且完整設計六個獨立 Scene。
- `animation_design_review.md = PASS`，且由獨立的 `animation-design-reviewer` 產出。
- 已取得使用者對完整設計的明確核准。
- `teaching_script.md` 存在。
- `script_review_result.md = PASS`。
- `voiceover.md`、`narration_manifest.json` 與可直接使用的旁白音訊都已完成。
- `generated_algo_scene.py` 存在。
- `scene_code_review_handoff.md` 存在，且正確識別受審程式碼版本。
- `scene_review_result.md = PASS`，且由獨立 reviewer 在渲染前產出。
- 六個 Scene MP4、最終合併 MP4 與 `render_manifest.md` 都已建立。
- handoff、review result、render manifest 的 Code SHA-256 與目前 `generated_algo_scene.py` 完全一致。
