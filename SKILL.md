---
name: algorithm-teaching-animation-v4
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫 v4

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、製作旁白、實作動畫、獨立檢查、QA 及交付成果。
主要負責的 agent 必須確保所有步驟依序完成，並確認每個階段都符合要求。

## 必要授權
利用此 skill 完成各階段任務需要使用者核准使用 subagent。
若目前對話中尚未取得明確授權，必須詢問：

```text
此任務會在動畫設計完成後使用 `animation-design-reviewer` 執行獨立內容審查，並在後續階段使用 subagent 處理腳本、旁白、動畫實作及品質驗證。你是否同意我在此任務中使用 subagent？請明確回答「同意」或「不同意」(若不同意則無法開始此任務)。
```

只有當使用者明確回答「同意」時，才能開始後續工作。
若使用者回答「不同意」、拒絕授權或未明確表示同意則立即結束工作，不得開始任何後續階段。

## 工作流程
依序執行以下階段：

1. `ANIMATION_DESIGN`
2. `SCRIPT`
3. `VOICEOVER`
4. `RENDER`
5. `QA`
6. `DELIVERY`

開始每個階段前確實閱讀完成目前階段需要的參考資料，不得跳過任何階段，也不得合併、提前或補做後續階段的工作來取代目前階段。
請照各階段的描述完成工作，且該階段規定的必要產物、審查與通過條件都已滿足後，才能進入下一個階段。

## 階段 1：ANIMATION_DESIGN

### 目標
先記錄使用者需求，再由主要 Agent 與使用者共同設計六個獨立 Manim Scene。完成內容審查與使用者最終核准後，直接進入 `SCRIPT`。

### 子階段 1：COLLECT_REQUIREMENTS
此子階段由協調者負責。開始任何行動前，必須完整閱讀並遵循 `references/how-to-collect-requirements.md`，依其要求建立 `confirmed_requirements.md`；不要提前閱讀後續子階段的參考資料。

只有在需求蒐集的完成條件全部成立後，才能進入 `DESIGN_DEVELOPMENT`。

### 子階段 2：DESIGN_DEVELOPMENT
開始前，主要 Agent 必須閱讀 `confirmed_requirements.md`、`references/how-to-design-animation.md`，以及唯一一份符合演算法類型的專用參考，並完整遵循這些文件完成 DESIGN_DEVELOPMENT。

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
要求 `script-writer` 在寫作前閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md` 與 `references/teaching-script.md`。
接著由 `script-writer` 根據已確認需求與已核准設計撰寫可供審查的教學腳本。
腳本必須清楚說明觀眾應學到什麼、各節拍的順序、教學重點與內容如何逐步推進，而且不得加入上游來源中沒有的新意思。
完成 `teaching_script.md` 後，派遣獨立的 custom agent `script-reviewer`，依已確認需求與已核准設計審查腳本。
要求 `script-reviewer` 在審查前閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md`、`teaching_script.md` 與 `references/script-review-checklist.md`。
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
製作符合已確認需求、已核准動畫設計與已通過審查之教學腳本的旁白產物。
旁白是正式流程的一個階段，不是最後才視情況加入的潤飾。

### 委派
此階段必須使用 `voiceover-manifest` subagent。
此階段不需要另外安排獨立審查者。

### 行動前須閱讀
`voiceover-manifest` subagent 必須閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md`、`teaching_script.md`、`script_review_result.md` 與 `references/voiceover.md`。
如果旁白內容似乎與已審查的腳本不一致，協調者應閱讀 `script_review_result.md`。

### 不得開始直到
`confirmed_requirements.md` 已明確記錄配音語言。
`teaching_script.md` 已存在。
`script_review_result.md = PASS`。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。
不得使用尚未審查或未通過審查的腳本。

### 執行事項
派遣 `voiceover-manifest` 製作符合已確認需求、已核准設計與已審查腳本的旁白文字、旁白清單資料及可直接使用的配音檔案。

### 必要輸出
建立 `voiceover.md`、`narration_manifest.json`，以及 `audio/voiceover/` 下可直接使用的旁白音訊。

### 通過／離開關卡
只有在 `voiceover.md`、`narration_manifest.json` 與可直接使用的旁白音訊都已完成，且能交給後續渲染與 QA 使用時，才能前進。

### 發生問題時退回
若需修正旁白用詞或節奏，退回 `VOICEOVER`。
若動畫節拍結構不符，退回 `SCRIPT`。
若配音語言等使用者需求記錄不準確，退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
若核心意思或教學設計本身未決、衝突或不完整，退回 `DESIGN_DEVELOPMENT`，完成共同設計、獨立內容審查與使用者重新核准後再繼續。

## 階段 4：RENDER

### 目標
將已確認需求、已核准動畫設計、已審查腳本與旁白資料實作成場景程式碼與渲染證據。
此階段只能實作已核准的上游內容，不得自行加入新的內容或意思。

### 委派
此階段必須由 `scene-writer` subagent 實作場景並產生渲染證據。
完成 `render_preflight.md` 後，再派遣獨立的 `scene-reviewer` subagent 審查場景。
場景審查者不得撰寫該場景。

### 行動前須閱讀
`scene-writer` 必須閱讀：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- `teaching_script.md`
- `voiceover.md`、`narration_manifest.json` 與 `audio/voiceover/` 下可直接使用的音訊
- `references/manim-guidelines.md`
- `references/render-preflight.md`

只有當渲染結果可能有問題、無法順利安排審查，或不確定問題應退回哪個階段處理時，協調者才閱讀 `references/scene-review-checklist.md` 或 `script_review_result.md`。

### 不得開始直到
`teaching_script.md` 存在且 `script_review_result.md = PASS`。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。
必要的旁白文件與可直接使用的音訊都已存在。
只有在已取得使用 subagent 的明確授權後，才能開始此階段。

### 執行事項
派遣 `scene-writer`，依已確認需求、已核准設計與已審查腳本實作 Manim 場景。
必須實作六個獨立 Manim `Scene` 類別並分別渲染，不得以 `Section` 代替。每個 Scene 結尾淡出至空白，下一個 Scene 再淡入；最後依核准順序合併成一支完整影片。
除非使用者明確要求，場景不得加入上游來源中沒有的新意思、額外的畫面解說、程式碼面板或註解層。
產生最新的渲染結果與對應證據。
使用可確認來自最新 MP4 的證據建立 `render_preflight.md`。
每次重新渲染都會使先前所有最新渲染證據、`render_preflight.md` 與 `scene_review_result.md` 失效。進入 `QA` 前，必須為同一個最新 MP4／版本重新產生證據與預檢，並由獨立的 `scene-reviewer` 重新產出 `PASS`。
準備場景審查所需的交接資訊，包括程式碼與渲染畫面的對應說明、預檢證據，以及受影響的影格資訊。
在 `render_preflight.md` 存在後，派遣 `scene-reviewer` 進行獨立審查。
對於某個 scene/render 的第一次獨立場景審查交接，一律使用 `Full`。
只有範圍明確且局限於 `RENDER` 的變更，並具備有效的受影響影格證據時，才允許差異審查。
受影響影格證據只有在仍適用於受審的明確範圍變更時才有效。
若修正變更已核准語意、腳本節拍順序、全場景結構、全場景版面、渲染對應關係，或以其他方式使受影響影格的證據失效，則退回完整審查。
若受影響影格的範圍擴大或影響不確定，視為受影響影格證據失效，並要求完整的獨立場景審查。

### 必要輸出
建立：

- `generated_algo_scene.py`
- 由最新 MP4 重新產生的渲染證據
- `render_preflight.md`
- 程式碼與渲染畫面的對應說明，或其他足以進行場景審查的交接資訊
- 由獨立審查者產出的 `scene_review_result.md`

### 通過／離開關卡
僅當 `generated_algo_scene.py`、最新渲染證據、`render_preflight.md` 均存在，且 `scene_review_result.md = PASS` 時，才能前進。
`scene_review_result.md` 必須由 `scene-reviewer` 產出，而非 `scene-writer`。
成功完成渲染、本機自行檢查或預檢，都不代表場景已通過審查。

### 發生問題時退回
如果已確認需求、已核准設計與腳本已經寫得很清楚，但場景在樣式、間距、時間、版面或實作內容上未遵守它們，退回 `RENDER`。
如果動畫節拍不符，或腳本不夠完整，導致場景實作者必須自行猜測結構、順序或強調重點，退回 `SCRIPT`。
如果使用者需求記錄不準確，退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
如果演算法行為、教學呈現、Scene 結構或使用者選定的設計有缺口，退回 `DESIGN_DEVELOPMENT`，完成共同設計、獨立內容審查與使用者重新核准後再繼續。不得在 `RENDER` 直接修補設計。

## 階段 5：QA

### 目標
由獨立審查者確認成品是否符合已確認需求、已核准動畫設計、已審查腳本、畫面附加資訊規則與旁白要求。
QA 不只確認影片能否播放，也要確認成品符合上游來源並具備交付條件。

### 委派
此階段必須使用獨立的 `qa-verifier` subagent。
`qa-verifier` 不得參與受審成品的製作。

### 行動前須閱讀
`qa-verifier` 必須閱讀：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- `teaching_script.md`
- 已渲染的媒體輸出
- `render_preflight.md`
- `scene_review_result.md`
- `voiceover.md`、`narration_manifest.json` 與 `audio/voiceover/` 下可直接使用的音訊
- `references/render-qa-checklist.md`

只有當 QA 無法繼續、不同審查結果互相衝突，或不確定問題應退回哪個階段時，協調者才閱讀 `scene_review_result.md` 與 `references/scene-review-checklist.md`。

### 不得開始直到
`scene_review_result.md = PASS` 已存在，並且是正式的檔案審查結果。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。
QA 必須由未參與受審成品製作的獨立審查者執行。
若 `scene_review_result.md` 缺失或不是 `PASS`，QA 不得開始，也不得產出 `qa_result.md`。

若完全沒有 `scene_review_result.md`，應退回 `RENDER` 完成場景審查。
若 `scene_review_result.md` 存在且結果為 `FAIL`，應依該檔案指定的階段處理，不得由 QA 另外決定新的處理路線。

### 執行事項
派遣 `qa-verifier`，依已確認需求、已核准設計與已審查腳本檢查實際渲染成品與所有必要產物。
QA 必須檢查內容意思、視覺清晰度、時間安排、版面、交付內容是否完整、畫面附加資訊是否符合規則、旁白要求與音訊同步。
不得用基本渲染測試、播放檢查或協調者自行檢查取代正式 QA。

### 必要輸出
建立 `qa_result.md`。

### 通過／離開關卡
僅當 `qa_result.md = PASS` 時，才能前進。
沒有 `scene_review_result.md = PASS`，QA 就不能開始。

### 發生問題時退回
若問題出在視覺、時間安排、版面或場景未正確實作上游內容，退回 `RENDER`。
若問題是缺少音訊、旁白語言錯誤、旁白文字偏離腳本，或音訊同步問題來自旁白產物，退回 `VOICEOVER`。
若動畫節拍結構不符，退回 `SCRIPT`。
若成品暴露使用者需求記錄不準確，退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
若成品暴露核心語意、主要心智模型、核心視覺語意、教學弧線或其他核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新審查與重新核准後再繼續。

## 階段 6：DELIVERY

### 目標
提供實際完成的產物與摘要，不得誇大已完成或已通過的項目。
所有交付聲明都必須有已通過的正式關卡檔案作為依據。

### 委派
此階段由協調者處理。
不需交給任何 subagent，也不需安排獨立審查者。

### 行動前須閱讀
閱讀 `qa_result.md`、`scene_review_result.md`、`confirmed_requirements.md` 與已核准的 `animation_design.md`。
只有當交付證據不足時，才閱讀 `references/render-qa-checklist.md`。

### 不得開始直到
`qa_result.md = PASS`。
目前的 `animation_design.md` 已通過內容審查並取得使用者明確核准。

### 執行事項
只回報實際存在的產物，以及有正式檔案佐證的關卡狀態。
交付摘要應與實際完成且已通過關卡的產物相符。

### 必要輸出
產出與實際產物相符的交付摘要。

### 通過／離開關卡
只有當必要產物存在，且有已通過的正式關卡檔案作為依據時，才算完成交付。
若沒有 `qa_result.md = PASS`，不得開始 `DELIVERY`。

### 發生問題時退回
若缺少交付證據或必要產物，退回 `QA`。
若交付摘要顯示使用者需求記錄不準確，退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
若交付摘要顯示成品偏離源自核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新審查與重新核准後再繼續。

## 不可接受的捷徑
遇到下列說法時，必須視為違反流程，不能當成可以省略步驟的理由：

| 捷徑 | 必要回應 |
| --- | --- |
| 「可以略過 `DESIGN_DEVELOPMENT`，直接把蒐集的需求交給下游。」 | 不得略過；`COLLECT_REQUIREMENTS` 不能取代共同動畫設計與獨立內容審查。 |
| 「reviewer 在聊天中說沒問題，所以不用建立審查檔。」 | 非正式意見不能取代由獨立 `animation-design-reviewer` 產出的 `animation_design_review.md = PASS`。 |
| 「`animation_design.md` 已經夠詳細，所以可以略過 `SCRIPT`。」 | 仍須執行 `SCRIPT`；場景程式碼不能取代 `teaching_script.md`。 |
| 「渲染能執行，所以等於已經完成審查。」 | 仍須由獨立審查者產出正式的 `scene_review_result.md`。 |
| 「預檢已通過，因此獨立場景審查是選用的。」 | 在 `render_preflight.md` 存在後執行場景審查。 |
| 「QA 可以由基本渲染測試取代。」 | 仍須執行獨立 QA 並產出 `qa_result.md`。 |
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
- 最新渲染證據存在，且確實來自最新 MP4。
- `render_preflight.md` 存在且引用最新渲染證據。
- `scene_review_result.md = PASS`。
- `qa_result.md = PASS`。
- 交付摘要符合實際產物，且沒有把尚未通過的關卡說成已完成。
