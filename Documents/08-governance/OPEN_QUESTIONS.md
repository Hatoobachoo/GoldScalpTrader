# GoldScalpTrader — Open Questions and Evidence Register

**Status:** FINAL POST-FREEZE REGISTER — NO UNRESOLVED ARCHITECTURE QUESTIONS
**Version:** 2.1-final-calibration-external-register
**Authority:** Remaining calibration, implementation choices, external proof, deferred architecture and future approval items. Frozen architecture decisions are not reopened here.

## 1. Classification

```text
CALIBRATION          approved design dimension; empirical value/shape pending
IMPLEMENTATION       source/tooling detail that must preserve frozen behavior
EXTERNAL PROOF       broker/platform/environment fact requiring connected verification
DEFERRED             deliberately outside current enabled architecture
APPROVAL_REQUIRED    future live/production change awaiting explicit operator approval
PRESERVED DEFAULT    current production default remains until a governed future change
```

There are **no unresolved core architecture questions** blocking implementation.

## 2. Frozen items — not open

The following are closed and must not be repeatedly reopened during coding:

- market-first Setup Detector;
- exactly one `ACTIVE_EXECUTION` strategy + five `SHADOW_ONLY` during isolation testing;
- no strategy forcing onto unrelated chart behavior;
- M5 setup authority + subordinate M1 entry refinement;
- News/Fundamental soft-only; no News hard block/cooldown/warmup;
- physical analytical concurrency profiling-driven;
- fixed emergency spread + spread/SL + spread/target + cost/reward architecture;
- preserved SMALL/MEDIUM/NORMAL Risk values;
- preserved disabled-by-default aggressive 8%/16% capability;
- one fresh same-episode re-entry + 3-loss/30m cooldown baseline;
- one independent Gold position initially;
- central Gate/one-shot Intent/sole writer/reconciliation;
- continuous backend invention/tuning/ML with final production approval gate;
- one-screen no-scroll Swing-style graphical dashboard;
- no runtime Git;
- sequential same-scope machine handoff;
- distributed active-active/fencing deferred;
- ~120/day as benchmark, not quota.

## 3. CALIBRATION register

| ID | Item | Evidence needed |
|---|---|---|
| CAL-001 | M1 entry-refinement patterns by family | chronological replay + shadow + DEMO |
| CAL-002 | M1 trigger freshness | replay/DEMO age vs outcomes |
| CAL-003 | M5 setup/event age | family/session/regime evidence |
| CAL-004 | chase distance | entry efficiency / missed vs bad chase outcomes |
| CAL-005 | Approved Entry→Executable Price drift | cost/room/outcome evidence |
| CAL-006 | absolute emergency spread ceiling | Exness spread distribution + anomaly evidence |
| CAL-007 | acceptable spread/SL ranges | family/volatility after-cost evidence |
| CAL-008 | acceptable spread/target ranges | target-room/cost evidence |
| CAL-009 | minimum total cost/reward quality | replay + DEMO fills |
| CAL-010 | slippage allowance | controlled DEMO distribution |
| CAL-011 | broker deviation policy | Exness execution mode + rejection/fill evidence |
| CAL-012 | decision→send latency budget | real Windows/MT5 stage timings |
| CAL-013 | minimum gross R | Scalp replay/DEMO after-cost evidence |
| CAL-014 | minimum net/cost-adjusted quality | same |
| CAL-015 | six family qualification thresholds | out-of-sample family evidence |
| CAL-016 | within-family evidence weights | ablation / stability |
| CAL-017 | event/family correlation caps | causal overlap analysis |
| CAL-018 | EMA/RSI/Fib/FVG/OB/Trendline/POC contribution per family | ablation / recall / expectancy |
| CAL-019 | Asia/London/NY/overlap family performance | segmented sample evidence |
| CAL-020 | time-efficiency EXIT | family/regime hold-time and progress distributions |
| CAL-021 | protection timing | MFE/MAE/capture evidence |
| CAL-022 | trailing timing/hierarchy | management replay + DEMO |
| CAL-023 | Runner conditions | continuation/objective/capture evidence |
| CAL-024 | partial-close expectancy | divisible-volume research |
| CAL-025 | PRE_CLOSE exact timing if reference baseline needs update | current broker evidence + policy review |
| CAL-026 | reopen/gap thresholds | current broker gap/spread/data behavior |
| CAL-027 | ~120/day throughput capability | opportunity funnel + after-cost expectancy |
| CAL-028 | Strategy Isolation evaluation-window length / switch evidence threshold | active-vs-shadow sample adequacy |
| CAL-029 | Dynamic Strategy Router value | only after clean family-isolation evidence |

## 4. PRESERVED DEFAULTS while calibration continues

Calibration does not mean production has no defaults.

Current preserved defaults include:

- exact SMALL/MEDIUM/NORMAL monetary profiles/bands;
- aggressive mode disabled by default;
- manual daily-loss reset disabled by default;
- one same-episode re-entry;
- 3 losses → at least 30m cooldown + release conditions;
- one independent Gold position;
- daily/weekend PRE_CLOSE and reopen reference baselines;
- News/context cache TTL 1800s as context freshness baseline;
- six preserved family definitions;
- current Strategy Isolation policy until a governed production switch.

## 5. IMPLEMENTATION choices

These may be decided during coding without changing frozen behavior:

| ID | Choice |
|---|---|
| IMP-001 | supported Python + current MetaTrader5 package combination |
| IMP-002 | exact SQLite WAL/synchronous/migration/checksum settings |
| IMP-003 | scheduler worker mechanism after deterministic serial baseline/profiling |
| IMP-004 | exact internal DTO/class/file decomposition when ownership remains unchanged |
| IMP-005 | graphical UI technology/library that can meet one-screen functional chart contract |
| IMP-006 | chart rendering/data-cache architecture |
| IMP-007 | consistent checkpoint/export format implementation |
| IMP-008 | document verifier implementation details |
| IMP-009 | local ML/research libraries that stay outside broker authority |
| IMP-010 | performance telemetry storage/aggregation format |

Any implementation choice that changes behavior becomes an architecture/governance change and is not automatically allowed.

## 6. EXTERNAL PROOF register

| ID | Required proof |
|---|---|
| EXT-001 | actual Exness XAUUSDm/XAUUSD digits/point/tick size/value/contract/volume min-max-step/stops/freeze/filling/trade mode |
| EXT-002 | current broker daily/weekend/DST/holiday schedule |
| EXT-003 | real quote timestamp/freshness behavior |
| EXT-004 | spread distributions by session/regime |
| EXT-005 | actual slippage/deviation/fill behavior |
| EXT-006 | decision→send→ack→reconcile latency |
| EXT-007 | margin/order_check behavior |
| EXT-008 | controlled OPEN/MODIFY/SL/TP/CLOSE lifecycle |
| EXT-009 | manual close of known bot position deal lineage |
| EXT-010 | restart during unresolved/active lifecycle |
| EXT-011 | checkpoint restore on fresh/new path |
| EXT-012 | sequential laptop handoff |
| EXT-013 | graphical dashboard performance on intended Windows display geometry |

## 7. DEFERRED items

Explicitly deferred:

```text
same-account active-active multi-machine broker writers
distributed DB / Redis / etcd / consensus fencing architecture
mandatory paid third-party News/macro API
GitHub Actions / cloud compute as a required project dependency
sophisticated partial-close optimizer as release dependency
```

These are intentional exclusions, not forgotten features.

## 8. APPROVAL_REQUIRED future items

Explicit operator approval is required before:

- changing preserved monetary Risk percentages/bands;
- production switch to a new strategy/candidate/policy where governance requires approval;
- enabling a future Dynamic Strategy Router in production;
- promoting any autonomous invention/ML candidate to live production;
- activating REAL trading;
- changing repository visibility;
- adding same-scope active-active/distributed execution;
- adding mandatory paid/cloud dependencies.

## 9. Closure rule

A calibration/external item closes only when evidence is attached to a versioned proposal and every affected owner/document/test is synchronized.

Research result alone never silently mutates production.
