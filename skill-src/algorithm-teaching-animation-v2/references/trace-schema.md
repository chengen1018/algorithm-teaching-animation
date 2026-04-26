# Trace Schema

本文件定義 `algorithm-teaching-animation` skill 中使用的 `action_trace.json` 格式。

`action_trace.json` 是演算法事件與狀態轉移的單一真相來源。  
它由 `generated_trace_script.py` 執行後輸出，並由 `generated_algo_scene.py` 進一步轉譯為 Manim 動畫。

本文件的目標是：

- 定義目前支援的 action vocabulary
- 說明每種 action 的語義、欄位與使用時機
- 限制 trace 層的責任範圍
- 避免將演算法邏輯偷偷塞進 Manim 層
- 提供未來擴充 schema 的原則

## 核心原則

Trace schema 應遵守以下原則：

- trace 必須 deterministic
- trace 必須對應真實的演算法執行
- trace 必須描述有教學價值的狀態轉移
- trace 不應記錄純裝飾性的動畫效果
- trace 不應包含 Manim 實作細節
- trace 必須足以支撐 `teaching_script.md` 的教學 beat

換句話說，trace 描述的是「演算法世界裡發生了什麼」，不是「畫面要怎麼做特效」。

## 基本格式

`action_trace.json` 是一個 JSON array。  
其中每一個元素都是一個 action object，至少必須包含：

- `action`：字串，表示 action 類型

範例：

```json
[
  {"action": "create_array", "id": "main", "values": [5, 2, 4, 6, 1, 3]},
  {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
  {"action": "swap", "target_id": "main", "i": 0, "j": 1}
]
```

## 命名規則

### ID 命名原則

所有可被後續 action 參照的物件都必須有穩定 ID。

建議命名方式：

- 陣列：`main`、`arr1`、`aux`
- 矩陣：`dp`、`table`
- 指標：`p_i`、`p_j`、`p_left`、`p_right`、`p_mid`
- 其他結構：依未來 schema 擴充規範命名

原則：

- 同一個 ID 在同一份 trace 中只能代表一個邏輯物件
- 不要重複使用已移除 pointer 的 ID 來表示不同角色
- 名稱應有語義，不要用無意義流水號，除非該結構本身真的需要

## Action 分類

目前 v2 支援五大類 action：

- Array Actions
- Matrix Actions
- Pointer Actions
- Graph Actions
- Range / Region Actions

## 1. Array Actions

用於排序、搜尋、一維 DP、雙指標、滑動視窗等以一維序列為核心的任務。

### `create_array`

用途：  
建立一個新的陣列視覺物件。

必要欄位：

- `action`: `"create_array"`
- `id`: `str`
- `values`: `list`

範例：

```json
{"action": "create_array", "id": "main", "values": [3, 1, 4]}
```

使用規則：

- 對同一個 array 進行任何操作前，必須先 `create_array`
- 同一個 array ID 不應重複建立，除非未來 schema 明確支援重建語義
- `values` 應反映該資料結構的初始狀態

### `highlight`

用途：  
標示目前被關注、比較或檢查的陣列元素。

必要欄位：

- `action`: `"highlight"`
- `target_id`: `str`
- `indices`: `list[int]`

選配欄位：

- `color`: `str`，預設通常為 `"YELLOW"`

範例：

```json
{"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"}
```

使用規則：

- 用於表達「目前焦點」或「目前比較對象」
- 不要把純裝飾性的閃爍也寫成 `highlight`
- 若某些元素不再是焦點，應搭配 `unhighlight`

### `unhighlight`

用途：  
取消陣列元素的焦點標示。

必要欄位：

- `action`: `"unhighlight"`
- `target_id`: `str`
- `indices`: `list[int]`

範例：

```json
{"action": "unhighlight", "target_id": "main", "indices": [0, 1]}
```

使用規則：

- 與 `highlight` 成對出現最清楚
- `unhighlight` 的目標是將元素還原為最近的穩定語義狀態，例如 `default`、`sorted`、`excluded`
- 若元素進入新的語義狀態，應由更具體的 action 先建立該狀態，再由 renderer 在 `unhighlight` 時回到該穩定狀態

### `swap`

用途：  
記錄兩個位置的值交換。

必要欄位：

- `action`: `"swap"`
- `target_id`: `str`
- `i`: `int`
- `j`: `int`

範例：

```json
{"action": "swap", "target_id": "main", "i": 1, "j": 2}
```

使用規則：

- `swap` 應發生在 Python 實際交換資料之前記錄
- 它表示「這兩個位置將交換」，而不是純動畫效果
- 若演算法概念上沒有交換，而是覆寫或搬移，應優先使用 `overwrite`

### `overwrite`

用途：  
記錄某個位置的值被新值覆蓋。

必要欄位：

- `action`: `"overwrite"`
- `target_id`: `str`
- `index`: `int`
- `new_value`: 任意 JSON 可表達值

範例：

```json
{"action": "overwrite", "target_id": "main", "index": 2, "new_value": 9}
```

使用規則：

- 用於 insertion、merge、一維 DP 更新、shift 類操作
- 若實際語義是值被覆寫，不應假裝成 `swap`
- `new_value` 必須與演算法執行後的真實結果一致

### `mark_sorted`

用途：  
標記某些位置已經完成、固定，或進入不再變動的狀態。

必要欄位：

- `action`: `"mark_sorted"`
- `target_id`: `str`
- `indices`: `list[int]`

範例：

```json
{"action": "mark_sorted", "target_id": "main", "indices": [4]}
```

使用規則：

- 不限於排序，也可表示「此元素狀態已確定」
- 但若語義其實不是 sorted，而是 visited 或 processed，未來應考慮擴充更精確的 action 名稱，而不是濫用 `mark_sorted`

## 1.5 Range / Region Actions

用於表達區間被排除、失效、或進入特殊區域狀態。這類 action 的重點是區域語義，不是單點焦點。

### `mark_excluded`

用途：  
標記一段陣列索引區間已被排除，不再屬於當前有效範圍。

必要欄位：

- `action`: `"mark_excluded"`
- `target_id`: `str`
- `indices`: `list[int]`

選配欄位：

- `color`: `str`，若未指定，通常由 renderer 使用較低存在感的 excluded style

範例：

```json
{"action": "mark_excluded", "target_id": "main", "indices": [0, 1, 2, 3]}
```

使用規則：

- 用於表達「這一段已被排除」這種穩定語義
- 不要再用 `unhighlight` 兼任排除區間語義
- 若某元素後續仍可能恢復為有效區域，應另行定義更精確的 action，而不是濫用 `mark_excluded`

## 2. Matrix Actions

用於二維 DP、表格建構、grid state 演算法等。

### `create_matrix`

用途：  
建立一個新的矩陣視覺物件。

必要欄位：

- `action`: `"create_matrix"`
- `id`: `str`
- `rows`: `int`
- `cols`: `int`
- `values`: `list[list]`

範例：

```json
{"action": "create_matrix", "id": "dp", "rows": 3, "cols": 4, "values": [[0,0,0,0],[0,0,0,0],[0,0,0,0]]}
```

使用規則：

- 任何 cell 操作前都必須先 `create_matrix`
- `values` 應反映初始表格狀態

### `highlight_cell`

用途：  
標示目前正在計算、比較或關注的 cell。

必要欄位：

- `action`: `"highlight_cell"`
- `target_id`: `str`
- `row`: `int`
- `col`: `int`

選配欄位：

- `color`: `str`

範例：

```json
{"action": "highlight_cell", "target_id": "dp", "row": 1, "col": 2, "color": "YELLOW"}
```

### `unhighlight_cell`

用途：  
取消 cell 焦點標示。

必要欄位：

- `action`: `"unhighlight_cell"`
- `target_id`: `str`
- `row`: `int`
- `col`: `int`

範例：

```json
{"action": "unhighlight_cell", "target_id": "dp", "row": 1, "col": 2}
```

### `set_cell`

用途：  
記錄某個 cell 被寫入新值。

必要欄位：

- `action`: `"set_cell"`
- `target_id`: `str`
- `row`: `int`
- `col`: `int`
- `new_value`: 任意 JSON 可表達值

範例：

```json
{"action": "set_cell", "target_id": "dp", "row": 2, "col": 3, "new_value": 7}
```

使用規則：

- 用於表示 DP 狀態被確定或更新
- 若某個 cell 的教學重點是其依賴來源，應在 `teaching_script.md` 中說明，不要把依賴語義藏進 `set_cell`

### `mark_cell`

用途：  
將 cell 標記為具有特殊穩定語義，例如路徑、最佳選擇或已完成狀態。

必要欄位：

- `action`: `"mark_cell"`
- `target_id`: `str`
- `row`: `int`
- `col`: `int`

選配欄位：

- `color`: `str`

範例：

```json
{"action": "mark_cell", "target_id": "dp", "row": 2, "col": 3, "color": "GREEN"}
```

## 3. Pointer Actions

用於表達索引、游標、邊界、搜尋位置、活動 cell 等移動式焦點。

### `create_pointer`

用途：  
建立一個指標。

必要欄位：

- `action`: `"create_pointer"`
- `id`: `str`
- `label`: `str`
- `target_id`: `str`
- `index`: `int` 或 `[row, col]`
- `position`: `str`，通常為 `"top"` 或 `"bottom"`

範例：

```json
{"action": "create_pointer", "id": "p_i", "label": "i", "target_id": "main", "index": 0, "position": "top"}
```

使用規則：

- pointer 應有明確語義，例如 `i`、`j`、`left`、`right`、`mid`
- 不要建立沒有教學意義的 pointer
- 同一個 pointer 應表示同一個概念，不要中途換角色

### `move_pointer`

用途：  
將既有 pointer 移動到新的位置。

必要欄位：

- `action`: `"move_pointer"`
- `id`: `str`
- `target_id`: `str`
- `index`: `int` 或 `[row, col]`

範例：

```json
{"action": "move_pointer", "id": "p_i", "target_id": "main", "index": 1}
```

使用規則：

- 只移動已建立的 pointer
- 若 pointer 的教學意義已結束，應考慮移除而不是長時間保留在畫面上

### `remove_pointer`

用途：  
移除已不再需要的 pointer。

必要欄位：

- `action`: `"remove_pointer"`
- `id`: `str`

範例：

```json
{"action": "remove_pointer", "id": "p_i"}
```

使用規則：

- 當 pointer 的教學角色完成時應及時移除
- 不要讓無效 pointer 長時間佔據畫面

## 4. Graph Actions

用於 graph traversal、節點探索、frontier 擴張與 visited 狀態展示。

### `create_graph`

用途：  
建立一個新的 graph 視覺物件。

必要欄位：

- `action`: `"create_graph"`
- `id`: `str`
- `nodes`: `list[str]`
- `edges`: `list[list[str]]` 或 `list[tuple[str, str]]`

選配欄位：

- `positions`: `object`，可提供節點到座標的映射；若未提供，renderer 可使用預設布局

範例：

```json
{
  "action": "create_graph",
  "id": "g1",
  "nodes": ["A", "B", "C"],
  "edges": [["A", "B"], ["A", "C"]]
}
```

使用規則：

- 任何 graph 節點操作前，必須先 `create_graph`
- `nodes` 與 `edges` 應反映本次教學任務的初始 graph

### `highlight_node`

用途：  
標示目前焦點節點，例如 current node 或正在檢查的節點。

必要欄位：

- `action`: `"highlight_node"`
- `target_id`: `str`
- `node_id`: `str`

選配欄位：

- `color`: `str`

範例：

```json
{"action": "highlight_node", "target_id": "g1", "node_id": "A", "color": "YELLOW"}
```

### `unhighlight_node`

用途：  
取消節點焦點標示。

必要欄位：

- `action`: `"unhighlight_node"`
- `target_id`: `str`
- `node_id`: `str`

範例：

```json
{"action": "unhighlight_node", "target_id": "g1", "node_id": "A"}
```

### `mark_visited`

用途：  
將節點標記為已訪問或已處理狀態。

必要欄位：

- `action`: `"mark_visited"`
- `target_id`: `str`
- `node_id`: `str`

選配欄位：

- `color`: `str`

範例：

```json
{"action": "mark_visited", "target_id": "g1", "node_id": "A", "color": "GREEN"}
```

### `mark_frontier`

用途：  
將節點標記為 frontier / queue 中待處理的節點。

必要欄位：

- `action`: `"mark_frontier"`
- `target_id`: `str`
- `node_id`: `str`

選配欄位：

- `color`: `str`

範例：

```json
{"action": "mark_frontier", "target_id": "g1", "node_id": "B", "color": "ORANGE"}
```

## Action 使用原則

### 1. trace 應記錄教學上重要的事件

應優先記錄：

- 結構建立
- 焦點轉移
- 關鍵比較
- 值交換
- 值覆寫
- cell 更新
- 指標建立與移動
- 狀態完成或確定
- 區間排除
- graph 節點狀態切換

不應記錄：

- 純視覺修飾
- 對教學沒有影響的微小閃動
- 只屬於 Manim 呈現層的動畫節奏細節

### 2. trace 必須能對齊教學 beat

`teaching_script.md` 中的每個 beat 都應對應到一段 trace 區間或一組 action。  
可以是：

- 一個 beat 對應一個 action
- 一個 beat 對應多個 action

但不應出現以下情況：

- 某個 beat 在 trace 中完全找不到對應事件
- 某段重要 trace 沒有對應的教學目的
- Manim 層自己補上 trace 中不存在的重要演算法事件

### 3. trace 描述的是事件，不是結論

trace 應表達：

- 哪個元素被比較
- 哪個位置被更新
- 哪個 pointer 被移動
- 哪個 cell 被寫入
- 哪個區間被排除
- 哪個 graph node 變成 current / frontier / visited

trace 不應直接偷塞抽象結論，例如：

- 「這一步代表 greedy choice」
- 「這裡形成最優子結構」

這些屬於 `teaching_script.md` 或 `plan.md` 的責任。

## 常見錯誤

### 錯誤 1：把 Manim 細節寫進 trace 思維

錯誤想法：

- 我要讓這一步慢慢 fade in，所以 trace 多加一個假 action

正確做法：

- trace 只記錄事件
- fade、run_time、位置微調屬於 Manim 層

### 錯誤 2：把不重要的每一步都 trace

錯誤想法：

- 每一次 loop iteration 都應該加大量 action

正確做法：

- 只記錄有教學意義的狀態轉移
- 若某個內部變化觀眾不需要知道，就不應強行 trace

### 錯誤 3：schema 不夠用時，改在 Manim 層偷補邏輯

錯誤想法：

- 先讓 Manim 直接猜這一步其實代表什麼

正確做法：

- 先擴充 trace schema
- 再讓 trace script 輸出新的 action
- 最後更新 Manim translation 規則

## 擴充原則

當現有 schema 無法支援某類演算法時，請依以下順序處理：

1. 確認教學需求是否真的需要新的視覺語義
2. 定義新的 action 名稱與欄位
3. 說明該 action 的事件語義，而不是動畫語法
4. 更新 tracer script 的產出邏輯
5. 更新 Manim translation 對該 action 的支援
6. 更新 teaching script 與相關 examples

不要直接在 `generated_algo_scene.py` 裡加特例，而不更新 schema。

## 最小範例

以下是一個簡化的 bubble sort trace：

```json
[
  {"action": "create_array", "id": "main", "values": [3, 1, 4]},
  {"action": "create_pointer", "id": "p_j", "label": "j", "target_id": "main", "index": 0, "position": "top"},
  {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
  {"action": "swap", "target_id": "main", "i": 0, "j": 1},
  {"action": "unhighlight", "target_id": "main", "indices": [0, 1]},
  {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 1},
  {"action": "highlight", "target_id": "main", "indices": [1, 2], "color": "YELLOW"},
  {"action": "unhighlight", "target_id": "main", "indices": [1, 2]},
  {"action": "mark_sorted", "target_id": "main", "indices": [2]},
  {"action": "remove_pointer", "id": "p_j"}
]
```

以下是一個簡化的 binary search trace 區間排除片段：

```json
[
  {"action": "create_array", "id": "main", "values": [1, 3, 5, 7, 9, 11, 13]},
  {"action": "create_pointer", "id": "p_left", "label": "left", "target_id": "main", "index": 0, "position": "bottom"},
  {"action": "create_pointer", "id": "p_right", "label": "right", "target_id": "main", "index": 6, "position": "bottom"},
  {"action": "create_pointer", "id": "p_mid", "label": "mid", "target_id": "main", "index": 3, "position": "top"},
  {"action": "highlight", "target_id": "main", "indices": [3], "color": "YELLOW"},
  {"action": "mark_excluded", "target_id": "main", "indices": [0, 1, 2, 3]},
  {"action": "move_pointer", "id": "p_left", "target_id": "main", "index": 4}
]
```

以下是一個簡化的 BFS graph trace 片段：

```json
[
  {
    "action": "create_graph",
    "id": "g1",
    "nodes": ["A", "B", "C"],
    "edges": [["A", "B"], ["A", "C"]]
  },
  {"action": "highlight_node", "target_id": "g1", "node_id": "A", "color": "YELLOW"},
  {"action": "mark_visited", "target_id": "g1", "node_id": "A", "color": "GREEN"},
  {"action": "mark_frontier", "target_id": "g1", "node_id": "B", "color": "ORANGE"},
  {"action": "mark_frontier", "target_id": "g1", "node_id": "C", "color": "ORANGE"}
]
```

## 與其他產出物的關係

- `plan.md`  
  定義這支動畫想教什麼，以及重要的不變量、beat 結構與視覺重點

- `teaching_script.md`  
  定義每個 beat 要如何講、觀眾要理解什麼

- `generated_trace_script.py`  
  以純 Python 執行演算法並輸出 trace

- `action_trace.json`  
  定義實際發生的演算法事件與狀態轉移

- `generated_algo_scene.py`  
  忠於 trace，並依據教學規劃把事件轉成可讀動畫

trace 不取代教學規劃；它負責的是事件事實層。
