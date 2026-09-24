# GoldScalpTrader — Complete File and Test Catalog

**Status:** POST-AUDIT-1 PRE-IMPLEMENTATION CATALOG — PRESERVATION-FIRST CORRECTED
**Version:** 1.2-profiled-risk-parallel-file-test-map
**Authority:** Current repository navigation plus planned source/test proof ownership.

## 1. Current repository reality

The repository still contains a small provisional Python safety scaffold plus the canonical 64-file `Documents/` manual. Planned files below do not claim implementation.

The provisional scaffold must not override preserved reference features/defaults.

## 2. Package/authority map

```text
market_data one read boundary
→ intelligence bounded-parallel analytical work
→ strategies six independent family teams
→ decisions BUY/SELL + Opportunity + completed-M5 timing + TradePlan
→ risk SMALL/MEDIUM/NORMAL profile authority + optional explicit aggressive overlay
→ execution Gate + Intent + sole writer + reconcile
→ management
→ app composition
→ operator read-only presentation

persistence local runtime state/backup
research evidence/learning/proposals only
```

## 3. Foundation/config/domain — planned

`config/settings.py`, `domain/enums.py`, `domain/ids.py`, `domain/market.py`, `domain/models.py`, `diagnostics/logging.py`, `diagnostics/reasons.py`, `diagnostics/health.py`, `security/financial_secrets.py`.

Proof includes mode/profile/aggressive/provider-cache configuration, serialization/identity, market normalization, health/reason and secret-redaction suites.

## 4. Market data/intelligence — planned

`market_data/mt5_reader.py`, `activity.py`, `snapshot.py`; `intelligence/candle_structure.py`, `indicators.py`, `technical.py`, `liquidity.py`, `confluence.py`, `session.py`, `news.py`, `snapshot.py`.

Proof includes one-read normalization, completed chronology, causal knowledge time, scalp timeframe roles, technical/liquidity geometry, News normalization and cache-source lineage.

## 5. Analytical scheduler — preserved feature

`strategies/parallel.py` or equivalent scheduler owns bounded physical concurrency for dependency-independent analytical work.

Required proof:

```text
one-worker run
vs
bounded-parallel run
→ same semantic outputs
→ deterministic canonical ordering
→ immutable inputs
→ no side effects from analytical workers
→ visible worker error/degradation
```

Exact worker count may be tuned; concurrency capability is not removed.

## 6. Session/News provider/cache — planned

Primary owner: `app/session_news.py`.

Responsibilities:

- provider/file resolution;
- bounded acquisition/retry;
- accepted LKG cache creation/loading;
- atomic replacement;
- schema/scope/coverage/TTL/integrity validation;
- preserved 1800-second baseline TTL;
- original timestamp/validity preservation on refresh failure;
- provider health/source diagnostics.

`intelligence/news.py` owns event normalization/tier mapping. `risk/permissions.py` owns CLEAR/BLACKOUT/UNKNOWN permission composition.

Proof includes fresh success, valid-cache fallback, expiry → UNKNOWN, wrong scope/schema, no timestamp laundering and BLACKOUT preservation.

## 7. Strategies/decisions — planned

`strategies/floor.py`, `parallel.py`, `confluence.py`; `decisions/fusion.py`, `snapshot.py`, `opportunity.py`, `timing.py`, `family_trade_plan.py`, `trade_plan.py`.

Proof includes six preserved families, BUY/SELL independence, correlation control, persistent Opportunity/re-arm, completed-M5 timing, family geometry and gross/cost-adjusted TradePlan quality.

## 8. Risk/execution — planned

`risk/engine.py`, `state.py`, `permissions.py`; `execution/models.py`, `checks.py`, `gate.py`, `intent_store.py`, `service.py`, `mt5_writer.py`, `reconcile.py`, `controller.py`, `sqlite_coordination.py`.

Risk proof includes:

- SMALL/MEDIUM/NORMAL DayStartEquity profile resolution;
- exact reference profile bands/daily locks;
- profile fixed through risk day;
- aggressive mode disabled by default;
- explicit sub-$1,000 eligibility/enable path;
- 8% maximum SL-risk ceiling is **not target**;
- 16% aggregate-open-risk and daily-loss ceilings;
- manual reset feature present but disabled by default;
- one fresh same-episode re-entry;
- three-loss / at-least-30-minute cooldown + release conditions;
- min-lot actual risk and no stop rewriting;
- margin/exposure/capacity/UNKNOWN semantics.

Execution proof includes Gate composition, one-shot Intent, sole-writer confinement, action-sensitive CLOSE, controller and reconciliation.

Controlled DEMO writer is implemented/proven before the separately governed future REAL capability.

## 9. Management/persistence — planned

`management/models.py`, `manager.py`, `execution.py`, `store.py`; `persistence/store.py`, `runtime_state.py`, `checkpoint.py`, `backup.py`, `local_recovery_package.py`.

Proof includes HOLD/PROTECT/TRAIL/RUNNER/EXIT, scalp time-efficiency EXIT, no stop widening, broker-valid partial-management handling where divisible, indivisible-volume fallback, exact close proof, typed state integrity, checkpoint/restore and sequential handoff.

No runtime Git publisher is planned.

## 10. App/operator — planned

`app/main.py`, `runtime.py`, `startup.py`, `recovery.py`, `recovery_mt5.py`, `cycle.py`, `loop.py`, `dashboard.py`, `live_presentation.py`, `session_news.py`; operator narrow/wide/fallback/presentation/graphical snapshot modules; optional `graphical_dashboard/*`.

Proof includes mode/startup/recovery, blocker-vs-Gate truth, Risk profile/overlay display, provider/cache truth, read-only isolation and render fallback.

## 11. Research/learning — planned

Research modules cover StrategyMemory, live learning, chronological replay, management/capacity replay, session history, stress, validation/holdout, datasets/acquisition, evidence packages, metrics/outcomes, ablation, episode journal, discovery, invention and promotion.

Proof preserves no-lookahead, costs/latency/duration/min-lot evidence, exactly-once actual learning, candidate semantic lock and no self-promotion.

## 12. Planned scripts

```text
run_walk_forward.py
acquire_mt5_dataset.py
report_demo_learning_evidence.py
restore_runtime_checkpoint.py
create_local_recovery_package.py
create_source_zip.py
scan_financial_secrets.py
verify_documents_manual.py
```

## 13. Preserved session/default proof

Test owner must include:

```text
Daily PRE_CLOSE T-20 / T-10
Weekend PRE_CLOSE T-60 / T-30
Daily reopen 1 clean completed M5
Weekend reopen 2 clean completed M5 + gap assessment
Provider TTL baseline 1800s
```

Connected broker/provider proof separately verifies current factual schedule/provider behaviour.

## 14. Test organization

Tests are organized by contract/authority, not mechanically by source filename. Expected families include market-data/chronology, bounded scheduler parity, intelligence, provider/cache, strategies/fusion, Opportunity/timing, TradePlan/Risk, session/news, execution/controller, persistence/recovery, management, dashboards, learning/research and local backup.

Exact test files enter this catalog only when actually created; planned names are not evidence.

## 15. Audit state

`AUDIT_1_FRESH_DESIGN_REVIEW.md` is corrected by the preservation-first requirement. `DOCUMENTATION_AUDIT.md` remains freeze-preparation work. Audits 2–7 run only when their required implementation/connected evidence exists.

## 16. Synchronization rule

Any source/test addition/removal/rename or proof-owner change updates this catalog, Module Structure, owning contract and affected audit/operator/research/release surfaces in the same coherent packet.