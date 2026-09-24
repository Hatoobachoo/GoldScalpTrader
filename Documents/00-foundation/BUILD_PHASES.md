# GoldScalpTrader — Build Phases

**Status:** DRAFT PRE-CHALLENGE BUILD MODEL
**Version:** 0.1-dependency-order
**Authority:** Dependency order, phase ownership, evidence order and universal exit gates.

## 1. Why phases exist

Phases define dependency and evidence order. They are not a progress diary and they do not allow a later feature to hide an incomplete earlier authority.

```text
1–2 Foundation + broker reads
→ 3 Market intelligence
→ 4 Strategy + decisions
→ 5 Trade Plan + monetary risk
→ 6 Session/news + persistence/recovery
→ 7 Execution + controller
→ 8 Trade Manager + close recovery
→ 9 Operator dashboards
→ 10 Research + durable/live learning
→ 11 Local backup + recovery drills + multi-machine boundaries
→ 12 Full compliance/challenge/release audits
```

Documentation for the complete intended surface is created and challenged before implementation begins. During implementation, each phase still requires its own synchronized source/test/document packet.

## 2. Universal phase exit gate

A phase is not complete merely because code exists.

Before a phase can be called implemented:

1. authoritative topic contract is current;
2. upstream/downstream contracts were checked for affected-graph impact;
3. source ownership is explicit;
4. failure/UNKNOWN behaviour is explicit;
5. persistence/restart consequence is explicit where relevant;
6. operator/dashboard consequence is explicit where relevant;
7. research/replay consequence is explicit where relevant;
8. deterministic tests prove the software contract;
9. external/calibration evidence is classified rather than guessed;
10. file/test catalogs and coder/build guides are synchronized.

## 3. Phase 1 — Product, domain and configuration

Owns:
- project identity and trading personality;
- typed IDs/enums/statuses;
- configuration loading/validation;
- runtime modes;
- policy/schema identity;
- secret-handling boundary;
- local-only default execution environment.

Must prove:
- unsafe/unknown configuration fails closed;
- secrets are never committed/logged;
- runtime mode cannot silently become broker-write authority.

## 4. Phase 2 — MT5 read boundary and normalized snapshot

Owns:
- MT5 initialization/readiness;
- account identity;
- broker-resolved Gold symbol;
- SymbolSpec;
- Bid/Ask/quote timestamp/spread;
- completed candle series and any separately typed live/tick facts later approved;
- positions/deals/current exposure;
- one immutable MarketSnapshot.

Must prove:
- no hidden strategy-side MT5 reads;
- chronology/freshness checks;
- broker specification normalization;
- market-closed/stale states remain truthful.

## 5. Phase 3 — Market intelligence

Owns staged analytical reports such as:
- candle/structure;
- indicators/volatility;
- technical levels/location;
- liquidity/SMC;
- session context;
- fundamental/news intelligence;
- optional confluence such as Fibonacci/trendline/volume POC where retained.

Parallelism may be introduced only after serial semantic parity is proved.

Scalp-specific emphasis:
- event freshness;
- short-horizon structure;
- cost/volatility context;
- causal timestamps;
- no-lookahead.

## 6. Phase 4 — Strategy floor and decision fusion

Owns:
- independent production scalp strategy families;
- strategy-family attribution;
- bounded parallel evaluation;
- independent BUY/SELL teams;
- Debate/Red Team challenge;
- Floor Manager / DecisionBoard;
- persistent Opportunity identity/lifecycle;
- entry-timing states including WAIT/MISSED/ENTER/re-arm semantics.

Exact scalp families and timeframe roles remain pre-challenge decisions until frozen.

## 7. Phase 5 — Trade Plan and monetary risk

Trade Plan owns:
- executable entry reference;
- family-aware structural invalidation;
- initial SL;
- objective hierarchy;
- target/path quality;
- original R;
- late/cost-invalid geometry classification.

Risk owns:
- per-trade monetary risk;
- broker-aware lot sizing;
- minimum-lot affordability;
- margin/exposure limits;
- daily safety P/L;
- loss lock/cooldown/profile policy;
- independent PASS/BLOCK/UNKNOWN result.

Risk cannot repair bad strategy geometry.

## 8. Phase 6 — Session/news, persistence and restart

Owns:
- broker/session schedule states;
- known news blackout truth;
- adaptive provider-health semantics;
- risk/system state machine;
- durable state store/events/checksums;
- startup reconciliation;
- checkpoint/restore;
- rolling local runtime backups.

No GitHub push is part of shutdown/recovery.

## 9. Phase 7 — Execution and controller

Owns:
- DEMO/live-mode policy as finally approved;
- account/symbol/controller identity;
- central ExecutionPermissionGate;
- action-sensitive OPEN/MODIFY/CLOSE permission;
- durable ExecutionIntent;
- one-shot submission;
- sole MT5Writer;
- request normalization;
- acceptance/timeout uncertainty handling;
- reconciliation.

Broker writes remain serial.

## 10. Phase 8 — Trade Manager and verified close

Owns:
- HOLD/PROTECT/TRAIL/RUNNER/EXIT states where retained;
- scalp-specific time stop/momentum failure/micro-structure exit semantics;
- monotonic protection rules;
- broker-side SL/TP/manual-close recovery;
- closure receipt;
- managed-trade retirement;
- downstream verified learning handoff.

## 11. Phase 9 — Operator surfaces

Owns:
- primary VS Code/terminal dashboard;
- responsive narrow/wide rendering;
- human-readable reason mapping;
- system health/diagnostics;
- optional local graphical dashboard.

All operator surfaces remain read-only and must not become dependencies of trading liveness.

## 12. Phase 10 — Research and learning

Owns:
- chronological replay;
- portable verified datasets;
- cost-aware scalp simulation;
- holdout/stress/walk-forward evidence;
- StrategyMemory;
- actual trade learning;
- missed/blocked/counterfactual episodes where evidence quality allows;
- governed strategy discovery;
- autonomous hypothesis invention;
- champion/challenger promotion and rollback.

Research never grants broker authority.

## 13. Phase 11 — Local backup and recovery drills

Owns:
- local source/history backup mechanism;
- runtime-state snapshot packaging;
- manifest/fingerprints/checksums;
- retention policy;
- restore-to-new-location drills;
- optional second-drive/USB destination support;
- sequential laptop handoff rules if retained.

Target backup layers:

```text
working Git clone
+ local Git history
+ rolling runtime-state backups outside repo
+ portable recovery package / Git bundle at controlled milestones
```

Automatic archives exclude secrets.

Graceful shutdown may write a local runtime backup but never auto-pushes GitHub.

## 14. Phase 12 — Challenge, compliance and release evidence

Owns:
- fresh-from-zero architecture audit;
- Documents → Code → Tests/evidence compliance;
- Gate/presentation truth audits;
- scalp-specific no-trade/over-trade/freshness/cost audits;
- individual component review;
- final release checklist;
- final release audit for one exact revision/config/environment.

## 15. Parallelism introduction rule

Do not add concurrency because it sounds faster.

For each parallel stage:

1. prove serial semantics first;
2. identify immutable shared inputs;
3. prohibit hidden side effects;
4. bound worker count;
5. make result ordering deterministic;
6. preserve one-worker fallback;
7. prove serial/parallel parity in tests;
8. keep all broker authority outside analytical worker pools.

## 16. Pre-challenge status

This phase map preserves the GoldSwingTraderAI engineering sequence but adds stronger explicit scalp-cost/freshness and local-backup emphasis.

The challenge phase may adjust phase contents, but dependency direction and hard-authority seriality require an explicit governance decision to change.
