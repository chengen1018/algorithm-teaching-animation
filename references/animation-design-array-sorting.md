# 動畫設計：Array Sorting

在套用通用教學設計指引之後，對 array-sorting 動畫使用這份參考。它補充如何理解 comparisons 或 updates、movement、identity 與 progress 的專用決策；不會取代流程或產物契約。

## 必要設計決策

### active comparison unit

設計必須定義符合該演算法的 active decision 或 update 單位。對 comparison-based sort，要說明這個單位是 pair、key 與 candidate、pivot 與 scanned item，或其他精確元素組合；比較的 operands 與結果必須在 resulting change 之前就變得可見。對 non-comparison sort，則要辨識 count、bucket placement、digit pass、distribution step，或其他造成下一個狀態變化的 update，並顯示其輸入與結果，而不是硬發明 comparison。

### movement model

當元素移動時，設計必須選定它是 swap、shift、copy，還是作為持續物件移動。Position 必須在整個操作中編碼一個穩定含義。要顯示足夠的路徑或中間空位，讓觀眾能分辨所選操作與視覺上相似但語意不同的操作。若演算法更新的是 counts、buckets 或 auxiliary storage，則應定義該 update 模型，而不要暗示其實不存在的元素移動。

### settled-progress expression

設計必須定義符合該演算法的 progress 模型，例如 settled boundary、completed pass、processed digit、accumulated counts、filled buckets 或 merged runs。不應預設一定有一個連續成長的 settled region。若「settled」有意義，必須精確說明它保證什麼；否則就使用更符合演算法的 progress 語言。Progress styling 必須與 active decision / update 以及 untouched data 保持區別，避免觀眾把「正在被注意」誤認成「已完成」。

### temporary holding position

若某項目離開 array，而其他項目會 shift，設計必須提供一個可見的 temporary holding position，並保留該項目與 open slot 之間的關聯。若演算法從未把項目暫時拿到 array 外，必須明確說明，且不得憑空發明一個會暗示錯誤狀態的 holding area。Auxiliary counts 或 buckets 不能被當成 temporary holding position，除非它們真的存放 array items。

### duplicate-value identity tracking

當 equal values 的相對順序、移動，或 bucket placement 會影響理解時，設計必須為這些項目提供持續身份。應透過 labels、tokens 或其他非純色彩線索，讓觀眾能區分 value equality 與 object identity，並正確觀察 stability 或 instability。若身份對既定目標不重要，就不要加入會暗示正在評估 stability 的追蹤機制。

## 教學風險

### 會掩蓋因果的 movement

不要在顯示造成它們的決策或 update 之前，就先動畫化多個 swaps、shifts、placements 或 auxiliary updates。對 comparison-based sorts，要把 comparison 證據與其結果分開；對 non-comparison sorts，則應保留相關的 count、digit、bucket 或 distribution 證據，直到因果連結足夠清楚。

### settled styling 與 active styling 太像

若設計使用 settled styling，就不要讓它與 active styling 相似。對沒有 settled elements 的演算法，應改為把所選 progress 模型與 active update 區分開。必須確認在暫停畫面時，不會讓 still-in-progress 的項目看起來像已完成或已永久定位。

### sample 從未示範關鍵操作

不要選一個避開演算法特徵性 comparison、swap、shift、partition、merge、count update、bucket placement、digit pass，或其他必要操作的 sample。應預先指出那個關鍵操作，並標明 sample 中哪個精確時刻迫使它發生。
