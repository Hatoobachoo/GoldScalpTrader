"""Bounded candidate discovery from recurring evidence clusters."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DiscoveryStatus:
    state:str; eligible_clusters:int; candidates:int; suppressed:int
def health(eligible:int,candidates:int,suppressed:int)->DiscoveryStatus:
    return DiscoveryStatus("HEALTHY" if eligible==candidates+suppressed else "DEGRADED",eligible,candidates,suppressed)
