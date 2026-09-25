"""Hard account-mode verification kept inside the normalized MT5 read boundary."""
from __future__ import annotations

from typing import Any


def _field(obj: Any, name: str, default: Any = None) -> Any:
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def demo_account_verified(api: Any) -> bool:
    """Fail closed unless MT5 explicitly reports ACCOUNT_TRADE_MODE_DEMO."""
    raw = api.account_info()
    if raw is None:
        return False
    mode = _field(raw, "trade_mode", None)
    if mode is None:
        return False

    demo_constant = getattr(api, "ACCOUNT_TRADE_MODE_DEMO", 0)
    if mode == demo_constant:
        return True
    if isinstance(mode, str):
        return mode.strip().upper() in {"DEMO", "ACCOUNT_TRADE_MODE_DEMO"}
    return False
