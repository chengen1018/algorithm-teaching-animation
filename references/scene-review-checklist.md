# Scene Review 檢查表

本文件定義 `algorithm-teaching-animation-v4` 的 `RENDER` gate review。

reviewer 的工作是檢查 scene 忠實性與觀眾可理解性。reviewer 不負責發明或修補語意。

## 必要輸出

回傳 `scene_review_result.md`，內容需包含：

- `PASS` 或 `FAIL`
- 審查結果必須由獨立 reviewer 撰寫
- reviewer 負責 `RENDER` gate
- 分類好的阻塞性 findings
- evidence references
- 修復方向：`RENDER`

使用以下 finding 類別：

- `styling`
- `layout`
- `semantic ambiguity`
- `source mismatch`

## 審查輸入

審查時應對照：

- `confirmed_requirements.md`
- 已核准的 `animation_design.md`
- 已審查的 `teaching_script.md`
- `generated_algo_scene.py`
- `render_preflight.md`
- rendered output 或 render evidence

已通過 gate 的上游產物是可執行契約。審查 `render_preflight.md` 的 `Render Assumptions`：每一項非平凡解讀都必須最小、保守、可追溯至其負責的來源範圍，且不得新增演算法步驟或教學目標。

在判斷視覺品質前，先確認 `render_preflight.md` 的 Source Evidence 指向最新 MP4，並由 reviewer 為該 MP4 準備最新 render evidence。若 preflight、MP4 或 reviewer evidence 缺失、過期、不完整或互不一致，這屬於被阻塞或無效的 review handoff，以及應送回 `RENDER` 的 evidence / process defect，而不是 `layout` finding。未準備符合最新 MP4 的 preflight 與 reviewer evidence 前，不得繼續審查或回傳 `PASS`。真正的視覺版面問題則分類為 `layout`。

## 審查問題

### Source Fidelity

- scene 是否實作了已凍結語意，而不是新的詮釋？
- 每個主要 beat 是否符合已核准 script 中的教學目的？
- 當已核准設計說 support structures 重要時，它們是否有出現？

### Visual Clarity

- 當前焦點是否明顯？
- pointers、boundaries 與 temporary structures 是否可讀？
- resolved regions 是否保持可理解，且不搶焦？
- active prefix、header、pointer 或 state labels 在 highlight 下是否仍可讀？
- explanatory text panels 是否以穩定畫面審查，而不是用不可讀的 transition frames？

### Layout Safety

- labels 與結構是否沒有碰撞？
- 重要內容是否都在安全邊界內？
- 若 overlays 啟用，它們是否避開教學關鍵區域？
- intro 是否避免出現未來 phase 的 helper objects？
- 最終畫面是否只包含預期的 final-result presentation？

### Semantic Safety

- 是否有任何 styling 選擇迫使觀眾推論需求或設計從未定義的規則？
- 是否有任何實作方便性改變了觀眾學到的內容？
- 是否有任何 assumptions 不是最小、保守或可追溯的解讀？

## 修復路由

所有 findings 一律回到 `RENDER`。包括 styling、spacing、layout execution、implementation fidelity、evidence／process defect，以及 assumptions 過度延伸、不可追溯或未能忠實實作上游契約的問題。修復時必須保留已確認語意；可合理解讀的細節改以更小、更保守且有明確來源依據的 assumptions 實作，不得重新啟動上游流程。

## Source Mismatch 規則

當 scene 與已確認需求、已核准設計或已審查 script 衝突時，使用 `source mismatch`。

不匹配一律由 `RENDER` 修正：先依需求、設計、script 與旁白產物各自的負責範圍選擇最小、保守解讀，再更新程式、畫面與 `Render Assumptions`。不得因來源存在可合理解讀的細節、歧義或衝突而路由上游。

## Delta Review

只有在局部 `RENDER` 變更且具有效受影響影格證據時，才允許 delta review。

某個 scene/render 的第一次獨立 scene-review 交接一律是 `Full`。

delta review 只檢查：

- 先前的 blocking findings
- 已變更影格及其直接相鄰 phases
- 修復造成的新視覺回歸
- 證據新鮮度

若修復改變了已核准語意、script beat order、全場景結構、全場景版面、render mapping，或使受影響影格證據失效，就必須回到 full review。

若受影響影格範圍擴大或影響不確定，就視為受影響影格證據失效，必須使用完整獨立 scene review。

若連續兩次失敗屬於同一類 Manim visual-state 問題，必須要求 scene writer 在再次送審前重寫 phase ownership 或 visibility planning。若在重寫後第三次仍失敗，則在 `RENDER` 內升級為架構層級修正，而不是繼續局部 patch 迴圈。

## PASS 標準

只有在以下條件成立時才能通過：

- scene 忠實於已確認需求、已核准設計與已審查 script
- scene 在視覺上可讀
- 版面安全
- `render_preflight.md` 已存在，且其 Source Evidence 指向最新 MP4
- 每個非平凡 Render Assumption 都最小、保守且可追溯
- reviewer 看不到任何仍未解決的語意問題
- `scene_review_result.md` 由獨立 reviewer 撰寫，而非 render executor
- `scene_review_result.md` 以明確 review artifact 存在；隱含通過、豁免或未記錄的替代品都不算

## 常見失敗

- 因 scene 可以執行就通過，即使它發明了語意。
- 把 assumptions 過度延伸、不可追溯或新增教學內容的問題誤標成 styling。
- 回傳 `FAIL` 卻沒有證據或沒有指出修復層級。
- 把移除 support structure 當成無害清理，明明它改變了課程。
- rerender 後仍拿過期影格來審查。
- 明明只需要 delta review，卻重做 full review。
