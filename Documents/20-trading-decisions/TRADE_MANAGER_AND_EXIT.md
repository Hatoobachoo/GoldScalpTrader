# GoldScalpTrader — Trade Manager and Exit

**Status:** DRAFT PRE-CHALLENGE MANAGEMENT CONTRACT
**Version:** 0.1-scalp-management
**Authority:** Post-entry management, structural protection, time/efficiency exits, target progression, modify/close decisions, broker-verified lifecycle updates and verified-close learning handoff.

## 1. Purpose and boundary

Trade Manager is the post-entry decision floor for a verified bot-owned Gold position.

It observes fresh structure, continuation, reversal, target, session and execution-condition facts and returns a governed action such as:

```text
HOLD
PROTECT
TRAIL
RUNNER
EXIT
```

For scalping, the challenge may add explicit `TIME_EXIT` or keep time-based logic as an EXIT reason rather than a separate action.

Trade Manager never creates a new entry thesis. Every modify/close action uses the same identity/controller/Gate/Intent/writer/reconciliation safety spine as entry.

## 2. Management pipeline

```text
verified bot-owned broker position
+ ManagedTrade + original R/objectives
→ fresh MarketSnapshot / IntelligenceSnapshot
→ continuation / reversal / structure / momentum / path / time-in-trade
→ HOLD / PROTECT / TRAIL / RUNNER / EXIT
→ action-specific hard checks
→ durable MODIFY/CLOSE Intent
→ sole broker writer
→ reconciliation
→ persist state only after broker verification
→ verified full close receipt/queue
→ downstream learning
```

Local state must never claim a modification/close succeeded before broker truth proves it.

## 3. Scalp management priorities

Compared with swing trading, GoldScalpTrader gives greater importance to:

- time in trade;
- speed/efficiency of progress after entry;
- rapid invalidation of the exact M5 thesis;
- spread/market deterioration;
- session transition/close proximity;
- avoiding turning a failed scalp into an accidental swing;
- protecting earned structure without suffocating normal Gold noise.

Profit alone does not decide management.

## 4. Action contract

| Action | Purpose | Draft minimum evidence |
|---|---|---|
| HOLD | allow healthy thesis to work | structure survives; no better action earned |
| PROTECT | reduce open risk | sufficient progress + confirmed protective reference |
| TRAIL | follow newly earned structure | valid tighter structural reference |
| RUNNER | extend beyond normal scalp objective | exceptional fresh continuation + real next objective |
| EXIT | close failed/inefficient/unsafe trade | structural failure, material reversal, exhausted path, time/efficiency failure or mandatory safety |

Mandatory safety outranks normal HOLD/RUNNER preference.

## 5. HOLD

HOLD when the original thesis remains healthy and no protective/exit condition has been earned.

A single opposite M5 candle, normal pullback, small RSI change or tiny positive profit is not sufficient alone.

However, a scalp is not allowed to drift indefinitely simply because no dramatic reversal appears. Time/efficiency rules may eventually require EXIT once frozen.

## 6. PROTECT

PROTECT reduces risk after market progress and confirmed structure justify it.

The proposed stop must come from a causal structural reference plus approved buffer. A fixed profit amount or arbitrary breakeven timer cannot by itself define the stop price.

Original R remains immutable for analytics even after protection.

## 7. TRAIL

Trailing follows earned structure and can only tighten risk.

Draft BUY progression might use:

```text
original structural stop
→ fresh M5 protected swing
→ stronger M5/M15 continuation structure
```

SELL is symmetric.

H1 runner structure may remain available only for exceptional continuation; a normal scalp should not require broad H1 management.

A stop must never intentionally widen beyond original approved risk.

## 8. Primary scalp objective

The Primary target is a major management checkpoint.

At/near Primary, the manager evaluates:

- rejection versus acceptance;
- remaining path room;
- continuation momentum;
- opposing structural evidence;
- current spread/execution health;
- elapsed trade time;
- session context.

The challenge must decide whether ordinary V1 scalps normally close fully at Primary or allow controlled continuation more often.

## 9. Expansion and Runner

Expansion is optional and must be tied to real structure/liquidity, not greed.

A Runner is exceptional in a scalper. It requires fresh continuation and a new objective. Profit alone cannot extend the target.

There must never be an infinite moving target.

## 10. Time/efficiency exit

Scalp validity includes time efficiency.

Potential evidence for a governed time/efficiency EXIT includes:

- little/no favorable progress after a calibrated number of completed M5 bars;
- declining momentum while target remains distant;
- spread/volatility regime deterioration;
- repeated inability to progress through a local obstacle;
- original trigger/event becoming stale while the position has not moved as expected;
- imminent hard session/pre-close boundary.

Exact bar/time thresholds are not frozen before research/challenge.

A time exit is not permission to ignore fresh structural evidence; it is a separate thesis-efficiency rule.

## 11. Normal EXIT

Normal EXIT may result from:

- exact family invalidation;
- confirmed opposing M5 structural shift;
- failed reclaim/failed continuation;
- strong opposing displacement;
- target rejection plus collapsing continuation;
- no credible remaining room;
- time/efficiency failure;
- mandatory session/execution safety.

A single soft indicator cannot force an exit by itself.

## 12. Mandatory PRE_CLOSE / market-safety exit

If policy requires flattening before a known symbol closure, the close uses the governed execution path while the broker remains tradeable.

Ambiguous acknowledgement or loss of broker access preserves unresolved exposure and enters reconciliation. It must never be marked closed by assumption.

## 13. Original R and durable state

ManagedTrade stores:

- ticket and bot ownership lineage;
- Opportunity/Episode/TradePlan identity;
- verified fill;
- original and current SL/TP;
- immutable original R;
- objective stage;
- action history/reasons;
- frozen policy/config identity;
- pending close/learning lineage where relevant.

Local state changes after MODIFY/CLOSE only after reconciliation verifies broker truth.

## 14. Manual/external and broker-side close

Trade Manager never adopts a foreign/manual position discovered while bot state is flat.

A manual close of an already-known ManagedTrade is different: the trade remains bot-originated, while closing origin may be external/mixed.

If the known position disappears, recovery must prove the full broker-side close from durable ticket/deal lineage before clearing the ManagedTrade or creating learning.

Partial-volume evidence that does not prove full closure remains reconciliation state.

## 15. Minimum-lot / partial-profit boundary

A small account may trade the broker minimum lot, making partial closes impossible or meaningless.

V1 correctness must not depend on partial profit. Full-position HOLD/PROTECT/TRAIL/EXIT remains valid for indivisible volume.

Partial-management policies can be researched later only for divisible positions.

## 16. Research metrics

Management research should retain:

- MAE/MFE;
- realized R;
- hold duration/bars;
- Entry Efficiency;
- Capture Efficiency;
- Premature Exit Cost;
- profit given back;
- stop-protection quality;
- Primary→Expansion rate;
- time-exit outcomes;
- spread/slippage around exit;
- family/session/regime attribution;
- close origin.

## 17. Dashboard

Where authoritative facts exist show:

```text
position ticket / ownership
entry + original/current SL/TP
original R / current open risk
current objective stage
continuation / reversal / structure / momentum health
trade age / M5 bars in trade
action + reason
session/pre-close status
Intent + reconciliation state
verified/pending close evidence
```

## 18. Planned implementation ownership

```text
src/gold_scalp_trader/management/models.py
src/gold_scalp_trader/management/manager.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/management/execution.py
src/gold_scalp_trader/execution/*
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/research/live_learning.py
```

## 19. Planned proof

Tests must cover ordinary HOLD, structural protection, no stop widening, time/efficiency exit semantics once frozen, Primary handling, Runner requiring a real new objective, PRE_CLOSE override, ambiguous acknowledgement, verified state updates, exact broker-side/manual close proof, partial-volume fail-closed behaviour and exactly-once downstream learning.

## 20. Pre-challenge calibration

Open items: normal scalp hold-time distribution, maximum/soft time stop, protection eligibility, M5/M15 trailing precedence, Primary full-exit policy, Expansion/Runner frequency, momentum/reversal thresholds and family-specific management profiles.
