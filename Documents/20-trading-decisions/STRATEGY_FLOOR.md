# GoldScalpTrader — Strategy Floor

**Status:** FROZEN V1 STRATEGY ARCHITECTURE — CALIBRATION PENDING
**Version:** 1.1-preserved-bounded-parallel-six-family-floor
**Authority:** Six independent production strategy-family hypotheses, shared evidence, bounded analytical concurrency, optional confluence, correlation control, attribution and runtime handoff.

## 1. Purpose

The Strategy Floor defines six independent, auditable scalp hypotheses. It does not own monetary Risk, hard session/news permission, broker identity, controller ownership or order execution.

> Parallel hypotheses, bounded evidence, no sequential filter soup, no unanimity requirement.

Every family consumes the same verified immutable IntelligenceSnapshot. Outputs remain attributable until BUY/SELL fusion.

## 2. Preserved six-family map

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

The narratives remain separate for attribution/research. No family is removed merely to simplify the scaler.

## 3. Frozen timeframe baseline

```text
H1  → broad soft regime / important directional-volatility context
M15 → opportunity location, path, liquidity/session context
M5  → primary completed-bar scalp setup/timing structure
H4  → optional major context only
M1  → diagnostic/research only
quote/spread → executable condition, not strategy-history authority
```

No family may quietly use M1 as independent production trigger.

## 4. FamilyReport contract

Each report preserves family identity, independent BUY/SELL cases, strength/evidence coverage, support/conflict labels, source timestamps/lineage, plausible objective/path room, timing profile, event/freshness context, session/regime attribution and correlation/event-cluster identity where needed.

A FamilyReport is soft evidence, not broker permission.

## 5. Family definitions

### Trend Pullback Continuation
Established short-horizon move resuming after controlled pullback into useful location.

### Breakout Expansion
Meaningful level accepted and releasing fresh expansion with remaining executable room; perfect retest not mandatory.

### Breakout Retest Continuation
Meaningful causal break holds on fresh retest with M5 continuation structure; exact geometry belongs to `BREAKOUT_RETEST_GEOMETRY.md`.

### Liquidity Sweep Reversal
Pre-existing pool taken/rejected with causal reclaim/shift; wick alone insufficient.

### Failed Breakout Reversal
Attempted acceptance fails and credible opposing response forms.

### Compression Expansion
Causal compressed range releases with directional evidence and enough remaining room; direction never guessed before release.

## 6. Optional confluence

```text
supportive Trendline/Fib/POC/FVG/OB → bounded positive support
missing optional context             → no automatic base penalty
opposed/unclear optional context     → visible conflict/context
POC alone                            → no direction
```

Optional confluence cannot become hidden universal gate.

## 7. Correlation / overlap

Families may describe the same episode. Fusion must bound correlated support using event lineage rather than count one sweep/break/reclaim sequence as several independent confirmations.

## 8. Preserved bounded analytical concurrency

Semantic contract:

```text
one immutable IntelligenceSnapshot
→ six dependency-independent FamilyReports
→ bounded physical workers as target capability
→ deterministic canonical result order
→ bounded optional confluence
→ BUY/SELL fusion
```

The reference bounded-parallel capability is preserved. A deterministic **one-worker fallback** is also mandatory and must be semantically identical.

Worker-count tuning is profiling/implementation choice; the concurrency feature itself is not optional removal.

Workers cannot mutate lifecycle state, size lots, persist Intents or call MT5.

## 9. Frequency / quality evidence

Research evaluates Opportunity Recall, meaningful missed moves, analytical ENTER/capacity-admitted frequency, Net R/expectancy after costs, drawdown/loss streak, MAE/MFE, entry/capture/exit efficiency, hold duration, spread/slippage/latency, family/session/regime attribution and correlated-family contribution.

Historical win rate alone cannot justify stricter universal filters.

## 10. Risk / hard-authority boundary

Family score never selects or increases monetary Risk. Downstream Risk resolves preserved SMALL/MEDIUM/NORMAL profile plus any explicitly enabled eligible aggressive overlay. Session/news/account/controller/Gate remain independent hard authorities.

## 11. Planned implementation ownership

```text
src/gold_scalp_trader/strategies/floor.py
src/gold_scalp_trader/strategies/parallel.py
src/gold_scalp_trader/strategies/confluence.py
src/gold_scalp_trader/decisions/fusion.py
src/gold_scalp_trader/decisions/opportunity.py
src/gold_scalp_trader/decisions/timing.py
```

## 12. Planned proof / calibration

Tests prove same-snapshot inputs, six-family availability, independent BUY/SELL cases, attribution, no unanimity, optional evidence semantics, correlation bounding, bounded-parallel ↔ one-worker parity and zero family broker/Risk authority.

Family weights/thresholds, trigger profiles, event freshness, session conditioning, correlation caps and Opportunity thresholds remain scalp research questions.