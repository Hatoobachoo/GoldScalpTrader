# GoldScalpTrader — Indicators and Volatility

**Status:** FROZEN V1 QUANTITATIVE EVIDENCE ARCHITECTURE — SCALP THRESHOLD CALIBRATION PENDING
**Version:** 1.0-scalp-quant-context
**Authority:** EMA20/EMA50, RSI14, ATR14, volatility normalization, momentum phase, compression/expansion measurement, extension/chase and short-horizon execution-context evidence.

## 1. Purpose

The Quant desk makes Gold price behaviour measurable across changing volatility regimes. It supports/normalizes structure; it does not replace structure.

> Indicators explain pressure, distance, volatility and extension. They do not independently create a trade or broker permission.

## 2. Invariants

| Rule | Meaning |
|---|---|
| Completed bars only | forming candles excluded from production indicator series |
| One calculation per snapshot | series computed once/shared |
| Chronological arrays | no future values |
| Explicit missingness | None/UNKNOWN is not bearish/neutral vote |
| ATR normalization | prefer volatility-relative geometry to fixed Gold points |
| Soft evidence | hard safety belongs elsewhere |
| No filter soup | no universal all-indicator/timeframe agreement |
| M1 boundary | diagnostics/research only under current V1 authority |

## 3. Preserved baseline indicators

```text
EMA fast  = 20
EMA slow  = 50
RSI       = 14 (Wilder)
ATR       = 14 (Wilder)
```

These reference primitives are preserved. Their existence is not a profitability claim and additional/alternative quantitative evidence requires governed research rather than silent replacement.

## 4. Quant pipeline

```text
completed CandleSeries
→ EMA/RSI/ATR chronological series
→ ATR-normalized candle/range/extension facts
→ volatility state
→ momentum phase
→ QuantReport + coverage
```

The shared report feeds Structure, Technical, Liquidity, Strategy, Entry Timing, TradePlan and Trade Manager.

## 5. EMA flow

EMA20 versus EMA50 may publish directional support:

```text
EMA20 > EMA50 → BUY support
EMA20 < EMA50 → SELL support
otherwise      → NONE/UNKNOWN
```

EMA order is context, not strategy permission. A scalp still needs structure, location, freshness, path room, cost viability and timing.

## 6. RSI pressure

RSI14 is pressure context, not rigid overbought/oversold reversal command. Strong trends may remain >70 or <30 while continuing. RSI disagreement is evidence, not automatic veto. Divergence remains research-only unless separately governed.

## 7. ATR as shared volatility unit

ATR may normalize candle strength, swing significance, zone width, liquidity clustering, volatility regime, extension/chase, structural stop/target context, spread/room ratios and entry drift/movement since trigger.

ATR does not independently set final SL/TP.

## 8. Volatility states

Vocabulary may include:

```text
UNKNOWN
QUIET
NORMAL
BUILDING
EXPANDING
EXTREME
DISLOCATED
```

Exact boundaries are scalp calibration. EXTREME is context/warning, not universal rejection. DISLOCATED is strong adverse evidence consumed by timing/session/execution owners.

## 9. Momentum phase

```text
UNKNOWN
BUILDING
EXPANDING
MATURE
EXHAUSTING
REVERSING
```

Momentum may combine EMA flow, completed-close progress, body/ATR efficiency, RSI pressure and extension.

Strong momentum can still be a poor scalp entry when price is extended or cost-adjusted room is small.

## 10. Extension / chase protection

A baseline measurement may use:

```text
abs(close - EMA20) / ATR
```

with states such as UNKNOWN, FRESH, NORMAL, EXTENDED and SEVERELY_EXTENDED.

Extension remains analytical evidence. Entry Timing combines it with event age, chase distance and current executable facts.

## 11. Scalp-specific quantitative context

Without inventing hidden indicators, Quant may publish:

- recent bar range/ATR;
- body efficiency;
- short-window expansion/compression;
- distance travelled since structural event in ATR;
- spread relative to ATR/gross room as descriptive context;
- recent volatility acceleration/deceleration.

If a metric becomes hard broker gate, ownership moves explicitly to the relevant Risk/Execution contract.

## 12. Frozen timeframe roles

| Timeframe | Quant role |
|---|---|
| H4 | optional broad volatility context |
| H1 | broad regime/trend support |
| M15 | opportunity volatility/extension context |
| M5 | primary scalp momentum/extension/setup quality |
| M1 | diagnostic/research micro-volatility only |

All-timeframe agreement is never required. M1 production promotion requires a future governed change.

## 13. Compression / expansion / exhaustion ownership

Quant supplies normalized measurements; Candle Structure owns multi-bar sequence labels. Exhaustion does not automatically reverse thesis or close trade without relevant structure/liquidity evidence.

## 14. Restart/replay

Same completed prefix plus QuantConfig must reproduce same series/report. Missing values stay missing rather than zero-filled. Replay uses production calculations at each prefix with no final-bar leakage.

## 15. Dashboard/research visibility

Expose EMA flow, RSI, ATR, volatility state/ratio, momentum phase, extension/ATR distance, coverage and report/config version.

Research evaluates expectancy/Net R, drawdown, frequency, MAE/MFE, entry/exit efficiency, hold duration and costs—not win rate alone.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/indicators.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests prove chronological EMA/RSI/ATR, no-future values, UNKNOWN handling, volatility/momentum/extension states, shared ATR reuse, frozen timeframe separation, M1 non-authority, restart determinism and replay parity.

## 18. Scalp calibration pending

Volatility-state bands, extension thresholds, short-window volatility metrics, optional divergence/percentile context and marginal value of any added metric remain evidence questions. EMA20/EMA50, RSI14 and ATR14 remain the preserved baseline unless a later governed evidence packet changes them.