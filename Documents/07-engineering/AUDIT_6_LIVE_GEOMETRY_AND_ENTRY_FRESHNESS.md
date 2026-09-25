# GoldScalpTrader — Audit 6: Live Geometry and Entry Freshness

**Status:** FINAL CORRECTIVE AUDIT PROTOCOL — NOT RUN AGAINST IMPLEMENTATION
**Version:** 2.0-consumed-geometry-m1-executable-freshness
**Authority:** Executable geometry validity, consumed/stale structural objects, fresh quote repricing, M1 timing freshness and preservation of unchanged structural invalidation.

## 1. Purpose

Audit 6 checks a dangerous class of scalp errors:

> A setup looks valid in analysis, but the structural objects or entry price used for execution are no longer live/usable.

Focus:

- consumed zones/liquidity;
- stale/raw swings;
- event-specific invalidation proof;
- M1 timing freshness;
- fresh executable quote;
- repriced current Risk/cost against unchanged structural SL;
- pre-submit broker checks.

## 2. Structural object eligibility

Executable TradePlan must not use:

```text
consumed zone
consumed liquidity pool
invalidated FVG/OB
raw/unconfirmed swing
future-confirmed pivot
stale event that no longer represents current thesis
```

Object lifecycle state must be explicit.

## 3. Event-specific geometry

For Breakout Retest / Sweep / Failed Break event stops:

- exact source event exists in causal snapshot;
- event is part of active-family setup;
- extreme is on correct side of entry;
- event not consumed/invalidated before plan construction;
- fallback used if proof missing.

Do not select a tighter event extreme simply because it improves R.

## 4. M1 refinement geometry

M1 may improve entry reference but cannot arbitrarily rewrite M5 thesis invalidation.

Audit compares:

```text
M5 structural invalidation
M1 refined entry
current executable quote
```

The correct result may be better/worse current R without moving the structural stop.

## 5. Fresh quote repricing

Before submit:

```text
fresh Bid/Ask
→ current spread
→ current distance to structural SL
→ remaining target room
→ spread/SL
→ spread/target
→ total cost/reward
→ current monetary risk at normalized volume
```

Structural SL stays unchanged unless a new TradePlan is legitimately rebuilt from new market structure.

## 6. Decision→send latency

If latency exceeds current budget:

```text
fresh quote
→ recompute drift/cost/current risk
→ still valid? continue
→ no longer valid? WAIT/MISSED/fail before send
```

Audit rejects code that sends using stale price simply because earlier Gate/plan passed.

## 7. Broker precheck

Immediately before irreversible send verify current:

- account/server/symbol;
- quote;
- symbol trade mode;
- volume/min/step;
- stops/freeze;
- margin;
- filling/order mode;
- `order_check` where supported.

If precheck fails:

```text
send count = 0
```

## 8. Ambiguous acknowledgement

After send ambiguity:

```text
ACCEPTED_UNKNOWN
→ broker reconciliation
→ no blind retry
```

Audit 6 treats duplicate retry as critical because fast scalping makes accidental duplicate exposure especially dangerous.

## 9. Setup/active-family freshness

Check that fresh quote repricing does not alter which historical setup existed.

```text
active family setup identity
→ stays same historical causal record

current quote/economics
→ may make entry no longer executable
```

If market now forms a different family setup, that becomes separate setup/shadow evidence—not a silent mutation of the current Opportunity.

## 10. Required scenarios

1. valid setup + consumed target zone → no executable plan using consumed zone;
2. valid M5 setup + fresh M1 entry → use refined entry, preserve structural invalidation;
3. stale M1 trigger + surviving M5 Opportunity → WAIT/re-evaluate;
4. drift increases spread/target burden → quality rejection without plan rewrite;
5. min-lot risk changes because entry moved → recalc actual Risk;
6. order_check failure → no send;
7. timeout after send → reconcile/no retry.

## 11. Required tests

```text
test_consumed_zone_excluded
test_consumed_liquidity_excluded
test_unconfirmed_swing_excluded
test_event_stop_requires_causal_proof
test_m1_entry_does_not_rewrite_m5_stop
test_fresh_quote_reprices_quality
test_fresh_quote_reprices_risk
test_latency_revalidation
test_order_check_zero_send
test_ambiguous_ack_no_retry
```

## 12. Current status

Protocol is synchronized to the final architecture and remains **NOT RUN** until live/replay/DEMO evidence exists.
