"""Deterministic execution-cost stress scenarios for research evidence."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StressScenario:
    spread_multiplier: float = 1.0
    slippage_add: float = 0.0
    latency_ms: int = 0
    adverse_entry_drift: float = 0.0

    def __post_init__(self) -> None:
        if self.spread_multiplier <= 0:
            raise ValueError("spread_multiplier must be positive")
        if self.slippage_add < 0 or self.latency_ms < 0 or self.adverse_entry_drift < 0:
            raise ValueError("stress dimensions cannot be negative")

@dataclass(frozen=True, slots=True)
class StressedExecution:
    spread: float
    slippage_allowance: float
    latency_ms: int
    adverse_entry_drift: float


def apply_execution_stress(*, base_spread: float, base_slippage_allowance: float, scenario: StressScenario) -> StressedExecution:
    if base_spread < 0 or base_slippage_allowance < 0:
        raise ValueError("base execution costs cannot be negative")
    return StressedExecution(
        spread=base_spread * scenario.spread_multiplier,
        slippage_allowance=base_slippage_allowance + scenario.slippage_add,
        latency_ms=scenario.latency_ms,
        adverse_entry_drift=scenario.adverse_entry_drift,
    )
