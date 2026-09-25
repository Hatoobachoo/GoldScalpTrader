"""Deterministic serial analytical scheduler; concurrency is profiling-driven."""
from .floor import StrategyPolicy
from .setup_detector import SetupRegistry,detect
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot

def run(snapshot: IntelligenceSnapshot, policy: StrategyPolicy | None=None)->SetupRegistry:
    return detect(snapshot,policy)
