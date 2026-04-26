---
name: algorithm-teaching-animation-v2
description: 當使用者希望把演算法敘述、輸入資料或狀態轉移概念，轉成具教學導向且包含旁白音訊的動畫工作流時使用此 skill。適用於演算法步驟講解、資料結構狀態變化、指標移動、動態規劃表格建構、圖遍歷，以及需要先建立 deterministic action trace、再轉譯為 Manim 動畫，並預設產出 beat 對齊的英文旁白稿、旁白音訊與 narrated animation 的任務。
---

# 演算法教學動畫

此 skill 用於把演算法說明任務轉成一套教學動畫工作流。

它不是單純的 Manim code generator。它的目標是幫助 Codex 先釐清要教什麼，再把演算法邏輯轉成可驗證的 trace，最後產出可讀、可教、可渲染，且具備 beat 對齊旁白音訊的動畫。

當任務涉及以下需求時，應使用此 skill：

- 演算法講解動畫
- 資料結構狀態變化視覺化
- 指標移動與控制流程說明
- 排序、搜尋、圖遍歷、樹操作、DP 的逐步教學
- 需要 voiceover、narration audio 或 narrated animation 的演算法教學影片

## 核心原則

- 教學優先於特效  
  每個畫面變化都必須有教學目的。

- 先 trace，後渲染  
  動畫層不可自行發明演算法邏輯。

- 先看狀態，再講規則  
  先展示資料結構如何變，再總結策略或結論。

- 一次只講一個 beat  
  每一拍只聚焦一個重點，避免資訊過載。

- 視覺語義必須穩定  
  顏色、標記、指標、完成狀態要有一致意義。

- 不變量要可見  
  若某個不變量是理解關鍵，畫面或說明中要明確呈現。

- 完整交付預設要有旁白音訊  
  除非使用者明確只要求無聲或文字稿，否則完整 workflow 應產出與 beat 結構對齊的英文旁白稿、旁白音訊與 narration manifest。

## 產出物

### 必要產出物

- `plan.md`
- `teaching_script.md`
- `voiceover.md`
- `narration_manifest.json`
- `audio/voiceover/*.wav`
- `generated_trace_script.py`
- `action_trace.json`
- `generated_algo_scene.py`

### 選配產出物

- `review_notes.md`
- `subtitle_script.md`，僅在使用者明確要求畫面字幕時產出
- `tts_config.json`，當專案需要記錄本次使用的 TTS provider 與非機密設定時產出
- 多場景 stitching、額外音軌、後製相關輸出

v2 預設由 `teaching_script.md` 承擔教學分鏡與較完整的教學說明，`voiceover.md` 承擔可口說的 beat 對齊旁白稿，`narration_manifest.json` 承擔旁白音訊與 beat 的對齊資料；`subtitle_script.md` 不是預設必要產出。

## 名詞定義

### `plan.md`
規劃文件。定義教學目標、觀眾程度、主要模式、核心資料結構、重要指標、不變量與 beat 結構。

### `teaching_script.md`
教學腳本。描述每個 beat 要教什麼、觀眾應注意什麼，以及搭配的簡短教學說明。

### `voiceover.md`
旁白稿。以 beat 為單位，提供可直接送入 TTS 或錄音流程的英文口說稿。它應由 `teaching_script.md` 收斂而來，必須忠於 beat 的教學目的與 trace mapping，且不可加入沒有被規劃或 trace 支撐的新演算法內容。

### `narration_manifest.json`
旁白同步 manifest。記錄每個 beat 的旁白文字、音訊路徑、音訊長度與 trace mapping，供 `generated_algo_scene.py` 安排 beat duration 與音訊播放使用。

### `audio/voiceover/*.wav`
beat-level 旁白音訊。每個 beat 通常對應一個 WAV 檔，檔名應穩定且能回對到 `narration_manifest.json`。

### `subtitle_script.md`
字幕腳本。僅在使用者明確要求畫面字幕時產出。字幕應以 beat 為單位，提供可直接顯示在影片中的短字幕，且不取代 voiceover 音訊。

### `generated_trace_script.py`
純 Python 的 tracer script。負責執行演算法並輸出 deterministic 視覺事件。

### `action_trace.json`
由 tracer script 產生的 action trace。它是演算法事件與狀態轉移的單一真相來源。若此 skill 提到 `trace`，預設指的就是它。

`plan.md` 與 `teaching_script.md` 仍負責教學目標、beat 結構與呈現重點；`action_trace.json` 不取代這些教學規劃文件。


### `generated_algo_scene.py`
Manim 轉譯層。負責把 `action_trace.json` 轉成動畫，不可重新推理演算法。

## 任務模式

先判斷任務屬於哪一種主要模式：

- `algorithm walkthrough`
- `data structure state transition`
- `pointer and control-flow explainer`
- `graph traversal explainer`
- `dynamic programming construction`
- `comparison or intuition explainer`

若任務同時跨多種模式，先選一個主要模式，維持整體敘事一致。

## 工作流程

除非使用者只要求某一部分，否則依序執行以下流程：

預設行為：

- 若使用者明確只要求某一層，僅處理該層
- 若使用者要求完整 workflow，應持續推進到可 review 的結果
- 若任一階段出現高風險歧義，應在進入下一主要階段前先確認
- 若沒有高風險歧義，預設應持續往下完成，而不是每一層都停下等待確認

### 1. PLAN
先寫 `plan.md`，確認：

- 這支動畫最重要的教學目標是什麼
- 核心資料結構與狀態變化是什麼
- 哪些指標、邊界或不變量需要持續呈現
- 教學 beat 應如何排序

### 2. SCRIPT
產出 `teaching_script.md`。

每個 beat 應包含：

- 畫面焦點
- 對應的演算法事件
- 觀眾應理解的重點
- 簡短教學說明

教學腳本應聚焦：

- 狀態變化
- 資料結構操作
- 控制流程
- 不變量
- 指標移動
- 局部決策如何累積成全域結果

`teaching_script.md` 的每個 beat 都必須對應到一段明確的 trace 區間或一組 action。  
若一個 beat 需要多個 action 才能完整表達，應將這些 action 視為同一個教學單位；但不得出現無對應 trace 的教學 beat，也不得出現無教學目的的重要 trace 段落。


### 3. AUDIO / VOICEOVER
產出 `voiceover.md`、旁白音訊與 `narration_manifest.json`。

要求：

- 預設完整 workflow 必須產出英文旁白稿與實際旁白音訊，除非使用者明確要求無聲或只要文字稿
- `voiceover.md` 必須以 beat 為單位，能回對到 `teaching_script.md` 與 trace mapping
- 旁白應是自然口說，不是畫面字幕、公式推導稿或逐字畫面描述
- 旁白不可偷塞新的演算法結論；若旁白需要新資訊，應先回修 `teaching_script.md`
- TTS provider 採可插拔設計，但 narrated final delivery 必須有可用 provider
- 若沒有設定可用 TTS provider，應在 final render 前停下來要求使用者設定，而不是默默跳過音訊
- 每個 beat 的音訊應寫入 `audio/voiceover/`，並由 `narration_manifest.json` 記錄路徑、duration 與對應 beat

若 `teaching_script.md` 很完整，但旁白仍然冗長、繞口或難以同步，應優先修正 `voiceover.md`，而不是在 Manim 層用等待時間掩蓋節奏問題。


### 4. TRACE
產出 `generated_trace_script.py`，再推導出 `action_trace.json`。

要求：

- 演算法實作必須正確
- trace 必須 deterministic
- trace 必須具視覺意義
- 不要把 Manim 邏輯混入 trace 層
- 不要過度追蹤沒有教學價值的細節
- trace 必須能回溯對應到 `teaching_script.md` 中的 beat 結構

若 `teaching_script.md` 與 trace 設計衝突，應優先回頭修正 `plan.md` 或 `teaching_script.md`，而不是在 Manim 層補救。


### 5. MANIM TRANSLATION
產出 `generated_algo_scene.py`。

要求：

- 將 `action_trace.json` 視為演算法事件與狀態轉移的單一真相來源
- 不在 Manim 層重新計算、補完或發明演算法邏輯
- `plan.md` 負責提供教學目標、主要模式、不變量與整體 beat 規劃
- `teaching_script.md` 負責提供每個 beat 的畫面焦點、教學重點與說明方式
- `voiceover.md` 與 `narration_manifest.json` 負責提供每個 beat 的旁白文字、音訊檔與音訊長度
- Manim 層必須在忠於 `action_trace.json` 的前提下，依據 `plan.md` 與 `teaching_script.md` 決定畫面焦點、節奏、標示與呈現方式
- Manim 層應依 `narration_manifest.json` 安排 beat duration；若視覺動作先結束，應等待旁白音訊完成
- 除非使用者明確要求字幕，Manim 層不應預設建立字幕層或 subtitle-safe area
- 保持視覺語義穩定
- 讓重要狀態變化足夠清楚、足夠可讀


### 6. RENDER AND REVIEW
先做低成本預覽，再檢查：

- 邏輯是否正確
- 教學是否清楚
- 畫面焦點是否明確
- 不變量與指標是否容易追蹤
- Manim 是否忠實遵守 action trace
- 旁白是否與 beat 對齊、音訊是否存在且可播放、節奏是否支撐畫面理解

若發現問題，必須明確標註應回到哪一層修正：

- `plan.md`：教學目標、模式選擇、beat 結構有誤
- `teaching_script.md`：教學節奏、重點安排、說明方式不清
- `voiceover.md` / `narration_manifest.json`：旁白太長、太短、與 beat 不對齊，音訊路徑或 duration 不正確
- `generated_trace_script.py` / `action_trace.json`：演算法事件記錄錯誤或不足
- `generated_algo_scene.py`：畫面呈現、節奏、標示或可讀性不足

若使用者要求完整交付或需要保留 review 過程，應額外產出 `review_notes.md`，簡要記錄檢查結果、主要問題與修正方向。

v2 先聚焦核心教學動畫流程、英文旁白音訊與 beat-level 音訊同步。多場景 stitching、電影式節奏設計與後製不屬於必要流程。


## 寫作與設計指引

- 規劃應從「觀眾要理解什麼」開始，不是從「要建立哪些 Manim 物件」開始。
- 教學說明應解釋操作的目的、狀態的變化、目前進度與結果意義。
- 不要把旁白預設寫成公式推導稿。
- 不要把整段教學說明原封不動當成旁白；旁白應是 beat 對齊、自然可說、可同步的短段落。
- 若現有 trace schema 不足以表達某類演算法，先擴充 action vocabulary，再做動畫轉譯。
- 畫面上同時不要有過多競爭焦點。
- 位置、顏色、指標與完成狀態要保持穩定語義。

## 不應做的事

除非使用者明確要求，否則不要：

- 跳過 `plan.md` 直接寫 Manim
- 讓 Manim 層重算演算法邏輯
- 用 cinematic 風格取代教學清晰度
- 在沒有 TTS provider 的情況下宣稱 narrated final delivery 已完成
- 把進階剪輯與後製列入 v2 必要流程

## 進階選配流程

只有在使用者明確要求更完整的教學影片工作流時，才加入以下內容：

- `subtitle_script.md`
- 多場景拆分
- 分段渲染與 stitching
- 片頭片尾
- 跨場景節奏調整
- 複雜音訊後製與混音
- 後製 review notes

## 建議的參考文件

主 skill 保持精簡，細節放到 references：

- `references/planning.md`
- `references/teaching-script.md`
- `references/voiceover.md`
- `references/subtitles.md`
- `references/trace-schema.md`
- `references/tracer-api.md`
- `references/visual-language.md`
- `references/manim-guidelines.md`
- `references/rendering.md`
- `references/modes.md`

## 建議的按需載入方式

為避免每次都載入全部 reference，應依當前階段選擇性閱讀：

- PLAN 階段：優先讀 `planning.md`、`modes.md`
- SCRIPT 階段：優先讀 `teaching-script.md`
- AUDIO / VOICEOVER 階段：優先讀 `voiceover.md`
- SUBTITLES 階段：僅在使用者要求字幕時讀 `subtitles.md`
- TRACE 階段：優先讀 `trace-schema.md`、`tracer-api.md`
- MANIM TRANSLATION 階段：優先讀 `visual-language.md`、`manim-guidelines.md`
- RENDER AND REVIEW 階段：優先讀 `rendering.md`

## 輸出期待

使用此 skill 時，最終輸出應清楚說明：

- 這支動畫的簡單介紹
- 產出了哪些文件
- 目前是預覽版還是可交付版本
- 是否已包含旁白稿、旁白音訊與 narration manifest
- 若缺少 TTS provider，明確說明目前只能交付旁白稿，不能宣稱 narrated final delivery 完成
- 若需 refinement，應優先調整哪一層
