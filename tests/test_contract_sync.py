from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def test_document_code_contract_sync() -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/verify_contract_sync.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
