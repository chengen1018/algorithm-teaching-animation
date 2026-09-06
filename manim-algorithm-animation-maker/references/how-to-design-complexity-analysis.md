# Complexity Analysis Design Reference

## Purpose and Position in the Workflow

本文件是 `DESIGN_DEVELOPMENT` 中 complexity 專有判斷的 single source of truth。在 Scene 1–3 已完成、Scene 4/5 尚未設計時使用本文件。

本流程先建立可審查的分析，再由使用者核准教學範圍，最後設計 Scene 4 的可見推導。`Complexity Analysis Proposal` 是供使用者選擇範圍的暫時提案；核准並持久化的 `Complexity Scope` 才是 Scene 4、Scene 5 與下游階段承接的契約。

## Required Inputs

- `confirmed_requirements.md`
- 本次動畫實際採用的 algorithm variant；使用者提供的 code 或 pseudocode 取自 `confirmed_requirements.md` 內保存的內容，否則使用標準演算法定義或可靠參考來源
- implementation 或 representation assumptions 與 operation-cost assumptions
- Scene 3 已建立的 sample operation 與可沿用的視覺語意

## Required Outputs

- 可審查的 `Analysis Basis`
- 完整的 `Complexity Analysis Proposal`
- 使用者對 time cases 與 space treatment 的明確決定
- `animation_design.md` 中位於 Scene 3 與 Scene 4 之間的 complete fixed `Complexity Scope` block
- 完整涵蓋已核准 scope 的 Scene 4 `Visual Derivation` 設計

## Workflow at a Glance

依序完成以下步驟；每一步的 Gate 通過後，才能進入下一步：

1. 建立 `Analysis Basis`。
2. 選擇 primary、optional time cases，並決定建議的 space treatment。
3. 建立固定格式的 `Complexity Analysis Proposal`。
4. 取得使用者核准，並將核准結果持久化為完整的 `Complexity Scope`。
5. 依已核准 scope 設計 Scene 4 的 `Visual Derivation`。

Step 4 的 Gate 通過前，工作保持在 `DESIGN_DEVELOPMENT`，不設計 Scene 4/5。

## Step 1 — Build Analysis Basis

### Required analysis fields

先記錄本次動畫實際採用的 algorithm variant 與 tie-breaking policy、input variables、implementation 或 representation assumptions、candidate cases、counted operation、derivation，以及能定位依據的 source locator。

Source 可以是 `confirmed_requirements.md` 內保存的使用者 code／pseudocode、標準演算法定義或可靠參考來源。使用者來源的 locator 指向該 Markdown 的對應段落；locator 用來佐證推導，推導本身仍要寫出工作量如何形成 expression。

### Unit and representation rules

所有 exact counted-operation bounds 與 input variables 使用同一 representation 與 unit。當一個 logical item 在 implementation representation 中展開成常數倍 records，visible claim 使用 `O(variable)`，或先寫出常數因子（例如 `≤ cE`）再化簡；`≤ variable` 只在 Analysis Basis 已證明同單位的一對一上界時使用。

### Visible relation rules

每個 counted-work formula 依已證明的精確度選擇 visible relation：

- `=` only when the Analysis Basis proves the count is exact for the defined inputs and conditions。
- `≤` for a finite upper bound when the exact count has not been proved。
- `Θ(...)` for a proved tight asymptotic bound。
- `O(...)` for an asymptotic upper bound that need not be tight。

A loose upper bound must never use `=`；先顯示適用的 `≤`、`Θ(...)` 或 `O(...)`，再推導 case label 與最終 complexity。

### Step 1 Gate

每個準備推薦的 case 都能由 algorithm variant、assumptions、counted operation 與 derivation 支撐。所有準備進入提案的 claims 都有可審查的推導與可定位來源。

## Step 2 — Select Scope Candidates

### Representative Case Selection

至少選擇一個 primary time case，代表該演算法最重要的保證、特色或實務使用方式。Contrast case 只在差異能解釋重要特性或取捨時加入；為每個 contrast case 寫出額外教學價值。保持 worst、average、expected 與 amortized 各自的分析模型與含義，case 名稱由實際保證決定。

Time-case selection 完成條件：至少有一個有依據的 primary time case；每個 optional case 都有獨立的教學理由與 include/omit 建議。

### Space Complexity Decision

當 auxiliary structure、recursion、representation 或 time-space tradeoff 影響理解時，選擇 visual derivation，並使用可見物件推導它如何隨 input size 成長。簡單且非核心的 `O(1)` 可以選擇 one-line summary。空間使用對教學不重要時，可以選擇 omit。

Space-treatment selection 完成條件：選擇 omit、one-line summary 或 visual derivation，並記錄此選擇如何符合演算法的 auxiliary structure、recursion、representation 或 time-space tradeoff。

### Step 2 Gate

- 至少有一個有依據的 primary time case。
- 每個 optional case 都有獨立教學理由與 include/omit 建議。
- Space treatment 已選擇 omit、one-line summary 或 visual derivation，且有具體理由。

## Step 3 — Create Complexity Analysis Proposal

使用下列固定結構向使用者提出建議。Optional additional analysis 可依實際需要有零項或多項，但下游不自行增刪欄位或發明另一種 proposal shape。

### Analysis Basis
- Algorithm variant: implementation and tie-breaking policy used by this animation
- Input variables: symbols and what each symbol measures
- Implementation assumptions: representation and operation-cost assumptions
- Counted operation: the work unit used by the derivation
- Derivation basis: why the work count yields each proposed expression
- Analysis source: source type and precise locator for the algorithm variant and derivation evidence

### Recommended primary analysis
- Case: the representative guarantee being recommended
- Complexity: the derived asymptotic expression
- Why representative: teaching or guarantee value
- Visual derivation: the visible sequence used in Scene 4

### Optional additional analysis

零項時仍輸出這個 section，並使用：

- Case: None — zero optional time cases
- Complexity: N/A
- Teaching value: N/A
- Recommendation: omit

有一項或多項時，每項使用：

- Case: an additional case only when it adds teaching value
- Complexity: its derived asymptotic expression
- Teaching value: the distinction it explains
- Recommendation: include or omit

### Space complexity
- Include or summarize: omit, one-line summary, or visual derivation
- Reason: why this treatment matches the algorithm

### Step 3 Gate

Proposal 的固定 sections 與欄位全部存在。每個 proposed claim 都能回溯到 Step 1 的 `Analysis Basis`；每個 optional case 與 space treatment 都包含 Step 2 建立的理由。

## Step 4 — Obtain Approval and Persist Complexity Scope

請使用者明確接受、加入或移除提案中的 time cases，並選擇 space treatment。若使用者不採用推薦的 primary case，請使用者選定一個 replacement time case。只有使用者明確核准的項目會進入 `Complexity Scope`；optional case 保持在 scope 外，直到使用者明確加入。

### Persisted Complexity Scope

核准後，把下列完整 block 寫入 `animation_design.md` 的 Scene 3 與 Scene 4 之間。本文件定義完整 `Complexity Scope` block；`how-to-design-animation.md` 定義它在五幕 `animation_design.md` 中的位置與其餘 topology。

- Analysis basis: <algorithm variant, input variables, implementation or representation assumptions, counted operation, and derivation basis>
- Analysis source: <source type and precise source locator for the algorithm variant and derivation evidence>
- Approved primary time case: <case and complexity>
- Approved contrast time cases: <None — zero approved contrast time cases, or every approved case and complexity>
- Approved space treatment: <omit, one-line summary, or visual derivation>
- Approval evidence: <the user's explicit decision>

Analysis basis 與 Analysis source 是不同欄位。Approved contrasts 為零時仍明確記錄 `None — zero approved contrast time cases`。六個欄位都必須有值。

先持久化 complete fixed `Complexity Scope` block before any Scene 4/5 design。Proposal 本身不是下游契約；只有此 block 中的核准項目會進入 Scene 4 與 Scene 5。

### Step 4 Gate

至少一個 primary time case 或使用者選定的 replacement time case 已獲明確核准，space treatment 也有明確決定，且 approval evidence 足以讓 reviewer 對照使用者決定。完整的固定 scope block 已持久化。未符合此條件時保持在 `DESIGN_DEVELOPMENT`。

## Step 5 — Design Visual Derivation

### Time-case derivation

每個已核准的 time case 都依序設計為可見鏈條：input size → counted operation → repetition、levels、phases 或 sum → expression → labeled complexity。

Scene 3 的 sample operation 是 Scene 4 的可見入口；Scene 4 將它一般化成輸入規模下的 work count。單次 sample run 只提供具體語意，完整鏈條才支撐 asymptotic claim。

依本文件後段的 `Pattern Catalog` 選擇符合 work structure 的可組合模式。每個模式都必須保留能形成 expression 的畫面證據。

### Multivariate simplification

Multivariate asymptotic simplification 依二選一完成：保留 full expression；或在 visible derivation 明確寫出並證成使某 term dominated 的 variable relationship/assumption，再顯示 simplified expression。若 standard bound 可由不同的 counted-operation unit 或 input-variable definition 直接得到，先採用並說明該 unit/definition；缺少已證成 relationship 或該 unit/definition 時，visible derivation 保留 full expression。

### Approved space treatment

- omit：Scene 4 不加入 space claim。
- one-line summary：Scene 4 使用一句話標示已核准的簡短 space claim。
- visual derivation：使用可見 slots、levels、stored states 或其他已核准物件，推導 space 如何隨 input size 成長。

### Step 5 Gate

每個已核准的 time case 都明確包含 input variables、工作單位、重複結構、組成的 expression，以及正確的 case label，使觀眾能從畫面指出完整推導鏈。Scene 4 的 space depth 正好覆蓋已核准的 space treatment。

## Failure Routing

- Unsupported claim：留在 `DESIGN_DEVELOPMENT`，補足或修正 Analysis Basis 後再提案。
- Algorithm variant 或 source 缺失：若使用者提供 code／pseudocode，先將完整內容保存至 `confirmed_requirements.md`；否則取得可定位的標準定義或可靠來源，再完成推導。
- 新資訊改變已核准 scope：更新 proposal 並重新取得使用者核准，之後才更新 Scene 4 與 Scene 5。
- 修正不改變已核准的 cases 或 space treatment：保留原 approval evidence。

完成條件：Scene 4 的每個 claim 都由目前 Analysis Basis 支撐，且內容與最新的使用者核准範圍完全一致。

## Reference — Pattern Catalog

依 work structure 選擇可組合的模式；每個模式都保留能形成 expression 的畫面證據。

| Pattern | 適用結構 | 畫面證據與 expression |
| --- | --- | --- |
| Repeated or nested scans | 同一集合被一次或多次掃描 | 保留 scan 範圍與 pass 計數，形成 elements per pass × passes |
| Shrinking candidate space | 候選範圍按固定比例或規則縮小 | 並列 successive sizes，從縮減次數形成 levels |
| Recursion levels | 工作分散到遞迴樹各層 | 顯示每層節點數與單節點成本，再彙總 level cost |
| Phase count × phase cost | 演算法分成可數 phases | 分別標示 phase 數量與每 phase 工作量，再相乘 |
| State or table count | 每個 state、cell 或 transition 被處理 | 以維度建立 state 數量，再乘上每 state 成本 |
| Unequal sums | 各步工作量不同 | 保留每步 term，顯示 series 或 bound 如何化簡 |
| Output-sensitive work | 工作量同時取決於輸入與輸出大小 | 同時保留 input 與 output variables，讓 expression 含有兩者 |
| Expected or amortized aggregation | 成本需跨機率分布或操作序列聚合 | 顯示 expectation 的加權項，或 sequence total ÷ operation count |
| Geometric growth or periodic rebuilding | 容量或 rebuild threshold 按固定倍數成長 | 分開顯示 operation count 與每次 triggering threshold，再以已證明的關係 bound 幾何和 |
| Auxiliary storage | 額外結構、recursion stack 或 representation 佔用空間 | 將可見 slots、levels 或 stored states 對應到 space expression |

### Geometric growth or periodic rebuilding

Geometric growth or periodic rebuilding 必須區分 operation count `n` 與 triggering capacity or rebuild threshold `m`。先用 `m` 寫出每次 rebuild 的工作量，並 prove a relation between `m` and `n` before substitution。After you prove every triggering `m < n` for the defined sequence，when thresholds double and each rebuild moves at most `m` items，for doubling across `n ≥ 1` operations，安全的 visible bound 是 total copied or moved items is `< 2n`；a tighter bound requires a proof under the exact variable definitions。
