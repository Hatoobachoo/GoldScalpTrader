from gold_scalp_trader.persistence.store import StateStore
NS="managed_trade"
def clear(store:StateStore,scope:str)->None:store.delete(NS,scope)
