# Manim 指引

本文件定義 `generated_algo_scene.py` 應如何實作 `v4` 教學設計。

scene 是已確認 brief 與已核准 teaching script 的渲染器。它可以自由選擇實作結構，但不能發明新語意。

## 核心原則

scene layer 負責：

- layout execution
- styling
- timing
- beat staging
- audio 與 overlay synchronization

scene layer 不負責：

- semantic fork 決策
- delivery-tier 變更
- 新的 support-structure 需求
- 對 teaching goal 的重新詮釋

## 必要輸入

scene 必須以下列內容為基礎：

- 已確認的 `pre_build_brief.md`
- 已核准的 `teaching_script.md`
- 當需要維持執行忠實性時使用的 algorithm code 或 pseudocode
- 當 delivery tier 包含 narration 時，必須使用已核准的 `voiceover.md`、`narration_manifest.json` 與所需音訊資產

若 scene 無法說明自己正在實作哪個已凍結決策，就代表它還沒準備好 render。

## 建議檔案結構

讓 scene code 保持明確且可檢視，不要強迫所有演算法都套同一個模板。

建議區段：

1. constants 與 styling roles
2. scene-state structures
3. layout builders
4. beat helpers
5. `construct()`

建議 helper 群組：

- `build_primary_layout()`
- `build_support_layout()`
- `apply_role_style()`
- `play_beat()`
- `sync_voiceover()`
- `show_overlay_if_enabled()`

這些是組織期待，不是填空模板。只要 style roles、layout setup、beat execution、visibility ownership 與 final cleanup 仍然容易稽核，scene writer 就可以依演算法需要採用不同結構。

## 狀態管理

維持明確的語意狀態，而不是從目前外觀去推論含義。

典型狀態結構：

```python
self.role_state = {}
self.pointer_state = {}
self.layout_state = {}
self.beat_state = {}
```

至少要追蹤：

- 每個可見物件的語意角色
- active pointers 及其含義
- support-structure visibility
- 目前 beat id

這能讓修復工作具決定性，並避免樣式改變時意外漂移。

## Manim 可見性防線

以下規則針對 render layer 常見失敗，同時保留視覺設計自由度。

### Hidden Objects

- 除非有明確 reveal path，否則避免預先把重要物件以 `opacity=0` 加進場景。
- 對於還不該存在的物件，優先使用延後建立 / 加入。
- 若物件已存在但被隱藏，應透過明確狀態變化揭露，例如 `mobject.animate.set_opacity(1)`。
- 不要假設 `FadeIn` 一定能恢復已存在且隱藏物件的可見性，除非你已驗證最後穩定畫面。

### Phase Ownership

- 每個 helper object 都應屬於某個具名 phase、beat 或 mode。
- Intro 畫面不得出現 traceback、future-iteration 或 finalization helpers。
- Fill / update helpers 不得滲入 reconstruction 或 final-result 畫面，除非 script 說它們仍有意義。
- Traceback、path 或 reconstruction helpers 不得早於對應 mode 被引入時出現。

### Label Highlighting

- 不要在單字元 labels、prefix labels、row headers 或 column headers 上覆蓋實心 highlight box。
- 優先使用文字顏色變化、底線、相鄰標記，或已驗證透明填色的 outline-only shapes。
- 證據至少要包含一個穩定影格，能證明 active row / column、pointer 或 state labels 在 highlight 下仍可讀。

### Explanatory Text

- 當多行說明文字的行長或措辭差異很大時，避免使用 morph-style transforms。
- 優先使用直接替換、短 fade swap，或穩定 panel sections。
- 不要用 transition frames 當作文字清晰度的審查證據；應截取文字穩定後的影格。

### Final Cleanup

- 最終畫面應有意識地移除、淡化或安靜化過期 labels、helper marks、暫時公式文字與中介指示。
- 只保留最終結果呈現，以及已核准 script 要求保留的脈絡。
- 若某個 support structure 留在最終畫面，它必須仍具教學價值，而不是單純殘留的實作狀態。

## 以 Beat 為核心的實作

`v4` scenes 應以教學 beats 組織，而不只是原始 loop mechanics。

每個 beat 實作都應讓以下問題容易回答：

- 觀眾應該看哪裡
- 哪些物件承載焦點
- beat 結束後保留了哪個進度線索

用 loop 為中心的 code 可以接受，但最終動作仍必須讀起來像以 beat 為中心的教學。

## 視覺穩定規則

- 保持主要結構空間穩定
- 只移動觀眾需要追蹤的東西
- 讓 pointer 的起點與終點都清楚可辨
- 除非消失本身是課程的一部分，否則應淡化 resolved regions，而不是刪除它們
- 當 brief 說 support structures 在語意上重要時，就要讓它們持續存在

## Render-Layer 修復政策

允許在 `RENDER` 中修復：

- color styling
- label micro-placement
- spacing
- safe-margin tuning
- animation pacing
- 不改變已凍結語意的 implementation-fidelity 修復

不允許在 `RENDER` 中修復：

- 改變 movement semantics
- 改變 pointer meaning
- 改變 visited timing
- 改變課程中的 active support structure
- 改變 delivery-tier obligations

若實作暴露 script 不完整或 beat-structure mismatch，就停止並回到 `SCRIPT`。

若實作暴露已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上有缺漏或衝突，就停止並回到 `DESIGN_DEVELOPMENT`；要求設計修復、重新審查與重新核准，再重新產生並重新核准 brief。

若已核准設計清楚，但 brief 有錯誤文字或來源標籤，或是不忠實轉換，就停止並回到 `CONTRACT` 做 brief 修復與重新核准，無需重新設計。

## Voiceover 與 Overlay 同步

當 delivery tier 包含 voiceover 時：

- 每個已核准 beat 對應一個 voiceover segment
- 對應 narration 開始前，visual focus 必須先建立
- 該 beat 必須在 segment 結束前保持視覺一致
- 若 narration 太長，應縮短 narration 或在上游拆分 beats，而不是用空白時間掩蓋

當 overlays 關閉時：

- 不要預設保留只給 overlay 用的版面空間

當 overlays 啟用時：

- 把它們放在穩定且不碰撞的區域
- 避免蓋住主要教學結構

## Constants 與 Styling

優先使用清楚的語意名稱，而不是臨時 style values。

範例：

- `ROLE_BASE`
- `ROLE_FOCUS`
- `ROLE_CANDIDATE`
- `ROLE_SETTLED`
- `ROLE_EXCLUDED`
- `ROLE_SUPPORT`
- `MIN_BEAT_HOLD`
- `POINTER_LABEL_BUFF`

具體數值可依專案調整，但語意命名應保持穩定。

## 常見場景模式

### Arrays

- 隔離 active compare 或 update 區域
- 保持整列其餘部分可讀
- 標記 settled progress，但不要搶走 active operation 的焦點

### Search Windows

- 將 active window 顯示成一致的整體區域
- 區分 boundary pointers 與 current probe
- 在 elimination 後保留更新後的 window

### Graph Traversal

- 保持 node layout 固定
- 在視覺上區分目前擴展與已發現結構
- 當 queue 或 stack 是 brief 的一部分時，保持它可讀

## 審查準備度

在把 scene 交給審查前，請確認：

- 每個主要 beat 都能追溯到 brief 與 script
- 沒有任何語意含義依賴未陳述的 styling convention
- support structures 只在 brief 有正當理由時才出現
- audio 行為與所需 voiceover 產物符合選定 delivery tier
- overlay 行為符合 brief 已凍結的 overlay policy，或符合明確使用者 opt-in
- `render_preflight.md` 已存在，且引用從最新 render 抽出的證據
- 代表性的穩定影格能證明可見性、label 可讀性、phase isolation 與 final cleanup

## 常見失敗

- 為了讓版面更乾淨而刪除語意上必要的 support structure。
- 因 brief 模糊，就在 scene code 內自行決定語意。
- 讓動畫 polish 蓋過焦點清晰度。
- 把實作方便性當成重新詮釋課程的理由。
- 已加入但隱藏的物件沒有可靠的 opacity 或 creation path 就被揭露。
- helper objects 太早出現在它們的教學 phase 前。
- 用實心 highlight shapes 蓋住 labels。
- 用不可讀的 transition frame 來判斷 explanatory text。
