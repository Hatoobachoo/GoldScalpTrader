from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from gold_scalp_trader.domain.enums import (
    Direction,
    SetupQualification,
    StrategyFamily,
    StrategyMode,
    Timeframe,
    TimingOutcome,
)
from gold_scalp_trader.domain.market import Candle
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.persistence.store import StateStore
from gold_scalp_trader.research.outcomes import SHADOW_OUTCOME_NS
from gold_scalp_trader.research.shadow_runtime import PLAN_NS, TERMINAL_NS, record_shadow_runtime
from gold_scalp_trader.strategies.isolation import IsolatedCandidate

UTC = timezone.utc
NOW = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)


class Market:
    def __init__(self, captured_at, m1=()):
        self.captured_at = captured_at
        self.quote = SimpleNamespace(spread=0.20)
        self._m1 = tuple(m1)

    def series(self, timeframe):
        return self._m1 if timeframe is Timeframe.M1 else ()


def _candidate():
    return SetupCandidate(
        candidate_id="SET-shadow",
        family=StrategyFamily.BREAKOUT_RETEST_CONTINUATION,
        qualification=SetupQualification.QUALIFIED_BUY,
        direction=Direction.BUY,
        score=0.8,
        coverage=1.0,
        source_event_ids=("M5-EVENT-1",),
        reasons=("qualified shadow setup",),
        m5_event_time=NOW - timedelta(minutes=5),
        preferred_m1_profile="CONTINUATION",
        policy_version="POLICY-1",
    )


def _result(market):
    isolated = IsolatedCandidate(_candidate(), StrategyMode.SHADOW_ONLY)
    cycle = SimpleNamespace(
        intelligence=SimpleNamespace(market=market),
        isolation=SimpleNamespace(candidates=(isolated,)),
    )
    return SimpleNamespace(cycle=cycle)


def test_shadow_episode_freezes_once_and_resolves_only_from_future_path(monkeypatch):
    import gold_scalp_trader.research.shadow_runtime as shadow_runtime

    monkeypatch.setattr(
        shadow_runtime,
        "timing_evaluate",
        lambda opportunity, snapshot: SimpleNamespace(outcome=TimingOutcome.READY_BUY),
    )
    monkeypatch.setattr(
        shadow_runtime,
        "build_trade_plan",
        lambda opportunity, timing, snapshot: SimpleNamespace(
            entry_reference=100.0,
            initial_sl=99.0,
            primary_target=101.0,
        ),
    )

    store = StateStore()
    created, resolved = record_shadow_runtime(store, _result(Market(NOW)))
    assert (created, resolved) == (1, 0)
    plans = store.list_records(PLAN_NS)
    assert len(plans) == 1
    plan_payload = plans[0].payload["plan"]
    assert plan_payload["cost_r"] == 0.2
    assert plan_payload["entry_time_iso"] == NOW.isoformat()
    assert plans[0].payload["broker_authority"] == "NONE"

    # The only outcome candle begins after the frozen entry timestamp. It hits
    # the hypothetical target and therefore resolves research evidence.
    future = Candle(Timeframe.M1, NOW + timedelta(minutes=1), 100.1, 101.2, 100.0, 101.0, 50)
    created2, resolved2 = record_shadow_runtime(
        store,
        _result(Market(NOW + timedelta(minutes=2), (future,))),
    )
    assert (created2, resolved2) == (0, 1)
    assert store.list_records(PLAN_NS) == ()
    terminals = store.list_records(TERMINAL_NS)
    assert len(terminals) == 1
    assert terminals[0].payload["status"] == "TARGET"
    assert terminals[0].payload["broker_authority"] == "NONE"
    outcomes = store.list_events(SHADOW_OUTCOME_NS)
    assert len(outcomes) == 1
    assert outcomes[0].payload["broker_executed"] is False
    assert outcomes[0].payload["outcome"]["mode"] == "SHADOW_ONLY"

    # Same still-qualified setup identity cannot be re-created after terminal
    # research resolution.
    created3, resolved3 = record_shadow_runtime(
        store,
        _result(Market(NOW + timedelta(minutes=3), (future,))),
    )
    assert (created3, resolved3) == (0, 0)
    assert len(store.list_events(SHADOW_OUTCOME_NS)) == 1
