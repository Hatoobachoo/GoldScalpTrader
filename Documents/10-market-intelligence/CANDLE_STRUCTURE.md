# GoldScalpTrader — Candle Structure and Price Behaviour

**Status:** FROZEN V1 INTELLIGENCE ARCHITECTURE — SCALP THRESHOLD CALIBRATION PENDING
**Version:** 1.0-causal-m5-structure
**Authority:** Candle anatomy, chronological sequences, causal swings, protected structure, BOS/MSS maturity, failed breaks, displacement, rejection, compression, expansion and short-horizon event freshness.

## 1. Purpose

This desk answers:

> What did Gold actually do on completed candles, when did that fact become knowable, and is that structural event still fresh enough to matter to a scalp?

It is market intelligence only. It does not choose a strategy, size Risk, approve broker write or manage an existing trade.

## 2. Non-negotiable invariants

| Invariant | Required behaviour |
|---|---|
| Completed-candle authority | forming candle is never structural proof |
| Causal knowledge time | geometry identity and knowable time remain separate |
| No lookahead | replay prefixes contain no future-confirmed swing/break |
| Timeframe independence | H1/M15/M5 and optional H4 reports do not rewrite each other |
| M1 boundary | diagnostic/research only; no independent production authority |
| Shared normalization | ATR/quant inputs reused from shared IntelligenceSnapshot |
| Soft output | structure evidence never becomes final broker permission |
| Explicit absence | insufficient evidence = UNKNOWN/lower coverage, never invented trend |
| Freshness lineage | actionable structural events carry event/confirmation time |

## 3. Causal pipeline

```text
completed chronological candles
→ candle anatomy
→ sequence state
→ candidate swing
→ confirmed swing
→ protected/major structure where earned
→ probe / qualified break / BOS / MSS / failed break
→ StructureReport + coverage + timestamps
```

Later stages may consume earlier facts but cannot manufacture them retroactively.

## 4. Published facts

Expose where applicable:

- `CandleFacts`: direction, range, body, wick, close position, ATR-normalized range;
- `CandleSequenceState`: continuation, expansion, rejection, compression or mixed;
- `SwingPoint`: side, price, pivot time, confirmed-at time, role, significance;
- `StructureState`: BULLISH, BEARISH, RANGE, TRANSITION or UNDETERMINED;
- `BreakEvent`: PROBE, QUALIFIED_BREAK, BOS, MSS or FAILED_BREAK;
- protected high/low where causally established;
- bounded bull/bear evidence and coverage;
- event age/freshness inputs for Entry Timing.

## 5. Timestamp semantics

MT5 candle time identifies bar open. Facts requiring completed OHLC become knowable no earlier than bar close.

```text
bar_open_time  = Candle.time_utc
bar_close_time = Candle.time_utc + timeframe_duration
```

A swing records pivot identity plus later confirmation time. BOS/MSS/failed-break events use the close time that made the event knowable.

For scalping, event-age accuracy is first-class because one completed M5 can materially change whether entry is fresh or chased.

## 6. Candle anatomy

For completed candles derive:

```text
range
body
upper_wick
lower_wick
body_ratio
close_position
range_in_ATR
```

Bullish/bearish candle labels are descriptive only. Named candlestick patterns cannot independently create BUY/SELL authority.

## 7. Sequence states

Baseline vocabulary:

```text
BULL_CONTINUATION
BEAR_CONTINUATION
BULL_EXPANSION
BEAR_EXPANSION
BULL_REJECTION
BEAR_REJECTION
COMPRESSION
MIXED
```

Expansion/rejection/compression are volatility-normalized. One large Gold candle is not automatically breakout; one wick is not automatically reversal.

## 8. Swing lifecycle

```text
CANDIDATE
→ CONFIRMED
→ PROTECTED
→ MAJOR / EXTERNAL where justified
```

A candidate has no structural authority until causally confirmed. Protected structure requires accepted consequence, not merely a visually important pivot.

## 9. Break/BOS/MSS lifecycle

```text
PROBE
→ QUALIFIED_BREAK
→ CONFIRMED_BOS or MSS_CANDIDATE
→ CONFIRMED_MSS or FAILED_BREAK
```

Wick-only penetration is not BOS/MSS. Counter-structure break is not automatically full reversal. Strategy family decides how much maturity its thesis requires.

## 10. Scalp freshness

Structure publishes factual event/knowledge time. Entry Timing owns family/event freshness and chase policy.

Downstream may classify:

```text
JUST_CONFIRMED
FRESH
AGING
STALE_FOR_ENTRY
```

Exact age/distance boundaries remain scalp calibration; the source event timestamp is mandatory.

## 11. Frozen timeframe roles

| Timeframe | Structure role |
|---|---|
| H4 | optional major context only |
| H1 | broad regime / major protected structure |
| M15 | opportunity/location structure |
| M5 | primary scalp setup, break, rejection and trigger structure |
| M1 | diagnostic/research microstructure only |

M1 production promotion is **not an open V1 question**; it requires a future governed design/evidence change.

## 12. Correlation and double counting

Rejection, failed break, sweep and MSS can describe the same episode. Structure publishes traceable facts; Strategy/Fusion must not count correlated labels as independent certainty.

## 13. Restart and replay

Same completed-candle prefix, configuration and shared quantitative inputs must rebuild the same report after restart.

Replay exposes only bars knowable at the simulated timestamp. A swing/event cannot appear before its `confirmed_at`/`event_time`.

## 14. Failure behaviour

| Condition | Result |
|---|---|
| no candles | explicit analysis failure |
| insufficient history | UNKNOWN/lower coverage |
| corrupt chronology | rejected upstream |
| forming-bar structural input | contract violation/reject |
| no downstream consumer | report remains valid; no hidden order path |

## 15. Dashboard/research visibility

Expose H1/M15/M5 structure separately, latest event/direction/age, protected high/low, sequence state, coverage and report/config version. M1 may appear only as explicitly labelled diagnostics/research.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/candle_structure.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests prove causal swing confirmation, bar-close knowledge timestamps, probe versus qualified break, BOS/MSS/failed-break semantics, no-lookahead replay, frozen timeframe separation, M1 non-authority, restart determinism, event-age lineage and shared ATR reuse.

## 18. Scalp calibration pending

Swing reversal distance, break penetration, follow-through maturity, protected-swing promotion, sequence thresholds, significance ranking and M5 family/event freshness categories remain evidence questions. The timeframe authority itself is frozen.