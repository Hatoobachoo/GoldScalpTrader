# GoldScalpTrader — System Health and Diagnostics

**Status:** FROZEN V1 DIAGNOSTICS CONTRACT — IMPLEMENTATION / CONNECTED OBSERVATION PENDING
**Version:** 1.0-profiled-risk-cache-aware-health
**Authority:** Operational visibility, reason semantics, blocker-stage truth, preserved policy visibility, local-backup health and diagnostic boundaries.

## 1. Purpose

Health is not a trading signal. It answers whether the process can trust market facts, identity, durable state and authority required for the next safe action.

A healthy process may legitimately show no trade. Learning/browser/local-backup degradation is not analytical evidence.

## 2. Health topology

```text
process heartbeat
+ MT5/account/symbol identity
+ market freshness/completeness
+ StateStore/checkpoint integrity
+ controller/fencing
+ session truth
+ News/provider/cache truth
+ reconciliation
+ Risk profile/overlay/state
+ learning queue/receipt
+ local backup health
→ HealthSnapshot
→ DashboardData / structured logs
```

## 3. Health dimensions

| Dimension | Healthy/known means | Degraded/block response |
|---|---|---|
| Process | heartbeat advances | liveness issue, not trading signal |
| MT5/identity | intended scope verified | hard block writes |
| Market data | required quote/bars meet policy | WAIT/block according to owner |
| Freshness | quote/event/trigger current enough | visible aging; no late send |
| Persistence | schema/integrity valid | recovery; no empty reset |
| Controller | current holder/epoch valid | fence writes |
| Session | broker market state known | OPEN/PRE_CLOSE/CLOSED/WARMUP/UNKNOWN |
| News | current accepted event truth/cache state known | CLEAR/BLACKOUT/UNKNOWN/warmup |
| Reconciliation | lifecycle agrees with broker | reconcile before conflicting write |
| Risk | DayStartEquity profile/overlay/equity/cash-flow/lot/margin known | upstream BLOCK/UNKNOWN |
| Learning | queue/receipt state explicit | learning degrade unless core persistence unsafe |
| Local backup | latest artifact/checkpoint verified | no recoverability claim from failed artifact |
| Secondary UI | snapshot/server healthy | PRIMARY independent |

## 4. State vocabularies are not interchangeable

```text
DataQuality     HEALTHY / STALE / SPARSE / CORRUPT / UNKNOWN
MarketState     OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
NewsState       CLEAR / BLACKOUT / UNKNOWN / POST_NEWS_WARMUP
TradePlan       READY / DEGRADED / INVALID
RiskProfile     SMALL / MEDIUM / NORMAL
AggressiveMode  DISABLED / ENABLED
RiskState       NORMAL / LOSS_LOCKED / COOLDOWN / UNKNOWN
Central Gate    ALLOW / BLOCK / UNKNOWN / NOT_EVALUATED
Runtime Health  HEALTHY / DEGRADED / RECONCILING / BLOCKED
Capability      READINESS / DRY_RUN / DEMO_PRIMARY / REAL_GATED
```

True `Market OPEN + News UNKNOWN` new-entry result is already frozen: new entry BLOCK/LIMITED while safe management remains action-sensitive.

## 5. Preserved policy diagnostics

Health surfaces but does not redefine:

```text
SMALL/MEDIUM/NORMAL profile identity + canonical bands
AGGRESSIVE_SMALL_ACCOUNT disabled/enabled state
8% maximum SL-risk ceiling (not target) when enabled
16% aggregate/daily ceilings when enabled
manual reset disabled/enabled state
one-fresh-reentry state
three-loss cooldown state
Provider TTL baseline 1800s
Daily PRE_CLOSE T-20/T-10
Weekend PRE_CLOSE T-60/T-30
Daily reopen 1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

Current broker schedule/provider facts remain separate external truth.

## 6. Blocker-stage semantics

```text
analytical WAIT/MISSED/INVALID
→ TradePlan blocker
→ Risk blocker
→ Session/News/other hard authority
→ actual central Gate
→ Intent/precheck/broker/reconciliation
```

`ENTRY_BLOCKED` is not proof Gate ran. Upstream rejection maps Gate to NOT_EVALUATED; only actual Gate BLOCK displays BLOCKED.

## 7. Stable reasons

Important state retains machine reason, concise explanation, scope/identity, observed value/threshold where owned, UTC time and next safe action.

Examples:

```text
TARGET_ROOM_POOR
STOP_FRAGILE
EVENT_STALE
TRIGGER_STALE
SPREAD_TOO_WIDE
PRICE_DRIFT_TOO_LARGE
MIN_LOT_UNAFFORDABLE
NEWS_BLACKOUT
NEWS_UNKNOWN
LOSS_LOCKED
COOLDOWN_ACTIVE
AGGRESSIVE_MODE_INELIGIBLE
RECONCILIATION_PENDING
CONTROLLER_STALE
LOCAL_BACKUP_FAILED
```

Dashboard never invents unresolved thresholds.

## 8. Runtime maintenance / shutdown

Safe downstream work such as learning-queue processing, local checkpoint maintenance and presentation may continue during recoverable waits if it does not rerun authority improperly.

```text
stop new work
→ reconcile/stop as allowed
→ release controller + MT5 authority
→ fresh verified local checkpoint
→ secret/integrity scan
→ local backup catalog update
→ explicit success/failure
```

No Git commit/push/pull in runtime health lifecycle.

## 9. Failure examples

| Failure | Truth | Response |
|---|---|---|
| MT5 identity failure | broker authority unavailable/mismatch | no writes |
| stale/insufficient data | recoverable wait where allowed | dashboard alive |
| future/corrupt chronology | corrupt | hard block |
| stale trigger/event | no longer executable | WAIT/MISSED/BLOCK by owner |
| SQLite integrity failure | state corrupt | recovery; no reset |
| controller loss | ownership lost | fence writes |
| ambiguous ack | lifecycle unresolved | reconcile only |
| known CLOSED + News unavailable | CLOSED + separate News state | market blocks |
| known blackout | BLACKOUT | hard new-entry block |
| valid LKG after refresh failure | accepted News truth + provider DEGRADED | use owner result |
| expired/invalid/no cache | NEWS UNKNOWN | new-entry block/limited |
| poor TradePlan | upstream rejection | Gate not evaluated |
| Risk/min-lot/margin/profile failure | upstream monetary rejection | no Intent |
| UI failure | presentation unavailable | PRIMARY continues |
| final backup failure | recoverability degraded | explicit failure; preserve last good state |

## 10. Source/proof map

```text
market freshness      market_data/*
session/news/cache    app/session_news.py + risk/permissions.py
Risk/profile state    risk/*
blocker/Gate display  operator/presentation.py
recovery              app/recovery.py + recovery_mt5.py
controller            execution/controller.py
Intent/reconcile      execution/service.py + reconcile.py
learning queue        management/store.py + research/live_learning.py
local backup          persistence/checkpoint.py + backup.py + local_recovery_package.py
```

## 11. Evidence boundary

Deterministic tests prove state/reason/failure semantics. They do not prove real broker latency, future opportunity frequency, profitability, special holiday hours or fresh-machine broker continuity.