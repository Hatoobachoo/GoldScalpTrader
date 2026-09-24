# GoldScalpTrader — Coder Guide

**Status:** DRAFT PRE-CHALLENGE DEVELOPER MANUAL
**Version:** 0.1-full-manual-draft
**Authority:** Developer navigation, phase boundaries, source/test ownership, implementation traces and completion evidence.

## 1. Read this before changing code

GoldScalpTrader is documentation-first. A convenient implementation must not quietly change the product boundary.

This guide answers:

1. What does the feature mean?
2. Where is its one implementation owner?
3. Which work may be parallel and which dependencies/authorities are ordered?
4. Which tests/evidence prove the change?
5. Which other `Documents/` contracts become stale when it changes?

`Documents/` is the only active documentation authority. Topic contracts own behaviour. This guide navigates them; it does not override them.

## 2. Current project stage

Current stage is:

```text
COMPLETE DRAFT MANUAL
→ Fresh-Zero Architecture Challenge
→ synchronize corrections
→ freeze approved contracts
→ then implementation
```

The existing Python scaffold is provisional safety code, not the final architecture.

Do not implement new trading functionality merely because a planned module path appears in this guide.

## 3. Authority reading order

Before a material change read:

1. `README.md` + `GLOSSARY.md`;
2. `00-foundation/SYSTEM_CONTRACT.md`;
3. relevant topic contract;
4. `90-governance/DESIGN_DECISIONS.md` + `OPEN_QUESTIONS.md`;
5. `00-foundation/ARCHITECTURE.md` + `TRADING_FLOOR_ARCHITECTURE.md`;
6. `60-engineering/CODING_STANDARD.md`;
7. `60-engineering/MODULE_STRUCTURE.md`;
8. `60-engineering/FILE_AND_TEST_CATALOG.md`;
9. `90-governance/DOCUMENTATION_STANDARD.md`;
10. current source/tests/diff/evidence.

If these conflict, stop the affected implementation and repair the canonical graph first.

## 4. Architectural spine

```text
one normalized MT5 read boundary
→ immutable MarketSnapshot
→ staged bounded-parallel intelligence
→ independent scalp strategy families
→ independent BUY / SELL fusion + Red Team
→ persistent Opportunity
→ Entry Timing / event freshness
→ family-aware structural TradePlan
→ independent monetary Risk
→ hard session/news/system/account/controller authorities
→ central ExecutionPermissionGate
→ durable one-shot ExecutionIntent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ exactly-once learning
→ research/discovery/promotion
→ local checkpoint/recovery
```

> Parallel analysis, serial financial/broker authority.

## 5. Independent versus ordered work

### May be logically independent / bounded-parallel

- timeframe intelligence whose dependencies are already satisfied;
- specialist technical/liquidity/quant work where snapshot inputs are immutable;
- independent strategy-family evaluations;
- read-only research calculations.

Requirements:

- bounded workers;
- immutable input;
- deterministic canonical result order;
- one-worker semantic parity;
- no persistence/lifecycle mutation inside workers;
- no Risk/Gate/controller/writer authority inside workers.

### Must remain ordered

```text
TradePlan
→ Risk
→ hard permission
→ Gate
→ Intent persisted
→ fresh broker prechecks
→ sole writer
→ reconciliation
```

Verified close precedes learning. Restore precedes broker reconciliation, which precedes new write authority.

## 6. Phase navigation

The canonical phase dependency order lives in `00-foundation/BUILD_PHASES.md`.

Developer shorthand:

```text
1–2 Foundation + read truth
3   Intelligence
4   Strategy / decision floor
5   TradePlan + monetary Risk
6   Session/news + persistence/recovery
7   Execution/controller/reconciliation
8   Trade Manager + close recovery
9   Operator dashboards
10  Research + durable/live learning
11  Local backup / restore / machine handoff
12  Connected external proof + release audits
```

A later phase never hides an incomplete earlier authority.

## 7. Planned source ownership

### Foundation

```text
config/
domain/
diagnostics/
security/
```

### Market truth

```text
market_data/mt5_reader.py
market_data/activity.py
market_data/snapshot.py
```

### Intelligence

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

### Strategies / decisions

```text
strategies/floor.py
strategies/parallel.py
strategies/confluence.py

decisions/fusion.py
decisions/snapshot.py
decisions/opportunity.py
decisions/timing.py
decisions/family_trade_plan.py
decisions/trade_plan.py
```

### Risk / execution

```text
risk/engine.py
risk/state.py
risk/permissions.py

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

### Management / persistence

```text
management/models.py
management/manager.py
management/execution.py
management/store.py

persistence/store.py
persistence/runtime_state.py
persistence/checkpoint.py
persistence/backup.py
persistence/local_recovery_package.py
```

### App / operator

```text
app/main.py
app/runtime.py
app/startup.py
app/recovery.py
app/recovery_mt5.py
app/cycle.py
app/loop.py
app/dashboard.py
app/live_presentation.py
app/session_news.py

operator/*
graphical_dashboard/*
```

### Research

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
research/promotion.py
```

These are planned owners until implementation creates them. Exact tree must stay synchronized with `FILE_AND_TEST_CATALOG.md`.

## 8. Scalping-specific engineering hotspots

### Timeframe authority

Current draft baseline is H1 broad regime, M15 opportunity/location, M5 primary setup/timing, H4 optional, M1 diagnostic.

This is a FIX-BEFORE-BUILD question until Audit 1 finishes. Do not hide M1 authority inside a helper while docs still say diagnostic.

### Freshness

Preserve separate timestamps for:

- bar identity;
- fact confirmation/knowledge time;
- structural/liquidity event time;
- Opportunity/TradePlan creation;
- final analytical decision;
- Intent/precheck/send/reconciliation.

A stale event may remain historically true while no longer being executable entry evidence.

### Transaction cost

Keep distinct:

- chart/gross geometry;
- current Bid/Ask spread;
- approved entry reference;
- actual executable quote;
- actual fill;
- slippage/commission evidence.

Never improve apparent R by silently changing stop/target or double-counting spread.

### Small account / minimum lot

If theoretical volume is below broker minimum, evaluate actual minimum volume against the structural stop and hard Risk policy.

Never tighten stop to make 0.01 fit.

## 9. Pure function rule

Prefer pure deterministic functions for:

- indicator calculations;
- candle/structure derivation;
- technical/liquidity geometry;
- family evaluation;
- fusion;
- TradePlan construction;
- monetary sizing from already-known broker facts;
- replay metrics.

Use stateful classes only where real lifecycle/resources exist: MT5 connection, StateStore, controller, Intent, recovery, runtime loop, Trade Manager.

## 10. UNKNOWN / stale / corrupt rules

Missing truth is typed, not guessed.

Examples:

```text
positions_get == []   → verified zero
positions_get == None → unavailable, not zero
missing News          → UNKNOWN, never CLEAR
future candle time    → CORRUPT
unknown equity        → Risk UNKNOWN
ambiguous send        → reconcile, never resend blindly
```

Policy rejection is a normal typed result, not necessarily an exception.

## 11. Execution safety rule

No irreversible broker path exists until its phase is deliberately implemented.

When it does:

- one sole writer;
- persist Intent before send;
- one send allowance per Intent;
- fresh account/symbol/quote/broker prechecks;
- ambiguous result → reconciliation;
- local state changes only after broker proof;
- stale controller denied;
- REAL requires separate governance decision.

DRY_RUN can exercise upstream semantics but can never fake `ACCEPTED_VERIFIED` broker evidence.

## 12. Persistence and local backup

GoldScalpTrader intentionally has **no trading-runtime Git commit/push feature**.

Durability path:

```text
transactional StateStore
→ rolling local checkpoint
→ graceful-shutdown final local checkpoint
→ portable local recovery package when requested
```

Source history backup is separate:

```text
normal local Git clone
+ optional deliberate local Git bundle at milestones
```

Backups exclude `.env`, broker secrets, PATs/tokens/private keys and credential-bearing URLs.

Restore into a new DB/path, then reconcile fresh broker truth before writes.

## 13. Operator semantics

Presentation is read-only.

Do not confuse:

```text
TradePlan/Risk stopped upstream
→ Gate NOT EVALUATED

actual Gate BLOCK
→ Gate BLOCKED
```

Do not hard-code unresolved thresholds such as Swing's old 1.20R or aggressive risk bands into dashboard wording.

## 14. Research boundary

Research may replay, measure, discover and propose.

It cannot:

- call writer;
- self-promote;
- mutate production code dynamically;
- remove hard safety;
- convert counterfactual R into actual P/L;
- reuse final holdout while tuning.

Scalp research must retain transaction-cost, latency, duration and minimum-lot evidence.

## 15. Feature packet before coding

For each material feature define:

| Part | Required content |
|---|---|
| purpose | user-visible problem/non-goals |
| authority | one topic owner + source owner |
| inputs | types, scope, units, freshness |
| outputs/state | typed result/lifecycle |
| parallel/serial | what may be independent vs ordered |
| failure | stale/UNKNOWN/corrupt/ambiguous |
| persistence | IDs/state/restart/backup |
| tests | positive/negative/chronology/idempotency |
| operator | visible state/reason |
| research | replay/learning/evidence effect |
| release | deterministic vs external proof |
| docs | full affected graph |

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

Never weaken a safety test, replace UNKNOWN with a happy default or delete a regression merely to get green output.

## 17. Crash / interrupted write rule

If previous Intent is `SUBMITTING`/acknowledgement ambiguous:

```text
DO NOT RESEND
→ restore Intent identity
→ query broker positions/orders/deals
→ reconcile exact lifecycle
→ only after prior truth is resolved may another governed Intent exist
```

If known ManagedTrade disappears, require exact ticket/exit role/full-volume close proof before clearing it or learning.

## 18. Context loss / new chat / new developer

Recover project state by repository truth:

```text
inspect main HEAD
→ read Documents/README.md
→ Documentation Standard + Preservation Ledger
→ System Contract + Architecture
→ relevant topic + Decisions/Open Questions
→ Module Structure + File/Test Catalog
→ current source/tests/diff
→ latest verified evidence/checkpoint
→ continue first incomplete dependency
```

Do not restart architecture from memory because chat context was lost.

## 19. Completion classification

Use:

```text
DONE
PARTIAL
MISSING
BROKEN
CALIBRATION PENDING
EXTERNAL PROOF PENDING
```

Green test count alone is never “project complete.”

## 20. Verification target once tooling exists

Expected local verification includes equivalent to:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python -m compileall -q src tests scripts
git diff --check
python scripts/scan_financial_secrets.py .
python scripts/verify_documents_manual.py .
```

Do not claim these pass before they are actually run on the exact revision/environment.

## 21. Change/handoff rule

A finished implementation packet states:

- exact revision;
- what changed;
- canonical owner;
- tests actually run/results;
- affected docs synchronized;
- unresolved calibration/external proof;
- exact next dependency.

Repository truth beats remembered conversation wording.