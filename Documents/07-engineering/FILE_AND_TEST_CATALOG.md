# GoldScalpTrader — Complete File and Test Catalog

**Status:** IMPLEMENTED FILE/TEST MAP — OFFLINE RELEASE PASS / CONNECTED DEMO CERTIFICATION PENDING  
**Version:** 2.6-institutional-scalp-implementation  
**Authority:** Actual source ownership, deterministic/integration proof, remaining connected proof, and implementation/document synchronization.

## 1. Evidence classes

```text
source exists
≠ deterministic test proof
≠ offline integration proof
≠ connected Exness DEMO proof
≠ future REAL release proof
```

The canonical 66-document manual remains the behavioral source of truth. Status/mapping documents describe the as-built implementation without weakening frozen behavior.

## 2. Current architecture map

```text
config/domain/diagnostics/security
→ market_data
→ intelligence
→ strategies: market-first setup detection + six families + isolation
→ decisions: independent BUY/SELL + Red Team + M5 Opportunity + M1 timing + TradePlan + executable quality
→ risk
→ app/session hard authority
→ execution Gate / Intent / sole writer / reconciliation
→ management / verified close
→ exactly-once learning + timing/management/shadow evidence
→ governed research candidate registry
→ operator/dashboard

persistence = durable local state/checkpoints/recovery
connected diagnostics = read-only Phase-15 evidence
REAL = hard-disabled
```

## 3. Foundation / market data / intelligence

Implemented owners include:

```text
config/settings.py
domain/enums.py
domain/ids.py
domain/market.py
domain/models.py
diagnostics/logging.py
diagnostics/reasons.py
diagnostics/health.py
diagnostics/metrics.py
diagnostics/connected_demo.py
security/financial_secrets.py
market_data/account_mode.py
market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py
intelligence/candle_structure.py
intelligence/indicators.py
intelligence/technical.py
intelligence/liquidity.py
intelligence/confluence.py
intelligence/session.py
intelligence/news.py
intelligence/snapshot.py
```

Proof includes settings/config/domain/MT5-reader/deal-history/activity/confluence/News tests plus secret and contract-sync scripts.

The normalized reader owns completed multi-timeframe history, quote age, account/symbol/position facts and deal history. `None` remains UNKNOWN rather than fabricated zero. Real Exness SymbolSpec/filling/schedule behavior remains connected proof.

## 4. Strategy / decision / Timing Intelligence

Source:

```text
strategies/floor.py
strategies/setup_detector.py
strategies/isolation.py
strategies/scheduler.py
strategies/confluence.py
decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
decisions/executable_quality.py
app/opportunity_lifecycle.py
research/timing_learning.py
```

Proof:

```text
tests/test_cycle_no_forcing.py
tests/test_strategy_isolation.py
tests/test_decision_pipeline.py
tests/test_executable_quality.py
tests/test_opportunity_lifecycle.py
tests/test_timing_learning_lineage.py
```

Critical behavior:

- market setup is detected before active-family execution eligibility;
- exactly one family may be `ACTIVE_EXECUTION`; others are `SHADOW_ONLY`;
- BUY/SELL are independently evaluated;
- M5 remains thesis/setup authority;
- M1 may only refine an existing M5 Opportunity;
- durable Opportunity/Episode identity survives refresh/restart;
- terminal `TRIGGERED` lifecycle prevents same causal setup being randomly re-armed;
- timing policy/profile/event-age/trigger-age/chase lineage is frozen before irreversible OPEN send and preserved through ManagedTrade/verified learning;
- no structural TradePlan may be fabricated merely to fit ATR/Risk.

## 5. Risk

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

Preserved policy:

```text
SMALL  3.0–4.5 / >4.5–6.5 / hard 7 / daily 12
MEDIUM 2.0–3.0 / >3.0–4.5 / hard 5 / daily 9
NORMAL 1.0–2.0 / >2.0–3.5 / hard 4 / daily 7
Aggressive overlay disabled by default; 8% single ceiling / 16% aggregate/day
3 losses → at least 30m cooldown
max independent Gold positions = 1
```

Durable UTC risk-day/account-safety state is restart-safe and read/accounting-only.

## 6. Session / News runtime authority

Source:

```text
app/session_news.py
app/session_authority.py
intelligence/session.py
intelligence/news.py
risk/permissions.py
```

Proof:

```text
tests/test_news_context.py
tests/test_session_news_provider.py
tests/test_session_runtime_authority.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

Required semantics:

```text
verified valid Session OPEN → session can report hard OPEN
PRE_CLOSE                  → never new-entry-allowed
expired/unverified Session → UNKNOWN
scope mismatch              → reject
obvious weekend fallback    → CLOSED, never fabricated weekday OPEN
News missing/stale          → soft UNAVAILABLE/STALE only
News health                 → never a hard-trading permission
```

`app/session_authority.py` is the runtime hard-authority composition layer. It has no broker-write authority. Current Exness schedule/DST/holiday correctness remains Phase-15 external proof.

## 7. Execution / runtime split

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
app/runtime.py
app/runtime_core.py
```

Proof:

```text
tests/test_execution_intent.py
tests/test_gate.py
tests/test_controller.py
tests/test_action_reconciliation.py
tests/test_writer_attribution.py
tests/test_guarded_demo_runtime.py
```

`app/runtime.py` owns runtime policy/orchestration around Session and durable Opportunity. `app/runtime_core.py` preserves the exactly-once financial lifecycle implementation. All OPEN/MODIFY/CLOSE paths retain:

```text
Gate
→ durable Intent
→ fresh local/broker prechecks
→ SUBMITTING
→ exactly one MT5Writer send
→ acknowledgement classification
→ reconciliation
```

No blind retry after ambiguous acknowledgement. Raw `order_send` remains inside the sole writer.

## 8. Management / verified close / timing lineage

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
tests/test_live_learning_pipeline.py
```

Verified OPEN freezes Opportunity/episode/TradePlan/M5 event/TimingDecision lineage into ManagedTrade. Exact close proof carries the same lineage into the learning queue. Missing efficiency metrics remain `None`; they are never fabricated.

## 9. Persistence / recovery

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

StateStore is strict/checksummed local context, not current broker truth. Recovery must reconcile restored local state against fresh MT5 truth before financial authority resumes. Fresh-machine/sequential handoff remains connected Phase-15 proof.

## 10. Research / continuous learning / shadow evidence

Source:

```text
research/learning.py
research/live_learning.py
research/timing_learning.py
research/runtime_evidence.py
research/candidate_registry.py
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
tests/test_timing_learning_lineage.py
tests/test_runtime_research_evidence.py
tests/test_candidate_registry.py
tests/test_research_governance.py
tests/test_research_integrity.py
scripts/report_demo_learning_evidence.py
scripts/run_walk_forward.py
```

Exactly-once actual learning remains:

```text
verified full-close queue item
→ validate immutable source identity
→ save StrategyMemory observation with allow_replace=False
→ consume queue only after durable save
```

Runtime research evidence records management-path observations and same-market shadow-family counterfactual facts without broker authority. Timing evidence is content-addressed/idempotent.

Autonomous invention is declarative research only. `research/candidate_registry.py` requires real durable source evidence, preserves deterministic candidate fingerprints and governed evidence chains, forbids stage skipping through the promotion model, and **runtime activation remains separate from candidate registry stage**. Production-stage research evidence alone does not mutate active runtime strategy, Risk, Gate or broker authority.

## 11. Application / operator / dashboard

Source:

```text
app/main.py
app/runtime.py
app/runtime_core.py
app/session_authority.py
app/opportunity_lifecycle.py
app/startup.py
app/recovery.py
app/recovery_mt5.py
app/cycle.py
app/loop.py
app/dashboard.py
app/live_presentation.py
app/session_news.py
app/demo_runner.py
app/graphical_demo_runner.py
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
tests/test_demo_launcher.py
tests/test_guarded_demo_runtime.py
tests/test_dashboard_controls.py
tests/test_graphical_runtime.py
tests/test_session_runtime_authority.py
tests/test_opportunity_lifecycle.py
```

The graphical dashboard is presentation-only. Runtime snapshots now expose hard Session state plus Opportunity/Timing lineage in addition to strategy, TradePlan, Risk, execution and ManagedTrade state.

## 12. Connected DEMO evidence / Phase 15

Implemented read-only tooling:

```text
src/gold_scalp_trader/diagnostics/connected_demo.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
tests/test_connected_demo_evidence.py
```

It cannot perform broker writes or enable REAL. Operator drill evidence must be DEMO/scope/hash/time bound. Missing connected/manual/restart/handoff/schedule/distribution drills remain PENDING, never inferred PASS.

## 13. Root engineering guides

These guides are intentionally outside the frozen 66-document manual topology:

```text
REAL_AND_DEMO_MODE_ARCHITECTURE.md
TIMING_INTELLIGENCE_AND_GOVERNED_LEARNING_IMPLEMENTATION.md
GOVERNED_AUTONOMOUS_STRATEGY_IMPLEMENTATION.md
```

They describe as-built implementation hierarchy and do not replace canonical behavioral contracts.

## 14. Offline release status

Latest operator-provided local run after commit `7fdf57c` reported:

```text
compileall     PASS
documents      PASS
contract-sync  PASS
secrets        PASS
pytest         PASS
OFFLINE STATUS: PASS
```

This proves the current offline release checks passed in the intended Windows working copy. It does not prove connected Exness broker behavior.

## 15. Connected DEMO proof — still external

Offline code/tests cannot prove:

- actual Exness SymbolSpec/filling/stops/freeze/margin/order-check behavior;
- real market schedule/DST/holiday/PRE_CLOSE facts;
- actual spread/slippage/deviation/fill distributions;
- real decision→send→ack→reconcile latency;
- controlled OPEN/MODIFY/PROTECT/TRAIL/CLOSE lifecycle;
- broker-side TP/SL visibility;
- manual close attribution;
- ambiguous acknowledgement/no duplicate under real broker behavior;
- restart during a real active lifecycle;
- fresh-machine restore/sequential handoff;
- statistically meaningful active/shadow/timing/management learning evidence.

These remain Phase-15 evidence requirements until actually observed.

## 16. Synchronization rule

Every material source/test/script addition, removal, rename, ownership change or proof-status change updates:

- this catalog;
- `MODULE_STRUCTURE.md` when module/file ownership changes;
- owning behavioral contract only when behavior itself changes;
- status/audit documentation;
- `scripts/verify_contract_sync.py` for high-value ownership/proof regressions.

Offline PASS must never be described as connected certification. `REAL` remains hard-disabled until the separate future release gate is explicitly approved.
