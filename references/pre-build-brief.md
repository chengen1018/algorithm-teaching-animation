# Pre-build Brief

本文件定義 `algorithm-teaching-animation-v4` 中作為下游 `CONTRACT` 產物的 `pre_build_brief.md`。

在目前精確版本的 `animation_design.md` 尚未同時擁有獨立 `animation_design_review.md = PASS` 與對該精確已審版本的明確外部使用者核准前，不得開始任何 `CONTRACT` 轉換。在轉換後的 brief 尚未獲得自己獨立的明確使用者核准前，不得開始任何 script、voiceover 或 scene 工作。

## 目的

`pre_build_brief.md` 是以下工作的唯一共享契約：

- script writing
- script review
- voiceover planning
- scene implementation
- scene review
- render QA

它的存在，是為了讓下游工作可以嚴格執行，而不必在後期臨時發明語意。轉換只是對已核准設計的忠實重述與整理，不是重新設計。

## 轉換前提

開始轉換前，以下內容都必須可用：

- 目前的 `animation_design.md`
- 對應該精確設計版本的 `animation_design_review.md = PASS`
- 通過審查中的 `Reviewed Design SHA-256`
- 一份外部明確使用者核准紀錄，其中包含 `Approved Design SHA-256` 與核准參照
- 對目前 `animation_design.md` 位元組新鮮計算出的 SHA-256

在轉換前立刻要求以下值完全收斂：

```text
Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

任何不一致都表示設計是新版本或過期版本。不得轉換。必須回到 `DESIGN_DEVELOPMENT`，取得必要的獨立重新審查、獲得 `PASS`，並對新的精確 SHA-256 重新取得明確外部使用者核准。

轉換前不要求 `Source Design SHA-256`。

## CONTRACT 轉換邊界

`pre_build_brief.md` 必須忠實轉換已核准設計中的語意、心智模型、視覺系統、場景結構、教學弧線、高層節拍、使用者決策、交付義務與風險。`CONTRACT` 可以整理、濃縮並加上來源標籤，但不能新增、修補，或默默定案任何核心設計決策。

在忠實轉換過程中，必須在外部 `CONTRACT` lineage 紀錄中，把 `Source Design SHA-256` 記錄為用來產出 `pre_build_brief.md` 的精確 current `Approved Design SHA-256`。Lineage 與核准紀錄都必須保留在外部；不要修改 `animation_design.md` 或 `pre_build_brief.md` 來存放它們。

若轉換過程暴露出缺少、衝突或有重大歧義的核心決策，必須停止並把缺口送回 `DESIGN_DEVELOPMENT`。修正後的 `animation_design.md` 必須重新走完完整所需的審查與核准路徑，之後才能恢復轉換：更新與 `DESIGN_READY` 自檢、適當的 full 或 delta 獨立審查、`animation_design_review.md = PASS`、精確版本的外部使用者核准，以及 SHA-256 收斂。

若只是 wording、formatting 或 source-label 問題，且不改變已核准含義，則留在 `CONTRACT`，可直接修正 `pre_build_brief.md`，不必重開設計。

任何對 `animation_design.md` 的編輯，都會使衍生出的 `pre_build_brief.md`、其 `Source Design SHA-256` lineage 與其核准失效。必須回到 `DESIGN_DEVELOPMENT`，重跑適用影響範圍的審查與精確版本設計核准，再用新的外部 lineage 重新產生 brief，並獨立重新核准 brief。

## Brief 的獨立核准 Gate

核准 `animation_design.md` 並不等於核准 `pre_build_brief.md`。在轉換完成且請求 brief 核准前，必須重新計算目前設計 SHA-256，並要求：

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
```

只有這時 orchestrator 才能在下游工作開始前，請求使用者對精確 `pre_build_brief.md` 給出獨立明確核准。該核准需在外部記錄：

- `Approved Brief SHA-256`，以精確已核准的 `pre_build_brief.md` 位元組計算；以及
- 一個可識別核准事件的明確使用者核准參照。

不要把核准狀態、`Approved Brief SHA-256` 或核准參照寫進 `pre_build_brief.md`。

每一次對 `pre_build_brief.md` 的編輯都會建立新版本並使先前核准失效，即使它看起來只是編輯性修改也一樣。必須對變更後的 brief 重新審查其忠實 `CONTRACT` 轉換，並重新取得新精確 SHA-256 的明確使用者核准。若某次編輯暴露或引入核心設計變更，則必須送回 `DESIGN_DEVELOPMENT`，重新完成設計審查、精確版本設計核准、重新轉換與 brief 核准。

在 `ANIMATION_DESIGN` 結束 gate，以及在 `SCRIPT` 或任何下游階段開始前，必須重新計算目前設計與 `pre_build_brief.md` 的 SHA-256，並要求：

```text
Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256
Approved Brief SHA-256 = current pre_build_brief.md SHA-256
```

若只有 `pre_build_brief.md` 不一致，且設計鏈仍滿足 `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`，則可留在或回到 `CONTRACT` 做 brief 重新審查與精確版本重新核准。若設計鏈本身出現任何不一致或任何編輯，不論是否核心，都必須回到 `DESIGN_DEVELOPMENT`，完成必要的 Full 或 Delta 重新審查、明確設計重新核准、brief 重新產生與 brief 重新核准，之後才能恢復 `CONTRACT` 轉換。

只有在以下其中一種情況發生，且外部精確版本核准紀錄完整時，brief 才能通過 gate：

- 使用者給出明確核准
- 使用者要求針對性修改，且之後明確核准可繼續

以下情況不算 brief 通過：

- 沉默
- 默示同意
- 在仍有隱藏未解決分歧時說「looks fine」

## 必要章節

每份 brief 都必須包含：

- `Algorithm Identity`
- `Teaching Goal`
- `Audience`
- `Sample Input / Scenario`
- `Confirmed User Requests`
- `Source Labels and Decision Provenance`
- `Resolved High-Impact Clarifications`
- `Agent Default Decisions`
- `Chosen Visual Semantics`
- `Scene Structure and Information Hierarchy`
- `Pointer / Boundary / Temp Slot Plan`
- `Beat Outline`
- `Overlay Policy`
- `Delivery Tier`
- `Narration Language`
- `Known Risks / Best-Effort Notes`

若其中任何章節因高影響問題尚未定案而顯得模糊，則 brief 尚未 ready。

## 章節指引

### Algorithm Identity

清楚說明演算法或概念。若需求特定於某個變體，就指出該變體。

### Teaching Goal

說明觀眾在最後應理解的核心內容。

### Audience

若使用者有指定受眾，就照實記錄；否則寫下工作中的假設。

### Sample Input / Scenario

使用場景真正能圍繞其構建的具體案例。

### Confirmed User Requests

只列出明確的使用者要求，不要列 agent 猜測。

### Source Labels and Decision Provenance

區分直接使用者要求、外部已核准設計決策、designer 預設值、衍生後果，以及低風險的 CONTRACT wording choices。當含義或驗收依賴來源措辭時，必須保留原始用語。

### Resolved High-Impact Clarifications

列出每個已凍結決策及其重要性。這個章節用來證明澄清工作已經完成。

### Agent Default Decisions

只記錄來自 `default-visual-semantics.md` 或其他非語意慣例的低風險預設值。

### Chosen Visual Semantics

描述場景必須遵守的具體面向觀眾規則。

範例：

- active regions 如何呈現
- 什麼算 settled progress
- support structures 如何保持可見

本章節必須轉換已核准的核心視覺語意；不得自行發明。

### Scene Structure and Information Hierarchy

延續已核准的主要場景區域、持續支援結構、主要與輔助資訊，以及預期的面向觀眾因果關係。

### Pointer / Boundary / Temp Slot Plan

明確說明 pointer meaning。若課程包含 temporary holding area，就在這裡說明；若沒有，也要明確說沒有。

### Beat Outline

提供高層課程弧線，而不是完整 narration。

### Overlay Policy

說明 overlays 是關閉、可選，還是必需。

### Delivery Tier

必須精確寫出以下其一：

- `no narration`
- `final narrated delivery`

### Narration Language

若 delivery tier 是 `no narration`，要明確寫出不欠任何 narration。

若 delivery tier 需要 narration，必須明確凍結 spoken language。

若使用者沒有指定 narration language，而工作流程使用了預設值，則必須記錄語言是預設為 English，而不是把它偽裝成使用者指示。

### Known Risks / Best-Effort Notes

用這個章節記錄 support-tier 限制、版面壓力，或剩餘的非語意不確定性。

## 撰寫規則

- 使用具體、面向觀眾的語言
- 除非會改變課程內容，否則避免實作瑣事
- 不要用含糊措辭隱藏語意分歧
- 分開寫明確使用者要求與 agent 預設值
- 當含義依賴來源時，保留已核准來源標籤與使用者原話
- 不要在 `CONTRACT` 轉換中新增或修補核心設計決策
- brief 必須強到足以讓 script 與 scene agents 被稽核

## 規劃紀律

在 brief 獨立核准之前：

- 驗證 brief 是否忠實承載已核准的演算法目標、情境、語意、視覺結構、節拍、delivery tier、narration language 與 overlay policy
- 若新暴露任何核心語意、教學、視覺、場景結構或交付分歧，送回 `DESIGN_DEVELOPMENT`
- 不要保留一份默默凌駕於 brief 之上的平行「真實計畫」

暫時的 scratch notes 可以存在，但任何會影響下游的決策都必須寫進 `pre_build_brief.md`。

若需求屬於 best-effort support，應明確寫在 `Known Risks / Best-Effort Notes` 中，而不是在其他地方偷偷弱化契約語氣。

## Beat Outline 指引

beat outline 應回答：

- 觀眾一開始需要哪個穩定心智模型
- 哪個局部動作會改變這個模型
- 該動作之後應保留哪個進度線索
- 哪個支援結構對教學至關重要
- 觀眾最可能在哪裡誤讀演算法

## 失敗條件

當 brief 有以下情況時，就算失敗：

- 遺漏已知高影響問題
- 缺少必要的設計、審查、核准紀錄或精確 SHA-256 收斂
- 在轉換前要求 `Source Design SHA-256`，而不是在轉換過程中建立它
- 外部 `CONTRACT` lineage 紀錄缺少 `Source Design SHA-256`，或其值不等於用來產生 brief 的精確已核准設計 SHA-256
- 語意模糊到能支援多個彼此衝突的場景
- 未寫明交付義務
- 未寫明 narration language 義務，或把它藏在默示預設中
- 未寫明 overlay policy
- beat outline 無法與已凍結語意對齊
- 轉換過程新增或修補核心設計決策
- brief 缺少獨立明確的使用者核准
- 外部核准紀錄缺少 `Approved Brief SHA-256` 或明確使用者核准參照
- 在 `SCRIPT` 或任何下游工作開始前，當前 brief SHA-256 不等於 `Approved Brief SHA-256`
- 在 brief 核准前、`ANIMATION_DESIGN` 結束時，或 `SCRIPT` 之前，設計雜湊鏈沒有滿足 `Source Design SHA-256 = Reviewed Design SHA-256 = Approved Design SHA-256 = current animation_design.md SHA-256`
- 把核准狀態或核准中繼資料寫進 `pre_build_brief.md`

## 建議範本

```md
# Pre-build Brief

## Algorithm Identity

## Teaching Goal

## Audience

## Sample Input / Scenario

## Confirmed User Requests

## Source Labels and Decision Provenance

## Resolved High-Impact Clarifications

## Agent Default Decisions

## Chosen Visual Semantics

## Scene Structure and Information Hierarchy

## Pointer / Boundary / Temp Slot Plan

## Beat Outline

## Overlay Policy

## Delivery Tier

## Narration Language

## Known Risks / Best-Effort Notes
```

## 下游規則

在 `pre_build_brief.md` 獨立確認後，下游階段可以套用已核准的低風險樣式與執行預設值，但不得修改上游已凍結的語意或設計。

若下游問題只涉及 `CONTRACT` wording 或 source labeling，則在 `CONTRACT` 中修復並重新核准 brief。若它暴露核心設計缺口，則必須回到 `DESIGN_DEVELOPMENT`，完成必要的設計重新審查、精確版本外部重新核准、SHA-256 收斂、重新轉換與 brief 獨立核准後，才能繼續。
