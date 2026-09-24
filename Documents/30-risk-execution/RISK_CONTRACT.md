# GoldScalpTrader — Monetary Risk Contract

**Status:** DRAFT PRE-CHALLENGE RISK CONTRACT
**Version:** 0.1-scalp-broker-aware-risk
**Authority:** Account profiles, executable risk, broker-aware dynamic sizing, exposure, daily safety P/L, loss locks, reset, cooldown and same-episode re-entry limits.

## 1. Purpose and boundary

This contract answers one question:

> Can this already-defined structural scalp plan be executed by this account at an affordable, broker-valid and policy-valid size?

Risk does not choose BUY/SELL, invent a setup, edit structural invalidation, improve poor target room or send an MT5 request.

```text
strong strategy score ≠ affordable trade
Risk PASS             ≠ final broker permission
unknown financial truth ≠ safe zero
```

Final broker permission belongs to the central Execution Gate.

## 2. Ordered evaluation pipeline

```text
TradePlan — approved entry reference, original SL, objectives, original R
→ verified RiskContext — equity, free margin, quote, SymbolSpec, exposure
→ fixed UTC risk-day account profile
→ broker-executable volume
→ realistic all-in monetary loss
→ daily state / capacity / cooldown / episode limits
→ RiskEvaluation PASS / BLOCK / UNKNOWN
→ central Gate
```

Risk asks in order:

1. Is the structural plan complete, finite and current?
2. Which fixed risk-day account profile applies?
3. What volume can the broker actually execute?
4. What is realistic account-currency loss if original SL is reached?
5. Is margin/exposure/capacity/daily state acceptable?
6. Is required financial/broker truth verified and fresh?

## 3. Account-profile architecture

The reference three-profile architecture is retained as a draft because broker granularity affects small accounts differently:

```text
SMALL
MEDIUM
NORMAL
```

Candidate equity boundaries may initially mirror the reference (`<300`, `300–999.99`, `>=1000` USD-equivalent) for research continuity, but both boundaries and monetary-risk bands remain **PRE-CHALLENGE**.

The profile is resolved from verified positive DayStartEquity at the UTC risk-day boundary and remains fixed for that risk day. Floating P/L does not silently switch the profile.

A positive account below $100 is not automatically rejected by an invented balance floor.

## 4. Risk percentages are intentionally not frozen yet

GoldSwingTraderAI's aggressive SMALL-account bands are **not copied as canonical scalp policy** merely because they exist in the reference.

GoldScalpTrader begins documentation with these facts only:

- the current temporary code scaffold uses `0.50%` default risk;
- final preferred/normal/elevated/hard-ceiling bands must be challenged against a ~$100 account, 0.01 minimum lot, Gold stop geometry and trade frequency;
- monetary risk must never increase merely because strategy confidence is high;
- any future aggressive profile must be explicit, bounded and disabled by default unless separately approved.

Exact percentages belong to fresh-zero challenge + replay/stress + connected broker evidence before freeze.

## 5. Broker-aware all-in risk

Use verified broker facts:

- tick size/value;
- point/digits;
- contract size where applicable;
- account currency;
- executable entry side;
- entry-to-stop distance;
- min/max/step volume;
- equity/free margin;
- spread;
- explicit slippage reserve assumptions where approved;
- commission/fees when reliably known.

Required question:

> For the normalized executable volume, what realistic account-currency loss is expected if the approved structural stop is hit, counting each friction source exactly once?

If Ask/Bid entry geometry already embeds spread in entry-to-stop distance, spread must not be double charged.

## 6. Dynamic lot sizing sequence

```text
resolve fixed risk-day profile
→ consume structural TradePlan
→ choose preferred risk target inside approved profile
→ calculate theoretical volume from entry, original SL and broker tick facts
→ normalize to broker min/step/max
→ calculate actual all-in risk at normalized volume
→ classify risk band
→ verify hard ceiling, margin, exposure, daily state and fresh facts
→ PASS / BLOCK / UNKNOWN
```

Dynamic lot means broker/account facts alter executable volume. It never means strategy confidence multiplies risk.

## 7. Minimum-lot handling

For a small Gold account:

```text
raw theoretical lot < broker minimum
→ evaluate broker minimum volume

minimum volume actual risk within approved policy
→ Risk stage may pass

minimum volume actual risk above hard ceiling
→ BLOCK current TradePlan

unknown tick/margin/equity facts
→ UNKNOWN / fail closed
```

The bot must never manufacture `0.005` when broker minimum is `0.01`, and never tighten structural SL to make minimum lot affordable.

`MIN_LOT_UNAFFORDABLE` means a real executable-affordability failure, not “account balance is small.”

## 8. Margin authority

Generic calculated margin may be diagnostic. Broker-native exact margin/order-check truth is authoritative where available.

Unknown or contradictory required margin facts fail closed for new entry.

Risk does not rely on a guessed leverage formula when MT5/broker-native authority exists.

## 9. Original risk versus current open risk

Keep separate:

- Original Approved Risk / immutable original R basis;
- Current Open Risk to current verified stop;
- Locked Profit if stop has moved beyond entry;
- Bot Performance P/L;
- Account Safety P/L.

Protection/trailing never rewrites historical original R.

## 10. Exposure and capacity

Initial V1 retains one independently risk-bearing Gold position per account/symbol scope:

```text
capacity 0/1 → a new independent entry may be considered
capacity 1/1 → new independent Gold entry BLOCKED
```

This is not a daily trade quota. Analysis, opposite-thesis observation, management, missed-opportunity logging and research continue while capacity is full.

Manual/foreign/unknown Gold exposure is never silently assigned to the bot. Unknown ownership blocks new bot entry until reconciled.

## 11. Risk-day boundary and Account Safety P/L

The risk day uses UTC unless the fresh-zero challenge establishes a better explicit broker-aligned policy.

Baseline formula:

```text
AccountSafetyPL
= CurrentVerifiedEquity
  - DayStartEquity
  - NetIdentifiableNonTradingCashFlowSinceDayStart
```

Equity already contains realized/floating trading P/L and applicable charges. Do not double count them.

Deposits, withdrawals, credits and identifiable non-trading cash flows are removed from trading safety P/L through the dedicated broker-activity lane.

Unknown equity/cash-flow truth blocks new entry.

## 12. Daily loss lock

At the approved profile lock threshold:

- state becomes `LOSS_LOCKED`;
- no new entry/re-entry/add-on;
- existing bot position continues under safe management;
- the lock alone does not force-close an otherwise safe position;
- cumulative risk-day history remains durable.

The exact scalp daily-loss percentages remain pre-challenge.

## 13. Governed manual reset

Manual daily-loss reset capability is retained but **disabled by default**.

If a later frozen policy explicitly enables it:

- only `LOSS_LOCKED` may be reset;
- at most one reset per risk day unless a later governance decision says otherwise;
- deliberate operator confirmation is required;
- current verified equity becomes the new cycle reference;
- cumulative day history/previous lock remains visible;
- reset state/count survives restart;
- reset cannot clear session/news, data, identity, execution, controller or reconciliation failures.

Exact UX/confirmation mechanism remains a later operator-contract item.

## 14. Consecutive-loss cooldown

The mechanism is retained, numbers remain challengeable.

Draft principle:

- one ordinary losing trade does not automatically create a global cooldown;
- repeated losses can trigger a global cooldown;
- time alone need not release it—fresh healthy market/execution context and a new valid Opportunity may also be required;
- abnormal feed/execution shocks can create condition-based cooldown;
- a winning bot trade may reset loss streak where policy allows, but cannot bypass an already-active minimum cooldown.

Reference `3 losses / 30 minutes` is a research seed, not yet frozen scalp policy.

## 15. Same-episode re-entry

Unlimited same-episode re-entry is prohibited.

Initial candidate policy retains:

- at most one genuinely fresh re-entry in the same market episode;
- re-entry requires explicit new causal event and rebuilt TradePlan;
- an unchanged next polling cycle is not a fresh setup;
- if a re-entry fails, that episode locks.

Exact rule remains challengeable.

## 16. Output contract

`RiskEvaluation` should expose where applicable:

```text
PASS / BLOCK / UNKNOWN
reason
account profile
preferred risk target / hard ceiling
theoretical and normalized volume
actual all-in risk amount and percentage
original stop monetary risk
friction diagnostics
margin diagnostic / broker result
DayStartEquity
AccountSafetyPL
loss-lock / reset / streak / cooldown
capacity / ownership
```

UNKNOWN values display as unavailable/UNKNOWN, never zero.

## 17. Persistence/restart

Durable risk state includes:

- risk-day identity and DayStartEquity;
- cash-flow baseline/delta;
- cycle reference;
- loss lock/reset count;
- loss streak/cooldown;
- same-episode re-entry state;
- ownership/exposure references needed for recovery.

Restart is not a risk reset.

Missing/corrupt/incompatible risk state becomes UNKNOWN/recovery-required, not a fresh empty day.

## 18. Prohibited behaviour

- martingale;
- averaging down to rescue a thesis;
- uncontrolled grid;
- arbitrary positive-account minimum balance;
- hidden risk-limit changes by strategy/AI/environment;
- higher risk because score is high or recent trades won;
- structural-stop distortion to fit risk;
- treating elevated risk as preferred target;
- assuming unknown exposure/equity/P&L/margin/cash flow is zero;
- counting manual trades as bot performance;
- deleting/replacing DB to reset loss state;
- double counting spread/fees;
- opening second independent Gold risk position in initial V1;
- unlimited same-episode re-entry.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/risk/engine.py
src/gold_scalp_trader/risk/state.py
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/market_data/activity.py
src/gold_scalp_trader/persistence/runtime_state.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
```

## 20. Planned proof / external evidence

Deterministic tests must prove dynamic lot normalization, minimum-lot evaluation, no stop rewriting, exact band/ceiling semantics once frozen, risk-day persistence, manual-reset default disabled, cooldown/re-entry state, cash-flow separation, exposure capacity and UNKNOWN fail-closed behaviour.

Connected Windows/Exness DEMO evidence separately proves real min-lot/tick-value/margin/spread/commission behaviour.

## 21. Pre-challenge questions

- exact SMALL/MEDIUM/NORMAL boundaries;
- final preferred/elevated/hard-ceiling percentages;
- daily-loss lock percentages;
- whether an optional aggressive mode should exist at all;
- slippage/commission reserve model;
- loss-streak/cooldown values;
- same-episode re-entry count;
- broker-specific margin verification;
- whether risk-day boundary remains UTC.
