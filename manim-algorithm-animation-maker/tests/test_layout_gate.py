from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class LayoutGateTests(unittest.TestCase):
    def test_generic_overlap_is_diagnostic_but_overflow_fails(self) -> None:
        runner = load_module("run_layout_audit_test", SKILL_ROOT / "scripts" / "run_layout_audit.py")
        checkpoints = ["initial", "beat:compare", "final"]

        self.assertEqual(
            runner.gate_failures(visible_errors=0, visible_warnings=3, checkpoints=checkpoints, require_adapter=True),
            [],
        )
        failures = runner.gate_failures(
            visible_errors=1,
            visible_warnings=0,
            checkpoints=checkpoints,
            require_adapter=True,
        )
        self.assertTrue(any("frame" in failure.lower() for failure in failures))

    def test_required_adapter_needs_initial_beat_and_final_checkpoints(self) -> None:
        runner = load_module("run_layout_audit_checkpoint_test", SKILL_ROOT / "scripts" / "run_layout_audit.py")

        failures = runner.gate_failures(
            visible_errors=0,
            visible_warnings=0,
            checkpoints=["initial", "final"],
            require_adapter=True,
        )

        self.assertTrue(any("beat" in failure.lower() for failure in failures))

    def test_scene_adapter_records_named_checkpoint(self) -> None:
        previous_manim = sys.modules.get("manim")
        sys.modules["manim"] = types.SimpleNamespace(config=types.SimpleNamespace(frame_width=14.222, frame_height=8.0))
        try:
            adapter = load_module("scene_layout_audit_test", SKILL_ROOT / "scripts" / "scene_layout_audit.py")
            adapter.reset_layout_audit_checkpoints()
            adapter.LayoutAudit(context="beat:swap").report(raise_on_issue=True)
            self.assertEqual(adapter.get_layout_audit_checkpoints(), ["beat:swap"])
        finally:
            if previous_manim is None:
                sys.modules.pop("manim", None)
            else:
                sys.modules["manim"] = previous_manim


if __name__ == "__main__":
    unittest.main()
