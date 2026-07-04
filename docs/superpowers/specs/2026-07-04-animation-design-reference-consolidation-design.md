# 階段一子階段二參考文件整併設計

## 目標

將 `DESIGN_DEVELOPMENT` 目前必讀的四份通用參考整併為單一文件，降低主要 Agent 在開始共同設計前需要載入與交叉比對的 Markdown 數量，同時完整保留既有流程、產物格式、教學設計與視覺語言規則。

整併完成後，子階段二只需閱讀：

1. 動態需求產物 `confirmed_requirements.md`
2. 單一通用參考 `references/how-to-design-animation.md`
3. 唯一一份符合演算法類型的專用參考

## 整併範圍

以下四份通用參考整編為 `references/how-to-design-animation.md`：

- `references/animation-design-process.md`
- `references/animation-design-document.md`
- `references/teaching-design.md`
- `references/visual-language.md`

整併完成並更新引用後，刪除上述四份舊文件，避免同一規則存在多個權威來源。

以下內容維持獨立：

- `confirmed_requirements.md`：每次任務產生的動態需求產物，不屬於靜態參考。
- `references/animation-design-array-sorting.md`
- `references/animation-design-graph-traversal.md`
- `references/animation-design-search.md`

演算法專用參考仍採條件式載入；每次只閱讀唯一一份符合類型的文件。沒有相符專用參考時，只使用通用參考，不建立虛構的專用語意。

## 新文件結構

`references/how-to-design-animation.md` 使用以下章節順序：

1. **目的、責任與開始條件**：定義 `DESIGN_DEVELOPMENT` 的擁有者、必要輸入與通用／專用參考的關係。
2. **六個固定 Scene 與文件格式**：保留六幕順序、每幕四個必要欄位、完整 Markdown 範本及場景規則。
3. **共同設計流程**：保留一次處理一個設計決定、何時詢問使用者、三個完整方案、決定後直接更新文件等規則。
4. **教學設計原則**：涵蓋樣本選擇、教學順序、先因後果、保留前一狀態及避免無意義方案。
5. **視覺語言**：涵蓋穩定含義、單一焦點、穩定版面、必要支援結構及文字與動作規則。
6. **完成與審查交接**：保留獨立審查、修正責任、重新審查與使用者最終核准 gate。

相同規則只保留一次。原本散落在不同文件中的重複內容，以語意較完整、限制較明確的版本為準；整併不得放寬現有要求，也不得新增流程關卡或產物欄位。

## 引用更新

更新儲存庫內所有指向四份舊文件的有效引用，使其改指向 `references/how-to-design-animation.md`。至少涵蓋：

- 頂層 `SKILL.md` 中 `DESIGN_DEVELOPMENT` 的必讀清單
- 演算法專用參考中描述通用指引或流程的文字
- agents、其他 references 或設定檔中的直接路徑引用

歷史規格與歷史實作計畫是過往決策紀錄，不回寫其中的舊路徑；驗證時應將 `docs/superpowers/` 排除於失效引用檢查之外。

## 相容性與邊界

- `animation_design.md` 的六幕結構、四個必要欄位與禁止內容維持不變。
- 主要 Agent 與使用者逐項共同設計的互動方式維持不變。
- `animation-design-reviewer` 的責任、`animation_design_review.md = PASS` 與使用者最終核准 gate 維持不變。
- 演算法專用參考只補充類型特有語意，不取代通用流程或文件契約。
- 本次不整併 reviewer checklist、`pre-build-brief.md` 規格或其他階段文件。

## 驗證

實作完成後應確認：

1. `references/how-to-design-animation.md` 存在且包含六個預定章節。
2. 四份舊通用參考已移除。
3. `SKILL.md` 的子階段二必讀清單只包含需求產物、單一通用參考與唯一一份演算法專用參考。
4. 排除歷史 `docs/superpowers/` 後，儲存庫不存在指向四份舊文件的有效引用。
5. 六幕名稱、每幕四個必要欄位、三方案規則、審查與核准 gate 都能在新文件或頂層 skill 中找到。
6. `git diff --check` 通過，且整併沒有意外修改其他階段的行為。
