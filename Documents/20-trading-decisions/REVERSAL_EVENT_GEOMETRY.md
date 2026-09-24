# GoldScalpTrader — Reversal Event Geometry

**Status:** DRAFT PRE-CHALLENGE CANONICAL EXTENSION
**Version:** 0.1-scalp-event-extreme-invalidation
**Authority:** Thesis-specific M5 invalidation for Failed Breakout Reversal and Liquidity Sweep Reversal before conservative generic fallback.

## 1. Purpose

Reversal scalps often have a thesis-specific event extreme that is more truthful than an unrelated broad structural stop.

This extension allows an exact completed event boundary to be used only when the event and event candle are causally provable from the same immutable snapshot.

It does not authorize a convenient tighter stop, lower R floor or higher risk.

## 2. Failed Breakout Reversal

For `FAILED_BREAKOUT_REVERSAL` the planner may inspect the latest completed M5 failed-break event aligned with the proposed reversal.

Draft event boundary:

```text
BUY reversal  → failed-break event candle low
SELL reversal → failed-break event candle high
```

The source should be explicit, e.g. `M5:FAILED_BREAK_EXTREME` or equivalent typed identity.

## 3. Liquidity Sweep Reversal

For `LIQUIDITY_SWEEP_REVERSAL` the planner may use the exact completed M5 confirmed-sweep event candle when it is causally linked to the Opportunity.

Draft boundary:

```text
BUY reversal  → sweep event candle low
SELL reversal → sweep event candle high
```

The source should be explicit, e.g. `M5:SWEEP_EXTREME`.

## 4. Required proof

Event-specific invalidation is permitted only when all are true:

- correct family identity;
- matching completed M5 structural/liquidity event;
- exact event candle located;
- event time/knowledge time matches the snapshot lineage;
- extreme is on the correct side of approved entry;
- event is not ambiguous/corrupt;
- event is fresh enough under the later timing/plan policy.

## 5. Fail-safe fallback

If any required fact is missing:

```text
M5 protected/confirmed structure
→ M5 relevant technical zone
→ M15 fallback
→ H1 fallback
```

No synthetic event boundary is allowed.

## 6. Scalp-specific rationale

Short-duration reversal trades can be destroyed by using a stop that belongs to a much broader structure than the actual thesis. But the opposite danger is even worse: using an arbitrary tight stop simply to improve R.

Therefore the rule is evidence-bound:

> local event geometry is preferred only when the event itself is the reason the reversal thesis exists.

## 7. Downstream policy remains independent

This extension does not change:

- target-quality requirements;
- cost-aware room policy;
- monetary risk;
- daily loss/cooldown;
- session/news safety;
- account/exposure/controller rules;
- central Gate;
- one-shot Intent/writer/reconciliation.

A plan with a valid event extreme may still be economically poor or blocked.

## 8. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/family_trade_plan.py
src/gold_scalp_trader/decisions/trade_plan.py
```

## 9. Planned proof

Tests must prove exact failed-break/sweep extreme selection, correct BUY/SELL side, causal event-candle lookup, freshness handoff, conservative fallback and non-interference with generic target/risk policy.

## 10. Evidence boundary

Deterministic tests can prove geometry semantics. They cannot prove that reversal scalps are profitable or that a particular event-age threshold is optimal.

## 11. Pre-challenge questions

- exact sweep/failed-break maturity required;
- whether M5 event extreme is always sufficient or needs a minimum structural buffer;
- family-specific freshness windows;
- whether M1 can improve trigger timing without redefining invalidation;
- treatment of multiple closely spaced failed events.
