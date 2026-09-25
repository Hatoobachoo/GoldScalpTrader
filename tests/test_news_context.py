from gold_scalp_trader.domain.enums import ProviderHealth
from gold_scalp_trader.intelligence.news import NewsContext

def test_news_owns_no_hard_permission():
    assert NewsContext(ProviderHealth.UNAVAILABLE,None).hard_trading_permission is None
