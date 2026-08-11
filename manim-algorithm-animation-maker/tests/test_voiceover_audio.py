from __future__ import annotations

import json
import math
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "generate_voiceover_audio.py"


def write_wav(path: Path, *, silent: bool) -> None:
    sample_rate = 24000
    frames = []
    for index in range(sample_rate // 2):
        value = 0 if silent else int(10000 * math.sin(2 * math.pi * 440 * index / sample_rate))
        frames.append(struct.pack("<h", value))
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(frames))


class VoiceoverAudioTests(unittest.TestCase):
    def test_validate_only_records_audio_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_path = root / "beat-001.wav"
            manifest_path = root / "narration_manifest.json"
            write_wav(audio_path, silent=False)
            manifest_path.write_text(
                json.dumps(
                    {
                        "language": "zh",
                        "beats": [
                            {"id": "beat-001", "text": "比較這兩個元素。", "audio_path": str(audio_path)}
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    str(root),
                    "--manifest",
                    str(manifest_path),
                    "--validate-only",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(manifest_path.read_text(encoding="utf-8"))["beats"][0]
            self.assertTrue(result["validation"]["passed"])
            self.assertEqual(result["sample_rate"], 24000)
            self.assertEqual(result["channels"], 1)
            self.assertGreater(result["peak"], 0)
            self.assertGreater(result["rms"], 0)
            self.assertGreater(result["duration_seconds"], 0)

    def test_validate_only_rejects_silent_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio_path = root / "beat-001.wav"
            manifest_path = root / "narration_manifest.json"
            write_wav(audio_path, silent=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "language": "en",
                        "beats": [
                            {"id": "beat-001", "text": "Compare the values.", "audio_path": str(audio_path)}
                        ],
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    str(root),
                    "--manifest",
                    str(manifest_path),
                    "--validate-only",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            result = json.loads(manifest_path.read_text(encoding="utf-8"))["beats"][0]
            self.assertFalse(result["validation"]["passed"])
            self.assertIn("silent", " ".join(result["validation"]["errors"]).lower())


if __name__ == "__main__":
    unittest.main()
