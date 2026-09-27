from datetime import datetime, timezone
from types import SimpleNamespace

from gold_scalp_trader.app.cycle import CycleResult
from gold_scalp_trader.app.runtime import _apply_durable_open_risk
from gold_scalp_trader.config import Settings
from gold_scalp_trader.decisions.trade_plan import TradePlan
from gold_scalp_trader.domain.enums import Direction, RiskDecision, RiskProfile
from gold_scalp_trader.domain.market import AccountFacts, SymbolSpec
from gold_scalp_trader.risk.engine import evaluate, resolve_profile
from gold_scalp_trader.risk.runtime import RiskAuthority
from gold_scalp_trader.risk.state import initial

UTC = timezone.utc


def test_profile_boundaries_are_preserved():
    assert resolve_profile(100) is RiskProfile.SMALL
    assert resolve_profile(300) is RiskProfile.MEDIUM
    assert resolve_profile(999.99) is RiskProfile.MEDIUM
    assert resolve_profile(1000) is RiskProfile.NORMAL


def test_min_lot_is_evaluated_not_automatically_rejected():
    p = TradePlan("p", "o", Direction.BUY, 100, 99.9, 101, None, "M5", 10, "READY", ())
    a = AccountFacts(1, "demo", "USD", 100, 100, 100, True, True)
    s = SymbolSpec("XAUUSDm", 3, .001, .001, 1, .01, 200, .01)
    r = evaluate(p, a, s, day_start_equity=100, target_risk_pct=3.0)
    assert r.volume is not None and r.decision in {RiskDecision.PASS, RiskDecision.BLOCK}


def test_target_above_hard_ceiling_blocks():
    p = TradePlan("p", "o", Direction.BUY, 100, 99, 101, None, "M5", 1, "READY", ())
    a = AccountFacts(1, "demo", "USD", 100, 100, 100, True, True)
    s = SymbolSpec("XAUUSDm", 3, .001, .001, 1, .01, 200, .01)
    assert evaluate(p, a, s, day_start_equity=100, target_risk_pct=7.1).decision is RiskDecision.BLOCK


def test_aggressive_aggregate_risk_ceiling_is_16_percent():
    p = TradePlan("p", "o", Direction.BUY, 100, 99.9, 101, None, "M5", 10, "READY", ())
    a = AccountFacts(1, "demo", "USD", 100, 100, 100, True, True)
    s = SymbolSpec("XAUUSDm", 3, .001, .001, 1, .01, 200, .01)
    r = evaluate(
        p,
        a,
        s,
        day_start_equity=100,
        target_risk_pct=3.0,
        aggressive_mode=True,
        aggregate_open_risk_pct=15.0,
    )
    assert r.decision is RiskDecision.BLOCK


def test_live_risk_sizing_uses_durable_day_start_profile_not_current_equity():
    """Crossing a profile boundary intraday must not re-profile live sizing."""
    now = datetime(2026, 9, 28, 12, 0, tzinfo=UTC)
    account = AccountFacts(1, "demo", "USD", 310, 310, 310, True, True)
    spec = SymbolSpec("XAUUSDm", 3, .001, .001, 1, .01, 200, .01)
    market = SimpleNamespace(account=account, symbol_spec=spec)
    plan = TradePlan("p", "o", Direction.BUY, 100, 99.9, 101, None, "M5", 10, "READY", ())
    cycle = CycleResult(
        intelligence=SimpleNamespace(market=market),
        registry=None,
        isolation=None,
        board=None,
        opportunity=None,
        timing=None,
        trade_plan=plan,
        quality=None,
        risk=None,
        live_action="RISK_PENDING",
        status="RISK_PENDING",
        reason="TARGET_RISK_PERCENT_NOT_SET",
    )
    authority = RiskAuthority(initial(299.0, now), RiskDecision.PASS, "RISK_STATE_PASS", 0.0)
    settings = Settings(target_risk_percent=1.0)

    out = _apply_durable_open_risk(cycle, settings, authority)

    assert out.risk is not None
    assert out.risk.profile is RiskProfile.SMALL
    assert out.risk.decision is RiskDecision.PASS
