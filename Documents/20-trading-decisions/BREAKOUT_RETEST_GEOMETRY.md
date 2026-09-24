# GoldScalpTrader — Breakout Retest Geometry Extension

**Status:** FROZEN V1 FAMILY-GEOMETRY EXTENSION — SCALP RETEST/FRESHNESS CALIBRATION PENDING
**Version:** 1.0-scalp-retest-invalidation
**Authority:** Family-specific invalidation ordering for Breakout Retest Continuation and preservation of general TradePlan/Risk boundaries.

## 1. Relationship to TradePlan

This document extends `TRADE_PLAN.md` for `BREAKOUT_RETEST_CONTINUATION`.

The executable retest thesis can fail at a more local M5 boundary than broader M15/H1 continuation structure. Using unnecessarily broad invalidation can make a good scalp structurally uneconomic, but this is never permission to invent convenient tight stop.

## 2. Frozen invalidation preference

```text
Breakout Retest Continuation:
exact causally proven M5 retest-failure boundary
→ M5 protected/confirmed structure
→ M15 meaningful structure
→ H1 fallback
```

The exact M5 boundary must come from the same immutable causal lineage and lie on the correct side of entry.

If retest evidence is missing/ambiguous, planner falls back conservatively. It never synthesizes a convenient level.

## 3. Why this is scalp-specific

Scalp targets are smaller and transaction cost proportionally larger. A broad stop can inflate original 1R, weaken nearby objective quality, increase minimum-lot dollar risk and convert a short-horizon thesis into a different broader trade.

Correct response is thesis-correct local geometry—not lower safety or arbitrary tightening.

## 4. Required event evidence

A valid retest boundary preserves:

- source breakout event;
- broken level identity;
- causal acceptance/displacement evidence;
- retest event time/knowledge time;
- retest hold/reclaim/rejection facts;
- exact invalidation source;
- event freshness;
- family/Opportunity/Episode identity.

The breakout must causally precede the retest. A stale/consumed retest cannot be reused as a fresh scalp trigger without a new causal event.

## 5. M1 boundary

M1 remains diagnostic/research only under current V1. It cannot redefine Breakout Retest invalidation or independently create a production trigger. Any future M1 production role requires a separate governed change/evidence packet.

## 6. Downstream policy unchanged

This extension does not own monetary risk percentage/profile/overlay, lot sizing, minimum structural/cost-adjusted room policy, session/news permission, exposure/controller authority, Gate or Intent/writer/reconciliation.

A valid retest plan may still be DEGRADED/INVALID or later BLOCKED.

## 7. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/family_trade_plan.py
src/gold_scalp_trader/decisions/trade_plan.py
```

## 8. Planned proof

Tests prove causal breakout-before-retest ordering, valid M5 retest-boundary preference, invalid/missing evidence fallback, no stale/consumed reuse, outward/broker-valid buffering, no account/Risk manipulation, current cost/target-room ownership and replay no-lookahead.

## 9. Scalp calibration pending

Exact retest hold/failure maturity, family-specific freshness/chase distance, whether some breakout subtypes should fall back to M15 earlier and final gross/cost-room threshold remain scalp evidence questions. M1 authority is not open.