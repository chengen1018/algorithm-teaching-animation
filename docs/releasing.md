# Release 維護流程

[返回 README](../README.md)

本文件供維護者發布正式版本時使用。

## 版本規則

- Major：破壞既有 Skill contract、必要輸入／輸出或使用方式。
- Minor：新增向後相容的 workflow 能力、工具或支援範圍。
- Patch：向後相容的錯誤修正、相容性修正或文件修正。

`0.x` 階段仍可能調整 contract。任何破壞性變更都必須在 Release notes 與 Changelog 中明確說明。

## 發布前檢查

1. 確認工作目錄乾淨，且版本分支不含未核准 commit。
2. 執行快速檢查：

   ```bash
   python3 scripts/check_repository.py
   ```

3. 從全新 clone 依 README 完成安裝與 Quickstart 文件檢查。
4. 確認 GitHub Actions 的 Python 3.10、3.11、3.12 jobs 全部通過。
5. 確認三張 poster、YouTube links 與待上傳 MP4 的對應關係。
6. 使用 FFprobe 檢查三支 MP4 的影像與聲音 streams、解析度、frame rate 和 duration。
7. 更新 `CHANGELOG.md`、`pyproject.toml` 版本與 Release notes。
8. 建立 signed 或 annotated tag，例如 `v0.1.0`。
9. 上傳 Release assets，並在 Release notes 記錄 SHA-256。
10. 從未登入瀏覽器檢查 README、Release 與所有下載連結。

## v0.1.0 影片 assets

| 演算法 | Release asset 名稱 | YouTube |
| --- | --- | --- |
| Quick Sort | `QuickSort_1080p60.mp4` | <https://www.youtube.com/watch?v=Lmz1Z9-1f3Q> |
| Longest Common Subsequence | `combined_lcs.mp4` | <https://www.youtube.com/watch?v=gUQMSyASYw0> |
| Johnson Algorithm | `JohnsonAlgorithmCombined.mp4` | <https://www.youtube.com/watch?v=jqRVnd7lnlc> |

完整 MP4 只附加在 GitHub Release，不加入一般 Git branch。

`v0.1.0` 的已驗證 SHA-256 與完整 Release 內容記錄於 [`docs/releases/v0.1.0.md`](releases/v0.1.0.md)。

## Release notes 必要內容

- 版本包含的功能與文件範圍。
- 安裝需求與支援的 Python 版本。
- 已知限制與可能的升級影響。
- 三支影片的檔名、duration、resolution、YouTube link 與 SHA-256。
- 完整測試與 CI 狀態。

## 發布後

- 確認 GitHub 正確顯示 tag、License、Release assets 與 Changelog link。
- 確認 README 的三個 `Download MP4` links 可以下載正確檔案。
- 若 asset、notes 或 checksum 有誤，修正 Release；不要以修改 Git 歷史代替 Release 修正。
