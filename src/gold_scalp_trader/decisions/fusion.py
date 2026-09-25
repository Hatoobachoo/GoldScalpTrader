"""Active-family BUY/SELL synthesis and bounded Red-Team challenge.

BUY and SELL are independent cases produced by the active strategy family.  The
opposite side is never fabricated as ``1 - score``.  Scores are explanatory
analytical qualities only: they are neither probabilities nor monetary-Risk
inputs.
"""
from __future__ import annotations

from dataclasses import dataclass

from gold_scalp_trader.domain.enums import Direction, EvidenceRole
from gold_scalp_trader.domain.models import DirectionalCase, Evidence, SetupCandidate


@dataclass(frozen=True, slots=True)
class FusionPolicy:
    """Versioned/calibratable Red-Team boundaries, not broker safety rules."""

    version: str = "FUSION_BASELINE_UNCALIBRATED_V2"
    minimum_coverage: float = 0.60
    strong_opposition_score: float = 0.60
    directional_conflict_margin: float = 0.15

    def __post_init__(self) -> None:
        for name, value in (
            ("minimum_coverage", self.minimum_coverage),
            ("strong_opposition_score", self.strong_opposition_score),
            ("directional_conflict_margin", self.directional_conflict_margin),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class Thesis:
    direction: Direction
    score: float
    reasons: tuple[str, ...]
    coverage: float = 0.0
    required_complete: bool = False
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True, slots=True)
class DecisionBoard:
    candidate: SetupCandidate | None
    buy: Thesis
    sell: Thesis
    leading_direction: Direction
    red_team_objections: tuple[str, ...]
    recommendation: str
    leading_score: float = 0.0
    opposing_score: float = 0.0
    coverage: float = 0.0
    policy_version: str = "FUSION_BASELINE_UNCALIBRATED_V2"
    reasons: tuple[str, ...] = ()


def _empty(reason: str, policy: FusionPolicy, candidate: SetupCandidate | None = None) -> DecisionBoard:
    buy = Thesis(Direction.BUY, 0.0, (reason,))
    sell = Thesis(Direction.SELL, 0.0, (reason,))
    return DecisionBoard(
        candidate,
        buy,
        sell,
        Direction.NONE,
        ("NO_ACTIVE_SETUP",),
        "WAIT",
        policy_version=policy.version,
        reasons=(reason,),
    )


def _legacy_case(candidate: SetupCandidate, direction: Direction) -> DirectionalCase:
    """Compatibility for old fixtures/state created before directional cases.

    The candidate's declared direction keeps its score.  The opposite case is
    unknown/unsupported with score zero; importantly it is *not* inferred as the
    inverse of the leading score.
    """

    is_declared = candidate.direction is direction
    return DirectionalCase(
        direction=direction,
        score=candidate.score if is_declared else 0.0,
        coverage=candidate.coverage if is_declared else 0.0,
        required_complete=bool(candidate.qualified and is_declared),
        reasons=candidate.reasons if is_declared else ("independent opposite case unavailable in legacy candidate",),
        evidence=candidate.evidence if is_declared else (),
    )


def _thesis(case: DirectionalCase) -> Thesis:
    return Thesis(
        direction=case.direction,
        score=case.score,
        reasons=case.reasons,
        coverage=case.coverage,
        required_complete=case.required_complete,
        evidence=case.evidence,
    )


def _opposition_count(case: DirectionalCase) -> int:
    return sum(1 for evidence in case.evidence if evidence.role is EvidenceRole.OPPOSITION)


def evaluate(candidate: SetupCandidate | None, policy: FusionPolicy | None = None) -> DecisionBoard:
    """Build independent active-family BUY/SELL theses and Red-Team the leader."""

    p = policy or FusionPolicy()
    if candidate is None or not candidate.qualified:
        return _empty("no qualified active-family setup", p, candidate)

    buy_case = candidate.buy_case or _legacy_case(candidate, Direction.BUY)
    sell_case = candidate.sell_case or _legacy_case(candidate, Direction.SELL)
    buy, sell = _thesis(buy_case), _thesis(sell_case)

    if buy.score > sell.score:
        lead, opposing = buy, sell
    elif sell.score > buy.score:
        lead, opposing = sell, buy
    else:
        lead = opposing = None

    objections: list[str] = []
    reasons: list[str] = []
    if lead is None:
        objections.append("DIRECTIONAL_CONFLICT")
        reasons.append("independent BUY and SELL cases are equally strong")
        return DecisionBoard(
            candidate,
            buy,
            sell,
            Direction.NONE,
            tuple(objections),
            "WAIT",
            leading_score=buy.score,
            opposing_score=sell.score,
            coverage=max(buy.coverage, sell.coverage),
            policy_version=p.version,
            reasons=tuple(reasons),
        )

    if lead.direction is not candidate.direction:
        objections.append("CANDIDATE_DIRECTION_MISMATCH")
        reasons.append("family candidate direction disagrees with strongest independent thesis")
    if not lead.required_complete or candidate.required_evidence_complete is False:
        objections.append("REQUIRED_EVIDENCE_INCOMPLETE")
        reasons.append("family-defining evidence is incomplete")
    if lead.coverage < p.minimum_coverage:
        objections.append("LOW_REQUIRED_EVIDENCE_COVERAGE")
        reasons.append(f"leading evidence coverage {lead.coverage:.2f} below policy {p.minimum_coverage:.2f}")
    if opposing.required_complete and opposing.score >= p.strong_opposition_score:
        objections.append("STRONG_ACTIVE_FAMILY_OPPOSING_THESIS")
        reasons.append(f"independent opposing thesis is strong at {opposing.score:.2f}")
    if abs(lead.score - opposing.score) < p.directional_conflict_margin and opposing.score > 0:
        objections.append("DIRECTIONAL_CONFLICT")
        reasons.append("BUY/SELL quality separation is too small")

    # Opposition evidence is deliberately explanatory rather than an automatic
    # veto.  Optional/contrary context must not turn into a hidden global gate.
    opposition_items = _opposition_count(
        buy_case if lead.direction is Direction.BUY else sell_case
    )
    if opposition_items:
        reasons.append(f"leading thesis carries {opposition_items} explicit opposing evidence item(s)")

    recommendation = "ARM" if not objections else "WAIT"
    if recommendation == "ARM":
        reasons.append(f"independent {lead.direction.value} thesis accepted; entry timing still downstream")

    return DecisionBoard(
        candidate=candidate,
        buy=buy,
        sell=sell,
        leading_direction=lead.direction,
        red_team_objections=tuple(dict.fromkeys(objections)),
        recommendation=recommendation,
        leading_score=lead.score,
        opposing_score=opposing.score,
        coverage=lead.coverage,
        policy_version=p.version,
        reasons=tuple(reasons),
    )
