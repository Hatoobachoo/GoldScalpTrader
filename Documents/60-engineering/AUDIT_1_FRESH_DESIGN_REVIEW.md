# GoldScalpTrader — Audit 1 Fresh Architecture and Design Review

**Status:** COMPLETE FRESH-ZERO DESIGN AUDIT — POST-AUDIT SYNC PACKET
**Version:** 1.0-fresh-zero-scalp-review
**Authority:** Fresh-from-zero architecture/design challenge, module-by-module and feature-by-feature. This audit does not claim profitability, connected broker proof or implementation completion.

## 1. Review question

This audit deliberately asks:

> If GoldScalpTrader were designed today from zero chat history, with the same user requirements and retail Exness/MT5 constraints, what architecture would we build, what would we keep, simplify, change, remove or add?

GoldSwingTraderAI is treated as a high-quality reference, not as automatic truth. The provisional GoldScalpTrader code is not treated as correct merely because it exists.

## 2. Classification vocabulary

```text
KEEP AS-IS
SMALL IMPROVEMENT
SHOULD CHANGE
MAJOR ARCHITECTURAL CHANGE
REMOVE / SIMPLIFY
ADD
NEEDS REAL-MARKET CALIBRATION
NEEDS EXTERNAL DEMO PROOF
```

## 3. High-level verdict

The reference engineering spine remains sound for a scalper:

```text
one normalized read boundary
→ immutable cycle snapshot
→ independent analytical desks
→ independent strategy families
→ BUY/SELL debate
→ persistent Opportunity
→ timing
→ structural TradePlan
→ independent monetary Risk
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

The fresh-zero review does **not** recommend a monolithic EMA bot, direct strategy-to-MT5 calls, multiple ad-hoc risk gates, self-editing live AI, active-active multi-laptop state, paid cloud infrastructure or HFT-style tick-history complexity for V1.

The largest upgrades are scalp-specific semantics inside otherwise strong boundaries: timeframe authority, cost/freshness treatment, risk-policy simplification, News UNKNOWN behaviour, time-efficiency management and developer backup workflow.

## 4. Module-by-module verdict

| Module / feature | Fresh-zero verdict | Result |
|---|---|---|
| Product mission | KEEP AS-IS | selective short-duration Gold trades; not HFT and not trade-every-noise |
| Documentation-first governance | KEEP AS-IS | 64-file canonical manual remains the durable project authority |
| One MT5 read boundary | KEEP AS-IS | avoids contradictory account/symbol/quote/candle truth |
| Immutable MarketSnapshot | KEEP AS-IS | shared deterministic facts for all desks |
| Completed-candle causality | KEEP AS-IS | structural/indicator facts use completed bars and knowledge time |
| H1/M15/M5 role hierarchy | KEEP AS-IS → FREEZE | H1 broad soft regime, M15 opportunity/location, M5 primary setup/timing/management |
| H4 role | KEEP AS-IS → FREEZE | optional major context only; never universal scalp veto |
| M1 role | REMOVE INDEPENDENT AUTHORITY / FREEZE | V1 diagnostic/research only; no hidden M1 trigger authority |
| quote/tick role | KEEP AS-IS | current executable condition/health, not retroactive structural proof |
| tick-history intelligence | DEFERRED V1 | unnecessary complexity until replay proves need |
| staged intelligence desks | KEEP AS-IS | structure/quant/technical/liquidity/session/news remain separable |
| physical analytical concurrency | SMALL IMPROVEMENT | logical independence is required; actual worker concurrency is optional and profiling-driven; one-worker path is canonical semantic fallback |
| six-family strategy floor | KEEP AS-IS | all six narratives remain meaningfully distinct at scalp horizon |
| family overlap/correlation | SMALL IMPROVEMENT | retain explicit correlation bounding/event lineage so one episode is not counted as several independent confirmations |
| BUY/SELL independent fusion | KEEP AS-IS | visible opposing thesis is better than one opaque score |
| Red Team / Floor Manager | KEEP AS-IS | analytical conflict remains separate from hard safety |
| persistent Opportunity | KEEP AS-IS | thesis identity must survive WAIT and restart context |
| terminal Opportunity semantics | KEEP AS-IS | same thesis cannot reappear as a fake new episode |
| event freshness | ADD / FREEZE ARCHITECTURE | every executable event needs causal knowledge time and entry-freshness classification; thresholds calibrate |
| M5 completed-bar timing | KEEP AS-IS → FREEZE | V1 entry timing remains completed-M5 based; quote revalidates execution conditions |
| chase/extension protection | KEEP AS-IS | strong idea can become MISSED instead of being chased |
| structural TradePlan before Risk | KEEP AS-IS | account size cannot rewrite market invalidation |
| family-aware invalidation | KEEP AS-IS | retest/sweep/failed-break geometry may use exact proven event structure |
| fixed Swing 1.20R floor | REMOVE AS INHERITED POLICY | no automatic transplant; scalp threshold is a calibration problem |
| gross structural room | KEEP / FREEZE | plan must remain structurally worthwhile independent of account size |
| cost-adjusted room | ADD / FREEZE ARCHITECTURE | TradePlan must preserve explicit spread/friction-aware room metric; final execution rechecks current quote/drift |
| transaction-cost double counting | KEEP PROHIBITED | spread/fees/slippage sources must be counted exactly once |
| fixed SMALL/MEDIUM/NORMAL risk tiers | REMOVE / SIMPLIFY | automatic equity tiers add policy complexity without improving actual min-lot affordability truth |
| V1 monetary risk policy | SHOULD CHANGE → FREEZE | one STANDARD policy with preferred risk, hard per-trade ceiling, daily limit and actual min-lot evaluation |
| optional aggressive small-account mode | DEFER / RESEARCH ONLY | explicit, disabled by default, never auto-selected by balance; old 8%/16% values are not active policy |
| dynamic lot sizing | KEEP AS-IS | normalize to broker min/max/step then evaluate actual all-in risk |
| structural-stop distortion to fit 0.01 | KEEP PROHIBITED | unaffordable minimum lot blocks current plan |
| one independent Gold position per scope | KEEP AS-IS | bounded exposure and simpler recovery |
| martingale/grid/averaging rescue | KEEP PROHIBITED | no loss-recovery escalation |
| News BLACKOUT | KEEP AS-IS | hard new-entry block |
| News UNKNOWN | SHOULD CHANGE → FREEZE | blocks **new entries** in V1; management/protection/mandatory CLOSE continue under their own authorities |
| session OPEN/CLOSED/PRE_CLOSE/WARMUP | KEEP AS-IS | mechanism retained; exact minutes/calibration remain external/research evidence |
| DRY_RUN first | KEEP AS-IS | no irreversible broker writer before implementation milestone |
| DEMO writer progression | KEEP AS-IS → FREEZE | controlled DEMO is first broker-write target after deterministic proof |
| REAL trading | DEFERRED V1 | separate future governance decision; no hidden flag |
| central Execution Gate | KEEP AS-IS | one permission composition surface |
| persist-before-send Intent | KEEP AS-IS | one irreversible send allowance per Intent |
| ambiguous acknowledgement | KEEP AS-IS | reconcile; never blind retry |
| sole MT5Writer | KEEP AS-IS | one raw irreversible boundary |
| action-sensitive CLOSE | KEEP AS-IS | OPEN friction rules must not mechanically trap unwanted exposure |
| scalp latency observability | KEEP / ADD | measure quote/decision/send/reconcile delay; not an HFT claim |
| Trade Manager action set | REMOVE / SIMPLIFY | keep HOLD/PROTECT/TRAIL/RUNNER/EXIT; time efficiency is an EXIT reason, not a separate TIME_EXIT action |
| runner behaviour | KEEP AS-IS WITH SCALP LIMIT | exceptional continuation only; not default target behaviour |
| partial close requirement | DEFERRED V1 | correctness cannot depend on divisible volume at 0.01 lot |
| SQLite local state | KEEP AS-IS | appropriate zero-cost transactional V1 boundary |
| current broker truth after restore | KEEP AS-IS | restored state is context, never exposure truth |
| local rolling runtime backup | KEEP AS-IS | independent of GitHub/network |
| runtime Git commit/push | REMOVE | no runtime GitHub credentials/publication authority |
| development/source backup | SHOULD CHANGE → FREEZE | major bulk commit → operator `git pull --ff-only`; local clone is primary full-history backup; optional secret-clean ZIP source snapshot after milestone |
| Git bundle | REMOVE AS DEFAULT | optional manual advanced backup only, not normal workflow/runtime responsibility |
| learning/StrategyMemory boundary | KEEP AS-IS | verified outcomes only; no direct broker authority |
| discovery/invention | KEEP AS-IS | declarative proposal only |
| promotion governance | KEEP AS-IS | no self-promotion; holdout/stress/approval remain explicit |
| terminal dashboard primary | KEEP AS-IS | read-only operator truth |
| browser dashboard | KEEP AS-IS | optional localhost/read-only; not trading dependency |
| GitHub Actions/Codespaces/LFS | REMOVE AS REQUIREMENT | local verification/source control keeps zero-cost target |
| same-scope active-active laptop control | MAJOR CHANGE — DEFERRED | would require shared atomic fencing + globally ordered durable lifecycle |

## 5. Final fresh-zero architecture choices

### 5.1 Timeframes

```text
H1   broad regime / major directional-volatility context — soft
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management structure
H4   optional major context only
M1   diagnostic / research only in V1
quote current executable Bid/Ask/spread/drift/health only
```

M1 cannot silently become production entry authority through a helper. Promoting it later requires a governed design change and replay/evidence.

### 5.2 Strategy families

Retain six starting families:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

No family is a universal gate. Correlated descriptions of the same episode must be bounded rather than counted as independent certainty.

### 5.3 Cost/freshness architecture

A scalp needs two separate truths:

```text
structural/gross geometry
AND
cost-adjusted executable room
```

TradePlan owns the first cost-aware planning view from current known facts. Execution owns the final fresh Bid/Ask/spread/drift recheck immediately before broker submission. Neither layer may move SL/target to manufacture acceptable R.

Exact minimum gross R, net/cost-adjusted room, spread reserve and drift thresholds remain calibration items.

### 5.4 Risk-policy simplification

V1 does not automatically select SMALL/MEDIUM/NORMAL risk bands from equity. Use one explicit STANDARD production policy:

```text
preferred per-trade risk target
hard per-trade risk ceiling
daily loss limit
one-position capacity
loss/cooldown/re-entry state
actual broker-minimum-lot affordability
```

Account size still matters mathematically through equity, tick value, structural stop, volume step/minimum and actual risk percentage.

An `AGGRESSIVE_EXPERIMENT` may exist later only as explicit research/future opt-in, disabled by default and never auto-selected. Historical 8%/16% values are not active policy.

### 5.5 News UNKNOWN

For V1 new entry:

```text
Session OPEN + News CLEAR    → may continue to other authorities
Session OPEN + News BLACKOUT → hard BLOCK
Session OPEN + News UNKNOWN  → new-entry BLOCK / limited state
```

News UNKNOWN is not renamed CLEAR. Existing bot position management/protection/mandatory CLOSE remains possible through action-specific authorities.

### 5.6 Trade management

No separate `TIME_EXIT` action in V1. Time/efficiency is a first-class reason that may produce ordinary `EXIT` when calibrated rules prove the scalp is no longer behaving like a scalp.

### 5.7 Parallel/serial rule

Logical specialist independence is architectural. Physical concurrent workers are an implementation optimization only when profiling shows benefit. Deterministic one-worker execution is always valid and must match bounded-parallel semantics.

### 5.8 Development backup

Normal development backup after a major documentation/code bulk:

```text
remote bulk commit
→ user runs git pull --ff-only
→ local clone now contains complete source + Git history
→ optional local secret-clean ZIP snapshot for an extra offline copy
```

The trading runtime does not create commits, push, pull or require GitHub credentials.

## 6. What I would not upgrade from zero

A fresh design would still keep:

- typed domain identities and explicit UNKNOWN;
- one read boundary and immutable snapshots;
- causal completed-bar knowledge time;
- separate intelligence desks;
- six attributable hypotheses rather than one opaque checklist;
- BUY/SELL debate + Red Team;
- persistent Opportunity identity;
- structural TradePlan before monetary Risk;
- broker-aware min-lot sizing;
- centralized Gate;
- durable one-shot Intent;
- sole writer + reconciliation;
- strict manual/bot ownership separation;
- crash-safe persistence/recovery;
- verified-close-before-learning ordering;
- governed research/discovery/promotion;
- read-only dashboards;
- local-first/zero-cost deployment.

The audit found no reason to replace these with a simpler-but-less-auditable monolith.

## 7. Main upgrades versus reference Swing design

1. Scalping timeframe hierarchy is explicit and M1 remains non-authoritative.
2. Event freshness and cost-adjusted room are first-class entry concepts.
3. Risk architecture is simplified from automatic account tiers to one explicit STANDARD policy.
4. News UNKNOWN is conservative for new entries.
5. Time efficiency is a management thesis rule without adding another lifecycle action.
6. Physical concurrency is optional, not architectural theatre.
7. Runtime repository publication is removed.
8. Development backup is bulk-pull + optional local ZIP, minimizing GitHub usage.
9. REAL execution is explicitly outside V1 rather than a configuration accident.

## 8. Remaining calibration

Architecture is decided; these values still require chronological replay/stress/holdout and/or connected DEMO evidence:

- minimum gross structural R;
- minimum cost-adjusted room / room-to-cost ratio;
- family/Opportunity/timing score thresholds;
- event age/distance/chase thresholds;
- spread/slippage/deviation limits;
- STANDARD preferred/hard per-trade risk values;
- daily-loss/cooldown/re-entry values;
- session specialization;
- blackout/post-news/reopen/pre-close times;
- time-efficiency exit thresholds;
- runner/Expansion frequency;
- worker count after profiling;
- backup cadence/retention.

These are `CALIBRATION PENDING`, not architecture gaps.

## 9. Remaining external proof

Connected Windows/Exness DEMO still must prove:

- exact XAUUSDm SymbolSpec/min lot/step/tick value/stops/freeze/filling/margin;
- real schedule/holiday behaviour;
- AutoTrading/trade API/order_check/order_send retcodes;
- spread/slippage/latency distributions;
- natural OPEN/MODIFY/CLOSE/reconciliation lifecycle;
- broker-side/manual close recovery;
- fresh-machine restore and no duplicate exposure;
- exactly-once live learning.

## 10. Implementation gate

Audit 1 closes the **fresh-zero architecture questions**, but implementation still waits for the affected canonical contracts/guides to be synchronized with these decisions.

After synchronization, accepted architecture contracts may be marked FROZEN while numerical values remain `CALIBRATION PENDING` and broker behaviour remains `EXTERNAL PROOF PENDING`.

No Audit 1 statement is a profitability claim.