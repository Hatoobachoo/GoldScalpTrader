# GoldScalpTrader — Release Checklist

**Status:** FINAL RELEASE GATE CHECKLIST — IMPLEMENTATION/DEMO EVIDENCE PENDING
**Version:** 2.0-institutional-scalp
**Authority:** Mandatory pre-release checks for documentation, code, tests, environment, broker lifecycle, recovery, dashboard, research governance and future REAL activation.

## 1. Release principle

A release is not “tests green”. It is a specific revision with synchronized documents/code/tests and the required evidence for its declared capability stage.

Release levels:

```text
DOCUMENTATION FREEZE
IMPLEMENTATION / DRY_RUN RELEASE
CONNECTED DEMO RELEASE
RECOVERY-CERTIFIED DEMO RELEASE
FUTURE REAL RELEASE
```

Each level must be named honestly.

## 2. Documentation gate

- [ ] canonical 66-file manual present;
- [ ] final `01`–`08` folder topology;
- [ ] no broken relative links;
- [ ] no stale 64-file claims;
- [ ] Setup Detector / active-vs-shadow semantics synchronized;
- [ ] M1 subordinate-refinement wording synchronized;
- [ ] News soft-context policy synchronized;
- [ ] preserved Risk table identical across owners/mirrors;
- [ ] graphical dashboard one-screen/no-scroll/functionality contract synchronized;
- [ ] Swing→Scalp comparison and preservation ledger current;
- [ ] Open Questions contains only genuine calibration/external/deferred items;
- [ ] Documentation Audit and Coverage Matrix current.

## 3. Repository/security gate

- [ ] exact release commit SHA recorded;
- [ ] working tree clean for release evidence;
- [ ] no `.env`/credentials/tokens/private keys;
- [ ] no live SQLite/WAL/SHM/runtime checkpoints committed;
- [ ] no backup ZIPs/large generated datasets/models committed accidentally;
- [ ] financial-secret scan PASS;
- [ ] `git diff --check` PASS;
- [ ] no runtime GitHub credential dependency;
- [ ] no required GitHub Actions/Codespaces/LFS/paid cloud dependency.

## 4. Package/config/domain gate

- [ ] installable package exists;
- [ ] settings validation PASS;
- [ ] account/server/symbol policy explicit;
- [ ] active strategy policy/version explicit;
- [ ] preserved Risk policy/version explicit;
- [ ] aggressive mode default disabled;
- [ ] manual daily-loss reset default disabled;
- [ ] all finite enums/reason codes documented/tested;
- [ ] UTC/timezone semantics tested.

## 5. Market-data gate

- [ ] one normalized MT5 read boundary;
- [ ] no analytical raw writer side channel;
- [ ] completed H1/M15/M5 chronology;
- [ ] bounded M1 timing data;
- [ ] optional H4 handled explicitly;
- [ ] quote freshness/future-clock tests;
- [ ] SymbolSpec normalization;
- [ ] positions `[]` vs unavailable `None/error` distinction;
- [ ] current connected intended-account/symbol proof at connected release level.

## 6. Intelligence / setup detection gate

- [ ] candle/structure no-lookahead tests;
- [ ] technical/liquidity/FVG/OB causal lifecycle tests;
- [ ] indicators/ATR/EMA/RSI chronology;
- [ ] session soft context tested;
- [ ] News soft-context behavior tested;
- [ ] all six family setup detectors implemented;
- [ ] `NONE` when no setup qualifies;
- [ ] active family cannot force a setup;
- [ ] multiple candidates preserve independent lineage;
- [ ] optional confluence not universalized.

## 7. Strategy Isolation gate

- [ ] exactly one `ACTIVE_EXECUTION` policy;
- [ ] exactly five `SHADOW_ONLY` preserved families;
- [ ] shadow cannot create production Opportunity/Intent;
- [ ] active-family switch versioned;
- [ ] historical attribution immutable;
- [ ] active/shadow state survives restart;
- [ ] family efficiency research receives actual vs shadow evidence separately.

## 8. Timing / TradePlan / quality gate

- [ ] M5 required before production Opportunity;
- [ ] M1 cannot create Opportunity alone;
- [ ] M1 READY/WAIT/MISSED/INVALID tests;
- [ ] event-age/chase/drift semantics;
- [ ] fresh-event-only re-arm;
- [ ] family-aware invalidation;
- [ ] Breakout Retest and reversal-event geometry tests;
- [ ] structural stop not rewritten for affordability;
- [ ] no hard inherited 1.20R dependency;
- [ ] emergency spread;
- [ ] spread/SL;
- [ ] spread/target;
- [ ] cost/reward;
- [ ] slippage allowance/deviation policy;
- [ ] latency revalidation;
- [ ] no cost double counting.

## 9. Risk gate

- [ ] exact SMALL/MEDIUM/NORMAL profile boundaries;
- [ ] exact documented target/elevated/hard/daily values;
- [ ] fixed profile through UTC risk day;
- [ ] dynamic broker-aware volume;
- [ ] min-lot actual risk;
- [ ] margin state;
- [ ] no stop distortion;
- [ ] aggressive mode default disabled;
- [ ] exact 8%/16% aggressive semantics;
- [ ] manual reset default disabled;
- [ ] one fresh same-episode re-entry;
- [ ] 3-loss / at-least-30m cooldown;
- [ ] Account Safety P/L/cash-flow separation;
- [ ] capacity/unknown exposure behavior;
- [ ] restart persistence.

## 10. Session / News gate

Hard session:

- [ ] OPEN/PRE_CLOSE/CLOSED/UNKNOWN;
- [ ] daily T-20/T-10 baseline;
- [ ] weekend T-60/T-30 baseline;
- [ ] reopen rules;
- [ ] connected current Exness schedule proof before applicable connected release.

News/context:

- [ ] no News hard entry block;
- [ ] provider unavailable/stale does not directly block;
- [ ] no News cooldown;
- [ ] no post-News warmup;
- [ ] stale cache not relabelled fresh;
- [ ] 1800s context baseline preserved/documented;
- [ ] event tags flow to dashboard/research.

## 11. Execution gate

- [ ] upstream blocker vs Gate state correct;
- [ ] controller holder/epoch required;
- [ ] persist Intent before send;
- [ ] precheck/order_check before writer;
- [ ] precheck failure send count 0;
- [ ] SUBMITTING persisted before raw write;
- [ ] one Intent ≤ one irreversible request;
- [ ] only `mt5_writer.py` raw write boundary;
- [ ] broker reject classified;
- [ ] ambiguous acknowledgement → reconciliation;
- [ ] no blind retry;
- [ ] OPEN/MODIFY/CLOSE reconciliation;
- [ ] manual/foreign exposure ownership separation;
- [ ] connected DEMO lifecycle proof for DEMO release.

## 12. Management gate

- [ ] HOLD/PROTECT/TRAIL/RUNNER/EXIT;
- [ ] no stop widening;
- [ ] time-efficiency EXIT;
- [ ] Runner requires fresh objective/evidence;
- [ ] partial management broker-valid only;
- [ ] 0.01-lot correctness without partial close;
- [ ] PRE_CLOSE flatten through governed execution;
- [ ] exact manual/broker known-trade close recovery;
- [ ] verified close before final learning.

## 13. Persistence / recovery gate

- [ ] strict StateStore schema/types;
- [ ] corruption fails closed;
- [ ] checkpoint hashes/integrity;
- [ ] restore into new path;
- [ ] active family policy preserved;
- [ ] Risk/cooldown/re-entry preserved;
- [ ] unresolved Intent recovery;
- [ ] ManagedTrade reconciliation;
- [ ] close queue/receipt exactly-once flow;
- [ ] candidate/promotion state preserved;
- [ ] no runtime Git operation;
- [ ] sequential same-scope machine handoff drill for recovery-certified release.

## 14. Dashboard gate

- [ ] primary graphical layout is one screen/no scrollbar at approved target desktop geometry;
- [ ] central chart rendered;
- [ ] M1/M5/M15/H1/H4 buttons functional;
- [ ] Indicators functional;
- [ ] Drawings functional;
- [ ] Settings functional within UI authority;
- [ ] Detected Setup displayed separately from Active Test Family;
- [ ] shadow setup clearly labelled research only;
- [ ] exact signal/reason/blocker;
- [ ] Gate NOT_EVALUATED vs BLOCKED truthful;
- [ ] TradePlan/Risk/execution/activity/learning/system/verified closes visible;
- [ ] dashboard cannot mutate trading authority.

## 15. Learning / research gate

- [ ] verified actual learning exactly once;
- [ ] active/shadow/missed/blocked/fault evidence separated;
- [ ] replay no-lookahead including M1;
- [ ] one-position capacity replay;
- [ ] cost/slippage/latency assumptions explicit;
- [ ] final holdout one-shot;
- [ ] stress/ablation;
- [ ] autonomous strategy invention bounded/declarative;
- [ ] advanced ML evidence identity;
- [ ] candidate stage transitions evidence-bound;
- [ ] production transition requires explicit operator approval;
- [ ] research has zero raw broker authority.

## 16. Performance gate

- [ ] stage latency telemetry implemented;
- [ ] no unnecessary repeated MT5/indicator calculations;
- [ ] one-worker deterministic baseline measured;
- [ ] bounded parallelism enabled only where profiling justifies it;
- [ ] parallel semantic parity proven when enabled;
- [ ] dashboard rendering does not materially block strategy critical path.

## 17. DRY_RUN release evidence

At minimum:

- [ ] full pipeline reaches pre-writer stop;
- [ ] no irreversible MT5 call possible;
- [ ] setup detector/isolation behavior visible;
- [ ] all exact blockers/reasons visible;
- [ ] shadow evidence recorded correctly;
- [ ] state/restart behavior proven locally.

## 18. DEMO release evidence

At minimum controlled proof of:

- [ ] intended account/server/symbol;
- [ ] actual SymbolSpec;
- [ ] OPEN;
- [ ] fill/slippage/deviation;
- [ ] MODIFY/protect/trail;
- [ ] TP/SL or broker-side close visibility;
- [ ] governed CLOSE;
- [ ] manual known-trade close attribution;
- [ ] restart/reconciliation;
- [ ] one-shot behavior/no duplicate;
- [ ] after-cost learning record;
- [ ] current broker schedule behavior.

## 19. Future REAL gate

REAL remains unavailable until a separate final release packet includes sufficient DEMO/recovery evidence, calibrated cost/latency, stable documented Risk behavior, security proof and **explicit operator approval**.

No environment variable/UI click alone may enable it.

## 20. Release verdict

Final verdict must be one of:

```text
PASS FOR DECLARED CAPABILITY
PASS WITH NON-BLOCKING EVIDENCE PENDING
BLOCKED
NOT RUN
```

Every exception is listed with owner, impact and evidence—not hidden in prose.
