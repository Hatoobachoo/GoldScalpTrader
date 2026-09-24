# GoldScalpTrader — Dashboard and UX Contract

**Status:** FROZEN V1 OPERATOR ARCHITECTURE — PRESERVATION-FIRST CORRECTED / IMPLEMENTATION PROOF PENDING
**Version:** 1.2-profiled-risk-cache-aware-operator
**Authority:** Operator visibility, typed dashboard mapping, primary terminal presentation, session/News/provider/cache truth, profiled Risk visibility, verified performance provenance and read-only controls.

## 1. Purpose

Within seconds the operator should understand:

1. XAUUSDm feed/market health and current SELL/BUY;
2. Soft Session, Hard Market State and News State;
3. News provider health/source and LKG cache validity;
4. H1/M15/M5 market picture plus optional H4 and diagnostic M1;
5. current BUY/SELL/Floor decision and why;
6. Opportunity/timing/event freshness;
7. TradePlan geometry, gross/cost-adjusted room and executable quote;
8. leading family/correlation/debate;
9. current SMALL/MEDIUM/NORMAL Risk profile and actual proposal;
10. aggressive small-account mode ENABLED/DISABLED and its ceilings when applicable;
11. daily loss / reset / streak / cooldown / capacity;
12. upstream blocker versus actual central Gate;
13. ManagedTrade/Trade Manager/partial-management state;
14. verified learning/research/local-backup health.

Dashboard is presentation, not a second trading engine.

## 2. One-way architecture

```text
authoritative market/intelligence/decision/TradePlan/Risk/execution/learning facts
+ session/news provider/cache facts
+ durable state/backup health
→ DashboardData / presentation DTO
→ terminal renderer
→ optional atomic read-only browser snapshot
```

Presentation never recalculates profile, risk, cache validity, signal, permission or lifecycle state.

## 3. Display pulse versus decision cadence

A fast display pulse may refresh PKT clock, Bid/Ask, spread, quote age, M5 countdown, provider/cache age and already-owned broker facts without rerunning analytical decisions.

Production bar-based setup/timing remains completed M5. M1 is diagnostic/research only.

## 4. Session / News / provider presentation

Show separately:

```text
Soft Session      ASIA / LONDON / NEW YORK / OVERLAP / OFF HOURS
Hard Market       OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
News              CLEAR / BLACKOUT / UNKNOWN / POST_NEWS_WARMUP
Provider Health   VERIFIED / DEGRADED / STALE / UNAVAILABLE / UNKNOWN
Provider Source   LIVE / FILE / LKG CACHE
Entry Permission  ALLOW / BLOCK / UNKNOWN as owned downstream
```

```text
OPEN + accepted CLEAR from fresh source/cache → may proceed
OPEN + BLACKOUT → BLOCK
OPEN + true NEWS_SAFETY_UNKNOWN → new-entry BLOCK / LIMITED
```

A refresh/API error is not itself UNKNOWN if accepted LKG cache remains valid under original timestamps/coverage/TTL.

## 5. Preserved session baselines shown when authoritative

```text
Provider TTL baseline       1800s
Daily no-entry/flatten      T-20 / T-10
Weekend no-entry/flatten    T-60 / T-30
Daily reopen baseline       1 clean M5
Weekend reopen baseline     2 clean M5 + gap assessment
```

Dashboard displays owning state and countdown; it never calculates broker schedule independently.

## 6. Risk/account presentation

Show current risk truth, not one generic `STANDARD` label.

```text
Profile               SMALL / MEDIUM / NORMAL
DayStartEquity         verified value
Normal target band     profile-owned range
Elevated band          profile-owned range
Hard new-entry ceiling profile-owned value
Daily loss lock        profile-owned value
Proposed lot/risk      when RiskEvaluation exists
Capacity               e.g. 0/1 or 1/1
Loss streak/cooldown   owned state
Manual reset           DISABLED / enabled-bounded state
```

Reference profile values:

| Profile | Normal | Elevated | Hard | Daily |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

### Aggressive small-account display

When explicit mode is disabled:

```text
Aggressive Small Account: DISABLED
```

When explicitly enabled and eligible:

```text
Aggressive Small Account: ENABLED
Per-trade SL-risk ceiling: 8% MAX — NOT TARGET
Aggregate open-risk cap:   16%
Daily loss ceiling:        16%
```

Never imply the bot is trying to size every aggressive trade to 8%.

If no TradePlan/RiskEvaluation exists, show `Risk Standby`, not Risk failure.

## 7. Primary visual hierarchy

```text
HEADER
  product / mode / PKT / Market / Session / News / Gate
  XAU SELL / BUY / spread / quote age / M5 countdown / Today P&L

NEWS / PROVIDER
  health / source / last success / cache age-validity / next event

MARKET PICTURE
  H1 / M15 / M5 / optional H4 / diagnostic M1
  EMA20/EMA50 / RSI / ATR / volatility / event freshness

CURRENT DECISION
  BUY thesis / SELL thesis / Floor Edge / leading family
  correlation / Red Team / Opportunity / M5 Timing / WHY

TRADE PLAN
  Approved Entry Reference / current Bid/Ask
  SL / Primary / optional Expansion / exceptional Runner
  gross room / cost-adjusted room / invalidation / quality

RISK & ACCOUNT
  profile / optional aggressive mode / actual proposal / capacity
  daily loss / reset / streak / cooldown

ACTIVITY / SYSTEM / EXECUTION / OPEN TRADE / LEARNING / LOCAL BACKUP
```

## 8. Current Blocker versus Gate

```text
TradePlan invalid/degraded
→ Current Blocker: TradePlan
→ Gate: NOT EVALUATED

Risk BLOCK/UNKNOWN before Gate
→ Current Blocker: Risk
→ Gate: NOT EVALUATED

News/Session owner blocks before central Gate
→ show owning blocker
→ do not fabricate Gate BLOCKED

central Gate actually BLOCKS
→ Current Blocker: Execution Gate
→ Gate: BLOCKED
```

## 9. TradePlan / freshness truth

Show only actual governed plan fields. Keep Approved Entry Reference and current executable Bid/Ask separate.

Useful scalp facts include event age, trigger age, entry drift, spread, target-room/cost context and latency diagnostics.

## 10. Verified strategy performance

Only verified actual approved-environment closed ManagedTrades count as production performance. Signal, WAIT/MISSED/BLOCK, replay/shadow/counterfactual evidence do not count as actual trades/P&L.

Zero verified closes = `NO SAMPLE`.

## 11. Open ManagedTrade

Show ticket/ownership, verified Entry, live executable price, original/current SL, objectives, original R/current risk, remaining volume, objective stage, any verified partial action, M5 bars/time in trade, management action/reason and Intent/reconciliation/close state.

Time/efficiency is an EXIT reason. Runner is exceptional.

## 12. Runtime capability display

Operator mode must clearly distinguish:

```text
READINESS
DRY_RUN
DEMO PRIMARY
REAL — future capability, disabled/unavailable until its release gate
```

No dashboard toggle may bypass the governed REAL release path.

## 13. Responsive terminal / fallback

Conceptual target:

```text
64–95 cells → stacked narrow renderer
96+ cells   → wide renderer
render failure → compact safe read-only fallback
```

Presentation failure cannot stop trading or create authority.

## 14. Local backup / research footer

May show StrategyMemory/discovery health, last local runtime checkpoint, backup status/path shorthand and recovery state. Research recommendation is never active policy unless governed promotion makes it so.

## 15. Planned proof

Tests cover blocker-vs-Gate truth, width/fallback, presentation pulse without new decisions, provider/cache states, profile/overlay Risk rendering, 8%-is-ceiling-not-target wording, reset/cooldown state, no-plan geometry, verified performance provenance, open-trade partial state and read-only authority.