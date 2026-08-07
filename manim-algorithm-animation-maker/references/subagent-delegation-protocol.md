# Subagent Delegation Protocol

本文件定義協調者如何把工作委派給 subagent。不得只用角色名稱要求 subagent 自行推測工作。

## 派遣資料

每次委派前，協調者必須準備：

- `project root`：本次動畫產物所在工作目錄的絕對路徑。
- subagent 的角色規格、必要參考文件、腳本、專案輸入與預期輸出的絕對路徑。

傳給 subagent 的角色規格、必要參考文件、腳本、專案輸入與輸出一律使用絕對路徑。

若 subagent 無法讀取派遣訊息提供的角色規格路徑，協調者必須先完整讀取角色規格，將規格全文放進派遣訊息；不得自行摘要、重寫或補造角色規則。

## 角色對應

| 工作 | task name | 角色規格 |
| --- | --- | --- |
| 動畫設計審查 | `animation_design_reviewer` | `references/subagent-animation-design-reviewer.md` |
| 教學腳本撰寫 | `script_writer` | `references/subagent-script-writer.md` |
| 教學腳本審查 | `script_reviewer` | `references/subagent-script-reviewer.md` |
| 旁白產生 | `voiceover_generator` | `references/subagent-voiceover-generator.md` |
| 場景程式碼與渲染 | `scene_writer` | `references/subagent-scene-writer.md` |
| 場景程式碼審查 | `scene_reviewer` | `references/subagent-scene-reviewer.md` |
| 渲染前 Scene 版面驗證 | `scene_layout_validator` | `references/subagent-scene-layout-validator.md` |

## 派遣訊息必要欄位

每次派遣 subagent 時，訊息必須明確包含：

1. **本次唯一角色與工作階段。**
   用途：界定 subagent 這次負責的身分與流程位置，避免同一個 subagent 同時承擔 writer、reviewer 或其他階段的工作，也避免提前處理尚未指派的內容。
2. **角色規格的絕對路徑，並要求開始任何動作前完整閱讀。**
   用途：讓 subagent 能直接找到這次工作的完整規則、Preflight、禁止事項與完成條件，不必根據角色名稱自行猜測。
3. **project root 的絕對路徑。**
   用途：指定本次動畫專案唯一的工作目錄，讓 subagent 知道專案輸入應從哪裡讀取、產物應寫到哪裡，避免操作到其他專案或 skill 資料夾。
4. **每一個必要輸入與 skill reference 的絕對路徑。**
   用途：明確指定這次工作的權威來源及執行指南，避免 subagent 因找不到工作指南而自行判斷並完成工作
5. **完成後明確回報 `DONE` 或 `BLOCKED`。**
   用途：提供協調者一致且可判讀的工作狀態。`DONE` 表示可以開始檢查必要產物與關卡，`BLOCKED` 表示必須先處理阻塞；狀態回報本身不等於產物已通過驗證。

使用下列訊息骨架；不得省略欄位：

```text
你負責本次 <ROLE / STAGE> 工作。

角色規格：
<absolute-role-spec-path>

工作目錄：
<absolute-project-root>

開始任何動作前：
1. 完整閱讀角色規格。
2. 確認並完整閱讀以下必要輸入與參考：
   - <absolute-path>
3. 執行角色規格中的 Preflight。

不要執行任何未指派的後續階段。

如果必要輸入缺失、無法讀取、互相矛盾：
- 不得猜測。
- 不得建立看似完整的替代內容。
- 回報 BLOCKED，列出檔案、證據位置與需要協調者處理的事項。

完成後依角色規格回報 DONE 或 BLOCKED。
```

## 協調者驗證

subagent 回報後，協調者應確認工作可安全交接：

1. 確認 subagent 明確回報 `DONE`；若回報 `BLOCKED`，停止目前階段並處理其說明的問題。
2. 確認所有必要輸出存在。
3. 確認輸出符合目前關卡的必要內容；審查角色的 `PASS` 或 `FAIL` 以實際審查檔內容為準，不以聊天摘要代替。
4. 只有確認可安全交接後才能繼續下個步驟。
5. 協調者不得自行補寫角色遺漏的專業內容；應把具體缺口退回原 subagent 修正，或依流程退回上游。

Writer 與 reviewer 必須是不同的 subagent。Reviewer 不得審查自己曾撰寫、修改或共同撰寫的產物。
