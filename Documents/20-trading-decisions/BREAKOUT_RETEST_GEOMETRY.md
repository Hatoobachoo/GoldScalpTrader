# GoldScalpTrader — Breakout Retest Geometry Extension

**Status:** DRAFT PRE-CHALLENGE CANONICAL EXTENSION
**Version:** 0.1-scalp-retest-invalidation
**Authority:** Family-specific invalidation ordering for Breakout Retest Continuation and preservation of general Trade Plan/risk boundaries.

## 1. Relationship to Trade Plan

This document extends `TRADE_PLAN.md` for the `BREAKOUT_RETEST_CONTINUATION` family.

It exists because the executable retest thesis can fail at a much more local M5 boundary than the broader M15/H1 continuation structure. Using an unnecessarily broad stop can make a good scalp appear structurally uneconomic.

This is not permission to invent a tighter stop.

## 2. Draft invalidation order

```text
Breakout Retest Continuation:
exact M5 retest-failure boundary
→ M5 protected/confirmed structure
→ M15 meaningful structure
→ H1 fallback
```

The exact M5 boundary must be causally proven from the same immutable snapshot and lie on the correct side of entry.

If the required retest evidence is missing or ambiguous, the planner falls back conservatively. It must never synthesize a convenient level.

## 3. Why scalping makes this important

Scalp targets are smaller and transaction cost is proportionally larger. A broad stop can:

- inflate original 1R;
- make nearby valid objectives look poor;
- increase minimum-lot dollar risk;
- convert a short-horizon thesis into a different, broader trade.

The correct fix is thesis-correct geometry—not lowering safety thresholds or tightening stops arbitrarily.

## 4. Required event evidence

A valid retest boundary should preserve:

- source breakout event;
- broken level identity;
- retest event time;
- retest hold/reclaim/rejection facts;
- exact local invalidation source;
- event freshness;
- family/Opportunity/Episode identity.

A stale old retest cannot be reused as a fresh scalp trigger without a new causal event.

## 5. Downstream policy is unchanged

This extension does not own:

- monetary risk percentage;
- lot sizing;
- minimum structural R/cost-adjusted room threshold;
- session/news permission;
- exposure/controller authority;
- final execution gate;
- Intent/writer/reconciliation.

A retest plan can still be DEGRADED/INVALID or later BLOCKED.

## 6. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/family_trade_plan.py
src/gold_scalp_trader/decisions/trade_plan.py
```

## 7. Planned proof

Tests must prove:

- valid M5 retest boundary is preferred when present;
- invalid/missing event evidence falls back conservatively;
- stop remains outward/buffered and broker-valid;
- no account/risk manipulation changes structural invalidation;
- transaction-cost/target-room policy remains owned by general Trade Plan;
- causal/replay timing prevents future retest knowledge.

## 8. Pre-challenge questions

- exact definition of a valid retest hold/failure;
- how long a retest remains fresh for an M5 scalp;
- whether M1 may refine timing without becoming invalidation authority;
- whether some breakout types should prefer M15 instead;
- final minimum R/cost-adjusted room requirement.
