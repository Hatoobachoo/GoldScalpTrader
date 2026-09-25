"""Finite domain states shared across GoldScalpTrader.

This module has no broker authority. It defines stable vocabulary so that
UNKNOWN/UNAVAILABLE states cannot be silently collapsed into False/zero.
"""
from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class RuntimeMode(StrEnum):
    DRY_RUN = "DRY_RUN"
    DEMO = "DEMO"
    REAL = "REAL"


class Timeframe(StrEnum):
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"


class Direction(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


class DataQuality(StrEnum):
    HEALTHY = "HEALTHY"
    INSUFFICIENT = "INSUFFICIENT"
    STALE = "STALE"
    SPARSE = "SPARSE"
    CORRUPT = "CORRUPT"
    UNKNOWN = "UNKNOWN"


class StrategyFamily(StrEnum):
    TREND_PULLBACK_CONTINUATION = "TREND_PULLBACK_CONTINUATION"
    BREAKOUT_EXPANSION = "BREAKOUT_EXPANSION"
    BREAKOUT_RETEST_CONTINUATION = "BREAKOUT_RETEST_CONTINUATION"
    LIQUIDITY_SWEEP_REVERSAL = "LIQUIDITY_SWEEP_REVERSAL"
    FAILED_BREAKOUT_REVERSAL = "FAILED_BREAKOUT_REVERSAL"
    COMPRESSION_EXPANSION = "COMPRESSION_EXPANSION"


class StrategyMode(StrEnum):
    ACTIVE_EXECUTION = "ACTIVE_EXECUTION"
    SHADOW_ONLY = "SHADOW_ONLY"
    RESEARCH_ONLY = "RESEARCH_ONLY"


class SetupQualification(StrEnum):
    QUALIFIED_BUY = "QUALIFIED_BUY"
    QUALIFIED_SELL = "QUALIFIED_SELL"
    POSSIBLE = "POSSIBLE"
    NOT_PRESENT = "NOT_PRESENT"
    UNKNOWN = "UNKNOWN"


class EvidenceRole(StrEnum):
    REQUIRED_FOR_FAMILY = "REQUIRED_FOR_FAMILY"
    STRONG_SUPPORT = "STRONG_SUPPORT"
    OPTIONAL_SUPPORT = "OPTIONAL_SUPPORT"
    OPPOSITION = "OPPOSITION"
    NOT_RELEVANT = "NOT_RELEVANT"
    UNKNOWN = "UNKNOWN"


class StructureState(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    RANGE = "RANGE"
    TRANSITION = "TRANSITION"
    UNDETERMINED = "UNDETERMINED"


class BreakEvent(StrEnum):
    NONE = "NONE"
    PROBE = "PROBE"
    QUALIFIED_BREAK = "QUALIFIED_BREAK"
    BOS = "BOS"
    MSS_CANDIDATE = "MSS_CANDIDATE"
    MSS = "MSS"
    FAILED_BREAK = "FAILED_BREAK"


class OpportunityState(StrEnum):
    DISCOVERED = "DISCOVERED"
    ARMED = "ARMED"
    WAITING = "WAITING"
    READY = "READY"
    TRIGGERED = "TRIGGERED"
    MISSED = "MISSED"
    INVALIDATED = "INVALIDATED"


class TimingOutcome(StrEnum):
    READY_BUY = "READY_BUY"
    READY_SELL = "READY_SELL"
    WAIT = "WAIT"
    MISSED = "MISSED"
    INVALID = "INVALID"


class RiskProfile(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    NORMAL = "NORMAL"


class RiskDecision(StrEnum):
    PASS = "PASS"
    BLOCK = "BLOCK"
    UNKNOWN = "UNKNOWN"


class MarketState(StrEnum):
    OPEN = "OPEN"
    PRE_CLOSE = "PRE_CLOSE"
    CLOSED = "CLOSED"
    REOPEN_WARMUP = "REOPEN_WARMUP"
    UNKNOWN = "UNKNOWN"


class GateState(StrEnum):
    ALLOW = "ALLOW"
    BLOCKED = "BLOCKED"
    NOT_EVALUATED = "NOT_EVALUATED"
    UNKNOWN = "UNKNOWN"


class ExecutionAction(StrEnum):
    OPEN = "OPEN"
    MODIFY = "MODIFY"
    CLOSE = "CLOSE"


class IntentState(StrEnum):
    CREATED = "CREATED"
    APPROVED = "APPROVED"
    SUBMITTING = "SUBMITTING"
    ACCEPTED_UNKNOWN = "ACCEPTED_UNKNOWN"
    ACCEPTED_VERIFIED = "ACCEPTED_VERIFIED"
    FAILED = "FAILED"


class ManagementAction(StrEnum):
    HOLD = "HOLD"
    PROTECT = "PROTECT"
    TRAIL = "TRAIL"
    RUNNER = "RUNNER"
    EXIT = "EXIT"


class ProviderHealth(StrEnum):
    VERIFIED = "VERIFIED"
    DEGRADED = "DEGRADED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
