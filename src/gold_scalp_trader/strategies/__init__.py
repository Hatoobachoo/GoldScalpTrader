"""Market-first setup detection and strategy isolation."""
from .floor import StrategyPolicy
from .setup_detector import SetupRegistry, detect
from .isolation import IsolationResult, apply
__all__=["StrategyPolicy","SetupRegistry","IsolationResult","detect","apply"]
