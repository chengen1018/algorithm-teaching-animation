# 預設視覺語意

當上游語意選擇已經定案後，使用這些低風險預設值來處理一般呈現選項。

## 權責分界

本檔案只負責在核心設計凍結後，提供一般呈現的低風險 fallback 決策，例如普通配色、小幅位置調整、easing 與局部 timing。

- 當已核准設計與較高層視覺原則仍留有一般性選擇空間時，使用本檔案提供例行預設值。
- 不要用這些預設值來取代缺失的核心設計決策。
- 不要用本檔案覆蓋已核准的 `animation_design.md` 或 `references/how-to-design-animation.md`。
- 不要用本檔案推翻 `references/how-to-design-animation.md` 所涵蓋的清晰度問題；核心缺口應升級送回 `DESIGN_DEVELOPMENT`。
- 這些預設值的權限最低，絕不能用來解決已核准設計與 `references/how-to-design-animation.md` 之間的衝突。遇到衝突時，應走動畫共同設計指南的回退路線，而不是自行決定優先順序或在本地修補設計。

## 適用範圍

可用這些預設值處理：

- 已定義角色的一般配色選擇
- pointer 與 label 的小幅位置調整
- 例行 label wording
- 一般 transitions 與 easing
- 局部 timing 與一般 beat pacing
- 常見 first-class support 版面

不可用這些預設值決定：

- 會改變觀眾理解內容的 movement semantics
- search variant semantics
- pointer meaning
- visited timing
- overlay enablement
- 核心視覺語意或角色定義
- 場景結構或資訊層級
- 支援結構是否存在或是否持續
- 面向觀眾的因果關係

## 全域預設

除非局部產物另有規定：

- 每個 beat 保留一個 primary focus cluster
- base elements 在不同 beats 之間保持空間穩定
- focus styling 強於 support styling
- settled 或 resolved 區域保持可見，但比 active focus 更安靜
- excluded regions 以 dimmed 呈現，不直接刪除；除非消失本身就是教學重點
- pointer labels 保持與演算法實際名稱一致，例如 `left`、`right`、`mid`、`i`、`j`、`front` 或 `back`
- pointer labels 放在其所支配結構附近，並保持在同一側
- 除非局部產物 opt in，否則 optional overlays 預設關閉
- 使用節制的 easing 與可讀的局部 timing；兩者都不得改變已核准的因果含義或節拍重點

## 預設角色詞彙

如果專案沒有自訂配色，請維持以下角色詞彙穩定：

- `base`：不活躍但仍相關的資料
- `focus`：目前主要要檢查的物件或區域
- `candidate`：正在比較、考慮或更新的值或區域
- `settled`：在課程中其角色已經確定的區域
- `excluded`：已不再活躍的區域
- `support`：像 queue、stack 或 temp slot 這樣的次要結構

## 一般版面預設

### Arrays 與索引型結構

- main array 預設維持水平，除非垂直版面明顯更好
- pointer labels 放在 array 的上方或下方，不要直接蓋在值上
- 當 index labels 不是教學焦點時，保持它們較小且次要
- 即使某些元素被抬起、比較或移動，也要保留元素間距

### Search Windows 與 Ranges

- 保持 active range 在視覺上連續
- excluded regions 以 dimmed 呈現，而不是直接刪除
- 只要 range boundaries 仍然重要，就保持可見
- 讓 current probe 與整個 active range 清楚區分

### Graph Traversal

- node positions 一旦引入就固定
- 除非 edge traversal 是當前焦點，否則 edge styling 要比 node state styling 更安靜
- 當已核准設計說支援結構重要時，就顯示該支援結構
- 讓處理完成的區域慢慢安靜下來，而不是消失

## First-Class Support 預設

### Array Sorting

- 給 active compare pair 最強的 focus treatment
- 只有當目前語意已包含該動作時，才讓正在移動或插入的值抬高或分離
- 讓 settled prefix 或 suffix 保持可見標記
- 讓非 active 值持續可見，這樣局部動作仍能被讀成整體 array 的一部分

### Binary Search 與區間 / 候選區域收縮型 Two-Pointer Search

- 把 active interval 顯示成一個可讀的整體區域
- 在每個相關 beat 的全程中，保持 active boundary pointers 可見
- 讓 probe location 與 boundaries、excluded region 都有明顯區別
- 在 boundary 更新後，保留新 interval 足夠久，讓收縮效果能被看見

### BFS 與 DFS

- 區分 current node 與 discovered-but-not-yet-expanded nodes
- 當 support structure 是課程的一部分時，保持它可讀
- 透過 grouping、border treatment 或 support-structure focus 來強調 frontier
- 只有在順序重要時才加入 neighbor-order cues

## 文字預設

- 優先用短 labels，不用句子型 labels
- 畫面文字應命名目前規則或觀察，而不是重複 narration
- 只有當局部產物 opt in 時，才使用 captions 或 overlay text
- 如果某句話更適合放在 voiceover，就優先放 voiceover

## 動作預設

- 只移動觀眾需要追蹤狀態的物件
- 優先採用直接、可讀的路徑，而不是裝飾性動作
- 引入新焦點前，先移除或淡化舊焦點
- 在加入裝飾之前，先保住觀眾的心理地圖

## 升級處理範例

- 明明沒有任何局部產物確認，卻出現了 temp slot。
- 某種 range style 暗示是 closed interval，但 interval convention 其實尚未指定。
- 課程依賴 queue semantics，卻把 queue visibility 拿掉了。
- 已核准設計缺少場景區域或持續支援結構，結果用預設值硬發明出來。

## 常見失敗

- 用顏色發明上游從未定案的語意。
- 因為版面比較乾淨就把 active support structure 藏起來。
- 一般 label 位置明明有合理預設值，卻仍把它升級成問題。
- 用預設值逃避真正的語意分歧。
- 當 ordinary colors、小幅位置、easing 或局部 timing 並不明確重要時，卻把它們當成核心設計 blocker。
