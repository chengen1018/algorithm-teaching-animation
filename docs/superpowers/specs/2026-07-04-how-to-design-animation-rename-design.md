# How to Design Animation 重新命名設計

## 目標

將原本的通用動畫設計指南重新命名為 `references/how-to-design-animation.md`，讓檔名直接表達文件用途。

## 變更範圍

- 保留文件內容與所有現行未提交修改，只改變檔案路徑。
- 將儲存庫內所有原檔名引用改為 `how-to-design-animation.md`。
- 更新範圍包含有效執行文件、references、歷史設計規格與實作計畫。
- 不保留舊檔或重新導向 stub；重新命名後舊名稱必須完全消失。

## 驗證

1. `references/how-to-design-animation.md` 存在。
2. 原檔路徑不存在。
3. 排除 `.git` 後，全儲存庫搜尋不到原檔名。
4. 所有原引用位置都改為 `references/how-to-design-animation.md`。
5. 新檔內容仍包含六個固定 Scene、四個必要欄位與審查 gate。
6. `git diff --check` 通過。
