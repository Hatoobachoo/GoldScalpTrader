from __future__ import annotations

from gold_scalp_trader.decisions.fusion import FusionPolicy, evaluate
from gold_scalp_trader.domain.enums import Direction, SetupQualification, StrategyFamily
from gold_scalp_trader.domain.models import DirectionalCase, SetupCandidate


def _candidate(buy_score: float, sell_score: float, *, buy_required: bool = True, sell_required: bool = False) -> SetupCandidate:
    buy = DirectionalCase(Direction.BUY, buy_score, 1.0, buy_required, ("buy evidence",))
    sell = DirectionalCase(Direction.SELL, sell_score, 1.0, sell_required, ("sell evidence",))
    return SetupCandidate(
        "SET-independent",
        StrategyFamily.TREND_PULLBACK_CONTINUATION,
        SetupQualification.QUALIFIED_BUY,
        Direction.BUY,
        buy_score,
        1.0,
        ("M5-event",),
        ("qualified buy family setup",),
        (),
        buy_case=buy,
        sell_case=sell,
        required_evidence_complete=buy_required,
        policy_version="TEST-POLICY",
    )


def test_buy_and_sell_are_independent_not_inverse() -> None:
    candidate = _candidate(0.82, 0.21)
    board = evaluate(candidate)

    assert board.buy.score == 0.82
    assert board.sell.score == 0.21
    assert board.sell.score != 1.0 - board.buy.score
    assert board.leading_direction is Direction.BUY
    assert board.recommendation == "ARM"


def test_strong_independent_opposite_case_red_teams_live_setup() -> None:
    candidate = _candidate(0.82, 0.68, sell_required=True)
    board = evaluate(candidate, FusionPolicy(strong_opposition_score=0.60))

    assert board.leading_direction is Direction.BUY
    assert "STRONG_ACTIVE_FAMILY_OPPOSING_THESIS" in board.red_team_objections
    assert board.recommendation == "WAIT"


def test_missing_family_required_evidence_cannot_arm() -> None:
    candidate = _candidate(0.82, 0.10, buy_required=False)
    board = evaluate(candidate)

    assert "REQUIRED_EVIDENCE_INCOMPLETE" in board.red_team_objections
    assert board.recommendation == "WAIT"


def test_legacy_candidate_does_not_fabricate_inverse_opposite_case() -> None:
    candidate = SetupCandidate(
        "legacy",
        StrategyFamily.TREND_PULLBACK_CONTINUATION,
        SetupQualification.QUALIFIED_BUY,
        Direction.BUY,
        0.80,
        0.90,
        (),
        ("legacy buy",),
    )
    board = evaluate(candidate)

    assert board.buy.score == 0.80
    assert board.sell.score == 0.0
    assert board.recommendation == "ARM"
