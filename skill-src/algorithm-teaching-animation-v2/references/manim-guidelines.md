# Manim Guidelines

本文件定義 `generated_algo_scene.py` 的寫法規範，目標是讓不同演算法產生的 Manim scene 保持一致的程式結構與可讀性。

## 核心原則

- Manim scene 是 trace 的 renderer，不是邏輯推理器
- 優先忠於 `action_trace.json`
- narrated workflow 應讀取或等價嵌入 `narration_manifest.json`
- 視覺語義應由顯式狀態維護，不應靠顏色反推語義
- 命名、常數與動作節奏應盡量一致

## 基本結構

建議優先使用：

```python
from manim import *


class AlgorithmAnimation(Scene):
    ...
    def construct(self):
        state_trace = [...]
        ...
```

除非專案已有固定 base class，否則 example 與 skill 預設以 `Scene` 為基礎。

## 常數命名

建議使用一致命名：

- `FONT_SIZE`
- `ELEM_WIDTH` / `ELEM_HEIGHT`
- `ELEM_BUFF`
- `POINTER_BUFF`
- `CELL_SIZE`
- `VOICEOVER_DIR`
- `MIN_BEAT_PAUSE`
- `SUBTITLE_FONT_SIZE`
- `SUBTITLE_BOX_HEIGHT`

顏色常數建議：

- `COLOR_DEFAULT`
- `COLOR_HIGHLIGHT`
- `COLOR_DONE`
- `COLOR_EXCLUDED`
- `COLOR_POINTER`

若有模式特定色，可再加：

- `COLOR_FRONTIER`
- `COLOR_VISITED`
- `COLOR_DEP`

## 狀態管理

不要用目前畫面上的 fill color 來反推語義狀態。  
應維護顯式狀態表，例如：

```python
node_states = {}
cell_states = {}
array_states = {}
```

這樣 `unhighlight` 才能回到最近的穩定語義狀態，而不是碰運氣依賴顏色值比較。

## 動畫時間

建議範圍：

- 結構建立：`0.5 - 0.8`
- highlight / unhighlight：`0.2 - 0.35`
- swap / pointer move：`0.35 - 0.6`
- overwrite / set_cell：`0.25 - 0.4`
- beat 間停頓：`0.15 - 0.3`

原則：

- 先求可讀，再求風格化
- 不同 scene 可以微調，但不要每個事件都用完全不同節奏
- narrated workflow 中，beat 的最短持續時間應由 `narration_manifest.json` 的 `duration_seconds` 決定
- 若視覺動作比旁白短，scene 應等待該 beat 的音訊播完
- 若視覺動作比旁白長，音訊可以先結束，但該 beat 的畫面焦點仍應保持一致
- 若 scene 有字幕，字幕切換應以 beat 為單位，不要每個 action 都跳字

## Scene 責任邊界

- Scene 不應重新計算演算法決策
- Scene 不應根據畫面需要自行發明新的 trace event
- Scene 可以決定 layout、顏色、停頓、標示方式
- Scene 應讓重要狀態變化可見
- Scene 應優先讀 `narration_manifest.json` 或等價的 beat 級 narration input，而不是臨時從畫面事件拼旁白
- Scene 應把每個 beat 的音訊檔視為同步輸入，不要在 Manim 層自行產生旁白文字
- Scene 若使用字幕，應優先讀 `subtitle_script.md` 或等價的 beat 級字幕輸入，而不是臨時從畫面事件拼字
- 除非使用者明確要求字幕，Scene 不應預設保留 subtitle-safe area

## 旁白建議

完整 workflow 預設包含旁白音訊，建議遵守以下原則：

- 以 beat 為單位播放旁白
- 每個 beat 的音訊路徑與長度應來自 `narration_manifest.json`
- 播放音訊時，畫面焦點應已經指向該 beat 要講解的資料結構或狀態
- 不要讓同一段旁白跨越多個不相關的視覺焦點
- 不要用額外等待時間掩蓋過長旁白；應回修 `voiceover.md` 或拆 beat
- 若缺少音訊檔或 duration，不能宣稱 narrated final delivery 完成

## 字幕建議

字幕是選配。只有在使用者明確要求字幕時，才加入字幕層並遵守以下原則：

- 以 beat 為單位切換字幕
- 將字幕固定在穩定區域，例如底部字幕列
- 主畫面與字幕列之間保留安全距離
- 切換字幕時保持短暫可讀停留
- 不要把字幕當成唯一教學來源；主畫面焦點仍應成立

## I/O 決策

目前 examples 採取「內嵌 `state_trace`」的設計。  
這樣做的優點是單檔可執行、便於教學與展示；缺點是 trace 更新時需同步 scene。

v2 預設：

- examples 可使用內嵌 trace
- narrated examples 可使用內嵌 narration manifest 或讀取外部 `narration_manifest.json`，但必須清楚說明採用哪一種
- 若進入正式 pipeline，亦可改為讀外部 JSON 與音訊檔，但需在專案層明確說明
