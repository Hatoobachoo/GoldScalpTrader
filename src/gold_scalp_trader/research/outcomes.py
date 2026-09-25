"""Typed research outcomes kept separate from broker/account authority."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from gold_scalp_trader.domain.enums import StrategyMode


@dataclass(frozen=True, slots=True)
class ResearchOutcome:
    episode_id: str
    family: str
    mode: StrategyMode
    qualified: bool
    executed: bool
    net_r: float | None = None
    mfe_r: float | None = None
    mae_r: float | None = None
    entry_efficiency: float | None = None
    capture_efficiency: float | None = None
    exit_efficiency: float | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.episode_id.strip() or not self.family.strip():
            raise ValueError("episode_id and family are required")
        if self.executed and self.mode is not StrategyMode.ACTIVE_EXECUTION:
            raise ValueError("shadow/research outcome cannot be marked as broker executed")
        for name in ("net_r", "mfe_r", "mae_r"):
            value = getattr(self, name)
            if value is not None and not isfinite(float(value)):
                raise ValueError(f"{name} must be finite when present")
        for name in ("entry_efficiency", "capture_efficiency", "exit_efficiency"):
            value = getattr(self, name)
            if value is not None and (not isfinite(float(value)) or not 0.0 <= float(value) <= 1.0):
                raise ValueError(f"{name} must be within 0..1 when present")
