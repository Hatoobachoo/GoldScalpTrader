# GoldScalpTrader — Monetary Risk Contract

**Status:** FROZEN V1 RISK ARCHITECTURE — PRESERVED SWING PROFILES + USER AGGRESSIVE OPTION; BROKER PROOF PENDING
**Version:** 1.1-preserved-profiles-aggressive-option
**Authority:** Account profiles, executable risk, broker-aware sizing, exposure, daily safety P/L, loss locks, governed reset, cooldown, same-episode re-entry and optional aggressive small-account policy.

## 1. Purpose and boundary

Risk answers:

> Can this already-defined structural scalp TradePlan be executed by this account at an affordable, broker-valid and policy-valid size?

Risk does not choose BUY/SELL, invent a setup, improve target room, edit structural invalidation or send MT5 requests.

```text
strong strategy score ≠ affordable trade
Risk PASS             ≠ final broker permission
unknown financial truth ≠ safe zero
```

The preservation rule for this contract is explicit: risk/account policy is not changed merely because the product is a scalper. GoldSwingTraderAI's account-profile architecture remains the default unless a later specifically justified scalp change is approved.

## 2. Evaluation pipeline

```text
TradePlan — entry, original SL, objectives, original R
→ RiskContext — DayStartEquity, current equity/free margin, quote, SymbolSpec, exposure
→ fixed UTC-day account profile — SMALL / MEDIUM / NORMAL
→ optional explicit AGGRESSIVE_SMALL_ACCOUNT overlay if enabled and eligible
→ theoretical executable volume
→ broker min/step/max normalization
→ actual all-in loss at normalized volume
→ margin / exposure / capacity / daily state / cooldown / episode limits
→ RiskEvaluation PASS / BLOCK / UNKNOWN
→ central Gate
```

Ordered questions:

1. Is the TradePlan complete/current/finite?
2. Which fixed DayStartEquity profile applies?
3. Is the explicit aggressive overlay enabled and eligible?
4. What volume can the broker execute?
5. What realistic account-currency loss follows from the structural SL at normalized volume?
6. Is margin/exposure/capacity/daily state/cooldown/re-entry acceptable?
7. Is required financial/broker truth verified and fresh?

## 3. Preserved automatic account profiles

The profile is resolved once from positive `DayStartEquity` at the UTC risk-day boundary and remains fixed for that risk day. Floating P/L does not switch the profile mid-day.

```text
SMALL   positive DayStartEquity below $300
MEDIUM  $300 through $999.99
NORMAL  $1,000 and above
```

| Profile | Normal / target risk | Elevated but acceptable | New-entry hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

These are inherited policy defaults, not profitability promises. They stay active unless a later **scalp-specific** governed decision explicitly replaces them.

### 3.1 SMALL

SMALL covers all positive DayStartEquity below $300. The normal target is 3.0%–4.5%, elevated is above 4.5%–6.5%, and no normal-profile new entry may exceed 7%.

A Gold broker minimum volume such as 0.01 does not create a fake minimum-balance rule. Evaluate the actual all-in risk of the executable minimum. If too expensive, block the current plan; never tighten the structural stop to make it fit.

### 3.2 MEDIUM

MEDIUM covers $300–$999.99 DayStartEquity. Normal target is 2.0%–3.0%, elevated is above 3.0%–4.5%, and the normal-profile hard ceiling is 5%.

### 3.3 NORMAL

NORMAL covers $1,000 or more. Normal target is 1.0%–2.0%, elevated is above 2.0%–3.5%, and the normal-profile hard ceiling is 4%.

## 4. Operator-requested AGGRESSIVE_SMALL_ACCOUNT mode

This capability is **preserved and operationally designed**, but **disabled by default**.

It is not research-only and it is not automatically enabled merely because account equity is small.

Eligibility baseline:

```text
explicit config/operator enable required
AND
positive DayStartEquity below $1,000
```

When enabled:

```text
8%  = MAXIMUM monetary SL-risk ceiling per new trade
      NOT a target that the bot tries to fill
16% = maximum aggregate open risk ceiling
16% = daily loss ceiling
```

Rules:

- existing SMALL/MEDIUM profile classification remains visible for context/accounting;
- the aggressive overlay changes only the approved risk ceilings it explicitly owns;
- 8% is never a confidence-based target and cannot be multiplied by strategy score;
- structural invalidation/SL is never tightened to make 8% or minimum lot fit;
- broker min/max/step, margin, session/news, exposure, controller, Gate, Intent and execution safety remain unchanged;
- one-position V1 capacity remains active unless separately changed, so the 16% aggregate cap is an additional hard cap rather than permission to open multiple positions;
- manual daily-loss reset remains disabled by default even when aggressive mode is enabled;
- enabling/disabling the mode is explicit, auditable and versioned; it is never silently auto-selected from equity alone.

## 5. Broker-aware all-in risk

Use verified broker/account facts:

- tick size/value;
- point/digits;
- contract size where applicable;
- account currency/equity/free margin;
- executable side context;
- entry-to-stop distance;
- min/max/step volume;
- approved slippage reserve/commission/fees where applicable.

Required question:

> For the normalized executable volume, what realistic account-currency loss is expected if the approved structural stop is hit, counting each friction source exactly once?

If current Ask/Bid entry geometry already embeds spread in entry-to-stop loss, do not add spread again as a second monetary charge.

## 6. Dynamic sizing sequence

```text
resolve fixed UTC-day profile
→ consume structural TradePlan
→ determine normal profile policy or explicit aggressive overlay
→ calculate theoretical volume from entry, original SL, equity and tick facts
→ normalize to broker min/step/max
→ calculate actual all-in risk for normalized volume
→ classify against target/elevated/hard ceilings
→ verify margin/exposure/daily state/cooldown/re-entry
→ PASS / BLOCK / UNKNOWN
```

Strategy confidence never multiplies risk.

## 7. Minimum-lot handling

```text
raw theoretical lot < broker minimum
→ evaluate broker minimum volume

actual minimum-volume risk inside active hard policy + all authorities valid
→ Risk may PASS

actual minimum-volume risk above active hard ceiling
→ BLOCK current TradePlan as MIN_LOT_UNAFFORDABLE / policy violation

required tick/margin/equity facts unknown
→ UNKNOWN / fail closed
```

Never manufacture a non-executable fractional lot and never change structural SL to make minimum lot affordable.

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

Initial V1 preserves one independently risk-bearing Gold position per account/symbol scope:

```text
capacity 0/1 → new entry may be considered
capacity 1/1 → new independent Gold entry BLOCKED
```

Analysis/research continues while capacity is full. Manual/foreign/unknown Gold exposure is not adopted by the bot; ownership ambiguity blocks new entry until reconciled.

The aggressive 16% aggregate-open-risk ceiling remains a hard account policy even while capacity is 0/1.

## 11. Risk day / Account Safety P/L

Risk day begins at 00:00 UTC unless a later governed policy changes it.

A new `DayStartEquity` is created only when verified equity is available and unresolved Intent, bot positions and reconciliation checks are clear.

```text
AccountSafetyPL
= CurrentVerifiedEquity
  - DayStartEquity
  - NetIdentifiableNonTradingCashFlowSinceDayStart
```

Deposits, withdrawals, credits/debits and other identifiable non-trading cash flow are separated through broker-activity accounting. Floating losses count through equity. Unknown equity/cash-flow truth blocks new entry.

## 12. Daily loss lock

At the active profile/overlay daily-loss threshold:

- state becomes `LOSS_LOCKED`;
- no new entry/re-entry/add-on;
- an existing verified bot position remains under safe Trade Manager control;
- daily lock alone does not force-close an otherwise healthy position;
- cumulative risk-day history remains durable through restart.

Normal profile locks are SMALL 12%, MEDIUM 9%, NORMAL 7%. Explicit aggressive small-account mode uses 16% daily-loss ceiling.

## 13. Governed manual daily-loss reset

The reset **feature is preserved** but is **disabled by default**.

Default:

```text
manual_daily_loss_reset_enabled = false
max_manual_resets_per_day = 0
```

If a later explicit operator configuration enables the preserved reset capability:

- only `LOSS_LOCKED` can be reset;
- at most one reset is allowed per UTC risk day unless a later explicit policy changes that bound;
- operator confirmation must be deliberate (reference workflow: double confirmation such as `R` then `R`);
- new cycle reference uses current verified equity/safety state;
- cumulative AccountSafetyPL, broker history and previous lock remain visible/immutable;
- the same active profile/overlay lock percentage applies to the new cycle;
- reset count/state survives restart;
- reset cannot clear News, identity, execution, data, controller, ownership or reconciliation faults.

## 14. Preserved cooldown and same-episode re-entry defaults

Reference behaviour is restored because removing/reopening it was not required by scalping.

- one ordinary losing trade does not create a global cooldown;
- one genuinely fresh same-episode re-entry is allowed when all other authorities pass;
- if that fresh re-entry also loses, that market episode locks;
- **three consecutive closed bot losses trigger at least 30 minutes of global cooldown**;
- release also requires no unresolved execution fault, fresh completed M15 context after the trigger and a fresh valid Opportunity/Episode;
- a winning closed bot trade resets the consecutive-loss counter but does not bypass an already active minimum cooldown;
- abnormal feed/execution shocks may create condition-based cooldown until responsible conditions normalize.

A later change to these values requires a specifically justified scalp change packet; they are not automatically reopened merely because the product is a scalper.

## 15. Output contract

`RiskEvaluation` exposes where applicable:

```text
PASS / BLOCK / UNKNOWN
reason
profile SMALL / MEDIUM / NORMAL
aggressive_small_account_enabled true/false
normal target / elevated band / active hard ceiling
proposed theoretical + normalized volume
actual all-in risk amount / percentage
aggregate open risk / active aggregate ceiling
original stop monetary risk
friction diagnostics
margin diagnostic / broker result
DayStartEquity / AccountSafetyPL
active daily loss threshold / lock
reset / streak / cooldown
capacity / ownership / re-entry state
```

UNKNOWN displays as unavailable, never zero.

## 16. Persistence / restart

Durable state includes risk-day identity, DayStartEquity/profile identity, active aggressive-mode policy identity, cash-flow baseline, daily lock/reset, loss streak/cooldown, same-episode state and ownership references needed for recovery.

Restart is not a risk reset. Missing/corrupt/incompatible state becomes recovery-required/UNKNOWN, not a fresh empty day.

## 17. Prohibited behaviour

- martingale;
- averaging down to rescue a thesis;
- uncontrolled grid;
- silently changing profile on floating P/L;
- silently auto-enabling aggressive mode by equity;
- treating 8% as a target to fill;
- higher risk because setup score is high or recent trades won;
- structural-stop distortion to fit risk;
- treating unknown exposure/equity/P&L/margin/cash flow as zero;
- counting manual activity as bot performance;
- deleting/replacing state to clear loss lock;
- double-counting spread/fees;
- opening a second independent Gold risk position without a separate governed capacity change;
- unlimited same-episode re-entry.

## 18. Planned implementation ownership

```text
src/gold_scalp_trader/risk/engine.py
src/gold_scalp_trader/risk/state.py
src/gold_scalp_trader/risk/permissions.py
src/gold_scalp_trader/market_data/activity.py
src/gold_scalp_trader/persistence/runtime_state.py
src/gold_scalp_trader/execution/checks.py
src/gold_scalp_trader/execution/gate.py
```

## 19. Planned proof / external evidence

Deterministic tests must cover:

- DayStartEquity profile resolution/fixed-daily profile;
- SMALL/MEDIUM/NORMAL target/elevated/hard/daily bands;
- aggressive mode disabled default;
- explicit aggressive enable/eligibility;
- 8% is ceiling not target;
- 16% aggregate/daily ceilings;
- lot normalization/minimum-lot evaluation;
- no stop rewriting;
- margin/exposure/capacity;
- daily-state persistence;
- manual reset disabled default + bounded explicit enable path;
- three-loss/30-minute cooldown;
- one fresh same-episode re-entry;
- cash-flow separation;
- UNKNOWN fail-closed.

Connected Exness DEMO proof separately validates actual tick value/min lot/step/margin/spread/commission/order-check behaviour.

## 20. Scalp-specific change boundary

The following are **not** reopened merely because this is a scalper:

- automatic account profiles;
- baseline risk bands;
- daily-loss percentages;
- preserved cooldown/re-entry defaults;
- governed reset capability.

If later replay/DEMO evidence shows a genuine scalp-horizon problem, the proposed change is discussed during documentation finalization and must update the full affected graph.

The genuinely scalp-specific geometry/cost/freshness thresholds remain owned by TradePlan/Entry Timing/Execution rather than being used as a reason to silently redesign monetary Risk.