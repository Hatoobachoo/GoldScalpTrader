# GoldScalpTrader — Candle Structure and Price Behaviour

**Status:** DRAFT PRE-CHALLENGE INTELLIGENCE CONTRACT
**Version:** 0.1-scalp-causal-structure
**Authority:** Candle anatomy, chronological sequences, causal swings, protected structure, BOS/MSS maturity, failed breaks, displacement, rejection, compression, expansion and short-horizon event freshness.

## 1. Purpose

This desk answers:

> What did Gold actually do on completed candles, when did that fact become knowable, and is that structural event still fresh enough to matter to a scalp?

It is market intelligence only. It does not choose a strategy, size risk, approve a broker write or manage an existing trade.

## 2. Non-negotiable invariants

| Invariant | Required behaviour |
|---|---|
| Completed-candle authority | A forming candle is never structural proof. |
| Causal knowledge time | Geometry identity and the time a fact became knowable remain separate. |
| No lookahead | Historical/replay prefixes cannot contain future-confirmed swings or breaks. |
| Timeframe independence | H1, M15, M5 and optional H4/M1 reports do not rewrite each other. |
| Shared normalization | ATR/quant inputs are reused from the shared IntelligenceSnapshot. |
| Soft output | Structure is evidence; it does not become final broker permission. |
| Explicit absence | Insufficient evidence is UNKNOWN/empty coverage, never invented trend. |
| Freshness lineage | Every actionable structural event carries event/confirmation time so downstream timing can detect stale setups. |

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

The draft model should expose:

- `CandleFacts`: direction, range, body, wick, close position and ATR-normalized range;
- `CandleSequenceState`: continuation, expansion, rejection, compression or mixed;
- `SwingPoint`: side, price, pivot time, confirmed-at time, role and significance;
- `StructureState`: BULLISH, BEARISH, RANGE, TRANSITION or UNDETERMINED;
- `BreakEvent`: PROBE, QUALIFIED_BREAK, BOS, MSS or FAILED_BREAK;
- protected high/low where causally established;
- bounded bull/bear evidence and coverage;
- event age/freshness inputs for downstream Entry Timing.

## 5. Timestamp semantics

MT5 candle time identifies bar open. Facts requiring the completed high/low/close become knowable no earlier than bar close.

```text
bar_open_time  = Candle.time_utc
bar_close_time = Candle.time_utc + timeframe_duration
```

A swing records both its pivot identity and when the later reversal confirmed it. BOS/MSS/failed-break events use the close time of the bar that made the event knowable.

This distinction is especially important for scalping because a five-minute error in event age can turn a fresh trigger into a chased move.

## 6. Candle anatomy

For a completed candle the baseline derives:

```text
range
body
upper_wick
lower_wick
body_ratio
close_position
range_in_ATR
```

A bullish or bearish candle label is descriptive only. Named candlestick patterns cannot become standalone BUY/SELL authority.

## 7. Sequence states

The initial vocabulary is:

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

Expansion, rejection and compression are normalized to volatility. One large Gold candle is not automatically a breakout and one wick is not automatically a reversal.

## 8. Swing lifecycle

```text
CANDIDATE
→ CONFIRMED
→ PROTECTED
→ MAJOR / EXTERNAL where justified
```

A candidate can move while new completed candles form. It has no structural authority until confirmed causally.

Protected structure requires an accepted consequence, not merely a visually important pivot.

## 9. Break/BOS/MSS lifecycle

Baseline progression:

```text
PROBE
→ QUALIFIED_BREAK
→ CONFIRMED_BOS or MSS_CANDIDATE
→ CONFIRMED_MSS or FAILED_BREAK
```

A wick-only penetration is not BOS/MSS. A counter-structure break is not automatically a full reversal. The strategy family decides how much maturity its thesis requires.

## 10. Scalp freshness

GoldScalpTrader adds a stronger downstream freshness requirement than a swing system.

Structure publishes the factual event time; it does not hard-code how many minutes the event remains tradable. Entry Timing owns the final freshness policy.

Downstream consumers should be able to distinguish:

```text
JUST_CONFIRMED
FRESH
AGING
STALE_FOR_ENTRY
```

These labels may be derived later from policy/calibration. The source event timestamp is mandatory even before those labels are frozen.

## 11. Timeframe baseline

| Timeframe | Draft structure role |
|---|---|
| H4 | optional major context only |
| H1 | broad regime / major protected structure |
| M15 | opportunity/location structure |
| M5 | primary scalp setup, break, rejection and trigger structure |
| M1 | diagnostic microstructure in baseline; no hidden independent authority |

The fresh-zero challenge must decide whether M1 graduates from diagnostic context into explicit timing evidence.

## 12. Correlation and double counting

A rejection, failed break, sweep and MSS can describe the same episode. Structure publishes traceable facts; later Strategy/Fusion must not count correlated labels as four independent votes.

## 13. Restart and replay

The same completed candle prefix, configuration and shared quantitative inputs must rebuild the same structure report after restart.

Replay must expose only bars whose close time is already knowable at the simulated decision timestamp. A swing/event cannot appear before its `confirmed_at`/`event_time`.

## 14. Failure behaviour

| Condition | Result |
|---|---|
| no candles | explicit analysis failure |
| insufficient history | UNKNOWN/lower coverage |
| corrupt chronology | rejected upstream |
| forming-bar input | contract violation; reject upstream |
| no downstream consumer | report remains valid; no hidden order path |

## 15. Dashboard/research visibility

Operator/research views should expose at least:

- H1/M15/M5 structure separately;
- latest event and direction;
- event age;
- protected high/low where known;
- sequence state;
- coverage;
- report/configuration version.

## 16. Planned implementation ownership

```text
src/gold_scalp_trader/intelligence/candle_structure.py
src/gold_scalp_trader/intelligence/snapshot.py
```

## 17. Planned proof

Tests must prove:

- causal swing confirmation;
- bar-close knowledge timestamps;
- probe versus qualified break;
- BOS versus MSS versus failed break;
- no-lookahead replay;
- timeframe separation;
- restart determinism;
- event age/freshness inputs;
- shared ATR reuse.

## 18. Pre-challenge calibration

Open items include swing reversal distance, break penetration, follow-through maturity, protected-swing promotion, sequence thresholds, significance ranking, M5 freshness categories and any M1 timing role.
