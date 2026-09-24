# GoldScalpTrader — Trading Floor Architecture

**Status:** FROZEN V1 ARCHITECTURE — PRESERVATION-FIRST CORRECTION / SCALP CALIBRATION PENDING
**Version:** 1.1-preserved-bounded-parallel-floor
**Authority:** Specialist-team ownership, bounded analytical parallelism, Opportunity capture, correlation control and hard-authority boundaries.

## 1. Why a trading floor

GoldScalpTrader is not one giant strategy function and not a checklist bot requiring every indicator to agree.

Each specialist desk asks one bounded question, publishes typed evidence and has an explicit authority limit.

Objectives:

1. build evidence-rich, internally challenged scalp theses;
2. preserve Opportunity Recall so valid Gold moves are not discarded merely because optional evidence is neutral/unavailable;
3. preserve the reference bounded-parallel analytical capability while keeping broker authority serial.

Soft analytical evidence and hard financial/broker authority remain separate.

## 2. Preservation rule

The six-family floor, BUY/SELL debate, Red Team, staged desk design and bounded concurrency remain reference features.

Only scalp-specific timing/freshness/cost semantics are changed. Simplifying a reference feature because a serial implementation is easier is not permitted.

## 3. Shared immutable truth

All analytical desks consume one normalized immutable MarketSnapshot plus declared upstream reports. No desk privately fetches a fresher MT5 truth.

Current quote/tick facts enter through normalized market-data boundaries and carry timestamps; they do not become retroactive structural evidence.

## 4. Staged floor

### Stage A — Core intelligence

- Candle/Structure;
- Indicators/Volatility;
- Session context;
- current quote/cost/freshness facts.

### Stage B — Specialist intelligence

- Technical Structure/Levels;
- Liquidity/SMC;
- Fundamental/News;
- bounded optional Trendline/Fibonacci/Volume-POC/FVG/OB confluence.

### Stage C — Six strategy-family teams

1. **Trend Pullback Continuation**
2. **Breakout Expansion**
3. **Breakout Retest Continuation**
4. **Liquidity Sweep Reversal**
5. **Failed Breakout Reversal**
6. **Compression Expansion**

Range mean-reversion is not added as a seventh production family without a separate governed decision.

## 5. Scalp timeframe roles

```text
H1   broad soft regime
M15  opportunity/location/path/liquidity/session context
M5   primary completed setup/timing/management structure
H4   optional major context
M1   diagnostic/research only
quote current executable condition
```

No family may hide M1 production authority.

## 6. Family independence / correlation

A family owns one hypothesis, uses shared evidence, publishes attributable BUY/SELL/neutral cases and never owns Risk/Gate/controller/order sending.

Several families can describe the same episode. Event lineage/correlation control prevents one sweep/failed-break/reclaim sequence from being counted as several independent confirmations.

## 7. BUY / SELL teams

BUY and SELL theses are built independently. Strong opposing evidence remains visible rather than merely subtracting points from one confidence score.

The directional floor exposes leading BUY/SELL families, supporting/conflicting evidence, coverage, correlation concerns, freshness/cost concerns and why one side leads or neither qualifies.

## 8. Red Team / Debate

Challenges include late/extended move, stale event, weak target room, probe versus accepted break, hostile volatility/momentum, spread/cost burden, correlated support, opposing thesis and unavailable optional evidence.

Red Team is analytical challenge, not broker permission.

## 9. Opportunity / timing boundary

Opportunity asks:

> Is this thesis worth stalking?

Entry Timing asks:

> Is the current completed-M5 moment fresh and efficient enough to act?

Scalp-specific timing guards chase distance, event age, drift, spread/cost context, remaining room and duplicate-entry/re-arm semantics.

## 10. Preserved bounded analytical concurrency

Dependency-independent desks and the six family evaluations retain bounded physical concurrency as a target feature.

Requirements:

- immutable common inputs;
- dependency-aware stages;
- bounded workers;
- deterministic canonical result order;
- visible worker errors/degradation;
- no persistence/Risk/Gate/broker writes in analytical workers;
- deterministic one-worker fallback;
- parity proof between bounded-parallel and one-worker paths.

Worker count may be tuned after profiling; that is not permission to delete the concurrency feature.

## 11. Hard-authority handoff

```text
DecisionBoard
→ Opportunity
→ completed-M5 Entry Timing
→ TradePlan gross + cost-adjusted room
---------------- analytical/geometry boundary ----------------
→ SMALL/MEDIUM/NORMAL monetary Risk
   + optional explicit aggressive overlay
→ hard permission authorities
→ central Gate
→ Intent
→ sole MT5Writer
→ reconciliation
```

## 12. Risk interaction

The Trading Floor does not pick account Risk policy.

Risk independently resolves the fixed DayStartEquity profile and any explicitly enabled eligible aggressive overlay. Family score/recent wins cannot increase monetary Risk.

## 13. Dashboard / research

Dashboard shows desk/family/debate/Opportunity/timing facts but recalculates no hidden signal/permission/policy.

Family attribution survives trade/close/learning so research can compare narratives and correlation without reconstructing ownership from P/L.

## 14. Scalp calibration pending

Family scores/weights, correlation caps, Opportunity thresholds, event freshness, chase distance and cost/freshness analytical penalties require chronological replay/stress/holdout and connected evidence.

Non-scalp reference floor features are preserved and are not automatically reopened.