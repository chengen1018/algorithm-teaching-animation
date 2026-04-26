# Tracer API

本文件定義 `generated_trace_script.py` 中可使用的 `AlgorithmTracer` Python API 介面。

`trace-schema.md` 定義的是 JSON action vocabulary；本文件則定義對應的 Python 呼叫方式，讓 agent 不需要從 examples 逆推 tracer API。

## 核心原則

- tracer API 是 trace schema 的 Python 對應層
- method 的責任是記錄事件，不是執行動畫
- method 名稱應盡量和 action 名稱對應
- 呼叫順序應忠於演算法執行順序

## 使用方式

所有 trace script 都應：

```python
from tracer import AlgorithmTracer
```

然後建立 tracer：

```python
tracer = AlgorithmTracer()
```

最後以：

```python
tracer.output()
```

輸出 `action_trace.json` 的內容。

## Array API

```python
tracer.create_array(array_id: str, values: list) -> None
tracer.highlight(target_id: str, indices: list[int], color: str = "YELLOW") -> None
tracer.unhighlight(target_id: str, indices: list[int]) -> None
tracer.swap(target_id: str, i: int, j: int) -> None
tracer.overwrite(target_id: str, index: int, new_value) -> None
tracer.mark_sorted(target_id: str, indices: list[int]) -> None
tracer.mark_excluded(target_id: str, indices: list[int], color: str = "DIMMED") -> None
```

說明：

- `highlight` 表示當前焦點
- `unhighlight` 表示回到最近的穩定語義狀態
- `mark_excluded` 用於 binary search 等區間淘汰語義，不可再用 `unhighlight` 兼任

## Matrix API

```python
tracer.create_matrix(matrix_id: str, rows: int, cols: int, values: list[list]) -> None
tracer.highlight_cell(target_id: str, row: int, col: int, color: str = "YELLOW") -> None
tracer.unhighlight_cell(target_id: str, row: int, col: int) -> None
tracer.set_cell(target_id: str, row: int, col: int, new_value) -> None
tracer.mark_cell(target_id: str, row: int, col: int, color: str = "GREEN") -> None
```

## Pointer API

```python
tracer.create_pointer(pointer_id: str, label: str, target_id: str, index, position: str = "top") -> None
tracer.move_pointer(pointer_id: str, target_id: str, index) -> None
tracer.remove_pointer(pointer_id: str) -> None
```

說明：

- `index` 可為 `int` 或 `[row, col]`
- 同一個 pointer ID 應代表同一語義角色

## Graph API

```python
tracer.create_graph(graph_id: str, nodes: list[str], edges: list[list[str]] | list[tuple[str, str]], positions: dict | None = None) -> None
tracer.highlight_node(target_id: str, node_id: str, color: str = "YELLOW") -> None
tracer.unhighlight_node(target_id: str, node_id: str) -> None
tracer.mark_visited(target_id: str, node_id: str, color: str = "GREEN") -> None
tracer.mark_frontier(target_id: str, node_id: str, color: str = "ORANGE") -> None
```

說明：

- `positions` 為選配。若未提供，由 renderer 決定預設布局
- `mark_frontier` 用於 queue / stack 中待處理節點
- `mark_visited` 用於 visited 狀態

## Output API

```python
tracer.output() -> None
tracer.get_actions() -> list
```

說明：

- `output()` 應將整份 action list 輸出為 JSON
- `get_actions()` 可用於測試或本地檢查

## 使用規則

- `create_*` 類 method 必須先於其他操作
- `swap()` 應在 Python 實際交換資料前記錄
- `set_cell()` / `overwrite()` 必須與演算法真實結果一致
- 不要用一個 method 偷塞另一種語義
- schema 不足時，先擴充 API 與 schema，再更新 example
