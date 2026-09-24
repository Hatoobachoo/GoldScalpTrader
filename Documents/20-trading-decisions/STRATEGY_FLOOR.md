# GoldScalpTrader — Strategy Floor

**Status:** FROZEN V1 STRATEGY ARCHITECTURE — CALIBRATION PENDING
**Version:** 1.0-six-family-scalp-floor
**Authority:** Six independent production strategy-family hypotheses, shared evidence, logical independence, optional confluence, correlation control, attribution and runtime handoff.

## 1. Purpose

The Strategy Floor defines six independent, auditable scalp hypotheses. It does not own monetary risk, hard session/news permission, broker identity, controller ownership or order execution.

> Parallel hypotheses, bounded evidence, no sequential filter soup, no unanimity requirement.

Every family consumes the same verified IntelligenceSnapshot. Outputs remain attributable until BUY/SELL fusion.

## 2. Frozen six-family map

Audit 1 retains:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

The narratives remain distinct enough at M5 scalp horizon that premature merging would reduce attribution and research clarity.

## 3. Frozen timeframe baseline

```text
H1  → broad soft regime / important directional-volatility context
M15 → opportunity location, path, liquidity/session context
M5  → primary completed-bar scalp setup/timing structure
H4  → optional major context only
M1  → diagnostic/research only
quote/spread → executable condition, not strategy-history authority
```

No family may quietly use M1 as an independent V1 trigger.

## 4. FamilyReport contract

Each report preserves:

- family identity;
- independent BUY and SELL cases;
- score/strength and evidence coverage;
- support/conflict labels;
- source timestamps/lineage;
- nearest plausible structural objective;
- path/room context;
- preferred timing profile;
- event/freshness context;
- session/regime attribution;
- correlation/event-cluster identity where needed.

A FamilyReport is soft analytical evidence, not broker permission.

## 5. Family definitions

### 5.1 Trend Pullback Continuation

Is an established short-horizon move resuming after a controlled pullback into useful location?

Evidence may include H1/M15 context, M15/M5 location, M5 pullback/resumption, EMA/ATR/momentum, liquidity path and session context. Optional FVG/OB/Fib/trendline/POC is not mandatory.

### 5.2 Breakout Expansion

Is a meaningful level being accepted and releasing fresh expansion with remaining executable room?

Use causal M15/M5 level/break evidence, completed-bar acceptance, M5 displacement/volatility, path/target room and chase protection. A perfect retest is not mandatory.

### 5.3 Breakout Retest Continuation

Did a meaningful break hold on a fresh retest with M5 continuation structure?

Use prior causal break, M15/M5 retest area, M5 hold/reclaim/rejection, target room and event freshness. Exact retest invalidation is owned by `BREAKOUT_RETEST_GEOMETRY.md`.

### 5.4 Liquidity Sweep Reversal

Was a pre-existing pool taken and rejected strongly enough for a short-horizon reversal scalp?

Require a pre-existing pool plus causal sweep/reclaim and credible M5 response. A wick alone is insufficient.

### 5.5 Failed Breakout Reversal

Did attempted acceptance beyond a meaningful level fail and produce a credible opposing response?

Use causal failed-break evidence, M5 opposing response/MSS/reclaim, M15 location/path, target room and freshness.

### 5.6 Compression Expansion

Did a real compressed range release with fresh directional evidence and enough remaining room?

Use M15/M5 compression, causal boundary, M5 release/acceptance, volatility build, path/room and session context. Direction is never guessed before release evidence.

## 6. Optional confluence

```text
supportive Trendline/Fib/POC/FVG/OB → bounded positive support
missing optional context             → no automatic base penalty
opposed/unclear optional context     → visible conflict/context
POC alone                            → no direction
```

Optional confluence cannot become a hidden universal gate.

## 7. Correlation / overlap

Families can describe the same episode:

- sweep + failed breakout;
- breakout/retest + pullback;
- compression release + breakout expansion.

Fusion must use event lineage/correlation bounding so correlated labels do not become fake independent certainty. Family identity still remains visible for attribution/research.

## 8. Logical parallelism / scheduling

Semantic contract:

```text
one immutable IntelligenceSnapshot
→ six pure FamilyReports
→ deterministic canonical ordering
→ bounded optional confluence
→ BUY/SELL fusion
```

Logical independence is required. Actual concurrent worker scheduling is optional and may be enabled only when profiling justifies it. A one-worker run is always valid and must be semantically identical.

Workers cannot mutate lifecycle state, size lots, persist Intents or call MT5.

## 9. Frequency / quality evidence

Research evaluates jointly:

- Opportunity Recall and meaningful missed moves;
- analytical ENTER and capacity-admitted trade frequency;
- Net R/expectancy after costs;
- drawdown/loss streak;
- MAE/MFE;
- entry/capture/exit efficiency;
- hold duration;
- spread/slippage/latency;
- family/session/regime attribution;
- correlated-family contribution.

Higher historical win rate alone is not sufficient to justify a stricter filter.

## 10. Planned implementation ownership

```text
src/gold_scalp_trader/strategies/floor.py
src/gold_scalp_trader/strategies/parallel.py
src/gold_scalp_trader/strategies/confluence.py
src/gold_scalp_trader/decisions/fusion.py
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
```

## 11. Planned proof

Tests must prove same-snapshot inputs, independent BUY/SELL cases, attribution survival, no unanimity requirement, optional-evidence semantics, correlation bounding, serial/parallel semantic parity and zero family broker/risk authority.

## 12. Calibration pending

Family evidence weights, thresholds, preferred trigger profiles, event freshness, session conditioning, correlation caps and Opportunity thresholds remain replay/stress/holdout questions.