# GoldScalpTrader — Complete File and Test Catalog

**Status:** IMPLEMENTED FILE/TEST MAP — CURRENT HEAD REQUIRES OPERATOR OFFLINE RE-VERIFICATION / CONNECTED DEMO CERTIFICATION PENDING  
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

The canonical 66-document manual remains behavioral authority. `REAL = hard-disabled`.

## 2. Current architecture

```text
normalized MT5 reads
→ intelligence
→ market-first six-family setup detection
→ exactly one ACTIVE_EXECUTION + five SHADOW_ONLY
→ independent BUY/SELL + Red Team
→ durable M5 Opportunity
→ subordinate M1 Timing Intelligence
→ structural TradePlan / executable quality
→ durable UTC Risk-day authority + monetary sizing
→ hard Session authority / soft News context
→ Gate → durable Intent → sole MT5Writer → reconciliation
→ ManagedTrade → verified close
→ actual timing/management learning
→ automatic causal shadow counterfactual lifecycle
→ verified-learning research triggers
→ bounded durable discovery / explicit suppression
→ governed invention / immutable verified stage-proof packages
→ explicit approval; runtime activation remains separate from candidate registry stage
→ normalized presentation DTO
→ Swing-style PRIMARY terminal + SECONDARY localhost visual floor
```

## 3. Market / intelligence / decisions

Canonical owners:

```text
market_data/mt5_reader.py
market_data/activity.py
intelligence/snapshot.py
intelligence/candle_structure.py
intelligence/indicators.py
intelligence/technical.py
intelligence/liquidity.py
intelligence/confluence.py
strategies/floor.py
strategies/setup_detector.py
strategies/isolation.py
decisions/fusion.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
decisions/executable_quality.py
app/opportunity_lifecycle.py
research/timing_learning.py
```

Proof includes:

```text
tests/test_cycle_no_forcing.py
tests/test_strategy_isolation.py
tests/test_decision_pipeline.py
tests/test_opportunity_lifecycle.py
tests/test_timing_learning_lineage.py
```

M5 remains thesis authority. M1 cannot independently invent a trade. Missing facts remain UNKNOWN rather than fabricated zero.

## 4. Risk / Session / hard runtime authorities

Source:

```text
risk/engine.py
risk/state.py
risk/runtime.py
risk/permissions.py
app/session_news.py
app/session_authority.py
app/runtime.py
app/runtime_core.py
```

Proof:

```text
tests/test_risk_profiles.py
tests/test_risk_state.py
tests/test_risk_runtime_state.py
tests/test_session_news_provider.py
tests/test_session_runtime_authority.py
tests/test_guarded_demo_runtime.py
scripts/verify_contract_sync.py
```

Preserved Risk bands:

```text
SMALL  3.0–4.5 / >4.5–6.5 / hard 7 / daily 12
MEDIUM 2.0–3.0 / >3.0–4.5 / hard 5 / daily 9
NORMAL 1.0–2.0 / >2.0–3.5 / hard 4 / daily 7
Aggressive overlay disabled by default; 8% single / 16% aggregate-day ceiling
3 verified bot losses → at least 30m cooldown
one independently risk-bearing Gold position
```

Durable Risk-day state owns live OPEN sizing/profile stability. `app/runtime.py` is the sole public guarded DEMO composer; caller-supplied `market_open` permission is forbidden. `app/runtime_core.py` is mechanics-only and cannot expose a second full guarded execution cycle.

Required Session semantics:

```text
verified valid Session OPEN → session can report hard OPEN
PRE_CLOSE                  → never new-entry-allowed
expired/unverified Session → UNKNOWN
scope mismatch              → reject
obvious weekend fallback    → CLOSED, never fabricated weekday OPEN
News missing/stale          → soft UNAVAILABLE/STALE only
News health                 → never a hard-trading permission
```

## 5. Execution / recovery

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
management/models.py
management/manager.py
management/execution.py
management/closure.py
management/store.py
persistence/store.py
persistence/checkpoint.py
app/recovery.py
app/recovery_mt5.py
```

Execution remains:

```text
Gate
→ durable Intent
→ fresh local/broker prechecks
→ controller/fencing verification immediately before send
→ SUBMITTING persisted
→ exactly one MT5Writer send
→ ACK classification
→ broker reconciliation
```

No blind retry after ambiguous ACK. GoldScalp uses mutation-scoped controller leases; `execute_once()` re-verifies fencing immediately before irreversible send.

## 6. Actual learning / verified close

Source:

```text
research/learning.py
research/live_learning.py
research/timing_learning.py
research/runtime_evidence.py
management/closure.py
```

Proof:

```text
tests/test_live_learning_pipeline.py
tests/test_timing_learning_lineage.py
tests/test_runtime_research_evidence.py
```

Exactly-once actual learning:

```text
verified full-close queue item
→ validate immutable source identity
→ save StrategyMemory observation with allow_replace=False
→ consume queue only after durable save
```

Observed MFE/MAE/capture/timing metrics remain conservative. Missing or undersampled evidence remains `None` rather than invented.

## 7. Automatic SHADOW_ONLY lifecycle

Source:

```text
research/runtime_evidence.py
research/outcomes.py
research/shadow_runtime.py
app/demo_runner.py
```

Proof:

```text
tests/test_runtime_research_evidence.py
tests/test_research_integrity.py
tests/test_shadow_runtime.py
tests/test_research_runtime_isolation.py
```

Each qualified shadow family may freeze its own contemporaneous research-only Opportunity/Timing/structural plan. Future outcome evaluation uses only future completed M1 candles. Same-bar stop+target ordering remains AMBIGUOUS. Quoted spread is explicit in R; missing future slippage/commission remains a limitation rather than a fabricated value. One causal shadow episode produces at most one terminal counterfactual result.

## 8. Governed autonomous research

Source:

```text
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
research/ablation.py
research/episode_journal.py
research/triggers.py
research/discovery.py
research/invention.py
research/promotion.py
research/candidate_registry.py
research/stage_orchestrator.py
```

Proof:

```text
tests/test_candidate_registry.py
tests/test_candidate_transition_history.py
tests/test_research_governance.py
tests/test_research_integrity.py
scripts/run_walk_forward.py
```

`research/triggers.py` derives conservative idempotent research episodes from verified StrategyMemory. Faults and hard-safety blocks are not strategy optimization targets.

`research/discovery.py` requires repeated independent evidence and immutable source lineage. Eligible clusters create either a durable candidate or durable suppression reason.

`research/candidate_registry.py` cannot manufacture caller-hash PASS evidence. `research/stage_orchestrator.py` verifies immutable package integrity, exact candidate fingerprint, exact target stage, evidence identity, manifest SHA and stage-specific checks.

Stage progression is sequential and actor-attributed. Production-stage research still requires explicit operator approval plus rollback lineage, and **runtime activation remains separate from candidate registry stage**.

A generic compiler/evaluator for arbitrary newly invented candidate semantics is not claimed. Candidate discovery/governance exists; automatic execution semantics require an explicitly defined auditable candidate policy rather than generated hidden trading code.

## 9. Checkpoint / persistence

The full checkpoint exports all current StateStore namespaces by default, including shadow plans/terminal markers/outcomes, discovery episodes/status/suppressions, candidate transition history and stage evidence. Recovery never treats UNKNOWN broker truth as empty/zero.

Proof:

```text
tests/test_checkpoint.py
tests/test_full_checkpoint.py
tests/test_recovery_package.py
```

Fresh-machine/sequential handoff remains connected proof until actually drilled.

## 10. Operator / dashboard

Implemented source ownership:

```text
operator/presentation.py          → normalized presentation DTO
operator/graphical_snapshot.py    → runtime/cycle → presentation facts
operator/terminal_dashboard.py    → primary renderer dispatcher
operator/rich_dashboard.py        → 96+ column Swing-style Rich floor
operator/narrow_dashboard.py      → 64–95 column stacked floor
operator/compact_dashboard.py     → crash-safe fallback
graphical_dashboard/snapshot.py   → atomic read-only browser payload
graphical_dashboard/server.py     → localhost-only read-only server
graphical_dashboard/ui.py         → Swing-style secondary visual floor
app/demo_runner.py                → terminal primary + optional browser secondary
```

Proof:

```text
tests/test_demo_launcher.py
tests/test_browser_dashboard.py
```

Implemented presentation hierarchy:

```text
PRIMARY terminal
  → Market / Session / SELL / BUY / Spread / M5 countdown
  → Market Picture + Trade Setup
  → Current Decision / Urdu action
  → Trade Plan
  → 1 ACTIVE + 5 SHADOW Strategy Isolation board
  → Risk & Account / Today & Activity / System & Execution
  → ManagedTrade
  → Learning / Discovery

SECONDARY localhost browser
  → robot + Arabic/English/Urdu masthead
  → market/live-price/countdown strip
  → M1/M5/M15/H1/H4 completed-candle chart
  → Indicators / Drawings / Bars presentation controls
  → Timing / Signal / Trade Plan / Blocker-Gate
  → six-family research board
  → Risk / ManagedTrade / Activity / Learning / Discovery / Execution / System
```

The browser has no BUY/SELL/MODIFY/CLOSE controls. Both surfaces are presentation-only and own no Risk, Gate or MT5 writer authority. `DASHBOARD_MODE=GUI` means primary terminal **plus** browser secondary.

## 11. Connected DEMO evidence

Read-only evidence tooling:

```text
src/gold_scalp_trader/diagnostics/connected_demo.py
src/gold_scalp_trader/diagnostics/connected_runtime_evidence.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
scripts/report_demo_learning_evidence.py
```

Local deterministic evidence never auto-proves real Exness broker behavior.

## 12. Current offline status

The operator previously proved full offline PASS at commit `3458b97e88371be6aa665d0891b20e384384cefe` after the backend authority/research changes. The later dashboard-parity implementation changes presentation code/tests/docs, so **current HEAD requires a fresh operator run of `python scripts/verify_offline_release.py` before that PASS is inherited**.

## 13. Connected DEMO proof — still external

Offline code/tests cannot prove:

- actual Exness SymbolSpec/filling/stops/freeze/margin/order-check behavior;
- real market schedule/DST/holiday/PRE_CLOSE facts;
- actual spread/slippage/deviation/fill distributions;
- decision→send→ack→reconcile latency;
- controlled OPEN/MODIFY/PROTECT/TRAIL/CLOSE lifecycle;
- broker-side TP/SL visibility;
- manual close attribution;
- ambiguous acknowledgement/no duplicate under real broker behavior;
- restart during real exposure;
- fresh-machine restore/sequential handoff;
- statistically meaningful active/shadow/timing/management/discovery evidence.

These remain connected evidence requirements.

## 14. Synchronization rule

Every material source/test/script addition, removal, rename, authority change or proof-status change updates this catalog, `MODULE_STRUCTURE.md` where ownership changes, the owning behavioral contract and static verifier where needed. Offline PASS must never be described as connected certification.
