"""Compatibility tests for the canonical config package."""
from gold_scalp_trader.config import Settings, validate_settings

def test_legacy_import_path_resolves_canonical_settings_package():
    settings=Settings(); validate_settings(settings); assert settings.max_open_positions==1
