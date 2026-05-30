import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNER = REPO_ROOT / "tools" / "public_safety_scan.py"


def run_scan(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), str(root), *args],
        check=False,
        text=True,
        capture_output=True,
    )


class PublicSafetyScanTests(unittest.TestCase):
    def test_clean_file_returns_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Public project notes.\n", encoding="utf-8")

            result = run_scan(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Status: OK", result.stdout)

    def test_fake_api_key_or_private_path_returns_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "/opt/" + "diviper" + "-stack/runtime"
            fake_key = "OPENAI_API_KEY=" + "sk-" + "fake1234567890"
            (root / "leak.md").write_text(
                f"{fake_key}\nDo not copy {private_path}\n",
                encoding="utf-8",
            )

            result = run_scan(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("Status: BLOCKER", result.stdout)
            self.assertIn("likely real credential-style value", result.stdout)
            self.assertIn("private stack", result.stdout)

    def test_safety_warning_text_returns_warning_not_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "guide.md").write_text(
                "Do not expose secrets in public documentation.\n",
                encoding="utf-8",
            )

            result = run_scan(root)

            self.assertEqual(result.returncode, 0)
            self.assertIn("Status: WARNING", result.stdout)
            self.assertIn("[WARNING]", result.stdout)
            self.assertNotIn("[BLOCKER]", result.stdout)

    def test_strict_fails_on_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "guide.md").write_text(
                "Do not publish tokens in examples.\n",
                encoding="utf-8",
            )

            result = run_scan(root, "--strict")

            self.assertEqual(result.returncode, 1)
            self.assertIn("Status: WARNING", result.stdout)

    def test_json_output_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Clean notes.\n", encoding="utf-8")

            result = run_scan(root, "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "OK")
            self.assertEqual(payload["blockers"], 0)
            self.assertEqual(payload["warnings"], 0)

    def test_ignored_directories_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ignored = root / "node_modules"
            ignored.mkdir()
            fake_key = "OPENAI_API_KEY=" + "sk-" + "ignored1234567890"
            (ignored / "leak.md").write_text(fake_key + "\n", encoding="utf-8")
            (root / "README.md").write_text("Clean notes.\n", encoding="utf-8")

            result = run_scan(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Status: OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
