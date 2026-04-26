# Rendering

本文件定義 `algorithm-teaching-animation` skill 中 `RENDER AND REVIEW` 階段的原則、檢查方式與回修順序。

此 skill 的 render 階段不只是把程式跑完，而是要確認最終動畫是否：

- 邏輯正確
- 教學清楚
- 視覺可讀
- 忠於 `plan.md`、`teaching_script.md` 與 `action_trace.json`
- 若是完整 workflow，旁白音訊也必須與 `voiceover.md`、`narration_manifest.json` 和 beat 結構對齊

換句話說，render 不是單純的技術成功，而是教學工作流的最終驗證階段。

## 核心原則

render 與 review 應遵守以下原則：

- 先求可讀，再求精緻  
  先確認觀眾看得懂，再考慮更高品質輸出。

- 先做低成本預覽，再做高成本輸出  
  不要在還沒確認邏輯與教學是否成立前，就直接投入高成本 render。

- 若結果有問題，優先回到正確層修正  
  不要用 Manim 特例去掩蓋 plan、script 或 trace 的問題。

- Review 不只看技術錯誤，也看教學錯誤  
  一支動畫即使沒有 crash，也可能教得很差。

- 最終輸出必須可說明  
  完成後應能清楚指出目前版本是 preview 還是 final，以及若需 refinement 應修哪一層。

## Render 的階段

建議將 render 分成兩個層級：

### 1. Preview Render

用途：

- 快速驗證程式可執行
- 快速檢查畫面是否可讀
- 快速發現 trace 與 Manim translation 是否對齊
- 快速檢查旁白 manifest 與 beat duration 是否合理

適用時機：

- 第一次產出 `generated_algo_scene.py` 後
- 修改 trace 後
- 修改教學節奏或畫面焦點後

Preview render 的重點不是畫質，而是快速獲得可檢查結果。

常見做法：

```bash
manim -pql generated_algo_scene.py AlgorithmAnimation
```

### 2. Final Render

用途：

- 在 preview 已確認成立後，輸出較完整或較高品質版本
- 作為可交付版本或展示版本

Final render 只應在以下條件成立後進行：

- 邏輯正確
- 教學節奏合理
- 視覺語義穩定
- 旁白音訊存在、可播放，且與 beat 對齊
- 主要問題已修正完畢

常見做法：

```bash
manim -pqh generated_algo_scene.py AlgorithmAnimation
```

## Review 檢查項目

每次 render 完成後，至少檢查以下面向。

### A. 邏輯正確性

檢查：

- 演算法步驟是否正確
- `action_trace.json` 是否忠實反映演算法執行
- `generated_algo_scene.py` 是否忠實反映 trace

常見問題：

- swap 或 overwrite 順序錯誤
- pointer 移動與實際邏輯不同步
- trace 漏掉關鍵事件

### B. 教學清晰度

檢查：

- 每個 beat 是否真的在教東西，而不只是描述畫面
- 是否能看出本拍最重要的教學重點
- 教學旁白與畫面是否一致
- voiceover 是否真的幫助理解，而不是只重複畫面描述
- 不變量是否有被看見

常見問題：

- 畫面正確，但不知道為什麼這一步重要
- beat 太快，觀眾來不及理解
- script 強調的內容沒有在畫面中被突出
- 旁白太長，導致畫面停留過久或節奏鬆散

### C. 視覺可讀性

檢查：

- 焦點是否清楚
- 顏色語義是否一致
- pointer 是否容易追蹤
- 文字是否可讀
- 畫面是否過擠或過亂
- 位置是否穩定
- 若使用者要求字幕，字幕是否遮住主體內容
- 若使用者要求字幕，字幕列是否讓畫面主焦點變得擁擠

常見問題：

- 同時太多 highlight
- 完成狀態與焦點狀態顏色太接近
- pointer 過於搶眼或太難看見
- 資料結構位置亂跳
- 選配字幕與圖形重疊，導致版面過擠

### D. 節奏、旁白與感知性

檢查：

- 重要事件是否停留足夠久
- 焦點轉移是否清楚
- 一拍結束後是否有足夠消化時間
- 動畫是否過快、過碎或過長
- `narration_manifest.json` 中的每個 `audio_path` 是否存在且可播放
- `duration_seconds` 是否與實際音訊長度大致一致
- 旁白是否與該 beat 的畫面焦點同步
- 若使用者要求字幕，字幕是否停留足夠久讓人讀完

常見問題：

- swap 太快，看不出發生什麼
- 一拍中發生太多事情
- 所有事件速度都一樣，缺乏節奏層次
- 旁白講的是上一個或下一個 beat 的內容
- 缺少 TTS provider 或音訊檔，卻宣稱 narrated final delivery 完成

## 問題分類與回修順序

若 render 後發現問題，必須優先判斷問題屬於哪一層。

### 1. 回修 `plan.md`

適用情況：

- 整支動畫主軸不清楚
- 教學目標選錯
- 觀眾程度設定不對
- 應強調的不變量沒有被規劃進去
- beat 高層順序本身就有問題

症狀：

- 動畫很努力，但教學方向本身不對
- 所有後續層都做得合理，結果仍然不好教

### 2. 回修 `teaching_script.md`

適用情況：

- beat 切得不好
- 某拍承載太多重點
- 旁白與畫面不對齊
- 觀眾不知道本拍應該學到什麼

症狀：

- 動畫正確，但節奏差
- 畫面有重點，說明卻沒接住
- 教學內容像流水帳

### 3. 回修 `generated_trace_script.py` / `action_trace.json`

適用情況：

- 演算法事件記錄錯誤
- 關鍵狀態變化沒有被 trace
- pointer、boundary、cell update 等事件缺失
- trace 無法支撐 teaching script 想講的重點

症狀：

- 畫面只能硬補，因為 trace 本身就不夠
- 某些教學重點在動畫中根本沒有對應事件

### 4. 回修 `voiceover.md` / `narration_manifest.json`

適用情況：

- 旁白太長、太短、太書面或不適合口說
- 旁白與 beat 不對齊
- 旁白沒有抓到真正想教的重點
- `narration_manifest.json` 的音訊路徑、duration 或 trace mapping 錯誤

症狀：

- 動畫正確，但旁白節奏拖慢或講解不清
- 有旁白音訊，卻沒有真正幫助理解
- Manim 必須靠不自然等待才能讓音訊播完

### 5. 回修 `generated_algo_scene.py`

適用情況：

- trace 是對的，但畫面表現不夠清楚
- 顏色、標示、節奏、位置安排不理想
- 焦點控制不夠好
- 旁白播放時機、beat duration 或等待時間不理想
- 選配字幕排版、字幕區或字幕切換節奏不理想

症狀：

- 邏輯正確，但畫面難懂
- 資訊都有，卻沒有被正確強調

## 不應做的事

render 階段不要做以下事情：

- 不要因為畫面不好懂，就直接在 Manim 層發明新的演算法事件
- 不要用視覺特效掩蓋教學問題
- 不要在 preview 尚未通過前就急著做 final render
- 不要把 trace 問題誤判成單純畫面問題
- 不要在沒有明確 review 結論時就宣稱完成
- 不要因為旁白不清楚，就在 Manim 層硬加新的教學結論
- 不要在沒有可用 TTS provider 或音訊檔時宣稱 narrated final delivery 完成

## Preview Render 的最小標準

一個 preview render 至少應達成：

- 程式可執行
- 沒有明顯 crash 或中斷
- 主要資料結構可辨識
- 主要焦點可辨識
- 重要狀態變化能被看懂
- 若是完整 workflow，至少能載入 `narration_manifest.json` 並找到對應音訊檔
- 至少能判斷下一步該修哪一層

Preview 不要求完美，但必須足夠讓人做出正確判斷。

## Final Render 的最小標準

一個 final render 至少應達成：

- 演算法邏輯正確
- 教學節奏清楚
- 畫面焦點穩定
- 視覺語義一致
- 不變量或進度概念可見
- `voiceover.md` 的旁白與畫面一致
- `narration_manifest.json` 的音訊路徑、duration 與 beat mapping 正確
- 旁白音訊可播放，且每個 beat 的視覺節奏能容納音訊
- 若使用者要求字幕，字幕內容、停留時間與畫面同步
- 沒有明顯干擾理解的視覺問題

若這些條件未達成，應視為仍處於 refinement 階段，而不是 final。

## 是否需要 `review_notes.md`

預設情況下，不一定每次都需要獨立 `review_notes.md`。

但若符合以下情況，建議或應該產出：

- 使用者要求完整交付
- 有多輪修正歷史需要保留
- 問題來源不單一，需要記錄回修策略
- 需要明確交代目前版本是否可交付

`review_notes.md` 可以簡短，但應至少包含：

- 本次檢查版本
- 發現的主要問題
- 問題屬於哪一層
- 建議的修正方向
- 目前判定：preview / refinement / final

## 建議格式

若需要寫 `review_notes.md`，可使用以下格式：

```md
# Review Notes

## Version
- Current stage:
- Render type: Preview / Final

## Findings
- Issue:
- Layer:
- Suggested fix:

## Overall Assessment
- Current status:
- Next recommended action:
```

## 最小 review 流程

每次 render 完成後，建議至少依以下順序檢查：

1. 能不能成功執行
2. trace 與 Manim 是否一致
3. 主焦點是否清楚
4. 教學 beat 是否成立
5. 不變量是否有被看見
6. 決定是否進入下一輪 refinement 或 final render

## 與其他文件的關係

- `planning.md`  
  決定動畫應該教什麼

- `teaching-script.md`  
  決定每個 beat 應如何被理解

- `voiceover.md`  
  決定每個 beat 應如何被口說講解

- `narration_manifest.json`  
  決定旁白音訊如何對齊 beat 與 scene duration

- `trace-schema.md`  
  決定事件如何被記錄

- `visual-language.md`  
  決定畫面應如何清楚表達事件與教學重點

- `generated_algo_scene.py`  
  是 render 的直接輸入之一

本文件的責任，是把「render 後如何判斷是否真的成功」正式化。
