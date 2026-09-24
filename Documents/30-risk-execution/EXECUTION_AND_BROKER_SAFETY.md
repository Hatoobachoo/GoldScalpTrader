# GoldScalpTrader — Execution and Broker Safety

**Status:** FROZEN V1 EXECUTION ARCHITECTURE — WRITER IMPLEMENTATION / CONNECTED DEMO PROOF PENDING
**Version:** 1.1-profiled-risk-future-real-one-shot
**Authority:** READINESS/DRY_RUN/controlled-DEMO safety, future governed REAL gate, account/symbol verification, final permission, fresh broker checks, one-shot requests, controller fencing and broker reconciliation.

## 1. Purpose

This is the final safety boundary before irreversible MT5 create/modify/close operation.

> Analysis can lose a trade. Execution safety must not create duplicate, wrong-account, wrong-symbol, wrong-volume or uncontrolled exposure.

Execution does not choose direction, improve score or rewrite structural geometry.

## 2. Capability progression

```text
READINESS   read-only diagnostic
→ DRY_RUN   governed analytical/runtime lifecycle with zero irreversible writes
→ PRIMARY   controlled DEMO writer after implementation + deterministic/recovery gates
→ REAL      preserved future governed capability after separate DEMO/release/explicit-approval gate
```

REAL is not removed, but no hidden environment/config flag may grant it. Its activation requires separate governed release authority.

## 3. Sole write path

```text
approved TradePlan / management action
→ active Risk profile/overlay + applicable hard authorities
→ central ExecutionPermissionGate
→ BLOCK/UNKNOWN: persist reason; no write
→ ALLOW: persist APPROVED ExecutionIntent
→ fresh account/terminal/symbol/quote/order prechecks
→ persist SUBMITTING before irreversible call
→ sole MT5Writer call
→ acknowledgement classification
→ broker reconciliation
→ persist verified lifecycle only from broker truth
```

## 4. Ownership boundaries

| Boundary | Owner | Invariant |
|---|---|---|
| analytical approval | decisions/management | idea/action exists |
| monetary affordability | Risk | active profile/overlay; no strategy authority |
| session/news/system permission | owning authorities + Gate | BLOCK/UNKNOWN cannot pass |
| durable Intent | execution/intent_store.py | one Intent has at most one irreversible send allowance |
| raw broker write | execution/mt5_writer.py | sole irreversible boundary |
| broker outcome | execution/reconcile.py | acknowledgement is not final truth |
| controller | execution/controller.py | fresh holder/epoch required |

## 5. Central Gate inputs

For requested action evaluate applicable:

- runtime capability/mode and DEMO/REAL release identity;
- exact account/server/symbol;
- fresh quote;
- SymbolSpec volume/stops/freeze/filling rules;
- current spread and adverse drift;
- TradePlan/event freshness and remaining room;
- current monetary RiskEvaluation using preserved SMALL/MEDIUM/NORMAL profile or explicitly enabled eligible aggressive overlay;
- margin/capacity/exposure/ownership;
- market/session/News policy;
- persistence/recovery state;
- unresolved Intent/order lifecycle;
- controller holder/fencing epoch;
- broker-native action precheck.

Hard BLOCK/UNKNOWN prevents write.

## 6. Upstream stop versus Gate

```text
TradePlan DEGRADED/INVALID or Risk BLOCK/UNKNOWN
→ Gate may be NOT EVALUATED

actual Gate BLOCK
→ Gate BLOCKED

actual Gate UNKNOWN
→ Gate UNKNOWN / reconciling authority
```

Dashboard cannot alter this truth.

## 7. Fresh pre-submit barrier

Immediately before irreversible call recheck official MT5 metadata appropriate to action: trading permission, terminal/EA/API status, symbol mode/direction, account/server/symbol identity, fresh quote and broker-native `order_check` where applicable.

BUY uses Ask context; SELL uses Bid context.

Precheck failure means zero `order_send` attempts for that Intent.

## 8. Scalp-specific execution friction

Revalidate current spread, spread relative to approved healthy baseline if policy uses one, spread relative to original SL/remaining target room, adverse drift from Approved Entry Reference, final trigger/snapshot age and measurable check/send/reconcile timing.

Exact thresholds remain genuine scalp replay + connected DEMO calibration. Execution cannot tighten SL or move target to force acceptable friction.

## 9. TradePlan cost split

TradePlan owns planning-time gross + cost-adjusted room using facts known then. Execution owns last-moment current Bid/Ask/spread/drift validity. Same cost source cannot be charged twice.

## 10. Intent / idempotency

```text
CREATED
→ APPROVED
→ SUBMITTING
→ ACCEPTED_VERIFIED
→ ACCEPTED_UNKNOWN
→ FAILED
```

Persisting `SUBMITTING` consumes the one irreversible send allowance **before** raw call.

Ambiguous acknowledgement:

```text
ACCEPTED_UNKNOWN / reconciliation-only
→ inspect broker positions/orders/deals
→ never blind retry
```

A new governed Intent is allowed only after prior truth resolves.

## 11. Reconciliation

| Action | Required truth |
|---|---|
| OPEN | resulting position/order/deal lineage, symbol/direction/volume |
| MODIFY | exact ticket and actual broker SL/TP |
| CLOSE/PARTIAL CLOSE | verified position reduction/absence and exit-history proof |

Magic/comment support lineage but do not replace broker truth. ManagedTrade changes only after verification.

## 12. Known managed position disappears

Reconcile unresolved Intent first, then require exact known ticket + official exit role + complete exit-volume evidence + valid close time before archive/learning/clear. Partial/missing/ambiguous evidence remains RECONCILING.

## 13. Manual/foreign exposure

Unknown external Gold position is visible and blocks new bot entry. Bot never silently adopts/modifies/closes it.

A human close of an already-known bot ManagedTrade preserves bot-entry lineage with EXTERNAL/MIXED close attribution after exact proof.

## 14. Controller / writer scope

One active PRIMARY writer per account/symbol scope. Same-scope active-active is unsupported in current local-state design. Stale epoch is denied. Controller acquisition never substitutes for broker reconciliation.

## 15. Action-sensitive CLOSE

Governed CLOSE requires correct identity/ticket, controller, lifecycle ownership, executable quote, broker permission, one-shot Intent and reconciliation.

Discretionary OPEN friction rules must not automatically trap unwanted exposure when CLOSE is risk-reducing.

## 16. Latency observability

Record snapshot/decision time, Intent approved/submitting, order_check duration, order_send duration, acknowledgement and reconciliation completion where practical.

This is evidence/observability, not HFT capability. If final calibrated freshness rules are exceeded, rebuild/block rather than send late.

## 17. DRY_RUN semantics

DRY_RUN exercises market → bounded analytical desks/families → Opportunity → timing → TradePlan → profiled Risk → permission/Gate diagnostics as safely possible, but never reaches irreversible writer.

It may record “would otherwise proceed” and blockers but cannot fabricate fills/slippage/reconciliation/DEMO proof.

## 18. Dashboard

Show capability stage, account/server/symbol, Bid/Ask/spread/quote age, blocker stage, Gate, active Risk profile/overlay/capacity, Intent/send count, precheck reason, reconciliation, ownership, controller and latency diagnostics.

No dashboard control bypasses Gate or REAL release gate.

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

`mt5_writer.py` remains absent/unimplemented until deliberate controlled-DEMO milestone.

## 20. Planned proof / external evidence

Tests prove writer confinement, Gate BLOCK/UNKNOWN no-write, one send allowance, persist-before-send, precheck failure zero sends, no blind retry, OPEN/MODIFY/CLOSE/PARTIAL reconciliation, external-position non-adoption, stale-controller denial, startup ordering, DRY_RUN no-write and action-sensitive CLOSE.

Connected Windows/Exness DEMO separately proves actual AutoTrading metadata, `order_check/order_send`, fill modes, stop/freeze rules, spread/slippage/latency and reconciliation.

Future REAL release requires separate explicit evidence/approval packet; DEMO proof alone does not auto-enable REAL.

## 21. Non-goals

Execution does not choose strategy, distort TradePlan, increase Risk from confidence, adopt foreign positions, infer zero exposure from failed reads, promise HFT latency, perform runtime Git operations or remove preserved future REAL capability by documentation shorthand.

## 22. Scalp calibration pending

Spread/drift/trigger-age thresholds, healthy-spread baseline, slippage/deviation policy and acceptable decision latency remain genuine scalp evidence questions. Fill-mode/retcode/controller values also require implementation/connected proof.