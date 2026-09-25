"""Crash-safe learning queue helpers."""
from gold_scalp_trader.persistence.store import StateStore
QUEUE="closed_trade_learning_queue"
def enqueue(store:StateStore,trade_id:str,payload:dict)->None:store.put(QUEUE,trade_id,payload,allow_replace=False)
def consume(store:StateStore,trade_id:str)->None:store.delete(QUEUE,trade_id)
def pending(store:StateStore)->int:return len(store.list_records(QUEUE))
