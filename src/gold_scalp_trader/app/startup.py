from contextlib import contextmanager
from typing import Iterator,Any
@contextmanager
def mt5_session()->Iterator[Any]:
    import MetaTrader5 as mt5  # type: ignore
    if not mt5.initialize():raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    try:yield mt5
    finally:mt5.shutdown()
