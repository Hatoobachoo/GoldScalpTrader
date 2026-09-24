# GoldScalpTrader — Market Data and History

**Status:** DRAFT PRE-CHALLENGE READ CONTRACT
**Version:** 0.1-scalp-read-boundary
**Authority:** Normalized MT5 facts, completed-candle chronology, quote/tick freshness, data quality, history roles and current exposure reads.

## 1. Reader promise

This document defines how raw MetaTrader 5 data becomes trusted typed facts for the scalp system. It does not decide whether a setup is attractive, affordable or executable.

GoldScalpTrader must never let strategies open their own MT5 clients or quietly reinterpret missing broker truth.

## 2. One normal read boundary

```text
MetaTrader5 terminal
        |
        v
market_data/mt5_reader.py
        |
        +--> AccountFacts
        +--> SymbolSpec
        +--> Quote / spread / capture time
        +--> completed CandleSeries
        +--> OpenPositionFacts / broker activity
        |
        v
immutable MarketSnapshot
        |
        v
IntelligenceSnapshot
```

Raw create/modify/close calls belong only to the later execution writer.

## 3. Facts and ownership

| Fact | Meaning | Missing/corrupt result |
|---|---|---|
| AccountFacts | account/server/currency/equity/mode/identity | unavailable or identity mismatch |
| SymbolSpec | digits, point, tick size/value, contract, volume and stop rules | UNKNOWN/BLOCK upstream |
| Quote | Bid, Ask, capture time, broker time and spread | stale/unavailable/corrupt |
| Candle | one completed UTC OHLCV bar | corrupt/sparse/future-clock failure |
| CandleSeries | chronological completed history | insufficient/stale/sparse |
| OpenPositionFacts | current broker exposure | unavailable/corrupt; never guessed zero |
| MarketSnapshot | one reusable cycle truth | weakest required input controls quality |

## 4. Gold symbol resolution

The preferred initial symbol is `XAUUSDm`, with configured aliases such as `XAUUSD` allowed only through explicit resolution.

Resolution is deterministic:

```text
preferred symbol
→ configured aliases in order
→ SYMBOL_NOT_FOUND
```

The resolved symbol and broker specification become part of the runtime scope and recovery identity.

## 5. Completed-candle authority

MT5 position 0 is forming and is not structural proof. Normal structural history begins with completed bars.

The reader must:

- normalize timestamps to timezone-aware UTC;
- return chronological order;
- reject duplicates, impossible OHLC, non-finite values and out-of-order data;
- preserve bar-open identity while downstream derived facts use their correct knowledge time;
- never insert a forming candle into a completed `CandleSeries`.

## 6. Scalp timeframe baseline

The final authority map remains challengeable, but the initial design supports:

| Timeframe | Draft role |
|---|---|
| H4 | optional broad macro/major-zone context; never a scalp trigger |
| H1 | broad regime and important structural context |
| M15 | opportunity/location/session path context |
| M5 | primary scalp setup and executable decision timeframe |
| M1 | optional diagnostic/micro-timing context only in the baseline |
| Quote/tick | current executable market condition; not historical structural proof |

M1/tick authority is intentionally not frozen before the fresh-zero challenge.

## 7. Freshness is first-class for scalping

Scalping has much smaller target room than swing trading, so stale broker truth can erase the edge even when the higher-level thesis remains valid.

The snapshot must expose enough timestamps to measure:

- quote age;
- latest completed bar age by timeframe;
- broker/runtime clock skew;
- snapshot construction time;
- current spread in price and points;
- resolved symbol specification age where relevant.

Exact hard thresholds are calibration/policy, not guessed constants in this contract.

Materially future-dated quote or candle facts are `CORRUPT`, not magically clamped to zero age.

## 8. Expected closure gaps versus missing history

Daily maintenance and weekend closure gaps must not automatically be classified as missing history when the supported broker/symbol schedule explains them.

```text
large recent gap
→ covered by known normal Gold closure
   → expected closure; do not mark SPARSE
→ otherwise
   → unexplained history hole; mark SPARSE/UNKNOWN
```

This classification does not itself prove the market is currently open. Hard market-session truth remains owned by the risk/execution permission layer.

## 9. Open-position truth

The distinction is mandatory:

```text
positions_get == []   → verified zero positions
positions_get == None → DATA_UNAVAILABLE
invalid/duplicate data → DATA_CORRUPT
SL/TP numeric zero     → explicit absence where broker semantics require it
```

Broker facts do not prove bot ownership. Bot ownership requires durable lineage, scope and execution/reconciliation records.

## 10. Data-quality states

The baseline quality vocabulary is:

```text
HEALTHY
INSUFFICIENT
STALE
SPARSE
CORRUPT
UNKNOWN
```

Recoverable waits may include STALE/INSUFFICIENT/SPARSE. CORRUPT chronology, identity failure and unknown exposure fail closed.

## 11. Snapshot reuse and fresh pre-submit truth

Normal analysis shares one immutable snapshot per cycle. A fresh execution/recovery read may occur where the execution contract explicitly requires it.

Snapshot reuse never overrides a fresh pre-submit Bid/Ask, spread, symbol-spec, exposure or session check.

## 12. Scalp history roles

- recent M5: trigger structure, displacement, rejection, compression and event freshness;
- wider M5/M15: local swings, liquidity pools, session path, target room and recent regimes;
- H1/H4: broad regime/major structure only;
- M1 when enabled: diagnostic micro-context, never hidden independent production authority in the baseline;
- deep portable history: offline replay/research input, not permanent live runtime state.

Raw historical archives never replace durable lifecycle state such as Opportunity, Trade Plan, Risk day, Intent, ManagedTrade and learning receipts.

## 13. Spread and transaction-cost facts

The reader reports raw Bid/Ask and spread. It does not decide whether spread is acceptable.

Hard acceptance belongs to Entry Timing/Trade Plan/Execution according to the final contracts. This separation prevents the data layer from becoming a hidden trading gate.

## 14. Restart and recovery

Recovery must rebuild current broker truth from MT5 rather than trusting local state as exposure truth.

A restart must prove account/symbol scope, current positions and pending execution lineage before normal new-entry work resumes.

Unknown exposure is never interpreted as zero.

## 15. Failure and operator meaning

| Failure | Meaning | Runtime behaviour |
|---|---|---|
| MT5 unavailable | terminal/read path unavailable | no readiness/new entry |
| symbol not found | no permitted Gold symbol | blocked |
| stale quote | current execution truth not advancing | visible wait |
| future quote/candle | chronology cannot be trusted | corrupt/fail closed |
| insufficient candles | warm-up incomplete | visible wait |
| expected closure gap | normal non-trading interval | do not mark sparse |
| unexplained recent gap | missing history | no new setup |
| unknown positions | exposure cannot be proven | recovery blocked |

The dashboard must never translate stale data into a confident claim that the market is closed.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/market_data/mt5_reader.py
    terminal reads and normalization

src/gold_scalp_trader/market_data/snapshot.py
    multi-timeframe immutable MarketSnapshot, freshness and quality

src/gold_scalp_trader/domain/market.py
    typed account/symbol/quote/candle/exposure facts

src/gold_scalp_trader/app/recovery_mt5.py
    current broker recovery truth adapter
```

Exact source names may change only through the module/file catalog affected-graph process.

## 17. Planned deterministic proof

Tests must cover at least:

- forming-bar exclusion;
- chronological normalization;
- corrupt/future timestamp rejection;
- expected closure gap versus genuine in-session sparse history;
- symbol alias resolution;
- Bid/Ask/spread mapping;
- verified zero versus unavailable exposure;
- timeframe separation;
- identical snapshot semantics in serial and later bounded-parallel orchestration.

Actual Windows MT5 freshness, broker schedule behaviour and live exposure are external connected evidence.

## 18. Pre-challenge questions

- final H4/H1/M15/M5/M1 roles;
- whether M1 enters production timing authority;
- minimum live history windows per timeframe;
- hard quote/candle freshness thresholds;
- whether tick streams are retained or only sampled as quotes;
- broker-specific closure-gap tolerance;
- how much recent market history belongs in portable recovery packages.
