"""Optional confluence DTOs; never a universal system gate."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConfluenceReport:
    trendline: str = "UNKNOWN"
    fibonacci: str = "UNKNOWN"
    poc: float | None = None
    fvg: str = "UNKNOWN"
    order_block: str = "UNKNOWN"
    coverage: float = 0.0
