from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "prepare_render_profile.py"


class RenderProfileTests(unittest.TestCase):
    def _stub_manim_environment(self, root: Path) -> dict[str, str]:
        (root / "manim.py").write_text("__version__ = '0.19.0-test'\n", encoding="utf-8")
        (root / "manimpango.py").write_text(
            "def list_fonts():\n"
            "    return ['Noto Sans CJK TC', 'Arial']\n",
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(root)
        return env

    def test_writes_approved_default_profile_from_verified_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            env = self._stub_manim_environment(project_root)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    str(project_root),
                    "--python",
                    sys.executable,
                    "--font",
                    "Noto Sans CJK TC",
                ],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            profile = json.loads((project_root / "render_profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["pixel_width"], 1920)
            self.assertEqual(profile["pixel_height"], 1080)
            self.assertEqual(profile["frame_rate"], 60)
            self.assertEqual(profile["renderer"], "cairo")
            self.assertEqual(profile["font"], "Noto Sans CJK TC")
            self.assertEqual(profile["python_executable"], str(Path(sys.executable).resolve()))
            self.assertEqual(profile["manim_version"], "0.19.0-test")

    def test_rejects_font_that_runtime_cannot_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            env = self._stub_manim_environment(project_root)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    str(project_root),
                    "--python",
                    sys.executable,
                    "--font",
                    "Missing Font",
                ],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Missing Font", completed.stderr)
            self.assertFalse((project_root / "render_profile.json").exists())


if __name__ == "__main__":
    unittest.main()
