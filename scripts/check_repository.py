#!/usr/bin/env python3
"""執行不需要 Manim render 或 TTS 模型的快速 Repository 檢查。"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CHANGELOG.md",
    "KOKORO_SETUP.md",
    "docs/compatibility.md",
    "docs/releasing.md",
    "docs/roadmap.md",
    "manim-algorithm-animation-maker/SKILL.md",
)

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MEDIA_SUFFIXES = {".mp3", ".mp4", ".wav"}
GENERATED_DIRECTORIES = {"__pycache__", "audio", "media", "video"}
SECRET_NAMES = {".env", ".tts-config"}


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        check=True,
    )
    return [Path(item.decode()) for item in result.stdout.split(b"\0") if item]


def disallowed_tracked_files(root: Path) -> list[Path]:
    disallowed: list[Path] = []
    for path in tracked_files(root):
        if path.name in SECRET_NAMES:
            disallowed.append(path)
        elif path.suffix.lower() in MEDIA_SUFFIXES or path.suffix.lower() in {".pyc", ".pyo"}:
            disallowed.append(path)
        elif GENERATED_DIRECTORIES.intersection(path.parts):
            disallowed.append(path)
    return disallowed


def markdown_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.md") if ".git" not in path.parts]


def broken_markdown_links(root: Path) -> list[str]:
    broken: list[str] = []
    for document in markdown_files(root):
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            relative_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            destination = root / relative_target.lstrip("/") if target.startswith("/") else document.parent / relative_target
            if relative_target and not destination.exists():
                broken.append(f"{document.relative_to(root)} -> {target}")
    return broken


def contract_errors(root: Path) -> list[str]:
    errors: list[str] = []
    generated = disallowed_tracked_files(root)
    if generated:
        paths = "\n    ".join(str(path) for path in generated)
        errors.append(f"不允許追蹤的產生檔案：\n    {paths}")

    broken = broken_markdown_links(root)
    if broken:
        paths = "\n    ".join(broken)
        errors.append(f"失效的本機 Markdown 連結：\n    {paths}")
    return errors


def public_file_errors(root: Path) -> list[str]:
    errors = [f"缺少必要公開檔案：{path}" for path in REQUIRED_FILES if not (root / path).is_file()]
    skill = root / "manim-algorithm-animation-maker" / "SKILL.md"
    if skill.is_file() and "name: manim-algorithm-animation-maker" not in skill.read_text(encoding="utf-8"):
        errors.append("SKILL.md frontmatter 缺少正確的 Skill 名稱")
    return errors


def python_source_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for source in root.rglob("*.py"):
        if ".git" in source.parts or any(part.startswith(".") for part in source.relative_to(root).parts):
            continue
        try:
            ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        except (SyntaxError, UnicodeDecodeError) as error:
            errors.append(f"Python source 無法解析：{source.relative_to(root)}：{error}")
    return errors


def run_unit_tests(root: Path) -> int:
    suites = ("manim-algorithm-animation-maker/tests", "tests")
    for suite in suites:
        command = [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            suite,
            "-p",
            "test_*.py",
            "-v",
        ]
        if subprocess.run(command, cwd=root, check=False).returncode != 0:
            return 1
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--contracts-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = contract_errors(root)
    if not args.contracts_only:
        errors.extend(public_file_errors(root))
        errors.extend(python_source_errors(root))

    if errors:
        print("Repository 檢查失敗：")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.contracts_only and run_unit_tests(root) != 0:
        print("Repository 檢查失敗：單元測試未通過")
        return 1

    print("Repository 檢查通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
