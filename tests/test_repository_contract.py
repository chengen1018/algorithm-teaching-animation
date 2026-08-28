from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_repository.py"


class RepositoryContractTests(unittest.TestCase):
    def make_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        return root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(root), "--contracts-only"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_rejects_tracked_generated_artifact(self) -> None:
        root = self.make_repository()
        cache = root / "package" / "__pycache__" / "module.pyc"
        cache.parent.mkdir(parents=True)
        cache.write_bytes(b"generated")
        subprocess.run(["git", "-C", str(root), "add", str(cache)], check=True)

        result = self.run_checker(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("不允許追蹤的產生檔案", result.stdout)
        self.assertIn("package/__pycache__/module.pyc", result.stdout)

    def test_rejects_broken_local_markdown_link(self) -> None:
        root = self.make_repository()
        readme = root / "README.md"
        readme.write_text("[不存在的文件](docs/missing.md)\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(readme)], check=True)

        result = self.run_checker(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("失效的本機 Markdown 連結", result.stdout)
        self.assertIn("docs/missing.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
