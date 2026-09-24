# GoldScalpTrader — Indicators and Volatility

**Status:** DRAFT PRE-CHALLENGE QUANTITATIVE EVIDENCE CONTRACT
**Version:** 0.1-scalp-quant
**Authority:** EMA20/EMA50, RSI14, ATR14, volatility normalization, momentum phase, compression/expansion measurement, extension/chase and short-horizon execution-context evidence.

## 1. Purpose

The Quant desk makes Gold price behaviour measurable across changing volatility regimes. It supports and normalizes structure; it does not replace structure.

> Indicators explain pressure, distance, volatility and extension. They do not independently create a trade or broker permission.

## 2. Invariants

| Rule | Meaning |
|---|---|
| Completed bars only | forming candles are excluded from indicator series |
| One calculation per snapshot | indicator series are computed once and shared |
| Chronological arrays | values use only information available at that point |
| Explicit missingness | None/UNKNOWN is not a bearish or neutral vote |
| ATR normalization | prefer volatility-relative geometry to fixed Gold points |
| Soft evidence | hard safety belongs elsewhere |
| No filter soup | no rule requiring every indicator/timeframe to agree |

## 3. Baseline indicator family

The initial reference set is retained for challenge:

```text
EMA fast  = 20
EMA slow  = 50
RSI       = 14 (Wilder)
ATR       = 14 (Wilder)
```

These are design seeds, not frozen profitability parameters. The challenge/research process may keep or replace them only with explicit evidence.

## 4. Quant pipeline

```text
completed CandleSeries
→ EMA/RSI/ATR chronological series
→ ATR-normalized candle/range/extension facts
→ volatility state
→ momentum phase
→ QuantReport + coverage
```

The report is shared with Structure, Technical, Liquidity, Strategy, Entry Timing, Trade Plan and Trade Manager.

## 5. EMA flow

EMA20 versus EMA50 may publish directional support:

```text
EMA20 > EMA50 → BUY support
EMA20 < EMA50 → SELL support
otherwise      → NONE/UNKNOWN
```

EMA order is not a strategy. A scalp still needs structure, location, freshness, path room, transaction-cost viability and timing.

Potential later research can inspect slope/separation/pullback depth without turning them into universal gates.

## 6. RSI pressure

RSI14 is pressure context, not a rigid overbought/oversold reversal command.

A strong trend can remain above 70 or below 30 while continuing. RSI disagreement is evidence, not automatic veto.

Divergence remains a research candidate until validated and governed.

## 7. ATR as shared volatility unit

ATR may normalize:

- candle strength;
- swing confirmation/significance;
- zone width;
- liquidity clustering;
- volatility regime;
- extension/chase;
- structural stop/target context;
- spread/room ratios;
- entry drift and movement since trigger.

ATR does not independently set the final SL/TP.

## 8. Volatility states

Draft vocabulary:

```text
UNKNOWN
QUIET
NORMAL
BUILDING
EXPANDING
EXTREME
DISLOCATED
```

Exact boundaries remain calibration.

EXTREME is context/warning, not universal rejection. DISLOCATED is adverse evidence that later timing/session/execution authorities may treat more strongly.

## 9. Momentum phase

Draft states:

```text
UNKNOWN
BUILDING
EXPANDING
MATURE
EXHAUSTING
REVERSING
```

Momentum may combine EMA flow, recent completed-close progress, body/ATR efficiency, RSI pressure and extension.

Strong momentum can still be a poor scalp entry when price is already too extended or transaction-cost-adjusted room is small.

## 10. Extension and chase protection

Baseline extension measurement can use:

```text
abs(close - EMA20) / ATR
```

with draft states:

```text
UNKNOWN
FRESH
NORMAL
EXTENDED
SEVERELY_EXTENDED
```

Extension is analytical evidence. Entry Timing combines it with structural-event age, trigger freshness and current executable market facts.

## 11. Scalp-specific quantitative context

Without adding hidden new indicators, the Quant desk may publish derived measurements useful for scalping:

- recent bar range/ATR;
- body efficiency;
- short-window realized expansion/compression;
- distance travelled since the structural event in ATR;
- current spread relative to ATR or intended gross room as descriptive context;
- recent volatility acceleration/deceleration.

Any metric that becomes a hard broker gate must move to or be explicitly owned by the appropriate risk/execution contract.

## 12. Timeframe baseline

| Timeframe | Draft quant role |
|---|---|
| H4 | optional broad volatility context |
| H1 | broad regime/trend support |
| M15 | opportunity volatility and extension context |
| M5 | primary scalp momentum/extension/setup quality |
| M1 | diagnostic micro-volatility until promoted |

The system never requires all timeframes to agree.

## 13. Compression, expansion and exhaustion ownership

Quant supplies normalized measurements. Candle Structure owns the multi-bar sequence label. This prevents the same market episode from being double counted as separate certainty.

Exhaustion does not automatically reverse the thesis or close a trade; relevant structural/liquidity evidence is still required.

## 14. Restart/replay

The same completed prefix plus QuantConfig must reproduce the same series/report after restart. Missing values remain missing rather than being filled with zero.

Chronological replay uses the production calculation at each prefix; no final-bar indicator value may leak backward.

## 15. Dashboard/research visibility

Operator/research views should expose at least:

```text
EMA flow
RSI
ATR
volatility state/ratio
momentum phase
extension state/ATR distance
coverage
report/config version
```

Research evaluates expectancy, Net R, drawdown, trade frequency, MAE/MFE, entry/exit efficiency, hold duration and transaction costs—not win rate alone.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/indicators.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests must prove chronological EMA/RSI/ATR, no-future values, UNKNOWN handling, volatility/momentum/extension states, shared ATR reuse, timeframe separation, restart determinism and replay parity.

## 18. Pre-challenge calibration

Open items: whether EMA20/50 and RSI14 remain optimal baselines, volatility-state bands, extension thresholds, short-window volatility metrics, M1 usefulness, divergence, percentile context and whether any added metric improves out-of-sample performance without creating filter soup.
