# Scene Writer First-Pass Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重構 Manim 實作指南並強制 scene writer 在首次送檢前完成 layout planning、完整程式重讀與逐 beat 靜態 audit，以降低 overflow、collision、遮擋和生命週期錯誤。

**Architecture:** `references/manim-guidelines.md` 是 Manim coding knowledge 與首次靜態驗證的唯一權威來源；`.codex/agents/scene-writer.toml` 只強制 plan → implement → reread → audit → fix → handoff 的流程，不複製指南細節。既有 render/preflight/reviewer 工具維持最後防線，除非實作時發現明確責任衝突，否則不修改。

**Tech Stack:** Markdown、Codex custom-agent TOML、Python 3.11+ `tomllib`、Python `unittest`、Git、Superpowers skill forward-testing。

## Global Constraints

- 不重做既有 frame overflow 或 collision 檢查工具。
- 不要求 scene writer 在首次送檢前觀看 preview render。
- 不修改已核准動畫的教學語意、Scene 結構或 beat 順序。
- 不強迫所有演算法使用單一固定視覺模板。
- 不模仿特定創作者的程式碼、作品或視覺品牌。
- 完整重構 `manim-guidelines.md`；不得只在舊文件尾端追加新章節。
- 保留工作目錄中與本計畫無關的既有修改；每次 commit 只 stage 當前 task 列出的檔案。

---

## File Map

- `references/manim-guidelines.md`：Manim layout planning、定位推理、衝突策略、物件生命週期、教學呈現與寫後靜態 audit 的唯一權威指南。
- `.codex/agents/scene-writer.toml`：scene writer 的角色、必要輸入、強制執行順序、交付物與送審條件。
- `tests/test_scene_writer_guidance.py`：以結構契約驗證指南章節、首次靜態流程、TOML 可解析性及文件責任邊界。
- `references/render-preflight.md`：既有 render 後檢查；預設不修改。
- `references/scene-review-checklist.md`：既有獨立 review；預設不修改。

### Task 1: 建立首次品質的 RED baseline 與失敗契約測試

**Files:**
- Create: `tests/test_scene_writer_guidance.py`
- Read: `references/manim-guidelines.md`
- Read: `.codex/agents/scene-writer.toml`

**Interfaces:**
- Consumes: UTF-8 Markdown 與 TOML files。
- Produces: 未接觸新版指南的行為 baseline，以及 `SceneWriterGuidanceContractTests`，供後續 tasks 驗證行為改善、文件結構與責任邊界。

- [ ] **Step 1: 建立 RED baseline 行為樣本**

使用未載入新版 `references/manim-guidelines.md` 的 fresh agent，分別提供下列 task-local prompts；不得告知預期 bug 或修正方法：

```text
請設計一個 16:9 Manim Scene：畫面中央顯示九格排序陣列，target 與 result 卡片同時存在，並呈現 binary search 的三輪狀態。只需輸出完整 Python code；完成後重新閱讀 code 並指出你主動修正的 layout 風險。
```

```text
請設計一個 16:9 Manim Scene：binary search 的 left、mid、right pointers 在過程中可能移到同一格，右上角 panel 會替換三組長度不同的文字。只需輸出完整 Python code；完成後重新閱讀 code 並指出你主動修正的 layout 風險。
```

記錄 baseline 是否主動處理：wide-array side overflow、pointer destination collision、longest panel content、peak state 與 stale helper lifecycle。至少一項應出現遺漏或無法證明安全，才構成有效 RED baseline；若全部通過，改用更密集但語意相同的輸入，直到觀察到真實 failure。Baseline 產物放在 session-local temporary location，不加入 repository。

- [ ] **Step 2: 建立結構契約測試**

建立 `tests/test_scene_writer_guidance.py`，內容如下：

```python
from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDELINES = ROOT / "references" / "manim-guidelines.md"
SCENE_WRITER = ROOT / ".codex" / "agents" / "scene-writer.toml"


class SceneWriterGuidanceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guidelines = GUIDELINES.read_text(encoding="utf-8")
        cls.agent = tomllib.loads(SCENE_WRITER.read_text(encoding="utf-8"))
        cls.instructions = cls.agent["developer_instructions"]

    def test_agent_toml_has_required_fields(self) -> None:
        self.assertEqual(self.agent["name"], "scene-writer")
        self.assertIsInstance(self.agent["description"], str)
        self.assertIsInstance(self.instructions, str)

    def test_guidelines_have_required_first_pass_sections(self) -> None:
        required_headings = (
            "## 寫 code 前：先完成 Layout Planning",
            "## Manim Frame、座標與尺寸推理",
            "## Layout Zones 與安全邊界",
            "## 物件定位與群組排版",
            "## 文字、卡片、公式與 Panel 容量",
            "## Pointer、Label 與共址衝突",
            "## Phase Ownership、Transform 與物件生命週期",
            "## Beat Staging 與教學呈現",
            "## 寫完 Python 後：強制靜態 Audit",
            "## 送交既有檢查流程前的完成條件",
        )
        for heading in required_headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.guidelines)

    def test_guidelines_name_known_positioning_risks(self) -> None:
        for term in (
            "next_to()",
            "to_edge()",
            "move_to()",
            "arrange()",
            "Transform()",
            "bounding box",
            "safe frame",
            "peak state",
        ):
            with self.subTest(term=term):
                self.assertIn(term, self.guidelines)

    def test_guidelines_require_pointer_destination_reasoning(self) -> None:
        self.assertRegex(
            self.guidelines,
            re.compile(r"pointer.*目的.*(?:已存在|現有).*pointer", re.IGNORECASE | re.DOTALL),
        )
        self.assertIn("left = mid = right = 5", self.guidelines)

    def test_guidelines_require_full_static_audit(self) -> None:
        for phrase in (
            "重新從頭閱讀",
            "每個 Scene",
            "每個穩定 beat",
            "positioning chain",
            "magic shift",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.guidelines)

    def test_agent_enforces_first_pass_sequence(self) -> None:
        ordered_phrases = (
            "layout plan",
            "generated_algo_scene.py",
            "重新從頭閱讀",
            "靜態 audit",
            "自行修正",
            "既有檢查流程",
        )
        positions = [self.instructions.index(phrase) for phrase in ordered_phrases]
        self.assertEqual(positions, sorted(positions))

    def test_guidelines_do_not_own_review_process(self) -> None:
        forbidden = (
            "Delta Review",
            "Full review",
            "evidence freshness",
            "scene_review_result.md",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.guidelines)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: 執行測試並確認 RED**

Run:

```bash
python3 -m unittest tests/test_scene_writer_guidance.py -v
```

Expected: 測試 suite 可載入，但 `test_guidelines_have_required_first_pass_sections`、`test_guidelines_require_full_static_audit` 或 `test_agent_enforces_first_pass_sequence` 至少一項 FAIL；失敗原因必須是新規則尚未完整存在，而不是 syntax/import error。

- [ ] **Step 4: 確認測試不會誤收 unrelated working-tree changes**

Run:

```bash
git diff -- tests/test_scene_writer_guidance.py
git status --short
```

Expected: 新增的 test file 清楚列出；不修改或 stage 其他既有檔案。

- [ ] **Step 5: 提交 RED contract test**

```bash
git add tests/test_scene_writer_guidance.py
git commit -m "test: define scene writer first-pass guidance contract"
```

Expected: commit 只包含 `tests/test_scene_writer_guidance.py`。

### Task 2: 完整重構 Manim 指南與 Scene Writer 首次流程

**Files:**
- Modify: `references/manim-guidelines.md`
- Modify: `.codex/agents/scene-writer.toml`
- Test: `tests/test_scene_writer_guidance.py`
- Read only unless a concrete conflict is found: `references/render-preflight.md`
- Read only unless a concrete conflict is found: `references/scene-review-checklist.md`

**Interfaces:**
- Consumes: Task 1 的 `SceneWriterGuidanceContractTests` 與已核准設計規格。
- Produces: 重構後的 Manim guide，以及強制 plan → implement → reread → audit → fix → handoff 的 `scene-writer` instructions。

- [ ] **Step 1: 先建立舊指南內容去留表（不新增檔案）**

在實作筆記中逐段標記下列處置，完成後直接依此改檔，不建立永久 auxiliary document：

```text
六個獨立 Scene              -> 保留並移入「實作責任」
核心原則                    -> 合併至「實作責任」與「不可改變事項」
建議檔案結構／狀態管理      -> 改寫至「layout plan 可稽核性」與「物件生命週期」
Hidden Objects              -> 合併至「Phase Ownership」
Phase Ownership             -> 保留、具體化首次出現/持續/更新/移除
Label Highlighting          -> 合併至「文字與 focus 可讀性」
Explanatory Text            -> 合併至「文字與 Panel 容量」
Final Cleanup               -> 合併至「物件生命週期」與完成條件
以 Beat 為核心的實作        -> 改寫為「Beat Staging 與教學呈現」
視覺穩定規則                -> 拆入 zones、pointer、visual continuity
Render-Layer 修復政策       -> 移回 TOML/既有流程，不留 review 路由細節
Voiceover／Overlay 同步      -> 保留 coding-relevant layout/timing，移除流程重複
Constants 與 Styling        -> 合併至 layout roles/zones 的可稽核性
常見場景模式                -> 保留並補上 peak-state 與共址風險
審查準備度                  -> 改寫為首次送檢前靜態完成條件
常見失敗                    -> 合併到對應規則，不保留重複尾章
```

- [ ] **Step 2: 以核准架構重寫 `references/manim-guidelines.md`**

完整替換文件，使其依序包含下列 headings 與不可省略的操作內容：

```markdown
# Manim 實作與首次靜態驗證指南

## 實作責任與不可改變事項
## 寫 code 前：先完成 Layout Planning
## Manim Frame、座標與尺寸推理
## Layout Zones 與安全邊界
## 物件定位與群組排版
## 文字、卡片、公式與 Panel 容量
## Pointer、Label 與共址衝突
## Phase Ownership、Transform 與物件生命週期
## Beat Staging 與教學呈現
## Voiceover 與 Overlay 的實作約束
## 演算法常見結構模式
## 寫完 Python 後：強制靜態 Audit
## 送交既有檢查流程前的完成條件
```

各章必須實作以下精確要求：

- Layout Planning：定義 primary structure、persistent regions、transient regions、safe frame、peak state、collision policy；先排 peak state，再沿用空間骨架。
- Frame reasoning：說明 `config.frame_x_radius`、`config.frame_y_radius` 與物件 `get_left()/get_right()/get_top()/get_bottom()` 的關係；要求以最終 bounding box 推理安全性，並在 frame 內保留一致內縮 margin。
- Positioning APIs：逐一說明 `next_to()`、`to_edge()`、`move_to()`、`arrange()` 與 `Transform()` 只處理局部幾何；定位鏈完成後必須重新推理群組整體尺寸。
- Zones：主結構與 side panel 必須先分配空間；寬主結構禁止在未預留 zone 時直接向右串接卡片。
- Text/panel：panel 依最長內容設計；動態文字使用固定 anchor 與最大寬度；不能靠不可讀縮放處理過載。
- Pointers：移動前檢查目的 index 的現有 pointers；共址時使用垂直分層、上下分流、共享 marker/legend、語意等價合併或合法的分階段顯示。
- Lifecycle：為每個 helper 定義首次出現、持續 beats、更新方式與移除時點；區分透明、遮擋、仍存在及真正移除。
- Teaching quality：納入 visual continuity、one visual question at a time、spatial meaning、progressive disclosure、meaningful transformation、visual economy、peak-state composition、pause on resolved states。
- Static audit：要求重新從頭閱讀完整 Python，逐 Scene、逐穩定 beat 回答設計規格列出的十個 audit 問題，發現無法證明安全的高風險定位時先改 layout。
- Completion：確認六個 Scenes、peak states、最長文字、pointer destinations、物件生命週期與 positioning chains 都已靜態複查，然後才交給既有檢查流程。

- [ ] **Step 3: 修改 `.codex/agents/scene-writer.toml`，加入強制首次流程**

保留既有角色、閱讀清單、上游忠實性、交付與送審內容；在「怎麼實作」後加入以下完整區段：

```markdown
## 第一次送檢前的必要流程

依 `references/manim-guidelines.md`，先為每個 Scene 完成 layout plan，至少確認 primary structure、persistent regions、transient regions、safe frame、peak state 與 collision policy，再開始撰寫 `generated_algo_scene.py`。

完成整支 `generated_algo_scene.py` 後，必須重新從頭閱讀完整檔案，依指南對六個 Scene 的每個穩定 beat 執行靜態 audit。特別追蹤每個 beat 仍存在的物件、最終 positioning chain、共享 anchor 或 index、最長文字、pointer 目的地、Transform 前後狀態及物件移除時點。

若發現 frame overflow、物件碰撞、遮擋、過期 helper、無法容納最長文字，或只能依賴未驗證 magic shift 的構圖，必須先自行修正並重新閱讀受影響的 Scene。完成這個 plan → implement → reread → audit → fix 流程後，才能進入既有檢查流程並準備 render preflight。
```

- [ ] **Step 4: 執行 contract tests 並確認 GREEN**

Run:

```bash
python3 -m unittest tests/test_scene_writer_guidance.py -v
```

Expected: `Ran 7 tests` 且全部 `OK`。

- [ ] **Step 5: 檢查責任邊界與重複內容**

Run:

```bash
rg -n "Delta Review|Full review|evidence freshness|scene_review_result\.md" references/manim-guidelines.md
rg -n "layout plan|peak state|靜態 audit|重新從頭閱讀|既有檢查流程" .codex/agents/scene-writer.toml references/manim-guidelines.md
```

Expected: 第一個 command 無輸出；第二個 command 顯示 TOML 有流程順序、guide 有詳細知識。相同細節不可在兩檔逐段複製。

- [ ] **Step 6: 驗證 TOML 與 diff 品質**

Run:

```bash
python3 -c 'import pathlib,tomllib; p=pathlib.Path(".codex/agents/scene-writer.toml"); d=tomllib.loads(p.read_text()); assert {"name","description","developer_instructions"} <= d.keys(); print("TOML OK")'
git diff --check -- references/manim-guidelines.md .codex/agents/scene-writer.toml tests/test_scene_writer_guidance.py
```

Expected: `TOML OK`；`git diff --check` 無輸出。

- [ ] **Step 7: 提交指南與首次流程重構**

```bash
git add references/manim-guidelines.md .codex/agents/scene-writer.toml
git commit -m "docs: improve scene writer first-pass layout reasoning"
```

Expected: commit 只包含上述兩個 files；Task 1 test 已在前一個 commit。

### Task 3: 行為壓力測試、收斂與最終驗證

**Files:**
- Modify if required by observed failures: `references/manim-guidelines.md`
- Modify if required by observed failures: `.codex/agents/scene-writer.toml`
- Modify if a structural regression needs coverage: `tests/test_scene_writer_guidance.py`
- Do not persist generated animation artifacts in the skill repository.

**Interfaces:**
- Consumes: Task 2 的 guide、agent TOML 與六類壓力案例。
- Produces: 經 forward-test 驗證、沒有明顯 loophole 或模板化傾向的首次品質規則。

- [ ] **Step 1: 使用新版指南執行 GREEN forward-tests**

以 fresh agent 執行相同 prompts，但只增加以下自然使用指示，不提供答案：

```text
請完整遵循此 skill 的 scene-writer 指令與 references/manim-guidelines.md。
```

對每個輸出依下表評分：

```text
PASS  wide structure 與 side information 有預先 zones 或整體 fit 推理
PASS  pointer 移動會檢查目的 index 並採用明確共址策略
PASS  panel 依最長內容設計或有可證明的容量策略
PASS  能指出 peak state，不只檢查開場畫面
PASS  能追蹤 Transform/FadeOut 後仍存在的 objects
PASS  沒有以連續 magic shifts 取代 layout strategy
PASS  沒有強迫所有畫面套用單一模板
```

Expected: 每個新版指南樣本七項全 PASS；若某項 FAIL，保留 agent 的原始理由作為 loophole evidence。

- [ ] **Step 2: 只針對實際 loophole 做最小修訂**

若 Step 1 有 FAIL，依 failure 類型修改唯一權威來源：

```text
缺少 Manim/layout 判斷       -> references/manim-guidelines.md
未執行既有指南或跳過重讀     -> .codex/agents/scene-writer.toml
結構契約無法攔截規則回歸     -> tests/test_scene_writer_guidance.py
```

每次修改必須引用 agent 的實際 rationalization，收緊一條規則後重新執行相同 prompt；不得新增與失敗無關的章節。

- [ ] **Step 3: 執行完整結構驗證**

Run:

```bash
python3 -m unittest tests/test_scene_writer_guidance.py -v
python3 -c 'import pathlib,tomllib; tomllib.loads(pathlib.Path(".codex/agents/scene-writer.toml").read_text()); print("TOML OK")'
git diff --check
```

Expected: `Ran 7 tests`（若 Task 3 新增 regression test，數量相應增加）且 `OK`；`TOML OK`；`git diff --check` 無輸出。

- [ ] **Step 4: 人工核對規格覆蓋與文件整體性**

逐項確認：

```text
[ ] 舊指南每一段已保留、改寫、合併、移出或刪除，沒有附加式重複
[ ] Binary Search overflow 案例由 wide-structure/zone/fit 規則覆蓋
[ ] Binary Search pointer overlap 由 destination/co-location 規則覆蓋
[ ] 指南保留 arrays、search windows、graph traversal 的必要模式
[ ] voiceover/overlay coding constraints 仍存在但沒有流程重複
[ ] TOML 保留上游忠實性、六個 Scenes、交付產物與獨立 review 規則
[ ] preflight/reviewer files 未被不必要修改
[ ] 工作目錄原有 unrelated changes 未被 stage
```

Expected: 全部勾選；任何未通過項目先修正，再重跑 Step 4。

- [ ] **Step 5: 提交 forward-test 收斂修改（僅在有修改時）**

```bash
git add references/manim-guidelines.md .codex/agents/scene-writer.toml tests/test_scene_writer_guidance.py
git commit -m "docs: close scene writer layout reasoning gaps"
```

Expected: 若 Step 2 沒有修改，跳過 commit；若有修改，commit 只包含實際受影響 files。

- [ ] **Step 6: 進行完成前驗證並保存結果**

Run:

```bash
python3 -m unittest tests/test_scene_writer_guidance.py -v
python3 -c 'import pathlib,tomllib; d=tomllib.loads(pathlib.Path(".codex/agents/scene-writer.toml").read_text()); print(d["name"], "OK")'
git diff --check
git status --short
```

Expected: tests 全 PASS；輸出 `scene-writer OK`；無 whitespace errors；`git status` 只顯示使用者既有 unrelated changes，沒有本計畫遺漏的未提交檔案。

## Execution Notes

- Task 1 必須先看見正確的 RED failure，才能實作 Task 2。
- 行為 forward-tests 必須使用 fresh agents，且只提供 raw task 與 skill path；不能洩漏已知 Binary Search 問題或預期解法。
- 若 forward-testing 需要 subagents，執行前依 repository skill 的授權規則取得使用者明確同意。
- 每個 task 完成後進行 spec compliance 與 document quality review，再進入下一個 task。
- 不使用 `git add .`；工作目錄已有其他未提交修改。
