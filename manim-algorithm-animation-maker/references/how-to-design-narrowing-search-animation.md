# 動畫設計：Search

只有當演算法維持並逐步收縮明確的候選區間或區域，且每次決策都會淘汰部分候選內容時，才使用這份參考。Linear、graph、substring 或其他沒有候選區域淘汰的搜尋只使用共通設計指南。

## 必要設計決策

### 區間採 closed 還是 half-open

設計必須宣告精確的 interval convention，例如 closed `[low, high]` 或 half-open `[low, high)`，並在 labels、brackets 與 region shading 中一致編碼。每一次 endpoint 更新都必須可見地保持該慣例。

### 每個 pointer 代表什麼

設計必須定義每個 pointer 所代表的意義：候選端點、probe position、insertion boundary，或其他精確角色。Pointer 的 labels 與位置必須避免讓觀眾把某個 index 與該 index 上存放的 value 混淆。

### 什麼情況下停止

設計必須以所選 interval convention 來說明 success 與 failure 的停止條件。最終畫面必須顯示符合該規則的狀態，而不是從最後一次 comparison 直接跳到結果 caption。

### 為什麼可以排除某一側

設計必須顯示為什麼某次 comparison 能證明某個區域不可能包含 target。要先強調被比較的 values 與相關排序事實，再標記被淘汰區域，讓 exclusion 是以證據為基礎，而不是像魔法消失。

### pointer 更新的呈現順序

設計必須讓每個循環依序呈現 probe、comparison、conclusion，再來 pointer update。若多個 pointers 都會變動，就必須排序呈現，或把它們綁到同一個 conclusion，讓觀眾能辨識是哪一次 comparison 導致每一個移動。

### 被排除的區域要保留多久

設計必須讓 excluded regions 在被理解之前，保持 dimmed 但可讀。這種持續性應傳達累積證明與逐步縮小的可能性，同時讓 active interval 仍是主角。

## 教學風險

### 太早刪除脈絡

不要立刻移除被排除的值。太早刪除會隱藏候選集合如何縮小，也會讓後續 pointer 位置顯得任意；應保留足夠脈絡，讓觀眾能比較舊區間與新區間。

### 視覺上暗示錯誤的 interval convention

不要把 endpoint markers、brackets 或 shading 放在與宣告慣例矛盾的位置。要檢查 boundary frames，尤其是 empty 與 one-element cases，因為這些畫面最容易暴露 off-by-one 含義。

### 移動 pointers 時沒有先顯示造成移動的 comparison

不要把 pointer update 動畫化成沒有解釋的導航步驟。在移動過程中，probe、target、comparison relation 與被淘汰那一側都應保持可見，讓觀眾能重建這個決策。
