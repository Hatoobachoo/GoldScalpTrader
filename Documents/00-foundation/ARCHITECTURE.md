# GoldScalpTrader — Runtime Architecture

**Status:** FROZEN V1 ARCHITECTURE — PRESERVATION-FIRST CORRECTION / CONNECTED PROOF PENDING
**Version:** 1.1-preserved-parallel-risk-features
**Authority:** System topology, bounded analytical concurrency, ordered lifecycle authority, recovery, presentation, persistence and runtime capability boundaries.

## 1. Core rule

GoldScalpTrader is a **bounded-parallel analytical system with a strictly serial financial/broker authority spine**.

GoldSwingTraderAI remains the default architecture/feature baseline. A feature is not removed merely because the Scalp implementation could be simpler.

Bounded physical concurrency for dependency-independent desks/families is preserved as a target capability. A deterministic one-worker path remains mandatory for fallback/testing and must produce the same semantic result.

## 2. Scalp timeframe model

| Role | Timeframe | Authority |
|---|---|---|
| broad regime | H1 | soft directional/volatility context |
| optional major context | H4 | soft/optional, never universal scalp veto |
| opportunity/location/path | M15 | structural/liquidity/session context |
| primary setup/timing/management | M5 | completed-bar production authority |
| micro diagnostics/research | M1 | no independent production trigger authority |
| executable current market | quote/tick | Bid/Ask/spread/drift/freshness, not structural-history authority |

## 3. Whole-system topology

```text
MT5 account/symbol/quote/candles/positions/deals
                ↓
      one immutable MarketSnapshot
                ↓
       causal core intelligence
                ↓
 dependency-independent specialist desks
       bounded-parallel where applicable
                ↓
 six independent scalp family hypotheses
       bounded-parallel where applicable
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
 profiled monetary Risk
 SMALL / MEDIUM / NORMAL
 + optional explicit aggressive overlay
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
```

Dashboard/research/backup remain downstream and cannot create broker permission.

## 4. Independent versus ordered lanes

| Lane | Owns | Must never do |
|---|---|---|
| MT5 read | normalized broker/account/symbol/quote/candle/position/deal facts | raw write |
| intelligence | causal structure/quant/technical/liquidity/session/news/cost context | broker permission |
| strategy families | six independent scalp hypotheses | monetary sizing/write |
| fusion / Opportunity | BUY/SELL debate, thesis identity | broker write |
| Entry Timing | completed-M5 executable readiness/freshness | monetary sizing |
| TradePlan | entry/invalidation/objectives/gross+cost-room geometry | alter monetary policy |
| Risk | profile/overlay affordability, volume, exposure, risk-day state | invent setup |
| permissions/Gate | action-specific final permission | mutate strategy thesis |
| Intent | durable one-shot action identity | duplicate send |
| MT5Writer | one normalized broker request | strategy/risk decisions |
| reconciliation | current broker outcome | guess success |
| Trade Manager | post-entry management thesis | create a new entry thesis |
| Persistence | durable state/lineage | override broker truth |
| Learning/research | evidence/memory/proposals | production broker authority |
| Dashboard | operator visibility | recalculate permission/policy |
| Local backup | recoverable state/source copies | live broker authority |

## 5. Preserved bounded analytical concurrency

Dependency-independent desks/families may execute concurrently after their inputs are ready.

Requirements:

- immutable common input;
- bounded worker count/resources;
- dependency-aware staging;
- deterministic canonical result order;
- no worker persistence, Risk, lifecycle or broker mutation;
- explicit worker failure/degradation;
- deterministic one-worker fallback;
- parity tests between one-worker and bounded-parallel paths.

Worker count may be tuned by profiling, but the bounded-parallel capability itself is not removed as a non-scalp simplification.

Broker/financial authority never runs as competing writers.

## 6. Startup order

1. load validated configuration/policy identities;
2. initialize diagnostics/logging;
3. open/validate durable state;
4. connect/read MT5;
5. verify account/server/resolved Gold symbol;
6. read exposure/deals as required;
7. reconcile pending Intents/ManagedTrade;
8. recover broker-side closures;
9. rebuild/validate risk-day profile/overlay state;
10. validate session/news provider + LKG cache;
11. acquire/validate controller authority for write-capable mode;
12. mark unresolved required truth UNKNOWN/BLOCKED;
13. only then permit normal new-entry cycles.

Restart never assumes flat exposure because local state is absent.

## 7. New-entry cycle

```text
fresh snapshot
→ staged bounded-parallel intelligence
→ six family reports
→ BUY/SELL debate
→ persistent Opportunity
→ completed-M5 timing / event freshness
→ TradePlan gross + cost-room geometry
→ SMALL/MEDIUM/NORMAL Risk
   + optional explicit aggressive overlay
→ session/news + hard authorities
→ central Gate
→ persist Intent
→ fresh pre-submit broker checks
→ sole writer
→ reconcile
```

## 8. Open-trade cycle

```text
fresh broker truth + snapshot
→ reconcile exposure
→ management intelligence
→ HOLD / PROTECT / TRAIL / RUNNER / EXIT
→ optional broker-valid partial management where divisible
→ action-specific hard authorities
→ durable MODIFY/CLOSE Intent
→ sole writer
→ reconcile
→ verified close when terminal
```

Time/efficiency can be a scalp-specific EXIT reason. Runner is exceptional.

## 9. Risk architecture

Profile resolved once from positive DayStartEquity per UTC risk day:

```text
SMALL < $300
MEDIUM $300–$999.99
NORMAL >= $1,000
```

Reference target/elevated/hard/daily bands remain canonical through `RISK_CONTRACT.md`.

`AGGRESSIVE_SMALL_ACCOUNT` is a preserved explicit option, disabled by default:

```text
8% max monetary SL risk per trade — not target
16% max aggregate open risk
16% daily loss ceiling
```

## 10. News / session architecture

Market schedule and News remain separate authorities.

```text
OPEN + NEWS_CLEAR       → may proceed
OPEN + NEWS_BLACKOUT    → BLOCK
OPEN + NEWS_UNKNOWN     → new-entry BLOCK / LIMITED
```

A refresh failure with still-valid accepted LKG cache keeps that cached News truth. Failed acquisition never refreshes cache timestamps/validity.

Preserved baselines:

```text
Provider TTL 1800s
Daily   T-20 no-entry / T-10 flatten
Weekend T-60 no-entry / T-30 flatten
Daily reopen   1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

Actual broker schedule/DST/holiday facts remain external proof.

## 11. Cost / freshness architecture

Scalping explicitly observes quote age, event age, Opportunity age, entry drift, spread, target room and decision/send/reconcile latency.

TradePlan retains gross and cost-adjusted planning truth. Execution owns final fresh quote/spread/drift recheck. Costs are never double counted and geometry is never rewritten merely to pass a threshold.

## 12. Persistence / recovery

V1 uses local transactional SQLite unless implementation proof discovers a blocking issue.

Corruption/unknown state is explicit, not silently replaced with empty defaults. Current broker truth outranks restored context.

## 13. Runtime local backup

```text
transactional StateStore
→ rolling local checkpoint
→ graceful-shutdown final verified local checkpoint
→ optional portable runtime recovery package outside repo
```

Safe shutdown/local checkpoint does not depend on GitHub/network.

## 14. Development/source backup

```text
one coherent remote bulk commit
→ operator git pull --ff-only
→ local clone has complete source + Git history
→ optional secret-clean ZIP milestone copy
```

Trading runtime never commits, pushes or pulls Git.

## 15. Multi-machine boundary

One PRIMARY writer per account/symbol scope. Different independent scopes may run separately. Same-scope simultaneous writers are unsupported without a future deliberate shared-fencing architecture.

## 16. Runtime capability stages

```text
READINESS  read-only diagnostic
DRY_RUN    governed analytical lifecycle with zero irreversible writes
PRIMARY    controlled DEMO writer after implementation/evidence gates
REAL       preserved future governed capability; disabled until DEMO/release/explicit approval gate
```

REAL is not removed and is not a hidden configuration shortcut.

## 17. Research / dashboard boundary

Research, learning, terminal dashboard and browser dashboard are downstream. They cannot create execution permission or silently select/change Risk profile/overlay.

## 18. Evidence pending

Scalp calibration: gross/net target quality, event freshness, spread/drift, time-efficiency, runner rules and latency thresholds.

Implementation/performance: worker count while preserving bounded-parallel capability.

External proof: current Exness SymbolSpec/schedule/order metadata, DEMO execution/reconciliation, spread/slippage/latency, close recovery and fresh-machine restore.