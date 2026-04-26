# Algorithm Teaching Animation Skill — 完整 Review

## 整體評價

這份 skill 的設計水準**非常高**。它不是一個簡單的 prompt，而是一套完整的教學動畫方法論系統。架構清晰、層次分明、原則一致，顯示出對「AI 如何做教學」這個問題有深入思考。

以下我會從**架構設計**、**Reference 文件品質**、**Examples 品質**、**可能的實際使用問題**四個面向，分別給出具體分析。

---

## 1. 架構設計

### ✅ 做得好的部分

| 面向 | 評價 |
|------|------|
| **五層分離** | `plan → script → trace → Manim` 的分層非常清楚，每一層的責任邊界明確 |
| **單一真相來源** | `action_trace.json` 作為事件事實層，禁止 Manim 層重新推理，這是整個架構最重要的設計決策 |
| **教學優先原則** | 從頭到尾堅持「先想教什麼，再做動畫」，這和大多數人「先寫 Manim 再想教什麼」的直覺完全相反 |
| **回修鏈清晰** | rendering.md 中明確定義了問題應回到哪一層修正，避免在 Manim 層打補丁 |
| **模式系統** | 六種模式的設計覆蓋了常見演算法教學場景，且每種模式有獨立的教學/trace/視覺重點 |

### ⚠️ 值得注意的設計考量

#### 1.1 `tracer` 模組是幽靈依賴

所有 `generated_trace_script.py` 都 `from tracer import AlgorithmTracer`，但 skill 中**沒有定義 `tracer.py` 的實作或介面**。Agent 看到這些 example 時，會遇到一個問題：

> 我要寫 `generated_trace_script.py`，但我不知道 `AlgorithmTracer` 到底提供哪些方法、參數型別、輸出格式是什麼。

`trace-schema.md` 定義了 action vocabulary，但它是用 JSON schema 的角度寫的，沒有對應到 Python API。Agent 必須自己推斷 `tracer.highlight("main", [0, 1], "YELLOW")` 這樣的呼叫方式。

> [!IMPORTANT]
> **建議**：在 references 中新增一份 `tracer-api.md`，或在 `trace-schema.md` 中為每個 action 附上對應的 Python method signature。這樣 agent 就不需要從 examples 逆推 API。

#### 1.2 `generated_algo_scene.py` 內嵌 trace 的設計是否刻意？

四個 example 中，所有 Manim scene 都把整份 `action_trace.json` 整塊複製貼進 `state_trace` list。這代表 Manim scene 是**自包含**的，不需要讀外部 JSON。

這是一個可以辯論的設計選擇：

| 做法 | 優點 | 缺點 |
|------|------|------|
| 內嵌 trace | 單檔可執行、不需要 I/O | trace 修改後必須手動同步 |
| 讀取外部 JSON | trace 與 scene 解耦 | 多了一層檔案依賴 |

目前 skill 中**沒有明確規定該用哪種做法**。如果是刻意設計成內嵌，建議在 SKILL.md 或 rendering.md 中明確說明原因。

#### 1.3 工作流缺少明確的人機互動點

SKILL.md 定義了 1→2→3→4→5 的工作流，但沒有說明：

- Agent 應該在每一步之間等使用者確認嗎？
- 還是持續輸出到最終結果？
- 使用者可以只要求某個 substep 的修正嗎？

> [!TIP]
> **建議**：在 SKILL.md 的工作流程段落加入一句：「除非使用者只要求特定步驟，否則應在每一主要階段完成後確認再繼續」或反之。讓 agent 知道預設行為。

---

## 2. Reference 文件品質

### 逐檔評價

| 檔案 | 評分 | 評語 |
|------|------|------|
| [planning.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/planning.md) | ⭐⭐⭐⭐⭐ | 極好。結構清晰、必填欄位說明完整、常見錯誤實用、最小範例恰當 |
| [teaching-script.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/teaching-script.md) | ⭐⭐⭐⭐⭐ | 極好。beat 欄位定義精準、好壞例子對比鮮明、與 trace 的對齊規則清楚 |
| [trace-schema.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/trace-schema.md) | ⭐⭐⭐⭐ | 很好。五大類 action 定義完整。但缺少 Python API 對應（如上述） |
| [visual-language.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/visual-language.md) | ⭐⭐⭐⭐⭐ | 極好。從原則到檢查清單都有，且與各任務模式的視覺重點有交叉呼應 |
| [rendering.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/rendering.md) | ⭐⭐⭐⭐ | 很好。Preview / Final 分級明確、回修順序是亮點。但未指出具體 Manim 渲染命令 |
| [modes.md](file:///c:/Users/Jason/independent%20study/algorithm-animation-generator/algorithm-teaching-animation%20skill/references/modes.md) | ⭐⭐⭐⭐⭐ | 極好。六種模式的教學/規劃/trace/視覺重點形成完整矩陣，非常實用 |

### Reference 整體亮點

1. **一致的結構**：每份 reference 都有「核心原則 → 詳細說明 → 常見錯誤 → 最小範例 → 與其他文件的關係」，agent 可以預期在哪裡找到什麼資訊。
2. **反面教材**：幾乎每份都有「不好的例子」和「常見錯誤」，這對 LLM 的指導效果極強。
3. **跨文件互參**：每份 reference 結尾都明確說明與其他文件的關係，避免歧義。

### Reference 可改進處

#### 2.1 `trace-schema.md` 中 `unhighlight` 的語義不夠精確

`unhighlight` 的語義是「取消焦點」，但在 bubble sort 的 `generated_algo_scene.py` 中，unhighlight 的實作需要判斷「目前是否已被 mark_sorted」來決定回退顏色：

```python
# bubble sort scene, line 125
target_color = self.COLOR_SORTED if rect.get_fill_color() == self.COLOR_SORTED else self.COLOR_DEFAULT
```

這代表 `unhighlight` 的語義其實是「還原到先前的穩定語義狀態」，但 trace-schema.md 沒有明確定義這個行為。不同 agent 可能對「unhighlight 完該變什麼色」有不同理解。

> [!TIP]
> **建議**：在 trace-schema.md 的 unhighlight 段落補上：「unhighlight 的目標是將元素還原為最近的穩定語義狀態（如 default、sorted、excluded），而非固定還原為預設色。」

#### 2.2 沒有 Manim coding guideline

References 對教學設計的規定極其完整，但對 **Manim code 本身的寫法**沒有指引：

- 應不應該使用 `Scene` 以外的 base class？
- 配色常數應該怎麼命名？（目前 bubble sort 用 `COLOR_SORTED`，binary search 用 `COLOR_FOUND`）
- `run_time` 的建議範圍？
- 是否支援 ManimCE vs ManimGL？

> [!TIP]
> **建議**：新增一份 `references/manim-guidelines.md`，定義 Manim scene 的寫法規範。這能讓不同演算法的 generated scene 保持一致的程式碼風格。

---

## 3. Examples 品質

### 3.1 四個 Example 的覆蓋度

| Example | 模式 | 資料結構 | Trace 複雜度 | 教 |
|---------|------|----------|------------|-----|
| Bubble Sort | algorithm walkthrough | Array | 完整多輪 | ✅ 最完整 |
| Binary Search | pointer and control-flow | Array + Pointer | 2 輪搜尋 | ✅ 很好 |
| BFS | graph traversal | Graph | 完整遍歷 | ✅ 適當 |
| 0/1 Knapsack DP | dynamic programming | Matrix | 極簡 demo | ⚠️ 過於簡化 |

> [!WARNING]
> **DP example 太過簡化**：3×3 矩陣、只填 3 個 cell、沒有真正的 knapsack 邏輯（weight/value 選擇）。`generated_trace_script.py` 是硬編碼的 demo，不是真正執行演算法。如果 agent 拿這個作為學習範例，可能會產出同樣硬編碼的 trace script，而非真正的 DP 實作。

#### DP Example 具體問題

1. **Trace script 不是真正的演算法**：`knapsack_demo_traced()` 直接手寫事件序列，不像其他三個 example 是真正執行演算法並記錄 trace
2. **沒有 items / weights / values**：一個 knapsack 教學連 item 清單都沒有
3. **只示範了 3 個 cell**：真實 DP 教學需要至少展示完整一行或一列的填表過程
4. **依賴來源不夠多元**：每次都只高亮一個依賴，但 0/1 knapsack 的特色是要在「包含當前 item」和「不包含」之間選擇，需要同時展示兩個依賴來源

### 3.2 Example 的內部一致性 — Bubble Sort（最完整的示範）

以 bubble sort 為例做詳細檢查：

#### ✅ 層間對齊良好

- `plan.md` 的 beat outline 6 個高層 beat → `teaching_script.md` 展開為 7 個 beat（加了最後的排序完成）→ trace 與 beat 的對應清楚
- `teaching_script.md` 每個 beat 都有 trace mapping，且 mapping 的 action 範圍可以回溯到 `action_trace.json`
- `generated_algo_scene.py` 忠實重現 trace，沒有自行發明邏輯

#### ⚠️ Trace 的冗餘 action

`action_trace.json` 第 3 行：
```json
{"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 0}
```
在第 2 行剛 `create_pointer` 在 index 0 之後，立刻又 `move_pointer` 到 index 0。這是因為 trace script 的迴圈結構導致的冗餘——第一輪 `j=0` 時 move_pointer 到 0 是多餘的。

這不是嚴重問題，但對「不要過度追蹤沒有教學價值的細節」這條原則來說是個小瑕疵。

#### ⚠️ Unhighlight 後的顏色還原邏輯

在 `generated_algo_scene.py` L120-127：

```python
elif action == "unhighlight":
    tid = step["target_id"]
    animations = []
    for i in step["indices"]:
        rect = arrays[tid][i][0]
        target_color = self.COLOR_SORTED if rect.get_fill_color() == self.COLOR_SORTED else self.COLOR_DEFAULT
        animations.append(rect.animate.set_fill(target_color))
```

這裡用 `get_fill_color() == self.COLOR_SORTED` 來判斷是否已排序。但 Manim 的 `get_fill_color()` 回傳的是 `ManimColor` 物件，直接用 `==` 比較可能在某些 Manim 版本不穩定。更重要的是，這意味著 Manim 層在**通過顏色反推語義**，而不是維護獨立的狀態表。

### 3.3 Example 的內部一致性 — Binary Search

#### ✅ 良好

- 正確使用了 `mark_excluded` 而不是濫用 `unhighlight` 來表示排除區間
- pointer 的 remove / re-create 模式清楚表達了 mid 在每輪是重新計算的

#### ⚠️ Trace 中缺少 `unhighlight`

第一輪 highlight mid (index 3) 後，直接 mark_excluded 然後 move_pointer，但沒有 unhighlight index 3。因為 mark_excluded 已經把 index 3 變灰了。但從嚴格的 highlight/unhighlight 配對來看，這裡的 highlight 在語義上沒有被關閉。

### 3.4 Example 的內部一致性 — BFS

#### ⚠️ `mark_frontier` → `mark_visited` 的語義過渡太快

在 trace 中，每個新發現的鄰居會快速經歷：
```
mark_frontier → mark_visited → unhighlight_node
```

這意味著 frontier 狀態稍縱即逝，觀眾可能看不到橘色存在的瞬間。如果要教「frontier 是什麼」，應該讓 frontier 狀態停留更久，等整個鄰居展開完再集體 mark_visited。

---

## 4. 實際使用時的潛在問題

### 4.1 Token 開銷

SKILL.md（223 行）+ 6 份 references（合計 ~2700 行）= 非常大的 context。如果 agent 在每次呼叫都載入全部 reference，token 成本會很高。

> [!TIP]
> **建議**：在 SKILL.md 中標示哪些 reference 在哪個步驟才需要載入。例如：
> - Step 1 PLAN 時載入 `planning.md` + `modes.md`
> - Step 2 SCRIPT 時載入 `teaching-script.md`
> - Step 3 TRACE 時載入 `trace-schema.md`
> - Step 4 MANIM 時載入 `visual-language.md` + `rendering.md`

### 4.2 「不該做的事」可以更強化

SKILL.md 的「不應做的事」只有 4 條，但 references 中散落了更多禁忌。可以考慮在 SKILL.md 中把最容易犯的錯誤集中成更完整的 anti-pattern list。

### 4.3 缺少失敗案例作為 reference

References 中有「常見錯誤」的文字描述，但如果能提供一份**刻意做錯的 example**（例如一個 Manim 層自行推理演算法的反面教材），agent 會更容易理解「不要這樣做」的具體意思。

### 4.4 `comparison or intuition explainer` 模式缺少 Example

六種模式中有四種有對應的 example：

| 模式 | 有 Example？ |
|------|------------|
| algorithm walkthrough | ✅ Bubble Sort |
| pointer and control-flow | ✅ Binary Search |
| graph traversal | ✅ BFS |
| dynamic programming | ✅ DP (但過於簡化) |
| data structure state transition | ❌ |
| comparison or intuition | ❌ |

建議至少補上 `data structure state transition` 的 example（例如 heap insert），因為它的 trace 模式與 array walkthrough 有明顯差異。

---

## 5. 總結與優先改進建議

### 整體成績：🟢 非常好

這份 skill 已經是一個有完整方法論支撐的教學系統設計。以一份寫給 AI agent 的 skill 來說，它的結構化程度、自洽性和反面教材的豐富度都遠超多數同類作品。

### 建議改進優先順序

| 優先級 | 改進項目 | 原因 |
|--------|---------|------|
| 🔴 高 | 新增 `tracer-api.md` 或在 trace-schema 中補上 Python method signatures | Agent 目前無法得知 tracer API，只能從 example 逆推 |
| 🔴 高 | 重寫 DP example 為真正的 knapsack 演算法 | 目前是硬編碼 demo，違反 skill 自己的原則 |
| 🟡 中 | 補充 `unhighlight` 的「還原到穩定語義狀態」語義定義 | 不同 agent 會有不同理解 |
| 🟡 中 | 新增 `manim-guidelines.md` 統一 scene 寫法規範 | 四個 example 的命名風格、配色常數名稱不統一 |
| 🟡 中 | 在 SKILL.md 加入 reference 的按需載入建議 | 降低 token 成本 |
| 🟢 低 | 補 `data structure state transition` example | 增加模式覆蓋度 |
| 🟢 低 | 說明 `generated_algo_scene.py` 內嵌 vs 讀取 JSON 的設計決策 | 消除歧義 |
| 🟢 低 | BFS trace 中讓 frontier 狀態停留更久 | 教學上 frontier 概念很重要 |
