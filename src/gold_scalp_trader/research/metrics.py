"""Deterministic research metrics for active/shadow opportunity analysis."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .outcomes import ResearchOutcome


@dataclass(frozen=True, slots=True)
class ResearchMetrics:
    samples: int
    qualified: int
    executed: int
    wins: int
    losses: int
    net_r: float
    average_r: float | None
    win_rate: float | None
    profit_factor: float | None
    opportunity_capture_rate: float | None
    average_entry_efficiency: float | None
    average_capture_efficiency: float | None
    average_exit_efficiency: float | None


def _average(values: list[float]) -> float | None:
    return None if not values else sum(values) / len(values)


def summarize(outcomes: Iterable[ResearchOutcome]) -> ResearchMetrics:
    rows = tuple(outcomes)
    qualified = sum(1 for row in rows if row.qualified)
    executed_rows = tuple(row for row in rows if row.executed)
    r_values = [float(row.net_r) for row in executed_rows if row.net_r is not None]
    wins = sum(1 for value in r_values if value > 0)
    losses = sum(1 for value in r_values if value < 0)
    gross_profit = sum(value for value in r_values if value > 0)
    gross_loss = abs(sum(value for value in r_values if value < 0))
    profit_factor = None if gross_loss == 0 else gross_profit / gross_loss
    entry = [float(row.entry_efficiency) for row in rows if row.entry_efficiency is not None]
    capture = [float(row.capture_efficiency) for row in rows if row.capture_efficiency is not None]
    exit_values = [float(row.exit_efficiency) for row in rows if row.exit_efficiency is not None]
    return ResearchMetrics(
        samples=len(rows),
        qualified=qualified,
        executed=len(executed_rows),
        wins=wins,
        losses=losses,
        net_r=sum(r_values),
        average_r=_average(r_values),
        win_rate=None if not r_values else wins / len(r_values),
        profit_factor=profit_factor,
        opportunity_capture_rate=None if qualified == 0 else len(executed_rows) / qualified,
        average_entry_efficiency=_average(entry),
        average_capture_efficiency=_average(capture),
        average_exit_efficiency=_average(exit_values),
    )
