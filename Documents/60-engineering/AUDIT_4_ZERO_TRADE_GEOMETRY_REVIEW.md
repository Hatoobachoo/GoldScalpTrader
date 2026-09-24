# GoldScalpTrader — Audit 4: Zero-Trade Geometry Review

**Status:** FROZEN CORRECTIVE AUDIT PROTOCOL — NOT RUN
**Version:** 1.0-preservation-first-zero-trade-geometry
**Authority:** Evidence-driven review when connected DEMO/DRY_RUN produces unexpectedly few or zero executable entries.

## 1. Trigger

Run when a meaningful active period has no trades or materially lower-than-expected qualified opportunities.

The question is not “how do we force more trades?” Ask whether market geometry/cost genuinely failed or implementation failed to express documented scalp thesis.

## 2. Required evidence

Retain exact revision/config/scope plus Market/Intelligence snapshots, family/Fusion, Opportunity/Timing, TradePlans, profiled Risk evaluations, Gate/Intent traces where reached, spread/drift/event-age, session/news/cache state, runtime journal and checkpoint identity.

## 3. Geometry classifications

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
PRESERVATION_VIOLATION
```

Never collapse all outcomes into Gate blocked.

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
→ preserved Risk profile/overlay only if Plan READY
→ hard authorities
→ Gate only if upstream ready
```

## 5. Scalp-specific checks

Inspect whether old events are treated as fresh, valid local M5 invalidation is ignored for overly broad structure, arbitrary tight invalidation is fabricated, spread/cost consumes room, trigger is chased, target already consumed, or time-efficiency semantics are wrong.

These are genuine scalp surfaces.

## 6. Preserved-policy checks

Also verify “zero trades” is not caused by accidental removal/rewrite of non-scalp reference features/defaults:

- SMALL/MEDIUM/NORMAL Risk profiles/bands;
- explicit disabled-by-default aggressive overlay semantics;
- one fresh same-episode re-entry;
- three-loss cooldown policy;
- PRE_CLOSE/reopen baselines;
- bounded six-family analytical floor/concurrency;
- provider/cache policy.

A preserved hard policy may legitimately block a trade. That is not itself a defect.

## 7. Corrective rule

Never reduce structural/Risk/safety standards merely to generate entries.

A change requires evidence of implementation/document mismatch, genuine scalp-specific design problem, explicit operator direction or proven reference defect, followed by full affected-graph sync.

## 8. Current state

```text
AUDIT RESULT: NOT RUN
No qualifying connected zero-trade session has been audited yet.
```

Protocol is frozen; result remains NOT RUN.