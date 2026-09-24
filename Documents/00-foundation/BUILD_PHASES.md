# GoldScalpTrader — Build Phases

**Status:** FROZEN V1 BUILD MODEL — PRESERVATION-FIRST CORRECTION / IMPLEMENTATION PENDING
**Version:** 1.1-preserved-feature-dependency-order
**Authority:** Dependency order, phase ownership, evidence order and universal exit gates.

## 1. Dependency order

```text
1–2 Foundation + broker reads
→ 3 Market intelligence + bounded analytical scheduler
→ 4 Six-family strategy + decisions
→ 5 TradePlan + profiled monetary Risk
→ 6 Session/news + persistence/recovery
→ 7 controlled DEMO execution + controller/reconciliation
→ 8 Trade Manager + close recovery
→ 9 Operator dashboards
→ 10 Research + durable/live learning
→ 11 Local runtime backup + recovery drills + machine handoff
→ 12 Compliance/connected/release audits
→ future governed REAL release gate
```

The reference feature set remains baseline. Build phases adapt trading-horizon semantics for scalping but do not remove unrelated capabilities.

## 2. Universal phase exit gate

A phase is not complete merely because code exists. Require current owning contracts, full affected-graph review, explicit source/test ownership, failure/UNKNOWN semantics, persistence/operator/research consequences, deterministic proof and honest classification of calibration/external evidence.

## 3. Phase 1 — Product/domain/config/package

Own project identity, typed IDs/enums, settings/modes, policy/schema identity, secret boundary and installable local package.

Configuration must represent:

- SMALL/MEDIUM/NORMAL profile policy;
- explicit disabled-by-default `AGGRESSIVE_SMALL_ACCOUNT` option;
- manual reset disabled by default;
- News provider/cache baseline including 1800s TTL;
- READINESS/DRY_RUN/DEMO stages and future REAL policy identity.

## 4. Phase 2 — MT5 read boundary / MarketSnapshot

Own MT5 readiness, account/server identity, Gold SymbolSpec, Bid/Ask/spread/timestamp, completed H1/M15/M5 (+ optional H4) candles, optional diagnostic M1, positions/deals/exposure and immutable snapshot.

## 5. Phase 3 — Market intelligence + scheduler

Own candle/structure, EMA/RSI/ATR/volatility, technical levels/location, liquidity/SMC, session, fundamental/news and bounded optional confluence.

Implement preserved bounded analytical concurrency for dependency-independent work plus deterministic one-worker fallback/parity.

Scalp emphasis: causal timestamps, event freshness, cost/volatility context and no-lookahead.

## 6. Phase 4 — Strategy / decisions

Own six preserved families, attribution/correlation control, BUY/SELL teams, Red Team, Floor Manager, persistent Opportunity and completed-M5 timing with WAIT/MISSED/ENTER/re-arm semantics.

## 7. Phase 5 — TradePlan / profiled Risk

TradePlan owns family-aware invalidation, SL, objectives, immutable original R, path/target quality, gross structural quality and cost-adjusted room.

Risk owns:

```text
SMALL / MEDIUM / NORMAL fixed risk-day profile
reference target/elevated/hard/daily bands
broker-aware lot/min-lot affordability
margin/exposure/capacity
preserved cooldown/re-entry
manual reset feature disabled by default
optional explicit AGGRESSIVE_SMALL_ACCOUNT overlay disabled by default
```

Aggressive overlay semantics:

```text
8% max SL-risk ceiling, not target
16% max aggregate open risk
16% daily loss ceiling
```

Risk never repairs bad geometry.

## 8. Phase 6 — Session/news / persistence/restart

Own market states, known blackout, scalp true-News-UNKNOWN new-entry block, valid LKG cache resilience, risk/system state machine, StateStore integrity, startup reconciliation, checkpoint/restore and rolling local runtime backups.

Initial preserved baselines:

```text
News provider TTL 1800 seconds
Daily PRE_CLOSE T-20 / T-10
Weekend PRE_CLOSE T-60 / T-30
Daily reopen 1 clean completed M5
Weekend reopen 2 clean completed M5 + gap assessment
```

Broker schedule remains connected external proof. No runtime Git operation.

## 9. Phase 7 — Execution/controller

Own controlled DEMO policy, account/symbol/controller identity, Gate, action-sensitive OPEN/MODIFY/CLOSE checks, durable Intent, one-shot submission, sole MT5Writer and reconciliation.

Future REAL capability is preserved but remains unavailable until the later REAL release gate.

## 10. Phase 8 — Trade Manager / verified close

Own HOLD/PROTECT/TRAIL/RUNNER/EXIT, scalp time-efficiency EXIT reasoning, monotonic protection, broker-valid partial management where divisible, broker-side/manual close recovery, closure receipt and exactly-once learning handoff.

Minimum-lot correctness cannot depend on partial close.

## 11. Phase 9 — Operator surfaces

Own terminal dashboard, responsive narrow/wide/fallback rendering, blocker/Gate truth, current Risk profile/overlay visibility, health diagnostics and optional localhost graphical dashboard. All remain read-only.

## 12. Phase 10 — Research / learning

Own chronological cost-aware replay, verified datasets, walk-forward/holdout/stress, StrategyMemory, actual trade learning, missed/blocked episodes, discovery/invention and governed promotion/rollback.

Scalp research emphasizes cost, latency, freshness, duration and capture efficiency. Research never grants broker authority.

## 13. Phase 11 — Local backup / recovery drills

Runtime:

```text
transactional StateStore
+ rolling checkpoints
+ final shutdown checkpoint
+ portable runtime recovery package
+ sequential machine handoff drill
```

Development:

```text
coherent remote bulk commit
→ operator git pull --ff-only
→ local clone = source + Git-history backup
→ optional secret-clean ZIP milestone copy
```

## 14. Phase 12 — Audits / DEMO release evidence

Audit 1 architecture review is corrected by the preservation-first rule. Later work includes Documents→Code→Tests compliance, Gate/presentation truth, corrective audits, component review, release checklist and final DEMO release audit.

## 15. Future governed REAL gate

The REAL feature is preserved, not implicitly enabled.

Its implementation/activation requires a separate governed release packet after the controlled DEMO system has the required deterministic, connected lifecycle, recovery and operator evidence plus explicit operator approval.

## 16. Parallelism rule

Bounded analytical concurrency is a preserved target capability. Immutable shared inputs, no side effects, bounded workers, deterministic output order, one-worker fallback and parity proof are mandatory.

Broker authority never enters analytical worker pools.