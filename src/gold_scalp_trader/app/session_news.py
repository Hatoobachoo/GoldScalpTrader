from dataclasses import dataclass
from gold_scalp_trader.domain.enums import MarketState,ProviderHealth
@dataclass(frozen=True,slots=True)
class BrokerSessionFacts:state:MarketState; source:str="UNVERIFIED"
@dataclass(frozen=True,slots=True)
class NewsContextFacts:health:ProviderHealth; source:str="NONE"
