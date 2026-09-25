"""Create a verified local runtime recovery package.

Usage:
    python scripts/create_local_recovery_package.py state/runtime.db recovery/runtime.zip [source_revision]

The live runtime should be stopped before this operator tool is used.
Credentials are never added to the package.
"""
from __future__ import annotations
import sys
from pathlib import Path
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.persistence.backup import create_verified_checkpoint_backup
from gold_scalp_trader.persistence.local_recovery_package import create_recovery_package


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4}:
        print("usage: create_local_recovery_package.py <state.db> <output.zip> [source_revision]")
        return 2
    db_path, output_zip = argv[1], argv[2]
    revision = argv[3] if len(argv) == 4 else None
    checkpoint = Path(output_zip).with_suffix(".checkpoint.json")
    store = StateStore(db_path)
    try:
        status = create_verified_checkpoint_backup(store, checkpoint)
    finally:
        store.close()
    package = create_recovery_package(checkpoint_path=status.path, output_zip=output_zip, source_revision=revision)
    print(f"checkpoint verified: {status.path}")
    print(f"package: {package.package_path}")
    print(f"package sha256: {package.sha256}")
    print("credentials included: NO")
    print("fresh MT5 reconciliation required after restore: YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
