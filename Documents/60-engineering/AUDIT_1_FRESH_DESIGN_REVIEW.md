# GoldScalpTrader — Audit 1 Fresh Architecture and Design Review

**Status:** COMPLETE FRESH-ZERO DESIGN AUDIT — PRESERVATION-FIRST CORRECTION APPLIED
**Version:** 1.1-preservation-corrected
**Authority:** Fresh-from-zero architecture/design challenge, constrained by the operator requirement that GoldSwingTraderAI features/defaults remain unless a direct scalping reason or explicit operator instruction justifies a change.

## 1. Review question

The corrected review question is:

> If GoldScalpTrader were designed for selective Gold scalping while preserving the requested GoldSwingTraderAI feature set, which reference behaviours genuinely need to change **because of scalping**, and which must remain unchanged?

Fresh-zero review is not permission to simplify unrelated features merely because a simpler design is possible.

Tie-breaker:

```text
clear direct scalp requirement → change may be justified
explicit operator instruction   → change as instructed
proven reference defect         → correct through governed packet
otherwise                       → preserve Swing feature/default
```

## 2. Classification vocabulary

```text
KEEP AS-IS
KEEP + SCALP EMPHASIS
SCALP-SPECIFIC CHANGE
USER-DIRECTED CHANGE
REFERENCE DEFECT CORRECTION
NEEDS SCALP CALIBRATION
NEEDS EXTERNAL DEMO PROOF
```

`REMOVE / SIMPLIFY` is not an acceptable verdict for a non-scalp feature without an explicit operator/governance decision.

## 3. High-level verdict

The reference engineering/feature spine remains the baseline:

```text
one normalized read boundary
→ immutable cycle snapshot
→ bounded-parallel independent analytical desks/families
→ BUY/SELL debate
→ persistent Opportunity
→ timing
→ structural TradePlan
→ account-profile monetary Risk
→ hard authorities
→ central Gate
→ persist-before-send Intent
→ sole writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ downstream learning/research
→ local recovery
```

Serial financial/broker authority remains unchanged.

The genuinely scalp-specific changes are primarily:

- shorter timeframe authority;
- stricter event/trigger freshness and anti-chase semantics;
- explicit cost-adjusted target-room treatment;
- removal of inherited 1.20R as an automatic hard scalp floor;
- runner/time-efficiency management changes;
- stronger quote/drift/latency observability;
- conservative News UNKNOWN handling with valid-cache resilience.

The earlier Audit-1 simplifications of account Risk profiles, analytical concurrency and future REAL capability were **not scalp-required** and are superseded by this correction.

## 4. Module-by-module verdict

| Module / feature | Corrected verdict | Result |
|---|---|---|
| Product mission | SCALP-SPECIFIC CHANGE | selective short-duration Gold scalps; not HFT/noise chasing |
| Documentation-first governance | KEEP AS-IS | 64-file canonical manual remains authority |
| One MT5 read boundary | KEEP AS-IS | preserved |
| Immutable MarketSnapshot | KEEP AS-IS | preserved |
| Completed-candle causality | KEEP AS-IS | preserved |
| H1/M15/M5 hierarchy | SCALP-SPECIFIC CHANGE | H1 broad soft, M15 opportunity/location, M5 setup/timing/management |
| H4 role | SCALP-SPECIFIC CHANGE | optional major context, not universal scalp veto |
| M1 role | KEEP AS-IS AFTER CHALLENGE | diagnostic/research only; no hidden production trigger |
| quote/tick role | KEEP + SCALP EMPHASIS | executable condition/freshness, not retroactive structure |
| staged intelligence desks | KEEP AS-IS | preserved |
| bounded analytical concurrency | KEEP AS-IS | reference target feature retained; deterministic one-worker fallback/parity also required |
| six-family strategy floor | KEEP AS-IS | all six retained |
| family overlap/correlation | KEEP + SMALL IMPROVEMENT | explicit event-lineage bounding |
| BUY/SELL independent fusion | KEEP AS-IS | preserved |
| Red Team / Floor Manager | KEEP AS-IS | preserved |
| persistent Opportunity | KEEP AS-IS | preserved |
| event freshness | SCALP-SPECIFIC CHANGE | first-class stale/chase/age semantics |
| M5 completed-bar timing | SCALP-SPECIFIC CHANGE | production timing on completed M5 |
| structural TradePlan before Risk | KEEP AS-IS | preserved |
| family-aware invalidation | KEEP + SCALP EMPHASIS | tighter event geometry only when causally proven |
| fixed Swing 1.20R hard floor | SCALP-SPECIFIC CHANGE | not automatically inherited; scalp gross/net/cost room must be calibrated |
| cost-adjusted room | SCALP-SPECIFIC ADDITION | spread/friction burden first-class |
| automatic SMALL/MEDIUM/NORMAL profiles | KEEP AS-IS | restored; non-scalp feature must not be removed |
| Swing profile risk bands/daily locks | KEEP AS-IS | restored baseline values |
| operator 8%/16% aggressive small-account mode | USER-DIRECTED KEEP | preserved operational option, disabled by default; 8% ceiling not target |
| manual daily-loss reset capability | KEEP AS-IS | feature preserved, disabled by default |
| cooldown/re-entry defaults | KEEP AS-IS | one fresh same-episode re-entry; three losses → at least 30m cooldown + release conditions |
| dynamic lot sizing | KEEP AS-IS | preserved |
| structural-stop distortion to fit 0.01 | KEEP PROHIBITED | preserved |
| one independent Gold position | KEEP AS-IS | preserved |
| News BLACKOUT | KEEP AS-IS | hard new-entry block |
| News UNKNOWN | SCALP-SPECIFIC CHANGE | true UNKNOWN blocks new entries; management remains action-sensitive |
| valid cached News during temporary API outage | REFERENCE/AVAILABILITY REFINEMENT + USER DIRECTION | still-valid last-known-good event truth remains usable; no timestamp laundering |
| provider TTL baseline | KEEP AS-IS | Swing 1800-second baseline retained until a specific scalp/provider reason changes it |
| PRE_CLOSE defaults | KEEP AS-IS | daily T-20/T-10; weekend T-60/T-30 restored |
| reopen defaults | KEEP AS-IS | daily 1 clean M5; weekend 2 + gap assessment restored |
| DRY_RUN first | KEEP AS-IS | preserved |
| DEMO writer progression | KEEP AS-IS | controlled DEMO before REAL |
| future REAL capability | KEEP AS-IS AS FUTURE FEATURE | preserved, disabled until DEMO/release/explicit approval; not silently removed |
| central Gate / Intent / sole writer / reconciliation | KEEP AS-IS | preserved |
| action-sensitive CLOSE | KEEP AS-IS | preserved |
| latency observability | KEEP + SCALP EMPHASIS | stronger because scalp edge decays quickly |
| Trade Manager action set | KEEP AS-IS | HOLD/PROTECT/TRAIL/RUNNER/EXIT |
| runner behaviour | SCALP-SPECIFIC CHANGE | exceptional rather than default continuation |
| time efficiency | SCALP-SPECIFIC CHANGE | first-class EXIT reason |
| partial management | KEEP AS CAPABILITY | broker-valid partial management may exist when volume divisible; 0.01 correctness cannot depend on it |
| SQLite/local recovery | KEEP AS-IS | preserved |
| runtime Git publication | USER-DIRECTED CHANGE | removed; no runtime GitHub credentials/push |
| development/source backup | USER-DIRECTED CHANGE | bulk remote commit → `git pull --ff-only` → optional clean ZIP |
| learning/StrategyMemory | KEEP AS-IS | preserved |
| discovery/invention/promotion | KEEP AS-IS | preserved |
| terminal/browser dashboards | KEEP AS-IS | read-only |
| same-scope single-writer safety | KEEP AS-IS | preserved |

## 5. Frozen scalp-specific decisions

### 5.1 Timeframes

```text
H1   broad soft regime / directional-volatility context
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/freshness
```

### 5.2 Strategy families

Retain:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

### 5.3 Cost/freshness

A scalp needs both:

```text
structural/gross geometry
AND
cost-adjusted executable room
```

Execution separately rechecks fresh Bid/Ask/spread/drift. Costs are counted once; stop/target are not moved to manufacture acceptable R.

### 5.4 News UNKNOWN

```text
OPEN + accepted News CLEAR    → may continue
OPEN + accepted News BLACKOUT → BLOCK
OPEN + true NEWS_UNKNOWN      → new-entry BLOCK / LIMITED
```

Temporary refresh failure with still-valid accepted cache does not itself create UNKNOWN.

### 5.5 Trade management

Time/efficiency weakness can produce normal `EXIT`. Runner is exceptional and requires fresh continuation/new objective.

## 6. Restored non-scalp reference defaults

### 6.1 Risk profiles

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal target | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

### 6.2 Aggressive small-account option

Explicitly preserved because the operator requested it:

```text
disabled by default
eligible baseline: positive DayStartEquity < $1,000
8%  = maximum monetary SL risk per trade, NOT target
16% = maximum aggregate open risk
16% = daily loss ceiling
```

All structural and hard safety remains intact.

### 6.3 Cooldown / re-entry

Preserve reference baseline: one genuinely fresh same-episode re-entry; three consecutive closed bot losses trigger at least 30 minutes global cooldown plus fresh M15/healthy-state release conditions.

### 6.4 Session/reopen/provider defaults

Preserve reference baselines until specifically justified otherwise:

```text
Daily pre-close:   T-20 no new entry, T-10 mandatory flatten
Weekend pre-close: T-60 no new entry, T-30 mandatory flatten
Daily reopen:      1 clean completed M5
Weekend reopen:    2 clean completed M5 + gap assessment
Provider TTL:      1800 seconds baseline
```

External broker schedule proof is still required; preservation does not turn an outdated broker schedule into current fact.

### 6.5 Analytical concurrency

Bounded physical concurrency remains a target feature for dependency-independent analysis. One-worker deterministic fallback and parity are mandatory.

### 6.6 REAL capability

REAL is preserved as a future governed capability, not an initial shortcut. It remains disabled/unavailable until DEMO evidence, release gates and explicit operator approval satisfy its policy.

## 7. What remains open for genuine scalp calibration

- minimum gross structural R / cost-adjusted room;
- event age/distance/chase thresholds;
- spread/slippage/deviation thresholds;
- session-specific strategy performance;
- News blackout/post-event stabilization if scalp evidence justifies changing inherited event behaviour;
- time-efficiency EXIT thresholds;
- Runner/Expansion continuation policy;
- latency thresholds and diagnostics.

Non-scalp reference features/defaults are not automatically reopened.

## 8. External proof still required

Connected Windows/Exness evidence must verify current SymbolSpec, broker schedule/holiday truth, margin, order metadata, spread/slippage/latency, DEMO OPEN/MODIFY/CLOSE/reconciliation, close recovery and recovery-package behaviour.

## 9. Implementation gate

Audit 1 is complete only together with this preservation-first correction. The affected canonical graph must reflect these corrected verdicts before implementation begins.

At final documentation review, the operator and project will explicitly discuss the remaining **genuinely scalp-specific** differences. No Audit 1 statement is a profitability claim.