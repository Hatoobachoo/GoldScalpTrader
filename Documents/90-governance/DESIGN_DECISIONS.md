# GoldScalpTrader — Design Decision Ledger

**Status:** DRAFT PRE-CHALLENGE DECISION LEDGER
**Version:** 0.2-full-manual-draft
**Authority:** Durable project decisions, supersession and rationale.

## 1. How to read this ledger

This ledger preserves **why** architecture choices exist. Topic contracts own exact behaviour.

Statuses:

```text
DRAFT        proposed before fresh-zero challenge
ACTIVE       approved/frozen current behaviour
SUPERSEDED   historical rationale retained; later decision owns current behaviour
CALIBRATE    architecture fixed, numeric value needs evidence
EXTERNAL     real broker/machine/provider proof required
DEFERRED     deliberately outside current V1
```

Nothing marked DRAFT is implementation permission.

## 2. Product / process decisions

| ID | Decision | Rationale / consequence | Status |
|---|---|---|---|
| DEC-001 | Documentation is completed/challenged before implementation expansion | prevent code-driven undocumented design | DRAFT |
| DEC-002 | `Documents/` is sole current documentation authority | one reconstructable truth surface | DRAFT |
| DEC-003 | GoldScalpTrader inherits GoldSwingTraderAI governance/engineering spine, not blindly its trading thresholds | preserve proven architecture while adapting personality | DRAFT |
| DEC-004 | Full reference-equivalent 64-file canonical manual will exist | no document/function silently omitted | DRAFT |
| DEC-005 | Fresh-zero Audit 1 runs before implementation freeze | challenge inheritance bias | DRAFT |
| DEC-006 | Every material change follows full affected-graph synchronization | docs/code/tests/operator/recovery/research stay consistent | DRAFT |
| DEC-007 | No runtime Git commit/push on graceful shutdown | reduce credentials/network coupling and GitHub account risk | DRAFT |
| DEC-008 | Runtime/source/cloud infrastructure target remains zero-cost | local MT5/Python/Git; no required paid API/cloud | DRAFT |

## 3. Runtime architecture decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-020 | One normalized MT5 read boundary | prevent contradictory broker truth | DRAFT |
| DEC-021 | One immutable MarketSnapshot per analytical cycle | shared deterministic facts | DRAFT |
| DEC-022 | Dependency-independent analytical work may run bounded-parallel | preserve specialist independence/performance | DRAFT |
| DEC-023 | Broker/lifecycle authority remains strictly serial | money/exposure cannot race | DRAFT |
| DEC-024 | One active PRIMARY writer per account/symbol scope | avoid split brain | DRAFT |
| DEC-025 | Same-scope multi-laptop is sequential handoff only in V1 | local DB cannot globally fence second machine | DRAFT |
| DEC-026 | Different independent account/symbol scopes may run separately | independent exposure/state | DRAFT |
| DEC-027 | UNKNOWN required financial/broker/lifecycle truth fails closed | missing truth is not safe zero | DRAFT |
| DEC-028 | Current broker truth outranks restored local context | restart/restore cannot invent exposure | DRAFT |

## 4. Scalping data/timeframe decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-040 | Structural facts use completed candles + causal knowledge time | no forming-bar/lookahead authority | DRAFT |
| DEC-041 | H1 broad regime, M15 opportunity/location, M5 primary setup/timing is baseline | scalp-native hierarchy derived from reference | DRAFT |
| DEC-042 | H4 optional major context | avoid making every scalp depend on swing horizon | DRAFT |
| DEC-043 | M1 diagnostic-only is baseline, not final | fresh-zero challenge must decide if explicit micro-timing authority adds value | DRAFT |
| DEC-044 | Quote/tick is executable condition, not retroactive structural proof | separate current market from historical structure | DRAFT |
| DEC-045 | Event/trigger freshness is first-class | stale evidence destroys scalp efficiency | DRAFT |
| DEC-046 | Transaction-cost context is first-class | small target room makes spread/slippage material | DRAFT |

## 5. Strategy / decision decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-060 | Start with six independent reference family narratives | preserves parallel hypothesis floor | DRAFT |
| DEC-061 | Six families may be merged/split/replaced only after fresh-zero review | avoid inheritance bias | DRAFT |
| DEC-062 | BUY and SELL theses remain independent | visible opposition/conflict | DRAFT |
| DEC-063 | No unanimity/filter-soup requirement | protect Opportunity Recall | DRAFT |
| DEC-064 | Persistent Opportunity is distinct from executable timing | strong idea can wait for efficient entry | DRAFT |
| DEC-065 | Terminal Opportunity cannot re-arm without a genuinely fresh causal event | prevent repeated chasing | DRAFT |
| DEC-066 | TradePlan owns structural geometry before monetary Risk | account cannot distort market invalidation | DRAFT |
| DEC-067 | Family-specific event/retest invalidation allowed only from exact proven causal geometry | local scalp stops without arbitrary tightening | DRAFT |
| DEC-068 | Swing reference 1.20R floor is not automatically frozen for scalping | cost/hold horizon differs | CALIBRATE |
| DEC-069 | Runner is exceptional, not default scalp objective | avoid accidental swing conversion | DRAFT |
| DEC-070 | Time/efficiency exit is a first-class scalp research/design question | scalp thesis includes expected speed | CALIBRATE |

## 6. Risk decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-080 | Monetary Risk is independent hard authority | confidence cannot increase financial permission silently | DRAFT |
| DEC-081 | Dynamic sizing uses broker min/max/step/tick geometry | executable reality | DRAFT |
| DEC-082 | Raw lot below minimum triggers evaluation of real minimum-lot risk | small-account truth | DRAFT |
| DEC-083 | Structural SL is never tightened merely to make 0.01 affordable | preserve thesis integrity | DRAFT |
| DEC-084 | One independent Gold risk position per scope in initial V1 | bounded exposure | DRAFT |
| DEC-085 | No martingale, uncontrolled grid or averaging-down rescue | bounded risk | DRAFT |
| DEC-086 | Exact risk bands/daily-loss thresholds are not copied from Swing | scalp frequency/small account require fresh evidence | CALIBRATE |
| DEC-087 | Current scaffold 0.50% risk is provisional only | existing safety seed, not final policy | DRAFT |
| DEC-088 | Optional aggressive mode, if retained, must be explicit and disabled by default | high-risk behaviour cannot be implicit | CALIBRATE |
| DEC-089 | Manual daily-loss reset capability remains disabled by default | prevent easy bypass of daily lock | DRAFT |

## 7. Session/news decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-100 | Soft session context and hard broker market state remain separate | labels do not prove tradeability | DRAFT |
| DEC-101 | Known blackout is hard new-entry block | event shock risk | DRAFT |
| DEC-102 | News UNKNOWN never becomes CLEAR | truthful uncertainty | DRAFT |
| DEC-103 | Swing's `OPEN + News UNKNOWN → PASS` is not automatically inherited | scalping is more immediate-event sensitive | CALIBRATE |
| DEC-104 | PRE_CLOSE two-stage mechanism retained, exact times recalibrated | safe flattening without blindly copying swing timing | CALIBRATE |
| DEC-105 | Reopen warmup retained, exact clean-bar requirements recalibrated | first quote is not normalized market proof | CALIBRATE |

## 8. Execution/lifecycle decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-120 | DRY_RUN precedes broker-write implementation | no accidental live execution | DRAFT |
| DEC-121 | Any future broker-write V1 is DEMO-governed first; REAL requires separate decision | safety boundary | DRAFT |
| DEC-122 | Central Gate does not replace upstream TradePlan/Risk owners | truthful authority | DRAFT |
| DEC-123 | Persist one-shot Intent before irreversible send | duplicate protection | DRAFT |
| DEC-124 | Sole MT5Writer owns raw irreversible operations | one write boundary | DRAFT |
| DEC-125 | Ambiguous acknowledgement means reconciliation, never blind retry | avoid duplicate exposure | DRAFT |
| DEC-126 | Execution rechecks spread/drift/trigger age/fresh broker facts | scalp edge can expire quickly | DRAFT |
| DEC-127 | Mandatory risk-reducing CLOSE is action-sensitive and not mechanically vetoed by every OPEN friction rule | avoid trapping risk | DRAFT |

## 9. Persistence / backup decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-140 | SQLite is V1 storage candidate, subject to fresh-zero review | simple local transactional state | DRAFT |
| DEC-141 | Full checkpoint is transportable context, not broker truth | restore safety | DRAFT |
| DEC-142 | Automatic backup root is outside active repo | prevent recursion/bloat/accidental commits | DRAFT |
| DEC-143 | Graceful shutdown creates final verified local checkpoint, no Git push | local safety independent of network/GitHub | DRAFT |
| DEC-144 | Source Git bundle is deliberate milestone backup, not every shutdown | separate source durability from runtime state | DRAFT |
| DEC-145 | Portable recovery package excludes secrets and restores to new DB/path | safe handoff | DRAFT |
| DEC-146 | Optional second HDD/SSD/USB backup is supported | physical-device resilience | DRAFT |

## 10. Learning/research decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-160 | Learning is downstream and cannot create broker authority | stable live trader | DRAFT |
| DEC-161 | Actual/counterfactual/system-fault evidence remain distinct | no fake performance | DRAFT |
| DEC-162 | Verified close uses queue + closure receipt + exactly-once StrategyMemory | crash-safe learning | DRAFT |
| DEC-163 | Scalping research explicitly models costs, latency, duration and min-lot affordability | realistic short-horizon evidence | DRAFT |
| DEC-164 | Autonomous invention is declarative proposal only | no generated-code authority | DRAFT |
| DEC-165 | Candidate cannot self-promote | approval/evidence governance | DRAFT |
| DEC-166 | Final holdout is one-shot after semantic lock | anti-overfitting | DRAFT |

## 11. Operator/engineering decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| DEC-180 | Terminal dashboard is primary, browser optional/read-only | no UI dependency for liveness | DRAFT |
| DEC-181 | Dashboard cannot recalculate authority | one owner per rule | DRAFT |
| DEC-182 | Upstream `ENTRY_BLOCKED` is not automatically Gate BLOCK | truthful blocker stage | DRAFT |
| DEC-183 | Audits are `NOT RUN` until evidence exists | no fake completion | DRAFT |
| DEC-184 | GitHub Actions not required | zero-cost/local verification strategy | DRAFT |

## 12. Freeze rule

After the 64-file manual is complete, `AUDIT_1_FRESH_DESIGN_REVIEW.md` challenges every DRAFT/CALIBRATE decision.

Only then are accepted choices marked ACTIVE/FROZEN and implementation begins.
