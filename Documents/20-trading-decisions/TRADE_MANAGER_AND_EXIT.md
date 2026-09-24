# GoldScalpTrader — Trade Manager and Exit

**Status:** FROZEN V1 MANAGEMENT ARCHITECTURE — PRESERVATION-FIRST / SCALP CALIBRATION PENDING
**Version:** 1.1-preserved-management-scalp-efficiency
**Authority:** Post-entry management, structural protection, time/efficiency exits, target progression, optional broker-valid partial management, modify/close decisions, broker-verified lifecycle updates and verified-close learning handoff.

## 1. Purpose and boundary

Trade Manager is the post-entry decision floor for a verified bot-owned Gold position.

Core actions remain:

```text
HOLD
PROTECT
TRAIL
RUNNER
EXIT
```

Time/efficiency is a scalp-specific first-class reason that can produce ordinary `EXIT`; no separate `TIME_EXIT` action is needed.

The preservation rule applies here too: reference management capabilities are not removed merely because a minimum-lot scalp may not always use them.

## 2. Management pipeline

```text
verified bot-owned broker position
+ ManagedTrade + original R/objectives
→ fresh MarketSnapshot / IntelligenceSnapshot
→ continuation / reversal / structure / momentum / path / time-in-trade
→ HOLD / PROTECT / TRAIL / RUNNER / EXIT
→ optional broker-valid partial management where divisible
→ action-specific hard checks
→ durable MODIFY/CLOSE Intent
→ sole writer
→ reconciliation
→ persist state only after broker verification
→ verified full-close receipt/queue
→ downstream learning
```

## 3. Scalp timeframe roles for management

```text
M5  primary normal management structure / efficiency clock
M15 supporting path/location/continuation context
H1  broad context; may support exceptional runner management
H4  optional major context only
M1  diagnostic/research only
quote current executable spread/price/health context
```

## 4. Scalp management priorities

- exact family invalidation;
- speed/efficiency of progress;
- fresh M5 continuation/reversal structure;
- target/path acceptance or rejection;
- spread/execution deterioration;
- session/pre-close transition;
- avoiding a failed scalp becoming an accidental swing;
- protecting earned structure without choking normal Gold noise.

Profit alone does not decide management.

## 5. Action contract

| Action | Purpose | Minimum concept |
|---|---|---|
| HOLD | let healthy thesis work | structure survives; no better action earned |
| PROTECT | reduce open risk | progress + causal protective reference |
| TRAIL | follow earned structure | valid tighter causal reference |
| RUNNER | extend beyond normal scalp objective | exceptional fresh continuation + real next objective |
| EXIT | close failed/inefficient/unsafe trade | invalidation, material reversal, exhausted path, time-efficiency failure or mandatory safety |

Mandatory safety outranks normal HOLD/RUNNER preference.

## 6. HOLD

A single opposite M5 candle, normal pullback, small RSI change or tiny profit is not enough alone.

A position also cannot drift indefinitely merely because no dramatic reversal appears; calibrated time/efficiency evidence may require EXIT.

## 7. PROTECT

Protection requires enough progress plus a causal confirmed structural reference and approved buffer. A fixed profit amount or arbitrary timer does not define stop price.

Original R remains immutable for analytics.

## 8. TRAIL

Trailing follows earned structure and can only tighten risk.

Typical BUY progression:

```text
original structural stop
→ fresh M5 protected structure
→ stronger M5/M15 continuation structure
```

SELL is symmetric. H1 may support exceptional runner management only when risk still tightens and the trade has genuinely evolved beyond ordinary scalp progression.

Stop must never intentionally widen beyond original approved risk.

## 9. Primary / Expansion / Runner

Primary is the normal scalp management checkpoint. Evaluate rejection/acceptance, remaining room, continuation momentum, opposing structure, spread/execution health, elapsed trade time and session context.

Expansion is optional and must tie to real structure/liquidity.

Runner is a genuine scalp-specific change from broader Swing continuation expectations: it is exceptional and requires fresh continuation plus a defined new structural objective. Profit alone cannot extend TP and there is never an infinite moving target.

Exact Primary full-exit versus continuation policy remains scalp calibration.

## 10. Time / efficiency EXIT reason

Scalp validity includes expected speed.

Evidence may include:

- little/no favorable progress after a calibrated number of completed M5 bars;
- declining momentum while objective remains distant;
- repeated failure to clear local obstacle;
- spread/volatility regime deterioration;
- original trigger/event becoming stale while position remains inefficient;
- imminent hard session/pre-close boundary.

Thresholds are not guessed before research.

## 11. Other normal EXIT reasons

- exact family invalidation;
- confirmed opposing M5 structural shift;
- failed reclaim/continuation;
- strong opposing displacement;
- objective rejection plus collapsing continuation;
- no credible remaining room;
- mandatory session/execution safety.

A single soft indicator cannot force exit by itself.

## 12. PRE_CLOSE / mandatory safety exit

Preserved session baselines apply through the owning state machine:

```text
Daily mandatory flatten baseline   T-10
Weekend mandatory flatten baseline T-30
```

When policy requires flattening, CLOSE uses the normal governed path while broker remains tradeable.

Ambiguous acknowledgement or broker-access loss preserves unresolved exposure and enters reconciliation; local state never assumes closed.

## 13. Durable ManagedTrade truth

Store:

- ticket and bot ownership lineage;
- Opportunity/Episode/TradePlan identity;
- verified fill;
- original/current SL/TP;
- immutable original R;
- objective stage;
- action/partial-action history and reasons;
- frozen policy/config identity;
- pending close/learning lineage.

State changes after MODIFY/CLOSE only after broker verification.

## 14. Manual / broker-side close

Trade Manager never adopts foreign/manual exposure discovered while bot state is flat.

A human close of an already-known ManagedTrade remains bot-originated entry lineage with EXTERNAL/MIXED close attribution after exact broker proof.

A disappeared known position requires exact ticket/deal/full-volume close evidence before clearing or learning. Partial/ambiguous evidence remains RECONCILING.

## 15. Preserved partial-management capability

Optional broker-valid partial management is **not removed**.

Rules:

- it may be used only when current volume is divisible into broker-valid remaining/closed quantities;
- it must pass normal identity/controller/Gate/Intent/writer/reconciliation safety;
- exact realized/remaining volume and risk are broker-verified;
- a minimum indivisible volume such as 0.01 simply cannot partial-close if broker step makes that impossible;
- therefore V1 correctness must never depend on partial close;
- full-position HOLD/PROTECT/TRAIL/RUNNER/EXIT always remains a valid management path.

Whether partial management improves scalp expectancy is a later research question; **the capability itself remains preserved**.

## 16. Risk-profile interaction

Open-trade management does not change the fixed UTC-day SMALL/MEDIUM/NORMAL profile or silently enable the aggressive overlay.

Aggressive mode affects approved monetary exposure policy only where its owner says so; management cannot use it to widen stops or rescue a thesis.

## 17. Research metrics

Track MAE/MFE, realized R, hold bars/duration, entry/capture/exit efficiency, premature-exit cost, profit given back, protection quality, Primary→Expansion/Runner progression, partial-management outcomes where applicable, time-efficiency exits, exit spread/slippage, family/session/regime and close origin.

## 18. Dashboard

Show ticket/ownership, entry/original/current SL/TP, original R/current open risk, objective stage, remaining volume, any verified partial action, continuation/reversal/structure/momentum health, M5 bars/time in trade, action/reason, session/pre-close, Intent/reconciliation and verified/pending close evidence.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/management/models.py
src/gold_scalp_trader/management/manager.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/management/execution.py
src/gold_scalp_trader/execution/*
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/research/live_learning.py
```

## 20. Planned proof

Tests cover HOLD, structural protection, no stop widening, time-efficiency EXIT, Primary handling, Runner requiring new objective, preserved broker-valid partial-management handling, indivisible-volume fallback, PRE_CLOSE override, ambiguous ack, verified state updates, exact manual/broker-side close proof and exactly-once downstream learning.

## 21. Scalp calibration pending

Normal hold-duration distribution, time-efficiency thresholds, protection eligibility, M5/M15 trailing precedence, Primary exit policy, partial-management expectancy, Expansion/Runner frequency and family-specific management profiles require replay/stress/holdout and connected DEMO evidence.