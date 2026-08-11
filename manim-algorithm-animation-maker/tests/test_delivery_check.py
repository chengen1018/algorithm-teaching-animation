from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "verify_delivery.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DeliveryCheckTests(unittest.TestCase):
    def _write_executable(self, path: Path, body: str) -> None:
        path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
        path.chmod(path.stat().st_mode | 0o111)

    def _build_fixture(
        self,
        root: Path,
        *,
        reported_fps: int,
        include_audio: bool = True,
    ) -> tuple[Path, Path, Path, Path, Path, Path]:
        source = root / "generated_algo_scene.py"
        profile = root / "render_profile.json"
        manifest = root / "render_manifest.md"
        output = root / "delivery_check_result.md"
        source.write_text("# approved source\n", encoding="utf-8")
        profile.write_text(
            json.dumps(
                {
                    "pixel_width": 1920,
                    "pixel_height": 1080,
                    "frame_rate": 60,
                    "renderer": "cairo",
                }
            ),
            encoding="utf-8",
        )

        scene_paths = []
        for index in range(1, 5):
            scene_path = root / f"scene-{index}.mp4"
            scene_path.write_bytes(b"media")
            scene_paths.append(scene_path)
        combined = root / "combined.mp4"
        combined.write_bytes(b"media")

        manifest.write_text(
            textwrap.dedent(
                f"""
                # Render Manifest

                ## Approved Source and Stage 4 Gate
                - Code path: `{source}`
                - Approved Code SHA-256: `{sha256(source)}`
                - Rendered Source Code SHA-256: `{sha256(source)}`

                ## Render Profile
                - Render Profile path: `{profile}`
                - Render Profile SHA-256: `{sha256(profile)}`

                ## Scene Outputs
                | Render order | Scene class | Exact Manim command | Exit code | MP4 path |
                | --- | --- | --- | --- | --- |
                | 1 | `SceneOne` | `render one` | `0` | `{scene_paths[0]}` |
                | 2 | `SceneTwo` | `render two` | `0` | `{scene_paths[1]}` |
                | 3 | `SceneThree` | `render three` | `0` | `{scene_paths[2]}` |
                | 4 | `SceneFour` | `render four` | `0` | `{scene_paths[3]}` |

                ## Concat and Combined Output
                - Exact concat command: `concat`
                - Concat exit code: `0`
                - Combined MP4 path: `{combined}`
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        ffprobe = root / "ffprobe"
        audio_stream = ', {"codec_type": "audio", "duration": str(duration)}' if include_audio else ""
        self._write_executable(
            ffprobe,
            textwrap.dedent(
                f"""
                import json
                import sys
                from pathlib import Path

                duration = 8.0 if Path(sys.argv[-1]).name == "combined.mp4" else 2.0
                print(json.dumps({{
                    "streams": [
                        {{"codec_type": "video", "width": 1920, "height": 1080, "avg_frame_rate": "{reported_fps}/1", "duration": str(duration)}}{audio_stream}
                    ],
                    "format": {{"duration": str(duration)}}
                }}))
                """
            ),
        )
        ffmpeg = root / "ffmpeg"
        self._write_executable(ffmpeg, "raise SystemExit(0)\n")
        return source, profile, manifest, output, ffprobe, ffmpeg

    def _run(self, fixture: tuple[Path, Path, Path, Path, Path, Path]) -> subprocess.CompletedProcess[str]:
        source, profile, manifest, output, ffprobe, ffmpeg = fixture
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--source",
                str(source),
                "--profile",
                str(profile),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
                "--ffprobe",
                str(ffprobe),
                "--ffmpeg",
                str(ffmpeg),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_passes_when_media_profile_duration_and_hashes_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._build_fixture(Path(temp_dir), reported_fps=60)
            completed = self._run(fixture)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            output = fixture[3].read_text(encoding="utf-8")
            self.assertIn("Result: PASS", output)
            self.assertIn("1920x1080", output)
            self.assertIn("60.000", output)
            self.assertIn("## Commands", output)
            self.assertIn(str(fixture[4]), output)
            self.assertIn(str(fixture[5]), output)
            self.assertIn("Source hash match: `PASS`", output)
            self.assertIn("Render profile hash match: `PASS`", output)
            self.assertIn("Scene duration total: `8.000s`", output)
            self.assertIn("Combined duration: `8.000s`", output)

    def test_fails_when_media_frame_rate_differs_from_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._build_fixture(Path(temp_dir), reported_fps=30)
            completed = self._run(fixture)

            self.assertNotEqual(completed.returncode, 0)
            output = fixture[3].read_text(encoding="utf-8")
            self.assertIn("Result: FAIL", output)
            self.assertIn("frame rate", output.lower())

    def test_fails_when_audio_stream_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._build_fixture(Path(temp_dir), reported_fps=60, include_audio=False)
            completed = self._run(fixture)

            self.assertNotEqual(completed.returncode, 0)
            output = fixture[3].read_text(encoding="utf-8")
            self.assertIn("audio stream is missing", output)

    def test_fails_when_profile_changed_after_manifest_was_frozen(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._build_fixture(Path(temp_dir), reported_fps=60)
            profile = fixture[1]
            data = json.loads(profile.read_text(encoding="utf-8"))
            data["frame_rate"] = 30
            profile.write_text(json.dumps(data), encoding="utf-8")

            completed = self._run(fixture)

            self.assertNotEqual(completed.returncode, 0)
            output = fixture[3].read_text(encoding="utf-8")
            self.assertIn("render profile hash does not match manifest", output)


if __name__ == "__main__":
    unittest.main()
