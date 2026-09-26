"""Exactly-once StrategyMemory observations."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from gold_scalp_trader.persistence.store import StateStore

NS = "strategy_learning_memory"


@dataclass(frozen=True, slots=True)
class LearningObservation:
    source_id: str
    family: str
    policy_version: str
    realized_r: float | None = None
    entry_efficiency: float | None = None
    capture_efficiency: float | None = None
    net_money: float | None = None
    close_origin: str | None = None
    position_ticket: int | None = None
    symbol: str | None = None
    opened_at: str | None = None
    closed_at: str | None = None
    opportunity_id: str | None = None
    episode_id: str | None = None
    trade_plan_id: str | None = None
    entry_reference: float | None = None
    m5_source_event_ids: tuple[str, ...] = ()
    m5_event_time: str | None = None
    timing_profile: str | None = None
    timing_policy_version: str | None = None
    timing_trigger_time: str | None = None
    m5_event_age_seconds: float | None = None
    m5_event_age_bars: int | None = None
    trigger_age_seconds: float | None = None
    chase_atr: float | None = None
    micro_extension_atr: float | None = None
    tags: tuple[str, ...] = ()


def save(store: StateStore, obs: LearningObservation) -> None:
    payload = asdict(obs)
    payload["tags"] = list(obs.tags)
    payload["m5_source_event_ids"] = list(obs.m5_source_event_ids)
    store.put(NS, obs.source_id, payload, allow_replace=False)


def _opt_float(value):
    return None if value is None else float(value)


def _opt_int(value):
    return None if value is None else int(value)


def _opt_str(value):
    return None if value is None else str(value)


def load(store: StateStore, source_id: str) -> LearningObservation | None:
    record = store.get(NS, source_id)
    if record is None:
        return None
    p = record.payload
    return LearningObservation(
        source_id=str(p["source_id"]),
        family=str(p["family"]),
        policy_version=str(p["policy_version"]),
        realized_r=_opt_float(p.get("realized_r")),
        entry_efficiency=_opt_float(p.get("entry_efficiency")),
        capture_efficiency=_opt_float(p.get("capture_efficiency")),
        net_money=_opt_float(p.get("net_money")),
        close_origin=_opt_str(p.get("close_origin")),
        position_ticket=_opt_int(p.get("position_ticket")),
        symbol=_opt_str(p.get("symbol")),
        opened_at=_opt_str(p.get("opened_at")),
        closed_at=_opt_str(p.get("closed_at")),
        opportunity_id=_opt_str(p.get("opportunity_id")),
        episode_id=_opt_str(p.get("episode_id")),
        trade_plan_id=_opt_str(p.get("trade_plan_id")),
        entry_reference=_opt_float(p.get("entry_reference")),
        m5_source_event_ids=tuple(str(x) for x in p.get("m5_source_event_ids", ())),
        m5_event_time=_opt_str(p.get("m5_event_time")),
        timing_profile=_opt_str(p.get("timing_profile")),
        timing_policy_version=_opt_str(p.get("timing_policy_version")),
        timing_trigger_time=_opt_str(p.get("timing_trigger_time")),
        m5_event_age_seconds=_opt_float(p.get("m5_event_age_seconds")),
        m5_event_age_bars=_opt_int(p.get("m5_event_age_bars")),
        trigger_age_seconds=_opt_float(p.get("trigger_age_seconds")),
        chase_atr=_opt_float(p.get("chase_atr")),
        micro_extension_atr=_opt_float(p.get("micro_extension_atr")),
        tags=tuple(str(x) for x in p.get("tags", ())),
    )


def count(store: StateStore) -> int:
    return len(store.list_records(NS))
