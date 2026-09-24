# GoldScalpTrader — Build Phases

**Status:** FROZEN V1 BUILD MODEL — IMPLEMENTATION / CALIBRATION / EXTERNAL PROOF PENDING
**Version:** 1.0-post-audit1-dependency-order
**Authority:** Dependency order, phase ownership, evidence order and universal exit gates.

## 1. Dependency order

```text
1–2 Foundation + broker reads
→ 3 Market intelligence
→ 4 Six-family strategy + decisions
→ 5 TradePlan + STANDARD monetary Risk
→ 6 Session/news + persistence/recovery
→ 7 DEMO execution + controller/reconciliation
→ 8 Trade Manager + close recovery
→ 9 Operator dashboards
→ 10 Research + durable/live learning
→ 11 Local runtime backup + recovery drills + machine handoff
→ 12 Compliance/connected/release audits
```

Canonical architecture was drafted and Fresh-Zero Audit 1 completed before implementation. Every phase still requires synchronized source/test/document evidence.

## 2. Universal phase exit gate

A phase is not complete merely because code exists. Require current owning contracts, full affected-graph review, explicit source/test ownership, failure/UNKNOWN semantics, persistence/operator/research consequences, deterministic proof, and honest classification of calibration/external evidence.

## 3. Phase 1 — Product/domain/config/package

Own project identity, typed IDs/enums, settings/modes, policy/schema identity, secret boundary and installable local package structure.

First implementation work also repairs provisional `src/` package/run layout.

## 4. Phase 2 — MT5 read boundary / MarketSnapshot

Own MT5 readiness, account/server identity, resolved Gold symbol, SymbolSpec, Bid/Ask/spread/timestamp, completed H1/M15/M5 (+ optional H4) candles, optional diagnostic M1, positions/deals/exposure and immutable snapshot.

M1 diagnostics cannot become hidden production timing authority.

## 5. Phase 3 — Market intelligence

Own candle/structure, EMA/RSI/ATR/volatility, technical levels/location, liquidity/SMC, session, fundamental/news and bounded optional confluence.

Emphasize causal timestamps, event freshness, cost/volatility context and no-lookahead.

Physical concurrency is optional only after one-worker semantics/profiling justify it.

## 6. Phase 4 — Strategy / decisions

Own six frozen families, attribution/correlation control, BUY/SELL teams, Red Team, Floor Manager, persistent Opportunity and completed-M5 timing with WAIT/MISSED/ENTER/re-arm semantics.

## 7. Phase 5 — TradePlan / Risk

TradePlan owns family-aware invalidation, SL, objectives, immutable original R, path/target quality, gross structural quality and cost-adjusted room.

Risk owns one STANDARD policy, broker-aware lot/min-lot affordability, hard ceiling, margin/exposure, daily safety state and cooldown/re-entry.

Risk never repairs bad geometry.

## 8. Phase 6 — Session/news / persistence/restart

Own market states, known blackout, V1 News UNKNOWN new-entry block, risk/system state machine, StateStore integrity, startup reconciliation, checkpoint/restore and rolling local runtime backups.

No runtime Git operation.

## 9. Phase 7 — Execution/controller

Own controlled DEMO policy, account/symbol/controller identity, Gate, action-sensitive OPEN/MODIFY/CLOSE checks, durable Intent, one-shot submission, sole MT5Writer and reconciliation.

REAL remains deferred V1.

## 10. Phase 8 — Trade Manager / verified close

Own HOLD/PROTECT/TRAIL/RUNNER/EXIT, time/efficiency EXIT reasoning, monotonic protection, broker-side/manual close recovery, closure receipt and exactly-once learning handoff.

## 11. Phase 9 — Operator surfaces

Own terminal dashboard, responsive narrow/wide/fallback rendering, blocker/Gate truth, health diagnostics and optional localhost graphical dashboard. All remain read-only.

## 12. Phase 10 — Research / learning

Own chronological cost-aware replay, verified datasets, walk-forward/holdout/stress, StrategyMemory, actual trade learning, missed/blocked episodes, discovery/invention and governed promotion/rollback.

Research never grants broker authority.

## 13. Phase 11 — Local backup / recovery drills

Runtime side:

```text
transactional StateStore
+ rolling checkpoints
+ final shutdown checkpoint
+ portable runtime recovery package
+ sequential machine handoff drill
```

Development side:

```text
coherent remote bulk commit
→ operator git pull --ff-only
→ local clone = source + Git-history backup
→ optional secret-clean ZIP milestone copy
```

Git bundle is optional advanced/manual only. Automatic archives exclude secrets.

## 14. Phase 12 — Audits / release evidence

Audit 1 fresh-zero architecture review is already complete. Later phase-12 work includes Documents→Code→Tests compliance, Gate/presentation truth, evidence-triggered corrective audits, component review, release checklist and final release audit for one exact revision/config/environment.

## 15. Parallelism rule

Serial semantics are canonical. If physical parallelism is added: immutable shared inputs, no side effects, bounded workers, deterministic output order, one-worker fallback and parity proof are mandatory. Broker authority never enters analytical pools.