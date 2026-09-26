# GoldScalpTrader — Complete File and Test Catalog

**Status:** IMPLEMENTED FILE/TEST MAP — OFFLINE CONTRACT SYNC ENFORCED / CONNECTED DEMO CERTIFICATION IN PROGRESS
**Version:** 2.5-institutional-scalp-implementation
**Authority:** Actual source ownership, actual deterministic/integration proof, remaining connected proof and implementation/document synchronization.

## 1. Current repository reality

The repository implements the documented architecture through guarded DEMO runtime components, ManagedTrade lifecycle, durable Risk/state components, governed research/learning tooling, read-only connected evidence tooling and the approved graphical dashboard.

Evidence classes remain separate:

```text
source exists
≠ deterministic test proof
≠ offline integration proof
≠ connected Exness DEMO proof
≠ future REAL release proof
```

`Documents/` remains the behavioral source of truth. Code and tests conform to it.

## 2. Source ownership summary

```text
config/domain/diagnostics/security
→ market_data
→ intelligence
→ strategies: setup detector + six families + isolation + scheduler
→ decisions: active-family debate + Opportunity + M1 timing + TradePlan + executable quality
→ risk: sizing + durable UTC-day authority
→ execution
→ management
→ app/operator

persistence = durable local context/recovery
research = verified-close learning + replay/discovery/invention/ML/promotion
graphical_dashboard = read-only local presentation
diagnostics connected-demo = read-only Phase-15 evidence aggregation
```

## 3. Foundation/config/domain/diagnostics

Source:

```text
src/gold_scalp_trader/config/settings.py
src/gold_scalp_trader/domain/enums.py
src/gold_scalp_trader/domain/ids.py
src/gold_scalp_trader/domain/market.py
src/gold_scalp_trader/domain/models.py
src/gold_scalp_trader/diagnostics/logging.py
src/gold_scalp_trader/diagnostics/reasons.py
src/gold_scalp_trader/diagnostics/health.py
src/gold_scalp_trader/diagnostics/metrics.py
src/gold_scalp_trader/diagnostics/connected_demo.py
src/gold_scalp_trader/security/financial_secrets.py
```

Proof includes:

```text
tests/test_settings.py
tests/test_config.py
tests/test_market_domain.py
tests/test_connected_demo_evidence.py
scripts/scan_financial_secrets.py
scripts/verify_contract_sync.py
```

The contract-sync verifier checks exact preserved Risk bands, disabled-by-default aggressive/manual-reset policy, `REAL_RELEASE_ENABLED = False`, canonical source/test ownership and selected no-broker boundaries.

## 4. Market-data layer

Source:

```text
market_data/account_mode.py
market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py
```

Proof:

```text
tests/test_mt5_reader.py
tests/test_deal_history_reader.py
tests/test_activity_accounting.py
tests/test_market_domain.py
tests/test_risk_runtime_state.py
```

Required semantics:

- one normalized analytical/recovery MT5 boundary;
- completed H1/M15/M5 and bounded M1 chronology;
- optional H4;
- Bid/Ask/source/capture timestamps;
- future-clock/stale/corrupt detection;
- `[]` vs `None` exposure semantics;
- symbol/spec normalization;
- account-wide and position-scoped deal-history normalization;
- whole-account flatness read preserving UNKNOWN rather than inventing zero;
- no raw write authority;
- connected DEMO account must positively report DEMO before writes.

Real Exness SymbolSpec, filling modes, schedule and timing remain Phase-15 evidence.

## 5. Intelligence layer

Source:

```text
intelligence/candle_structure.py
intelligence/indicators.py
intelligence/technical.py
intelligence/liquidity.py
intelligence/confluence.py
intelligence/session.py
intelligence/news.py
intelligence/snapshot.py
```

Proof includes:

```text
tests/test_indicators_structure.py
tests/test_confluence.py
tests/test_news_context.py
tests/test_decision_pipeline.py
```

Frozen behavior: completed/causal structure, optional-evidence neutrality, M1 subordinate to valid M5 Opportunity, News soft-only and no broker authority.

## 6. Setup Detector / Strategy Isolation / six families

Source:

```text
strategies/floor.py
strategies/setup_detector.py
strategies/isolation.py
strategies/scheduler.py
strategies/confluence.py
```

Proof:

```text
tests/test_strategy_isolation.py
tests/test_cycle_no_forcing.py
tests/test_decision_pipeline.py
scripts/verify_contract_sync.py
```

Critical invariant:

```text
active family = Breakout Retest
market setup = Liquidity Sweep only
→ no fabricated Breakout Retest setup
→ live WAIT
→ Liquidity Sweep remains shadow/research evidence
```

No family setup → no production Opportunity.

## 7. Active-family decision / Opportunity / timing

Source:

```text
decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
```

Proof:

```text
tests/test_decision_pipeline.py
tests/test_cycle_no_forcing.py
tests/test_strategy_isolation.py
```

Coverage includes independent active-family BUY/SELL evidence, Red-Team challenge, persistent M5 Opportunity, subordinate M1 timing, freshness/chase/drift and no M1-only production setup.

## 8. TradePlan / executable quality

Source:

```text
decisions/family_trade_plan.py
decisions/trade_plan.py
decisions/executable_quality.py
```

Proof:

```text
tests/test_executable_quality.py
tests/test_decision_pipeline.py
```

Must preserve family-correct structural invalidation, no fabricated `entry ± ATR` plan geometry, ATR only as a structural/noise buffer, no SL rewrite to fit Risk, no inherited fixed Swing 1.20R hard dependency, gross R distinct from current costs and fixed+aware execution-quality dimensions.

## 9. Risk

Source:

```text
risk/engine.py
risk/state.py
risk/runtime.py
risk/permissions.py
```

Proof:

```text
tests/test_risk_profiles.py
tests/test_risk_state.py
tests/test_risk_runtime_state.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

`risk/runtime.py` is read/accounting authority only. Deterministic proof covers fixed UTC risk-day profile persistence, strict SQLite round-trip, DayStartEquity reconstruction from verified flat-account history, identifiable non-trading cash-flow separation, fail-closed bootstrap, persisted daily loss lock, idempotent verified-close loss-streak/cooldown accounting and true-breakeven handling.

Preserved regression values:

```text
SMALL  3.0–4.5 / >4.5–6.5 / hard 7 / daily 12
MEDIUM 2.0–3.0 / >3.0–4.5 / hard 5 / daily 9
NORMAL 1.0–2.0 / >2.0–3.5 / hard 4 / daily 7
Aggressive disabled default; 8% single ceiling / 16% aggregate/day
3 losses → at least 30m cooldown
max independent Gold positions = 1
```

## 10. Session / News provider

Source:

```text
app/session_news.py
intelligence/session.py
intelligence/news.py
risk/permissions.py
```

Proof:

```text
tests/test_news_context.py
tests/test_session_news_provider.py
tests/test_guarded_demo_runtime.py
```

`app/session_news.py` now implements the frozen typed provider boundary with schema/version validation, exact account/server/symbol scope, timezone-aware observation/validity timestamps and explicit market states.

Deterministic proof covers:

```text
verified valid Session OPEN → session can report hard OPEN
PRE_CLOSE                  → never new-entry-allowed
expired/unverified Session → UNKNOWN
scope mismatch              → reject
News missing/stale          → soft UNAVAILABLE/STALE only
News health                 → never a hard-trading permission
```

The preserved 1800-second News-context freshness baseline is supported by the loader. Current Exness schedule correctness remains Phase-15 external proof.

## 11. Execution / controller / reconciliation

Source:

```text
execution/models.py
execution/checks.py
execution/gate.py
execution/intent_store.py
execution/service.py
execution/mt5_writer.py
execution/reconcile.py
execution/controller.py
execution/sqlite_coordination.py
```

Proof:

```text
tests/test_execution_intent.py
tests/test_gate.py
tests/test_controller.py
tests/test_action_reconciliation.py
tests/test_writer_attribution.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

Persist-before-send, one send per Intent, no blind retry, action-sensitive reconciliation, sole writer and controller fencing remain mandatory.

## 12. Management / close proof

Source:

```text
management/models.py
management/manager.py
management/execution.py
management/closure.py
management/store.py
```

Proof:

```text
tests/test_managed_trade_store.py
tests/test_management_lifecycle.py
tests/test_action_reconciliation.py
tests/test_deal_history_reader.py
tests/test_risk_runtime_state.py
```

`management/closure.py` owns exact broker/manual close proof and immutable closure receipt. The receipt preserves verified net monetary result used by restart-safe Risk streak/cooldown accounting. Unknown/manual Gold exposure is never adopted.

## 13. Persistence / recovery

Source:

```text
persistence/store.py
persistence/runtime_state.py
persistence/checkpoint.py
persistence/backup.py
persistence/local_recovery_package.py
app/recovery.py
app/recovery_mt5.py
```

Proof:

```text
tests/test_state_store.py
tests/test_checkpoint.py
tests/test_full_checkpoint.py
tests/test_recovery_package.py
tests/test_risk_runtime_state.py
```

Fresh-machine + connected MT5 reconciliation/handoff remains Phase-15 external proof.

## 14. Application runtime / DEMO launcher

Source:

```text
app/main.py
app/runtime.py
app/startup.py
app/cycle.py
app/loop.py
app/demo_runner.py
app/graphical_demo_runner.py
app/dashboard.py
app/live_presentation.py
```

Proof:

```text
tests/test_demo_launcher.py
tests/test_guarded_demo_runtime.py
tests/test_graphical_runtime.py
```

Write-capable DEMO behavior requires explicit DEMO confirmation and positive MT5 DEMO account proof. REAL remains hard-disabled. Read/accounting authorities remain separate from raw broker-write ownership.

## 15. Operator / graphical dashboard

Source:

```text
operator/presentation.py
operator/terminal_dashboard.py
operator/graphical_snapshot.py
graphical_dashboard/ui.py
graphical_dashboard/chart.py
graphical_dashboard/controls.py
graphical_dashboard/server.py
graphical_dashboard/__main__.py
```

Proof:

```text
tests/test_dashboard_controls.py
tests/test_graphical_runtime.py
```

Approved GUI remains one-screen/no-scroll. Chart controls are presentation-only and cannot trigger a broker cycle/write.

## 16. Research / learning / ML

Source:

```text
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
research/models.py
research/promotion.py
```

Proof:

```text
tests/test_live_learning_pipeline.py
tests/test_research_governance.py
tests/test_research_integrity.py
scripts/report_demo_learning_evidence.py
scripts/run_walk_forward.py
```

`research/live_learning.py` now provides exactly-once queue processing:

```text
verified full-close queue item
→ validate immutable source identity
→ save StrategyMemory observation with allow_replace=False
→ consume queue only after durable save
```

Tests prove identical successful processing is idempotent, a conflicting existing observation leaves the queue intact, incomplete evidence remains pending, and missing realized-R/entry/capture metrics are not fabricated.

The broader research toolkit retains causal replay, one-position production-capacity replay, actual/shadow separation, opportunity/efficiency metrics, stress, walk-forward/holdout, ablation and immutable evidence packages. Candidate production promotion stops at `APPROVAL_REQUIRED`.

## 17. Connected DEMO evidence / Phase 15

Source/tooling:

```text
src/gold_scalp_trader/diagnostics/connected_demo.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
tests/test_connected_demo_evidence.py
```

The collector/monitor are read-only, scope-bound and conservative. Verified OPEN/MODIFY/CLOSE/learning evidence can accumulate once observed; current unresolved-Intent status uses the latest sample; scope mismatch or certification-tool broker-write/REAL claims reject the evidence set; missing manual/restart/handoff/schedule/distribution drills stay PENDING.

## 18. Implemented scripts

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

`report_demo_learning_evidence.py` is read-only. `verify_contract_sync.py` fails offline release when covered high-value frozen-document invariants drift.

## 19. Integration test families represented

```text
market-first setup / no strategy forcing
strategy isolation
M5→M1 decision pipeline
executable quality
Risk policy/state + durable UTC risk-day accounting
Session/News provider authority separation
one-shot Intent / Gate / controller
guarded DEMO runtime
ManagedTrade lifecycle
OPEN/MODIFY/CLOSE reconciliation
broker deal-history close proof
exactly-once verified-close StrategyMemory ingestion
StateStore/checkpoint/recovery package
graphical runtime/chart controls
research no-lookahead/capacity/metrics/governance/integrity
connected DEMO evidence accumulation safety
```

## 20. Connected DEMO proof — still external

Offline code/tests cannot prove actual Exness SymbolSpec, real schedule/DST/holiday facts, filling/order modes, actual spread/slippage/deviation distributions, real latency, live OPEN/MODIFY/CLOSE lifecycle, manual known-trade close visibility, restart during real active lifecycle or fresh-machine MT5 recovery/handoff.

The read-only connected collector/monitor records facts that can be observed without manufacturing broker events. These remain Phase-15 requirements until actually observed.

## 21. Synchronization rule

Every material source/test/script addition, removal, rename or ownership change updates this catalog, `MODULE_STRUCTURE.md`, the owning behavioral contract when behavior changes and release/audit status when evidence changes.

Offline release sequence:

```text
verify_documents_manual.py
→ verify_contract_sync.py
→ financial-secret scan
→ pytest
```

A green offline result does not claim connected DEMO certification.
