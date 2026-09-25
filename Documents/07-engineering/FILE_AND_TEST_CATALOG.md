# GoldScalpTrader — Complete File and Test Catalog

**Status:** FINAL PRE-IMPLEMENTATION FILE/TEST MAP — IMPLEMENTATION PENDING
**Version:** 2.0-institutional-scalp
**Authority:** Planned source ownership, planned deterministic/integration/connected proof and current repository reality.

## 1. Current repository reality

The repository still contains a small provisional Python scaffold plus the canonical documentation manual. Planned files/tests in this catalog are **targets**, not implementation claims.

The provisional scaffold must not override canonical Documents.

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
```

## 3. Foundation/config/domain — planned source

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

Planned proof families:

```text
test_settings.py
test_domain_ids.py
test_domain_serialization.py
test_reason_codes.py
test_health_models.py
test_metrics.py
test_financial_secrets.py
```

Must prove mode/policy validation, preserved Risk configuration, active-family identity, finite/UTC-safe serialization, secret redaction and no credential leakage.

## 4. Market-data layer

Source:

```text
market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py
```

Tests:

```text
test_mt5_reader_normalization.py
test_market_snapshot.py
test_symbol_resolution.py
test_quote_freshness.py
test_completed_candles.py
test_m1_bounded_history.py
test_positions_empty_vs_unavailable.py
test_activity_accounting.py
test_deal_lineage.py
```

Proof:

- one normalized analytical MT5 boundary;
- completed H1/M15/M5 and bounded M1 chronology;
- optional H4;
- Bid/Ask/source/capture timestamps;
- future-clock/stale/corrupt detection;
- `[]` vs `None` exposure semantics;
- symbol/spec normalization;
- no raw write authority.

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

Tests:

```text
test_candle_structure.py
test_structure_chronology.py
test_indicators.py
test_technical_zones.py
test_liquidity_smc.py
test_confluence.py
test_session_context.py
test_news_context.py
test_intelligence_snapshot.py
```

Required proof includes no-lookahead, pivot-vs-confirmation time, pool-before-sweep, FVG/OB lifecycle, optional evidence neutrality, family-specific confluence, News soft-only semantics and causal replay parity.

## 6. Setup detector / Strategy Isolation / six families

Source:

```text
strategies/floor.py
strategies/setup_detector.py
strategies/isolation.py
strategies/scheduler.py
strategies/confluence.py
```

Tests:

```text
test_strategy_families.py
test_setup_detector.py
test_setup_detector_none.py
test_setup_detector_multiple_candidates.py
test_strategy_isolation.py
test_active_family_not_forced.py
test_shadow_cannot_trade.py
test_active_family_switch_attribution.py
test_family_event_lineage.py
test_scheduler_parity.py
```

Critical invariant tests:

```text
active family = Breakout Retest
market setup = Liquidity Sweep only
→ no live Breakout Retest Opportunity
→ live WAIT
→ Liquidity Sweep shadow record exists
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

Tests:

```text
test_active_buy_sell_independence.py
test_red_team.py
test_optional_evidence.py
test_correlation_caps.py
test_opportunity_lifecycle.py
test_opportunity_restart.py
test_m1_subordinate_timing.py
test_m1_cannot_create_opportunity.py
test_m1_trigger_freshness.py
test_m5_event_age.py
test_chase_drift.py
test_terminal_rearm.py
```

## 8. TradePlan / executable quality

Source:

```text
decisions/family_trade_plan.py
decisions/trade_plan.py
decisions/executable_quality.py
```

Tests:

```text
test_trade_plan.py
test_family_invalidation.py
test_breakout_retest_geometry.py
test_reversal_event_geometry.py
test_target_provenance.py
test_original_r.py
test_executable_quality.py
test_emergency_spread.py
test_spread_sl_ratio.py
test_spread_target_ratio.py
test_cost_reward.py
test_slippage_allowance.py
test_price_drift.py
test_latency_revalidation.py
```

Must prove:

- structural SL never rewritten to fit Risk;
- no fixed inherited Swing 1.20R dependency;
- gross R separate from current costs;
- spread/SL and spread/target use consistent units;
- cost components not double-counted;
- latency triggers fresh revalidation;
- current deterioration does not rewrite historical plan.

## 9. Risk

Source:

```text
risk/engine.py
risk/state.py
risk/permissions.py
```

Tests:

```text
test_risk_profiles.py
test_risk_profile_day_lock.py
test_dynamic_volume.py
test_min_lot_affordability.py
test_aggressive_mode.py
test_account_safety_pl.py
test_daily_loss_lock.py
test_manual_reset.py
test_same_episode_reentry.py
test_consecutive_loss_cooldown.py
test_margin.py
test_capacity.py
test_risk_restart.py
```

Exact preserved profile table and disabled-by-default aggressive 8%/16% semantics must be regression-tested.

## 10. Session / News provider

Source:

```text
app/session_news.py
intelligence/session.py
intelligence/news.py
risk/permissions.py
```

Tests:

```text
test_session_schedule.py
test_preclose_reopen.py
test_session_unknown.py
test_news_provider_health.py
test_news_cache.py
test_news_context_soft_only.py
test_no_news_blackout.py
test_no_news_cooldown.py
test_no_post_news_warmup.py
```

Required semantics:

```text
News event / provider unavailable
→ no direct hard block

actual broker session UNKNOWN/CLOSED/PRE_CLOSE
→ hard state according to owner
```

1800s remains context-cache freshness baseline; stale data is never relabelled fresh.

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

Tests:

```text
test_execution_gate.py
test_gate_not_evaluated.py
test_execution_intent.py
test_persist_before_send.py
test_precheck_zero_send.py
test_mt5_writer_boundary.py
test_order_check.py
test_ambiguous_ack.py
test_no_blind_retry.py
test_open_reconciliation.py
test_modify_reconciliation.py
test_close_reconciliation.py
test_controller_fencing.py
test_manual_external_exposure.py
test_startup_execution_recovery.py
```

## 12. Management

Source:

```text
management/models.py
management/manager.py
management/execution.py
management/store.py
```

Tests:

```text
test_trade_manager_hold.py
test_protect_trail.py
test_no_stop_widening.py
test_time_efficiency_exit.py
test_runner_conditions.py
test_partial_management.py
test_min_lot_no_partial_dependency.py
test_preclose_flatten.py
test_manual_known_trade_close.py
test_verified_close_archive.py
```

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

Tests:

```text
test_store_integrity.py
test_store_strict_types.py
test_idempotency.py
test_checkpoint.py
test_restore_new_path.py
test_opportunity_plan_ordering.py
test_intent_crash_recovery.py
test_close_learning_queue.py
test_active_family_restore.py
test_candidate_state_restore.py
test_sequential_handoff.py
test_no_runtime_git.py
```

## 14. Operator / graphical dashboard

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

Tests:

```text
test_dashboard_dto.py
test_dashboard_read_only.py
test_detected_setup_display.py
test_active_shadow_display.py
test_blocker_vs_gate.py
test_no_scroll_layout_contract.py
test_chart_timeframe_controls.py
test_chart_indicators_controls.py
test_chart_drawings_controls.py
test_chart_settings_controls.py
test_dashboard_snapshot_atomicity.py
```

No visual test claims exact aesthetics until the actual UI is implemented and reviewed, but layout/interaction contracts are testable.

## 15. Research / learning / ML

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

Tests:

```text
test_replay_no_lookahead.py
test_replay_strategy_isolation.py
test_replay_m1.py
test_replay_capacity.py
test_evidence_identity.py
test_holdout_one_shot.py
test_stress.py
test_actual_shadow_separation.py
test_live_learning_exactly_once.py
test_discovery_liveness.py
test_candidate_fingerprint.py
test_strategy_invention.py
test_ml_evidence_identity.py
test_promotion_stages.py
test_approval_required.py
```

Research has zero raw broker authority.

## 16. Planned scripts

```text
scripts/run_walk_forward.py
scripts/acquire_mt5_dataset.py
scripts/report_demo_learning_evidence.py
scripts/restore_runtime_checkpoint.py
scripts/create_local_recovery_package.py
scripts/create_source_zip.py
scripts/scan_financial_secrets.py
scripts/verify_documents_manual.py
```

`verify_documents_manual.py` should check final 66-file inventory, `01`–`08` folder topology, broken links, stale legacy paths/terms and required metadata/visual sections where practical.

## 17. Integration test families

Expected integration suites:

```text
entry pipeline: snapshot → setup detection → isolation → Opportunity → M1 → plan → quality → Risk
DRY_RUN full cycle
DEMO one-shot OPEN
DEMO MODIFY / CLOSE
restart with unresolved Intent
restart with ManagedTrade
broker/manual known-close recovery
Risk-day/cash-flow rollover
Strategy Isolation active-family switch
shadow research pipeline
checkpoint → restore → reconcile
sequential machine handoff
operator snapshot/read-only dashboard
```

## 18. Connected DEMO proof

Mocks cannot prove:

- actual Exness SymbolSpec;
- real market schedule/DST/holiday facts;
- broker filling/order modes;
- actual spread/slippage/deviation;
- latency;
- OPEN/MODIFY/CLOSE lifecycle;
- manual close visibility;
- fresh-machine MT5 recovery.

These remain connected evidence requirements.

## 19. Synchronization rule

Every actual source/test addition, removal or rename updates this catalog, Module Structure, owning contract and relevant release/audit docs in the same coherent packet.
