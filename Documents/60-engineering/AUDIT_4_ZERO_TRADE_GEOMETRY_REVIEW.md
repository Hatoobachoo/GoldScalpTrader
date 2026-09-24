# GoldScalpTrader — Audit 4: Zero-Trade Geometry Review

**Status:** DRAFT CORRECTIVE AUDIT PROTOCOL — NOT RUN
**Version:** 0.1-scalp-zero-trade-geometry
**Authority:** Evidence-driven review when a connected DEMO/DRY_RUN session produces unexpectedly few or zero executable entries.

## 1. Trigger

Run this audit when the operator observes a meaningful active period with no trades or materially lower-than-expected qualified opportunities.

The question is **not** “how do we force more trades?”

Ask:

> Did the market genuinely offer poor/expensive geometry, or did implementation fail to express the documented scalp thesis accurately?

## 2. Required evidence

Retain exact revision/config/scope plus:

- Market/Intelligence snapshots;
- family reports/Fusion;
- Opportunity/Entry Timing events;
- TradePlans and reasons;
- Risk evaluations;
- Gate/Intent traces where reached;
- spread/drift/event-age context;
- session/news state;
- runtime event journal;
- local checkpoint/backup identity.

## 3. Geometry classifications

Classify each qualified candidate outcome:

```text
NO_ANALYTICAL_EDGE
TIMING_WAIT
TIMING_MISSED
EVENT_STALE
STOP_FRAGILE
TARGET_ROOM_POOR
TRANSACTION_COST_POOR
MIN_LOT_UNAFFORDABLE
RISK_BLOCK
HARD_AUTHORITY_BLOCK
GATE_BLOCK
EXECUTION_FAILURE
VALID_NO_TRADE
IMPLEMENTATION_DEFECT
```

Do not collapse all outcomes into “Gate blocked.”

## 4. Review order

```text
MarketSnapshot quality
→ causal structure/liquidity/technical/quant facts
→ family hypothesis
→ BUY/SELL fusion
→ Opportunity identity/freshness
→ M5 timing
→ family-specific invalidation
→ target/path/cost geometry
→ TradePlan state
→ Risk only if Plan READY
→ Gate only if upstream ready
```

## 5. Scalp-specific checks

Inspect whether:

- old events are treated as fresh;
- valid local M5 event/retest invalidation is ignored in favor of overly broad structure;
- arbitrary tight invalidation is fabricated to improve R;
- cost/spread consumes too much target room;
- M5 trigger arrives after most movement is complete;
- min-lot affordability rather than strategy quality is the blocker;
- time/session policy suppresses valid setups unexpectedly;
- six-family overlap/filtering reduces Opportunity Recall.

## 6. Corrective rule

Never reduce structural/Risk/safety standards just to generate entries.

A corrective change must prove a document/code mismatch or evidence-backed design problem and update the full affected graph.

## 7. Current state

```text
AUDIT RESULT: NOT RUN
No connected zero-trade session has been audited for this project yet.
```
