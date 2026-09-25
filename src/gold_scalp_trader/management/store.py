"""Durable ManagedTrade storage with original strategy/R preservation."""
from gold_scalp_trader.domain.enums import Direction,StrategyFamily
from gold_scalp_trader.persistence.store import StateStore
from .models import ManagedTrade
NS="managed_trade"
def save(store:StateStore,scope:str,trade:ManagedTrade)->None:store.put(NS,scope,{"trade_id":trade.trade_id,"ticket":trade.ticket,"symbol":trade.symbol,"direction":trade.direction.value,"volume":trade.volume,"entry":trade.entry,"original_sl":trade.original_sl,"current_sl":trade.current_sl,"primary_target":trade.primary_target,"expansion_target":trade.expansion_target,"family":trade.family.value,"policy_version":trade.policy_version,"original_r_price":trade.original_r_price})
def load(store:StateStore,scope:str)->ManagedTrade|None:
    r=store.get(NS,scope)
    if r is None:return None
    p=r.payload;return ManagedTrade(str(p["trade_id"]),int(p["ticket"]),str(p["symbol"]),Direction(p["direction"]),float(p["volume"]),float(p["entry"]),float(p["original_sl"]),float(p["current_sl"]),float(p["primary_target"]),None if p["expansion_target"] is None else float(p["expansion_target"]),StrategyFamily(p["family"]),str(p["policy_version"]),float(p["original_r_price"]))
def clear(store:StateStore,scope:str)->None:store.delete(NS,scope)
