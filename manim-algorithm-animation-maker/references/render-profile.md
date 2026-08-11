# Render Profile

`render_profile.json` 是 layout audit 與正式 render 共用的唯一輸出設定。Coordinator 在需求確認後建立它；後續角色只讀取，不自行改寫。

## 建立方式

先找出能成功 `import manim` 的 Python 絕對路徑，再選擇一個支援畫面文字語言、且已安裝在相同環境中的字型。執行：

```bash
python <absolute-skill-root>/scripts/prepare_render_profile.py \
  --project-root <absolute-project-root> \
  --python <absolute-manim-python> \
  --font <font-name>
```

除非使用者明確指定其他輸出規格，使用以下預設值：

- `pixel_width`: `1920`
- `pixel_height`: `1080`
- `frame_rate`: `60`
- `renderer`: `cairo`
- `frame_width`: `14.2222222222`
- `frame_height`: `8.0`

Script 會確認指定 Python 能載入 Manim、記錄 Manim 版本，並確認指定字型出現在 ManimPango 可用字型清單中。找不到字型時必須改選實際存在的字型；不能依賴 fallback。

## 必要欄位

```json
{
  "schema_version": 1,
  "pixel_width": 1920,
  "pixel_height": 1080,
  "frame_rate": 60,
  "renderer": "cairo",
  "frame_width": 14.2222222222,
  "frame_height": 8.0,
  "font": "<resolved font name>",
  "python_executable": "<absolute path>",
  "manim_version": "<detected version>"
}
```

## 使用規則

- Scene Writer 使用 profile 的 `font` 與 frame geometry 實作版面。
- Layout Validator 使用 profile 的 `python_executable` 執行 runner，並把 profile 絕對路徑與 SHA-256 寫入 `layout_audit_result.md`。
- Final Renderer 使用同一個 Python、renderer、解析度與 frame rate。
- `render_manifest.md` 記錄 profile path 與 SHA-256。
- Profile 內容改變後，舊的 handoff、layout result、scene review、render manifest、MP4 與 delivery result 都失效；從 Stage 4 `CODE_PREPARATION` 重新開始。
