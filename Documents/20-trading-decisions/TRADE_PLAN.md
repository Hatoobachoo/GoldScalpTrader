# GoldScalpTrader — Structural Trade Plan

**Status:** FROZEN V1 TRADE-PLAN ARCHITECTURE — CALIBRATION PENDING
**Version:** 1.0-cost-aware-scalp-geometry
**Authority:** Approved entry reference, family-aware structural invalidation, initial SL, objective hierarchy, immutable original R, gross structural quality and cost-adjusted executable room.

## 1. Purpose and boundary

TradePlan converts a valid Opportunity plus analytical `ENTER` timing into explicit market geometry **before** monetary sizing or broker submission.

> Strategy decides whether an idea is worth pursuing. TradePlan defines how it would be entered, invalidated and targeted. Risk decides whether the account can afford that geometry.

TradePlan does not size lots, distort a structural stop for account convenience, call MT5 or grant final execution permission.

## 2. Construction pipeline

```text
READY analytical Opportunity
→ Approved Entry Reference
→ family-aware structural invalidation
→ volatility/noise + broker-tick outward buffer
→ Immediate / Primary / optional Expansion objectives
→ Stop Quality
→ path / target / gross structural quality
→ current known transaction-cost context
→ cost-adjusted executable-room diagnostics
→ READY / DEGRADED / INVALID TradePlan
→ independent monetary Risk
```

## 3. Price identities

| Identity | Meaning | Owner |
|---|---|---|
| Signal Price | where evidence formed | decisions/timing |
| Approved Entry Reference | geometry reference | TradePlan |
| Executable Quote | fresh Bid/Ask immediately before submit | execution |
| Actual Fill | broker-confirmed filled price | reconciliation |

A scalp is especially sensitive to the difference between Signal Price, Approved Entry Reference and Actual Fill.

## 4. TradePlan output

Preserve:

- Opportunity / Episode / family identity;
- direction;
- signal and approved entry reference;
- invalidation source/price and evidence lineage;
- buffer and initial SL;
- Stop Quality;
- Immediate Obstacle;
- Primary Scalp Target;
- optional Expansion Target;
- optional exceptional Runner Objective;
- immutable original structural risk distance;
- gross structural R / room;
- current spread/cost diagnostics;
- cost-adjusted remaining room / room-to-cost context;
- path/target/plan quality;
- event/plan freshness;
- state and exact reason.

States:

```text
READY
DEGRADED
INVALID
```

## 5. Family-aware structural invalidation

Core question:

> What causal price behaviour proves this exact thesis wrong?

Candidate sources include protected/confirmed M5 structure, retest-failure boundary, sweep extreme, failed-break extreme, M15 fallback structure and meaningful technical zone.

A source must be causal, provable from the same immutable market/intelligence lineage and on the correct side of entry.

### V1 preferred hierarchy

| Family | Preferred invalidation |
|---|---|
| Trend Pullback Continuation | M5 local pullback failure → M15 structure → H1 fallback |
| Breakout Expansion | M5/M15 acceptance-failure geometry → broader fallback |
| Breakout Retest Continuation | M5 retest-failure boundary → M15 → H1 |
| Liquidity Sweep Reversal | exact proven M5 sweep extreme → generic M5 → M15 → H1 |
| Failed Breakout Reversal | exact proven M5 failed-break extreme → generic M5 → M15 → H1 |
| Compression Expansion | M5 release/range failure → M15 range boundary → H1 fallback |

Exact event extremes are used only when matching event/candle lineage is provable. Otherwise fall back conservatively; never invent a tighter stop.

## 6. Initial SL and Stop Quality

Initial SL is:

```text
structural invalidation
+ volatility/noise-aware buffer
+ outward broker-valid tick normalization
```

ATR supports structure; it does not replace structure.

If broker stop/freeze/tick constraints materially distort the thesis, the plan becomes INVALID rather than silently moving geometry.

Stop Quality vocabulary:

```text
ROBUST
ACCEPTABLE
FRAGILE
INVALID
```

FRAGILE normally degrades/waits while the Opportunity may survive for better geometry.

## 7. Objective hierarchy

V1 scalp hierarchy:

```text
Immediate Obstacle
→ Primary Scalp Target
→ optional Expansion Target when fresh continuation/session structure supports it
→ Runner Objective only as exceptional continuation
```

Targets come from causally known structure/liquidity/session geometry, not arbitrary fixed-dollar TP values.

Multiple analytical objectives do not imply multiple orders or mandatory partial closes.

## 8. Gross structural quality and cost-adjusted room

Audit 1 freezes a dual-truth design:

```text
A) gross structural geometry
B) current cost-adjusted executable room
```

TradePlan must preserve current known facts sufficient to reason about:

- gross reward distance;
- original stop distance;
- current spread;
- approved slippage/commission reserve assumptions where available;
- remaining room after known cost context;
- room-to-cost ratio or equivalent normalized metric.

The old Swing `1.20R` floor is **not active scalp policy**. Exact minimum gross R / net room thresholds remain calibration pending.

Do not double-count spread if executable Bid/Ask geometry already embeds it. Do not invent future slippage/fill values that are not yet known.

## 9. Final execution revalidation

A plan can deteriorate between analytical ENTER and broker submit because:

- price drifts;
- spread expands;
- target room shrinks;
- new completed structure changes the thesis;
- event freshness expires;
- broker constraints make the request invalid.

Execution owns the final fresh Bid/Ask/spread/drift/trigger-age recheck. Risk may block affordability but cannot rewrite the plan.

## 10. Original R

After verified fill plus original structural SL, original risk distance defines immutable historical 1R for management/research. Later protection/trailing never rewrites original R.

## 11. Persistence / recovery

A persisted TradePlan belongs to exactly one Opportunity/Episode identity. Recovery validates identity plus fresh broker/market truth before any write. Restored plan is context, not permission.

When a terminal Opportunity is replaced by a genuinely new episode, retire mismatched old TradePlan before persisting the new active identity.

## 12. Dashboard

When valid geometry exists, show separately:

```text
Entry Reference
current executable Bid/Ask
SL
Primary / optional Expansion objective
Gross structural R/room
Cost-adjusted room context
Invalidation source
Stop/Path/Target quality
Plan state/reason
```

Never display zero placeholders as valid geometry.

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/decisions/trade_plan.py
src/gold_scalp_trader/decisions/family_trade_plan.py
```

## 14. Planned proof

Tests cover BUY/SELL geometry, family-aware invalidation, event-specific extremes, tick normalization, broker constraints, objective ordering, gross/cost-room calculations, no double-counting, original-R immutability, stale/drift degradation and strict Risk independence.

## 15. Calibration pending

Minimum gross R, minimum cost-adjusted room/ratio, buffers, fragile-stop threshold, target/path quality, session-target sources, runner policy, target merge tolerance and plan/event freshness values require replay/stress/holdout and connected execution evidence.