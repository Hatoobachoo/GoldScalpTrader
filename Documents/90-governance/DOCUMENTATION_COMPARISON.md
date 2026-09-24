# GoldScalpTrader — GoldSwingTraderAI versus GoldScalpTrader Explicit Change Record

**Status:** POST-AUDIT-1 EXPLICIT REFERENCE COMPARISON — ACTIVE
**Version:** 1.0-explicit-swing-to-scalp-delta
**Authority:** Permanent record of what is intentionally preserved, changed, removed, added, recalibrated or deferred relative to the GoldSwingTraderAI reference.

## 1. Purpose

GoldSwingTraderAI is the reference architecture/preservation source. GoldScalpTrader is a separate scalp product.

```text
GoldSwingTraderAI Documents/ → reference meaning and engineering lessons
GoldScalpTrader Documents/   → sole current authority for this project
```

This file exists so the project never depends on chat memory for the question:

> Exactly what did we change from SwingTrader, and why?

## 2. What is preserved substantially as-is

The following reference architecture remains because Fresh-Zero Audit 1 found it sound for scalping:

- documentation-first governance and affected-graph synchronization;
- one normalized MT5 read boundary;
- immutable shared MarketSnapshot;
- causal completed-candle chronology / no lookahead;
- specialist intelligence desks;
- independent strategy-family hypotheses;
- independent BUY and SELL theses + Red Team/Floor Manager;
- persistent Opportunity distinct from current entry timing;
- structural TradePlan before monetary Risk;
- Risk as independent hard authority;
- hard session/system/account/exposure/controller separation;
- central execution Gate;
- persist-before-send one-shot Intent;
- sole MT5Writer;
- ambiguous acknowledgement → reconciliation, never blind retry;
- bot/manual/foreign ownership separation;
- ManagedTrade lifecycle and verified-close evidence;
- restart/persistence discipline;
- downstream learning/research with no broker authority;
- governed discovery/invention/promotion;
- read-only dashboard authority;
- local single PRIMARY per account/symbol scope;
- evidence separation between deterministic tests, replay, connected DEMO and profitability.

## 3. Explicit changes from Swing to Scalp

| # | Area | GoldSwingTraderAI reference | GoldScalpTrader V1 decision | Change class / reason |
|---:|---|---|---|---|
| 1 | Product horizon | meaningful intraday/swing/open-session move | selective short-duration Gold scalp | **CHANGED** product personality |
| 2 | Broad timeframe | H4 strong broad regime role | H1 broad soft regime; H4 optional context only | **CHANGED** to avoid swingifying every scalp |
| 3 | Opportunity/timeframe chain | H4 → H1 → M15 → M5 | H1 → M15 → M5, with H4 optional | **CHANGED** shorter hierarchy |
| 4 | M1 role | diagnostic-only reference role | diagnostic/research-only V1 | **KEPT** after explicit challenge, not blind copy |
| 5 | Tick history | not required production thesis authority | outside V1; quote/tick current condition only | **DEFERRED/SIMPLIFIED** |
| 6 | Strategy families | six: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal, Compression Expansion | same six retained | **KEPT** after fresh-zero review; overlap now explicitly correlation-bounded |
| 7 | Event freshness | important after Swing audits | first-class scalp entry contract with family/event age, chase distance and stale-for-entry semantics | **STRENGTHENED/ADDED emphasis** |
| 8 | Cost sensitivity | material execution consideration | gross geometry **plus explicit cost-adjusted room** before Risk/execution | **STRENGTHENED** because small scalp targets are cost-sensitive |
| 9 | Structural RR | Swing Primary hard floor included 1.20R baseline/policy | 1.20R not inherited; exact gross/net/cost-room floors calibrate for scalp | **REMOVED as inherited threshold** |
| 10 | Risk model | automatic SMALL/MEDIUM/NORMAL equity profiles with profile-specific bands | one explicit `STANDARD` production policy | **SIMPLIFIED/CHANGED**; actual min-lot risk already captures account size |
| 11 | Swing SMALL risk bands | SMALL target 3.0–4.5%, elevated 4.5–6.5%, ceiling 7%, daily lock 12% | not active V1 policy; all exact scalp values recalibrate | **REMOVED as production policy** |
| 12 | Historical aggressive 8%/16% idea | legacy small-account context outside final Swing profile table / prior project history | not active V1; only possible explicit disabled research experiment | **DEFERRED/REJECTED for production** |
| 13 | Min-lot handling | evaluate real broker minimum rather than invent fractional lot or move stop | same invariant retained | **KEPT** |
| 14 | News UNKNOWN | Swing explicitly allowed `Session OPEN + News UNKNOWN → combined PASS` | News UNKNOWN blocks **new entries** in V1 | **CHANGED** to conservative scalp event-risk policy |
| 15 | News API outage | Swing public-calendar failure could still PASS when session OPEN | temporary failure uses valid last-known-good cache; only expired/invalid/no cache becomes UNKNOWN and blocks | **CHANGED/REFINED**: availability without stale-data optimism |
| 16 | News cache | Swing used bounded successful weekly-feed cache and adaptive unknown-news PASS | cache is accepted safety truth only inside original TTL/scope/coverage; failure never refreshes timestamps | **STRENGTHENED** cache integrity |
| 17 | Blackout/warmup durations | Swing had specific event/session values | mechanism retained, exact scalp windows recalibrate | **CALIBRATE**, not copied |
| 18 | PRE_CLOSE timings | Swing used daily T-20/T-10 and weekend T-60/T-30 mechanisms/values | two-stage mechanism retained; exact minutes recalibrate | **MECHANISM KEPT / NUMBERS REOPENED** |
| 19 | Reopen clean bars | Swing daily=1 completed M5, weekend=2 + gap assessment | warmup mechanism retained; exact counts require scalp/broker evidence | **MECHANISM KEPT / NUMBERS REOPENED** |
| 20 | Runner | meaningful continuation path in Swing | exceptional, not default scalp objective | **CHANGED** to prevent accidental swing conversion |
| 21 | Time efficiency | less central to Swing | first-class management evidence; produces normal `EXIT`, not separate `TIME_EXIT` action | **ADDED/STRENGTHENED** |
| 22 | Trade Manager action vocabulary | HOLD/PROTECT/TRAIL/RUNNER/EXIT | same action vocabulary | **KEPT**, with stronger scalp time-efficiency semantics |
| 23 | Physical parallelism | reference implemented bounded concurrent analytical scheduling | logical independence retained; physical concurrency optional/profiling-driven; one-worker parity canonical | **SIMPLIFIED** to avoid concurrency theatre |
| 24 | Execution latency | observable but less central to trade horizon | explicit scalp diagnostic for trigger/quote staleness; no HFT claim | **STRENGTHENED** |
| 25 | Runtime mode | governed DEMO path in reference with release evidence | READINESS/DRY_RUN first → controlled DEMO; REAL outside V1 | **TIGHTENED** release scope |
| 26 | REAL trading | future/controlled reference capability context | explicitly DEFERRED V1 and requires separate governance | **DEFERRED** |
| 27 | Runtime Git publication | Swing included graceful-shutdown Git archive/commit/push publication | completely removed from trading runtime | **REMOVED** to eliminate credential/network/GitHub-account coupling |
| 28 | Runtime backup | reference had durable checkpoint plus publication path | local transactional state → rolling/final local checkpoint → optional recovery package | **CHANGED** to local-first |
| 29 | Development backup | reference relied more heavily on repository publication workflow | major coherent remote commit → user `git pull --ff-only` → optional secret-clean ZIP | **ADDED/CHANGED** for minimum GitHub usage |
| 30 | Git bundle | useful portable source-history mechanism | optional advanced/manual only, not normal workflow | **SIMPLIFIED** |
| 31 | Same-scope multi-machine | single-writer safety | sequential handoff only; no active-active V1 | **KEPT/EXPLICIT** |
| 32 | Research metrics | R, MAE/MFE, management/family evidence | adds stronger cost, latency, duration, entry/capture efficiency and min-lot block analysis | **STRENGTHENED** for scalping |
| 33 | Reference audit results | Swing Audits 1–7 contain real findings for that project | treated as lessons only, never copied as Scalp PASS/results | **EVIDENCE BOUNDARY CHANGED** |

## 4. Important thresholds deliberately not copied

These reference values/mechanisms are not automatically GoldScalpTrader production truth:

- Swing 1.20R Primary floor;
- Swing SMALL/MEDIUM/NORMAL risk percentages;
- Swing profile equity boundaries;
- exact Swing daily-loss percentages;
- 3-loss/30-minute cooldown as a frozen scalp value;
- exact same-episode re-entry count;
- exact News blackout windows;
- exact PRE_CLOSE minutes;
- exact reopen clean-bar counts;
- Swing provider TTL (including 1800 seconds) as an automatic scalp value;
- exact spread/drift/deviation thresholds;
- historical reference test counts or audit PASS claims.

They are classified as CALIBRATION, EXTERNAL PROOF, DEFERRED or SUPERSEDED as appropriate.

## 5. Explicit removals

Removed from GoldScalpTrader V1 architecture:

1. trading-runtime Git add/commit/push/pull;
2. runtime GitHub credential dependency;
3. automatic SMALL/MEDIUM/NORMAL production risk-tier selection;
4. inherited Swing 1.20R hard floor;
5. `OPEN + News UNKNOWN → PASS` as V1 entry policy;
6. M1/tick-history production trigger authority;
7. active-active same-scope multi-laptop design;
8. REAL trading as an implicit V1 mode;
9. any requirement that scalp correctness depend on partial profit-taking at 0.01 lot.

## 6. Explicit additions / stronger contracts

GoldScalpTrader adds or elevates:

- cost-adjusted target-room truth;
- event freshness / distance-since-trigger / chase control;
- explicit current Bid/Ask versus Signal/Entry Reference/Fill separation;
- scalp time-efficiency exit reasoning;
- provider last-known-good cache with no timestamp laundering;
- conservative stale-news safety after cache expiry;
- local development pull/ZIP backup workflow;
- more explicit latency diagnostics;
- accidental-swing-conversion prevention;
- scalp-specific min-lot affordability frequency research.

## 7. Final rule

This file is the permanent explicit-delta ledger. If a future governed change alters one of these differences, update this file, `DESIGN_DECISIONS.md`, the owning topic contract and affected operator/engineering docs in the same change packet.