# GoldScalpTrader — Runtime Architecture

**Status:** FROZEN V1 ARCHITECTURE — CALIBRATION / CONNECTED DEMO PROOF PENDING
**Version:** 1.0-post-fresh-zero
**Authority:** System topology, logical analytical parallelism, ordered lifecycle authority, recovery, presentation, persistence and runtime boundaries.

## 1. Core rule

GoldScalpTrader is a **logically parallel analytical system with a strictly serial financial/broker authority spine**.

Logical specialist independence is mandatory. Physical concurrent workers are optional/profiling-driven. A deterministic one-worker path is always valid and must produce the same semantic outputs as any bounded-parallel implementation.

## 2. Frozen timeframe model

| Role | V1 timeframe | Authority |
|---|---|---|
| broad regime | H1 | soft directional/volatility context |
| optional major context | H4 | soft/optional, never universal scalp veto |
| opportunity/location/path | M15 | structural/liquidity/session context |
| primary setup/timing/management | M5 | completed-bar production authority |
| micro diagnostics/research | M1 | no production decision authority |
| executable current market | quote/tick | Bid/Ask/spread/drift/freshness, not structural-history authority |

## 3. Whole-system topology

```text
MT5 account/symbol/quote/candles/positions/deals
                ↓
      one immutable MarketSnapshot
                ↓
   core causal intelligence
 structure + indicators + session + cost facts
                ↓
   specialist intelligence
 technical + liquidity/SMC + confluence + news
                ↓
 six independent scalp family hypotheses
                ↓
 BUY Team ↔ SELL Team ↔ Red Team/Debate
                ↓
          Floor Manager
                ↓
 persistent Opportunity + completed-M5 Entry Timing
                ↓
 family-aware structural TradePlan
 + gross / cost-adjusted room truth
                ↓
        independent monetary Risk
                ↓
 session/news/system/account/controller authority
                ↓
   central ExecutionPermissionGate
                ↓
   durable one-shot ExecutionIntent
                ↓
      MT5Writer — sole raw write
                ↓
         reconciliation
          ↙            ↘
      active           closed
        ↓                ↓
 Trade Manager      close receipt/queue
        └──────────────→ verified learning

Downstream/read-only:
operator dashboards / diagnostics / research / local backups
```

## 4. Independent versus ordered lanes

| Lane | Owns | Must never do |
|---|---|---|
| MT5 read | normalized broker/account/symbol/quote/candle/position/deal facts | raw write |
| intelligence | causal structure/quant/technical/liquidity/session/news/cost context | broker permission |
| strategy families | six independent scalp hypotheses | risk sizing/write |
| fusion / Opportunity | BUY/SELL debate, thesis identity | broker write |
| Entry Timing | completed-M5 executable readiness/freshness | monetary sizing |
| TradePlan | entry/invalidation/objectives/gross+cost-room geometry | alter account policy |
| Risk | affordability/normalized volume/exposure/risk-day state | invent setup |
| permissions/Gate | action-specific final permission | mutate strategy thesis |
| Intent | durable one-shot action identity | duplicate send |
| MT5Writer | one normalized broker request | strategy/risk decisions |
| reconciliation | current broker outcome | guess success |
| Trade Manager | post-entry management thesis | create a new entry thesis |
| Persistence | durable state/lineage | override broker truth |
| Learning/research | evidence/memory/proposals | production broker authority |
| Dashboard | operator visibility | recalculate permission |
| Local backup | recoverable state/source copies | live broker authority |

## 5. Parallelism rule

Specialist/timeframe/family computations may run concurrently **only** when dependencies are already satisfied and inputs are immutable.

Requirements:

- bounded resources;
- deterministic canonical output ordering;
- no worker lifecycle mutation;
- no persistence/broker writes inside analytical workers;
- one-worker parity tests;
- actual concurrency enabled only if profiling demonstrates benefit.

Broker authority never runs as competing parallel writers.

## 6. Startup order

1. load validated configuration;
2. initialize diagnostics/logging;
3. open/validate durable state;
4. connect/read MT5;
5. verify account/server and resolved Gold symbol;
6. read exposure/deals as required;
7. reconcile pending Intents/ManagedTrade;
8. recover broker-side closures;
9. rebuild/validate risk-day state;
10. validate session/news provider state;
11. acquire/validate controller authority for write-capable mode;
12. mark unresolved required truth UNKNOWN/BLOCKED;
13. only then permit normal new-entry cycles.

Restart never assumes flat exposure because local state is absent.

## 7. New-entry cycle

```text
fresh snapshot
→ intelligence
→ six family reports
→ BUY/SELL debate
→ persistent Opportunity
→ completed-M5 timing / event freshness
→ TradePlan gross + cost-room geometry
→ STANDARD monetary Risk
→ session/news + hard authorities
→ central Gate
→ persist Intent
→ fresh pre-submit broker checks
→ sole writer
→ reconcile
```

A strong Opportunity can remain WAITING while entry timing improves.

## 8. Open-trade cycle

```text
fresh broker truth + snapshot
→ reconcile exposure
→ management intelligence
→ HOLD / PROTECT / TRAIL / RUNNER / EXIT
→ action-specific hard authorities
→ durable MODIFY/CLOSE Intent
→ sole writer
→ reconcile
→ verified close when terminal
```

Time/efficiency can be an EXIT reason. There is no separate TIME_EXIT action in V1.

## 9. News / session architecture

Market schedule and News are separate authorities.

For new entry:

```text
OPEN + NEWS_CLEAR    → may proceed
OPEN + NEWS_BLACKOUT → BLOCK
OPEN + NEWS_UNKNOWN  → BLOCK / LIMITED
CLOSED/PRE_CLOSE/WARMUP/SESSION_UNKNOWN → BLOCK/UNKNOWN as owned by policy
```

Existing-position management remains action-sensitive; News UNKNOWN does not trap risk or fabricate CLEAR.

## 10. Cost / freshness architecture

Scalping requires explicit observability of:

- quote age;
- newest evidence knowledge time;
- event/trigger age;
- Opportunity age;
- approved-entry drift;
- current spread;
- remaining target room;
- analytical/Intent/send/reconcile duration.

TradePlan retains gross and cost-adjusted planning truth. Execution owns final fresh Bid/Ask/spread/drift recheck. Costs are never double counted and geometry is never rewritten merely to pass a threshold.

## 11. Persistence / recovery

V1 uses local transactional SQLite unless implementation proof discovers a blocking issue.

Corruption/unknown state is explicit, not silently replaced by empty defaults. Checkpoint/restore writes a verified new copy rather than destructive in-place overwrite where practical.

Current broker truth outranks restored local context.

## 12. Runtime local backup

```text
transactional StateStore
→ rolling local checkpoint
→ graceful-shutdown final verified local checkpoint
→ optional portable runtime recovery package outside repo
```

Secrets are excluded. Safe shutdown/local checkpoint does not depend on GitHub/network.

## 13. Development/source backup

Normal low-GitHub-use workflow:

```text
one coherent remote bulk commit
→ operator git pull --ff-only
→ local clone has complete source + Git history
→ optional secret-clean ZIP snapshot after major milestone
```

Git bundle is optional advanced/manual tooling only. Trading runtime never commits, pushes or pulls Git.

## 14. Shutdown

1. stop accepting new entry work;
2. complete/record safe current obligations;
3. persist/flush durable state;
4. release write/controller authority safely;
5. shut down MT5 resources;
6. create final verified **local** checkpoint/catalog result;
7. terminate/report explicit success/failure.

There is no automatic GitHub publication path.

## 15. Multi-machine boundary

One production PRIMARY writer per account/symbol scope. Different independent scopes may run separately. Same-scope simultaneous writers are unsupported.

Sequential movement requires old stop → verified checkpoint/package → new DB restore → fresh broker reconciliation → controller acquisition → READY.

## 16. Runtime modes

```text
READINESS  read-only diagnostic
DRY_RUN    full governed analytical lifecycle with zero irreversible broker writes
PRIMARY    later controlled DEMO writer after implementation/evidence gates
REAL       deferred V1 / separate future governance
```

## 17. Research / dashboard boundary

Research, learning, terminal dashboard and browser dashboard are downstream. They cannot create execution permission. Their failure must never silently grant broker authority.

## 18. Remaining calibration / external proof

Calibration: family thresholds, gross/net target quality, event freshness, spread/drift, risk values, session/news timing, time-efficiency exit, runner rules and worker count.

External proof: real Exness SymbolSpec/schedule/order metadata, DEMO execution/reconciliation, spread/slippage/latency, broker-side close recovery and fresh-machine restore.