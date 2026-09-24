# GoldScalpTrader — Execution and Broker Safety

**Status:** FROZEN V1 EXECUTION ARCHITECTURE — WRITER IMPLEMENTATION / DEMO PROOF PENDING
**Version:** 1.0-dryrun-demo-one-shot
**Authority:** READINESS/DRY_RUN/DEMO safety, account/symbol verification, final permission, fresh broker checks, one-shot requests, controller fencing and broker reconciliation.

## 1. Purpose

This is the final safety boundary before any irreversible MT5 create/modify/close operation.

> Analysis can be wrong and lose a trade. Execution safety must not create duplicate, wrong-account, wrong-symbol, wrong-volume or uncontrolled exposure.

Execution does not choose direction, improve a score or rewrite structural geometry.

## 2. V1 mode progression

```text
READINESS   read-only diagnostic
→ DRY_RUN   governed analytical/runtime lifecycle with zero irreversible writes
→ PRIMARY   controlled DEMO writer only after implementation + deterministic proof
REAL        deferred V1 / separate future governance decision
```

No hidden environment/config flag may silently grant REAL authority.

## 3. Sole write path

```text
approved TradePlan / management action
→ Risk + applicable hard authorities
→ central ExecutionPermissionGate
→ BLOCK/UNKNOWN: persist reason, no write
→ ALLOW: persist APPROVED ExecutionIntent
→ fresh account/terminal/symbol/quote/order prechecks
→ persist SUBMITTING before irreversible call
→ sole MT5Writer call
→ acknowledgement classification
→ broker reconciliation
→ persist verified lifecycle only from broker truth
```

Only the governed writer module may reach irreversible MT5 calls.

## 4. Ownership boundaries

| Boundary | Owner | Invariant |
|---|---|---|
| analytical approval | decisions/management | idea/action exists |
| monetary affordability | risk | no strategy authority |
| session/news/system permission | owning authorities + central Gate | BLOCK/UNKNOWN cannot pass |
| durable Intent | execution/intent_store.py | one Intent has at most one irreversible send allowance |
| raw broker write | execution/mt5_writer.py | sole irreversible boundary |
| broker outcome | execution/reconcile.py | acknowledgement is not final truth |
| controller | execution/controller.py | fresh holder/epoch required |

## 5. Central Gate inputs

For the requested action evaluate applicable:

- runtime mode / DEMO identity;
- exact account/server/symbol;
- fresh quote;
- SymbolSpec volume/stops/freeze/filling rules;
- current spread and adverse drift;
- TradePlan/event freshness and remaining room;
- STANDARD monetary Risk and margin;
- capacity / exposure / ownership;
- market/session/News policy;
- persistence/recovery state;
- unresolved Intent/order lifecycle;
- controller holder/fencing epoch;
- broker-native action precheck.

Hard BLOCK/UNKNOWN prevents write.

## 6. Upstream stop versus Gate

```text
TradePlan DEGRADED/INVALID or Risk BLOCK/UNKNOWN
→ central Gate may be NOT EVALUATED

actual Gate BLOCK
→ Gate BLOCKED

actual Gate UNKNOWN
→ Gate UNKNOWN / reconciling authority
```

Dashboard may present this truth but cannot alter it.

## 7. Fresh pre-submit barrier

Immediately before an irreversible call recheck official MT5 metadata appropriate to the action, including account trading permission, terminal/EA/API status, symbol trade mode/direction, account/server/symbol identity, fresh quote and broker-native `order_check` where applicable.

BUY uses Ask context; SELL uses Bid context.

Precheck failure results in zero `order_send` attempts for that Intent.

## 8. Scalp-specific execution friction

Execution revalidates at least:

- current spread;
- spread relative to approved healthy baseline if final policy uses one;
- spread relative to original SL / remaining target room;
- adverse drift from Approved Entry Reference;
- age of final analytical trigger/snapshot;
- broker check/send/reconcile timing where measurable.

Exact thresholds remain replay + connected DEMO calibration.

Execution cannot tighten SL or move target to force acceptable friction.

## 9. TradePlan cost split

TradePlan owns planning-time gross + cost-adjusted room using facts known then.

Execution owns last-moment current Bid/Ask/spread/drift validity.

The same cost source must not be charged twice across TradePlan/Risk/Execution.

## 10. Intent / idempotency

Lifecycle:

```text
CREATED
→ APPROVED
→ SUBMITTING
→ ACCEPTED_VERIFIED
→ ACCEPTED_UNKNOWN
→ FAILED
```

Persisting `SUBMITTING` consumes the one irreversible send allowance **before** raw broker call.

Ambiguous acknowledgement:

```text
ACCEPTED_UNKNOWN / reconciliation-only
→ inspect broker positions/orders/deals
→ never blind retry
```

A new attempt requires a new governed Intent only after prior truth is resolved.

## 11. Reconciliation

| Action | Required truth |
|---|---|
| OPEN | resulting position/order/deal lineage, symbol/direction/volume |
| MODIFY | exact ticket and actual broker SL/TP |
| CLOSE | position reduction/absence and exit-history proof where required |

Magic/comment are supporting lineage, not substitutes for broker truth. ManagedTrade changes only after verification.

## 12. Known managed position disappears

Reconcile unresolved Intent first, then require exact known ticket + official exit role + complete original exit volume + valid close time before archiving/learning/clearing active state. Partial/missing/ambiguous evidence remains RECONCILING.

## 13. Manual/foreign exposure

Unknown external Gold position is visible and blocks new bot entry. Bot never adopts/modifies/closes it.

A human close of an already-known bot ManagedTrade preserves bot-entry lineage but may have EXTERNAL/MIXED close attribution after exact proof.

## 14. Controller / writer scope

One active PRIMARY writer per account/symbol scope. Same-scope active-active is unsupported. Stale epoch is denied. Controller acquisition never substitutes for broker reconciliation.

## 15. Action-sensitive CLOSE

A governed CLOSE still requires correct account/symbol/ticket, controller, lifecycle ownership, executable quote, broker permission, one-shot Intent and reconciliation.

But discretionary OPEN friction rules such as elevated spread/healthy-baseline availability must not automatically trap unwanted exposure when CLOSE is the risk-reducing action.

## 16. Latency observability

Record where practical:

```text
snapshot/decision time
Intent approved/submitting time
order_check duration
order_send duration
acknowledgement time
reconciliation completion time
```

This is evidence/observability, not HFT capability. If final calibrated freshness rules are exceeded, rebuild/block rather than send late.

## 17. DRY_RUN semantics

DRY_RUN exercises as much of market → intelligence → strategies → Opportunity → timing → TradePlan → Risk → permission/Gate diagnostics as safely possible, but never reaches irreversible writer calls.

It can record “would otherwise proceed” and blockers but cannot fabricate fill/slippage/reconciliation/MAIN_DEMO proof.

## 18. Dashboard

Show mode, account/server/symbol, Bid/Ask/spread/quote age, blocker stage, Gate state, STANDARD Risk/capacity, Intent state/send count, broker-precheck reason, reconciliation, ownership, controller and useful latency diagnostics.

No dashboard control bypasses Gate.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/execution/models.py
src/gold_scalp_trader/execution/intent_store.py
src/gold_scalp_trader/execution/gate.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/controller.py
src/gold_scalp_trader/execution/sqlite_coordination.py
src/gold_scalp_trader/execution/mt5_writer.py
src/gold_scalp_trader/execution/service.py
src/gold_scalp_trader/execution/reconcile.py
src/gold_scalp_trader/app/recovery.py
```

`mt5_writer.py` remains absent/unimplemented until its deliberate milestone.

## 20. Planned proof / external evidence

Tests prove writer confinement, Gate BLOCK/UNKNOWN prevents write, exactly-one send allowance, persist-before-send, precheck failure zero sends, no blind retry, action-specific reconciliation, external-position non-adoption, stale controller denial, startup ordering, DRY_RUN no-write and action-sensitive CLOSE.

Connected Windows/Exness DEMO separately proves AutoTrading metadata, `order_check/order_send` retcodes, fill modes, stop/freeze rules, spread/slippage/latency and reconciliation.

## 21. Non-goals

Execution does not choose strategy, distort TradePlan, increase Risk from confidence, adopt foreign positions, infer zero exposure from failed reads, promise HFT latency or perform Git commit/push/pull.

## 22. Calibration pending

Spread/drift/trigger-age thresholds, healthy-spread baseline, slippage/deviation policy, acceptable decision latency, fill-mode/retcode support and controller lease/heartbeat values remain evidence questions.