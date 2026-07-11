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
