"""Exactly-once StrategyMemory observations."""
from __future__ import annotations
from dataclasses import asdict,dataclass
from gold_scalp_trader.persistence.store import StateStore
NS="strategy_learning_memory"
@dataclass(frozen=True,slots=True)
class LearningObservation:
    source_id:str
    family:str
    policy_version:str
    realized_r:float|None=None
    entry_efficiency:float|None=None
    capture_efficiency:float|None=None
    net_money:float|None=None
    close_origin:str|None=None
    position_ticket:int|None=None
    symbol:str|None=None
    opened_at:str|None=None
    closed_at:str|None=None
    tags:tuple[str,...]=()
def save(store:StateStore,obs:LearningObservation)->None:
    store.put(NS,obs.source_id,{**asdict(obs),"tags":list(obs.tags)},allow_replace=False)
def load(store:StateStore,source_id:str)->LearningObservation|None:
    record=store.get(NS,source_id)
    if record is None:return None
    p=record.payload
    return LearningObservation(source_id=str(p["source_id"]),family=str(p["family"]),policy_version=str(p["policy_version"]),realized_r=None if p.get("realized_r") is None else float(p["realized_r"]),entry_efficiency=None if p.get("entry_efficiency") is None else float(p["entry_efficiency"]),capture_efficiency=None if p.get("capture_efficiency") is None else float(p["capture_efficiency"]),net_money=None if p.get("net_money") is None else float(p["net_money"]),close_origin=None if p.get("close_origin") is None else str(p["close_origin"]),position_ticket=None if p.get("position_ticket") is None else int(p["position_ticket"]),symbol=None if p.get("symbol") is None else str(p["symbol"]),opened_at=None if p.get("opened_at") is None else str(p["opened_at"]),closed_at=None if p.get("closed_at") is None else str(p["closed_at"]),tags=tuple(str(x) for x in p.get("tags",())))
def count(store:StateStore)->int:return len(store.list_records(NS))
