# GoldScalpTrader — Coder Guide

**Status:** POST-AUDIT-1 DEVELOPER MANUAL — FREEZE-PREPARATION, IMPLEMENTATION NOT STARTED
**Version:** 1.1-cache-aware-handoff
**Authority:** Developer navigation, phase boundaries, source/test ownership, implementation traces and completion evidence.

## 1. Read before code

GoldScalpTrader is documentation-first. Topic contracts own behaviour; this guide navigates them and cannot override them.

Current sequence:

```text
64-file canonical manual           COMPLETE
Fresh-Zero Audit 1                 COMPLETE
Core affected-graph sync           COMPLETE
Documentation metadata/cross-links CURRENT
Final documentation freeze         PENDING audit closure
Implementation                     NOT STARTED
```

The old Python scaffold is provisional safety seed, not final architecture.

## 2. Authority reading order

1. `README.md` + `GLOSSARY.md`;
2. `00-foundation/SYSTEM_CONTRACT.md`;
3. relevant topic contract;
4. active `DESIGN_DECISIONS.md` + remaining `OPEN_QUESTIONS.md`;
5. Architecture / Trading Floor;
6. Coding Standard;
7. Module Structure + File/Test Catalog;
8. Documentation Standard;
9. current source/tests/diff/evidence.

For reference changes also read `90-governance/DOCUMENTATION_COMPARISON.md`.

Repair contradictions before coding.

## 3. Architectural spine

```text
one normalized MT5 read boundary
→ immutable MarketSnapshot
→ staged logically independent intelligence
→ six independent scalp families
→ BUY / SELL fusion + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing / event freshness
→ family-aware TradePlan
→ gross + cost-adjusted room
→ STANDARD monetary Risk
→ hard session/news/system/account/controller authorities
→ central Gate
→ durable one-shot Intent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ exactly-once learning
→ research/discovery/promotion
→ local checkpoint/recovery
```

Logical parallel analysis, serial financial/broker authority.

## 4. Frozen V1 timeframe authority

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote executable Bid/Ask/spread/drift/health
```

Do not hide M1 production authority in a helper.

## 5. Parallel versus serial implementation

Logically independent desks/families may be scheduled concurrently only if inputs are immutable and outputs deterministic.

Physical worker concurrency is optional/profiling-driven. A one-worker implementation is fully valid and must be semantically identical.

Must remain ordered:

```text
TradePlan
→ STANDARD Risk
→ hard permission
→ Gate
→ Intent persisted
→ fresh broker prechecks
→ sole writer
→ reconciliation
```

Verified close precedes learning; restore precedes broker reconciliation; broker reconciliation precedes new write authority.

## 6. Phase dependency order

```text
1–2 Foundation + read truth
3   Intelligence
4   Strategy / decision floor
5   TradePlan + STANDARD monetary Risk
6   Session/news provider/cache + persistence/recovery
7   Execution/controller/reconciliation
8   Trade Manager + close recovery
9   Operator dashboards
10  Research + durable/live learning
11  Local runtime backup / restore / machine handoff
12  Connected external proof + release audits
```

A later phase never hides an incomplete earlier authority.

## 7. Planned source ownership

Foundation: `config/`, `domain/`, `diagnostics/`, `security/`.

Market truth: `market_data/mt5_reader.py`, `activity.py`, `snapshot.py`.

Intelligence: `intelligence/candle_structure.py`, `indicators.py`, `technical.py`, `liquidity.py`, `confluence.py`, `session.py`, `news.py`, `snapshot.py`.

Strategies/decisions: `strategies/floor.py`, `parallel.py`, `confluence.py`; `decisions/fusion.py`, `snapshot.py`, `opportunity.py`, `timing.py`, `family_trade_plan.py`, `trade_plan.py`.

Risk/execution: `risk/engine.py`, `state.py`, `permissions.py`; `execution/models.py`, `checks.py`, `gate.py`, `intent_store.py`, `service.py`, `mt5_writer.py`, `reconcile.py`, `controller.py`, `sqlite_coordination.py`.

Management/persistence: `management/models.py`, `manager.py`, `execution.py`, `store.py`; `persistence/store.py`, `runtime_state.py`, `checkpoint.py`, `backup.py`, `local_recovery_package.py`.

App/operator: `app/main.py`, `runtime.py`, `startup.py`, `recovery.py`, `recovery_mt5.py`, `cycle.py`, `loop.py`, `dashboard.py`, `live_presentation.py`, `session_news.py`; `operator/*`, optional `graphical_dashboard/*`.

Research: learning/live-learning/replay/management-replay/session-history/stress/validation/datasets/acquisition/evidence/packages/metrics/outcomes/ablation/episode-journal/discovery/invention/promotion.

Exact tree stays synchronized with `MODULE_STRUCTURE.md` and `FILE_AND_TEST_CATALOG.md` as implementation appears.

## 8. Scalping engineering hotspots

### Freshness

Keep separate bar identity, knowledge time, event time, Opportunity/TradePlan creation, final decision and Intent/precheck/send/reconcile times. Historically true does not mean fresh enough to enter.

### Cost / geometry

Keep distinct gross structural geometry, Approved Entry Reference, current Bid/Ask/spread, explicit reserve assumptions and Actual Fill. Never double count costs or change SL/target to improve apparent R.

### Small account / min lot

Use one STANDARD policy. If theoretical volume is below broker minimum, evaluate actual minimum volume against structural stop and hard ceiling. Never tighten stop to make 0.01 fit.

### News provider / last-known-good cache

Keep these separate:

```text
provider refresh health
accepted event truth
hard News permission
```

Canonical flow:

```text
live/file refresh succeeds
→ validate schema/scope/coverage/TTL
→ normalize event facts
→ atomically update accepted LKG cache

refresh fails
+ existing LKG cache still valid under ORIGINAL timestamps/coverage/TTL
→ use cached accepted event truth
→ provider may be DEGRADED

refresh fails
+ cache expired/invalid/missing
→ NEWS_SAFETY_UNKNOWN
→ V1 new-entry BLOCK / LIMITED
```

Never rewrite `fetched_at`, `as_of`, coverage or `valid_until` merely because acquisition failed. Cache existence alone is not validity.

Ownership:

- `app/session_news.py`: provider/cache transport, atomic replacement, scope/schema/TTL/coverage/integrity;
- `intelligence/news.py`: normalized event/tier facts;
- `risk/permissions.py`: CLEAR/BLACKOUT/UNKNOWN permission semantics;
- dashboard: display only, no cache validation authority.

### Time efficiency

No separate TIME_EXIT action; calibrated time weakness is an `EXIT` reason.

## 9. Pure function rule

Prefer pure deterministic functions for indicator/structure/technical/liquidity derivation, event normalization, family evaluation, fusion, TradePlan, already-known-fact monetary sizing and replay metrics.

Use stateful components only for real resources/lifecycle such as MT5, provider/cache I/O, StateStore, controller, Intent, recovery/runtime loop and Trade Manager.

## 10. UNKNOWN / corrupt / ambiguous examples

```text
positions_get == []
→ verified zero

positions_get == None
→ unavailable, not zero

News refresh failed + valid LKG cache
→ NOT automatically UNKNOWN; use accepted cached truth, provider may be DEGRADED

News refresh failed + expired/invalid/no cache
→ NEWS_SAFETY_UNKNOWN; new-entry BLOCK / LIMITED

future candle/provider fetch time
→ CORRUPT / reject

unknown equity
→ Risk UNKNOWN

ambiguous broker send
→ reconcile, never blind resend
```

## 11. Execution boundary

No irreversible writer exists until its deliberate phase.

When implemented: one writer; persist Intent before send; one send allowance; fresh account/symbol/quote/order prechecks; ambiguous result → reconciliation; state changes only after broker proof; stale controller denied; REAL remains outside V1.

## 12. Runtime persistence / local backup

```text
transactional StateStore
→ rolling local checkpoint
→ graceful-shutdown final local checkpoint
→ portable runtime recovery package when requested
```

No runtime Git commit/push/pull.

Provider/cache files are current safety context and must be revalidated after restart; a restored cache never grants broker authority by itself.

## 13. Development/source backup

Normal operator workflow after a major coherent bulk:

```text
one remote fast-forward commit
→ operator git pull --ff-only
→ local clone now has latest project + full Git history
→ optional secret-clean ZIP source snapshot
```

Do not create noisy micro-commit/pull cycles when one coherent bulk is safer. Git bundle is optional advanced/manual only.

## 14. Research boundary

Research may replay, measure, discover and propose. It cannot call writer, self-promote, mutate production dynamically, remove hard safety, convert counterfactual R into actual P/L or reuse final holdout during tuning.

Scalp research explicitly preserves costs, latency, duration, minimum-lot affordability and causal provider/cache truth.

## 15. Feature packet before coding

For each material feature define purpose, one authority, typed inputs/freshness, output/state, logical parallel vs ordered work, failure semantics, persistence, tests, operator view, research effect, release proof and full affected documentation graph.

For provider/cache features include acquisition failure, last-known-good reuse, expiry, restart, scope/schema mismatch and no-timestamp-laundering cases.

## 16. Test failure loop

```text
reproduce
→ identify violated canonical invariant
→ locate one owner
→ fix root cause
→ add regression
→ focused suite
→ module/integration suite
→ full local verification
→ affected Documents sync
```

Never weaken safety/UNKNOWN semantics just to make tests green.

## 17. Crash / interrupted write

`SUBMITTING` or ambiguous acknowledgement:

```text
DO NOT RESEND
→ restore Intent identity
→ inspect broker positions/orders/deals
→ reconcile exact lifecycle
→ only then allow a new governed Intent
```

Known ManagedTrade disappearance needs exact close proof before clearing/learning.

## 18. Context loss recovery

```text
inspect main HEAD
→ read Documents/README
→ Documentation Standard + Preservation Ledger + explicit Comparison
→ System Contract + Architecture
→ relevant topic + Decisions/Open Questions
→ Module Structure + File/Test Catalog
→ current source/tests/diff
→ latest verified evidence/checkpoint
→ continue first incomplete dependency
```

Repository truth beats remembered chat.

## 19. Completion classification

Use DONE / PARTIAL / MISSING / BROKEN / CALIBRATION PENDING / EXTERNAL PROOF PENDING. Green test count alone never means project complete.

## 20. Verification target once tooling exists

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

Do not claim these pass before actually run on exact revision/environment.

## 21. Next implementation dependency

Implementation begins only after `DOCUMENTATION_AUDIT.md` closes the freeze-preparation metadata/cross-link scan. First dependency is packaging/config/domain/read-only market truth, not MT5 order execution.