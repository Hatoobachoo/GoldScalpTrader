# GoldScalpTrader — Complete File and Test Catalog

**Status:** DRAFT PRE-IMPLEMENTATION CATALOG — MUST STAY SYNCHRONIZED
**Version:** 0.1-scalp-file-test-map
**Authority:** Exact current repository navigation plus intended source/test proof ownership.

## 1. Purpose

This is the engineering navigation sheet. When a source/script/test file is added, renamed, removed or changes proof ownership, this catalog changes in the same affected-graph packet.

A planned file is not claimed implemented merely because it appears below.

## 2. Current repository reality before implementation

At documentation phase start, the repository contains a small provisional scaffold including:

```text
README.md
.env.example
.gitignore
requirements.txt
bot.py
src/gold_scalp_trader/__init__.py
src/gold_scalp_trader/config.py
tests/test_config.py
Documents/...
```

The scaffold is not the final module architecture. Implementation migration must preserve safe DRY_RUN behaviour while bringing source/test ownership into line with the challenged/frozen manual.

## 3. Intended package/authority map

```text
market_data one read boundary
→ intelligence staged analytical work
→ strategies independent family teams
→ decisions BUY/SELL + Opportunity + timing + TradePlan
→ risk monetary authority
→ execution Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

persistence local state/backup
research evidence/learning/proposals only
```

## 4. Foundation/config/domain — planned

| Planned source | Responsibility | Minimum intended proof |
|---|---|---|
| `config/settings.py` | validated modes/settings | settings/mode boundary tests |
| `domain/enums.py` | stable vocabulary | enum serialization/state tests |
| `domain/ids.py` | typed IDs | identity tests |
| `domain/market.py` | account/symbol/quote/candle/position/deal facts | normalization/validation tests |
| `domain/models.py` | shared typed contracts | model invariants |
| `diagnostics/logging.py` | structured redacted logs | logging/redaction tests |
| `diagnostics/reasons.py` | stable machine reasons | reason mapping tests |
| `diagnostics/health.py` | health snapshot | health/blocker tests |
| `security/financial_secrets.py` | secret detection | scanner positive/negative tests |

## 5. Market data/intelligence — planned

| Planned source | Responsibility | Proof family |
|---|---|---|
| `market_data/mt5_reader.py` | sole MT5 read normalization | data/identity/freshness tests |
| `market_data/activity.py` | bot/external activity + close proof | broker activity/manual tests |
| `market_data/snapshot.py` | immutable snapshot/quality/gaps | market snapshot/gap tests |
| `intelligence/candle_structure.py` | causal swings/BOS/MSS/events | structure/no-lookahead tests |
| `intelligence/indicators.py` | EMA/RSI/ATR/volatility | quant chronology tests |
| `intelligence/technical.py` | zones/location/room | technical geometry tests |
| `intelligence/liquidity.py` | pools/sweeps/FVG/OB | liquidity chronology tests |
| `intelligence/confluence.py` | bounded optional confluence | confluence/ablation boundary tests |
| `intelligence/session.py` | soft session/ranges | DST/session tests |
| `intelligence/news.py` | normalized event facts | event mapping/freshness tests |
| `intelligence/snapshot.py` | staged bounded composition | serial/parallel parity tests |

## 6. Strategies/decisions — planned

| Planned source | Responsibility | Proof family |
|---|---|---|
| `strategies/floor.py` | final approved family hypotheses | family tests |
| `strategies/parallel.py` | bounded scheduler/canonical order | parallel parity tests |
| `strategies/confluence.py` | bounded optional support | confluence boundary tests |
| `decisions/fusion.py` | BUY/SELL + Red Team/Floor Manager | fusion/opposition tests |
| `decisions/snapshot.py` | analytical orchestration | decision integration tests |
| `decisions/opportunity.py` | episode/opportunity lifecycle | lifecycle/re-arm tests |
| `decisions/timing.py` | ENTER/WAIT/MISSED/INVALID | freshness/chase tests |
| `decisions/family_trade_plan.py` | event/retest-specific invalidation | family geometry tests |
| `decisions/trade_plan.py` | structural SL/targets/R/cost-room | plan/risk boundary tests |

## 7. Risk/execution — planned

| Planned source | Responsibility | Proof family |
|---|---|---|
| `risk/engine.py` | monetary sizing/affordability | dynamic lot/min-lot/margin tests |
| `risk/state.py` | risk-day/lock/cooldown/cash-flow | persistence/rollover tests |
| `risk/permissions.py` | market/news/system permission substates | session/news policy tests |
| `execution/models.py` | broker/Intent contracts | model tests |
| `execution/checks.py` | fresh spread/drift/stops/volume checks | execution friction tests |
| `execution/gate.py` | central ALLOW/BLOCK/UNKNOWN | Gate composition tests |
| `execution/intent_store.py` | one-shot Intent lifecycle | idempotency/restart tests |
| `execution/service.py` | governed broker operation | execution integration tests |
| `execution/mt5_writer.py` | sole irreversible call boundary | raw-writer confinement tests |
| `execution/reconcile.py` | broker outcome truth | reconciliation tests |
| `execution/controller.py` | holder/fencing | controller tests |
| `execution/sqlite_coordination.py` | local transactional coordination | coordination tests |

## 8. Management/persistence — planned

| Planned source | Responsibility | Proof family |
|---|---|---|
| `management/models.py` | ManagedTrade models | model/serialization tests |
| `management/manager.py` | HOLD/PROTECT/TRAIL/RUNNER/EXIT | management tests |
| `management/execution.py` | governed modify/close bridge | management execution tests |
| `management/store.py` | ManagedTrade/queue/receipt state | lifecycle persistence tests |
| `persistence/store.py` | typed SQLite StateStore | corruption/schema tests |
| `persistence/runtime_state.py` | coherent runtime bundle | bundle/restart tests |
| `persistence/checkpoint.py` | full checkpoint/restore | checkpoint tests |
| `persistence/backup.py` | local rolling/final backup catalog | backup tests |
| `persistence/local_recovery_package.py` | portable local recovery package | integrity/secret/restore tests |

No `shutdown_publish.py` automatic Git publisher is planned.

## 9. App/operator — planned

| Planned source | Responsibility | Proof family |
|---|---|---|
| `app/main.py` | launcher/modes/safe shutdown | app mode/shutdown tests |
| `app/runtime.py` | dependency composition | startup/runtime tests |
| `app/startup.py` | ordered startup authorities | startup tests |
| `app/recovery.py` | lifecycle recovery | recovery tests |
| `app/recovery_mt5.py` | broker recovery adapter | recovery-MT5 tests |
| `app/cycle.py` | one governed cycle | cycle tests |
| `app/loop.py` | cadence/maintenance/presentation | runtime-loop tests |
| `app/dashboard.py` | base DTO mapping | dashboard tests |
| `app/live_presentation.py` | read-only live enrichment | live-dashboard tests |
| `app/session_news.py` | provider boundary | provider tests |
| `operator/presentation.py` | blocker/Gate truth + wording | operator presentation tests |
| `operator/narrow_dashboard.py` | 64–95 width renderer | width tests |
| `operator/rich_dashboard.py` | wide renderer | dashboard tests |
| `operator/compact_dashboard.py` | safe fallback | fallback tests |
| `operator/live_dashboard.py` | DTO/helpers | presentation tests |
| `operator/graphical_snapshot.py` | atomic browser snapshot | graphical tests |
| `operator/__init__.py` | presentation dispatch | dashboard tests |
| `graphical_dashboard/*` | localhost read-only UI | server/isolation tests |

## 10. Research/learning — planned

| Group | Responsibility | Proof family |
|---|---|---|
| `research/learning.py` | StrategyMemory | idempotency/conflict tests |
| `research/live_learning.py` | verified close → actual observation | live-learning tests |
| `research/replay.py` | chronological replay | no-lookahead tests |
| `research/management_replay.py` | management/capacity replay | replay tests |
| `research/session_history.py` | historical schedule inputs | schedule replay tests |
| `research/stress.py` | spread/slippage/delay stress | stress tests |
| `research/validation.py` | walk-forward/holdout | validation tests |
| `research/datasets.py` | portable verified datasets | manifest/hash tests |
| `research/acquisition.py` | read-only historical acquisition | acquisition tests |
| `research/evidence.py`, `packages.py` | immutable evidence package | integrity tests |
| `research/metrics.py`, `outcomes.py` | R/MAE/MFE/cost/duration metrics | metric tests |
| `research/ablation.py` | marginal optional-feature value | ablation tests |
| `research/episode_journal.py` | labelled research episodes | journal tests |
| `research/discovery.py` | candidate discovery | discovery tests |
| `research/invention.py` | declarative invention | primitive/complexity tests |
| `research/promotion.py` | evidence-bound lifecycle | promotion/holdout tests |

## 11. Planned scripts

```text
run_walk_forward.py
acquire_mt5_dataset.py
report_demo_learning_evidence.py
restore_runtime_checkpoint.py
create_local_recovery_package.py
create_source_git_bundle.py
scan_financial_secrets.py
verify_documents_manual.py
```

Each gets explicit tests or a documented manual proof route.

## 12. Test naming principle

Tests are organized by authority/contract, not by mirroring implementation mechanically.

Expected major suites include market data, chronology, intelligence, strategy/fusion, opportunity/timing, TradePlan/Risk, session/news, execution safety, controller, persistence/recovery, management, dashboards, learning/research and local backup.

Exact test filenames are added to this catalog only when created; planned names do not count as implemented proof.

## 13. Audit documents

`AUDIT_1...AUDIT_7` are audit records/protocols. During pre-implementation stage their status is `NOT RUN`; they must not cite nonexistent test results or source behaviour as verified.

## 14. Synchronization rule

A source/test addition/removal/rename updates:

- this catalog;
- `MODULE_STRUCTURE.md` if ownership changes;
- canonical behaviour owner;
- relevant audit/release/test docs;
- operator/research/persistence consequences.

Completion is an affected-graph property, not a local file-edit property.
