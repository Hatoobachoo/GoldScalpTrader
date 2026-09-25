from pathlib import Path
import json, zipfile
import pytest
from gold_scalp_trader.persistence.backup import create_verified_checkpoint_backup
from gold_scalp_trader.persistence.local_recovery_package import create_recovery_package
from gold_scalp_trader.persistence.store import StateStore


def test_verified_checkpoint_and_recovery_package(tmp_path: Path):
    db = tmp_path / "state.db"
    store = StateStore(db)
    try:
        store.put("risk", "day", {"profile": "SMALL", "loss_locked": False})
        checkpoint = tmp_path / "runtime.checkpoint.json"
        status = create_verified_checkpoint_backup(store, checkpoint)
    finally:
        store.close()
    assert status.verified and status.sha256 and checkpoint.exists()
    package = create_recovery_package(checkpoint_path=checkpoint, output_zip=tmp_path / "recovery.zip", source_revision="abc123")
    assert package.secret_scan_passed and package.sha256
    with zipfile.ZipFile(package.package_path) as archive:
        manifest = json.loads(archive.read("recovery_manifest.json"))
        assert manifest["credentials_included"] is False
        assert manifest["restore_requires_fresh_broker_reconciliation"] is True
        assert manifest["source_revision"] == "abc123"


def test_recovery_package_rejects_probable_secret(tmp_path: Path):
    checkpoint = tmp_path / "bad.json"
    checkpoint.write_text('token=ghp_abcdefghijklmnopqrstuvwxyz123456', encoding="utf-8")
    with pytest.raises(ValueError, match="probable authority-bearing secret"):
        create_recovery_package(checkpoint_path=checkpoint, output_zip=tmp_path / "bad.zip")
