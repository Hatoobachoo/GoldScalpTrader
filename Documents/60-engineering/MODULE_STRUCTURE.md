# GoldScalpTrader — Module Structure and File Map

**Status:** DRAFT PRE-CHALLENGE MODULE MAP
**Version:** 0.1-scalp-source-ownership
**Authority:** Intended file ownership, dependency direction and placement before implementation freeze.

## 1. Purpose

This file decides where code belongs. Behavioural meaning remains in topic contracts. It prevents duplicated ownership and keeps the eventual source/test tree reconstructable from canonical `Documents/`.

Current code is only a provisional scaffold; entries below marked planned do not claim implementation.

## 2. Dependency direction

```text
config + domain + diagnostics + security
→ market_data
→ intelligence — staged bounded analytical work
→ strategies — independent scalp family teams
→ decisions — BUY/SELL + debate + Opportunity + timing + TradePlan
→ risk — monetary authority
→ execution — hard authority + Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

research/learning → evidence/proposals only; never upstream broker authority
persistence → durable context/checkpoints/local backups; never broker truth
```

Dependency-independent analytical work may be concurrent. TradePlan → Risk → hard authority → Gate → Intent → writer → reconciliation remains ordered.

## 3. Package ownership

| Package | Owns | Must not own |
|---|---|---|
| `config` | validated settings/modes | hidden policy override |
| `domain` | enums/IDs/typed facts | MT5 calls |
| `diagnostics` | logs/reasons/health | trading decisions |
| `security` | secret detection/redaction | credentials |
| `market_data` | sole normalized MT5 read boundary + activity | raw write |
| `intelligence` | descriptive specialist evidence | money/write |
| `strategies` | independent scalp hypotheses/scheduler | Risk/Gate |
| `decisions` | fusion/Opportunity/timing/TradePlan | MT5/final permission |
| `risk` | affordability/risk-day/capacity + permission substates | strategy rewrite/send |
| `execution` | Gate/fresh checks/Intent/controller/sole writer/reconcile | strategy invention |
| `management` | ManagedTrade decision/lifecycle | raw MT5 write |
| `persistence` | typed state/checkpoint/local backup/recovery package | broker truth/Git push |
| `app` | startup/runtime/provider/composition/authoritative DTO | duplicate domain policy |
| `operator` | read-only normalization/render/snapshot | authority mutation |
| `research` | replay/learning/discovery/promotion | production broker authority |
| `graphical_dashboard` | local read-only browser | MT5/trading mutation |

## 4. Application/configuration — planned

```text
app/main.py              launcher/runtime modes; no shutdown Git push
app/runtime.py           dependency composition/cycle facts
app/startup.py           startup authority sequence
app/recovery.py          lifecycle recovery/exact close ordering
app/recovery_mt5.py      broker recovery-truth adapter
app/cycle.py             one governed entry/management cycle
app/loop.py              M5/event cadence, heartbeat, learning, local backup, presentation
app/dashboard.py         authoritative DTO mapping
app/live_presentation.py read-only live enrichment/performance facts
app/session_news.py      session/news provider boundary
config/settings.py       validated READINESS/DRY_RUN/PRIMARY/DEMO boundary
```

Current provisional `src/gold_scalp_trader/config.py` may be migrated here only during implementation with tests/docs synchronized.

## 5. Domain / diagnostics / security — planned

```text
domain/enums.py
domain/ids.py
domain/market.py
domain/models.py
diagnostics/logging.py
diagnostics/reasons.py
diagnostics/health.py
security/financial_secrets.py
```

Raw external facts normalize once into typed finite/UTC/domain-validated models.

## 6. Market Data / intelligence — planned

```text
market_data/mt5_reader.py     sole MT5 read boundary
market_data/activity.py       bot/external activity + close proof
market_data/snapshot.py       immutable MarketSnapshot/freshness/quality

intelligence/candle_structure.py
intelligence/indicators.py
intelligence/technical.py
intelligence/liquidity.py
intelligence/confluence.py
intelligence/session.py
intelligence/news.py
intelligence/snapshot.py      dependency-aware bounded composition
```

Baseline semantic order is H1/M15/M5 with optional H4/M1 according to final challenged timeframe contract.

## 7. Strategies / decisions — planned

```text
strategies/floor.py
strategies/parallel.py
strategies/confluence.py

decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
```

The six-family map is a pre-challenge starting design, not implementation proof.

Family geometry adapters may prefer exact causal event boundaries only when proven; they may not invent tighter stops or override general cost/target/risk policy.

## 8. Risk / execution — planned

```text
risk/engine.py
risk/state.py
risk/permissions.py

execution/models.py
execution/checks.py
execution/gate.py
execution/intent_store.py
execution/service.py
execution/mt5_writer.py       sole raw irreversible write boundary — later milestone only
execution/reconcile.py
execution/controller.py
execution/sqlite_coordination.py
```

No `mt5_writer.py` broker-send capability is implemented until the documented execution milestone is approved.

## 9. Management / persistence / learning — planned

```text
management/models.py
management/manager.py
management/execution.py
management/store.py

persistence/store.py
persistence/runtime_state.py
persistence/checkpoint.py
persistence/backup.py
persistence/local_recovery_package.py

research/learning.py
research/live_learning.py
research/replay.py
research/management_replay.py
research/session_history.py
research/stress.py
research/validation.py
research/datasets.py
research/acquisition.py
research/evidence.py
research/packages.py
research/metrics.py
research/outcomes.py
research/ablation.py
research/episode_journal.py
research/discovery.py
research/invention.py
research/promotion.py
```

**Not planned:** `persistence/shutdown_publish.py` runtime Git commit/push path.

## 10. Operator — planned

```text
operator/presentation.py
operator/narrow_dashboard.py
operator/live_dashboard.py
operator/rich_dashboard.py
operator/compact_dashboard.py
operator/graphical_snapshot.py
operator/__init__.py

graphical_dashboard/ui.py
graphical_dashboard/server.py
graphical_dashboard/__main__.py
```

Presentation never recalculates authority.

## 11. Scripts — planned

Potential scripts:

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_git_bundle.py
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
```

No operator script may hide credentials or become an ungoverned broker-write path.

## 12. Forbidden dependency directions

```text
strategy/intelligence worker → MetaTrader5 raw API      NO
parallel analytical worker → lifecycle persistence      NO
parallel analytical worker → Risk/controller/Gate       NO
operator/dashboard → authority recalculation             NO
research/learning → raw broker authority                 NO
checkpoint restore → broker permission                   NO
unknown position → empty exposure                        NO
ambiguous broker result → blind retry                    NO
trading runtime → Git commit/push                        NO
backup package → credential transport by default         NO
```

## 13. Intended runtime trace

```text
app/main.py
→ validated Settings / MT5Reader
→ immutable MarketSnapshot
→ startup/recovery authorities
→ app/cycle.py
   → staged intelligence
   → bounded family scheduler
   → BUY/SELL + Debate/Floor Manager
   → Opportunity/Timing
   → family-aware structural TradePlan
   → monetary Risk
   → hard authorities
   → central Gate
   → Intent → sole MT5Writer → reconciliation
   → ManagedTrade / Trade Manager
→ app/loop.py safe learning/local-backup/presentation maintenance
→ graceful stop releases MT5/controller
→ final verified LOCAL checkpoint only
```

## 14. Deterministic proof map

| Boundary | Minimum proof |
|---|---|
| raw reads | normalization/freshness/completed chronology |
| intelligence | causal evidence/UNKNOWN semantics |
| bounded parallel | one-worker parity/deterministic order |
| strategies/decisions | families, BUY/SELL, Opportunity/timing |
| event geometry | exact causal local extreme + fallback |
| TradePlan/Risk | structural geometry, min lot, policy ceilings |
| session/news | selected frozen composition policy |
| execution | Gate, one-shot Intent, writer/reconcile |
| operator | upstream blocker vs actual Gate |
| controller | lease/epoch/stale-holder block |
| management | monotonic protection/verified close ordering |
| persistence | strict restore/checkpoint/local backup |
| learning | exact close + exactly-once observation |
| research | no-lookahead/cost/holdout/package integrity |

## 15. Placement decision tree

1. Raw broker fact → market_data/domain.
2. Descriptive evidence → intelligence.
3. Family hypothesis/scheduler → strategies.
4. Fusion/Opportunity/timing/TradePlan → decisions.
5. Monetary affordability/risk state → risk.
6. Final broker permission/Intent/writer/reconciliation/controller → execution.
7. Open-trade lifecycle → management.
8. Durable state/checkpoint/local backup → persistence.
9. Runtime composition/provider/DTO → app.
10. Human presentation → operator.
11. Replay/learning/R&D/promotion → research/scripts.

If two locations seem correct, choose one owner and use typed adapters rather than duplicate policy.

## 16. Synchronization rule

Once implementation begins, any added/renamed/removed source/test file or changed proof owner updates this document and `FILE_AND_TEST_CATALOG.md` in the same affected-graph packet.
