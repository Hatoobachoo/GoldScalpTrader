# GoldScalpTrader — Reversal Event Geometry

**Status:** FROZEN V1 FAMILY-GEOMETRY EXTENSION — SCALP EVENT-FRESHNESS CALIBRATION PENDING
**Version:** 1.0-scalp-event-extreme-invalidation
**Authority:** Thesis-specific M5 invalidation for Failed Breakout Reversal and Liquidity Sweep Reversal before conservative generic fallback.

## 1. Purpose

Reversal scalps often have a thesis-specific event extreme that is more truthful than unrelated broad structural stop.

An exact completed event boundary is used only when the event/event candle are causally provable from the same immutable snapshot. This does not authorize a convenient tighter stop, lower target-quality requirement or higher Risk.

## 2. Failed Breakout Reversal

For `FAILED_BREAKOUT_REVERSAL`, inspect latest completed M5 failed-break event aligned with proposed reversal.

Preferred boundary:

```text
BUY reversal  → failed-break event candle low
SELL reversal → failed-break event candle high
```

Source identity should be explicit, such as `M5:FAILED_BREAK_EXTREME`.

## 3. Liquidity Sweep Reversal

For `LIQUIDITY_SWEEP_REVERSAL`, use exact completed M5 confirmed-sweep event candle only when causally linked to Opportunity.

Preferred boundary:

```text
BUY reversal  → sweep event candle low
SELL reversal → sweep event candle high
```

Source identity should be explicit, such as `M5:SWEEP_EXTREME`.

## 4. Required proof

Event-specific invalidation is permitted only when all are true:

- correct family identity;
- matching completed M5 structural/liquidity event;
- exact event candle located;
- event time/knowledge time matches snapshot lineage;
- event extreme lies on correct side of approved entry;
- event is not ambiguous/corrupt/consumed;
- event remains fresh enough under Entry Timing/TradePlan policy.

## 5. Fail-safe fallback

```text
M5 protected/confirmed structure
→ M5 relevant technical zone
→ M15 fallback
→ H1 fallback
```

No synthetic event boundary is allowed.

## 6. Scalp-specific rationale

Short-duration reversal trade can be destroyed by stop geometry belonging to a much broader thesis. The opposite error—arbitrary tight stop to improve apparent R—is prohibited.

> Local event geometry is preferred only when the event itself is the reason the reversal thesis exists.

## 7. M1 boundary

M1 remains diagnostic/research only. It cannot redefine event invalidation or independently authorize production reversal timing. Any future promotion requires a separate governed design/evidence decision.

## 8. Downstream policy remains independent

This extension does not change target-quality requirements, cost-aware room, preserved account Risk profiles/aggressive overlay, daily loss/cooldown/re-entry, session/news safety, account/exposure/controller, Gate or Intent/writer/reconciliation.

A valid event extreme may still produce economically poor/blocked plan.

## 9. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/family_trade_plan.py
src/gold_scalp_trader/decisions/trade_plan.py
```

## 10. Planned proof

Tests prove exact failed-break/sweep extreme selection, correct BUY/SELL side, causal event-candle lookup, no stale/consumed reuse, freshness handoff, conservative fallback, M1 non-authority and non-interference with general TradePlan/Risk policy.

## 11. Evidence boundary

Deterministic tests prove geometry semantics, not profitability or optimal freshness thresholds.

## 12. Scalp calibration pending

Exact sweep/failed-break maturity, minimum structural buffer, family-specific freshness/chase windows and treatment of closely spaced failed events remain evidence questions. M1 authority is not open.