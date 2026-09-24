# GoldScalpTrader — Broker Activity and Manual Trade Accounting

**Status:** DRAFT PRE-CHALLENGE ACCOUNTING CONTRACT
**Version:** 0.1-scalp-activity
**Authority:** Separation of bot-owned activity, actual bot trade counters, external/manual activity, non-trading account cash flow, account-level safety P/L and known-trade manual-close attribution.

## 1. Why this contract exists

The broker account can change for reasons not produced by GoldScalpTrader: manual trades, another EA, broker SL/TP closures, deposits, withdrawals, credits and other adjustments.

Collapsing these facts would corrupt bot P/L, trade counts, risk-day state and learning.

## 2. Questions that must remain separate

| Question | Authority |
|---|---|
| Is the account safe to risk more? | Account Safety P/L |
| How many actual bot entries occurred today? | broker activity attribution |
| How many verified bot OPEN lifecycles exist in this durable runtime lineage? | terminal verified Intent history |
| What did the bot realize? | bot-attributed exit deals |
| What manual/foreign trading occurred? | external activity model |
| Is there foreign Gold exposure? | current positions + recovery |
| Can a missing known ManagedTrade be considered closed? | exact durable lineage + broker exit proof |

Trading activity models do not replace current broker position truth.

## 3. Read-only data flow

```text
one initialized MT5 reader
→ Gold deal history
→ account-wide financial-deal history
→ current Gold positions

Gold deals
→ normalized DealFacts
→ bot vs external/manual attribution
→ Today Trades / Bot Realized / External Realized

account-wide history
→ identifiable non-trading cash flow
→ risk-day reconciliation

current positions + deal history + durable ManagedTrade
→ ownership / close recovery
```

No second MT5 connection is created just for accounting.

## 4. Bot identity

The bot uses one configured MT5 magic/identity per account/symbol scope.

```text
deal/position magic matches configured bot identity
→ bot-attributed broker activity

magic differs / zero / missing
→ external/manual activity unless exact durable ManagedTrade lineage proves the original position was bot-owned
```

Symbol alone never proves ownership.

Comments may support Intent lineage but are not sole ownership authority because brokers may alter them.

## 5. Unknown external position versus manual close of known bot trade

These are fundamentally different.

### Unknown manual/foreign position

```text
manual/foreign Gold position appears while bot has no matching durable ManagedTrade
→ External Open
→ block new bot entry
→ never adopt/modify/close it
```

### Human closes an already-known ManagedTrade

The original trade remains bot-originated. The closing broker action may be `EXTERNAL` or `MIXED`.

Recovery must prove:

- exact durable position ticket;
- official exit role/history;
- complete original exit volume;
- valid close time;
- no unresolved competing Intent.

Only then may the ManagedTrade be archived/cleared and downstream learning created with the close origin preserved.

## 6. UTC-day trading activity

Draft day boundary remains UTC for consistency with the Risk Contract unless challenge changes it.

Raw deals are fills, not necessarily trades. Partial fills/partial closes can create multiple rows.

Draft dashboard semantics:

| Field | Rule |
|---|---|
| Today Trades | unique bot-owned position lineages with entry role in current risk day |
| Total Trades | terminal verified `OPEN` Intent lineages in current durable project/runtime lineage |
| Bot Realized | net realized exit-deal P/L attributed to bot identity |
| External Realized | net realized exit-deal P/L not attributed to bot identity |
| External Open | current Gold positions not proven bot-owned |
| External Activity | external deals or exposure |

Signals, WAIT/MISSED/BLOCKED Opportunities, failed/unknown Intents and MODIFY/CLOSE actions are not new trades.

## 7. Non-trading account cash flow

Identifiable balance/credit/bonus/interest/dividend/tax-style financial rows may be classified as non-trading cash flow where the broker exposes reliable types.

Trading deals/commissions are not non-trading cash flow; equity already includes them.

Repeated history reads must not repeatedly apply the same funding adjustment. Risk-day logic therefore uses a frozen cumulative baseline/delta model or equivalent idempotent accounting.

Unknown non-zero financial row types, missing history APIs, malformed timestamps, duplicates or non-finite values make cash-flow truth incomplete/UNKNOWN.

## 8. Safety consequence of UNKNOWN activity

```text
flat account + required cash-flow truth UNKNOWN
→ no new entry / recovery not READY

verified managed bot position + cash-flow truth UNKNOWN
→ management/protection may continue where safe
→ no new independent entry
```

Unknown trading history displays `—`/UNKNOWN, never a false zero.

## 9. Manual trading and account safety

Manual/foreign trading remains excluded from **Bot Performance P/L**, but it still changes actual account equity and therefore **Account Safety P/L**.

This prevents the bot from ignoring losses caused by other activity on the same risk-bearing account.

Deposits/withdrawals/credits remain separately adjusted so funding is not mistaken for trading performance.

## 10. Known broker-side SL/TP/manual close recovery

If a durable known ManagedTrade ticket disappears:

```text
unresolved Intent?
→ reconcile Intent first
→ if unresolved: RECONCILING
→ otherwise query normalized exit history
→ require exact ticket + exit role + complete original volume + close time
→ incomplete/ambiguous: retain ManagedTrade
→ complete proof: durable close archive + receipt + learning queue + clear active trade
```

Partial exit volume is not full closure.

Unknown external positions are never adopted from history.

## 11. Dashboard/operator meaning

Show independently:

```text
Today Trades
Total Verified Trades
Account Safety P/L
Bot Realized P/L
External Realized P/L
External Open Exposure
External Activity
cash-flow truth / UNKNOWN
close origin BOT / EXTERNAL / MIXED when known
```

## 12. Persistence/restart

Durable trade counters derive from verified lifecycle records rather than mutable UI counters.

Deleting/replacing state to change trade counts is not approved.

Risk-day cash-flow baselines and close lineage survive restart and local recovery packages.

Restored records remain context; current positions/deals are re-read from MT5.

## 13. Planned implementation ownership

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

## 14. Planned proof

Tests must cover:

- magic/ownership attribution;
- unique entry counting despite partial fills;
- bot vs external realized P/L;
- non-trading cash-flow idempotency;
- UNKNOWN history/cash-flow semantics;
- foreign position non-adoption;
- exact manual close of known ManagedTrade;
- full-volume proof requirement;
- close origin BOT/EXTERNAL/MIXED;
- restart/recovery preservation.

## 15. Affected-graph rule

Changes to identity/day boundary/manual attribution/cash flow must synchronize Risk, Execution, Persistence, Live Learning, Dashboard, User Manual and release evidence.

## 16. Pre-challenge questions

- final magic-number scope strategy;
- unusual Exness balance/credit row classification;
- UTC risk-day boundary;
- treatment of simultaneous manual and bot activity on the same Gold symbol;
- whether any additional dashboard counters are useful without confusing fills with trades.
