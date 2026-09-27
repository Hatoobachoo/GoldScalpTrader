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
→ governed invention / immutable verified stage-proof packages
→ explicit approval; runtime activation remains separate from candidate registry stage
```

## 3. Market / intelligence / decisions

Canonical owners include:

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

## 4. Risk / hard runtime authorities

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

Durable Risk-day state now owns live OPEN sizing/profile stability. `app/runtime.py` is the sole public guarded DEMO composer; caller-supplied `market_open` permission is forbidden. `app/runtime_core.py` is mechanics-only and cannot expose a second full guarded execution cycle.

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

No blind retry after ambiguous ACK. GoldScalp deliberately uses mutation-scoped controller leases rather than adding an unnecessary long-lived heartbeat; `execute_once()` re-verifies fencing immediately before irreversible send.

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

Exactly-once actual learning remains:

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

Each qualified shadow family may freeze its own contemporaneous research-only Opportunity/Timing/structural plan. It cannot copy active broker authority. Future outcome evaluation uses only completed M1 candles opening at/after the frozen hypothetical entry. Same-bar stop+target ordering remains AMBIGUOUS. Quoted spread is recorded explicitly in R; missing future slippage/commission is declared as a limitation, not fabricated. One causal shadow episode can produce at most one terminal counterfactual result.

Research recording is best-effort relative to broker authority: a timing/management/shadow evidence failure is surfaced as research degradation but cannot erase or reclassify a completed broker cycle.

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
research/discovery.py
research/invention.py
research/promotion.py
research/candidate_registry.py
research/stage_orchestrator.py
```

Proof:

```text
tests/test_candidate_registry.py
tests/test_research_governance.py
tests/test_research_integrity.py
scripts/run_walk_forward.py
```

`research/candidate_registry.py` no longer exposes an arbitrary caller-hash PASS issuer. Promotion evidence must come through `research/stage_orchestrator.py` as an immutable verified evidence package bound to the exact candidate fingerprint, exact next target stage, recomputed evidence identity, package-manifest SHA-256, and target-stage-specific required checks. No profitability threshold is invented where frozen policy has not defined one.

Stage progression remains sequential; final Production-stage research still requires explicit operator approval plus rollback lineage, and **runtime activation remains separate from candidate registry stage**.

## 9. Checkpoint / persistence

The full checkpoint exports all current StateStore namespaces (records and append-only events), including shadow plans/terminal markers/outcomes and candidate-stage evidence. Recovery never treats UNKNOWN broker truth as empty/zero.

Proof includes:

```text
tests/test_checkpoint.py
tests/test_full_checkpoint.py
tests/test_recovery_package.py
```

Fresh-machine/sequential handoff remains connected proof until actually drilled.

## 10. Operator/dashboard

Dashboard implementation remains present but visual parity work is intentionally deferred until non-dashboard safety/research completion is verified. Primary terminal and secondary localhost browser remain presentation-only; they own no Risk, Gate or MT5 writer authority.

## 11. Connected DEMO evidence

Read-only evidence tooling remains:

```text
src/gold_scalp_trader/diagnostics/connected_demo.py
src/gold_scalp_trader/diagnostics/connected_runtime_evidence.py
scripts/certify_connected_demo.py
scripts/monitor_connected_demo.py
scripts/report_demo_learning_evidence.py
```

Local deterministic evidence never auto-proves real Exness broker behavior.

## 12. Current offline status

A prior operator-run baseline passed compileall/documents/contract-sync/secrets/pytest. Since the later Session/Risk authority, automatic shadow lifecycle and verified stage-package changes, **current HEAD requires a fresh operator run of `python scripts/verify_offline_release.py` before OFFLINE PASS is inherited**.

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
- statistically meaningful active/shadow/timing/management learning evidence.

These remain Phase-15 connected evidence requirements.

## 14. Synchronization rule

Every material source/test/script addition, removal, rename, authority change or proof-status change must update this catalog, `MODULE_STRUCTURE.md` where ownership changes, owning behavioral contracts when behavior changes, and the static verifier. Offline PASS must never be described as connected certification.
