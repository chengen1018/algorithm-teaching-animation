# 動畫設計：Array Sorting

對 array sorting 動畫使用這份參考。Designer 以 `references/how-to-design-animation.md` 為共通流程；Reviewer 將本文件列出的要求加入專用審查條件。

## 必須說清楚的設計內容

### 每一步正在比較或更新哪些資料

Comparison-based sort 必須寫清楚每一步比較哪兩個元素，例如一對相鄰元素、key 與 candidate，或 pivot 與目前掃描的元素。比較對象與結果要先出現在畫面上，再呈現交換、移動或其他變化。

Non-comparison sort 必須改為寫清楚這一步正在更新什麼，例如 count、bucket、目前 digit 或 distribution；不要替原本沒有 comparison 的演算法加入比較動作。

### 元素要怎麼移動或更新

寫清楚畫面使用 swap、shift、copy，還是讓同一個元素物件移到新位置。觀眾必須能從路徑或空位看出實際發生的操作，不能把不同操作畫得一模一樣。

如果演算法更新的是 counts、buckets 或 auxiliary storage，就直接顯示那些資料的更新，不要暗示 array 元素正在移動。

### 如何顯示目前已完成到哪裡

選擇符合演算法的進度表示，例如已固定的 boundary、完成的 pass、處理完成的 digit、累積完成的 counts、已填入的 buckets 或完成合併的 runs。

不要預設所有 sorting 都有一段連續成長的 settled region。畫面必須讓觀眾分得出「目前正在處理」、「已完成」與「尚未處理」。

### 元素暫時移出陣列時放在哪裡

如果某個元素會暫時離開 array，而其他元素向空位 shift，畫面要提供清楚的暫放位置，並讓觀眾看得出該元素和空位的關係。

演算法沒有這種操作時，不要自行加入暫放區。Counts 或 buckets 只有在真的存放 array items 時，才可以視為元素的暫放位置。

### 相同數值的元素是否需要區分

如果 equal values 的相對順序或移動會影響教學目標，使用 labels、tokens 或其他不只依賴顏色的方式維持元素身份，讓觀眾能判斷 stability。

如果元素身份與教學目標無關，就不要加入會讓觀眾誤以為動畫正在檢查 stability 的標記。

## 教學風險

### 動作太快，觀眾看不出原因

先顯示造成變化的 comparison 或 update，再呈現 swap、shift、placement 或 auxiliary update。必要證據要保留到因果關係已經清楚。

### 正在處理和已完成看起來一樣

目前焦點與完成進度必須使用不同呈現。暫停畫面時，不能讓仍在處理的元素看起來已經完成或永久定位。

### 範例沒有出現關鍵操作

範例至少要實際出現這個演算法最重要的操作，例如 comparison、swap、shift、partition、merge、count update、bucket placement 或 digit pass。設計中要指出它發生在哪一步。
