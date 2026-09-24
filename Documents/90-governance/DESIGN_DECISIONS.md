# GoldScalpTrader — Design Decision Ledger

**Status:** POST-AUDIT-1 DECISION LEDGER — ARCHITECTURE DECISIONS ACTIVE
**Version:** 1.1-cache-resilient-news
**Authority:** Durable project decisions, supersession and rationale. Topic contracts own exact behaviour.

## 1. Status vocabulary

```text
ACTIVE       approved current architecture/policy
SUPERSEDED   retained history; later decision owns current behaviour
CALIBRATE    architecture fixed; numerical value needs evidence
EXTERNAL     real broker/machine/provider proof required
DEFERRED     deliberately outside current V1
```

## 2. Product / process

| ID | Decision | Rationale / consequence | Status |
|---|---|---|---|
| DEC-001 | Documentation is designed/challenged before implementation expansion | prevent code-driven undocumented behaviour | ACTIVE |
| DEC-002 | `Documents/` is sole current documentation authority | one reconstructable truth surface | ACTIVE |
| DEC-003 | Preserve GoldSwingTraderAI governance/engineering spine, not its untested scalp calibration | reuse strong boundaries without copy bias | ACTIVE |
| DEC-004 | Maintain reference-equivalent 64-file canonical manual | no documentation/component surface silently omitted | ACTIVE |
| DEC-005 | Fresh-zero Audit 1 precedes implementation freeze | inheritance is not proof | ACTIVE |
| DEC-006 | Every material change follows full affected-graph synchronization | docs/code/tests/operator/recovery/research stay aligned | ACTIVE |
| DEC-007 | No trading-runtime Git commit/push/pull | remove credential/network coupling and GitHub account risk | ACTIVE |
| DEC-008 | Required infrastructure target remains zero-cost/local-first | no mandatory paid API/cloud/Actions/Codespaces/LFS | ACTIVE |

## 3. Runtime / parallel-serial architecture

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-020 | One normalized MT5 read boundary | prevent contradictory broker truth | ACTIVE |
| DEC-021 | One immutable MarketSnapshot per analytical cycle | shared deterministic facts | ACTIVE |
| DEC-022 | Specialist work is logically independent; physical bounded concurrency is optional/profiling-driven | preserve parallel design without concurrency theatre | ACTIVE |
| DEC-023 | One-worker analytical execution must be semantically identical to bounded-parallel execution | deterministic fallback | ACTIVE |
| DEC-024 | Broker/lifecycle authority is strictly serial | money/exposure cannot race | ACTIVE |
| DEC-025 | One active PRIMARY writer per account/symbol scope | avoid split brain | ACTIVE |
| DEC-026 | Same-scope multi-laptop is sequential handoff only in V1 | local state cannot globally fence another machine | ACTIVE |
| DEC-027 | Different independent account/symbol scopes may run separately | independent exposure/state | ACTIVE |
| DEC-028 | UNKNOWN required financial/broker/lifecycle truth fails closed | missing truth is not safe zero | ACTIVE |
| DEC-029 | Current broker truth outranks restored local context | restore cannot invent exposure | ACTIVE |

## 4. Scalping timeframes / data

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-040 | Structural/indicator authority uses completed candles + causal knowledge time | no forming-bar/lookahead authority | ACTIVE |
| DEC-041 | H1 = broad soft regime; M15 = opportunity/location/path; M5 = primary completed setup/timing/management | scalp-native but stable hierarchy | ACTIVE |
| DEC-042 | H4 is optional major context, never universal scalp veto | avoid swingifying every scalp | ACTIVE |
| DEC-043 | M1 is diagnostic/research only in V1 | avoid hidden micro-timeframe authority before evidence | ACTIVE |
| DEC-044 | Quote/current tick is executable condition/health, not structural-history authority | separate current market from causal history | ACTIVE |
| DEC-045 | Tick-history intelligence is outside V1 | complexity not justified without evidence | DEFERRED |
| DEC-046 | Event/trigger freshness is first-class entry evidence | stale events can destroy scalp efficiency | ACTIVE |
| DEC-047 | Exact freshness/chase thresholds are family/event specific calibration | numerical evidence required | CALIBRATE |

## 5. Strategy / decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-060 | Retain six independent families: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal, Compression Expansion | narratives remain meaningfully distinct at M5 scalp horizon | ACTIVE |
| DEC-061 | Correlated family evidence must be bounded and preserve event lineage | prevent one episode becoming fake multi-confirmation | ACTIVE |
| DEC-062 | BUY and SELL theses remain independent | visible opposition/conflict | ACTIVE |
| DEC-063 | No unanimity/filter-soup requirement | protect Opportunity Recall | ACTIVE |
| DEC-064 | Persistent Opportunity is distinct from executable timing | strong idea can wait for efficient entry | ACTIVE |
| DEC-065 | Terminal Opportunity cannot re-arm without genuinely fresh causal event | prevent repeated chasing | ACTIVE |
| DEC-066 | TradePlan owns structural geometry before monetary Risk | account cannot distort invalidation | ACTIVE |
| DEC-067 | Family-specific event/retest invalidation only from exact proven causal geometry | tighter scalp geometry without arbitrary stops | ACTIVE |
| DEC-068 | Swing's 1.20R Primary floor is not inherited as scalp policy | horizon/cost structure differs | SUPERSEDED |
| DEC-069 | TradePlan must retain both gross structural quality and explicit cost-adjusted room diagnostics | gross chart R alone is insufficient for scalping | ACTIVE |
| DEC-070 | Exact gross/net/cost-room thresholds require replay/stress/holdout | calibration, not architecture | CALIBRATE |
| DEC-071 | Runner is exceptional, not default scalp objective | avoid accidental swing conversion | ACTIVE |
| DEC-072 | Time/efficiency weakness is a first-class EXIT reason, not a separate TIME_EXIT lifecycle action | simpler state machine with scalp-specific semantics | ACTIVE |

## 6. Monetary Risk

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-080 | Monetary Risk is independent hard authority | confidence cannot silently increase financial permission | ACTIVE |
| DEC-081 | V1 uses one explicit STANDARD production risk policy rather than automatic SMALL/MEDIUM/NORMAL equity tiers | actual broker/min-lot risk already captures account-size reality with less policy complexity | ACTIVE |
| DEC-082 | STANDARD policy has preferred per-trade target, hard per-trade ceiling, daily loss limit, one-position capacity and durable cooldown/re-entry state | simple bounded policy | ACTIVE |
| DEC-083 | Dynamic sizing uses broker min/max/step/tick geometry and actual normalized-volume risk | executable reality | ACTIVE |
| DEC-084 | Raw lot below minimum triggers evaluation of real minimum-lot risk | truthful small-account handling | ACTIVE |
| DEC-085 | Structural SL is never tightened merely to make 0.01 affordable | preserve thesis integrity | ACTIVE |
| DEC-086 | One independent Gold risk position per scope in V1 | bounded exposure | ACTIVE |
| DEC-087 | No martingale, uncontrolled grid or averaging-down rescue | bounded risk | ACTIVE |
| DEC-088 | Current scaffold 0.50% is provisional, not frozen production risk | implementation seed only | CALIBRATE |
| DEC-089 | Historical aggressive 8%/16% small-account values are not active V1 policy | excessive/unverified for frequent scalp risk | DEFERRED |
| DEC-090 | Any future AGGRESSIVE_EXPERIMENT is explicit, disabled by default and never auto-selected by equity | preserve optional research without hidden escalation | CALIBRATE |
| DEC-091 | Manual daily-loss reset capability remains disabled by default | prevent easy bypass of daily lock | ACTIVE |
| DEC-092 | Exact preferred/hard ceiling/daily-loss/cooldown/re-entry values require research and DEMO evidence | numerical calibration | CALIBRATE |

## 7. Session / News

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-100 | Soft session context and hard broker market state remain separate | labels do not prove tradeability | ACTIVE |
| DEC-101 | Known high-impact blackout is hard new-entry BLOCK | event shock risk | ACTIVE |
| DEC-102 | News UNKNOWN never becomes CLEAR | truthful uncertainty | ACTIVE |
| DEC-103 | `Session OPEN + News UNKNOWN` blocks **new entry** in V1 while management/protection/mandatory CLOSE remain action-sensitive | conservative scalp exposure to immediate event risk | ACTIVE |
| DEC-104 | PRE_CLOSE two-stage mechanism retained; exact times recalibrate | safe flattening without copying Swing minutes | CALIBRATE |
| DEC-105 | Reopen warmup retained; exact clean-bar requirements recalibrate | first quote is not normalized market proof | CALIBRATE |
| DEC-106 | A temporary News API/provider refresh failure may reuse last-known-good event truth only while original scope/schema/coverage/TTL remain valid; failure never refreshes timestamps, and expired/invalid cache becomes News UNKNOWN | avoid needless provider kill-switch without accepting stale safety truth | ACTIVE |

## 8. Execution / lifecycle

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-120 | READINESS/DRY_RUN precede any irreversible writer | no accidental broker execution | ACTIVE |
| DEC-121 | Controlled DEMO is first broker-write target after deterministic proof | external proof boundary | ACTIVE |
| DEC-122 | REAL trading is outside V1 and requires separate future governance | no hidden environment escalation | DEFERRED |
| DEC-123 | Central Gate does not replace upstream TradePlan/Risk owners | truthful authority | ACTIVE |
| DEC-124 | Persist one-shot Intent before irreversible send | duplicate protection | ACTIVE |
| DEC-125 | Sole MT5Writer owns raw irreversible operations | one write boundary | ACTIVE |
| DEC-126 | Ambiguous acknowledgement means reconciliation, never blind retry | avoid duplicate exposure | ACTIVE |
| DEC-127 | Execution rechecks current spread/drift/trigger age/fresh broker facts | scalp edge can expire quickly | ACTIVE |
| DEC-128 | Mandatory risk-reducing CLOSE is action-sensitive and not mechanically vetoed by discretionary OPEN friction rules | avoid trapping unwanted risk | ACTIVE |
| DEC-129 | Latency is measured/observable but is not an HFT design claim | evidence before threshold | ACTIVE |

## 9. Persistence / source backup / multi-machine

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-140 | SQLite is V1 local transactional storage | simple zero-cost state authority | ACTIVE |
| DEC-141 | Full checkpoint is transportable context, not broker truth | restore safety | ACTIVE |
| DEC-142 | Automatic runtime backup root is outside active repo | prevent recursion/bloat/accidental commits | ACTIVE |
| DEC-143 | Graceful shutdown creates final verified **local** checkpoint; no Git operation | network-independent safety | ACTIVE |
| DEC-144 | Normal development backup is major bulk commit → user `git pull --ff-only` | minimizes GitHub operations while preserving full local Git history | ACTIVE |
| DEC-145 | Local working clone is primary source/history backup after pull | simple and complete | ACTIVE |
| DEC-146 | Optional local ZIP source snapshot may be created after milestone with secrets/runtime artifacts excluded | simple offline copy requested by operator | ACTIVE |
| DEC-147 | Git bundle is optional advanced/manual tooling only, not normal runtime/development requirement | reduce complexity | ACTIVE |
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

## 12. Freeze rule

Audit 1 has resolved the fresh-zero architecture questions. Topic contracts affected by these decisions must remain synchronized before implementation begins.

Architecture may be FROZEN while:

- numeric thresholds remain `CALIBRATION PENDING`;
- broker/platform/provider behaviours remain `EXTERNAL PROOF PENDING`;
- implementation/test evidence remains not-yet-run until exact code exists.

No decision in this ledger is a profitability guarantee.