# GoldScalpTrader — Design Decision Ledger

**Status:** ACTIVE RECONSTRUCTION DECISION LEDGER — OPERATOR-APPROVED ARCHITECTURE RECORDED
**Version:** 2.0-institutional-rebuild-decisions
**Authority:** Durable approved project decisions, supersession, calibration classification and explicit operator changes. Topic contracts own exact implementation details.

## 1. Status vocabulary

```text
ACTIVE        approved current architecture/policy
PRESERVED     reference behavior explicitly retained
SUPERSEDED    historical decision replaced by later decision
CALIBRATE     architecture/dimension approved; numerical/empirical threshold needs evidence
EXTERNAL      current broker/platform/environment fact requires connected proof
DEFERRED      deliberately outside current enabled architecture/release dependency
APPROVAL      production/live change requires explicit operator approval
```

## 2. Documentation / process decisions

| ID | Decision | Status |
|---|---|---|
| DEC-001 | Documents are designed/challenged before implementation expansion; code must not outrun them | ACTIVE |
| DEC-002 | `Documents/` is the durable reconstructable project baseline | ACTIVE |
| DEC-003 | Latest verified GoldSwingTraderAI `Published_B/Documents` is the structural/depth reference for reconstruction | ACTIVE |
| DEC-004 | Canonical reference target is **66 Markdown docs**, not 64 | ACTIVE |
| DEC-005 | Missing `GITHUB_STRICT_USE_POLICY.md` and `BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md` must exist in Scalp | ACTIVE |
| DEC-006 | Every useful reference section is preserved/adapted/classified; no silent compression/removal for convenience | ACTIVE |
| DEC-007 | Substantive docs use diagrams/tables/state/sequence visuals where meaningful | ACTIVE |
| DEC-008 | Empirical charts use real replay/DEMO evidence only; fake performance charts prohibited | ACTIVE |
| DEC-009 | Final folder numbering becomes `01`–`08` in one atomic rename/link migration | ACTIVE |
| DEC-010 | One canonical authority owner per rule; consumer docs remain deeply explanatory mirrors | ACTIVE |
| DEC-011 | Final freeze requires reference→Scalp coverage, cross-link validation, 100+ challenge and operator approval | ACTIVE |

## 3. Product objective

| ID | Decision | Status |
|---|---|---|
| DEC-020 | Product philosophy = Opportunity-First, Evidence-Weighted, Precision-Timed, Cost-Aware, Execution-Disciplined, Continuously-Learning | ACTIVE |
| DEC-021 | Optimize qualified after-cost edge captured, not merely win rate or low trade count | ACTIVE |
| DEC-022 | Avoid unnecessary analytical restrictions; hard blocks reserved for objective required Risk/broker/lifecycle facts | ACTIVE |
| DEC-023 | 120 trades/day is a research throughput benchmark/capability question, never a forced quota | ACTIVE |
| DEC-024 | Track Opportunity Recall, Capture Rate, Net Expectancy, Entry/Capture/Exit Efficiency, false blocks, missed opportunity cost, cost burden and throughput | ACTIVE |

## 4. Market/timeframe decisions

| ID | Decision | Status |
|---|---|---|
| DEC-040 | Completed-candle + causal knowledge-time rules remain mandatory | PRESERVED |
| DEC-041 | H1 = broad regime/context | ACTIVE |
| DEC-042 | M15 = opportunity location/path/target context | ACTIVE |
| DEC-043 | M5 = primary setup/thesis + normal management structure | ACTIVE |
| DEC-044 | H4 = optional major context, never universal veto | ACTIVE |
| DEC-045 | **M1 becomes subordinate entry refinement after a valid M5 Opportunity** | ACTIVE |
| DEC-046 | M1 cannot independently originate a production trade | ACTIVE |
| DEC-047 | Quote/tick = current executable condition; cannot retroactively prove historical structure | ACTIVE |
| DEC-048 | M1 patterns/freshness, M5 event age, chase distance and Approved Entry→Executable Price drift are calibration dimensions | CALIBRATE |
| DEC-049 | Production tick-history authority remains unchanged from preserved reference unless separately approved | PRESERVED |

## 5. Strategy-floor / isolation decisions

| ID | Decision | Status |
|---|---|---|
| DEC-060 | Preserve six families: Trend Pullback, Breakout Expansion, Breakout Retest, Liquidity Sweep Reversal, Failed Breakout Reversal, Compression Expansion | PRESERVED |
| DEC-061 | **Exactly one family is `ACTIVE_EXECUTION` at a time for live trade production** | ACTIVE |
| DEC-062 | Remaining five families are `SHADOW_ONLY`; they analyze/research but cannot originate live trades | ACTIVE |
| DEC-063 | Active family evaluates BUY/SELL independently | ACTIVE |
| DEC-064 | Red Team challenges active-family thesis; shadow signals cannot vote a trade into existence | ACTIVE |
| DEC-065 | Active-family switching is versioned/governed and preserves historical attribution | ACTIVE |
| DEC-066 | Persistent Opportunity remains distinct from entry timing | PRESERVED |
| DEC-067 | Terminal Opportunity requires genuinely fresh causal event to re-arm | PRESERVED |
| DEC-068 | Correlated evidence retains event lineage and cannot become fake independent confirmation | PRESERVED |
| DEC-069 | Exact family qualification thresholds | CALIBRATE |
| DEC-070 | Fusion/analytical weights may be used transparently/bounded; exact weights require evidence | CALIBRATE |
| DEC-071 | Family correlation caps/de-duplication dimensions require calibration; de-duplication itself is mandatory | CALIBRATE |

## 6. Indicators/confluence/session context

| ID | Decision | Status |
|---|---|---|
| DEC-080 | EMA/RSI/Fib/FVG/OB/Trendline/POC may be very important to relevant families but are not unrelated universal hard vetoes | ACTIVE |
| DEC-081 | A family may require evidence central to its own definition without forcing the same evidence on other families | ACTIVE |
| DEC-082 | London/NY/Asia performance is tracked per family and may influence future evidence-based tuning, not blanket session bans by default | CALIBRATE |
| DEC-083 | Session analytical context is soft; actual broker OPEN/CLOSED/PRE_CLOSE remains hard factual authority | ACTIVE |

## 7. Physical parallelism / performance decisions

| ID | Decision | Status |
|---|---|---|
| DEC-100 | One normalized MT5 analytical read boundary + immutable snapshot | PRESERVED |
| DEC-101 | Logical specialist/family independence is mandatory | ACTIVE |
| DEC-102 | **Physical analytical parallelism is profiling-driven, not mandatory** | ACTIVE |
| DEC-103 | Optimization order: shared calculations → vectorize/cache → profile → bounded parallelism only if faster | ACTIVE |
| DEC-104 | One-worker and parallel modes must be semantically identical and deterministic | ACTIVE |
| DEC-105 | Financial/broker authority remains strictly serial | PRESERVED |
| DEC-106 | Track critical-path latency by stage, including decision→send | ACTIVE |

## 8. TradePlan / executable-quality decisions

| ID | Decision | Status |
|---|---|---|
| DEC-120 | TradePlan freezes structural geometry before monetary Risk | PRESERVED |
| DEC-121 | Structural SL is never tightened merely to make minimum lot affordable | PRESERVED |
| DEC-122 | Swing 1.20R floor is not automatically imposed as hard Scalp entry floor | ACTIVE |
| DEC-123 | Minimum gross R requires evidence | CALIBRATE |
| DEC-124 | Minimum net/cost-adjusted opportunity quality requires evidence | CALIBRATE |
| DEC-125 | Fixed + aware spread architecture is approved | ACTIVE |
| DEC-126 | Absolute emergency spread ceiling retained as circuit breaker; exact ceiling | CALIBRATE |
| DEC-127 | Spread/SL ratio is an approved executable-quality dimension | ACTIVE |
| DEC-128 | Spread/target ratio is an approved executable-quality dimension | ACTIVE |
| DEC-129 | Total cost/reward ratio is an approved executable-quality dimension | CALIBRATE |
| DEC-130 | Slippage allowance is calibrated from real/DEMO broker evidence rather than an arbitrary huge constant | CALIBRATE |
| DEC-131 | Broker deviation is bounded/dynamic by execution mode and broker evidence | CALIBRATE |
| DEC-132 | Decision→send latency outside budget normally triggers fresh quote/geometry/Risk revalidation, not automatic permanent rejection | CALIBRATE |

## 9. Monetary Risk decisions — do not change baseline

| ID | Decision | Status |
|---|---|---|
| DEC-140 | Monetary Risk remains independent hard authority | PRESERVED |
| DEC-141 | Preserve SMALL/MEDIUM/NORMAL automatic profiles | PRESERVED |
| DEC-142 | Preserve exact existing risk bands/percentages; do not change them during this reconstruction | PRESERVED |
| DEC-143 | Dynamic broker-aware sizing/min-lot actual-risk check remains | PRESERVED |
| DEC-144 | No arbitrary $100 minimum-account eligibility floor | PRESERVED |
| DEC-145 | One independently risk-bearing Gold position per scope initially | PRESERVED |
| DEC-146 | No martingale/grid/averaging-down rescue | PRESERVED |
| DEC-147 | Aggressive small-account mode remains operational capability, disabled by default | PRESERVED |
| DEC-148 | Aggressive semantics: 8% max single-trade SL-risk ceiling (not target), 16% aggregate, 16% daily | PRESERVED |
| DEC-149 | Manual daily-loss reset capability preserved, disabled by default | PRESERVED |
| DEC-150 | One genuinely fresh same-episode re-entry baseline preserved; future alternatives researchable | PRESERVED / CALIBRATE |
| DEC-151 | Three consecutive closed bot losses → at least 30m cooldown baseline preserved; future alternatives researchable | PRESERVED / CALIBRATE |
| DEC-152 | Current UTC risk-day behavior stays baseline; typed/configurable policy identity may be architected but cannot be used to reset losses casually | PRESERVED |

### Canonical preserved profile table

| Profile | DayStartEquity | Normal | Elevated | Hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|---:|
| SMALL | positive < $300 | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | $300–$999.99 | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | >= $1,000 | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

## 10. News/Fundamental decisions — superseding prior hard-block model

| ID | Decision | Status |
|---|---|---|
| DEC-160 | Fundamental/News remains soft context, dashboard and research attribution | ACTIVE |
| DEC-161 | **Known News event no longer directly hard-blocks trading** | ACTIVE |
| DEC-162 | **News UNKNOWN/provider/API failure no longer directly hard-blocks trading** | ACTIVE |
| DEC-163 | **News-based cooldown and mandatory post-News warmup are removed** | ACTIVE |
| DEC-164 | Actual event-induced bad market conditions are governed by spread/drift/dislocation/quote/cost/slippage/latency/broker facts | ACTIVE |
| DEC-165 | Provider health/provenance remains visible and truthful; missing News is not renamed CLEAR | ACTIVE |
| DEC-166 | Mandatory paid third-party News API is not required | DEFERRED |

Historical News hard-block decisions are superseded by DEC-160–166.

## 11. Broker/session/execution decisions

| ID | Decision | Status |
|---|---|---|
| DEC-180 | Actual broker OPEN/CLOSED/symbol tradeability remains hard factual authority | PRESERVED |
| DEC-181 | Daily PRE_CLOSE T-20/T-10 baseline preserved; exact schedule evidence/calibration approved | PRESERVED / CALIBRATE |
| DEC-182 | Weekend PRE_CLOSE T-60/T-30 baseline preserved; exact schedule evidence/calibration approved | PRESERVED / CALIBRATE |
| DEC-183 | Daily reopen one clean M5 and weekend two clean M5 + gap baseline preserved; thresholds researchable | PRESERVED / CALIBRATE |
| DEC-184 | Central Gate remains distinct from upstream TradePlan/Quality/Risk blockers | PRESERVED |
| DEC-185 | Persist one-shot Intent before irreversible broker request | PRESERVED |
| DEC-186 | Sole MT5Writer owns raw irreversible operations | PRESERVED |
| DEC-187 | Ambiguous acknowledgement → reconciliation, never blind retry | PRESERVED |
| DEC-188 | Controlled DEMO precedes future governed REAL | PRESERVED |
| DEC-189 | REAL production activation requires its separate evidence/release gates and explicit operator approval | APPROVAL |

## 12. Management decisions

| ID | Decision | Status |
|---|---|---|
| DEC-200 | Management actions remain HOLD/PROTECT/TRAIL/RUNNER/EXIT | PRESERVED |
| DEC-201 | Time/efficiency weakness is a first-class EXIT reason | ACTIVE / CALIBRATE |
| DEC-202 | Protection/trailing timing is evidence-calibrated | CALIBRATE |
| DEC-203 | Runner remains optional/exceptional; exact continuation conditions | CALIBRATE |
| DEC-204 | Basic broker-valid partial-management capability preserved where divisible | PRESERVED |
| DEC-205 | Partial-close expectancy/optimization is researched; sophisticated optimization is not release dependency | CALIBRATE / DEFERRED |
| DEC-206 | Correctness at broker minimum lot cannot depend on partial close | PRESERVED |

## 13. Learning / AI / invention / promotion decisions

| ID | Decision | Status |
|---|---|---|
| DEC-220 | Learning remains downstream from verified evidence | PRESERVED |
| DEC-221 | Actual, missed, blocked, shadow/counterfactual and system-fault evidence remain distinguishable | ACTIVE |
| DEC-222 | Autonomous strategy invention remains an active backend capability | ACTIVE |
| DEC-223 | AI/candidate parameter optimization remains active backend capability | ACTIVE |
| DEC-224 | Advanced ML research remains active backend capability | ACTIVE |
| DEC-225 | Candidates may automatically progress through governed evidence stages where contracts allow | ACTIVE |
| DEC-226 | Candidate research may change candidate/shadow parameters, not current production silently | ACTIVE |
| DEC-227 | Final production/live promotion always stops at `APPROVAL_REQUIRED` until operator explicitly approves | APPROVAL |
| DEC-228 | Candidate cannot acquire broker-write authority directly | PRESERVED |

## 14. Persistence / machine / backup decisions

| ID | Decision | Status |
|---|---|---|
| DEC-240 | SQLite/local transactional state remains current target | PRESERVED |
| DEC-241 | Runtime shutdown performs no Git commit/push/pull | PRESERVED |
| DEC-242 | Development source checkpoint = coherent remote commit → operator `git pull --ff-only` | PRESERVED |
| DEC-243 | Optional secret-clean source ZIP/off-site package is separate from runtime state | PRESERVED |
| DEC-244 | Same-account active-active/distributed broker writer is deferred | DEFERRED |
| DEC-245 | Distributed DB/fencing/consensus infrastructure is deferred | DEFERRED |
| DEC-246 | Sequential same-account machine handoff remains supported target | PRESERVED |
| DEC-247 | Restore context never outranks current broker truth | PRESERVED |
| DEC-248 | `GITHUB_STRICT_USE_POLICY.md` and backup architecture are canonical top-level docs | ACTIVE |

## 15. GitHub / repository decisions

| ID | Decision | Status |
|---|---|---|
| DEC-260 | GitHub is source/history/collaboration remote, never trading-runtime dependency | PRESERVED |
| DEC-261 | No GitHub Actions/cloud compute dependency | DEFERRED |
| DEC-262 | Low-churn coherent commits; stop retry storms on remote errors | ACTIVE |
| DEC-263 | Repository visibility is currently public and **must not be changed now** without later explicit operator approval | ACTIVE |
| DEC-264 | Future privacy recommendation does not authorize a visibility mutation | ACTIVE |

## 16. Documentation reconstruction decisions

| ID | Decision | Status |
|---|---|---|
| DEC-280 | Current compressed Scalp docs are not sufficient merely because filenames exist | ACTIVE |
| DEC-281 | Reconstruct every document to reference-equivalent-or-better coverage | ACTIVE |
| DEC-282 | Restore full audit/source-test/recovery/state-machine detail | ACTIVE |
| DEC-283 | Code later must be expert-level: clean, optimized, typed, explicit docstrings/comments for non-obvious reasoning/safety | ACTIVE |
| DEC-284 | Comments explain why/invariants/broker quirks/chronology, not trivial syntax narration | ACTIVE |

## 17. Historical decisions explicitly superseded

The following prior Scalp decisions are no longer current authority:

```text
M1 diagnostic/research only
physical bounded analytical concurrency required by default
News BLACKOUT as automatic hard new-entry block
News UNKNOWN as automatic hard new-entry block
News-triggered mandatory post-event warmup/cooldown
64-file manual complete
final documentation review ready before full reference-depth reconstruction
```

They remain useful project history but must disappear from current behavioral topic owners during reconstruction.

## 18. Freeze rule

The architecture may be frozen while numerical items remain `CALIBRATE` and broker facts remain `EXTERNAL`, provided:

- their dimensions/owners are explicit;
- production defaults are explicit;
- no calibration variable is silently guessed into permanent policy;
- operator-approved preserved values are not changed;
- production-changing research remains approval-gated.

No decision is a profitability guarantee.
