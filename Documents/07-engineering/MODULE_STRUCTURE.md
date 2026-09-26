# GoldScalpTrader — Module Structure and File Map

**Status:** IMPLEMENTED ARCHITECTURE MAP — CONNECTED DEMO CERTIFICATION IN PROGRESS
**Version:** 2.5-institutional-scalp-implementation
**Authority:** Actual package/file ownership, dependency direction, setup-detection/isolation boundaries, durable Risk-day authority, typed session/News provider separation, exactly-once learning, serial financial authority, connected evidence observation and research/presentation separation.

## 1. Dependency direction

```mermaid
flowchart TB
    BASE["config / domain / diagnostics / security"] --> DATA["market_data"]
    DATA --> INTEL["intelligence"]
    INTEL --> STRAT["strategies: setup detection + six families + isolation"]
    STRAT --> DEC["decisions: active BUY/SELL, Opportunity, M1 timing, TradePlan, executable quality"]
    DEC --> RISK["risk"]
    RISK --> EXEC["execution"]
    EXEC --> MGMT["management"]
    MGMT --> APP["app composition"]
    APP --> OP["operator / graphical dashboard"]

    DATA --> RESEARCH["research"]
    INTEL --> RESEARCH
    STRAT --> RESEARCH
    DEC --> RESEARCH
    MGMT --> RESEARCH

    PERSIST["persistence"] -. "durable context" .-> APP
    PERSIST -.-> RISK
    PERSIST -.-> EXEC
    PERSIST -.-> MGMT
    PERSIST -.-> RESEARCH
    APP -. "read-only certification observations" .-> DIAG["diagnostics"]
```

Broker/financial authority remains serial even if analytical work is physically parallelized after profiling.

## 2. Package authority table

| Package | Owns | Must never own |
|---|---|---|
| `config` | validated settings/policy identities | hidden live policy mutation |
| `domain` | enums, typed IDs/DTOs, units/states | MT5 calls |
| `diagnostics` | structured logs, reason/health models, metrics, read-only accumulated connected-DEMO evidence summaries | trading authority |
| `security` | secret detection/redaction | secret storage |
| `market_data` | sole normalized analytical/recovery MT5 read boundary, account-mode verification and activity normalization | raw irreversible writes |
| `intelligence` | causal descriptive structure/technical/liquidity/quant/session/News context | money/Gate |
| `strategies` | six family definitions, market-first setup detection, Strategy Isolation, analytical scheduler | Risk/broker writes |
| `decisions` | active-family BUY/SELL/Red Team, Opportunity, M1 timing, TradePlan, executable quality | raw MT5 write |
| `risk` | preserved profiles, monetary sizing, durable UTC risk-day/account-safety state, cooldown/re-entry/capacity | strategy rewrite or broker write |
| `execution` | Gate, controller, Intent, checks, sole writer, reconciliation | strategy invention |
| `management` | ManagedTrade, close-proof lineage and HOLD/PROTECT/TRAIL/RUNNER/EXIT decisions | raw writer |
| `persistence` | strict local state/checkpoints/recovery packages | current broker truth |
| `app` | startup/recovery/runtime composition/cadence/DTO assembly, typed session/News provider boundary, guarded DEMO runners | duplicate policy ownership |
| `operator` | read-only terminal/graphical view models/renderers | authority recomputation |
| `graphical_dashboard` | approved one-screen interactive local UI | trading mutation |
| `research` | replay, exactly-once actual learning, discovery, invention, ML, promotion evidence | production broker authority |

## 3. Implemented package tree

```text
src/gold_scalp_trader/
├── config/
│   └── settings.py
├── domain/
│   ├── enums.py
│   ├── ids.py
│   ├── market.py
│   └── models.py
├── diagnostics/
│   ├── logging.py
│   ├── reasons.py
│   ├── health.py
│   ├── metrics.py
│   └── connected_demo.py
├── security/
│   └── financial_secrets.py
├── market_data/
│   ├── account_mode.py
│   ├── mt5_reader.py
│   ├── activity.py
│   └── snapshot.py
├── intelligence/
│   ├── candle_structure.py
│   ├── indicators.py
│   ├── technical.py
│   ├── liquidity.py
│   ├── confluence.py
│   ├── session.py
│   ├── news.py
│   └── snapshot.py
├── strategies/
│   ├── floor.py
│   ├── setup_detector.py
│   ├── isolation.py
│   ├── scheduler.py
│   └── confluence.py
├── decisions/
│   ├── fusion.py
│   ├── snapshot.py
│   ├── opportunity.py
│   ├── timing.py
│   ├── family_trade_plan.py
│   ├── trade_plan.py
│   └── executable_quality.py
├── risk/
│   ├── engine.py
│   ├── state.py
│   ├── runtime.py
│   └── permissions.py
├── execution/
│   ├── models.py
│   ├── checks.py
│   ├── gate.py
│   ├── intent_store.py
│   ├── service.py
│   ├── mt5_writer.py
│   ├── reconcile.py
│   ├── controller.py
│   └── sqlite_coordination.py
├── management/
│   ├── models.py
│   ├── manager.py
│   ├── execution.py
│   ├── closure.py
│   └── store.py
├── persistence/
│   ├── store.py
│   ├── runtime_state.py
│   ├── checkpoint.py
│   ├── backup.py
│   └── local_recovery_package.py
├── research/
│   ├── learning.py
│   ├── live_learning.py
│   ├── replay.py
│   ├── management_replay.py
│   ├── session_history.py
│   ├── stress.py
│   ├── validation.py
│   ├── datasets.py
│   ├── acquisition.py
│   ├── evidence.py
│   ├── packages.py
│   ├── metrics.py
│   ├── outcomes.py
│   ├── ablation.py
│   ├── episode_journal.py
│   ├── discovery.py
│   ├── invention.py
│   ├── models.py
│   └── promotion.py
├── operator/
│   ├── presentation.py
│   ├── terminal_dashboard.py
│   ├── graphical_snapshot.py
│   └── __init__.py
└── app/
    ├── main.py
    ├── runtime.py
    ├── startup.py
    ├── recovery.py
    ├── recovery_mt5.py
    ├── cycle.py
    ├── loop.py
    ├── dashboard.py
    ├── live_presentation.py
    ├── session_news.py
    ├── demo_runner.py
    └── graphical_demo_runner.py

graphical_dashboard/
├── ui.py
├── chart.py
├── controls.py
├── server.py
└── __main__.py
```

Physical files may be refactored only when ownership remains identical and this map plus the file/test catalog are synchronized in the same change packet.

## 4. Setup Detector ownership

`strategies/setup_detector.py` answers:

```text
Given one causal IntelligenceSnapshot,
which strategy-family setup(s) genuinely qualify now?
```

It may return `NONE`, one qualified setup or multiple independently qualified setup candidates. It cannot force the active family onto the chart, create monetary Risk/broker permission, or silently switch the production family.

`strategies/isolation.py` applies the current policy:

```text
qualified candidate belongs to ACTIVE_EXECUTION family
→ eligible for live decision path

qualified candidate belongs only to SHADOW_ONLY family
→ research/shadow record; live WAIT
```

## 5. Analytical scheduler

`strategies/scheduler.py` owns physical scheduling only.

```text
shared precomputation
→ vectorization/cache
→ serial deterministic baseline
→ profiling
→ bounded parallel execution only where critical path improves
```

Immutable inputs, bounded resources, deterministic ordering, visible worker errors, no broker/lifecycle side effects and one-worker/parallel semantic parity are mandatory.

## 6. Data/timeframe ownership

`market_data` reads H4 optional, H1, M15, M5, bounded M1 and quote/tick through one normalized boundary. `market_data/account_mode.py` proves connected DEMO mode before any write-capable path proceeds.

`market_data/mt5_reader.py` also owns normalized account-wide/position-scoped deal history and whole-account position reads used by recovery/Risk accounting. Unavailable history/positions remain UNKNOWN rather than zero.

M1 is production-relevant only as subordinate timing after a valid M5 Opportunity; it cannot independently create a setup.

## 7. Decision ownership

```text
strategies/setup_detector.py → family setup classification
strategies/isolation.py      → live-active vs shadow eligibility
decisions/fusion.py          → active-family BUY/SELL + Red Team only
decisions/opportunity.py     → persistent M5 Opportunity/Episode
decisions/timing.py          → subordinate M1 READY/WAIT/MISSED/INVALID
decisions/trade_plan.py + family_trade_plan.py → structural geometry
decisions/executable_quality.py → fresh spread/cost/drift/latency economics
```

These owners remain distinct in behavior even if implementation refactors file placement.

## 8. Risk ownership

`risk/engine.py` owns preserved profiles/bands, broker-aware volume/min-lot actual risk, margin/aggregate-capacity risk and the disabled-by-default aggressive 8%/16% overlay.

`risk/state.py` owns strict durable serialization for fixed UTC risk-day identity/DayStartEquity/profile, Account Safety P/L, daily lock/reset, consecutive-loss streak, cooldown and same-episode re-entry state.

`risk/runtime.py` is a **read/accounting authority component with no broker-write capability**. It bootstraps a UTC day only from verified account-wide history while flat/reconciled, loads the persisted profile on restart, separates identifiable non-trading cash flow, consumes exact verified close receipts idempotently, and returns typed PASS/BLOCK/UNKNOWN for new exposure.

`risk/permissions.py` composes Risk-related hard facts. News context is not a hard permission input.

## 9. Session / News provider ownership

`app/session_news.py` implements the typed provider boundary defined by the frozen provider contract.

It supports a bounded, schema-versioned, exact-scope local provider snapshot with:

- account/server/symbol scope validation;
- timezone-aware observation and validity timestamps;
- verified `OPEN / PRE_CLOSE / CLOSED / REOPEN_WARMUP / UNKNOWN` market state;
- explicit schedule verification/tradeability/provenance;
- reopen/gap/execution-normalization fields;
- News provider health/events with the preserved 1800-second freshness baseline when invoked with project settings.

Critical separation:

```text
expired/unverified/mismatched Session facts → hard Session UNKNOWN
missing/stale News context                 → soft News health only
```

The provider module performs no broker write and does not infer hard session permission from News.

## 10. Execution ownership

Only `execution/mt5_writer.py` may perform raw irreversible broker operations.

All OPEN/MODIFY/CLOSE paths use:

```text
Gate → durable Intent → fresh checks/order_check → SUBMITTING
→ one writer call → acknowledgement classification → reconciliation
```

No blind retry after ambiguous broker acknowledgement.

## 11. Management ownership

`management/manager.py` decides `HOLD / PROTECT / TRAIL / RUNNER / EXIT`. `management/execution.py` turns approved actions into the governed Intent path.

`management/closure.py` owns exact known-trade close proof/archival handoff. Its durable receipt includes verified close monetary result for restart-safe Risk streak/cooldown accounting; unknown external Gold is never adopted.

## 12. Persistence / recovery

`persistence/store.py` is strict durable context, not broker truth. `persistence/checkpoint.py` exports consistent state. `app/recovery.py` reconciles restored local context against current MT5 truth before trading resumes. No runtime Git publication module exists.

## 13. Research / learning ownership

`research/live_learning.py` owns the durable verified-close learning queue and exactly-once processing into `research/learning.py` StrategyMemory.

Ordering is:

```text
verified close queue item
→ validate immutable source identity
→ durable StrategyMemory observation
→ consume queue item only after durable save
```

Missing `realized_r`, Entry Efficiency or Capture Efficiency are preserved as UNKNOWN/`None`; they are never fabricated from incomplete close evidence. The observation preserves actual family/policy, net money, close origin, ticket/symbol and open/close timestamps when known.

Replay/discovery/invention/ML/promotion remain downstream. `research/promotion.py` stops at `APPROVAL_REQUIRED` before production promotion.

## 14. Application / DEMO runner ownership

`app/demo_runner.py` and `app/graphical_demo_runner.py` compose the governed DEMO runtime only. They preserve explicit DEMO account proof, persistent StateStore, fixed cadence, governed cycle/management lifecycle and local checkpoint on safe shutdown.

The graphical runner supplies immutable/read-only snapshots to the GUI. Chart buttons cannot trigger broker cycles or writes.

## 15. Graphical dashboard ownership

Approved Swing-style Scalp graphical dashboard is local and presentation-only. `graphical_dashboard/chart.py` owns chart interactions; `controls.py` owns M1/M5/M15/H1/H4, Indicators, Drawings and Settings; `operator/graphical_snapshot.py` supplies atomic read-only DTOs. No dashboard module recalculates or mutates authority.

## 16. Connected DEMO evidence ownership

`diagnostics/connected_demo.py` aggregates already-captured read-only connected-DEMO reports. `scripts/certify_connected_demo.py` captures one read-only observation and `scripts/monitor_connected_demo.py` accumulates them at a bounded interval while the governed bot may trade.

They write only ignored local evidence files; they never mutate broker state, source control, production policy or REAL enablement. Missing manual/restart/handoff/schedule/distribution drills remain explicitly PENDING.

## 17. Implemented scripts

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_zip.py
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
scripts/verify_contract_sync.py
scripts/verify_offline_release.py
```

The connected certification/monitor scripts are read-only. `verify_contract_sync.py` statically enforces selected high-value frozen-document invariants and does not replace connected proof.

## 18. Forbidden dependency directions

```text
intelligence/strategy worker → MT5Writer                    NO
setup detector → Risk/Gate                                 NO
shadow family → live Intent                                NO
M1 alone → production Opportunity                          NO
dashboard → authority mutation/recalculation               NO
research/ML → live production mutation                     NO
unknown position/history → zero                            NO
ambiguous broker acknowledgement → blind retry             NO
Risk → tighten structural SL to fit volume                 NO
Risk runtime/accounting authority → broker write            NO
Session/News provider → broker write                       NO
News provider failure → hard trading kill switch           NO
trading runtime → Git commit/push/pull                     NO
backup package → credentials                               NO
connected certification/monitor tool → broker write        NO
connected certification/monitor tool → REAL enablement     NO
```

## 19. Source-map synchronization

Any source/test rename, ownership change or new material script/package updates this file, `FILE_AND_TEST_CATALOG.md`, the owning behavioral contract when behavior changes, affected tests/audits/operator docs and final release traceability.

The local offline release verifier must fail when a covered high-value frozen contract and source tree drift.
