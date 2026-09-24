# GoldScalpTrader — Monetary Risk Contract

**Status:** FROZEN V1 RISK ARCHITECTURE — NUMERICAL CALIBRATION / BROKER PROOF PENDING
**Version:** 1.0-standard-policy
**Authority:** Broker-aware dynamic sizing, per-trade policy, exposure, daily safety P/L, loss locks, cooldown and same-episode re-entry.

## 1. Purpose and boundary

Risk answers:

> Can this already-defined structural scalp plan be executed by this account at an affordable, broker-valid and policy-valid size?

Risk does not choose BUY/SELL, invent a setup, improve target room, edit structural invalidation or send MT5 requests.

```text
strong strategy score ≠ affordable trade
Risk PASS             ≠ final broker permission
unknown financial truth ≠ safe zero
```

## 2. Audit-1 simplification: one STANDARD policy

V1 removes automatic `SMALL / MEDIUM / NORMAL` risk tiers selected from equity.

Use one explicit production policy:

```text
STANDARD
```

It contains:

- preferred per-trade risk target;
- hard per-trade risk ceiling;
- daily loss limit;
- one-position capacity;
- durable loss-streak / cooldown state;
- same-episode re-entry state;
- manual daily-loss reset disabled by default.

Exact percentages remain calibration pending.

Account size still matters mathematically through verified equity, structural stop, tick value, margin and broker minimum/step volume. Removing tiers does **not** ignore small-account reality; it removes policy duplication.

## 3. Aggressive policy boundary

Historical aggressive small-account values such as `8% / 16%` are **not active V1 policy**.

Any future `AGGRESSIVE_EXPERIMENT`:

- is explicit, never auto-selected by balance;
- remains disabled by default;
- requires separate stress/holdout/DEMO evidence and governance;
- cannot silently alter STANDARD or hard safety.

## 4. Ordered evaluation

```text
current TradePlan
→ verified RiskContext: equity/free margin/quote/SymbolSpec/exposure
→ STANDARD policy
→ theoretical volume
→ broker min/step/max normalization
→ actual all-in loss at executable normalized volume
→ margin / exposure / capacity / daily state / cooldown / episode limits
→ RiskEvaluation PASS / BLOCK / UNKNOWN
→ central Gate
```

Risk asks:

1. Is the TradePlan complete/current/finite?
2. What is the STANDARD preferred risk target and hard ceiling?
3. What volume can the broker execute?
4. What realistic account-currency loss follows from the structural SL at normalized volume?
5. Is margin/exposure/capacity/daily state acceptable?
6. Is required financial/broker truth verified and fresh?

## 5. Broker-aware all-in risk

Use verified broker/account facts where available:

- tick size/value;
- point/digits;
- contract size when applicable;
- account currency/equity/free margin;
- executable side context;
- entry-to-stop distance;
- min/max/step volume;
- explicit slippage reserve/commission assumptions where approved.

Question:

> For the normalized executable volume, what realistic account-currency loss occurs if the approved original SL is reached, counting each friction source exactly once?

Do not double-count spread if Bid/Ask entry geometry already embeds it.

## 6. Dynamic sizing sequence

```text
consume structural TradePlan
→ read verified account/SymbolSpec facts
→ use STANDARD preferred risk target
→ calculate theoretical volume
→ normalize to broker min/step/max
→ calculate actual all-in risk at normalized volume
→ compare actual risk with preferred target + hard ceiling
→ verify margin/exposure/daily state/cooldown/re-entry
→ PASS / BLOCK / UNKNOWN
```

Strategy confidence never multiplies risk.

## 7. Minimum-lot handling

```text
raw theoretical lot < broker minimum
→ evaluate broker minimum volume

actual minimum-volume risk ≤ hard policy ceiling and all authorities valid
→ Risk may PASS

actual minimum-volume risk > hard ceiling
→ BLOCK current TradePlan as MIN_LOT_UNAFFORDABLE

required tick/margin/equity facts unknown
→ UNKNOWN / fail closed
```

Never manufacture a non-executable fractional lot and never tighten structural SL to make minimum lot affordable.

## 8. Margin authority

Broker-native exact margin/order-check truth is authoritative where available. Generic formulas may be diagnostic only. Unknown/contradictory required margin facts fail closed for new entry.

## 9. Original risk versus current open risk

Keep separate:

- Original Approved Risk / immutable original R basis;
- Current Open Risk to verified current stop;
- Locked Profit where applicable;
- Bot Performance P/L;
- Account Safety P/L.

Protection/trailing never rewrites historical original R.

## 10. Exposure / capacity

V1 allows one independently risk-bearing Gold position per account/symbol scope:

```text
capacity 0/1 → new entry may be considered
capacity 1/1 → new independent Gold entry BLOCKED
```

Analysis/research continues while capacity is full. Manual/foreign/unknown Gold exposure is not adopted by the bot; ownership ambiguity blocks new entry until reconciled.

## 11. Risk day / Account Safety P/L

Use one explicit risk-day boundary, initially UTC unless later evidence justifies a governed change.

Conceptual formula:

```text
AccountSafetyPL
= CurrentVerifiedEquity
  - DayStartEquity
  - NetIdentifiableNonTradingCashFlowSinceDayStart
```

Deposits/withdrawals/credits/non-trading cash flow are separated through broker-activity accounting. Unknown equity/cash-flow truth blocks new entry.

## 12. Daily loss lock

At the calibrated STANDARD daily-loss threshold:

- state becomes `LOSS_LOCKED`;
- no new entry/re-entry/add-on;
- existing verified bot position remains under safe management;
- lock alone does not force-close an otherwise healthy position;
- history remains durable through restart.

Exact threshold is calibration pending.

## 13. Manual reset

Manual daily-loss reset capability remains **disabled by default**.

If a later approved configuration enables it, reset must be explicit, auditable, bounded, persistent and unable to clear unrelated session/news/data/identity/execution/controller failures.

## 14. Consecutive-loss cooldown

Mechanism retained, numbers calibrated later. Repeated losses or abnormal execution/feed conditions may activate cooldown. Time alone need not release it; a fresh valid Opportunity and healthy conditions may also be required according to final policy.

## 15. Same-episode re-entry

Unlimited re-entry is prohibited.

A fresh re-entry requires a genuinely new causal event, rebuilt TradePlan, current Risk PASS and explicit episode policy. An unchanged next polling cycle is never a fresh setup.

Initial candidate of at most one fresh same-episode re-entry remains calibration/policy detail until evidence supports it.

## 16. Output contract

`RiskEvaluation` exposes where applicable:

```text
PASS / BLOCK / UNKNOWN
reason
policy = STANDARD
preferred risk target / hard ceiling
theoretical + normalized volume
actual all-in risk amount / percentage
original stop monetary risk
friction diagnostics
margin diagnostic / broker result
DayStartEquity / AccountSafetyPL
loss lock / reset / streak / cooldown
capacity / ownership / re-entry state
```

UNKNOWN displays as unavailable, never zero.

## 17. Persistence / restart

Durable state includes risk-day identity, DayStartEquity, cash-flow baseline, loss lock/reset, loss streak/cooldown, same-episode state and ownership references needed for recovery.

Restart is not a risk reset. Missing/corrupt/incompatible state becomes recovery-required/UNKNOWN, not a fresh empty day.

## 18. Prohibited behaviour

- martingale;
- averaging down to rescue a thesis;
- uncontrolled grid;
- automatic equity-tier escalation;
- higher risk because a setup score is high or recent trades won;
- structural-stop distortion to fit risk;
- treating unknown exposure/equity/P&L/margin/cash flow as zero;
- counting manual activity as bot performance;
- deleting/replacing state to clear loss lock;
- double-counting spread/fees;
- opening a second independent Gold risk position;
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

Deterministic tests: lot normalization, minimum-lot evaluation, no stop rewriting, STANDARD preferred/ceiling semantics once calibrated, daily-state persistence, manual-reset disabled default, cooldown/re-entry state, cash-flow separation, capacity and UNKNOWN fail-closed.

Connected Exness DEMO proof: actual tick value/min lot/step/margin/spread/commission/order-check behaviour.

## 21. Calibration pending

STANDARD preferred risk target, hard per-trade ceiling, daily-loss limit, loss-streak/cooldown values, same-episode re-entry limit, slippage/commission reserve and risk-day boundary evidence remain calibration/external questions.