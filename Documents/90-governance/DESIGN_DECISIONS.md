# GoldScalpTrader — Design Decision Ledger

**Status:** POST-AUDIT-1 DECISION LEDGER — PRESERVATION-FIRST CORRECTION ACTIVE
**Version:** 1.2-preserve-swing-unless-scalp-specific
**Authority:** Durable project decisions, supersession and rationale. Topic contracts own exact behaviour.

## 1. Status vocabulary

```text
ACTIVE       approved current architecture/policy
SUPERSEDED   retained history; later decision owns current behaviour
CALIBRATE    architecture fixed; numerical value needs evidence
EXTERNAL     real broker/machine/provider proof required
DEFERRED     deliberately outside current enabled scope, not necessarily removed as a future capability
```

## 2. Product / process

| ID | Decision | Rationale / consequence | Status |
|---|---|---|---|
| DEC-001 | Documentation is designed/challenged before implementation expansion | prevent code-driven undocumented behaviour | ACTIVE |
| DEC-002 | `Documents/` is sole current documentation authority | one reconstructable truth surface | ACTIVE |
| DEC-003 | GoldSwingTraderAI is the default feature/behaviour baseline; GoldScalpTrader changes it only for a direct scalping requirement, an explicit operator instruction, or a separately proven reference defect | preserve requested functionality and avoid convenience-driven simplification | ACTIVE |
| DEC-004 | Maintain reference-equivalent 64-file canonical manual | no documentation/component surface silently omitted | ACTIVE |
| DEC-005 | Fresh-zero review may challenge inherited behaviour but cannot silently remove a non-scalp feature merely because a simpler design is possible | challenge must respect preservation requirement | ACTIVE |
| DEC-006 | Every material change follows full affected-graph synchronization | docs/code/tests/operator/recovery/research stay aligned | ACTIVE |
| DEC-007 | No trading-runtime Git commit/push/pull | explicit operator requirement; remove credential/network coupling and GitHub account risk | ACTIVE |
| DEC-008 | Required infrastructure target remains zero-cost/local-first | no mandatory paid API/cloud/Actions/Codespaces/LFS | ACTIVE |
| DEC-009 | When it is unclear whether a reference difference is genuinely scalp-specific, preserve the Swing behaviour/default and record the possible scalp change for final documentation discussion instead of changing it early | preservation-first tie-breaker | ACTIVE |

## 3. Runtime / parallel-serial architecture

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-020 | One normalized MT5 read boundary | prevent contradictory broker truth | ACTIVE |
| DEC-021 | One immutable MarketSnapshot per analytical cycle | shared deterministic facts | ACTIVE |
| DEC-022 | Preserve bounded physical concurrency for dependency-independent analytical desks/families as a target feature; keep deterministic one-worker fallback/parity | concurrency is a reference engineering feature, not a scalp-specific feature to remove | ACTIVE |
| DEC-023 | One-worker analytical execution must be semantically identical to bounded-parallel execution | deterministic fallback / testability | ACTIVE |
| DEC-024 | Broker/lifecycle authority is strictly serial | money/exposure cannot race | ACTIVE |
| DEC-025 | One active PRIMARY writer per account/symbol scope | avoid split brain | ACTIVE |
| DEC-026 | Same-scope multi-laptop is sequential handoff unless a future shared-fencing architecture is deliberately added | local state cannot globally fence another machine | ACTIVE |
| DEC-027 | Different independent account/symbol scopes may run separately | independent exposure/state | ACTIVE |
| DEC-028 | UNKNOWN required financial/broker/lifecycle truth fails closed | missing truth is not safe zero | ACTIVE |
| DEC-029 | Current broker truth outranks restored local context | restore cannot invent exposure | ACTIVE |

## 4. Scalping timeframes / data

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-040 | Structural/indicator authority uses completed candles + causal knowledge time | no forming-bar/lookahead authority | ACTIVE |
| DEC-041 | H1 = broad soft regime; M15 = opportunity/location/path; M5 = primary completed setup/timing/management | direct scalp-horizon change | ACTIVE |
| DEC-042 | H4 is optional major context, never universal scalp veto | direct scalp-horizon change | ACTIVE |
| DEC-043 | M1 is diagnostic/research only in V1 | retained after challenge; avoids hidden micro-timeframe authority without evidence | ACTIVE |
| DEC-044 | Quote/current tick is executable condition/health, not structural-history authority | separate current market from causal history | ACTIVE |
| DEC-045 | Tick-history intelligence is outside initial implementation scope | complexity not required by preserved reference feature set | DEFERRED |
| DEC-046 | Event/trigger freshness is first-class entry evidence | stale events can destroy scalp efficiency | ACTIVE |
| DEC-047 | Exact freshness/chase thresholds are family/event specific calibration | numerical evidence required | CALIBRATE |

## 5. Strategy / decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-060 | Retain six independent families: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal, Compression Expansion | preserve reference feature set; narratives remain distinct at scalp horizon | ACTIVE |
| DEC-061 | Correlated family evidence must be bounded and preserve event lineage | prevent one episode becoming fake multi-confirmation | ACTIVE |
| DEC-062 | BUY and SELL theses remain independent | visible opposition/conflict | ACTIVE |
| DEC-063 | No unanimity/filter-soup requirement | protect Opportunity Recall | ACTIVE |
| DEC-064 | Persistent Opportunity is distinct from executable timing | strong idea can wait for efficient entry | ACTIVE |
| DEC-065 | Terminal Opportunity cannot re-arm without genuinely fresh causal event | prevent repeated chasing | ACTIVE |
| DEC-066 | TradePlan owns structural geometry before monetary Risk | account cannot distort invalidation | ACTIVE |
| DEC-067 | Family-specific event/retest invalidation only from exact proven causal geometry | tighter scalp geometry without arbitrary stops | ACTIVE |
| DEC-068 | Swing's 1.20R Primary floor is not inherited as a hard scalp entry floor | direct scalp cost/target-horizon difference | SUPERSEDED |
| DEC-069 | TradePlan must retain both gross structural quality and explicit cost-adjusted room diagnostics | gross chart R alone is insufficient for scalping | ACTIVE |
| DEC-070 | Exact scalp gross/net/cost-room thresholds require replay/stress/holdout | calibration, not architecture | CALIBRATE |
| DEC-071 | Runner is exceptional, not default scalp objective | direct scalp hold-horizon change | ACTIVE |
| DEC-072 | Time/efficiency weakness is a first-class EXIT reason, not a separate TIME_EXIT lifecycle action | direct scalp management semantics | ACTIVE |
| DEC-073 | Preserve optional broker-valid partial-management capability where executable volume is divisible; minimum-lot correctness must not depend on partial close | preserve feature without making 0.01 unmanageable | ACTIVE |

## 6. Monetary Risk

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-080 | Monetary Risk is independent hard authority | confidence cannot silently increase financial permission | ACTIVE |
| DEC-081 | Preserve automatic `SMALL / MEDIUM / NORMAL` account profiles resolved from positive DayStartEquity and fixed for the UTC risk day | operator requested preservation; not a scalp-specific feature to remove | ACTIVE |
| DEC-082 | Preserve Swing baseline profile boundaries and bands unless a later scalp-specific governed decision changes them: SMALL < $300, MEDIUM $300–$999.99, NORMAL >= $1,000 | baseline continuity | ACTIVE |
| DEC-083 | Dynamic sizing uses broker min/max/step/tick geometry and actual normalized-volume risk | executable reality | ACTIVE |
| DEC-084 | Raw lot below minimum triggers evaluation of real minimum-lot risk | truthful small-account handling | ACTIVE |
| DEC-085 | Structural SL is never tightened merely to make 0.01 affordable | preserve thesis integrity | ACTIVE |
| DEC-086 | One independent Gold risk position per scope in initial V1 | bounded exposure | ACTIVE |
| DEC-087 | No martingale, uncontrolled grid or averaging-down rescue | bounded risk | ACTIVE |
| DEC-088 | Current scaffold 0.50% is provisional implementation seed only and does not supersede the preserved profile contract | existing scaffold is not canonical risk truth | ACTIVE |
| DEC-089 | Preserve the operator-requested `AGGRESSIVE_SMALL_ACCOUNT` mode as an operational capability, disabled by default and never auto-enabled merely by balance | requested feature must not be removed | ACTIVE |
| DEC-090 | When explicitly enabled for eligible sub-$1,000 account operation, 8% is a **maximum monetary SL-risk ceiling, not a target**; maximum aggregate open risk is 16% and daily-loss ceiling is 16%, while all structural/session/execution safeguards remain | preserve requested 8%/16% semantics without making them default | ACTIVE |
| DEC-091 | Preserve governed manual daily-loss reset capability but keep it disabled by default | requested/reference behaviour; prevents casual lock bypass | ACTIVE |
| DEC-092 | Preserve Swing baseline loss-streak/cooldown/re-entry policy unless later scalp evidence justifies a change: one genuinely fresh same-episode re-entry; three consecutive closed bot losses trigger at least 30 minutes global cooldown plus freshness/health release conditions | non-scalp default restored | ACTIVE |

### 6.1 Preserved baseline profile table

| Profile | DayStartEquity | Normal / target risk | Elevated acceptable | New-entry hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|---:|
| SMALL | positive and < $300 | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | $300–$999.99 | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | >= $1,000 | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

These are inherited policy defaults, not profitability promises. A future scalp-specific change must be explicit and discussed through the governed documentation process.

## 7. Session / News

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-100 | Soft session context and hard broker market state remain separate | labels do not prove tradeability | ACTIVE |
| DEC-101 | Known high-impact blackout is hard new-entry BLOCK | event shock risk | ACTIVE |
| DEC-102 | News UNKNOWN never becomes CLEAR | truthful uncertainty | ACTIVE |
| DEC-103 | `Session OPEN + News UNKNOWN` blocks **new entry** while management/protection/mandatory CLOSE remain action-sensitive | direct scalp event-sensitivity decision | ACTIVE |
| DEC-104 | Preserve Swing PRE_CLOSE defaults unless later scalp-specific evidence changes them: daily T-20 no new entry / T-10 mandatory flatten; weekend T-60 / T-30 | non-scalp safety default restored | ACTIVE |
| DEC-105 | Preserve Swing reopen defaults unless later scalp-specific evidence changes them: daily one clean completed M5; weekend two clean completed M5 plus gap assessment | non-scalp safety default restored | ACTIVE |
| DEC-106 | A temporary News API/provider refresh failure may reuse last-known-good event truth only while original scope/schema/coverage/TTL remain valid; failure never refreshes timestamps, and expired/invalid cache becomes News UNKNOWN | explicit operator-requested resilience with truthful stale-data boundary | ACTIVE |
| DEC-107 | Preserve Swing provider TTL baseline of 1800 seconds until a specific scalp/provider reason justifies changing it | reference default restored | ACTIVE |

## 8. Execution / lifecycle

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-120 | READINESS/DRY_RUN precede any irreversible writer | no accidental broker execution | ACTIVE |
| DEC-121 | Controlled DEMO is first broker-write target after deterministic proof | external proof boundary | ACTIVE |
| DEC-122 | Preserve a future governed REAL capability; it remains disabled/unavailable until DEMO evidence, release gates and explicit operator approval satisfy the separate REAL policy | preserve feature without creating a hidden shortcut | ACTIVE |
| DEC-123 | Central Gate does not replace upstream TradePlan/Risk owners | truthful authority | ACTIVE |
| DEC-124 | Persist one-shot Intent before irreversible send | duplicate protection | ACTIVE |
| DEC-125 | Sole MT5Writer owns raw irreversible operations | one write boundary | ACTIVE |
| DEC-126 | Ambiguous acknowledgement means reconciliation, never blind retry | avoid duplicate exposure | ACTIVE |
| DEC-127 | Execution rechecks current spread/drift/trigger age/fresh broker facts | scalp edge can expire quickly | ACTIVE |
| DEC-128 | Mandatory risk-reducing CLOSE is action-sensitive and not mechanically vetoed by discretionary OPEN friction rules | avoid trapping unwanted risk | ACTIVE |
| DEC-129 | Latency is measured/observable but is not an HFT design claim | scalp freshness evidence before threshold | ACTIVE |

## 9. Persistence / source backup / multi-machine

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-140 | SQLite is V1 local transactional storage | simple zero-cost state authority | ACTIVE |
| DEC-141 | Full checkpoint is transportable context, not broker truth | restore safety | ACTIVE |
| DEC-142 | Automatic runtime backup root is outside active repo | prevent recursion/bloat/accidental commits | ACTIVE |
| DEC-143 | Graceful shutdown creates final verified **local** checkpoint; no Git operation | explicit operator requirement / network-independent safety | ACTIVE |
| DEC-144 | Normal development backup is major bulk commit → user `git pull --ff-only` | explicit operator workflow; minimizes GitHub operations while preserving local Git history | ACTIVE |
| DEC-145 | Local working clone is primary source/history backup after pull | simple and complete | ACTIVE |
| DEC-146 | Optional local ZIP source snapshot may be created after milestone with secrets/runtime artifacts excluded | simple offline copy | ACTIVE |
| DEC-147 | Git bundle is optional advanced/manual tooling only, not normal runtime/development requirement | operator-preferred simplicity | ACTIVE |
| DEC-148 | Portable runtime recovery package excludes secrets and restores to new DB/path | safe handoff | ACTIVE |
| DEC-149 | Optional second HDD/SSD/USB copy is supported | physical-device resilience | ACTIVE |

## 10. Learning / research

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-160 | Learning is downstream and cannot create broker authority | stable live trader | ACTIVE |
| DEC-161 | Actual/counterfactual/system-fault evidence remain distinct | no fake performance | ACTIVE |
| DEC-162 | Verified close uses queue + closure receipt + exactly-once StrategyMemory | crash-safe learning | ACTIVE |
| DEC-163 | Scalp research explicitly models costs, latency, duration and min-lot affordability | realistic short-horizon evidence | ACTIVE |
| DEC-164 | Autonomous invention is declarative proposal only | no generated-code authority | ACTIVE |
| DEC-165 | Candidate cannot self-promote | approval/evidence governance | ACTIVE |
| DEC-166 | Final holdout is one-shot after semantic lock | anti-overfitting | ACTIVE |

## 11. Operator / engineering

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-180 | Terminal dashboard is primary; browser optional/read-only | no UI dependency for trading liveness | ACTIVE |
| DEC-181 | Dashboard cannot recalculate authority | one owner per rule | ACTIVE |
| DEC-182 | Upstream `ENTRY_BLOCKED` is not automatically Gate BLOCK | truthful blocker stage | ACTIVE |
| DEC-183 | Green tests do not equal connected broker proof/profitability | evidence boundaries | ACTIVE |
| DEC-184 | GitHub Actions are not required | local verification / zero-cost strategy | ACTIVE |
| DEC-185 | Documentation finalization includes an explicit operator discussion of the remaining genuinely scalp-specific deltas before implementation begins | user-requested final review checkpoint | ACTIVE |

## 12. Freeze rule

The preservation-first correction supersedes earlier Audit-1 simplifications that removed or reopened non-scalp reference features/defaults.

Architecture can be frozen while:

- genuinely scalp-specific thresholds remain `CALIBRATION PENDING`;
- broker/platform/provider behaviours remain `EXTERNAL PROOF PENDING`;
- implementation/test evidence remains not-yet-run until exact code exists.

A non-scalp inherited feature/default stays in force unless a later explicit governed decision replaces it. No decision in this ledger is a profitability guarantee.