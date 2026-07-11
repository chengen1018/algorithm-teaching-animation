from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDELINES = ROOT / "references" / "manim-guidelines.md"
SCENE_WRITER = ROOT / ".codex" / "agents" / "scene-writer.toml"
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-07-11-scene-writer-first-pass-quality-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-07-11-scene-writer-first-pass-quality.md"


class SceneWriterGuidanceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guidelines = GUIDELINES.read_text(encoding="utf-8")
        cls.agent = tomllib.loads(SCENE_WRITER.read_text(encoding="utf-8"))
        cls.instructions = cls.agent["developer_instructions"]
        cls.design = DESIGN.read_text(encoding="utf-8")
        cls.plan = PLAN.read_text(encoding="utf-8")

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
            "## Construction Patterns：以構造降低失敗機率",
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
        missing_phrases = []
        for phrase in ordered_phrases:
            with self.subTest(phrase=phrase):
                if phrase not in self.instructions:
                    missing_phrases.append(phrase)
                self.assertIn(phrase, self.instructions)
        if missing_phrases:
            return
        positions = [self.instructions.index(phrase) for phrase in ordered_phrases]
        self.assertEqual(positions, sorted(positions))

    def test_construction_patterns_cover_known_failure_modes(self) -> None:
        heading = "## Construction Patterns：以構造降低失敗機率"
        self.assertIn(heading, self.guidelines)
        section = self.guidelines.partition(heading)[2].split("\n## ", 1)[0]
        required = (
            "### Peak-first scene skeleton",
            "### Group-first zone fitting",
            "### Content-first containers",
            "### State-first pointer layout",
            "### Current-object replacement ownership",
            "### Phase-owned helper construction",
            "### Stable-zone composition",
            "所有候選",
            "active pointer roles",
            "立即重新綁定",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)

    def test_construction_examples_teach_creation_not_checkers(self) -> None:
        heading = "## Construction Patterns：以構造降低失敗機率"
        self.assertIn(heading, self.guidelines)
        section = self.guidelines.partition(heading)[2].split("\n## ", 1)[0]
        subsections = (
            "### Content-first containers",
            "### State-first pointer layout",
            "### Current-object replacement ownership",
        )
        for subsection_heading in subsections:
            with self.subTest(subsection=subsection_heading):
                subsection = section.partition(subsection_heading)[2].split("\n### ", 1)[0]
                self.assertIn("Bad", subsection)
                self.assertIn("Good", subsection)
        for forbidden in ("assert ", "layout guard", "audit schema"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, section.lower())

    def test_content_first_example_preserves_readable_line_plan(self) -> None:
        heading = "### Content-first containers"
        subsection = self.guidelines.partition(heading)[2].split("\n### ", 1)[0]
        self.assertIn("line_plans", subsection)
        self.assertNotIn("scale_to_fit_width", subsection)

    def test_agent_delegates_pattern_detail_to_guide(self) -> None:
        self.assertIn("construction patterns", self.instructions.lower())
        self.assertIn("references/manim-guidelines.md", self.instructions)
        for detail in ("Content-first containers", "State-first pointer layout", "Current-object replacement ownership"):
            with self.subTest(detail=detail):
                self.assertNotIn(detail, self.instructions)

    def test_guidance_does_not_require_generated_guard_artifacts(self) -> None:
        combined = self.guidelines + self.instructions + self.design + self.plan
        for forbidden in (
            "## Generated-code 輕量 Layout Guards",
            "Generated-code layout guard 交付 gate",
            "每支 `generated_algo_scene.py` 必須定義或匯入",
            "raw generated code 定義或匯入並實際呼叫 guards",
            "canonical audit interface",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)

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
