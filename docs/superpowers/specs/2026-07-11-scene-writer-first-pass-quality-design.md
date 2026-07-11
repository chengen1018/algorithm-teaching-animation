# Scene Writer 首次產出品質改進設計

## 背景

`scene-writer` 目前能依上游需求、動畫設計與 teaching script 產生 Manim scene，但首次產出的程式仍可能包含版面缺陷。真實 Binary Search 產物已確認兩種代表性問題：

- 寬陣列右側使用 `next_to()` 放置 target 與 output 卡片，造成卡片超出 frame。
- `left`、`mid`、`right` 移至同一 index 時仍各自使用固定 `label_shift`，造成 pointer labels 重疊。

既有流程已有 frame overflow 與物件碰撞的輕量檢查工具。本次不重做檢查工具，而是提高 `scene-writer` 在進入既有檢查流程前的首次程式品質。

## 目標

讓 `scene-writer` 僅靠上游文件與 `generated_algo_scene.py` 的靜態推理，就能在首次送檢前主動避免或修正常見的 overflow、collision、遮擋與物件生命週期錯誤。

首次工作流程為：

1. 閱讀必要上游文件與 Manim 指南。
2. 先規劃每個 Scene 的 layout，再撰寫動畫程式。
3. 完成 `generated_algo_scene.py` 後，重新從頭閱讀整支檔案。
4. 逐 Scene、逐穩定 beat 進行靜態 audit 並自行修正。
5. 完成後才進入既有 render preflight、layout/collision 檢查與獨立 review。

本次不要求 scene writer 在首次送檢前觀看 preview render。

## 採用方案

採用「Manim 知識重構加強＋強制靜態設計流程」，並少量吸收固定 layout framework 的低階不變條件。

不強迫所有演算法使用同一份視覺模板。Scene writer 仍可依演算法設計不同構圖，但必須遵守安全邊界、peak-state planning、共址衝突處理及靜態 audit 等不變條件。

## 文件責任

### `references/manim-guidelines.md`

作為 scene writer 的 Manim 實作與首次靜態驗證指南，包含：

- 寫 code 前的 layout planning。
- Manim frame、座標、尺寸與 positioning API 的推理方式。
- Layout zones、安全邊界、文字容量與物件衝突策略。
- Pointer 共址、Transform、phase ownership 與物件生命週期。
- Beat staging 與高品質教學動畫原則。
- 常見演算法視覺結構模式。
- 寫完 `generated_algo_scene.py` 後的強制靜態 audit。

不包含 reviewer 身分、證據新鮮度、Full/delta review 或流程回退等交接規則。

### `.codex/agents/scene-writer.toml`

負責強制執行順序與產物契約：

- 完整閱讀 Manim 指南。
- 先規劃、再實作。
- 完成後重新閱讀整支 Python 檔。
- 對六個 Scene 與各 Scene 的 peak state 執行靜態 audit。
- 在進入既有檢查流程前自行修正發現的問題。
- 保留既有上游忠實性、必要產物、技術阻礙與獨立送審規則。

TOML 不複製 Manim 指南的詳細規則。

### `references/render-preflight.md` 與 review checklist

既有檢查與獨立 review 仍是最後防線，不因 writer 自我檢查而降低標準。本次只在文字與新的首次靜態 audit 發生責任衝突或重複時進行最小一致性調整，不重新設計既有檢查工具。

## `manim-guidelines.md` 重構原則

本次須完整重構現有文件，不能只在末尾附加新知識。逐段依下列方式處理：

- **保留**：仍會影響首次實作品質的原則，例如 beat staging、phase ownership、文字可讀性與 final cleanup。
- **改寫**：把「保持穩定」「避免碰撞」等抽象提醒改成能從 Python code 靜態判斷的操作規則。
- **合併**：整合分散在核心原則、視覺穩定、審查準備度與常見失敗中的重複要求。
- **移出**：將純流程、交接與證據新鮮度內容留給 agent TOML、preflight 或 reviewer checklist。
- **刪除**：移除沒有可操作結果的口號，或已被更精確規則完整涵蓋的內容。
- **新增**：加入 layout planning、frame budgeting、bounding-box reasoning、peak-state planning、高風險定位 API、pointer 共址、文字容量及寫後靜態 audit。

重構後的預期架構：

1. Scene writer 的實作責任與不可改變事項。
2. 寫 code 前的 layout planning。
3. Manim frame、座標與尺寸推理。
4. Layout zones 與安全邊界。
5. 物件定位與群組排版規則。
6. 文字、卡片、公式與 panel 容量。
7. Pointer、label 與共址衝突策略。
8. Phase ownership、Transform 與物件生命週期。
9. Beat staging 與教學呈現原則。
10. 演算法常見結構模式。
11. 寫完 Python 後的強制靜態 audit。
12. 送交既有檢查流程前的完成條件。

## 寫 code 前的 Layout Planning

每個 Scene 必須先確定：

- **Primary structure**：陣列、圖、樹或表格等主視覺。
- **Persistent regions**：標題、狀態 panel、公式或 overlay 等持續區域。
- **Transient regions**：比較卡片、pointer labels 與臨時說明。
- **Safe frame**：所有必要內容必須位於的內縮邊界。
- **Peak state**：同時物件最多、文字最長、pointer 最密集或最容易越界的穩定 beat。
- **Collision policy**：空間不足時採用縮放、換區、上下分流、合併標籤或分階段顯示中的哪一種策略。

先為 peak state 排版，再讓較簡單的 beats 使用同一個空間骨架。不得先排簡單開場，再以連續 `shift()` 把後續資訊硬塞進剩餘空間。

Layout plan 不建立額外必要文件；它應反映在 layout constants、zones、builders、groups 與 helper interfaces 中，使 reviewer 能從程式結構理解設計。

## Manim 靜態尺寸與定位推理

指南必須明確指出下列 API 是局部定位，不是自動排版：

- `next_to()` 不保證新物件仍位於 frame 或 safe frame 內。
- `to_edge()` 只處理被呼叫物件，不會替其他區域保留空間。
- `move_to()` 不會處理來源與目標的寬高差異。
- `arrange()` 只安排群組內部，不代表群組適合目前區域。
- `.to_edge(...).shift(...)` 等定位鏈必須以最終 bounding box 重新推理。
- `Transform()` 必須同時考慮來源、目標與未被移除的相鄰物件。

寬主結構旁串接側邊資訊屬於高風險模式。應先建立完整 layout group 或先分配 zones，再採用整體縮放、雙欄構圖、上下分區、較短 label 或分 beat 揭露。不得假設個別定位成功就代表整體構圖合法。

## Pointer 與共址衝突策略

多個 pointers 可能落在同一個 index 時，不能各自使用相同 anchor 再依賴固定 `label_shift`。必須在 layout plan 中選擇：

- 垂直分層並維持一致間距。
- 上下分流。
- 共用 marker 並將 labels 移至 legend。
- 語意等價時合併 label，例如 `left = mid = right = 5`。
- 只有在不隱藏 script 要求的同時狀態時，才分階段顯示。

每次 pointer 移動都要檢查目的 index 已存在的 pointers，而不只推理自身目的位置。

## 文字與 Panel 容量

- Panel 依最長可能內容設計，不依第一段或最短內容設計。
- 動態替換文字使用一致 anchor 與最大可用寬度。
- 長文字優先縮短措辭、合理換行或移至專屬區域；不得縮到低於可讀標準。
- 卡片、公式與主結構組合後才判斷是否 fit。
- 標題、狀態、主視覺與臨時說明不能各自獨立 `to_edge()` 後假設彼此不碰撞。
- Morph-style text transforms 只用於結構相近且過渡仍可讀的文字；差異大時使用穩定替換。

## Phase Ownership 與物件生命週期

每個 helper、label、highlight 與 support structure 必須有清楚的首次出現、持續 beats、更新方式及移除時點。

靜態推理必須區分：

- 物件是否仍在 `scene.mobjects`。
- 物件是否只是透明或被其他物件遮住。
- `Transform` 是否改變既有 reference 的幾何與語意。
- `ReplacementTransform`、`FadeOut` 與 cleanup 是否真正處理舊狀態。
- 新 phase 是否仍保留已失去教學用途的 helper。

## 教學動畫品質原則

將可借鑑的高品質數學動畫特點轉成可執行規則，不要求模仿任何特定作品或視覺品牌：

- **Visual continuity**：同一概念盡量由同一物件延續。
- **One visual question at a time**：每個 beat 僅有一個主要焦點群組。
- **Spatial meaning**：相同位置與區域維持穩定語意。
- **Progressive disclosure**：只在需要時引入物件。
- **Meaningful transformation**：動畫移動表達狀態變化，不作裝飾性繞路。
- **Visual economy**：刪減重複文字與無教學作用的裝飾，而不是把所有內容縮小塞入。
- **Peak-state composition**：先確保資訊最密集的穩定畫面清楚。
- **Pause on resolved states**：為觀眾保留可辨識的穩定結果畫面。

## 寫完 Python 後的強制靜態 Audit

Scene writer 完成 `generated_algo_scene.py` 後，必須重新從頭閱讀完整檔案，為每個 Scene 建立心中的物件狀態時間線。每個穩定 beat 至少回答：

1. 當下有哪些物件仍存在？
2. 每個物件的最終 positioning chain 是什麼？
3. 哪些物件共享 anchor、cell、edge 或 zone？
4. 此 Scene 的寬度、高度、文字長度與物件數量峰值在哪個 beat？
5. 舊物件是否確實被替換、淡出或清理？
6. 是否有過期物件仍占空間、遮擋內容或分散焦點？
7. 是否存在只能靠未驗證 magic shift 才可能成立的構圖？
8. 每次 pointer 移動後，目的地的所有 labels 是否仍可共存？
9. 動態文字替換後，最長內容是否仍位於 panel 與 safe frame 內？
10. 個別合法的 objects 組合後是否可能越界或碰撞？

發現高風險定位或無法從程式證明安全時，scene writer 必須先修改 layout，再進入既有檢查流程；不能把已知疑點留給 reviewer 首次發現。

## 驗證策略

### 結構驗證

- `.codex/agents/scene-writer.toml` 可由 Python `tomllib` 解析。
- TOML 明確強制 plan、implement、reread、audit、fix、handoff 順序。
- `manim-guidelines.md` 沒有重複的流程、reviewer 或 evidence freshness 規則。
- `manim-guidelines.md` 的舊內容已逐段保留、改寫、合併、移出或刪除，沒有只追加新章節。
- `git diff --check` 通過。

### 行為壓力案例

使用下列案例檢查新版指南能否引導首次靜態推理：

1. 寬陣列右側放 target/output，重現 frame overflow。
2. `left`、`mid`、`right` 移到同一 index，重現 pointer collision。
3. 固定大小 panel 連續替換長短差異大的文字。
4. `Transform` 後舊 helper 仍存在，造成遮擋或語意殘留。
5. 多個物件分別 `to_edge()`，個別合法但組合後碰撞。
6. 早期 beat 稀疏、後期 peak state 過載。

評估重點為 agent 是否會主動辨識 peak state、避開高風險定位、提出 zone 或衝突策略，並在重讀 code 時找出潛在 overflow、collision 與生命週期問題。驗證不得把預期修正答案洩漏給受測 agent。

若 agent 仍依賴大量 magic shifts，收緊不變條件與 audit 問題；若所有輸出變得模板化，則保留安全不變條件並放寬可接受的實作模式。

## 不在本次範圍

- 重做既有 frame overflow 或 collision 檢查工具。
- 要求首次送檢前觀看 preview render。
- 修改已核准動畫的教學語意、scene 結構或 beat 順序。
- 強迫所有演算法使用單一固定視覺模板。
- 模仿特定創作者的程式碼、作品或視覺品牌。

## 完成條件

- `manim-guidelines.md` 已依新架構完整重寫，沒有互相衝突或重複的舊規則。
- `scene-writer.toml` 強制首次 layout planning 與寫後靜態 audit。
- 必要時已對 preflight/review 文字做最小一致性調整。
- 結構驗證全部通過。
- 行為壓力案例顯示 agent 能在不看 render 的情況下，從程式碼主動辨識代表性的 overflow、collision 與生命週期風險。
