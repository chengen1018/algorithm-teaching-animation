# Render Preflight

本文件定義在獨立 scene review 前必須執行的精簡自檢。

Preflight 不是 review 的替代品。它的作用是避免明顯的 render-layer 缺陷在正式 review 時才第一次被當成視覺除錯。

## 必要輸出

在請求 scene review 前，先撰寫 `render_preflight.md`。

請使用以下精簡格式：

```markdown
# Render Preflight

## Source Evidence
- MP4: `<path>`
- MP4 last-write time: `<timestamp>`
- MP4 size: `<bytes or human-readable size>`
- Evidence frames regenerated after latest render: `PASS` or `FAIL`

## Checks
| Check | Result | Evidence |
| --- | --- | --- |
| Intro has no future-phase helper objects | PASS/FAIL/N/A | `<frame or timestamp>` |
| Required base values and labels are visible | PASS/FAIL/N/A | `<frame or timestamp>` |
| One mismatch/update beat shows focus, references, formula/state, and written result | PASS/FAIL/N/A | `<frame or timestamp>` |
| One match/success beat shows focus, references, formula/state, and written result | PASS/FAIL/N/A | `<frame or timestamp>` |
| Completed structure shows all required final values | PASS/FAIL/N/A | `<frame or timestamp>` |
| Traceback/path/reconstruction beat has readable current state and labels | PASS/FAIL/N/A | `<frame or timestamp>` |
| Final frame contains only the intended final-result presentation | PASS/FAIL/N/A | `<frame or timestamp>` |
| No explanatory text is captured mid-transition or visually corrupted | PASS/FAIL/N/A | `<frame or timestamp>` |
```

每個 evidence 欄位都只能是一個簡短參照，不要寫成段落。

## 證據新鮮度

每次 rerender 都會使先前抽出的 review frames 失效。

在每次 rerender 之後：

- 從最新 MP4 重新產生所有 review frames
- 更新 `render_preflight.md`
- 記錄 MP4 路徑、大小與最後寫入時間
- 不要重用比 MP4 還舊的 frame evidence

在重新產生最新證據與 `render_preflight.md` 之後，再依照下列範圍規則選擇 delta 或 full 的獨立 scene review。

某個 scene/render 的第一次獨立 scene-review 交接一律是 `Full`。

若任何 frame evidence 比 MP4 還舊，scene review 在判斷視覺品質前就必須拒絕交接。

## 首輪正確性檢查

在送審前，scene writer 必須檢查具代表性的穩定影格：

- opening 或 intro 畫面
- 至少一個一般 update 或 mismatch 畫面（若適用）
- 至少一個 match、success 或 acceptance 畫面（若適用）
- completed primary structure 畫面
- traceback、path、reconstruction 或 finalization 畫面（若適用）
- 最終結果畫面

只有當演算法或已核准 script 確實沒有該類 beat 時，才能使用 `N/A`。

## 迴圈控制

只有在局部 `RENDER` 變更且具有效受影響影格證據時，才允許 delta review。

若修復改變了已核准語意、script beat order、delivery tier、已核准契約、全場景結構、全場景版面、render mapping，或使受影響影格證據失效，就必須回到 full review。

若受影響影格範圍擴大或影響不確定，就視為受影響影格證據失效，必須進行完整獨立 scene review。

一份 delta 交接必須包含：

- 先前的 blocking finding ids
- 每個 finding 的變更內容
- 受影響影格的更新後證據參照
- 每個被改動 helper 或 visibility rule 的一項相鄰 phase regression 檢查

若連續兩次失敗都由同一類 Manim visual-state 缺陷造成，必須停止局部修補，改在 `RENDER` 中重寫場景的 phase ownership 或 visibility plan，再重新請求 review。

若重寫之後出現第三次 scene-review 失敗，則應將問題升級為架構層級，而不是繼續 patch-and-review 迴圈。若缺陷由 `RENDER` 或 `SCRIPT` 持有，就送回對應階段。若已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上有缺漏或衝突，則送回 `DESIGN_DEVELOPMENT`；要求設計修復、重新審查與重新核准，再重新產生並重新核准 brief。若已核准設計清楚，但 brief 有錯誤文字或來源標籤，或是不忠實轉換，則送回 `CONTRACT`，修復並重新核准 brief，無需重新設計。
