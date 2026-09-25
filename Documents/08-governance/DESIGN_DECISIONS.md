# GoldScalpTrader — Design Decision Ledger

**Status:** FINAL FROZEN ARCHITECTURE DECISION LEDGER — IMPLEMENTATION PENDING
**Version:** 2.1-final-freeze
**Authority:** Durable approved project decisions, preservation status, Scalp/operator deltas, calibration boundaries and superseded decisions. Topic contracts own exact implementation detail.

## 1. Decision states

```text
FROZEN        approved production architecture/default
PRESERVED     Swing/reference behavior explicitly retained
CALIBRATE     dimension approved; empirical numerical value pending
EXTERNAL      current broker/platform fact requires connected proof
DEFERRED      deliberately outside current architecture/release dependency
APPROVAL      future production/live change requires explicit operator approval
SUPERSEDED    historical decision no longer current authority
```

## 2. Documentation/governance

| ID | Decision | Status |
|---|---|---|
| DEC-001 | Documents are designed/challenged/frozen before production implementation; code must not outrun them | FROZEN |
| DEC-002 | `Documents/` is the single canonical reconstructable project manual | FROZEN |
| DEC-003 | Latest verified GoldSwingTraderAI `Published_B/Documents` is the preservation/depth reference | FROZEN |
| DEC-004 | Canonical manual target is 66 Markdown documents | FROZEN |
| DEC-005 | `GITHUB_STRICT_USE_POLICY.md` and `BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md` are canonical top-level documents | FROZEN |
| DEC-006 | Final numbered folders are `01` through `08`; old `00/10/.../90` paths are retired | FROZEN |
| DEC-007 | Relevant docs use diagrams/tables/state/sequence representations where meaningful | FROZEN |
| DEC-008 | Empirical performance charts use real replay/DEMO evidence only; no fabricated performance charts | FROZEN |
| DEC-009 | One canonical policy owner; mirrors remain explanatory and synchronized | FROZEN |
| DEC-010 | Final architecture was challenged with 100+ attacks before freeze | FROZEN |

## 3. Product objective

| ID | Decision | Status |
|---|---|---|
| DEC-020 | Product philosophy = Opportunity-First, Evidence-Weighted, Precision-Timed, Cost-Aware, Execution-Disciplined, Continuously-Learning | FROZEN |
| DEC-021 | Optimize qualified after-cost edge captured, not win rate or trade count alone | FROZEN |
| DEC-022 | Track Opportunity Recall, Capture Rate, Net Expectancy, Entry/Capture/Exit Efficiency, false blocks, missed opportunity cost, cost burden, throughput and drawdown | FROZEN |
| DEC-023 | ~120 trades/day is a research throughput benchmark, never a forced quota | FROZEN |
| DEC-024 | Avoid unnecessary analytical restrictions; objective broker/account/lifecycle safety remains hard | FROZEN |

## 4. Market-first setup detection and Strategy Isolation

| ID | Decision | Status |
|---|---|---|
| DEC-050 | Chart/market facts determine which setup(s), if any, actually exist before live-strategy eligibility is applied | FROZEN |
| DEC-051 | Active strategy may never be forced onto a chart that does not satisfy its own family definition | FROZEN |
| DEC-052 | Setup Detector may return NONE, one, or multiple causal family candidates | FROZEN |
| DEC-053 | Preserve six families: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal, Compression Expansion | PRESERVED |
| DEC-054 | Exactly one family is `ACTIVE_EXECUTION` during isolation evaluation | FROZEN |
| DEC-055 | Remaining five families are `SHADOW_ONLY`; they may analyze/research but cannot originate live production trades | FROZEN |
| DEC-056 | If only a shadow-family setup is detected, live action is WAIT; shadow setup remains research evidence | FROZEN |
| DEC-057 | Active-family switching is versioned/governed and preserves historical attribution | FROZEN |
| DEC-058 | Future Dynamic Strategy Router is a research/promotion candidate, not current production behavior | APPROVAL |

## 5. Timeframes / chronology

| ID | Decision | Status |
|---|---|---|
| DEC-070 | Completed-candle and knowledge-time causality remain mandatory | PRESERVED |
| DEC-071 | H4 = optional major context | FROZEN |
| DEC-072 | H1 = broad soft regime/context | FROZEN |
| DEC-073 | M15 = opportunity location/path/target context | FROZEN |
| DEC-074 | M5 = primary production setup/thesis + normal management structure | FROZEN |
| DEC-075 | M1 = subordinate entry refinement only after a valid M5 Opportunity | FROZEN |
| DEC-076 | M1 cannot independently create a production Opportunity/trade | FROZEN |
| DEC-077 | Quote/tick = current executable condition, never retroactive historical structure proof | FROZEN |
| DEC-078 | M1 pattern/freshness, M5 event age, chase distance and approved-entry drift | CALIBRATE |

## 6. Evidence / confluence / scoring

| ID | Decision | Status |
|---|---|---|
| DEC-090 | EMA/RSI/Fib/FVG/OB/Trendline/POC may be highly important to relevant families but are not unrelated universal vetoes | FROZEN |
| DEC-091 | Family evidence is classified required/supportive/opposing/not-relevant/unknown | FROZEN |
| DEC-092 | Active family evaluates BUY and SELL independently | PRESERVED |
| DEC-093 | Red Team challenges the active-family thesis; shadow families do not live-vote a trade into existence | FROZEN |
| DEC-094 | Correlated evidence retains causal lineage and cannot create fake independent certainty | FROZEN |
| DEC-095 | Family qualification thresholds, within-family weights and correlation caps | CALIBRATE |
| DEC-096 | Session performance may inform future family tuning but does not create blanket session bans by default | CALIBRATE |

## 7. Analytical performance / concurrency

| ID | Decision | Status |
|---|---|---|
| DEC-110 | One normalized analytical MT5 read boundary + immutable snapshot | PRESERVED |
| DEC-111 | Logical specialist/family independence is mandatory | FROZEN |
| DEC-112 | Physical analytical parallelism is profiling-driven, not mandatory | FROZEN |
| DEC-113 | Optimization order = shared calculations → vectorize/cache → deterministic serial baseline → profile → bounded parallelism if beneficial | FROZEN |
| DEC-114 | One-worker and parallel semantics must be identical/deterministic if parallel mode exists | FROZEN |
| DEC-115 | Financial/broker authority remains strictly serial | PRESERVED |

## 8. Opportunity / TradePlan / executable quality

| ID | Decision | Status |
|---|---|---|
| DEC-130 | Persistent Opportunity remains distinct from current timing | PRESERVED |
| DEC-131 | Terminal Opportunity re-arms only on genuinely fresh causal evidence and applicable re-entry policy | PRESERVED |
| DEC-132 | TradePlan freezes structural geometry before monetary Risk | PRESERVED |
| DEC-133 | Structural SL is never tightened merely to make minimum lot affordable | PRESERVED |
| DEC-134 | Breakout Retest may use causal M5 retest-failure geometry before broader fallback | FROZEN |
| DEC-135 | Sweep/Failed Break reversal may use exact causal event extreme before generic fallback | FROZEN |
| DEC-136 | Swing 1.20R floor is not automatically imposed as hard Scalp floor | FROZEN |
| DEC-137 | Minimum gross R and minimum net/cost-adjusted opportunity quality | CALIBRATE |
| DEC-138 | Fixed + aware spread architecture is mandatory | FROZEN |
| DEC-139 | Absolute emergency spread ceiling | CALIBRATE |
| DEC-140 | Spread/SL is an approved executable-quality dimension | FROZEN |
| DEC-141 | Spread/Target is an approved executable-quality dimension | FROZEN |
| DEC-142 | Total cost/reward is an approved executable-quality dimension | FROZEN |
| DEC-143 | Slippage allowance | CALIBRATE |
| DEC-144 | Broker deviation | CALIBRATE |
| DEC-145 | Decision→send latency outside budget normally triggers fresh revalidation rather than unconditional permanent rejection | FROZEN / CALIBRATE |

## 9. Monetary Risk — explicitly preserved

| ID | Decision | Status |
|---|---|---|
| DEC-160 | Monetary Risk is independent hard authority | PRESERVED |
| DEC-161 | Preserve automatic SMALL/MEDIUM/NORMAL profiles | PRESERVED |
| DEC-162 | Preserve exact profile percentages/bands; do not change without future explicit approval | PRESERVED |
| DEC-163 | Dynamic broker-aware sizing/min-lot actual-risk check remains | PRESERVED |
| DEC-164 | No arbitrary $100 minimum account eligibility floor | PRESERVED |
| DEC-165 | One independently risk-bearing Gold position per scope initially | PRESERVED |
| DEC-166 | No martingale/grid/averaging down | PRESERVED |
| DEC-167 | Aggressive small-account capability preserved, disabled by default | PRESERVED |
| DEC-168 | Aggressive semantics = 8% max single-trade monetary SL-risk ceiling (not target), 16% aggregate, 16% daily | PRESERVED |
| DEC-169 | Manual daily-loss reset preserved, disabled by default | PRESERVED |
| DEC-170 | One genuinely fresh same-episode re-entry baseline | PRESERVED |
| DEC-171 | Three consecutive closed bot losses → at least 30m cooldown + release conditions | PRESERVED |
| DEC-172 | UTC risk-day behavior remains current baseline | PRESERVED |

Canonical profile table:

| Profile | DayStartEquity | Normal | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|---:|
| SMALL | positive < $300 | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | $300–$999.99 | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | >= $1,000 | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

## 10. News / session

| ID | Decision | Status |
|---|---|---|
| DEC-190 | News/Fundamental = soft context, dashboard and research attribution only | FROZEN |
| DEC-191 | Known News event does not directly hard-block a trade | FROZEN |
| DEC-192 | News UNKNOWN/provider/API failure does not directly hard-block trading | FROZEN |
| DEC-193 | News cooldown and mandatory post-News warmup are removed | FROZEN |
| DEC-194 | Actual event-induced bad conditions are governed by spread/drift/dislocation/quote/cost/slippage/latency/broker facts | FROZEN |
| DEC-195 | Provider health/provenance remains truthful; stale/unavailable context is never relabelled CLEAR | FROZEN |
| DEC-196 | 1800-second News/context cache TTL remains current freshness baseline, not trading permission | PRESERVED |
| DEC-197 | Actual broker OPEN/CLOSED/PRE_CLOSE remains hard factual authority | PRESERVED |
| DEC-198 | Daily T-20/T-10 and weekend T-60/T-30 PRE_CLOSE baselines remain pending current broker proof | PRESERVED / EXTERNAL |
| DEC-199 | Daily 1-clean-M5 and weekend 2-clean-M5 + gap reopen baselines remain pending current broker proof | PRESERVED / EXTERNAL |

## 11. Execution / ownership

| ID | Decision | Status |
|---|---|---|
| DEC-210 | Central Gate remains distinct from upstream analytical/plan/quality/Risk stops | PRESERVED |
| DEC-211 | Upstream stop means Gate `NOT_EVALUATED`, not Gate BLOCKED | FROZEN |
| DEC-212 | Persist one-shot Intent before irreversible broker request | PRESERVED |
| DEC-213 | Sole MT5Writer owns raw irreversible MT5 operations | PRESERVED |
| DEC-214 | Fresh broker checks/order_check precede send; precheck failure sends zero requests | PRESERVED |
| DEC-215 | Ambiguous acknowledgement → `ACCEPTED_UNKNOWN` + reconciliation; never blind retry | PRESERVED |
| DEC-216 | Manual/foreign/unknown exposure is never silently adopted | PRESERVED |
| DEC-217 | Controlled DEMO precedes future governed REAL | PRESERVED |
| DEC-218 | REAL activation requires separate evidence/release gate + explicit operator approval | APPROVAL |

## 12. Management

| ID | Decision | Status |
|---|---|---|
| DEC-230 | Management actions remain HOLD/PROTECT/TRAIL/RUNNER/EXIT | PRESERVED |
| DEC-231 | Time/efficiency weakness is a first-class EXIT reason | FROZEN / CALIBRATE |
| DEC-232 | Protection/trailing timing | CALIBRATE |
| DEC-233 | Runner is exceptional and requires fresh continuation/objective | FROZEN / CALIBRATE |
| DEC-234 | Basic broker-valid partial management remains where divisible | PRESERVED |
| DEC-235 | Sophisticated partial-close optimization is not a release dependency | DEFERRED |
| DEC-236 | Minimum-lot correctness cannot depend on partial close | PRESERVED |

## 13. Learning / AI / invention / promotion

| ID | Decision | Status |
|---|---|---|
| DEC-250 | Learning remains downstream from verified evidence | PRESERVED |
| DEC-251 | Actual/shadow/missed/blocked/fault evidence remain separate | FROZEN |
| DEC-252 | Autonomous strategy invention remains active backend capability | PRESERVED |
| DEC-253 | AI/candidate parameter tuning remains active backend capability | PRESERVED |
| DEC-254 | Advanced ML research remains active backend capability | PRESERVED |
| DEC-255 | Candidates may automatically progress through governed evidence stages | FROZEN |
| DEC-256 | Candidate/shadow policy may change in research; current production policy may not silently change | FROZEN |
| DEC-257 | Final production/live promotion stops at `APPROVAL_REQUIRED` until explicit operator approval | APPROVAL |
| DEC-258 | Research/candidates have zero direct broker-write authority | PRESERVED |

## 14. Persistence / machine / GitHub

| ID | Decision | Status |
|---|---|---|
| DEC-270 | Local transactional SQLite remains current StateStore target | PRESERVED |
| DEC-271 | Runtime shutdown performs no Git commit/push/pull | FROZEN |
| DEC-272 | Development source checkpoint = coherent remote commit → operator `git pull --ff-only` | FROZEN |
| DEC-273 | Optional secret-clean source ZIP is separate from runtime state | FROZEN |
| DEC-274 | Same-account active-active/distributed writer is deferred | DEFERRED |
| DEC-275 | Distributed DB/fencing/consensus infrastructure is deferred | DEFERRED |
| DEC-276 | Sequential same-scope machine handoff is the supported architecture | FROZEN |
| DEC-277 | Restore context never outranks current broker truth | PRESERVED |
| DEC-278 | No mandatory paid News API | DEFERRED |
| DEC-279 | No GitHub Actions/cloud compute dependency | DEFERRED |
| DEC-280 | Repository visibility remains unchanged unless operator later explicitly approves a change | FROZEN |

## 15. Dashboard

| ID | Decision | Status |
|---|---|---|
| DEC-300 | Approved visual baseline = GoldSwingTraderAI institutional graphical dashboard adapted to Scalp | FROZEN |
| DEC-301 | Primary desktop dashboard is one screen with no scrollbars | FROZEN |
| DEC-302 | M1/M5/M15/H1/H4 chart buttons are functional | FROZEN |
| DEC-303 | Indicators/Drawings/Settings chart controls are functional | FROZEN |
| DEC-304 | Dashboard separately shows Detected Setup, Active Test Family and Shadow status | FROZEN |
| DEC-305 | Dashboard separately shows exact upstream blocker and actual Gate state | FROZEN |
| DEC-306 | Dashboard is read-only regarding trading authority | PRESERVED |

## 16. Superseded historical decisions

No current owner may use these as present policy:

```text
64-file manual complete
single STANDARD Risk policy
Risk percentages reopened/changed without approval
aggressive 8%/16% research-only
M1 diagnostic-only final Scalp role
News BLACKOUT/UNKNOWN hard entry permission
News cooldown / mandatory post-News warmup
mandatory physical analytical parallelism
blended six-family live voting
active strategy forced onto chart
future REAL removed
partial management removed
```

## 17. Freeze rule

Architecture is now frozen for implementation while explicitly tagged `CALIBRATE`, `EXTERNAL`, `DEFERRED` and `APPROVAL` items remain open in their proper evidence lanes.

No calibration result or research candidate silently changes production.
