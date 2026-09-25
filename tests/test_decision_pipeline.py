from datetime import datetime,timezone
from gold_scalp_trader.domain.enums import Direction,SetupQualification,StrategyFamily
from gold_scalp_trader.domain.models import SetupCandidate
from gold_scalp_trader.decisions.fusion import evaluate
from gold_scalp_trader.decisions.opportunity import create
UTC=timezone.utc
def test_only_qualified_active_candidate_arms_opportunity():
    c=SetupCandidate("x",StrategyFamily.TREND_PULLBACK_CONTINUATION,SetupQualification.QUALIFIED_BUY,Direction.BUY,.8,.9,(),("good",),()); opp=create(evaluate(c),datetime.now(tz=UTC)); assert opp is not None and opp.direction is Direction.BUY
def test_no_candidate_is_wait(): assert evaluate(None).recommendation=="WAIT"
