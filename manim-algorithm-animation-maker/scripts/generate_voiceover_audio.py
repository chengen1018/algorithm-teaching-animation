from __future__ import annotations

import argparse
import audioop
import json
import subprocess
import sys
import wave
from pathlib import Path


LANGUAGE_SETTINGS = {
    "en": {"lang_code": "a", "voice": "af_heart"},
    "zh": {"lang_code": "z", "voice": "zm_yunxi"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and validate beat-level Kokoro WAV files.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("language") not in LANGUAGE_SETTINGS:
        raise ValueError("manifest language must be 'zh' or 'en'")
    beats = data.get("beats")
    if not isinstance(beats, list) or not beats:
        raise ValueError("manifest beats must be a non-empty list")
    for index, beat in enumerate(beats, start=1):
        if not isinstance(beat, dict):
            raise ValueError(f"beat {index} must be an object")
        for field in ("id", "text", "audio_path"):
            if not isinstance(beat.get(field), str) or not beat[field].strip():
                raise ValueError(f"beat {index} is missing {field}")
        if not Path(beat["audio_path"]).is_absolute():
            raise ValueError(f"beat {beat['id']} audio_path must be absolute")
    return data


def parse_tts_python(config_path: Path) -> Path:
    if not config_path.is_file():
        raise ValueError(f"TTS config not found: {config_path}")
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("TTS_PYTHON="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            path = Path(value).expanduser().resolve()
            if not path.is_file():
                raise ValueError(f"TTS_PYTHON does not exist: {path}")
            return path
    raise ValueError(f"TTS_PYTHON is missing from {config_path}")


def generate_audio(manifest: dict[str, object]) -> None:
    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline
    except Exception as exc:
        raise RuntimeError(f"Kokoro environment is unavailable: {exc}") from exc

    settings = LANGUAGE_SETTINGS[str(manifest["language"])]
    voice = str(manifest.get("voice") or settings["voice"])
    speed = float(manifest.get("speed", 1.0))
    pipeline = KPipeline(lang_code=settings["lang_code"])

    for beat in manifest["beats"]:
        audio_path = Path(beat["audio_path"])
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        chunks = []
        for _graphemes, _phonemes, audio in pipeline(beat["text"], voice=voice, speed=speed):
            chunks.append(np.asarray(audio, dtype=np.float32))
        if not chunks:
            raise RuntimeError(f"Kokoro returned no audio for {beat['id']}")
        samples = np.concatenate(chunks)
        sf.write(str(audio_path), samples, 24000, subtype="PCM_16")


def validate_wav(path: Path, text: str) -> dict[str, object]:
    errors: list[str] = []
    sample_rate = 0
    channels = 0
    duration = 0.0
    peak = 0.0
    rms = 0.0
    frames = b""
    sample_width = 0

    try:
        with wave.open(str(path), "rb") as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            frame_count = wav_file.getnframes()
            frames = wav_file.readframes(frame_count)
            duration = frame_count / sample_rate if sample_rate else 0.0
    except Exception as exc:
        errors.append(f"audio is not a decodable PCM WAV: {exc}")

    if not errors:
        if not frames or duration <= 0:
            errors.append("audio is empty")
        if channels <= 0 or sample_rate <= 0 or sample_width not in {1, 2, 3, 4}:
            errors.append("audio metadata is invalid")
        if frames and sample_width in {1, 2, 3, 4}:
            max_amplitude = float((1 << (sample_width * 8 - 1)) - 1)
            peak = audioop.max(frames, sample_width) / max_amplitude
            rms = audioop.rms(frames, sample_width) / max_amplitude
            if peak <= 1e-4 or rms <= 1e-5:
                errors.append("audio is silent")
        maximum_duration = max(15.0, len(text.strip()) * 2.0)
        if duration < 0.1 or duration > maximum_duration:
            errors.append(f"audio duration {duration:.3f}s is outside the expected range")

    return {
        "duration_seconds": round(duration, 6),
        "sample_rate": sample_rate,
        "channels": channels,
        "peak": round(peak, 6),
        "rms": round(rms, 6),
        "validation": {"passed": not errors, "errors": errors},
    }


def validate_manifest_audio(manifest: dict[str, object]) -> bool:
    passed = True
    for beat in manifest["beats"]:
        result = validate_wav(Path(beat["audio_path"]), beat["text"])
        beat.update(result)
        passed = passed and bool(result["validation"]["passed"])
    return passed


def write_manifest(path: Path, manifest: dict[str, object]) -> None:
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    try:
        manifest = load_manifest(manifest_path)
        if not args.validate_only and not args.worker:
            tts_python = parse_tts_python(project_root / ".tts-config")
            command = [
                str(tts_python),
                str(Path(__file__).resolve()),
                "--project-root",
                str(project_root),
                "--manifest",
                str(manifest_path),
                "--worker",
            ]
            completed = subprocess.run(command, check=False)
            return completed.returncode

        if args.worker:
            generate_audio(manifest)
        passed = validate_manifest_audio(manifest)
        write_manifest(manifest_path, manifest)
        print(f"[voiceover] validated {len(manifest['beats'])} beat audio files")
        return 0 if passed else 1
    except Exception as exc:
        print(f"[voiceover] failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
