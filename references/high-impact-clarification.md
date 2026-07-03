# 高影響澄清

將這份參考當成 `animation-designer` 在 `DESIGN_DEVELOPMENT` 階段使用的高影響問題清單。這份清單幫助設計師找出會阻塞的核心選擇；澄清是為了支援設計，不可取代 `animation_design.md` 的產出。

## 批次協定

設計師應先在內部規劃一小批、彼此緊密相關、對下一步設計必要的阻塞性問題。每個問題都要提供：

- 具體建議；
- 該建議的理由；
- 重要取捨或後果；
- 在適合時提供簡潔選項。

orchestrator 每次只向使用者提出一個面向使用者的問題，等待答案，忠實記錄後再問下一題。不得重述、弱化、合併，或悄悄以建議取代使用者答案。

等整批規劃好的問題都回答完後，orchestrator 應一次把忠實記錄的整批答案回傳給 `animation-designer`。不要在每個答案之後就回到 designer。designer 只更新一次設計，並重新評估所有剩餘核心缺口。只要重新評估後仍有任何未解決阻塞，不論是原本已知或新暴露出來的，就應再規劃另一小批問題。

## 何謂高影響

若答案會改變以下任一項，該缺口就屬於高影響：

- 動畫語意
- 教學焦點
- 交付內容

若答案只影響一般樣式或顏色、小幅位置調整、例行 transition、easing，或局部 timing，則不算高影響；除非該選項被明確指出對 accessibility、正確性、驗收或教學目標很重要。

## 決策類別

### 語意分歧

當存在多個合理詮釋，且選擇會改變觀眾學到什麼時，使用這個類別。

範例：

- insertion sort 的移動模型
- binary search 的區間慣例
- graph traversal 在 discovery 時標記節點，還是在 processing 時標記

### 教學焦點分歧

當不同強調方向會改變節拍結構或視覺注意力時，使用這個類別。

範例：

- 將 binary search 視為區間推理，或視為分支控制推理
- 將 BFS 視為 queue 行為，或視為 layer 擴展
- 將 sorting 視為移動直覺，或視為邊界進展

### 影響交付的分歧

當答案會改變交付形態或版面義務時，使用這個類別。

範例：

- no narration 與 final narrated delivery
- overlays 是否啟用
- 某個支援結構是否必須持續可見

## First-Class Support 問題清單

當 intake 類別屬於 first-class support 時，使用以下精簡清單。

### Array Sorting

至少檢查：

- active comparison unit
- 是否存在重要的 movement-semantics 分歧
- settled-progress 表達方式
- temporary holding position 是否屬於課程內容的一部分

### Binary Search 與區間 / 候選區域收縮型 Two-Pointer Search

這份 first-class 清單只適用於 binary search，以及會淘汰候選區間或區域的 two-pointer searches。

至少檢查：

- interval convention
- pointer meaning
- stopping rule 或 success criterion
- 課程是否強調 elimination logic、pointer choreography，或兩者皆重視

廣義或非淘汰型的 two-pointer / search 類需求，不能自動使用這份清單。若有相符專用參考，應用它；否則使用通用設計指引，將需求標記為 best-effort，揭露覆蓋風險，並要求強化獨立審查。

### BFS 與 DFS

至少檢查：

- support-structure visibility
- visited timing
- discovery 與 processing 的強調差異
- frontier 或 stack/path 的強調
- 當 sample input 讓順序可見時，neighbor-order 預期為何

## 不該問的問題

不要把澄清預算花在：

- 一般顏色偏好
- 小幅 pointer 或 label 位置
- 例行 transitions
- easing
- 局部 timing 或 pacing 微調
- 一般鏡頭克制選擇
- 除非使用者真的要 overlays，否則不要問字幕需求

這些低影響細節應交給 best-effort 預設值處理，不能阻塞 `DESIGN_READY`。只有當 intake 或目前設計明確指出它們具有高影響時，才可提問。

## Designer Inventory 結果

在規劃下一小批問題前，designer 可以先用以下格式整理內部清單：

```md
# High-Impact Inventory

## Resolved High-Impact Decisions
- Decision:
- Why it matters:
- Source: user answer / user-approved default

## Delivery Decisions
- Delivery tier:
- Overlay policy:

## Still Blocked
- None

## Low-Impact Defaults (Not Questions)
- Default:
- Why it is low risk:
```

## 預設值提案規則

提出預設值時，應把它寫成使用者可以核准或修改的明確決策。

好的寫法：

- 「如果你沒有偏好，我會把 active search interval 視為 closed，並讓被淘汰區域保持 dimmed。」

不好的寫法：

- 默默把 interval rule 寫進 brief
- 問一個含糊問題，卻不解釋為什麼這個選擇重要

## 升級處理範例

- 若 intake 提出兩種合理教學 framing，且它們都會改變節拍重心，就應直接詢問該 teaching-focus fork，而不是自行決定。
- 若使用者對某個高影響語意分歧沒有偏好，應提出一個具體預設值供其核准，而不是把它藏進 brief。
- 若 delivery-tier 的改動也會影響 overlays、narration 或 support-structure visibility，就應一起凍結這些決策。
- 若在完成一批問題後的重新評估中暴露出新的語意、教學或交付 blocker，就應再規劃一小批問題，而不是猜測或直接宣告 `DESIGN_READY`。

## 常見失敗

- 問了很多低價值問題，卻漏掉真正重要的語意分歧。
- 明明交付決策會改變版面或輸出，卻把它當作可選項。
- 寫出「follow standard semantics」，但其實存在多種標準。
- 把未解決的歧義偷偷塞進「show the normal process」這類模糊文字裡。
- 把整批問題當成一個多段式使用者提問，或把答案一題一題送回 designer。
- 問題中缺少建議、理由或取捨說明。
