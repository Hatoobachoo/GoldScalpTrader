# GoldScalpTrader — Dashboard and UX Contract

**Status:** FROZEN V1 OPERATOR ARCHITECTURE — IMPLEMENTATION / CONNECTED PRESENTATION PROOF PENDING
**Version:** 1.1-cache-aware-operator
**Authority:** Operator visibility, typed dashboard mapping, primary terminal presentation, session/News/provider/cache truth, verified performance provenance and read-only controls.

## 1. Purpose

Within seconds the operator should understand:

1. XAUUSDm feed/market health and current SELL/BUY;
2. Soft Session, Hard Market State and News State;
3. News provider health/source and whether a last-known-good cache is currently carrying accepted truth;
4. H1/M15/M5 market picture plus optional H4 and diagnostic M1;
5. current BUY/SELL/Floor decision and why;
6. Opportunity/timing/event freshness;
7. actual TradePlan geometry, gross/cost-adjusted room and current executable quote;
8. leading family/correlation/debate;
9. STANDARD Risk/capacity/daily state;
10. upstream blocker versus actual central Gate;
11. ManagedTrade/Trade Manager state;
12. verified learning/research/local-backup health.

Dashboard is presentation, not a second trading engine.

## 2. One-way architecture

```text
market/intelligence/strategy/decision/TradePlan/Risk/execution/learning facts
+ session/news provider/cache facts
+ durable state/backup health
→ authoritative DashboardData / presentation DTO
→ terminal renderer
→ optional atomic read-only browser snapshot
```

Presentation explains already-owned facts and never recalculates permission or cache validity.

## 3. Display pulse versus decision cadence

A fast display pulse may refresh PKT clock, Bid/Ask, spread, quote age, M5 countdown, provider/cache age and already-owned broker facts without rerunning families, timing, TradePlan, Risk or Intent.

Production bar-based setup/timing remains completed M5. M1 is diagnostic/research only.

## 4. Session / News / provider presentation

Show separately:

```text
Soft Session      ASIA / LONDON / NEW YORK / OVERLAP / OFF HOURS
Hard Market       OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
News              CLEAR / BLACKOUT / UNKNOWN / POST_NEWS_WARMUP
Provider Health   VERIFIED / DEGRADED / STALE / UNAVAILABLE / UNKNOWN
Provider Source   LIVE / FILE / LAST-KNOWN-GOOD CACHE where known
Entry Permission  ALLOW / BLOCK / UNKNOWN as owned downstream
```

Frozen V1 semantics:

```text
OPEN + accepted CLEAR from fresh source
→ may proceed to remaining authorities

OPEN + accepted CLEAR/BLACKOUT from still-valid LKG cache
→ use owning News state
→ Provider Health may be DEGRADED

OPEN + NEWS_SAFETY_UNKNOWN because no valid current source/cache exists
→ BLOCK / LIMITED for new entry
```

A refresh/API error is **not itself** News UNKNOWN. Renderer must display the owning provider/cache validity result rather than infer from network error text.

News UNKNOWN never appears as CLEAR. A stale/expired cache never appears as valid merely because it was the last successful fetch. Existing management/protection/mandatory CLOSE remains action-sensitive.

Useful provider fields when authoritative:

```text
last successful refresh
last refresh error
cache age
cache valid-until / coverage window
next accepted event + countdown
```

## 5. Primary visual hierarchy

```text
HEADER
  product / mode / PKT / Market / Session / News / Gate
  XAU SELL / BUY / spread / quote age / M5 countdown / Today P&L

NEWS / PROVIDER
  provider health / source / last success / cache age-validity / next event

MARKET PICTURE
  H1 / M15 / M5
  optional H4
  diagnostic M1 only if explicitly available
  EMA20/EMA50 / RSI / ATR / volatility / latest event freshness

CURRENT DECISION
  BUY thesis / SELL thesis / Floor Edge / leading family
  correlation / Red Team / Opportunity / completed-M5 Timing / WHY

TRADE PLAN
  Approved Entry Reference / current Bid/Ask separately
  SL / Primary / optional Expansion / exceptional Runner
  gross structural room / cost-adjusted room / invalidation / quality

RISK & ACCOUNT
  STANDARD policy / actual proposal / capacity / daily state / cooldown

ACTIVITY / SYSTEM / EXECUTION / OPEN TRADE / LEARNING / LOCAL BACKUP
```

Exact layout is presentation calibration; meanings are not.

## 6. Responsive terminal

Conceptual target:

```text
64–95 display cells → stacked narrow renderer
96+ display cells    → wide renderer
render failure       → compact safe read-only fallback
```

Presentation crash/fallback cannot stop trading or create authority.

## 7. Current Blocker versus Gate

```text
TradePlan DEGRADED/INVALID
→ Current Blocker: TradePlan
→ Gate: NOT EVALUATED

Risk BLOCK/UNKNOWN before Gate
→ Current Blocker: Risk
→ Gate: NOT EVALUATED

News UNKNOWN owner blocks before Gate composition completes
→ Current Blocker: News/Permission owner as applicable
→ do not fabricate Gate BLOCKED if Gate never evaluated

central Gate actually BLOCKS
→ Current Blocker: Execution Gate
→ Gate: BLOCKED
```

Broad `ENTRY_BLOCKED` is not synonymous with Gate BLOCKED.

## 8. TradePlan truth

Show only actual governed plan fields. If no plan exists, do not fabricate Entry/SL/targets/R as zero.

Keep Approved Entry Reference and current executable Bid/Ask separate. Show gross structural room and cost-adjusted room diagnostics without inventing future fill/slippage.

## 9. Strategy performance

Only verified actual approved-environment closed ManagedTrades enter production performance tables. Signal, WAIT/MISSED/BLOCK, replay, shadow or canary counterfactuals do not count as actual trades/P&L.

Zero verified closes shows `NO SAMPLE`, not fake 0% performance.

## 10. Spread / freshness / latency

Useful display facts include current spread, approved healthy baseline if owned/known, entry drift, trigger/event age, quote age and execution latency diagnostics when available.

Dashboard never invents thresholds.

## 11. STANDARD Risk / account

Show balance/equity where appropriate, capacity, proposed normalized lot/actual risk if RiskEvaluation exists, daily loss state/budget, streak/cooldown and external exposure warnings.

There are no auto-selected SMALL/MEDIUM/NORMAL production tiers in V1.

If no TradePlan/RiskEvaluation exists, show `Risk Standby`, not a risk failure.

## 12. Open ManagedTrade

Show ticket/ownership, verified Entry, live executable price, original/current SL, objectives, immutable original R/current open risk, current objective stage, M5 bars/time in trade, management action/reason and Intent/reconciliation/close state.

Time/efficiency is an EXIT reason, not a separate dashboard authority/action.

## 13. Local backup / research footer

May show StrategyMemory/discovery health, last local runtime checkpoint, backup status/path shorthand and recovery state. Research recommendation is never displayed as active policy unless governed promotion has made it active.

## 14. Planned ownership

```text
src/gold_scalp_trader/app/dashboard.py
src/gold_scalp_trader/app/live_presentation.py
src/gold_scalp_trader/operator/presentation.py
src/gold_scalp_trader/operator/narrow_dashboard.py
src/gold_scalp_trader/operator/rich_dashboard.py
src/gold_scalp_trader/operator/compact_dashboard.py
src/gold_scalp_trader/operator/live_dashboard.py
src/gold_scalp_trader/operator/__init__.py
src/gold_scalp_trader/app/loop.py
```

## 15. Planned proof

Tests cover blocker-vs-Gate truth, width/fallback, presentation pulse without new decisions, fresh-provider versus valid-cache versus true-UNKNOWN rendering, no timestamp/validity inference in presentation, no-plan geometry, verified performance provenance, PKT/M5 countdown, M1 non-authority, STANDARD Risk mapping, open-trade mapping and read-only authority.