# 視覺語言

使用這些面向觀眾的規則，讓演算法狀態、控制與進度保持可讀。

## 權責分界

`DESIGN_DEVELOPMENT` 負責核心視覺語意、場景結構、持續存在的支援結構、資訊層級，以及讓演算法狀態可教的面向觀眾因果關係。這些決策都必須定義在已審查且已核准的 `animation_design.md` 中。

本檔案提供較高層、面向觀眾的原則，用來判斷那些設計決策是否清楚、一致且語意穩定。

- 當要判斷某個預設呈現方式對觀眾是否足夠清楚時，使用本檔案。
- 若已核准設計或 brief 與這些清晰度或語意穩定原則衝突，應把該衝突視為上游契約缺陷。下游 agents 不得自行決定優先順序，也不得在本地修補。
- 若 `pre_build_brief.md` 錯誤轉譯了已核准的 `animation_design.md`，就送回 `CONTRACT`。若衝突出自已核准設計本身，則送回 `DESIGN_DEVELOPMENT`，並要求重新獨立審查、精確版本的外部重新核准、重新做 CONTRACT 轉換，以及在下游恢復前重新核准 brief。
- `default-visual-semantics.md` 的權限最低，絕不可用來解決已核准設計、已核准 brief 與視覺語言原則之間的衝突。
- 不要用本檔案引入、修補，或默默補完那些上游從未定案的核心語意。
- 若下游視覺語言檢查發現缺少核心語意、場景結構、持續支援結構、資訊層級或因果關係，就必須把缺口送回 `DESIGN_DEVELOPMENT`；不得在本地自行修補。

## 核心原則

- 教學清晰度優先於裝飾性動作
- 穩定語意優先於視覺變化
- 每個 beat 只保留一個主導焦點
- 已解決區域應保持可理解，但不與當前動作競爭
- 版面穩定性也是課程的一部分

## 語意穩定性

每一個持續存在的視覺線索，在動畫中都應只維持一個穩定含義。

這包括：

- role color
- border 或 fill 強調方式
- pointer 樣式
- support-structure 的處理方式
- excluded-region 的處理方式

若觀眾在動畫中途必須重新學一次某個線索的含義，就代表視覺語言失敗了。

## 焦點控制

每個 beat 都應該讓以下事情一目了然：

- 第一眼應該看哪裡
- 第二重要的是什麼
- 現在什麼只是背景脈絡

常見焦點工具：

- 更強的對比
- 局部動作
- 暫時性的放大或分離
- 降低非活躍區域的存在感

不要一次強調所有東西。

## 版面穩定

- 保持主要結構固定
- 不要為了局部更新就讓整個場景重新排版
- 讓 pointer 的移動路徑容易追蹤
- 只有在局部契約要求時，才引入新的支援結構

## 角色區分

至少要讓觀眾能分辨出：

- base data
- current focus
- candidate 或 active comparison target
- settled progress
- excluded region
- support structure

## 支援結構

Queues、stacks、temp slots、helper windows 與類似結構不是中性的裝飾。

- 若局部契約說這個結構重要，就在課程依賴它時保持可見。
- 若局部契約說它非必要，就不要為了好看硬加。
- 支援結構應呈現為次要，但不能隱形。

支援結構是否存在、是否持續可見，屬於核心設計決策。本參考只判斷已核准選擇的清晰度，不會在下游發明這個選擇。

## 文字與標籤

- labels 保持短且具體
- 優先用 label 命名角色，而不是在畫面上寫完整說明
- labels 的放置位置要一致
- 只有當局部產物 opt in 時，才使用 overlay text

## 動作規則

- motion 應幫助說清楚因果
- active motion 應對應該 beat 的教學重點
- pause 是用來確認進度，不是用來裝飾轉場
- 若 motion 讓角色區分變得模糊，就應簡化它

## 模式專用強調

### Array Sorting

- 把 active pair 與 settled region 分開
- 讓進度邊界容易辨識
- 保持整列可見，讓局部動作仍有整體脈絡

### Binary Search 與區間 / 候選區域收縮型 Two-Pointer Search

- 保持 active interval 在視覺上是連續且一致的
- 區分 boundary pointers 與 active probe
- 讓 elimination 可見，但不要過早刪除脈絡

### BFS 與 DFS

- 把目前擴展中的部分與已發現結構分開
- 當 traversal support structures 是課程的一部分時，要讓它們保持可讀
- 當順序影響理解時，讓 ordering cues 清晰可辨

## Overlay 安全性

- 不要預設保留 overlay 空間
- 不要只是因為有空間就加字幕或 callouts
- 不要僅因 delivery tier 就推斷 overlays 必須存在
- 若 overlays 已啟用，要讓它們避開教學關鍵區域

## 升級處理範例

- 某種 highlight 處理讓 `candidate` 和 `settled` 看起來一模一樣。
- 新增某個支援結構只是為了讓畫面看起來更滿。
- overlay 的位置蓋住了 active comparison 或 active interval。
- 因為已核准設計漏掉某個場景區域或因果視覺線索，導致下游階段不得不自行發明。

## 常見失敗

- 使用一種 style flourish，卻改變了角色含義。
- 為了讓畫面更乾淨而隱藏教學關鍵結構。
- 把每個 active object 都當成同樣重要。
- 讓 overlays 擠壓主要教學內容。
