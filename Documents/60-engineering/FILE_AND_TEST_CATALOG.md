# GoldScalpTrader — Complete File and Test Catalog

**Status:** POST-AUDIT-1 PRE-IMPLEMENTATION CATALOG — MUST STAY SYNCHRONIZED
**Version:** 1.0-scalp-file-test-map
**Authority:** Current repository navigation plus planned source/test proof ownership.

## 1. Current repository reality

The repository still contains a small provisional Python safety scaffold plus the canonical 64-file `Documents/` manual. Planned files below do not claim implementation.

Implementation must migrate safely from scaffold to the frozen architecture rather than treating existing `bot.py/config.py` layout as final.

## 2. Package/authority map

```text
market_data one read boundary
→ intelligence logically independent analytical work
→ strategies six independent family teams
→ decisions BUY/SELL + Opportunity + completed-M5 timing + TradePlan
→ risk STANDARD monetary authority
→ execution Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

persistence local runtime state/backup
research evidence/learning/proposals only
```

## 3. Foundation/config/domain — planned

`config/settings.py`, `domain/enums.py`, `domain/ids.py`, `domain/market.py`, `domain/models.py`, `diagnostics/logging.py`, `diagnostics/reasons.py`, `diagnostics/health.py`, `security/financial_secrets.py`.

Proof: settings/mode, serialization/identity, market normalization, health/reason and secret-redaction suites.

## 4. Market data/intelligence — planned

`market_data/mt5_reader.py`, `activity.py`, `snapshot.py`; `intelligence/candle_structure.py`, `indicators.py`, `technical.py`, `liquidity.py`, `confluence.py`, `session.py`, `news.py`, `snapshot.py`.

Proof includes one-read normalization, completed chronology, causal knowledge time, H1/M15/M5 roles, M1 non-authority, technical/liquidity geometry, News normalization and scheduler parity if concurrency exists.

## 5. Strategies/decisions — planned

`strategies/floor.py`, `parallel.py`, `confluence.py`; `decisions/fusion.py`, `snapshot.py`, `opportunity.py`, `timing.py`, `family_trade_plan.py`, `trade_plan.py`.

Proof includes six frozen families, BUY/SELL independence, correlation control, persistent Opportunity/re-arm, completed-M5 timing, family geometry and gross/cost-adjusted TradePlan quality.

## 6. Risk/execution — planned

`risk/engine.py`, `state.py`, `permissions.py`; `execution/models.py`, `checks.py`, `gate.py`, `intent_store.py`, `service.py`, `mt5_writer.py`, `reconcile.py`, `controller.py`, `sqlite_coordination.py`.

Proof includes STANDARD policy sizing/min-lot, daily state, News CLEAR/BLACKOUT/UNKNOWN matrix, Gate composition, one-shot Intent, sole-writer confinement, action-sensitive CLOSE, controller and reconciliation.

`mt5_writer.py` irreversible capability is a later controlled-DEMO milestone only. REAL is outside V1.

## 7. Management/persistence — planned

`management/models.py`, `manager.py`, `execution.py`, `store.py`; `persistence/store.py`, `runtime_state.py`, `checkpoint.py`, `backup.py`, `local_recovery_package.py`.

Proof includes HOLD/PROTECT/TRAIL/RUNNER/EXIT, time-efficiency EXIT reason, no stop widening, exact close proof, typed state integrity, checkpoint/restore, local backup and sequential handoff.

No `shutdown_publish.py` runtime Git publisher is planned.

## 8. App/operator — planned

`app/main.py`, `runtime.py`, `startup.py`, `recovery.py`, `recovery_mt5.py`, `cycle.py`, `loop.py`, `dashboard.py`, `live_presentation.py`, `session_news.py`; operator narrow/wide/fallback/presentation/graphical snapshot modules; optional `graphical_dashboard/*`.

Proof includes mode/startup/recovery, blocker-vs-Gate truth, dashboard read-only isolation and render fallback.

## 9. Research/learning — planned

Research modules cover StrategyMemory, live learning, chronological replay, management/capacity replay, session history, stress, validation/holdout, datasets/acquisition, evidence packages, metrics/outcomes, ablation, episode journal, discovery, invention and promotion.

Proof preserves no-lookahead, costs/latency/duration/min-lot evidence, exactly-once actual learning, candidate semantic lock and no self-promotion.

## 10. Planned scripts

```text
run_walk_forward.py
acquire_mt5_dataset.py
report_demo_learning_evidence.py
restore_runtime_checkpoint.py
create_local_recovery_package.py
create_source_zip.py              # optional operator development backup helper
scan_financial_secrets.py
verify_documents_manual.py
```

A Git bundle helper is optional advanced/manual tooling and is not required by the normal source backup workflow.

## 11. Test organization

Tests are organized by contract/authority, not mechanically by source filename. Expected families include market-data/chronology, intelligence, strategies/fusion, Opportunity/timing, TradePlan/Risk, session/news, execution/controller, persistence/recovery, management, dashboards, learning/research and local backup.

Exact test files enter this catalog only when actually created; planned names are not evidence.

## 12. Audit state

`AUDIT_1_FRESH_DESIGN_REVIEW.md` is complete as an architecture audit. Audits 2–7 are not pre-filled PASS records; they run only when their required implementation/connected evidence exists.

## 13. Synchronization rule

Any source/test addition/removal/rename or proof-owner change updates this catalog, Module Structure, owning contract and affected audit/operator/research/release surfaces in the same coherent packet.