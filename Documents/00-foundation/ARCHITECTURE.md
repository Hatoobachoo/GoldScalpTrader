# GoldScalpTrader — Runtime Architecture

**Status:** DRAFT PRE-CHALLENGE ARCHITECTURE CONTRACT
**Version:** 0.1-parallel-serial
**Authority:** System topology, staged analytical parallelism, ordered lifecycle authority, recovery, presentation, persistence and runtime boundaries.

## 1. Purpose

This document explains how the whole runtime fits together. Topic contracts will own detailed market, strategy, risk, execution and research behaviour.

This architecture owns:
- which work can run independently or concurrently;
- which facts are shared;
- where dependencies require ordering;
- where authority becomes strictly serial;
- startup versus normal-cycle behaviour;
- closed/stale/degraded liveness;
- entry versus open-trade management;
- broker-side close recovery;
- verified close → learning ordering;
- persistence/local-backup/restart boundaries;
- per-account/symbol runtime ownership;
- operator presentation boundaries;
- research/AI boundaries.

## 2. Core rule

GoldScalpTrader is a parallel analytical system with a serial authority spine.

Parallel work may improve latency and preserve independent hypotheses. It may not create multiple broker authorities.

## 3. Timeframe model

Final timeframe authority is deliberately pending challenge.

The architecture supports role-based timeframes rather than assuming every timeframe has equal authority.

Candidate roles to challenge:

| Role | Candidate timeframe(s) | Purpose |
|---|---|---|
| broad regime | H1 / M15 | directional/volatility environment |
| scalp location/opportunity | M15 / M5 | fresh structure, liquidity and target room |
| executable setup | M5 | setup geometry and short-horizon structure |
| micro trigger/diagnostic | M1 / tick | fine timing, execution health, microstructure |

No timeframe becomes authority merely because it is faster.

## 4. Meaning of parallel

“Parallel” has two meanings:

1. **logical independence** — specialist desks consume one immutable normalized snapshot without hidden side effects;
2. **bounded production concurrency** — independent intelligence/timeframe work and strategy-family jobs may run concurrently with deterministic semantic output and a one-worker fallback.

Parallelism never applies to broker authority.

## 5. Whole-system topology

```text
MT5 account/symbol/quote/candles/positions/deals
                |
                v
      one immutable MarketSnapshot
                |
                v
   Stage A: core causal intelligence
   structure + indicators + session + cost facts
                |
                v
   Stage B: specialist intelligence
 technical + liquidity/SMC + confluence + news
                |
                v
   Stage C: independent scalp strategy families
                |
                v
 BUY Team <-> SELL Team <-> Red Team/Debate
                |
                v
          Floor Manager
                |
                v
 persistent Opportunity + Entry Timing
                |
                v
       Structural Trade Plan
                |
                v
        Independent Risk
                |
                v
 session/news/system/account/controller authority
                |
                v
   Central ExecutionPermissionGate
                |
                v
   durable one-shot ExecutionIntent
                |
                v
      MT5Writer — sole raw write
                |
                v
         reconciliation
                |
         +------+------+
         |             |
      active        closed
         |             |
 Trade Manager    close receipt
         |             |
         +------> verified learning

Downstream only:
operator dashboards / diagnostics / research / backups
```

## 6. Independent versus ordered lanes

| Lane | Owns | May influence | Must never do |
|---|---|---|---|
| MT5 read | normalized broker facts | all analytical/runtime truth | raw write |
| core intelligence | causal structure/indicators/session/cost context | specialists/strategies | broker permission |
| specialist intelligence | technical/liquidity/news/confluence reports | strategies/plan/management | size/send order |
| strategy families | independent scalp hypotheses | BUY/SELL fusion | risk/write |
| decision floor | debate, directional thesis, Opportunity | timing/plan | broker write |
| Entry Timing | current executable readiness | Trade Plan | monetary sizing |
| Trade Plan | entry/invalidation/objectives/R geometry | Risk | alter account policy |
| Risk | affordability/volume/exposure/risk state | Gate | invent setup |
| permissions/gate | final action permission | Intent | mutate strategy thesis |
| Intent | durable action identity | writer/reconciliation | duplicate send |
| MT5Writer | normalized single broker request | reconciliation | strategy/risk decisions |
| Trade Manager | post-entry management thesis | modify/close pipeline | new-entry thesis |
| Persistence | durable state and lineage | recovery | override broker truth |
| Learning/research | evidence/memory/proposals | governed future policy | production broker authority |
| Dashboard | operator visibility | human understanding | strategy/risk/write authority |
| Local backup | recoverable copies/manifests | restore workflows | live broker authority |

## 7. Startup order

Startup must be ordered before normal opportunity scanning:

1. load validated configuration;
2. initialize diagnostics/logging;
3. open/validate durable state;
4. connect/read MT5;
5. verify account mode/identity and resolved Gold symbol;
6. read current exposure/deals as required;
7. reconcile pending Intents and managed-trade state;
8. recover broker-side closures;
9. rebuild/validate risk-day state;
10. validate session/provider state;
11. mark unresolved required truth UNKNOWN/BLOCKED;
12. only then permit normal new-entry cycles.

A restart never assumes “no position” from missing local state.

## 8. Normal new-entry cycle

```text
fresh snapshot
→ intelligence
→ strategy families
→ BUY/SELL debate
→ Opportunity lifecycle
→ Entry Timing
→ Trade Plan
→ Risk
→ hard permissions
→ central Gate
→ persist Intent
→ writer
→ reconcile
```

If a valid Opportunity exists but the current trigger is not ready, it remains durable rather than being recreated each loop.

## 9. Open-trade cycle

When a bot-owned position exists, the lifecycle focus changes:

```text
fresh broker truth + fresh snapshot
→ reconcile exposure
→ management intelligence
→ Trade Manager
→ action-specific Risk/permission/Gate
→ durable modify/close Intent
→ sole writer
→ reconcile
→ verified close if terminal
```

New-entry logic must respect configured one-position/exposure rules.

## 10. Stale/closed/degraded liveness

The process should stay alive and truthful during recoverable blocks:

- broker market closed;
- stale quote/candles;
- spread too wide;
- no valid opportunity;
- news provider degraded;
- reconciliation pending;
- risk lock/cooldown;
- local-backup warning;
- presentation failure.

These states do not justify guessed PASS values.

## 11. Scalp-specific latency/freshness observability

Architecture should capture timestamps sufficient to measure, where practical:

- snapshot creation age;
- quote age;
- newest evidence knowledge time;
- strategy/decision computation duration;
- Opportunity age;
- Entry Timing trigger age;
- Intent creation time;
- send/ack/reconcile duration.

These metrics are diagnostics/research inputs unless a topic contract explicitly makes one a hard safety threshold.

## 12. Persistence model

Durable state should use a local transactional store such as SQLite unless the challenge identifies a better zero-cost option.

Persistence must make corruption/unknown state explicit rather than silently replacing it with empty defaults.

Checkpoint/restore should prefer creating a verified new copy rather than destructive in-place overwrite.

## 13. Local backup topology

Local backup is deliberately separated from GitHub publication.

```text
repository working tree/.git
        |
        +--> controlled local Git bundle / source snapshot

runtime SQLite/checkpoint/state
        |
        +--> consistent rolling local snapshot

both + manifest/fingerprints
        |
        +--> portable recovery package outside repository
```

Recommended default destination model:

```text
C:\GoldScalpTrader_Backups\
    source\
    runtime\
    recovery-packages\
```

The actual path will be configurable. A second physical disk/USB path may be used for stronger hardware-failure protection without changing trading semantics.

Secrets are not automatically archived.

## 14. Shutdown

Graceful shutdown order should eventually include:

1. stop accepting new entry work;
2. complete/record currently safe local obligations;
3. flush durable state/logs;
4. create a consistent local runtime backup/closure receipt if configured;
5. release controller/runtime resources;
6. terminate.

There is **no automatic GitHub commit or push** in this shutdown path.

## 15. Multi-machine boundary

Initial V1 candidate rule: one production PRIMARY writer per account/symbol scope. Different independent scopes may be allowed on different machines only if state ownership remains unambiguous.

Same-scope simultaneous active writers are not allowed without an explicit distributed coordination design.

Local backup portability supports sequential recovery/handoff, not active-active trading.

## 16. Research and dashboard boundary

Research, learning, terminal dashboard and graphical dashboard are downstream consumers.

They cannot create execution permission. Their failure must not silently grant broker authority.

## 17. Pre-challenge questions

The fresh-zero challenge must explicitly test:
- final timeframe roles;
- whether M1/tick evidence is decision authority or diagnostic only;
- strategy-family count and membership;
- concurrency worker policy;
- runtime backup trigger/retention;
- V1 DEMO/live boundary;
- same-scope handoff method;
- exact latency/freshness hard thresholds versus diagnostic-only metrics.
