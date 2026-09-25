"""Durable actual/shadow/missed/blocked research episodes."""
from __future__ import annotations
from dataclasses import dataclass,asdict
from gold_scalp_trader.persistence.store import StateStore
NS="research_episode_journal"
@dataclass(frozen=True,slots=True)
class EpisodeRecord:
    episode_id:str; evidence_class:str; active_family:str|None; shadow_families:tuple[str,...]; outcome_r:float|None; reason:str
def append(store:StateStore,record:EpisodeRecord)->None:
    p=asdict(record); p["shadow_families"]=list(record.shadow_families); store.append_event(NS,record.episode_id,p)
