# Teaching Script

本文件定義 `algorithm-teaching-animation-v3` 中的 `teaching_script.md`。

script 是介於已確認 brief 與最終 scene 之間的教學結構層。

它不是：

- 澄清工作的替代品
- 用來定案未解決語意的地方
- 逐行場景實作

## 目的

script 應把已凍結 brief 轉成一個節拍序列，回答以下問題：

- 每個 beat 想教什麼
- 觀眾應該看哪裡
- 局部動作如何逐步累積成整體課程

## 真實來源

script 必須從以下來源推導而來：

- 已核准的 `pre_build_brief.md`
- 具體 sample input 或 scenario
- 只有在為了忠於演算法流程時，才使用 code 或 pseudocode

若 script 需要做出語意選擇，原因是已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上有缺漏或衝突，則必須停止並回到 `DESIGN_DEVELOPMENT`；要求設計修復、重新審查與重新核准，再重新產生並重新核准 brief。

若已核准設計是清楚的，但 brief 有錯誤文字或來源標籤，或在忠實轉換上失敗，則必須停止並回到 `CONTRACT` 做 brief 修復與重新核准，無需重新設計。

## Gate 依賴

在獨立審查產出 `script_review_result.md = PASS` 前，`teaching_script.md` 不得被視為已核准供下游 narration 或 render 使用。

在 script review 通過前，不得開始任何 narration 工作。

## 建議結構

```md
# Teaching Script

## Summary
- Algorithm:
- Teaching goal:
- Audience:
- Delivery tier:
- Key semantics:

## Beats

### Beat 1: ...
- Viewer goal:
- Algorithm moment:
- Visual focus:
- Teaching note:
- Progress cue:
- Voiceover intent:

### Beat 2: ...
...
```

標題可略有變化，但資訊仍必須容易稽核。

## 必要 Beat 內容

每個 beat 都應定義：

- `Viewer goal`：觀眾應從此 beat 理解什麼
- `Algorithm moment`：此 beat 對應演算法流程中的哪一段
- `Visual focus`：畫面中最該被注意的是什麼
- `Teaching note`：為什麼這一刻重要
- `Progress cue`：此 beat 結束後，什麼仍然成立
- `Voiceover intent`：後續 voiceover 應承載的口語 takeaway

## Script 規則

- 一個 beat 應只有一個主要教學點與一個主要局部教學事件
- 使用具體、面向觀眾的語言
- beat 順序必須忠於已凍結語意
- 當支援結構對教學重要時，應在相應 beats 保持可見
- 不要用「the normal step」這種泛稱來隱藏未解決歧義
- 不要把多個具名的局部比較、選擇、交換或 pointer move 塞進同一個 beat，若它們其實需要分開被講述

## Beat 設計指引

好的 beat 通常遵循以下節奏：

1. 建立當前局部狀態
2. 顯示局部決策或轉換
3. 顯露進度線索或不變量

一個 beat 可以長於或短於一次 loop iteration，但仍要保持可教。

## Beat 原子性指引

對需要 narration 的 tier，beat 通常應對應到一個能在單一 voiceover segment 下維持視覺一致的教學單位。

當觀眾需要依序追蹤多個局部決策時，應進一步細分 beat，尤其是像下面這些情況：

- compare-then-choose 於兩個 active candidates 之間
- 會改變局部狀態的 swap 或 pointer move
- 被移動 candidate 在新位置上的重新檢查

若口語解說必須一路說「然後……然後……然後……」來跨越多個局部比較、交換或 pointer 移動，這個 beat 通常就太粗，應在 `SCRIPT` 上游先拆開。

只有當教學目標明確是摘要層級，而不是逐步理解時，beat 才可以總結重複工作。

## 與 Voiceover 的關係

script 是上游教學來源，供後續 voiceover 依照 beats 忠實產生 narration。

這表示：

- script 本身就應包含教學邏輯
- 後續 voiceover 應在不改變 beat 含義的前提下，將其壓縮並口語化
- 如果 voiceover 需要發明新想法，表示 script 不完整

## Script Review 交接

在任何 narration 或 scene 階段把 script 當成已定案前，它必須能依據已核准 brief 被審查。

審查 gate 結果是 `script_review_result.md`。

利用這個審查確認：

- script 符合已核准 brief
- 每個 beat 都有具體教學目的
- 下游 voiceover 可以忠於 beat 而不用猜
- 下游 render 工作不需要自行發明缺失語意

## 與 Scene 工作的關係

script 必須強到讓 scene writer 不用猜就能實作：

- 焦點應落在哪裡
- 哪個結構必須保持可見
- 何時進度應變得可見

scene 可以選擇版面細節，但不應該還要替課程本身做決策。

## 常見失敗

- 寫成場景描述，而不是教學規劃。
- 寫出無法映射到 beats 的通用演算法散文。
- 把多個彼此無關的 takeaway 塞進同一個 beat。
- 把多個連續局部決策塞進同一個 beat，卻期待下游 voiceover 或 scene 自行推論隱藏子節拍時序。
- 讓 script 結構偏離已凍結 brief。
