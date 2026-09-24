# GoldScalpTrader — Market Data and History

**Status:** FROZEN V1 READ ARCHITECTURE — FRESHNESS THRESHOLD / CONNECTED MT5 PROOF PENDING
**Version:** 1.0-scalp-read-boundary
**Authority:** Normalized MT5 facts, completed-candle chronology, quote/tick freshness, data quality, frozen timeframe roles, history and current exposure reads.

## 1. Reader promise

This document defines how raw MetaTrader 5 data becomes trusted typed facts. It does not decide whether a setup is attractive, affordable or executable.

Strategies/intelligence never open private MT5 read clients or reinterpret missing broker truth.

## 2. One read boundary

```text
MetaTrader5 terminal
        ↓
market_data/mt5_reader.py
        ├─ AccountFacts
        ├─ SymbolSpec
        ├─ Quote / spread / capture time
        ├─ completed CandleSeries
        └─ OpenPositionFacts / broker activity
        ↓
immutable MarketSnapshot
        ↓
IntelligenceSnapshot
```

Irreversible create/modify/close belongs only to execution writer.

## 3. Facts and missingness

| Fact | Meaning | Missing/corrupt result |
|---|---|---|
| AccountFacts | account/server/currency/equity/mode/identity | unavailable or identity mismatch |
| SymbolSpec | digits, point, tick size/value, contract, volume, stop/freeze/filling rules | UNKNOWN/BLOCK upstream |
| Quote | Bid, Ask, capture/broker time, spread | stale/unavailable/corrupt |
| Candle | completed UTC OHLCV bar | corrupt/sparse/future-clock failure |
| CandleSeries | chronological completed history | insufficient/stale/sparse |
| OpenPositionFacts | current broker exposure | unavailable/corrupt; never guessed zero |
| MarketSnapshot | reusable cycle truth | weakest required input controls quality |

## 4. Gold symbol resolution

Preferred initial symbol is `XAUUSDm`, with configured aliases such as `XAUUSD` only through deterministic resolution:

```text
preferred symbol
→ configured aliases in order
→ SYMBOL_NOT_FOUND
```

Resolved symbol + broker specification are part of runtime/recovery identity.

## 5. Completed-candle authority

MT5 position 0/forming bar is not structural proof. Reader normalizes UTC chronology, rejects duplicates/impossible OHLC/non-finite/out-of-order data and never inserts a forming bar into completed `CandleSeries`.

## 6. Frozen scalp timeframe roles

| Timeframe | Role |
|---|---|
| H4 | optional major/macro context; never scalp trigger |
| H1 | broad regime / important structure |
| M15 | opportunity/location/session path context |
| M5 | primary completed scalp setup/timing/management structure |
| M1 | diagnostic/research micro-context only |
| quote/tick | current executable condition, not historical structural proof |

The fresh-zero question is closed: M1/tick history has no hidden production trigger authority in current V1. Any future promotion requires governed design/evidence change.

## 7. Freshness is first-class

Snapshot exposes enough timestamps to measure quote age, latest completed-bar age, clock skew, snapshot construction time, spread and relevant SymbolSpec age.

Exact hard age thresholds remain scalp calibration. Material future-dated quote/candle facts are CORRUPT, not clamped.

## 8. Expected closure gaps versus missing history

```text
large recent gap
→ explained by verified/accepted normal broker closure
   → expected closure; not automatically SPARSE
→ otherwise
   → unexplained history hole; SPARSE/UNKNOWN
```

This does not itself prove market currently OPEN. Hard session authority owns that truth.

## 9. Open-position truth

```text
positions_get == []    → verified zero positions
positions_get == None  → DATA_UNAVAILABLE
invalid/duplicate data → DATA_CORRUPT
SL/TP numeric zero      → explicit absence where broker semantics require it
```

Broker position fact does not prove bot ownership; ownership requires durable lineage/reconciliation.

## 10. Data-quality states

```text
HEALTHY
INSUFFICIENT
STALE
SPARSE
CORRUPT
UNKNOWN
```

Recoverable waits may include STALE/INSUFFICIENT/SPARSE. Corrupt chronology, identity failure and unknown exposure fail closed for affected writes/new entry.

## 11. Snapshot reuse and fresh pre-submit truth

Normal analysis shares one immutable snapshot. Execution/recovery may perform explicit fresh reads where their contracts require them.

Snapshot reuse never overrides fresh pre-submit Bid/Ask, spread, symbol rules, exposure, account identity or hard session state.

## 12. Scalp history roles

- recent M5: trigger structure, displacement, rejection, compression, event freshness;
- wider M5/M15: local swings, liquidity pools, session path, target room and recent regimes;
- H1/H4: broad/major context;
- M1: diagnostics/research only;
- deep portable history: offline replay/research input, not permanent live lifecycle state.

Historical archives never replace durable Opportunity, TradePlan, Risk day/profile, Intent, ManagedTrade or learning receipts.

## 13. Spread / transaction-cost facts

Reader reports raw Bid/Ask/spread. It does not decide acceptability. TradePlan/Entry Timing/Execution own their respective cost/freshness policies.

## 14. Restart and recovery

Recovery rebuilds current broker truth from MT5. It must prove account/symbol scope, current exposure and pending execution lineage before normal new-entry work resumes. Unknown exposure is never zero.

## 15. Failure/operator meaning

| Failure | Runtime meaning |
|---|---|
| MT5 unavailable | no readiness/new entry |
| symbol not found | blocked |
| stale quote | visible wait/block where required |
| future quote/candle | corrupt/fail closed |
| insufficient candles | warm-up wait |
| expected closure gap | normal non-trading interval |
| unexplained recent gap | no new setup |
| unknown positions | recovery/new-entry blocked |

Dashboard never translates stale data into a confident claim that market is closed.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/market_data/mt5_reader.py
src/gold_scalp_trader/market_data/snapshot.py
src/gold_scalp_trader/domain/market.py
src/gold_scalp_trader/app/recovery_mt5.py
```

## 17. Planned deterministic proof

Tests cover forming-bar exclusion, chronology normalization, corrupt/future rejection, expected closure gap handling, symbol alias resolution, Bid/Ask/spread mapping, zero versus unavailable exposure, frozen timeframe roles, M1 non-authority and identical snapshot semantics under one-worker/bounded-parallel orchestration.

Connected Windows/MT5 freshness, current SymbolSpec and actual broker schedule remain external evidence.

## 18. Pending evidence / implementation choices

Hard quote/candle freshness thresholds, minimum live history windows, whether raw tick streams are retained or only current quotes sampled, broker-specific closure-gap handling and portable recent-history size remain implementation/scalp-evidence questions. Timeframe authority itself is frozen.