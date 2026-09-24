# GoldScalpTrader — Live DEMO Trade Learning Pipeline

**Status:** DRAFT PRE-CHALLENGE SOFTWARE CONTRACT
**Version:** 0.1-scalp-causal-learning
**Authority:** Automatic verified DEMO trade outcome capture, broker-side close recovery, passive post-close learning, evidence quality and exactly-once StrategyMemory ingestion.

## 1. Purpose

When future governed DEMO execution exists, an actual bot trade must not disappear into a P/L number after close.

The system must preserve:

- which family/thesis created it;
- exact Opportunity/TradePlan lineage;
- approved entry reference versus actual fill;
- original R;
- what market path followed;
- how long the scalp lasted;
- spread/slippage/latency evidence where available;
- how efficiently entry/exit performed;
- which policy version owned the decision.

> Learn only from an already-known bot ManagedTrade whose close is positively proven from broker lineage and whose context can be reconstructed causally.

Learning cannot create broker authority, relax risk or convert UNKNOWN into PASS.

## 2. Supported close paths

The intended DEMO software contract covers a known ManagedTrade closed by:

- governed bot EXIT;
- broker stop-loss;
- broker take-profit;
- manual/operator close of that exact known position;
- multi-deal/partial execution that eventually proves the full volume closed.

Unknown external positions are never adopted into learning.

A manual close of a known bot trade preserves original bot ownership but records closing origin as EXTERNAL/MIXED where broker evidence says so.

## 3. Authority flow

```text
READY TradePlan
→ verified broker OPEN
→ durable ManagedTrade + frozen learning identity
→ governed EXIT or broker-side verified close
→ durable close archive
→ learning queue + closure receipt
→ clear active ManagedTrade safely
→ re-verify broker close/outcome
→ reconstruct causal M5/M15/H1 path/context
→ one MAIN_DEMO LearningObservation
→ StrategyMemory
→ local verified backup
```

No step in learning calls the broker writer.

## 4. Learning identity frozen at entry

ManagedTrade freezes at least:

```text
strategy_family
approved_entry_reference
policy_version
direction
original_r_price
actual entry price
position ticket
TradePlan ID
Opportunity ID
Episode ID
entry timestamp
session/regime identifiers
```

Later policy edits cannot relabel history.

If legacy data lacks required identity, keep it recoverable/manageable but do not invent missing learning facts.

## 5. Crash-safe close archive

A verified close is financial lifecycle truth. Learning failure must never delay/undo closure.

Required order:

```text
1. persist closed_trade_learning_queue item
2. persist managed_trade_closure_receipt
3. clear active ManagedTrade after verified close
4. retire matching TradePlan/Opportunity in crash-safe order
5. later build StrategyMemory observation
6. remove queue only after durable observation save
```

Restart repeats idempotently from durable source identity.

## 6. Closure receipt

The receipt persists even after learning queue consumption.

It stores exact lifecycle identity, position ticket, plan/opportunity/episode IDs, symbol, verified close time and close origin/reason.

This prevents restart from interpreting an old verified OPEN as unexplained missing ManagedTrade context.

Same source with conflicting closure evidence is an integrity failure.

## 7. ExecutionIntent precedence

Passive close recovery never bypasses uncertain execution state.

```text
SUBMITTING / ACCEPTED_UNKNOWN Intent
→ normal Intent reconciliation first
→ unresolved → RECONCILING / stop
→ resolved → inspect ManagedTrade/broker close state
```

This prevents a manual/SL/TP inference from hiding an ambiguous broker write.

## 8. Broker-side close proof

Read-only reconciliation receives the already-known ManagedTrade identity.

Required proof includes:

```text
exact durable position ticket
AND official broker exit role
AND positive finite deal volume
AND summed exit volume == original managed volume within strict tolerance
AND trustworthy UTC deal timestamp
```

Origin classification across matched exit deals:

```text
all bot identity → BOT
none             → EXTERNAL
mixture          → MIXED
```

EXTERNAL is valid only for the exact already-known bot position.

Incomplete history/volume/entry-role truth remains RECONCILING.

## 9. Pending learning queue

Queue source identity should be stable, e.g.:

```text
managed-trade:<immutable-trade-id>
```

Queue item carries frozen ManagedTrade evidence plus verified close time/reason/origin.

Rules:

- same source/same evidence = idempotent;
- same source/different evidence = explicit conflict;
- corruption never becomes empty queue;
- queue removed only after durable StrategyMemory save;
- full local checkpoints preserve pending queue automatically.

## 10. Broker outcome re-verification

Before creating a final learning observation, the learning processor re-reads normalized broker DealFacts rather than trusting one transient in-memory close result.

It again proves ticket, full exit volume, valid exit roles and ownership/origin.

It derives volume-weighted actual exit price and broker net trade money from the complete exit set.

## 11. Realized R

Where broker tick-money geometry is valid:

```text
risk_money = (original_r_price / tick_size) × tick_value × volume
realized_R = broker_net_trade_result / risk_money
```

If reliable money geometry is unavailable, actual exit-price R may be used from verified entry/exit price and original R distance.

Account-level equity change is never substituted for missing trade-level evidence.

## 12. Entry efficiency and execution quality

Draft adverse-entry slippage metric:

```text
BUY  adverse_slippage_R = max(0, actual_fill - approved_entry_reference) / original_R
SELL adverse_slippage_R = max(0, approved_entry_reference - actual_fill) / original_R
EntryEfficiency = clamp(1 - adverse_slippage_R, 0, 1)
```

Scalp learning should also retain where observable:

- signal spread;
- final pre-submit spread;
- fill drift;
- check/send/reconcile durations;
- trigger age at submit;
- cost as fraction of gross target/R.

Missing measurements remain missing, not zero.

## 13. MFE / MAE and causal bar boundaries

MT5 candle timestamp is bar open. Excursion metrics may use only completed bars causally contained inside actual trade interval:

```text
bar_open >= verified entry time
AND
bar_close <= verified close time
```

Boundary bars that begin before entry or close after exit are excluded unless future tick-level data supports exact slicing.

Exact broker exit price remains separately included.

For BUY:

```text
MFE_R = max(high - entry) / original_R
MAE_R = max(entry - low) / original_R
```

SELL is symmetric.

Capture Efficiency can compare realized R against positive MFE_R with bounded interpretation.

## 14. Scalp duration metrics

Add explicit short-horizon metrics:

- seconds/minutes in trade;
- completed M5 bars fully inside trade;
- time to MFE;
- time to first +0.5R / +1R or researchable thresholds;
- time spent stagnant before exit;
- whether time/efficiency EXIT occurred;
- whether trade unintentionally exceeded intended scalp lifecycle.

Threshold interpretation remains governed research, not live self-editing.

## 15. Causal regime/session at entry

Entry session uses immutable entry timestamp.

Entry H1/M15 regime requests enough historical data to reach the original entry and includes only bars/facts knowable by entry time.

A later-completed candle may not retroactively improve the stored entry regime.

## 16. Exactly-once StrategyMemory

Environment identity for actual future governed DEMO outcome:

```text
MAIN_DEMO
```

The queue source ID is reused for StrategyMemory:

- first valid save → one observation;
- identical retry → idempotent;
- conflicting retry → integrity error;
- queue removed after durable success only.

## 17. Failure semantics

| Condition | Behaviour |
|---|---|
| unresolved Intent | reconcile first |
| known position missing/no complete exit proof | retain ManagedTrade, RECONCILING |
| partial exit | no full-close learning yet |
| exact manual close | learn original bot trade with EXTERNAL/MIXED close origin |
| unknown manual position | never adopt |
| path data unavailable/corrupt | keep learning pending or store reduced-quality evidence explicitly |
| boundary bar partial | exclude from bar-extreme metrics |
| required frozen identity missing | do not invent |
| StrategyMemory write fails | keep queue |
| duplicate conflicting source | integrity error |

## 18. Local backup / laptop handoff

Queue, closure receipt and StrategyMemory live in canonical StateStore and therefore in full verified local checkpoints.

GoldScalpTrader does not publish learning automatically to GitHub at shutdown.

Same-scope handoff:

```text
old PRIMARY stopped
→ verified local checkpoint/recovery package
→ restore new DB
→ broker reconciliation
→ new PRIMARY only after authorities pass
```

One production learning writer per account/symbol scope.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/management/models.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/management/execution.py
src/gold_scalp_trader/execution/reconcile.py
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/research/learning.py
```

## 20. Planned deterministic proof

Tests must cover frozen learning identity, governed EXIT archive, SL/TP/manual exact-close recovery, full-volume requirement, Intent precedence, queue/receipt durability, delayed-restart history reconstruction, causal bar boundaries, realized R, entry efficiency, MFE/MAE, scalp-duration metrics, exactly-once memory and local-backup preservation.

Connected Exness DEMO evidence remains required for real deal-history timing, SL/TP attribution and broker fields.

## 21. Evidence boundary

Implementing this pipeline proves learning correctness mechanics—not profitability, useful adaptation or future strategy edge.
