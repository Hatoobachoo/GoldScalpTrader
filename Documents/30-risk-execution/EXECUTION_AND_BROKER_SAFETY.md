# GoldScalpTrader — Execution and Broker Safety

**Status:** DRAFT PRE-CHALLENGE EXECUTION CONTRACT
**Version:** 0.1-scalp-one-shot-execution
**Authority:** DRY_RUN/DEMO safety, account/symbol verification, final permission, fresh broker checks, one-shot requests, controller fencing and broker reconciliation.

## 1. Purpose

This is the last safety boundary before an irreversible MT5 create, modify or close operation.

> Analysis can be wrong and lose a trade. Execution safety must not create duplicate, wrong-account, wrong-symbol, wrong-volume or uncontrolled exposure.

Execution does not choose direction, improve a score, rewrite structural invalidation or adopt foreign positions.

## 2. Initial release-mode boundary

Current project development remains `DRY_RUN` first.

No live/DEMO broker write should exist until the documentation/manual is challenged, frozen and the execution milestone is deliberately implemented.

When broker-write capability is later introduced, the intended progression is:

```text
READINESS / observation
→ DRY_RUN analytical lifecycle
→ controlled DEMO-only governed execution
→ any later REAL capability requires a separate explicit governance decision
```

There is no hidden environment flag that silently grants REAL authority.

## 3. Sole broker-write path

Intended production path:

```text
approved TradePlan / management action
→ applicable hard authorities
→ central ExecutionPermissionGate
→ if BLOCK/UNKNOWN: persist reason, no write
→ if ALLOW: persist APPROVED ExecutionIntent
→ fresh account/terminal/symbol/order prechecks
→ persist SUBMITTING before irreversible call
→ sole MT5Writer call
→ acknowledgement classification
→ broker reconciliation
→ persist verified lifecycle
```

Only the governed writer module may reach irreversible MT5 create/modify/close calls.

## 4. Ownership boundaries

| Boundary | Planned owner | Invariant |
|---|---|---|
| analytical approval | decisions/management | idea/action exists |
| monetary risk | risk | affordability only |
| hard permission | risk/session/execution gate | BLOCK/UNKNOWN cannot pass |
| durable Intent | execution/intent_store.py | one Intent has at most one irreversible send allowance |
| raw MT5 write | execution/mt5_writer.py | sole irreversible boundary |
| current broker outcome | execution/reconcile.py | acknowledgement is not final truth |
| controller | execution/controller.py | fresh holder/epoch required |

## 5. Central Gate inputs

For the requested action, evaluate applicable:

- runtime mode / DEMO guard when write-capable mode exists;
- exact account/server identity;
- resolved Gold symbol;
- current quote and freshness;
- SymbolSpec / volume / stop / freeze / filling rules;
- current spread and adverse drift;
- TradePlan freshness / target-room validity;
- monetary risk and margin;
- capacity / exposure / ownership;
- market session and News policy;
- persistence/recovery state;
- unresolved Intent/order lifecycle;
- controller holder/fencing epoch;
- action-specific broker-native precheck.

`BLOCK` and hard `UNKNOWN` prevent the write.

## 6. Upstream stop versus central Gate

A candidate may stop before the central Gate because:

```text
TradePlan DEGRADED/INVALID
Risk BLOCK/UNKNOWN
entry pipeline missing required state
```

Therefore a broad runtime action like `ENTRY_BLOCKED` does not prove the central Gate returned BLOCK.

Dashboard semantics must distinguish:

```text
upstream TradePlan/Risk stop → Gate NOT EVALUATED / WAIT
actual Gate BLOCK            → Gate BLOCKED
actual Gate UNKNOWN          → unresolved/checking authority
```

Presentation is read-only and cannot modify permission.

## 7. Fresh broker permission barrier

Immediately before an irreversible broker call, recheck official MT5 metadata appropriate to the action, such as:

```text
account trading allowed
expert/EA trading allowed where applicable
terminal AutoTrading / trade API status
symbol trade mode and direction
current account/server/symbol identity
fresh quote
broker-native order_check(request)
```

A precheck failure results in zero `order_send` attempts for that Intent.

A partial/incomplete permission metadata surface is not interpreted optimistically.

BUY uses current Ask context; SELL uses current Bid context.

## 8. Scalp-specific execution friction

Spread, drift and latency matter materially more for a scalp because intended reward distance is smaller.

Execution must measure/revalidate at least:

- current spread in price/points;
- spread relative to recent healthy baseline;
- spread relative to original SL distance;
- spread relative to remaining target room;
- adverse drift from approved entry reference;
- elapsed age from final analytical snapshot/trigger;
- broker check/submit/reconcile timing where measurable.

The reference system's numerical spread/drift thresholds are **not automatically frozen** for GoldScalpTrader.

Exact thresholds require replay + connected Exness DEMO evidence.

Execution never tightens structural SL merely to make friction acceptable.

## 9. Healthy spread baseline

A persistent runtime may derive a robust healthy-spread baseline from completed/verified broker observations where the final design approves it.

Requirements:

- bounded historical window;
- exclude stale/corrupt/closed-market observations;
- explicit operator override only when positive/valid;
- baseline provenance visible;
- missing baseline becomes explicit degraded/UNKNOWN context according to action policy.

For OPEN, poor/unknown cost conditions may block according to final policy. For mandatory risk-reducing CLOSE, elevated spread should not automatically trap exposure when broker execution is otherwise possible.

## 10. ExecutionIntent lifecycle and idempotency

Draft lifecycle:

```text
CREATED
→ APPROVED
→ SUBMITTING
→ ACCEPTED_VERIFIED
→ ACCEPTED_UNKNOWN
→ FAILED
```

Persisting `SUBMITTING` consumes the one irreversible send allowance **before** the raw broker call.

One Intent ID may cause at most one irreversible request.

If acknowledgement is ambiguous:

```text
ACCEPTED_UNKNOWN / reconciliation-only
→ inspect broker positions/orders/deals
→ never blind retry
```

If later proof shows no effect, any new attempt requires a new governed Intent after truth is resolved.

## 11. Action-specific reconciliation

| Action | Required reconciliation concept |
|---|---|
| OPEN | prove resulting position/order/deal lineage, symbol, direction and volume |
| MODIFY | verify exact ticket and actual broker SL/TP |
| CLOSE | prove position reduction/absence and exit history where required |

Magic/comment are supporting lineage, not substitutes for broker truth.

Local ManagedTrade state changes only after broker verification.

## 12. Known managed position disappears

If durable ManagedTrade ticket is missing from current positions:

```text
unresolved ExecutionIntent?
→ reconcile it first
→ if unresolved: RECONCILING
→ else read normalized broker exit history
→ require exact ticket + official exit role + complete original exit volume + valid close time
→ only then archive close / receipt / learning queue / clear active trade
```

Partial/missing/ambiguous evidence remains RECONCILING.

## 13. Manual/foreign exposure

```text
unknown manual/foreign Gold position
→ visible External Open
→ new bot entry blocked
→ bot never adopts/modifies/closes it
```

A human closing an **already-known bot ManagedTrade** is a different case. Original ownership remains bot lineage while closing action origin may be EXTERNAL/MIXED after exact broker proof.

## 14. Controller and writer scope

Initial V1 target:

```text
one active PRIMARY writer per account/symbol scope
fresh controller holder + monotonic fencing epoch before irreversible write
local SQLite coordination unless challenge changes backend
same-scope cross-laptop active-active unsupported
```

A stale old epoch is denied.

A higher epoch after takeover-like state still requires reconciliation; epoch alone is not broker-write permission.

Different independent account/symbol scopes may have separate runtimes/state.

## 15. Startup recovery integration

Recovery itself performs no raw broker write.

It validates:

- StateStore integrity;
- current account/server/symbol;
- unresolved Intent;
- ManagedTrade vs current broker positions;
- exact known-position close proof when necessary;
- risk/session/news/exposure authorities;
- controller ownership/epoch.

Any unresolved hard authority prevents write-capable READY.

Even after startup READY, fresh execution metadata/order checks are repeated immediately before each irreversible action.

## 16. Action-sensitive CLOSE safety

CLOSE reduces exposure and should not inherit every discretionary OPEN veto mechanically.

A governed CLOSE still requires:

- correct account/symbol/ticket;
- controller authority;
- valid lifecycle ownership;
- fresh executable quote where required;
- broker trade permission/order-check;
- one-shot Intent;
- reconciliation.

But elevated spread or missing healthy-spread baseline may be diagnostic rather than veto if vetoing would deliberately retain unwanted risk.

Exact action policy must be frozen jointly with the Session/Risk state machine.

## 17. Latency observability

GoldScalpTrader should record bounded timing diagnostics where practical:

```text
snapshot_completed_at
analytical_decision_at
Intent approved/submitting time
order_check duration
order_send duration
acknowledgement time
reconciliation completion time
```

This is observability, not a claim of HFT capability.

If measured processing delay makes the trigger/quote too stale under final policy, the entry should be rebuilt/blocked rather than sent late.

## 18. Runtime failure states

Representative reasons:

```text
PRE_SUBMIT_BLOCK
BROKER_REJECTED
AMBIGUOUS_ACK
ACCEPTED_VERIFIED
RECONCILIATION_FAILED
AUTOTRADING_DISABLED
TRADE_API_DISABLED
SYMBOL_CLOSE_ONLY
SYMBOL_DIRECTION_NOT_ALLOWED
CONTROLLER_STALE
STARTUP_RECOVERY_NOT_READY
SPREAD_TOO_WIDE
PRICE_DRIFT_TOO_LARGE
TRIGGER_STALE
```

Names may change during implementation but semantics must remain stable/auditable.

## 19. DRY_RUN semantics

DRY_RUN must exercise as much of the analytical/TradePlan/Risk/Gate decision path as safely possible without reaching raw irreversible broker calls.

It should preserve:

- Would Otherwise Trade where meaningful;
- exact upstream/gate blocker;
- proposed TradePlan/Risk result;
- current quote/spread/drift diagnostics;
- no fake `ACCEPTED_VERIFIED` broker state.

DRY_RUN cannot be used to claim real fill/slippage/reconciliation proof.

## 20. Dashboard/operator visibility

Show authoritative facts where available:

```text
runtime mode
account/server/symbol identity
current Bid/Ask / spread / quote age
Gate state
upstream blocker stage
Risk/capacity
Intent ID/state/send count
broker precheck reason
reconciliation state
bot vs external ownership
controller holder/epoch
latency diagnostics where useful
```

No dashboard control can bypass the Gate.

## 21. Planned implementation ownership

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

`mt5_writer.py` remains absent/unimplemented until the documented execution milestone is deliberately reached.

## 22. Planned deterministic proof

Tests must prove:

- raw writer confinement;
- Gate BLOCK/UNKNOWN prevents write;
- exactly one send allowance per Intent;
- persist-before-send;
- precheck failure → zero sends;
- ambiguous ack → no blind retry;
- action-specific reconciliation;
- foreign position non-adoption;
- known managed close proof;
- stale controller/fencing denial;
- startup recovery ordering;
- DRY_RUN cannot reach irreversible writer;
- truthful upstream-vs-Gate presentation;
- action-sensitive mandatory CLOSE behaviour.

Connected Windows/Exness DEMO evidence separately proves real AutoTrading metadata, order_check/order_send/retcodes, spread/slippage, fill modes, stop/freeze rules, latency and reconciliation.

## 23. Non-goals

Execution must not:

- choose strategy direction;
- change TradePlan geometry to force a fill;
- increase risk because confidence is high;
- adopt unknown manual positions;
- blind retry uncertain sends;
- allow multiple raw writer paths;
- infer zero exposure from failed reads;
- treat DRY_RUN as broker proof;
- promise HFT/zero latency;
- auto-push anything to GitHub.

## 24. Pre-challenge questions

- final DRY_RUN→DEMO promotion boundary;
- exact spread/drift/trigger-age thresholds;
- healthy spread baseline method/window;
- slippage/deviation policy;
- acceptable end-to-end decision latency;
- supported filling modes/retcodes;
- controller lease/heartbeat values;
- whether REAL trading is permanently out of scope or a separately governed future phase.
