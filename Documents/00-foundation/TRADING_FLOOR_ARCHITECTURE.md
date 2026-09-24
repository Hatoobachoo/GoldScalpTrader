# GoldScalpTrader — Trading Floor Architecture

**Status:** FROZEN V1 ARCHITECTURE — CALIBRATION PENDING
**Version:** 1.0-six-family-logical-floor
**Authority:** Specialist-team ownership, logical analytical parallelism, Opportunity capture, correlation control and hard-authority boundaries.

## 1. Why a trading floor

GoldScalpTrader is not one giant strategy function and not a checklist bot requiring every indicator to agree.

Each specialist desk asks one bounded question, publishes typed evidence and has an explicit authority limit.

Objectives:

1. build evidence-rich, internally challenged scalp theses;
2. preserve Opportunity Recall so valid Gold moves are not discarded merely because optional evidence is neutral/unavailable.

Soft analytical evidence and hard financial/broker authority remain separate.

## 2. Opportunity-first, not frequency-first

- optional disagreement stays score/conflict/debate;
- one strong attributable family may lead with others neutral;
- required safety failures remain hard BLOCK/UNKNOWN;
- stale/cost-dominated opportunities become WAIT/MISSED instead of chase;
- frequency is an evidence outcome, never a safety override.

## 3. Shared immutable truth

All analytical desks consume one normalized immutable MarketSnapshot plus declared upstream reports. No desk privately fetches a fresher MT5 truth.

Current quote/tick facts enter through normalized market-data boundaries and carry timestamps; they do not become retroactive structural evidence.

## 4. Frozen staged floor

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

Audit 1 freezes:

1. **Trend Pullback Continuation** — controlled retracement then short-horizon directional resumption.
2. **Breakout Expansion** — fresh accepted break releasing expansion without late chase.
3. **Breakout Retest Continuation** — meaningful break holds on a fresh executable retest.
4. **Liquidity Sweep Reversal** — pre-existing pool is taken/rejected with reclaim/shift.
5. **Failed Breakout Reversal** — attempted acceptance fails and opposing response forms.
6. **Compression Expansion** — causal compressed range releases with directional evidence.

Range mean-reversion is not a seventh V1 production family; it may be researched later. Generic “Momentum Expansion” is represented through Breakout/Compression narratives rather than an overlapping family.

## 5. Frozen timeframe roles

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

Several families can describe the same episode. Event lineage/correlation control must prevent one sweep/failed-break/reclaim sequence from being counted as several independent confirmations.

## 7. BUY / SELL teams

BUY and SELL theses are built independently. Strong opposing evidence remains visible rather than merely subtracting points from one confidence score.

The directional floor exposes leading BUY/SELL families, supporting/conflicting evidence, coverage, correlation concerns, freshness/cost concerns and why one side leads or neither qualifies.

## 8. Red Team / Debate

Challenges include:

- late/extended move;
- stale event;
- weak target room;
- probe versus accepted break;
- hostile volatility/momentum;
- spread/cost burden;
- correlated support;
- opposing thesis;
- unavailable optional evidence.

Red Team is analytical challenge, not broker permission.

## 9. Floor Manager

Produces an auditable DecisionBoard/Opportunity handoff such as BUY_LEADS, SELL_LEADS, CONFLICTED, WAIT or NO_QUALIFIED_OPPORTUNITY.

It does not set monetary risk or grant final permission.

## 10. Opportunity / timing boundary

Opportunity asks:

> Is this thesis worth stalking?

Entry Timing asks:

> Is the current completed-M5 moment fresh and efficient enough to act?

Timing guards chase distance, event age, drift, spread/cost context, remaining room and duplicate-entry/re-arm semantics. M1 remains diagnostic only.

## 11. Logical parallelism / physical concurrency

All six families and dependency-independent desks are **logically independent**.

Physical concurrent workers are optional/profiling-driven. Requirements if used:

- immutable common input;
- bounded workers;
- deterministic canonical result order;
- one-worker semantic parity;
- visible worker failure/degradation;
- no persistence/Risk/Gate/broker writes inside analytical workers.

Concurrency is an optimization, not an authority.

## 12. Hard-authority handoff

```text
DecisionBoard
→ Opportunity
→ completed-M5 Entry Timing
→ TradePlan gross + cost-adjusted room
---------------- analytical/geometry boundary ----------------
→ STANDARD monetary Risk
→ hard permission authorities
→ central Gate
→ Intent
→ sole MT5Writer
→ reconciliation
```

This serial financial/broker spine is non-negotiable without a governed architecture change.

## 13. Dashboard / research

Dashboard shows desk/family/debate/Opportunity/timing facts but recalculates no hidden signal/permission.

Family attribution survives through trade/close/learning so research can compare narratives and correlation without reconstructing ownership from P/L.

## 14. Calibration pending

Family scores/weights, correlation caps, Opportunity thresholds, session conditioning, event freshness and cost/freshness analytical penalties require chronological replay/stress/holdout and connected evidence.