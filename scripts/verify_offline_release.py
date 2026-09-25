"""Local offline release verifier.

Runs only local deterministic checks. It deliberately does not claim connected
Exness/DEMO certification.
"""
from __future__ import annotations
import compileall
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> bool:
    print(f"\n[{label}] {' '.join(command)}")
    completed = subprocess.run(command, cwd=ROOT, check=False)
    print(f"{label}: {'PASS' if completed.returncode == 0 else 'FAIL'}")
    return completed.returncode == 0


def main() -> int:
    checks: list[tuple[str, bool]] = []
    checks.append(("compileall", compileall.compile_dir(str(ROOT / "src"), quiet=1) and compileall.compile_dir(str(ROOT / "graphical_dashboard"), quiet=1)))
    checks.append(("documents", run("documents", [sys.executable, "scripts/verify_documents_manual.py"])))
    checks.append(("secrets", run("secrets", [sys.executable, "scripts/scan_financial_secrets.py", "."])))
    checks.append(("pytest", run("pytest", [sys.executable, "-m", "pytest", "-q"])))
    failed = [name for name, passed in checks if not passed]
    print("\nOFFLINE RELEASE AUDIT")
    for name, passed in checks:
        print(f"  {name:<12} {'PASS' if passed else 'FAIL'}")
    if failed:
        print(f"OFFLINE STATUS: FAIL ({', '.join(failed)})")
        return 1
    print("OFFLINE STATUS: PASS")
    print("CONNECTED DEMO / EXNESS CERTIFICATION: STILL REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
