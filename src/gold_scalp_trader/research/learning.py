"""Exactly-once StrategyMemory observations."""
from __future__ import annotations
from dataclasses import dataclass,asdict
from gold_scalp_trader.persistence.store import StateStore
NS="strategy_learning_memory"
@dataclass(frozen=True,slots=True)
class LearningObservation:
    source_id:str; family:str; policy_version:str; realized_r:float|None; entry_efficiency:float|None; capture_efficiency:float|None; tags:tuple[str,...]=()
def save(store:StateStore,obs:LearningObservation)->None:
    store.put(NS,obs.source_id,{**asdict(obs),"tags":list(obs.tags)},allow_replace=False)
def count(store:StateStore)->int:return len(store.list_records(NS))
