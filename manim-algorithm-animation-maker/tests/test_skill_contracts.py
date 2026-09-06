from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"


def read(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_stage_and_default_render_profile_are_unambiguous(self) -> None:
        skill = read("SKILL.md")
        self.assertIn("FINAL_RENDER_AND_DELIVERY_CHECK", skill)
        self.assertIn("render_profile.json", skill)
        self.assertIn("1920", skill)
        self.assertIn("1080", skill)
        self.assertIn("60", skill)
        self.assertIn("Cairo", skill)

    def test_design_reviewer_contract_lists_its_complete_inputs(self) -> None:
        contract = read("references/subagent-animation-design-reviewer.md")
        self.assertIn("confirmed_requirements.md", contract)
        self.assertIn("animation_design.md", contract)
        self.assertIn("how-to-review-design.md", contract)
        self.assertIn("唯一一份", contract)
        self.assertIn("專用", contract)

    def test_voiceover_contract_lists_its_complete_inputs(self) -> None:
        contract = read("references/subagent-voiceover-generator.md")
        for required_input in (
            "confirmed_requirements.md",
            "animation_design.md",
            "teaching_script.md",
            ".tts-config",
            "how-to-write-and-generate-voiceover.md",
            "generate_voiceover_audio.py",
        ):
            self.assertIn(required_input, contract)

    def test_handoff_and_manifest_record_scene_order_and_exit_codes(self) -> None:
        handoff = read("references/how-to-hand-off-scene-code-for-review.md")
        render = read("references/how-to-render-approved-manim-scenes.md")
        self.assertIn("Scene class", handoff)
        self.assertIn("核准順序", handoff)
        self.assertIn("Exit code", render)

    def test_render_profile_change_restarts_code_preparation(self) -> None:
        skill = read("SKILL.md")
        self.assertIn("`render_profile.json` 改變，回到 `CODE_PREPARATION`", skill)
        self.assertIn("profile 未改變但執行環境", skill)

    def test_layout_gate_uses_scene_adapter_checkpoints(self) -> None:
        active_files = [
            SKILL_ROOT / "SKILL.md",
            REFERENCES / "layout-audit.md",
            REFERENCES / "subagent-scene-layout-validator.md",
            SKILL_ROOT / "scripts" / "run_layout_audit.py",
        ]
        for path in active_files:
            self.assertIn("--require-adapter", path.read_text(encoding="utf-8"), str(path))

    def test_visible_warnings_are_authoritative_across_active_contracts(self) -> None:
        active_files = (
            "SKILL.md",
            "references/layout-audit.md",
            "references/subagent-scene-layout-validator.md",
        )
        for relative_path in active_files:
            content = read(relative_path)
            self.assertIn("unresolved warning", content, relative_path)
            self.assertIn("FAIL", content, relative_path)

    def test_graph_best_effort_and_complete_reports_are_narrowly_documented(self) -> None:
        layout = read("references/layout-audit.md")
        self.assertIn("register_graph_root", layout)
        self.assertIn("best-effort", layout)
        self.assertIn("同一個 registered graph root", layout)
        self.assertIn("不同 graph roots：嚴格規則", layout)
        self.assertIn("graph 對 non-graph：嚴格規則", layout)
        self.assertIn("line-like", layout)
        self.assertIn("完整 JSON", layout)
        self.assertIn("infos", layout)
        self.assertIn("source_sha256", layout)

        for relative_path in (
            "SKILL.md",
            "references/subagent-scene-layout-validator.md",
            "references/subagent-scene-writer.md",
        ):
            self.assertIn("best-effort", read(relative_path), relative_path)

    def test_specialized_design_headings_use_plain_language(self) -> None:
        specialized = "\n".join(
            read(path)
            for path in (
                "references/how-to-design-array-sorting-animation.md",
                "references/how-to-design-graph-traversal-animation.md",
                "references/how-to-design-narrowing-search-animation.md",
            )
        )
        for clear_heading in (
            "每一步正在比較或更新哪些資料",
            "元素要怎麼移動或更新",
            "如何顯示目前已完成到哪裡",
            "元素暫時移出陣列時放在哪裡",
            "相同數值的元素是否需要區分",
        ):
            self.assertIn(clear_heading, specialized)


if __name__ == "__main__":
    unittest.main()
