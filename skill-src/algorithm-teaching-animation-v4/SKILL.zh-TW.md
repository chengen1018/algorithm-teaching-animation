---
name: algorithm-teaching-animation-v3
description: 當使用者要求以 Manim 將演算法名稱、範例輸入或執行過程製作成完整的動畫時使用。適用於需要規劃、實作、渲染及驗證動畫成品的任務；不適用於純文字演算法解說、一般非演算法動畫，或只修改既有場景的局部需求。
---

# 演算法教學動畫 v3

## 概述
此 skill 用來把使用者的演算法需求製作成完整的 Manim 教學動畫。整個製作過程包含動畫設計、撰寫教學腳本、視需要製作旁白、實作動畫、獨立檢查、QA 及交付成果。
主要負責的 agent 必須確保所有步驟依序完成，並確認每個階段都符合要求。

## 必要授權
利用此 skill 完成各階段任務需要使用者核准使用 subagent。
若目前對話中尚未取得明確授權，必須原文詢問：

```text
此任務需要使用 subagent，由 `animation-designer` 執行動畫設計、`animation-design-reviewer` 執行獨立動畫設計審查，再由下游角色分別執行內容撰寫、審查、旁白製作、動畫實作及品質驗證。你是否同意我在此任務中使用 subagent？請明確回答「同意」或「不同意」(若不同意則無法開始此任務)。
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

不得跳過任何階段。
開始每個階段前，先確認該階段列出的前置條件都已完成。
只讀取目前階段需要的參考資料；除非遇到問題且規則明確要求，否則不要提前讀取後續階段的資料。
如果在後續階段發現前面階段的決定不清楚、有錯誤或缺少必要資訊，不要直接在目前階段修補。應回到問題所屬的階段完成修正，再依序繼續。

## 委派規則
當某個階段要求使用特定 subagent 時，必須由該 subagent 執行指定工作。
即使工作已交給 subagent，協調者仍須負責確認階段順序、必要產物、通過條件，以及發生問題時應退回哪個階段。當某個階段要求獨立審查時，必須等受審產物完成後，再派遣指定的審查者，且審查者不得是受審產物的作者。

依照各階段的「行動前須閱讀」章節讀取所需資料。
只有當產物可能有問題、關卡未通過，或不確定應退回哪個階段時，協調者才讀取額外的參考資料。

## 產物順序
正常情況下，工作流程會依序產生以下產物：

```text
intake_summary.md
animation_design.md
animation_design_review.md
pre_build_brief.md
teaching_script.md
script_review_result.md
voiceover.md
narration_manifest.json
audio/voiceover/
generated_algo_scene.py
render_preflight.md
scene_review_result.md
qa_result.md
```

若交付層級為 `no narration`，已核准的 `pre_build_brief.md` 必須明確說明不需要旁白，也不需要任何配音檔案。
此時不需要 `voiceover.md`、`narration_manifest.json`，也不需要 `audio/voiceover/` 下的檔案。

若交付層級為 `final narrated delivery`，在渲染與 QA 通過前，必須完成 `voiceover.md`、`narration_manifest.json`，以及 `audio/voiceover/` 下可直接使用的旁白音訊。

## 全程適用的規則
以下規則適用於整個工作流程：

- 本文件 `SKILL.zh-TW.md` 是目前中文流程的主要契約。
- `references/*.md` 補充各階段的執行細節；`agents/*.md` 規範各角色的工作方式。兩者均不得覆蓋或改變本契約。
- `SKILL.zh-TW.md` 與 `SKILL.md` 必須維持語意同步。
- 即使支援檔案漏讀、工作已委派、渲染成功或已有非正式審查意見，也不得略過 `SKILL.zh-TW.md` 規定的階段、產物或正式關卡。
- 除非使用者明確要求，否則不得新增契約以外的畫面解說、程式碼面板或註解層。
- 所有審查與 QA 都必須以各階段指定的正式關卡檔案為準。
- 下游若發現使用者來源擷取不準確，退回 `INTAKE`；若發現核心語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線或其他核心設計缺口，退回 `DESIGN_DEVELOPMENT` 並重新審查與重新核准；若問題只在 brief 的文字、來源標籤或忠實轉換，退回 `CONTRACT`。只有指稱整個第一個頂層階段時才使用 `ANIMATION_DESIGN`。

## 階段 1：ANIMATION_DESIGN

### 目標
先準確記錄使用者來源，再完成動畫的教學與視覺設計、獨立審查、精確版本的外部核准，以及忠實的下游實作契約轉換。
在腳本、旁白或場景製作開始前，只有這個階段可以定義或修改核心語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線或高階動畫節拍。

### 委派
協調者負責 `INTAKE`、面向使用者的逐題提問、忠實記錄回答，以及所有外部核准關卡。
必須派遣 `animation-designer` 負責 `DESIGN_DEVELOPMENT`、建立或修訂 `animation_design.md`，並在設計通過精確版本核准後負責 `CONTRACT` 的忠實轉換。
必須在設計者完成 `DESIGN_READY` 後，另行派遣獨立的 `animation-design-reviewer` 審查。審查者不得參與該版本設計的撰寫、修訂或修復。

### 行動前須閱讀
`INTAKE` 前，協調者閱讀 `references/intake-contract.md`。
`DESIGN_DEVELOPMENT` 前，`animation-designer` 依其角色契約閱讀 `references/high-impact-clarification.md`、共用設計參考、視覺參考，以及符合演算法類型時唯一一份相符的類型參考。
設計審查前，`animation-design-reviewer` 閱讀 `references/animation-design-review-checklist.md`，並使用與設計者相同的參考路由。
`CONTRACT` 前，`animation-designer` 閱讀 `references/pre-build-brief.md`。
不要只因為「可能會用到」就提前閱讀後續階段的參考資料。

### 子階段 1：INTAKE
協調者準確擷取使用者提出的演算法、版本或情境、範例輸入、目標受眾、教學目標、動畫需求、交付層級、限制、禁止事項及先前決定，並保留會影響語意、教學、交付或驗收的原始措辭與來源標籤。
依 `references/intake-contract.md` 建立 `intake_summary.md`，清楚區分使用者來源與 agent 分析。
`INTAKE` 只負責記錄、分類與提出非約束性的候選教學方向；不得完成動畫設計，不得凍結核心視覺語意、場景結構、資訊層級、教學弧線或高階節拍。

### 子階段 2：DESIGN_DEVELOPMENT
派遣 `animation-designer` 規劃小批、彼此密切相關的核心問題，並實際設計演算法動畫。設計至少涵蓋演算法版本與操作語意、教學目標、要預防的觀眾誤解、主要心智模型及其界線、範例與教學理由、核心視覺隱喻與穩定視覺語意、資料結構呈現、場景結構、資訊層級、教學弧線、高階動畫節拍，以及明確的建議、理由、實質替代方案與取捨。

協調者每次只向使用者提出一個問題、忠實記錄並轉交回答，不負責設計問題清單或動畫設計。不得以設計者的建議取代使用者決定。完成整批問題後，將完整回答一次交回 `animation-designer`，不得每取得一個回答就要求設計者更新。
只要仍有會實質改變演算法語意、主要心智模型、核心視覺語意、教學弧線、場景結構或高階節拍的阻塞問題，就繼續下一個小批次。低影響細節不得阻塞設計；採用合理的 best-effort 預設值並記錄風險後繼續。

`animation-designer` 依 `references/animation-design-document.md` 建立 `animation_design.md`，完成規範中的 `DESIGN_READY` 條件自我檢查，且只有在全部通過、沒有阻塞核心問題時才能交出 `DESIGN_READY`。
接著派遣獨立的 `animation-design-reviewer`，由其建立唯一的正式審查產物 `animation_design_review.md`。審查必須以 `references/animation-design-process.md` 規範中的 `DESIGN_READY` 條件建立完整證據矩陣，並依變更影響採用 `Full` 或可完整追蹤的 `Delta` 路由；初次審查，以及演算法語意、主要心智模型、核心視覺隱喻或語意、教學弧線、場景結構、高階節拍或影響不明的變更，必須使用 `Full`。

審查者在審查開始與結束前都必須對實際受審的 `animation_design.md` 位元組內容計算 SHA-256，並在 `PASS` 結果中記錄 `Reviewed Design SHA-256`。只有 `animation_design_review.md = PASS` 後，協調者才能請求使用者明確核准該精確受審版本；核准記錄必須在 `animation_design.md` 外部保存 `Approved Design SHA-256` 與明確的使用者核准參照。
使用者可以直接編輯 `animation_design.md`；每次這種直接編輯都會建立新版本並使先前的審查與核准失效，且依變更影響套用 Full 或 Delta 重新審查規則。先前的 `pre_build_brief.md`、其 `Source Design SHA-256` 血緣記錄與其核准也會失效。任何新版本都必須退回 `DESIGN_DEVELOPMENT`，依影響重新進行完整或差異審查、取得 `PASS`，由使用者重新明確核准，再重新產生 `pre_build_brief.md`、建立新的外部血緣記錄並另行核准；沉默、未回覆、編輯檔案本身或核准其他版本都不算核准。

### 子階段 3：CONTRACT
只有在目前 `animation_design.md` 的精確版本已由獨立審查取得 `PASS`、使用者已明確核准相同版本，且下列值完全收斂時，才能派遣 `animation-designer` 忠實轉換為 `pre_build_brief.md`：

```text
Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

`Source Design SHA-256` 在轉換前尚非必要。忠實轉換期間，將它記錄於外部 `CONTRACT` 血緣記錄，其值必須是用來產生 `pre_build_brief.md` 的精確目前 `Approved Design SHA-256`；不得將血緣或核准中繼資料寫入 `animation_design.md` 或 `pre_build_brief.md`。
轉換可以整理、濃縮與標示已核准決定的來源，但不得新增、修補或默默決定任何核心語意、心智模型、核心視覺語意、場景結構、教學弧線或高階節拍。
完成轉換後、請求 brief 核准前，重新計算目前設計的 SHA-256，並要求 `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`。接著協調者必須另外請求使用者明確核准 `pre_build_brief.md` 的精確版本。設計核准不能取代 `pre_build_brief.md` 的核准；外部核准記錄必須保存 `Approved Brief SHA-256` 與明確的使用者核准參照，不得將核准狀態或中繼資料寫入 brief。
每次編輯 `pre_build_brief.md` 都使先前核准失效，必須重新檢查忠實轉換並取得新版本的明確核准。緊接在開始 `SCRIPT` 前，重新計算目前設計與 brief 的 SHA-256，並要求：

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
Approved Brief SHA-256 = current pre_build_brief.md SHA-256
```

### 必要輸出
建立：

- `intake_summary.md`
- `animation_design.md`
- 由獨立審查者產出的 `animation_design_review.md`，且 verdict 為 `PASS`
- `pre_build_brief.md`

### 通過／離開關卡
僅當下列條件全部成立，才能離開 `ANIMATION_DESIGN` 並開始 `SCRIPT`：

- `intake_summary.md` 存在，且使用者來源已準確保留。
- `animation_design.md` 存在並已交出 `DESIGN_READY`。
- `animation_design_review.md = PASS`，且由獨立的 `animation-design-reviewer` 產出。
- `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`。
- 已取得使用者對該精確受審設計版本的明確外部核准。
- `pre_build_brief.md` 存在，且是該核准設計的忠實轉換。
- `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`。
- 已另外取得使用者對該精確 brief 版本的明確外部核准。

非正式 reviewer 留言、聊天中的口頭意見或協調者自行檢查，都不能取代檔案化的 `animation_design_review.md = PASS`。

### 回退規則
若來源擷取不準確、遺漏使用者原始措辭，或來源標籤錯誤發生在 intake，退回 `INTAKE` 修正 `intake_summary.md`，再將修正後的來源重新送入設計流程。
若發現演算法核心語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高階節拍或其他核心設計缺口，或 `animation_design.md` 有任何變更，退回 `DESIGN_DEVELOPMENT`。修正後必須重新完成 `DESIGN_READY`、適當的完整或差異獨立審查、檔案化 `PASS`、SHA-256 收斂，以及精確版本的使用者重新核准；既有的 `pre_build_brief.md`、其 `Source Design SHA-256` 血緣記錄與其核准失效，必須重新產生 brief、建立新的外部血緣記錄並另行核准。
若問題只涉及 brief 的文字、格式、來源標籤或忠實轉換，且不改變已核准設計的意思，留在或退回 `CONTRACT`，修正後重新檢查忠實轉換、更新 `Source Design SHA-256`，並取得新 SHA-256 的 `pre_build_brief.md` 核准。
若 `CONTRACT` 暴露缺漏、衝突或實質模糊的核心決定，停止轉換並退回 `DESIGN_DEVELOPMENT`；不得在 brief 中補做設計。

## 階段 2：SCRIPT

### 目標
將已核准的 `pre_build_brief.md` 整理成適合教學的動畫節拍與內容順序。

### 不得開始直到
已核准的 `pre_build_brief.md` 存在。
緊接在開始本階段前，已重新計算目前設計與 brief 的 SHA-256，且 `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`、`Approved Brief SHA-256 = current pre_build_brief.md SHA-256`；另有該精確版本的外部 `pre_build_brief.md` 明確核准記錄。

### 執行事項
派遣 `script-writer` subagent 建立教學腳本。
要求 `script-writer` 在寫作前閱讀已核准的 `pre_build_brief.md` 與 `references/teaching-script.md`。
接著由 `script-writer` 根據已核准的 `pre_build_brief.md` 撰寫可供審查的教學腳本。
腳本必須清楚說明觀眾應學到什麼、各節拍的順序、教學重點與內容如何逐步推進，而且不得加入契約中沒有的新意思。
完成 `teaching_script.md` 後，派遣獨立的 `script-reviewer` subagent，依已核准的 `pre_build_brief.md` 審查腳本。
要求 `script-reviewer` 在審查前閱讀已核准的 `pre_build_brief.md`、`teaching_script.md` 與 `references/script-review-checklist.md`。
腳本審查者不得撰寫該腳本。

### 必要輸出
建立 `teaching_script.md`。
提供足夠的審查資訊，讓 `script-reviewer` 能依已核准的 `pre_build_brief.md` 評估腳本。
透過獨立審查者建立 `script_review_result.md`。

### 通過／離開關卡
僅當 `teaching_script.md` 存在且 `script_review_result.md = PASS` 時，才能前進。
審查結果必須由 `script-reviewer` 產出，而非 `script-writer`。

### 發生問題時退回
若問題只在腳本的內容順序、表達或對 brief 的遵循，退回 `SCRIPT`。
若腳本暴露 brief 的文字、來源標籤或忠實轉換錯誤，退回 `CONTRACT`，修正並重新取得精確版本的 brief 核准。
若腳本暴露核心語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高階節拍或其他核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新設計、獨立審查、設計重新核准、`CONTRACT` 轉換並另行核准 `pre_build_brief.md` 後再繼續。不得在 `SCRIPT` 直接修補核心設計。

## 階段 3：VOICEOVER

### 目標
製作符合已核准 `pre_build_brief.md` 與已通過審查之教學腳本的旁白產物。
旁白是正式流程的一個階段，不是最後才視情況加入的潤飾。

### 委派
如果已核准的交付層級包含旁白，此階段必須使用 `voiceover-manifest` subagent。
此階段不需要另外安排獨立審查者。

### 行動前須閱讀
`voiceover-manifest` subagent 必須閱讀已核准的 `pre_build_brief.md`、`teaching_script.md`、`script_review_result.md` 與 `references/voiceover.md`。
如果旁白內容似乎與已審查的腳本不一致，協調者應閱讀 `script_review_result.md`。

### 不得開始直到
交付層級已確認，不再變更。
`teaching_script.md` 已存在。
`script_review_result.md = PASS`。
如果需要旁白，不得使用尚未審查或未通過審查的腳本。

### 執行事項
若已核准的交付層級為 `no narration`，確認已核准的 `pre_build_brief.md` 明確說明不需要旁白，也不需要任何配音檔案。
不得只為了湊齊產物清單而建立沒有實際用途的旁白佔位檔案。

若已核准的交付層級為 `final narrated delivery`，派遣 `voiceover-manifest` 製作符合 `pre_build_brief.md` 與已審查腳本的旁白文字、旁白清單資料及可直接使用的配音檔案。

### 必要輸出
若為 `no narration`，不需額外的旁白產物。
若為 `final narrated delivery`，建立 `voiceover.md`、`narration_manifest.json`，以及 `audio/voiceover/` 下可直接使用的旁白音訊。

### 通過／離開關卡
若為 `no narration`，僅當已核准的 `pre_build_brief.md` 明確說明不需旁白，也不需要任何配音檔案時，才能前進。
若為 `final narrated delivery`，只有在 `voiceover.md`、`narration_manifest.json` 與可直接使用的旁白音訊都已完成，且能交給後續渲染與 QA 使用時，才能前進。

### 發生問題時退回
若需修正旁白用詞或節奏，退回 `VOICEOVER`。
若動畫節拍結構不符，退回 `SCRIPT`。
若已核准設計已明確定義交付層級或旁白義務，但 brief 的文字、來源標籤或忠實轉換有誤，退回 `CONTRACT`，修正並重新取得精確版本的 brief 核准。
若交付層級、核心意思或教學設計本身未決、衝突或不完整，退回 `DESIGN_DEVELOPMENT`，完成重新設計、獨立審查、設計重新核准、`CONTRACT` 轉換並另行核准 `pre_build_brief.md` 後再繼續。

## 階段 4：RENDER

### 目標
將已核准的 `pre_build_brief.md`、已審查腳本與必要的旁白資料，實作成場景程式碼與渲染證據。
此階段只能實作已核准的契約，不得自行加入新的內容或意思。

### 委派
此階段必須由 `scene-writer` subagent 實作場景並產生渲染證據。
完成 `render_preflight.md` 後，再派遣獨立的 `scene-reviewer` subagent 審查場景。
場景審查者不得撰寫該場景。

### 行動前須閱讀
`scene-writer` 必須閱讀：

- 已核准的 `pre_build_brief.md`
- `teaching_script.md`
- 需要旁白時的 `voiceover.md`、`narration_manifest.json` 與 `audio/voiceover/` 下可直接使用的音訊
- `references/manim-guidelines.md`
- `references/render-preflight.md`

只有當渲染結果可能有問題、無法順利安排審查，或不確定問題應退回哪個階段處理時，協調者才閱讀 `references/scene-review-checklist.md` 或 `script_review_result.md`。

### 不得開始直到
`teaching_script.md` 存在且 `script_review_result.md = PASS`。
目前 `pre_build_brief.md` 仍等於已另外核准的精確版本，且 `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`。
若為 `no narration`，已核准的 `pre_build_brief.md` 明確說明不需旁白，也不需要任何配音檔案。
若交付層級需要旁白，必要的旁白文件與可直接使用的音訊都已存在。
只有在已取得使用 subagent 的明確授權後，才能開始此階段。

### 執行事項
派遣 `scene-writer`，依已核准的契約與已審查腳本實作 Manim 場景。
除非使用者明確要求，場景不得加入契約中沒有的新意思、額外的畫面解說、程式碼面板或註解層。
產生最新的渲染結果與對應證據。
使用可確認來自最新 MP4 的證據建立 `render_preflight.md`。
每次重新渲染都會使先前所有最新渲染證據、`render_preflight.md` 與 `scene_review_result.md` 失效。進入 `QA` 前，必須為同一個最新 MP4／版本重新產生證據與預檢，並由獨立的 `scene-reviewer` 重新產出 `PASS`。
準備場景審查所需的交接資訊，包括程式碼與渲染畫面的對應說明、預檢證據，以及受影響的影格資訊。
在 `render_preflight.md` 存在後，派遣 `scene-reviewer` 進行獨立審查。
場景審查失敗後，下一次預設只審查修改差異。
若修正變更已核准語意、腳本節拍順序、交付層級、已核准契約、全場景結構、全場景版面、渲染對應關係，或以其他方式使受影響影格的證據失效，則退回完整審查。

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
如果已核准的 `pre_build_brief.md` 與腳本已經寫得很清楚，但場景在樣式、間距、時間、版面或實作內容上未遵守它們，退回 `RENDER`。
如果動畫節拍不符，或腳本不夠完整，導致場景實作者必須自行猜測結構、順序或強調重點，退回 `SCRIPT`。
如果已核准設計清楚，但 brief 的文字、來源標籤或忠實轉換不完整，退回 `CONTRACT`，修正並重新取得精確版本的 brief 核准。
如果仍有未解決的核心語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線或其他核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新設計、獨立審查、設計重新核准、`CONTRACT` 轉換並另行核准 `pre_build_brief.md` 後再繼續。不得在 `RENDER` 直接修補核心設計。

## 階段 5：QA

### 目標
由獨立審查者確認成品是否符合已核准的 `pre_build_brief.md`、已審查腳本、選定的交付層級、畫面附加資訊規則與旁白要求。
QA 不只確認影片能否播放，也要確認成品符合契約並具備交付條件。

### 委派
此階段必須使用獨立的 `qa-verifier` subagent。
`qa-verifier` 不得參與受審成品的製作。

### 行動前須閱讀
`qa-verifier` 必須閱讀：

- 已核准的 `pre_build_brief.md`
- `teaching_script.md`
- 已渲染的媒體輸出
- `render_preflight.md`
- `scene_review_result.md`
- 需要旁白時的 `voiceover.md`、`narration_manifest.json` 與 `audio/voiceover/` 下可直接使用的音訊
- `references/render-qa-checklist.md`

只有當 QA 無法繼續、不同審查結果互相衝突，或不確定問題應退回哪個階段時，協調者才閱讀 `scene_review_result.md` 與 `references/scene-review-checklist.md`。

### 不得開始直到
`scene_review_result.md = PASS` 已存在，並且是正式的檔案審查結果。
目前 `pre_build_brief.md` 仍等於已另外核准的精確版本，且 `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`。
QA 必須由未參與受審成品製作的獨立審查者執行。
若 `scene_review_result.md` 缺失或不是 `PASS`，QA 不得開始，也不得產出 `qa_result.md`。

若完全沒有 `scene_review_result.md`，應退回 `RENDER` 完成場景審查。
若 `scene_review_result.md` 存在且結果為 `FAIL`，應依該檔案指定的階段處理，不得由 QA 另外決定新的處理路線。

### 執行事項
派遣 `qa-verifier`，依已核准的契約檢查實際渲染成品與所有必要產物。
QA 必須檢查內容意思、視覺清晰度、時間安排、版面、交付內容是否完整、畫面附加資訊是否符合規則、旁白要求，以及有旁白時的音訊同步。
不得用基本渲染測試、播放檢查或協調者自行檢查取代正式 QA。

### 必要輸出
建立 `qa_result.md`。

### 通過／離開關卡
僅當 `qa_result.md = PASS` 時，才能前進。
沒有 `scene_review_result.md = PASS`，QA 就不能開始。

### 發生問題時退回
若問題出在視覺、時間安排、版面或場景未正確實作契約，退回 `RENDER`。
若問題是缺少音訊、旁白語言錯誤、旁白文字偏離腳本，或音訊同步問題來自旁白產物，退回 `VOICEOVER`。
若動畫節拍結構不符，退回 `SCRIPT`。
若成品偏離源自 brief 的文字、來源標籤或忠實轉換錯誤，退回 `CONTRACT`，修正並重新取得精確版本的 brief 核准。
若成品暴露核心語意、主要心智模型、核心視覺語意、教學弧線或其他核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新審查、重新核准與後續 `CONTRACT` 關卡後再繼續。

## 階段 6：DELIVERY

### 目標
依已核准的交付層級提供正確的產物與摘要，不得誇大已完成或已通過的項目。
所有交付聲明都必須有已通過的正式關卡檔案作為依據。

### 委派
此階段由協調者處理。
不需交給任何 subagent，也不需安排獨立審查者。

### 行動前須閱讀
閱讀 `qa_result.md`、`scene_review_result.md` 與已核准的 `pre_build_brief.md`。
只有當交付證據不足，或不確定交付內容是否符合指定層級時，才閱讀 `references/render-qa-checklist.md`。

### 不得開始直到
`qa_result.md = PASS`。
目前 `pre_build_brief.md` 仍等於已另外核准的精確版本，且 `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`。

### 執行事項
只回報實際存在的產物，以及有正式檔案佐證的關卡狀態。
交付摘要應與已核准的交付層級相符。

### 必要輸出
產出與實際產物及已核准交付層級相符的交付摘要。

### 通過／離開關卡
只有當交付的產物符合已核准的交付層級，且有已通過的正式關卡檔案作為依據時，才算完成交付。
若沒有 `qa_result.md = PASS`，不得開始 `DELIVERY`。

### 發生問題時退回
若缺少交付證據，或交付內容不符合指定層級，退回 `QA`。
若交付摘要顯示 brief 的文字、來源標籤或忠實轉換有誤，退回 `CONTRACT`，修正並重新取得精確版本的 brief 核准。
若交付摘要顯示成品偏離源自核心設計缺口，退回 `DESIGN_DEVELOPMENT`，完成重新審查、重新核准與後續 `CONTRACT` 關卡後再繼續。

## 不可接受的捷徑
遇到下列說法時，必須視為違反流程，不能當成可以省略步驟的理由：

| 捷徑 | 必要回應 |
| --- | --- |
| 「可以略過 `DESIGN_DEVELOPMENT`，直接把 intake 整理成 brief。」 | 不得略過；`INTAKE` 不能取代實際動畫設計、`DESIGN_READY` 與獨立設計審查。 |
| 「reviewer 在聊天中說沒問題，所以不用建立審查檔。」 | 非正式意見不能取代由獨立 `animation-design-reviewer` 產出的 `animation_design_review.md = PASS`。 |
| 「`pre_build_brief.md` 已經夠詳細，所以可以略過 `SCRIPT`。」 | 仍須執行 `SCRIPT`；場景程式碼不能取代 `teaching_script.md`。 |
| 「渲染能執行，所以等於已經完成審查。」 | 仍須由獨立審查者產出正式的 `scene_review_result.md`。 |
| 「預檢已通過，因此獨立場景審查是選用的。」 | 在 `render_preflight.md` 存在後執行場景審查。 |
| 「QA 可以由基本渲染測試取代。」 | 仍須執行獨立 QA 並產出 `qa_result.md`。 |
| 「再做一次本機修補，比追查反覆發生的畫面問題更省事。」 | 如果問題顯示前面階段仍有歧義，應退回對應階段處理。 |
| 「為求保險，我現在應該閱讀所有參考資料。」 | 只讀取目前階段要求的資料；遇到指定情況時，再讀取額外參考資料。 |
| 「我已委派這個階段，所以不再負責該關卡。」 | 協調者仍負責階段順序、產物是否存在與通過條件。 |
| 「這個核心設計缺口很小，可以直接在 `SCRIPT` 或 `RENDER` 中補上。」 | 不得在下游修補核心設計；退回 `DESIGN_DEVELOPMENT`，重新審查與重新核准後，再完成 `CONTRACT` 關卡。 |
| 「只改了 `animation_design.md` 一個字，所以原本的審查與核准仍有效。」 | 每次編輯都使舊審查與核准失效；依影響進行完整或差異審查，重新取得 `PASS` 與精確版本核准。 |
| 「設計已核准，所以 brief 不需要另外核准。」 | 設計與 brief 是兩個獨立外部核准關卡；`Approved Brief SHA-256` 必須等於目前 brief 的 SHA-256。 |

## 完成檢查
在聲稱工作流程完成前，確認：

- `intake_summary.md` 存在，且準確保留使用者來源與來源標籤。
- `animation_design.md` 存在並通過 `DESIGN_READY`。
- `animation_design_review.md = PASS`，且由獨立的 `animation-design-reviewer` 產出。
- `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`。
- 已取得使用者對該精確受審設計版本的明確外部核准。
- `pre_build_brief.md` 存在，且忠實轉換已核准的設計。
- `Approved Brief SHA-256 = current pre_build_brief.md SHA-256`。
- 已另外取得使用者對該精確 brief 版本的明確外部核准。
- `teaching_script.md` 存在。
- `script_review_result.md = PASS`。
- 旁白產物符合已核准的交付層級要求。
- `generated_algo_scene.py` 存在。
- 最新渲染證據存在，且確實來自最新 MP4。
- `render_preflight.md` 存在且引用最新渲染證據。
- `scene_review_result.md = PASS`。
- `qa_result.md = PASS`。
- 交付摘要符合已核准的交付層級，且沒有把尚未通過的關卡說成已完成。
