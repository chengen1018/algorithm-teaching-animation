# Layout Audit

在 Stage 4 `LAYOUT_VERIFICATION` 使用本文件。Layout audit 會建立真實 Manim mobjects，但不寫入 frame 或 MP4。

## 執行輸入與 Preflight

執行前，確認派遣訊息中的所有 `Required inputs` 均存在且可讀，並確認 `Scene classes and approved order` 依核准順序列出五個互不重複、且存在於目前 `Scene source` 的 Scene class。

Preflight 失敗時，建立 `layout_audit_result.md` 並寫入 `Result: FAIL` 與失敗證據；只有連結果檔都無法建立時才是 `BLOCKED`。

## 適用範圍

- Scene Writer 只使用 project-side adapter/checkpoint contract。
- Scene Writer 不執行 Layout Validator Preflight、必要命令或建立 `layout_audit_result.md`。
- Layout Validator 使用 execution input/Preflight、必要命令、gate/result。

## 三個元件各自負責什麼

- `run_layout_audit.py`：載入 Scene、把動畫直接推到結束狀態、跳過 `wait()` 與音訊，並執行檢查。
- `visible_layout_audit.py`：掃描所有可見物件。超出 frame 是錯誤；overlap 只輸出診斷，因為泛用掃描不知道重疊是否符合畫面語意。
- `scene_layout_audit.py`：由 Scene Writer 以具名物件建立 adapter，檢查文字是否放得進 panel、標籤是否撞到節點、標題與主要區域是否保有距離等具體關係。

泛用掃描不能取代 scene-specific adapter。每個交付 Scene 都必須有 adapter。

## 加入 project

把 helper 複製到 `generated_algo_scene.py` 同一層：

```text
<project>/
├── generated_algo_scene.py
└── scene_layout_audit.py
```

Scene 中使用：

```python
import os
from scene_layout_audit import LayoutAudit

LAYOUT_AUDIT_ENABLED = os.getenv("MANIM_LAYOUT_AUDIT", "1").lower() not in {"0", "false", "no"}
LAYOUT_AUDIT_FAIL = os.getenv("MANIM_LAYOUT_AUDIT_FAIL", "0").lower() in {"1", "true", "yes"}

def _audit_layout(self, context, nodes, labels, panels, header=None, extra_items=None):
    audit = LayoutAudit(context=context, enabled=LAYOUT_AUDIT_ENABLED)
    header = header or []
    extra_items = extra_items or []
    all_items = nodes + labels + panels + header + extra_items

    for name, mob in all_items:
        audit.check_inside_frame(name, mob)

    audit.check_no_internal_overlaps(labels, min_gap=0.05)
    audit.check_no_overlaps_between(labels, nodes, min_gap=0.03)
    audit.check_no_overlaps_between(nodes + labels, panels, min_gap=0.05)
    audit.check_no_overlaps_between(header + extra_items, nodes + labels + panels, min_gap=0.05)
    audit.report(raise_on_issue=LAYOUT_AUDIT_FAIL)
```

只有真的應該分開的物件才放進 `check_no_overlap`。例如文字在自己的 panel 內、highlight 包住元素、arrow 接觸 node，都不應被寫成禁止重疊的關係。

## 必要 checkpoint

每個 Scene 至少執行三類穩定狀態：

```python
self._audit_layout("initial", nodes, labels, panels, header=[("title", title)])
self._audit_layout(f"beat:{beat_id}", nodes, labels, panels, header=[("title", title), ("message", message)])
self._audit_layout("final", nodes, labels, panels, extra_items=[("result", result_text)])
```

- `initial`：主要版面建立完成後。
- `beat:<id>`：每個文字、pointer、panel 或物件組合發生重要變化的穩定 beat。
- `final`：結果與最後保留內容完成後。

Runner 會檢查三類名稱是否都出現。缺少任一類時，該 Scene 不能通過 gate。

Scene 4 必須在每個必要 derivation phase 的 resolved state 建立 `beat:<id>` checkpoint，並把當下可見的公式、case label、多變數圖或 auxiliary-space diagram 納入具名 adapter；不能只檢查公式最後完整出現的畫面。

## 必要命令

對派遣訊息提供的五個 Scene class 依核准順序分別執行：

```bash
<render-profile-python> <absolute-runner-path> \
  <absolute-project-root>/generated_algo_scene.py <SceneClass> \
  --render-profile <absolute-project-root>/render_profile.json \
  --audit-visible \
  --require-adapter \
  --visible-report-level warning
```

Runner 會：

1. 驗證目前 Python、Manim 版本、字型與 `render_profile.json` 一致。
2. 套用 profile 記錄的 frame geometry、解析度、frame rate 與 renderer；未經使用者覆寫時即為 1920×1080、60 fps、Cairo。
3. 執行 Scene adapter 與泛用可見物件掃描。
4. 在 stdout 記錄 profile 設定與 adapter checkpoint 名稱。

## Gate 判定

以下任一情況使命令 exit `1`：

- Scene 建立或動畫狀態推進失敗。
- 可見物件超出 frame。
- Adapter 的 fit、collision 或 spacing 檢查失敗。
- 缺少 initial、beat 或 final checkpoint。
- 執行中的 Python、Manim、font 或 profile 設定不一致。

泛用 overlap 訊息保留在輸出中協助找問題，但不單獨決定 exit code。真正需要禁止的重疊必須由 adapter 以具名物件明確檢查。

## `layout_audit_result.md`

結果檔必須記錄：

- `Result: PASS` 或 `Result: FAIL`
- Render profile 及執行環境欄位
- 五個 Scene 的核准順序
- 每個實際 command、stdout、stderr 與 exit code
- 每個 Scene 的 adapter checkpoint summary
- 所有 blocking findings

只有 Preflight 通過、五個核准 Scene 全部受檢、每個 Scene 的 initial／beat／final checkpoint 完整，且五個必要 command 全部 exit `0` 時，才能寫入 `Result: PASS`。其餘情況寫入 `Result: FAIL`。

## Adapter 可用檢查

- `check_inside_frame(name, mob, margin=0.1)`：物件是否留在 safe frame。
- `check_fits(inner_name, inner, outer_name, outer, padding=0.15)`：文字或內容是否放得進 panel。
- `check_no_overlap(a_name, a, b_name, b, min_gap=0.05)`：兩個具名物件是否重疊或距離不足。
- `check_no_internal_overlaps(items, min_gap=0.05)`：同一組 labels 或 repeated items 是否互撞。
- `check_no_overlaps_between(group_a, group_b, min_gap=0.05)`：兩組具名物件是否互撞。

## 限制

- Dry-run 只檢查動畫完成後的穩定狀態，不檢查逐 frame interpolation。
- Bounding box 不適合直接判斷 arrow 或 curved path；只在有明確需求時加入相關 adapter 規則。
- Adapter 只會執行 Scene 程式碼實際呼叫的 checkpoint，因此重要 beat 必須明確呼叫。
