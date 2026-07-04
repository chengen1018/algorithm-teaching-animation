# voiceover-manifest

## 角色

根據已確認需求、已核准設計與已審查 script 規劃並產出 narration 套件。

## 必要輸出

- 一份以 beats 為鍵的 `voiceover.md` 規劃。
- 一份與相同 beat 結構對齊的 `narration_manifest.json`。
- 與 `voiceover.md`、`narration_manifest.json` 對齊、可供觀眾使用的音訊資產。
- narration 工作所需的語言與 pacing notes。
- 當上游未修復前無法繼續 narration 規劃時，提供 blocker note。

## 規則

- 開始前閱讀 `confirmed_requirements.md`、已核准的 `animation_design.md`、`teaching_script.md` 與 `script_review_result.md`。
- 讓 `voiceover.md` 與 `narration_manifest.json` 對齊到已審查 script 的 beat 結構、已核准設計與已確認需求。
- 口說語言必須與 `confirmed_requirements.md` 一致。
- 保持 optional overlays 為 opt-in。narration 規劃不得藉由暗示額外加入 overlay 需求。
- 只記錄支援 render 與 QA 所需的 timing 與 pacing 假設，不得藉此重寫 script 結構。

## 失敗條件

- 引入已確認需求、已核准設計或 script 中不存在的語意。
- 未經核准就更改配音語言或畫面附加資訊預期。
- 沒有可供觀眾使用的音訊資產。
- 寫出的時序預期與已核准 beat 結構相矛盾。
- 使用 narration 規劃來掩蓋需求、設計或 script 的缺陷。

## 回退規則

- 若問題是在相同已核准 script 下的措辭、節奏或 manifest 結構，則在 `VOICEOVER` 內修復。
- 若問題來自 script 結構或 beat 組織，則退回 `SCRIPT`。
- 若配音語言等使用者需求記錄不準確，則退回 `COLLECT_REQUIREMENTS` 修正後重新送入設計流程。
- 若已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍或使用者選定設計上存在缺漏或衝突，則退回 `DESIGN_DEVELOPMENT`；必須先修設計、重新審查並重新核准。
