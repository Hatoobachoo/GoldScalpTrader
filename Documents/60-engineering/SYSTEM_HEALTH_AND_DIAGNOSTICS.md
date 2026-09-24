# GoldScalpTrader — System Health and Diagnostics

**Status:** DRAFT PRE-CHALLENGE DIAGNOSTICS CONTRACT
**Version:** 0.1-scalp-health
**Authority:** Operational visibility, reason semantics, blocker-stage truth, local-backup health and diagnostic boundaries.

## 1. Purpose

Health is not a trading signal. It answers whether the process can currently trust market facts, identity, durable state and authority required for the next safe action.

A healthy process may legitimately show no trade. A good analytical setup may stop upstream at TradePlan/Risk before the central Gate. Learning/browser/local-backup degradation may be visible without becoming analytical evidence.

## 2. Health topology

```text
process heartbeat
+ MT5 / account / symbol identity
+ market freshness/completeness
+ StateStore/checkpoint integrity
+ controller/fencing
+ session truth
+ News truth
+ reconciliation
+ Risk truth
+ learning queue/receipt
+ local backup health
→ HealthSnapshot
→ DashboardData / structured logs
```

## 3. Health dimensions

| Dimension | Healthy/known means | Degraded/block response |
|---|---|---|
| Process | heartbeat advances | investigate; liveness is not broker permission |
| MT5/identity | intended scope verified | hard block writes |
| Market data | required quote/bars satisfy policy | WAIT or hard block according to state |
| Freshness | quote/event/trigger current enough | visible stale/aging; no late send |
| Persistence | schema/integrity valid | recovery; no empty reset |
| Controller | current holder/epoch valid | fence writes |
| Session | broker schedule truth known | CLOSED/PRE_CLOSE/WARMUP/UNKNOWN per policy |
| News | current event context known/unknown truth | preserve actual state; known blackout hard |
| Reconciliation | lifecycle agrees with broker | reconcile before conflicting write |
| Risk | equity/cash-flow/lot/margin state known | upstream BLOCK/UNKNOWN |
| Learning | pending/complete evidence explicit | degrade learning only unless persistence itself unsafe |
| Local backup | latest package/checkpoint verified | no recoverability claim from failed artifact |
| Secondary UI | snapshot/server healthy | primary process independent |

## 4. State vocabularies are not interchangeable

Examples:

```text
DataQuality     HEALTHY / STALE / SPARSE / CORRUPT / UNKNOWN
MarketState     OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN
NewsState       CLEAR / BLACKOUT / UNKNOWN / POST_NEWS_WARMUP
TradePlan       READY / DEGRADED / INVALID
RiskState       NORMAL / LOSS_LOCKED / COOLDOWN / UNKNOWN
Central Gate    ALLOW / BLOCK / UNKNOWN / NOT_EVALUATED
Runtime Health  HEALTHY / DEGRADED / RECONCILING / BLOCKED
Runtime Role    READINESS / PRIMARY
```

The final `Market OPEN + News UNKNOWN` permission result follows the challenged Session/Risk contract; diagnostics must not assume it in advance.

## 5. Blocker-stage semantics

The operator must know **where** a candidate stopped:

```text
analytical WAIT/MISSED/INVALID
→ TradePlan blocker
→ Risk blocker
→ hard authority / actual central Gate
→ Intent / precheck / broker / reconciliation
```

`ENTRY_BLOCKED` alone is not proof Gate ran.

Presentation maps upstream rejection to `Gate NOT EVALUATED / WAIT`. Only actual Gate BLOCK displays `Gate BLOCKED`.

## 6. Stable reasons

Important block/degradation retains:

- stable machine reason;
- concise human explanation;
- scope/identity;
- observed value/threshold where relevant;
- UTC timestamp;
- next safe action where one exists.

Scalp-relevant examples include:

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
RECONCILIATION_PENDING
CONTROLLER_STALE
LOCAL_BACKUP_FAILED
```

Dashboard wording reflects owner policy; it does not hard-code unresolved thresholds.

## 7. Runtime maintenance lifecycle

Safe downstream work such as learning queue processing, local checkpoint maintenance and presentation may continue during recoverable waits where it does not rerun strategy or grant broker permission.

Graceful PRIMARY shutdown:

```text
stop new work
→ reconcile/stop as allowed
→ release controller + MT5 authority
→ fresh verified local checkpoint
→ secret/integrity scan
→ local backup catalog update
→ explicit success/failure
```

No Git commit/push exists in runtime health lifecycle.

## 8. Logging/redaction

Structured logs record lifecycle transitions, blockers, Intent/reconciliation, learning and local-backup events without giant snapshots or secrets.

Never log broker passwords, tokens/PATs, private keys or credential-bearing URLs.

## 9. Failure handling examples

| Failure | Truth | Response |
|---|---|---|
| MT5 init/identity failure | broker authority unavailable/mismatch | no writes |
| stale/insufficient/sparse data | recoverable wait if policy allows | dashboard alive |
| future/corrupt chronology | corrupt | hard block |
| stale trigger/event | analytical/execution timing no longer valid | WAIT/MISSED/BLOCK as owner specifies |
| SQLite integrity failure | state corrupt | recovery; no reset |
| controller loss | ownership lost | fence writes |
| ambiguous ack | lifecycle unresolved | reconcile only |
| known CLOSED + News unavailable | CLOSED + News UNKNOWN | session blocks |
| known blackout | BLACKOUT | hard new-entry block |
| session schedule unknown | UNKNOWN | fail closed |
| poor TradePlan geometry | upstream rejection | Gate not evaluated |
| risk/min-lot/margin failure | upstream monetary rejection | no Intent |
| secondary UI failure | presentation unavailable | PRIMARY continues |
| local final backup failure | recoverability degraded | explicit shutdown backup failure; keep last good state |

## 10. Source/proof map — intended

```text
market freshness      market_data/*
session/news          app/session_news.py + risk/permissions.py
blocker/Gate display  operator/presentation.py
recovery              app/recovery.py + recovery_mt5.py
controller            execution/controller.py
Intent/reconcile      execution/service.py + reconcile.py
learning queue        management/store.py + research/live_learning.py
local backup          persistence/checkpoint.py + backup.py + local_recovery_package.py
```

## 11. Evidence boundary

Deterministic tests prove state/reason/failure semantics. They do not prove real broker latency, future opportunity frequency, profitability, special holiday hours or fresh-machine broker continuity.
