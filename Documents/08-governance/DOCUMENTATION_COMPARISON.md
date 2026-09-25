# GoldScalpTrader — GoldSwingTraderAI → GoldScalpTrader Explicit Change Record

**Status:** FINAL CANONICAL DELTA LEDGER — DOCUMENTATION FREEZE BASELINE
**Version:** 2.0-final-explicit-differences
**Authority:** Permanent record of exactly what changed from the GoldSwingTraderAI reference, why it changed, what was explicitly operator-directed, and what was intentionally preserved.

## 1. Governing rule

GoldScalpTrader is a Scalp specialization, not permission to redesign every SwingTrader feature.

```text
reference feature/default
→ preserve by default
→ change only for direct Scalp reason
   OR explicit operator instruction
   OR proven reference defect/current factual correction
```

This file is the canonical answer to:

> **“What exactly did we change from SwingTrader?”**

## 2. Summary

Changes fall into three classes:

```text
A. SCALP-SPECIFIC
B. OPERATOR-DIRECTED / PROJECT-OPERATING
C. PRESERVED — DO NOT CHANGE
```

No change is implied merely because implementation has not started.

# 3. A — Genuine Scalp-specific changes

| # | Area | GoldSwingTraderAI reference | GoldScalpTrader final design | Reason |
|---:|---|---|---|---|
| 1 | Product horizon | wider intraday/swing-style opportunity | short-duration high-opportunity-recall Gold scalping | direct product change |
| 2 | H4 role | stronger broad context role | optional major context only | scalp horizon |
| 3 | H1 role | stronger higher-timeframe directional role | broad soft regime/context | avoid overrestricting short-horizon setups |
| 4 | M15 role | broader setup/entry support | opportunity location/path/target context | scalp hierarchy |
| 5 | M5 role | lower execution/entry timeframe within Swing hierarchy | **primary setup/thesis + normal management structure** | scalp production timeframe |
| 6 | M1 role | diagnostic/research-only reference behavior | **subordinate live entry refinement after valid M5 Opportunity** | improve entry precision without M1-only overtrading |
| 7 | Entry freshness | important but less central | M5 event age, M1 trigger freshness, chase and drift first-class | scalp edge decays quickly |
| 8 | Executable economics | transaction costs material | explicit spread/SL, spread/target, cost/reward, slippage, drift, latency | small scalp targets amplify friction |
| 9 | Fixed spread logic | reference fixed/standard spread safety emphasis | fixed emergency ceiling **plus** context-aware ratios/cost | avoid both broken-market fills and needless normal-market restriction |
| 10 | 1.20R floor | reference hard/primary minimum | not automatically inherited as hard Scalp floor | Scalp gross/net quality differs |
| 11 | Trade efficiency | wider holding horizon tolerated | time-efficiency is first-class EXIT evidence | prevent accidental swing conversion |
| 12 | Runner | broader continuation relevance | exceptional; fresh objective/continuation required | preserve scalp identity |
| 13 | Research metrics | R/MFE/MAE etc. | adds strong opportunity-recall, entry/capture/exit efficiency, cost/latency/throughput metrics | Scalp optimization needs efficiency/throughput |
| 14 | Throughput target | not central | ~120 trades/day used as **research benchmark**, never quota | operator Scalp throughput goal |

# 4. B — Explicit operator-directed architecture/project changes

These are real project changes but are **not falsely labelled “because scalping requires them.”**

## 4.1 One strategy takes live trades at a time

Final policy:

```text
6 families analyze
1 = ACTIVE_EXECUTION
5 = SHADOW_ONLY
```

Purpose: cleanly measure each strategy's efficiency/expectancy before allowing more advanced routing.

This is operator-directed evaluation architecture.

## 4.2 Market-first Setup Detector

Clarified operator requirement:

> Chart/market facts must determine what setup is actually forming. Do not insert every strategy into every trade or force the active strategy onto the chart.

Final behavior:

```text
market facts
→ detect genuine setup(s) or NONE
→ apply active-family eligibility
```

If Liquidity Sweep forms while Breakout Retest is active:

```text
live WAIT
Liquidity Sweep = shadow research
```

No fabricated Breakout Retest.

## 4.3 News removed from hard trading permission

Reference/earlier Scalp drafts used News BLACKOUT/UNKNOWN hard entry protection.

Operator final decision:

```text
News/Fundamental = soft context/research/dashboard only
```

Therefore removed as direct causes of:

- hard new-entry block;
- News cooldown;
- mandatory post-News warmup;
- forced close.

Actual event-induced spread/drift/dislocation/data/execution problems remain governed by their real owners.

## 4.4 Physical parallelism changed to profiling-driven

Reference architecture emphasized bounded physical analytical concurrency as an intended feature.

Final Scalp/operator decision:

```text
logical independence = mandatory
physical concurrency  = profiling-driven
```

Optimization order:

```text
share calculations
→ vectorize/cache
→ serial deterministic baseline
→ profile
→ bounded parallelism only where measured benefit exists
```

Financial/broker authority remains serial.

## 4.5 Runtime Git publication removed

Final rule:

```text
trading runtime performs NO Git fetch/pull/add/commit/push
```

GitHub is source/history/collaboration only.

## 4.6 Development/source backup changed

Final development workflow:

```text
coherent remote commit
→ operator git pull --ff-only
→ local clone contains current source + Git history
→ optional secret-clean ZIP
```

Runtime-state backup is a separate local checkpoint/recovery system.

## 4.7 Same-scope distributed execution deferred

Operator approved deferral of:

- same-account active-active broker writers;
- distributed database/fencing/consensus infrastructure.

Current design supports one PRIMARY + sequential machine handoff.

## 4.8 Paid/cloud mandatory dependencies rejected/deferred

Not required:

- mandatory paid News/macro API;
- GitHub Actions/cloud compute as project dependency.

## 4.9 Sophisticated partial-close optimization deferred

Basic broker-valid partial management capability is preserved. Sophisticated optimizer is not a release dependency.

# 5. C — Explicitly preserved Swing features/defaults — DO NOT CHANGE

These were specifically protected from unintended Scalp simplification.

## 5.1 Monetary Risk profiles and percentages

**No change approved.**

| Profile | DayStartEquity | Normal | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|---:|
| SMALL | positive < $300 | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | $300–$999.99 | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | >= $1,000 | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Do not replace these with one `STANDARD` Risk policy.

## 5.2 Aggressive small-account capability

Preserved, disabled by default:

```text
8%  maximum single-trade monetary SL-risk ceiling — NOT target
16% maximum aggregate open risk
16% daily loss ceiling
```

Do not demote to “research only” and do not auto-enable from balance.

## 5.3 Manual daily-loss reset

Preserved capability, disabled by default.

## 5.4 Cooldown and same-episode re-entry

Preserved baseline:

```text
one genuinely fresh same-episode re-entry
3 consecutive closed bot losses → at least 30-minute cooldown + release conditions
```

Research may propose alternatives later; production baseline is not silently changed.

## 5.5 Six strategy families

All six preserved:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Isolation changes who may take live trades during evaluation; it does not delete strategies.

## 5.6 One normalized MT5 read boundary / immutable snapshot

Preserved.

## 5.7 Causal chronology / no lookahead

Preserved and strengthened for M1.

## 5.8 Independent BUY/SELL and Red Team

Preserved inside the active family. Shadow families are no longer live votes during isolation testing.

## 5.9 Persistent Opportunity vs timing

Preserved.

## 5.10 Structural TradePlan before monetary Risk

Preserved.

## 5.11 Dynamic broker-aware volume/min-lot affordability

Preserved.

Structural stop remains thesis-based and is never tightened just to make minimum volume fit.

## 5.12 One independently risk-bearing Gold position initially

Preserved.

## 5.13 PRE_CLOSE/reopen safety baselines

Preserved pending current broker fact verification:

```text
Daily:   T-20 no entry / T-10 flatten
Weekend: T-60 no entry / T-30 flatten
Daily reopen:   1 clean M5
Weekend reopen: 2 clean M5 + gap assessment
```

A current broker schedule correction is an external fact update, not a strategy redesign.

## 5.14 Central Gate / one-shot Intent / sole writer / reconciliation

Preserved exactly in principle.

Ambiguous acknowledgement → reconciliation, never blind retry.

## 5.15 Manual/external exposure ownership separation

Preserved.

## 5.16 ManagedTrade / verified close

Preserved.

## 5.17 Optional partial management

Preserved where broker-valid/divisible. 0.01-lot correctness cannot depend on partial close.

## 5.18 Persistence/restart/recovery

Preserved local transactional-state architecture, adapted only for no runtime Git publication.

## 5.19 Learning / StrategyMemory

Preserved.

## 5.20 Autonomous strategy invention / AI parameter research / advanced ML

**Preserved as bot-improvement features**, not removed/deferred.

They operate in backend candidate/research lanes and may automatically progress through governed evidence stages.

Final production/live promotion requires explicit operator approval.

## 5.21 Future REAL capability

Preserved as future governed capability; disabled/unavailable until DEMO/recovery/release proof + explicit operator approval.

## 5.22 Graphical dashboard

**Preserved and approved as the Swing-style institutional graphical design adapted for Scalp.**

Final Scalp dashboard requirements:

- same premium one-screen institutional style;
- no scrollbars;
- functional M1/M5/M15/H1/H4 chart controls;
- functional Indicators/Drawings/Settings;
- central chart;
- setup/signal/plan/risk/execution/learning/system panels;
- read-only trading-authority boundary.

Scalp additions include Detected Setup, Active Test Family and Shadow state clarity.

# 6. Reference values preserved but still need external proof

Preserving a reference value does not claim the current broker fact is verified.

Examples:

- Exness trading schedule/DST/holiday behavior;
- SymbolSpec/filling/stops/margin;
- actual spread/slippage/deviation;
- latency;
- DEMO order lifecycle.

Connected proof may update factual broker metadata without reopening unrelated architecture.

# 7. Scalp calibration — architecture approved, numbers not frozen by guess

Approved calibration dimensions:

- M1 patterns/freshness;
- M5 event age;
- chase/drift;
- emergency spread ceiling;
- spread/SL acceptable ranges;
- spread/target acceptable ranges;
- cost/reward;
- slippage allowance;
- broker deviation;
- decision→send latency;
- minimum gross R;
- minimum net/cost-adjusted quality;
- six family thresholds;
- within-family weights;
- event/family correlation caps;
- confluence contribution;
- session performance;
- time-efficiency EXIT;
- protection/trailing;
- Runner conditions;
- partial-close expectancy;
- PRE_CLOSE/reopen-gap current evidence;
- throughput against ~120/day benchmark.

Research/calibration cannot silently mutate production.

# 8. Earlier unintended changes explicitly superseded

Do not revive these prior wrong directions:

```text
single STANDARD Risk policy
reopening/changing preserved Risk bands without approval
8%/16% aggressive mode demoted to research-only
M1 diagnostic-only final Scalp policy
News BLACKOUT/UNKNOWN hard trading block
News cooldown / post-News warmup
mandatory physical analytical parallelism
64-file manual complete claim
removing future REAL capability
removing optional partial management
```

# 9. Final comparison invariant

> **GoldScalpTrader changes what genuinely needs to change for fast Gold scalping and what the operator explicitly directed; all other SwingTrader capabilities/defaults remain preserved. The most visible final changes are market-first setup detection, one-strategy-at-a-time live evaluation, M1 subordinate precision timing, cost-aware execution, News soft-only treatment, profiling-driven concurrency and local-first source/runtime recovery separation.**
