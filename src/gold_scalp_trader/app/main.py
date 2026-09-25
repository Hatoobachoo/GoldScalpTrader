"""Read-only application composition entry point for implementation phase 1."""
from __future__ import annotations
from gold_scalp_trader.config import load_settings
from gold_scalp_trader.domain.enums import RuntimeMode, Timeframe
from gold_scalp_trader.intelligence import build as build_intelligence
from gold_scalp_trader.market_data import Mt5ReadError, Mt5Reader

def run() -> int:
    settings=load_settings()
    print("="*72); print(" GoldScalpTrader — implementation foundation"); print("="*72)
    print(f"Mode              : {settings.mode.value}")
    print(f"Preferred symbol  : {settings.preferred_symbol}")
    print(f"Active family     : {settings.active_strategy_family or 'UNSET (allowed in DRY_RUN)'}")
    print(f"Broker write      : {'ENABLED BY CONFIG' if settings.broker_write_enabled else 'DISABLED'}")
    if settings.mode is RuntimeMode.REAL:
        print("REAL mode configuration present; execution implementation is not active in this phase.")
    try:
        result=Mt5Reader(settings).read()
    except Mt5ReadError as exc:
        print(f"MT5 read boundary : UNAVAILABLE — {exc}"); print("No broker action was attempted."); return 2
    intelligence=build_intelligence(result.snapshot)
    print(f"Resolved symbol   : {result.resolved_symbol}"); print(f"Bid / Ask         : {result.snapshot.quote.bid} / {result.snapshot.quote.ask}"); print(f"Spread            : {result.snapshot.quote.spread}"); print(f"Positions truth   : {result.snapshot.positions_quality.value}")
    for tf in (Timeframe.H1,Timeframe.M15,Timeframe.M5,Timeframe.M1):
        report=intelligence.by_timeframe.get(tf)
        print(f"{tf.value:<4} intelligence  : unavailable" if report is None else f"{tf.value:<4} intelligence  : structure={report.structure.state.value} EMA={report.quant.ema_flow} ATR={report.quant.atr14}")
    print("Read-only foundation cycle complete. No order path invoked."); return 0

def main() -> None:
    raise SystemExit(run())
