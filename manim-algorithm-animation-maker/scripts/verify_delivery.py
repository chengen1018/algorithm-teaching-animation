from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class SceneOutput:
    order: int
    scene_class: str
    command: str
    exit_code: int
    path: Path


@dataclass
class MediaResult:
    path: Path
    probe_command: list[str]
    probe_exit_code: int
    width: int | None = None
    height: int | None = None
    frame_rate: float | None = None
    duration: float | None = None
    has_video: bool = False
    has_audio: bool = False
    errors: list[str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify rendered Manim delivery artifacts.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_cell(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1].strip()
    return value


def field(markdown: str, label: str) -> str:
    pattern = rf"^-\s*{re.escape(label)}:\s*(.+?)\s*$"
    match = re.search(pattern, markdown, flags=re.MULTILINE)
    if match is None:
        raise ValueError(f"render manifest is missing '{label}'")
    return clean_cell(match.group(1))


def parse_scene_outputs(markdown: str) -> list[SceneOutput]:
    lines = markdown.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.strip().startswith("|") and "Render order" in line and "Exit code" in line),
        None,
    )
    if header_index is None:
        raise ValueError("render manifest is missing the Scene Outputs table")

    outputs: list[SceneOutput] = []
    for line in lines[header_index + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = [clean_cell(cell) for cell in line.strip().split("|")[1:-1]]
        if len(cells) != 5:
            raise ValueError("Scene Outputs rows must contain five columns")
        outputs.append(
            SceneOutput(
                order=int(cells[0]),
                scene_class=cells[1],
                command=cells[2],
                exit_code=int(cells[3]),
                path=Path(cells[4]).expanduser().resolve(),
            )
        )
    if len(outputs) != 4 or [item.order for item in outputs] != [1, 2, 3, 4]:
        raise ValueError("Scene Outputs must contain render orders 1 through 4 exactly once")
    return outputs


def parse_frame_rate(value: object) -> float:
    if value in (None, "", "0/0"):
        return 0.0
    return float(Fraction(str(value)))


def probe_media(path: Path, ffprobe: str, profile: dict[str, object]) -> MediaResult:
    command = [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]
    result = MediaResult(path=path, probe_command=command, probe_exit_code=1, errors=[])
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    result.probe_exit_code = completed.returncode
    if completed.returncode != 0:
        result.errors.append(f"ffprobe failed: {completed.stderr.strip() or 'no error text'}")
        return result

    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        result.errors.append(f"ffprobe returned invalid JSON: {exc}")
        return result

    streams = data.get("streams") if isinstance(data.get("streams"), list) else []
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    result.has_video = bool(video_streams)
    result.has_audio = bool(audio_streams)
    if not result.has_video:
        result.errors.append("video stream is missing")
    if not result.has_audio:
        result.errors.append("audio stream is missing")

    if video_streams:
        video = video_streams[0]
        result.width = int(video.get("width", 0))
        result.height = int(video.get("height", 0))
        result.frame_rate = parse_frame_rate(video.get("avg_frame_rate") or video.get("r_frame_rate"))
        expected_width = int(profile["pixel_width"])
        expected_height = int(profile["pixel_height"])
        expected_rate = float(profile["frame_rate"])
        if (result.width, result.height) != (expected_width, expected_height):
            result.errors.append(
                f"resolution {result.width}x{result.height} does not match profile {expected_width}x{expected_height}"
            )
        if abs(result.frame_rate - expected_rate) > 0.01:
            result.errors.append(
                f"frame rate {result.frame_rate:.3f} does not match profile {expected_rate:.3f}"
            )

    format_data = data.get("format") if isinstance(data.get("format"), dict) else {}
    duration_value = format_data.get("duration")
    if duration_value in (None, "") and video_streams:
        duration_value = video_streams[0].get("duration")
    try:
        result.duration = float(duration_value)
    except (TypeError, ValueError):
        result.duration = 0.0
    if result.duration <= 0:
        result.errors.append("duration is missing or not positive")
    return result


def render_result(
    output: Path,
    passed: bool,
    source_hash: str | None,
    profile_hash: str | None,
    source_hash_matches: bool | None,
    profile_hash_matches: bool | None,
    media: list[MediaResult],
    decode_command: list[str] | None,
    decode_exit_code: int | None,
    scene_duration_total: float | None,
    combined_duration: float | None,
    duration_tolerance: float | None,
    findings: list[str],
) -> None:
    def status(value: bool | None) -> str:
        if value is None:
            return "NOT RUN"
        return "PASS" if value else "FAIL"

    lines = [
        "# Delivery Check Result",
        "",
        f"- Result: {'PASS' if passed else 'FAIL'}",
        f"- Source SHA-256: `{source_hash or 'unavailable'}`",
        f"- Render Profile SHA-256: `{profile_hash or 'unavailable'}`",
        f"- Combined decode exit code: `{decode_exit_code if decode_exit_code is not None else 'not-run'}`",
        "",
        "## Hash comparisons",
        f"- Source hash match: `{status(source_hash_matches)}`",
        f"- Render profile hash match: `{status(profile_hash_matches)}`",
        "",
        "## Duration comparison",
        f"- Scene duration total: `{f'{scene_duration_total:.3f}s' if scene_duration_total is not None else 'not-run'}`",
        f"- Combined duration: `{f'{combined_duration:.3f}s' if combined_duration is not None else 'not-run'}`",
        f"- Allowed difference: `{f'{duration_tolerance:.3f}s' if duration_tolerance is not None else 'not-run'}`",
        "",
        "## Commands",
    ]
    lines.extend(f"- ffprobe: `{shlex.join(item.probe_command)}`" for item in media)
    lines.append(
        f"- combined decode: `{shlex.join(decode_command) if decode_command is not None else 'not-run'}`"
    )
    lines.extend([
        "",
        "## Media",
        "| MP4 path | ffprobe exit | Streams | Resolution | Frame rate | Duration |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for item in media:
        streams = f"video={'yes' if item.has_video else 'no'}, audio={'yes' if item.has_audio else 'no'}"
        resolution = f"{item.width}x{item.height}" if item.width is not None and item.height is not None else "unknown"
        frame_rate = f"{item.frame_rate:.3f}" if item.frame_rate is not None else "unknown"
        duration = f"{item.duration:.3f}s" if item.duration is not None else "unknown"
        lines.append(f"| `{item.path}` | `{item.probe_exit_code}` | {streams} | {resolution} | {frame_rate} | {duration} |")
    lines.extend(["", "## Findings"])
    lines.extend([f"- {finding}" for finding in findings] or ["- None"])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    profile_path = Path(args.profile).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    findings: list[str] = []
    media_results: list[MediaResult] = []
    source_hash: str | None = None
    profile_hash: str | None = None
    decode_exit_code: int | None = None
    decode_command: list[str] | None = None
    source_hash_matches: bool | None = None
    profile_hash_matches: bool | None = None
    scene_duration_total: float | None = None
    combined_duration: float | None = None
    duration_tolerance: float | None = None

    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        for required in ("pixel_width", "pixel_height", "frame_rate", "renderer"):
            if required not in profile:
                raise ValueError(f"render profile is missing {required}")
        manifest = manifest_path.read_text(encoding="utf-8")
        scene_outputs = parse_scene_outputs(manifest)
        combined = Path(field(manifest, "Combined MP4 path")).expanduser().resolve()

        source_hash = sha256(source)
        profile_hash = sha256(profile_path)
        approved_source_hash = field(manifest, "Approved Code SHA-256")
        rendered_source_hash = field(manifest, "Rendered Source Code SHA-256")
        manifest_profile_path = Path(field(manifest, "Render Profile path")).expanduser().resolve()
        manifest_profile_hash = field(manifest, "Render Profile SHA-256")
        manifest_source_path = Path(field(manifest, "Code path")).expanduser().resolve()
        concat_exit_code = int(field(manifest, "Concat exit code"))

        if manifest_source_path != source:
            findings.append(f"manifest code path does not match source: {manifest_source_path}")
        source_hash_matches = approved_source_hash == source_hash and rendered_source_hash == source_hash
        if not source_hash_matches:
            findings.append("source hash does not match approved/rendered manifest hashes")
        if manifest_profile_path != profile_path:
            findings.append(f"manifest render profile path does not match: {manifest_profile_path}")
        profile_hash_matches = manifest_profile_hash == profile_hash
        if not profile_hash_matches:
            findings.append("render profile hash does not match manifest")
        for scene in scene_outputs:
            if scene.exit_code != 0:
                findings.append(f"{scene.scene_class} render exit code is {scene.exit_code}")
        if concat_exit_code != 0:
            findings.append(f"concat exit code is {concat_exit_code}")

        paths = [scene.path for scene in scene_outputs] + [combined]
        for path in paths:
            item = probe_media(path, args.ffprobe, profile)
            media_results.append(item)
            findings.extend(f"{path}: {error}" for error in item.errors or [])

        if len(media_results) == 5 and all(item.duration is not None for item in media_results):
            scene_duration_total = sum(item.duration or 0.0 for item in media_results[:4])
            combined_duration = media_results[4].duration or 0.0
            duration_tolerance = max(0.25, 2.0 / float(profile["frame_rate"]))
            if abs(scene_duration_total - combined_duration) > duration_tolerance:
                findings.append(
                    f"combined duration {combined_duration:.3f}s does not match Scene total {scene_duration_total:.3f}s"
                )

        decode_command = [args.ffmpeg, "-v", "error", "-i", str(combined), "-f", "null", "-"]
        decode = subprocess.run(
            decode_command,
            text=True,
            capture_output=True,
            check=False,
        )
        decode_exit_code = decode.returncode
        if decode.returncode != 0:
            findings.append(f"combined decode failed: {decode.stderr.strip() or 'no error text'}")
    except Exception as exc:
        findings.append(str(exc))

    passed = not findings
    render_result(
        output,
        passed,
        source_hash,
        profile_hash,
        source_hash_matches,
        profile_hash_matches,
        media_results,
        decode_command,
        decode_exit_code,
        scene_duration_total,
        combined_duration,
        duration_tolerance,
        findings,
    )
    print(f"[delivery-check] {'PASS' if passed else 'FAIL'}: {output}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
