from __future__ import annotations

from dataclasses import dataclass

from gold_scalp_trader.domain.enums import ManagementAction, Timeframe
from gold_scalp_trader.intelligence.snapshot import IntelligenceSnapshot
from .models import ManagedTrade


@dataclass(frozen=True, slots=True)
class ManagementDecision:
    action: ManagementAction
    reason: str
    proposed_sl: float | None = None
    proposed_tp: float | None = None


def evaluate(
    trade: ManagedTrade,
    snapshot: IntelligenceSnapshot,
    bars_in_trade: int,
) -> ManagementDecision:
    m5 = snapshot.by_timeframe.get(Timeframe.M5)
    if m5 is None:
        return ManagementDecision(ManagementAction.HOLD, "M5 management context unavailable")
    if trade.original_r_price <= 0:
        return ManagementDecision(ManagementAction.EXIT, "invalid original R geometry")

    market = snapshot.market
    price = market.quote.bid if trade.direction.value == "BUY" else market.quote.ask
    open_r = (
        (price - trade.entry) / trade.original_r_price
        if trade.direction.value == "BUY"
        else (trade.entry - price) / trade.original_r_price
    )

    if open_r <= -1.0:
        return ManagementDecision(ManagementAction.EXIT, "structural/original risk exhausted")

    # Scalp positions must not silently become swings when progress fails.
    if bars_in_trade >= 6 and open_r < 0.25:
        return ManagementDecision(ManagementAction.EXIT, "TIME_EFFICIENCY_FAILURE")

    # First earned protection: remove initial risk only after >=1R progress.
    if open_r >= 1.0 and abs(trade.current_sl - trade.original_sl) <= 1e-9:
        proposed = max(trade.current_sl, trade.entry) if trade.direction.value == "BUY" else min(trade.current_sl, trade.entry)
        return ManagementDecision(
            ManagementAction.PROTECT,
            "earned protection after >=1R",
            proposed,
            trade.expansion_target or trade.primary_target,
        )

    # Structural trailing uses a confirmed M5 swing and never widens the stop.
    if open_r >= 1.5:
        atr = m5.quant.atr14
        buffer = max((atr or 0.0) * 0.05, market.symbol_spec.tick_size)
        if trade.direction.value == "BUY" and m5.structure.last_swing_low is not None:
            proposed = m5.structure.last_swing_low.price - buffer
            if trade.current_sl < proposed < price:
                return ManagementDecision(
                    ManagementAction.TRAIL,
                    "confirmed M5 protected low earned tighter stop",
                    proposed,
                    trade.expansion_target or trade.primary_target,
                )
        if trade.direction.value == "SELL" and m5.structure.last_swing_high is not None:
            proposed = m5.structure.last_swing_high.price + buffer
            if price < proposed < trade.current_sl:
                return ManagementDecision(
                    ManagementAction.TRAIL,
                    "confirmed M5 protected high earned tighter stop",
                    proposed,
                    trade.expansion_target or trade.primary_target,
                )

    # Runner is exceptional and only descriptive until a fresh structural
    # continuation objective exists. The broker TP remains the expansion target.
    reached_primary = (
        price >= trade.primary_target
        if trade.direction.value == "BUY"
        else price <= trade.primary_target
    )
    if open_r >= 2.0 and reached_primary and trade.expansion_target is not None:
        return ManagementDecision(
            ManagementAction.RUNNER,
            "primary objective accepted; expansion objective remains",
        )

    return ManagementDecision(ManagementAction.HOLD, "thesis remains active")
