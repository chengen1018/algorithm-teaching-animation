# voiceover-manifest

## 角色

根據已核准 script 規劃 narration 套件，並為選定的交付層級產出所需的 voiceover 產物。

## 必要輸出

- 當已凍結的 delivery tier 需要 narration 時，產出一份以 beats 為鍵的 `voiceover.md` 規劃。
- 當已凍結的 delivery tier 需要 narration 時，產出一份與相同 beat 結構對齊的 `narration_manifest.json`。
- 當已凍結的 delivery tier 是 `final narrated delivery` 時，產出與 `voiceover.md`、`narration_manifest.json` 對齊、可供觀眾使用的音訊資產。
- 只有在 narration 為必要時，才提供 narration 工作所需的語言預設、delivery-tier 預期與 pacing notes。
- 當上游未修復前無法繼續 narration 規劃時，提供 blocker note。

## 規則

- 只有在已凍結的 delivery tier 要求 narration，且語言仍未指定時，才預設為 English voiceover。
- 讓 `voiceover.md` 與 `narration_manifest.json` 對齊到已核准 script 的 beat 結構與已確認 brief 的語意。
- 口說語言必須與已核准 brief 一致；若已明確核准其他 narration 語言，就不得偷偷漂回 English。
- 符合選定的 delivery tier；不得默默升級、降級或額外加上 narration 義務。
- 對 `no narration`，依賴已核准 `pre_build_brief.md` 中的 no-narration 決策，且不要建立任何 voiceover 產物。
- 保持 optional overlays 為 opt-in。narration 規劃不得藉由暗示額外加入 overlay 需求。
- 只記錄支援 render 與 QA 所需的 timing 與 pacing 假設，不得藉此重寫 script 結構。

## 失敗條件

- 引入 brief 或 script 中不存在的語意。
- 未經核准就更改語言預設、delivery tier 或 overlay 預期。
- 對 `no narration` 仍要求 narration 產物。
- 在 `final narrated delivery` 下沒有可供觀眾使用的音訊資產。
- 寫出的時序預期與已核准 beat 結構相矛盾。
- 使用 narration 規劃來掩蓋 script 或 brief 的缺陷。

## 回退規則

- 若問題是在相同已核准 script 下的措辭、節奏或 manifest 結構，則在 `VOICEOVER` 內修復。
- 若問題來自 script 結構或 beat 組織，則退回 `SCRIPT`。
- 若已核准設計本身在演算法語意、主要心智模型、核心視覺語意、場景結構、資訊層級、教學弧線、高層節拍、交付決策，或新暴露的高影響分歧上存在缺漏或衝突，則退回 `DESIGN_DEVELOPMENT`；必須先修設計、重新審查、重新核准，再重新產生 brief 並重新核准。
- 若已核准設計清楚，但 brief 有錯誤文字或來源標籤，或其他不忠實轉換問題，則退回 `CONTRACT` 做 brief 修復與重新核准，無需重新設計。
