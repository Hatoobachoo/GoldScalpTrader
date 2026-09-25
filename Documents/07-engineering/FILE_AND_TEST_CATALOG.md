# GoldScalpTrader — Complete File and Test Catalog

**Status:** IMPLEMENTED FILE/TEST MAP — OFFLINE CONTRACT SYNC ENFORCED / CONNECTED DEMO PROOF PENDING
**Version:** 2.1-institutional-scalp-implementation
**Authority:** Actual source ownership, actual deterministic/integration proof, remaining connected proof and implementation/document synchronization.

## 1. Current repository reality

The repository is no longer a provisional scaffold. The documented architecture is implemented through the live guarded DEMO runtime, managed-trade lifecycle and approved graphical dashboard.

Current evidence classes must remain separate:

```text
source exists
≠ deterministic test proof
≠ offline integration proof
≠ connected Exness DEMO proof
≠ future REAL release proof
```

`Documents/` remains the source of truth for behavior. Code and tests must conform to it.

## 2. Source ownership summary

```text
config/domain/diagnostics/security
→ market_data
→ intelligence
→ strategies: setup detector + six families + isolation + scheduler
→ decisions: active-family debate + Opportunity + M1 timing + TradePlan + executable quality
→ risk
→ execution
→ management
→ app/operator

persistence = durable local context/recovery
research = downstream replay/learning/discovery/invention/ML/promotion
graphical_dashboard = read-only local presentation
```

## 3. Foundation/config/domain — implemented source

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
src/gold_scalp_trader/security/financial_secrets.py
```

Current proof includes:

```text
tests/test_settings.py
tests/test_config.py
tests/test_market_domain.py
scripts/scan_financial_secrets.py
scripts/verify_contract_sync.py
```

The contract-sync verifier additionally checks exact preserved Risk bands, disabled-by-default aggressive/manual-reset policy and `REAL_RELEASE_ENABLED = False`.

## 4. Market-data layer

Source:

```text
market_data/account_mode.py
market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py
```

Current tests:

```text
tests/test_mt5_reader.py
tests/test_deal_history_reader.py
tests/test_activity_accounting.py
tests/test_market_domain.py
```

Required semantics remain:

- one normalized analytical MT5 boundary;
- completed H1/M15/M5 and bounded M1 chronology;
- optional H4;
- Bid/Ask/source/capture timestamps;
- future-clock/stale/corrupt detection;
- `[]` vs `None` exposure semantics;
- symbol/spec normalization;
- no raw write authority;
- connected DEMO account must positively report DEMO before writes.

Real Exness SymbolSpec, filling modes, schedule and timing remain Phase 15 evidence.

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

Current tests include:

```text
tests/test_indicators_structure.py
tests/test_confluence.py
tests/test_news_context.py
tests/test_decision_pipeline.py
```

Required frozen behavior:

- completed/casual structure;
- optional evidence neutrality;
- M1 subordinate to valid M5 Opportunity;
- News context soft-only;
- no broker authority.

Future test-depth additions may split current combined tests into finer files, but test-file naming is not behavioral authority.

## 6. Setup Detector / Strategy Isolation / six families

Source:

```text
strategies/floor.py
strategies/setup_detector.py
strategies/isolation.py
strategies/scheduler.py
strategies/confluence.py
```

Current proof:

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

And:

```text
market forms no family setup
→ Setup Detector = NONE
→ no production Opportunity
```

## 7. Active-family decision / Opportunity / timing

Source:

```text
decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
```

Current integrated proof:

```text
tests/test_decision_pipeline.py
tests/test_cycle_no_forcing.py
tests/test_strategy_isolation.py
```

Required coverage includes active-family BUY/SELL independence, Red-Team challenge, persistent M5 Opportunity, subordinate M1 timing, freshness/chase/drift and no M1-only production setup.

## 8. TradePlan / executable quality

Source:

```text
decisions/family_trade_plan.py
decisions/trade_plan.py
decisions/executable_quality.py
```

Current proof:

```text
tests/test_executable_quality.py
tests/test_decision_pipeline.py
```

Must preserve:

- family-correct structural invalidation;
- no SL rewrite to fit Risk;
- no inherited fixed Swing 1.20R hard dependency;
- gross R distinct from current costs;
- fixed emergency spread plus spread/SL, spread/target and cost/reward dimensions;
- current deterioration does not rewrite historical plan.

## 9. Risk

Source:

```text
risk/engine.py
risk/state.py
risk/permissions.py
```

Current proof:

```text
tests/test_risk_profiles.py
tests/test_risk_state.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

Exact preserved policy regression-checked by the contract-sync verifier:

```text
SMALL  3.0–4.5 / >4.5–6.5 / hard 7 / daily 12
MEDIUM 2.0–3.0 / >3.0–4.5 / hard 5 / daily 9
NORMAL 1.0–2.0 / >2.0–3.5 / hard 4 / daily 7
Aggressive overlay disabled by default; 8% single ceiling / 16% aggregate/day
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

Current proof:

```text
tests/test_news_context.py
tests/test_guarded_demo_runtime.py
```

Required semantics:

```text
News event / provider unavailable
→ no direct hard block

actual broker session UNKNOWN/CLOSED/PRE_CLOSE
→ hard state according to owner
```

The 1800-second context-cache freshness baseline remains preserved.

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

Current proof:

```text
tests/test_execution_intent.py
tests/test_gate.py
tests/test_controller.py
tests/test_action_reconciliation.py
tests/test_writer_attribution.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

Must preserve persist-before-send, one send per Intent, no blind retry, action-sensitive OPEN/MODIFY/CLOSE reconciliation, sole writer and controller fencing.

## 12. Management / close proof

Source:

```text
management/models.py
management/manager.py
management/execution.py
management/closure.py
management/store.py
```

Current proof:

```text
tests/test_managed_trade_store.py
tests/test_management_lifecycle.py
tests/test_action_reconciliation.py
tests/test_deal_history_reader.py
```

`management/closure.py` exists because exact broker/manual close proof is a separate responsibility from deciding HOLD/PROTECT/TRAIL/RUNNER/EXIT.

Unknown/manual Gold exposure is never silently adopted as bot-owned.

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

Current proof:

```text
tests/test_state_store.py
tests/test_checkpoint.py
tests/test_full_checkpoint.py
tests/test_recovery_package.py
```

The remaining fresh-machine + connected MT5 reconciliation/handoff drill belongs to Phase 15, not to offline test claims.

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

Current proof:

```text
tests/test_demo_launcher.py
tests/test_guarded_demo_runtime.py
tests/test_graphical_runtime.py
```

Write-capable DEMO behavior requires explicit DEMO confirmation and positive MT5 DEMO account proof. REAL remains hard-disabled.

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

Current proof:

```text
tests/test_dashboard_controls.py
tests/test_graphical_runtime.py
```

The approved GUI is one-screen/no-scroll. Timeframe, Indicators, Drawings and Settings controls are presentation-only and cannot trigger a broker cycle/write.

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

Current proof:

```text
tests/test_research_governance.py
tests/test_research_integrity.py
scripts/report_demo_learning_evidence.py
```

Research has zero raw broker authority. Candidate progression may advance through governed research stages but production promotion stops at `APPROVAL_REQUIRED`.

Phase 13 remains an area for additional depth/coverage while the architecture and safety boundaries are implemented.

## 17. Implemented scripts

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_zip.py
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
scripts/verify_contract_sync.py
scripts/verify_offline_release.py
```

`report_demo_learning_evidence.py` is read-only and reports durable StateStore evidence; it never connects to MT5 or performs a broker action.

`verify_contract_sync.py` fails the offline release when selected high-value frozen-document invariants drift from the source tree.

## 18. Integration test families currently represented

The current suite contains combined/integration tests for:

```text
market-first setup / no strategy forcing
strategy isolation
M5→M1 decision pipeline
executable quality
Risk policy/state
one-shot execution Intent / Gate / controller
guarded DEMO runtime
ManagedTrade lifecycle
OPEN/MODIFY/CLOSE reconciliation
broker deal-history close proof
StateStore/checkpoint/recovery package
graphical runtime and chart controls
research governance/integrity
```

Future file splits or additional edge-case tests must update this catalog only when they change material proof ownership.

## 19. Connected DEMO proof — still external

Offline code/tests cannot prove:

- actual Exness SymbolSpec;
- real market schedule/DST/holiday facts;
- broker filling/order modes;
- actual spread/slippage/deviation distributions;
- real decision/send/ack/reconcile latency;
- live OPEN/MODIFY/CLOSE lifecycle;
- broker/manual known-trade close visibility;
- restart during a real active lifecycle;
- fresh-machine MT5 recovery/handoff.

These remain Phase 15 evidence requirements.

## 20. Synchronization rule

Every material source/test addition, removal, rename or ownership change updates:

- this catalog;
- `MODULE_STRUCTURE.md`;
- the owning behavioral contract if behavior changes;
- release/audit status if evidence changes.

The offline release sequence includes:

```text
verify_documents_manual.py
→ verify_contract_sync.py
→ financial-secret scan
→ pytest
```

A green offline result does not claim connected DEMO certification.
