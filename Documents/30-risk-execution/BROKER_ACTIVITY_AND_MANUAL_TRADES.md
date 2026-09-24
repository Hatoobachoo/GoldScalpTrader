# GoldScalpTrader — Broker Activity and Manual Trade Accounting

**Status:** FROZEN V1 ACCOUNTING CONTRACT — BROKER-TYPE / CONNECTED PROOF PENDING
**Version:** 1.0-profiled-risk-activity-accounting
**Authority:** Separation of bot-owned activity, actual bot trade counters, external/manual activity, non-trading cash flow, account-level safety P/L and known-trade close attribution.

## 1. Purpose

The broker account can change for reasons not produced by GoldScalpTrader: manual trades, another EA, broker SL/TP, deposits, withdrawals, credits and other adjustments.

Collapsing these facts would corrupt bot P/L, trade counts, DayStartEquity Risk state and learning.

## 2. Separate questions

| Question | Authority |
|---|---|
| Is account safe to risk more? | Account Safety P/L / Risk state |
| Which Risk profile applies? | fixed UTC-day DayStartEquity profile |
| How many actual bot entries occurred? | broker activity attribution |
| What did bot realize? | bot-attributed exit deals |
| What external/manual trading occurred? | external activity model |
| Is there foreign Gold exposure? | current positions + recovery |
| Can a missing known ManagedTrade be closed? | exact durable lineage + broker exit proof |

Activity models never replace current broker position truth.

## 3. Read-only data flow

```text
one initialized MT5 read boundary
→ Gold deal history
→ account-wide financial history
→ current Gold positions

Gold deals
→ normalized DealFacts
→ bot/external attribution
→ trade counts / Bot Realized / External Realized

account-wide history
→ identifiable non-trading cash flow
→ risk-day reconciliation

positions + deals + durable ManagedTrade
→ ownership / close recovery
```

No second MT5 client is created for accounting.

## 4. Bot identity

One configured MT5 magic/identity applies per account/symbol scope.

```text
magic matches configured identity
→ bot-attributed broker activity

magic differs / zero / missing
→ external/manual
   unless exact durable ManagedTrade lineage proves original position bot-owned
```

Symbol alone never proves ownership. Comments may support Intent lineage but are not sole authority.

Exact magic-number allocation/configuration remains implementation choice; the ownership semantics are frozen.

## 5. Unknown external position versus manual close of known bot trade

Unknown foreign Gold position with no matching ManagedTrade:

```text
External Open
→ block new bot entry
→ never silently adopt/modify/close
```

Human close of already-known ManagedTrade remains bot-originated entry; close origin may be EXTERNAL/MIXED after exact proof.

Require exact ticket, official exit role/history, complete original exit volume, valid close time and no unresolved competing Intent.

## 6. UTC risk-day activity

UTC day boundary is frozen by the Risk Contract unless later explicitly changed through governed policy.

Raw deals are fills, not necessarily trades. Partial fills/closes may create multiple rows.

| Field | Rule |
|---|---|
| Today Trades | unique bot-owned entry lineages in current UTC risk day |
| Total Verified Trades | verified OPEN Intent lineages in durable project/runtime lineage |
| Bot Realized | net realized exit-deal P/L attributed to bot-owned lineage |
| External Realized | net realized exit-deal P/L not bot-attributed |
| External Open | current Gold positions not proven bot-owned |
| External Activity | external deals/exposure |

Signals, WAIT/MISSED/BLOCKED Opportunities, failed/unknown Intents and MODIFY/CLOSE actions are not new trades.

## 7. Non-trading account cash flow

Identifiable balance/credit/bonus/interest/dividend/tax-style rows may be classified as non-trading cash flow where broker types are reliable.

Trading deals/commissions are not non-trading cash flow; equity already includes them.

Repeated history reads must not reapply the same funding change. Use cumulative baseline/delta or equivalent idempotent accounting.

Unknown non-zero financial row type, missing history, malformed timestamp, duplicate or non-finite value makes cash-flow truth incomplete/UNKNOWN.

Exact Exness financial-deal type mapping remains connected implementation proof.

## 8. Risk-profile / aggressive-overlay relationship

Activity accounting supplies verified DayStartEquity/cash-flow/equity truth to the preserved Risk system:

```text
SMALL   DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

Profile remains fixed for UTC risk day.

`AGGRESSIVE_SMALL_ACCOUNT` is explicit and disabled by default; activity/equity alone never auto-enables it. When enabled by policy, accounting still reports actual equity/cash flow without trying to target 8% Risk.

## 9. UNKNOWN activity safety

```text
flat account + required cash-flow truth UNKNOWN
→ no new entry / recovery not READY

verified ManagedTrade + cash-flow truth UNKNOWN
→ safe management/protection may continue
→ no new independent entry
```

Unknown displays UNKNOWN/`—`, never false zero.

## 10. Manual trading and Account Safety P/L

Manual/foreign trading is excluded from Bot Performance P/L but changes actual account equity and therefore Account Safety P/L.

Deposits/withdrawals/credits are separately adjusted so funding is not mistaken for trading performance.

## 11. Broker-side SL/TP/manual-close recovery

If known ManagedTrade ticket disappears:

```text
unresolved Intent?
→ reconcile first
→ otherwise query normalized exit history
→ exact ticket + official exit role + complete original volume + close time
→ incomplete/ambiguous: retain ManagedTrade / RECONCILING
→ complete: close archive + receipt + learning queue + clear active trade
```

Partial exit volume is not full closure. Preserved broker-valid partial management may create intermediate deals; full-close accounting waits for complete volume proof.

## 12. Dashboard

Show Today Trades, Total Verified Trades, Account Safety P/L, Bot Realized, External Realized, External Open Exposure, External Activity, cash-flow truth and BOT/EXTERNAL/MIXED close origin.

Also expose active Risk profile/overlay through its owner without recalculating it here.

## 13. Persistence / restart

Trade counters derive from verified lifecycle records, not mutable UI counters. Risk-day cash-flow baselines, profile identity and close lineage survive restart/checkpoint. Restored records are context; positions/deals re-read from MT5.

## 14. Planned implementation ownership

```text
src/gold_scalp_trader/domain/market.py
src/gold_scalp_trader/market_data/mt5_reader.py
src/gold_scalp_trader/market_data/activity.py
src/gold_scalp_trader/risk/state.py
src/gold_scalp_trader/execution/intent_store.py
src/gold_scalp_trader/execution/reconcile.py
src/gold_scalp_trader/app/recovery.py
src/gold_scalp_trader/management/store.py
src/gold_scalp_trader/research/live_learning.py
```

## 15. Planned proof / implementation questions

Tests cover identity attribution, unique entry counting despite partial fills, bot/external P/L, non-trading cash-flow idempotency, UNKNOWN semantics, foreign-position non-adoption, known-trade manual close, full-volume proof, close origin and restart preservation.

Implementation/external questions are magic-number allocation, unusual Exness balance/credit type mapping and simultaneous manual/bot operational handling. UTC risk-day policy itself is no longer pre-challenge.