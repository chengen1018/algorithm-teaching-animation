# 選擇並驗證 Manim 輸出設定

## 目的

主要 Agent 在需求確認後建立 `<project-root>/render_profile.json`。這個檔案固定本次動畫使用的 Manim 執行環境、字型、畫面範圍與影片輸出規格，讓後續版面檢查和正式渲染使用相同設定。

## 執行前準備

1. 確認 `<absolute-project-root>` 是動畫專案根目錄的絕對路徑。
2. 找出能成功 `import manim` 的 Python，並取得它的絕對路徑。
3. 選擇預期能完整顯示畫面文字、且列在 ManimPango 可用字型清單中的字型。
4. 檢查使用者是否主動指定解析度、frame rate、renderer 或 frame geometry。未指定的項目使用本指南列出的預設值。

## 建立設定檔

執行：

```bash
python <absolute-skill-root>/scripts/prepare_render_profile.py \
  --project-root <absolute-project-root> \
  --python <absolute-manim-python> \
  --font <font-name>
```

若使用者指定其他輸出規格，先執行以下命令查看支援的選項，再把對應參數加入建立命令：

```bash
python <absolute-skill-root>/scripts/prepare_render_profile.py --help
```

Helper 會確認指定的 Python 能載入 Manim、取得 Manim 版本、確認所有數值大於零，並把字型名稱對應到 ManimPango 回報的正式名稱。指定字型不在可用清單時，改選實際存在的字型後重新執行。

Helper 只確認字型可供 ManimPango 使用，不檢查字型是否包含畫面文字需要的所有字形。主要 Agent 仍須依動畫文字的語言選擇合適字型。

## `render_profile.json` 的內容與來源

| 欄位 | 來源 | 未指定時的值 |
| --- | --- | --- |
| `schema_version` | Helper 固定寫入 | `1` |
| `python_executable` | 主要 Agent 選擇；Helper 寫入解析後的絕對路徑 | 無預設值 |
| `manim_version` | Helper 從指定 Python 自動偵測 | 無預設值 |
| `font` | 主要 Agent 選擇；Helper 寫入 ManimPango 回報的正式名稱 | 無預設值 |
| `pixel_width` | 使用者指定或 Helper 預設值 | `1920` |
| `pixel_height` | 使用者指定或 Helper 預設值 | `1080` |
| `frame_rate` | 使用者指定或 Helper 預設值 | `60` |
| `renderer` | 使用者指定或 Helper 預設值 | `cairo` |
| `frame_width` | 使用者指定或 Helper 預設值 | `14.2222222222` |
| `frame_height` | 使用者指定或 Helper 預設值 | `8.0` |

## 完成條件

以下條件全部成立後，才算完成：

- Helper 的 exit code 是 `0`。
- `<project-root>/render_profile.json` 已建立，並且能解析為 JSON。
- 檔案包含表格列出的全部欄位。
- 使用者指定的設定已正確寫入；其餘設定使用表格列出的預設值。
- `python_executable`、`manim_version` 與 `font` 對應本次通過 Helper 驗證的 Manim 環境。

完成後，把 `render_profile.json` 作為後續階段共用的唯讀輸入。若之後需要修改它，依 `SKILL.md` 的階段回退規則重新取得受影響的檢查結果。
