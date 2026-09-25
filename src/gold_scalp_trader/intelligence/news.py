"""Soft-only scheduled-event and macro context."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from gold_scalp_trader.domain.enums import ProviderHealth

@dataclass(frozen=True, slots=True)
class NewsEvent:
    event_id: str; title: str; currency: str; scheduled_at: datetime; tier: str; provider: str

@dataclass(frozen=True, slots=True)
class NewsContext:
    provider_health: ProviderHealth; fetched_at: datetime | None; events: tuple[NewsEvent,...]=(); source: str | None=None
    @property
    def hard_trading_permission(self) -> None:
        return None
