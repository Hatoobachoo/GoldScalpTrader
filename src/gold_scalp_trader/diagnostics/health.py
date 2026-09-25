"""Read-only health DTOs."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    component: str
    healthy: bool
    state: str
    reason: str = ""
