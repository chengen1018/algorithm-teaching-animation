# Subtitles

本文件定義 `algorithm-teaching-animation` skill 中 `subtitle_script.md` 的角色、格式與撰寫原則。

`subtitle_script.md` 是選配的字幕層文件。  
它的責任不是補充新的演算法邏輯，也不是取代 `teaching_script.md` 或預設的 voiceover 音訊 workflow，而是在使用者明確要求畫面字幕時，把每個教學 beat 收斂成可直接顯示在影片中的短字幕。

## 核心目的

`subtitle_script.md` 的存在，是為了在需要畫面文字輔助時，提供短、穩定、beat 對齊的字幕。v2 預設以旁白音訊承擔講解，不預設產出畫面字幕。

它的主要目的包括：

- 讓使用者明確要求字幕時，workflow 具備可顯示的字幕稿
- 把 `teaching_script.md` 的教學說明壓縮成螢幕可讀的短句
- 讓字幕能和 beat 對齊，而不是逐 action 亂跳
- 讓 Manim scene 有穩定的字幕輸入來源

## 核心原則

- 字幕不是逐字旁白稿  
  字幕應短、清楚、可掃讀，不應把完整教學說明原封不動搬上螢幕。

- 一個 beat 對應一組字幕  
  預設以 beat 為單位切字幕，不要每個小 action 都換字。

- 字幕必須忠於 `teaching_script.md`  
  若需要新的教學內容，應先回修 `teaching_script.md`。

- 字幕必須為畫面服務  
  字幕應補充主畫面焦點，而不是與主畫面競爭。

## 預設要求

完整 workflow 預設不產出 `subtitle_script.md`。只有在使用者明確要求畫面字幕、雙語字幕、無聲版本或可讀文字輔助時，才產出 `subtitle_script.md`。

v2 預設情況下：

- 要有 `voiceover.md`
- 要有 `narration_manifest.json`
- 要有 beat-level 旁白音訊
- 不需要 `subtitle_script.md`

## 建議格式

推薦格式如下：

```md
# Subtitle Script

## Summary
- Language:
- Subtitle mode:
- Source:

## Beats

### Beat 1: ...
- Trace mapping:
- Subtitle text:
  - ...
  - ...
- Display rule:

### Beat 2: ...
- Trace mapping:
- Subtitle text:
  - ...
- Display rule:
```

此格式不是唯一合法格式，但若沒有特殊需求，建議維持一致。

## 欄位說明

### Summary

建議至少包含：

- `Language`：字幕語言
- `Subtitle mode`：例如 `on-screen subtitles only`
- `Source`：例如 `condensed from teaching_script.md`

### Beat title

用途：  
與 `teaching_script.md` 的 beat 保持對齊。

### Trace mapping

用途：  
讓字幕能回對到哪一段 trace 與哪一個教學單位。

### Subtitle text

用途：  
提供實際要顯示在影片中的文字。

建議：

- 每個 beat 1 到 2 行
- 每行盡量短
- 優先寫出這一步做什麼、為什麼重要

### Display rule

用途：  
說明這組字幕應該覆蓋哪個 beat、在什麼時機切換。

預設寫法可簡單使用：

- `Show for the whole beat`
- `Show after the dependency highlight appears`
- `Keep until the updated value is written`

若沒有特殊需要，不必先寫精準時間戳。

## 字幕寫作建議

字幕應優先表達：

- 現在正在做什麼
- 為什麼這一步重要
- 這一步如何推進全局理解

好例子：

- 先固定 base cases：`F(0)=0`、`F(1)=1`
- 新的 Fibonacci 值，來自前兩項相加
- 已完成前綴再往右延伸一格

不好的例子：

- 這是一個非常重要而且很酷的步驟
- 如投影片所示我們接著看到
- 把整段教學旁白原封不動貼上

## 與 `teaching_script.md` 的關係

兩者的關係應理解為：

- `teaching_script.md`：較完整的教學說明
- `subtitle_script.md`：畫面上真正顯示的短字幕

因此：

- `subtitle_script.md` 應由 `teaching_script.md` 收斂而來
- 若 beat 重點變了，應優先回修 `teaching_script.md`
- 若只是字太長、太難讀，應回修 `subtitle_script.md`

## 與 `generated_algo_scene.py` 的關係

若使用者要求字幕，Manim scene 應把 `subtitle_script.md` 視為字幕輸入來源，而不是臨時從畫面狀態猜字。

建議：

- 保留穩定的 subtitle-safe area
- 以 beat 為單位切換字幕
- 切換字幕時保持節奏清楚
- 避免字幕遮住主體資料結構

## 常見錯誤

### 錯誤 1：字幕太長

問題：

- 觀眾來不及讀
- 畫面容易變擠

正確方向：

- 壓縮成一到兩句短句

### 錯誤 2：每個 action 都換字幕

問題：

- 字幕閃動過快
- 觀眾跟不上 beat

正確方向：

- 以 beat 為單位切換

### 錯誤 3：字幕講了畫面完全沒有表現的新結論

問題：

- 觀眾無法核對
- 造成教學不一致

正確方向：

- 回到 `teaching_script.md` 或 trace 補強

## 最小範例

```md
# Subtitle Script

## Summary
- Language: zh-TW
- Subtitle mode: on-screen subtitles only
- Source: condensed from teaching_script.md

## Beats

### Beat 1: 建立 base cases
- Trace mapping: `actions 1-2`
- Subtitle text:
  - 先固定 Fibonacci 的兩個 base cases。
  - `F(0)=0`，`F(1)=1`。
- Display rule: Show for the whole beat.

### Beat 2: 產生下一個值
- Trace mapping: `actions 3-7`
- Subtitle text:
  - 新的值來自前兩項相加。
  - 所以 `F(2)=F(1)+F(0)=1`。
- Display rule: Keep until the new value is written.
```
