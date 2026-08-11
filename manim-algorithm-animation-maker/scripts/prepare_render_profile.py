from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_FRAME_WIDTH = 14.2222222222
DEFAULT_FRAME_HEIGHT = 8.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a verified Manim render_profile.json.")
    parser.add_argument("--project-root", required=True, help="Absolute animation project root.")
    parser.add_argument("--python", required=True, dest="python_executable", help="Python that imports Manim.")
    parser.add_argument("--font", required=True, help="Exact installed font family name.")
    parser.add_argument("--output", help="Output path. Defaults to <project-root>/render_profile.json.")
    parser.add_argument("--pixel-width", type=int, default=1920)
    parser.add_argument("--pixel-height", type=int, default=1080)
    parser.add_argument("--frame-rate", type=int, default=60)
    parser.add_argument("--renderer", choices=("cairo", "opengl"), default="cairo")
    parser.add_argument("--frame-width", type=float, default=DEFAULT_FRAME_WIDTH)
    parser.add_argument("--frame-height", type=float, default=DEFAULT_FRAME_HEIGHT)
    return parser.parse_args()


def probe_runtime(python_executable: Path) -> dict[str, object]:
    probe = (
        "import json, manim, manimpango; "
        "print(json.dumps({'manim_version': manim.__version__, 'fonts': list(manimpango.list_fonts())}))"
    )
    completed = subprocess.run(
        [str(python_executable), "-c", probe],
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "unknown import error"
        raise RuntimeError(f"Manim runtime probe failed: {detail}")

    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("Manim runtime probe returned no JSON output")
    try:
        result = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Manim runtime probe returned invalid JSON: {lines[-1]}") from exc
    if not isinstance(result.get("manim_version"), str) or not isinstance(result.get("fonts"), list):
        raise RuntimeError("Manim runtime probe omitted manim_version or fonts")
    return result


def positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def main() -> int:
    args = parse_args()
    try:
        project_root = Path(args.project_root).expanduser().resolve()
        if not project_root.is_dir():
            raise ValueError(f"project root is not a directory: {project_root}")

        python_executable = Path(args.python_executable).expanduser().resolve()
        if not python_executable.is_file():
            raise ValueError(f"Manim Python does not exist: {python_executable}")

        for name, value in (
            ("pixel_width", args.pixel_width),
            ("pixel_height", args.pixel_height),
            ("frame_rate", args.frame_rate),
            ("frame_width", args.frame_width),
            ("frame_height", args.frame_height),
        ):
            positive(name, value)

        runtime = probe_runtime(python_executable)
        font_by_case = {str(font).casefold(): str(font) for font in runtime["fonts"]}
        canonical_font = font_by_case.get(args.font.casefold())
        if canonical_font is None:
            raise ValueError(f"Font is not available to ManimPango: {args.font}")

        profile = {
            "schema_version": 1,
            "pixel_width": args.pixel_width,
            "pixel_height": args.pixel_height,
            "frame_rate": args.frame_rate,
            "renderer": args.renderer,
            "frame_width": args.frame_width,
            "frame_height": args.frame_height,
            "font": canonical_font,
            "python_executable": str(python_executable),
            "manim_version": runtime["manim_version"],
        }
        output = Path(args.output).expanduser().resolve() if args.output else project_root / "render_profile.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        print(f"[render-profile] wrote {output}")
        print(f"[render-profile] SHA-256 {digest}")
        return 0
    except Exception as exc:
        print(f"[render-profile] failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
