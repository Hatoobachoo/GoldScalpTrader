# GoldScalpTrader — Live DEMO Trade Learning Pipeline

**Status:** FROZEN V1 DEMO-LEARNING SOFTWARE CONTRACT — IMPLEMENTATION / CONNECTED PROOF PENDING
**Version:** 1.0-causal-exactly-once-learning
**Authority:** Automatic verified DEMO trade outcome capture, broker-side close recovery, passive post-close learning, evidence quality and exactly-once StrategyMemory ingestion.

## 1. Purpose

When governed DEMO execution exists, an actual bot trade must not disappear into only a P/L number after close.

Preserve family/thesis, Opportunity/TradePlan lineage, approved reference versus fill, original R, market path, duration, spread/slippage/latency evidence, entry/exit efficiency and policy/Risk-profile identity.

> Learn only from an already-known bot ManagedTrade whose close is positively proven from broker lineage and whose context can be reconstructed causally.

Learning cannot create broker authority, relax Risk or convert UNKNOWN into PASS.

## 2. Supported close paths

Known ManagedTrade may close by governed bot EXIT, broker SL, broker TP, manual/operator close of that exact known position, or multi-deal/partial execution that eventually proves full volume closed.

Unknown external positions are never adopted into learning. Manual close of known bot trade preserves bot-entry lineage and records EXTERNAL/MIXED close origin where proven.

## 3. Authority flow

```text
READY TradePlan
→ active preserved Risk profile/optional overlay
→ verified broker OPEN
→ durable ManagedTrade + frozen learning identity
→ governed EXIT or broker-side verified close
→ durable close archive
→ learning queue + closure receipt
→ safe active-state clear
→ re-verify broker outcome
→ reconstruct causal H1/M15/M5 path/context
→ one MAIN_DEMO LearningObservation
→ StrategyMemory
→ local verified backup
```

No learning step calls broker writer.

## 4. Learning identity frozen at entry

Freeze at least:

```text
strategy_family
approved_entry_reference
policy_version
risk_profile SMALL / MEDIUM / NORMAL
aggressive_overlay_enabled true/false
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

Later policy edits cannot relabel history. Missing legacy facts are never invented.

## 5. Crash-safe close archive

```text
1. persist closed_trade_learning_queue item
2. persist managed_trade_closure_receipt
3. clear active ManagedTrade after verified close
4. retire matching TradePlan/Opportunity safely
5. later build StrategyMemory observation
6. remove queue only after durable observation save
```

Restart repeats idempotently from durable identity.

## 6. Closure receipt

Receipt persists after learning queue consumption and retains lifecycle identity, position ticket, plan/opportunity/episode IDs, symbol, close time and close origin/reason.

Same source with conflicting closure evidence is integrity failure.

## 7. ExecutionIntent precedence

```text
SUBMITTING / ACCEPTED_UNKNOWN Intent
→ reconcile Intent first
→ unresolved → RECONCILING / stop
→ resolved → inspect ManagedTrade/broker close state
```

Passive close inference never hides ambiguous broker write.

## 8. Broker-side close proof

Require exact durable position ticket, official exit role, positive finite deal volume, summed exit volume equal to original managed volume within strict tolerance and trustworthy UTC deal timestamp.

Origin across matched exits:

```text
all bot identity → BOT
none             → EXTERNAL
mixture          → MIXED
```

Incomplete history/volume/role remains RECONCILING.

## 9. Partial-management boundary

Preserved broker-valid partial management may generate intermediate exit deals, but **full-close learning is not emitted until full managed volume is positively reconciled closed**.

Intermediate partial actions may be stored as management evidence. An indivisible minimum-lot position simply has no partial action; learning correctness never depends on partial close.

## 10. Pending learning queue

Stable source identity such as:

```text
managed-trade:<immutable-trade-id>
```

Rules: same source/same evidence idempotent; same source/different evidence conflict; corruption never empty queue; queue removed only after durable memory save; checkpoints preserve pending queue.

## 11. Broker outcome re-verification

Before final observation, re-read normalized DealFacts and re-prove ticket/full exit volume/roles/origin. Derive volume-weighted exit price and broker net trade money from complete exit set.

## 12. Realized R

Where money geometry is valid:

```text
risk_money = (original_r_price / tick_size) × tick_value × volume
realized_R = broker_net_trade_result / risk_money
```

Otherwise verified price-R may be used when supported. Account-level equity change is never substituted for missing trade-level evidence.

## 13. Entry/execution quality

Retain where observable approved-reference-to-fill drift, spread at signal/check/send/fill, adverse slippage, check/send/reconcile timings, trigger age and cost as fraction of gross target/original R.

Missing measurements remain missing.

## 14. MFE / MAE causal boundary

Completed-bar excursion estimate uses only bars causally contained in trade interval:

```text
bar_open >= verified entry time
AND
bar_close <= verified close time
```

Boundary bars are excluded unless future tick-accurate data proves exact path. M1 remains diagnostic/research only and cannot be used as hidden production authority simply because it is available for analysis.

## 15. Scalp duration metrics

Track seconds/minutes in trade, completed M5 bars fully inside trade, time to MFE, time to research thresholds, stagnant duration, time-efficiency EXIT and accidental swing-conversion indicators.

Interpretation remains research, not live self-editing.

## 16. Causal session/regime at entry

Entry session/regime uses immutable entry timestamp and only facts knowable then. Later-completed bars never retroactively improve stored context.

## 17. Exactly-once StrategyMemory

Current actual governed DEMO environment identity:

```text
MAIN_DEMO
```

First valid source save → one observation; identical retry → idempotent; conflicting retry → integrity error; queue removed after durable success only.

Future governed REAL capability may later define a distinct approved evidence environment; DEMO records are never relabelled REAL.

## 18. Failure semantics

| Condition | Behaviour |
|---|---|
| unresolved Intent | reconcile first |
| known position missing/no complete exit proof | retain ManagedTrade, RECONCILING |
| partial exit | no full-close observation yet |
| exact manual close | learn original bot trade with EXTERNAL/MIXED origin |
| unknown manual position | never adopt |
| path data unavailable/corrupt | pending or explicit reduced-quality evidence |
| required frozen identity missing | never invent |
| StrategyMemory write fails | keep queue |
| duplicate conflicting source | integrity error |

## 19. Local backup / laptop handoff

Queue, receipt and StrategyMemory live in canonical StateStore/full local checkpoints. No learning publication to GitHub occurs at shutdown.

Same-scope handoff is sequential stop → verified checkpoint/package → new DB restore → fresh broker reconciliation → controller acquisition → READY.

## 20. Planned implementation ownership

```text
src/gold_scalp_trader/management/models.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/management/execution.py
src/gold_scalp_trader/execution/reconcile.py
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/research/live_learning.py
src/gold_scalp_trader/research/learning.py
```

## 21. Planned proof / evidence boundary

Tests cover frozen family/profile/overlay identity, EXIT/SL/TP/manual close recovery, partial-to-full-volume handling, Intent precedence, queue/receipt durability, delayed restart, causal path boundaries, realized R, efficiency/MFE/MAE/duration and exactly-once memory.

Connected Exness DEMO proves real deal-history timing/fields. Correct learning mechanics do not prove profitable adaptation.