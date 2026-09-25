# GoldScalpTrader — Shared Glossary

**Status:** FINAL CANONICAL VOCABULARY — DOCUMENTATION FREEZE BASELINE
**Version:** 2.0-institutional-scalp
**Authority:** Shared terminology used by every GoldScalpTrader document, implementation, test, dashboard and audit.

## 1. Documentation / governance

| Term | Canonical meaning |
|---|---|
| Canonical Documents manual | The single active `Documents/` design/build/proof authority for GoldScalpTrader. |
| Preservation-first rule | Preserve GoldSwingTraderAI feature/default behaviour unless a direct scalp requirement, explicit operator decision or proven reference defect justifies a governed difference. |
| Affected-graph sync | When one policy changes, update its owner plus every relevant architecture, operator, engineering, test and governance consumer. |
| Calibration | Architecture/dimension is approved, but the numerical value needs evidence. |
| External proof | Current broker/platform/environment fact must be verified in the real intended environment. |
| Approval Required | Research/candidate work may continue, but production/live promotion stops until explicit operator approval. |

## 2. Market / setup vocabulary

| Term | Canonical meaning |
|---|---|
| MarketSnapshot | One immutable normalized cycle snapshot of account/symbol/quote/completed candles and required exposure facts. |
| IntelligenceSnapshot | Causal reusable structure, technical, liquidity, quant, session and soft News context built from one MarketSnapshot. |
| Setup Detector | Analytical process that asks what recognizable setup the chart/market currently forms; it never forces the currently active strategy onto unrelated market behaviour. |
| Setup Candidate | A causally detected market pattern that appears to match one strategy-family definition; may be active-family eligible or shadow-only. |
| Detected Setup | Best currently qualified setup classification with evidence/reasons, or `NONE/WAIT` when nothing qualifies. |
| Strategy Family | One independent market hypothesis/recipe with no monetary or broker authority. |
| ACTIVE_EXECUTION family | Exactly one strategy family currently eligible to originate live production Opportunities during isolation testing. It may trade only when its own setup is actually detected/qualified. |
| SHADOW_ONLY family | Strategy family that analyzes and records counterfactual opportunities but cannot originate live production trades. |
| Strategy Isolation Mode | One live trade-producing family at a time for clean efficiency attribution; the other five remain shadow/research. |
| Dynamic Strategy Router | Future candidate capability that could select among proven families by detected setup. It is **not current production behaviour** and requires evidence + approval. |
| BUY / SELL thesis | Independent directional cases inside the active setup/family; absence of one is not automatic proof of the other. |
| Red Team | Analytical challenge of the active-family thesis; never monetary/broker authority. |
| Opportunity | Durable identity for a qualified active-family M5 thesis that may persist while timing waits. |
| Episode | Causal market episode that groups Opportunity/re-entry lineage without allowing next-poll identity reset. |

## 3. Timeframe / chronology

| Term | Canonical meaning |
|---|---|
| H4 context | Optional major context only; soft. |
| H1 regime | Broad soft directional/volatility context. |
| M15 opportunity context | Location, path, liquidity and target-room context. |
| M5 production setup | Primary completed-bar setup/thesis and normal management structure. |
| M1 refinement | Subordinate micro-entry refinement **after** a valid M5 Opportunity exists; cannot independently create a production trade. |
| Quote/current tick | Current executable Bid/Ask/spread/drift/freshness truth, not historical structural proof. |
| Knowledge time | Earliest moment a fact could causally be known. |
| Completed candle | Closed bar allowed to become confirmed bar-based structure. |
| Signal Price | Price where causal evidence formed. |
| Approved Entry Reference | Price reference used to construct TradePlan geometry. |
| Executable Quote | Fresh side-specific Bid/Ask used for current economic/execution validation. |
| Actual Fill | Broker-confirmed executed price. |
| Trigger/Event age | Time/bars since setup/refinement evidence became knowable. |
| Chase | Current price has moved far enough from intended geometry that entry efficiency may be damaged. |
| Drift | Movement between approved/reference price and current executable price. |
| Re-arm | New timing opportunity only after genuinely fresh causal evidence and applicable re-entry policy. |

## 4. Strategy families

Preserved six production families:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Important evidence such as EMA, RSI, Fib, FVG, OB, Trendline and POC may be `REQUIRED_FOR_THIS_FAMILY`, `STRONG_SUPPORT`, `OPTIONAL_SUPPORT`, `OPPOSITION`, `NOT_RELEVANT` or `UNKNOWN`. Importance to one family never makes it a universal checklist for all trades.

## 5. Timing / plan / executable quality

| Term | Canonical meaning |
|---|---|
| READY | Analytical timing is currently suitable; not broker permission. |
| WAIT | Setup survives but current entry moment is not efficient/ready. |
| MISSED | Exact current entry opportunity escaped/staled economically. |
| INVALID | Underlying thesis/geometry failed. |
| TradePlan | Structural invalidation/SL, objectives and gross geometry constructed before monetary sizing. |
| Structural stop | Thesis invalidation price; never tightened merely to make minimum lot affordable. |
| Immediate Obstacle | Nearest meaningful opposing structural/path fact. |
| Primary Target | First credible structural objective. |
| Expansion Target | Next credible continuation objective. |
| Runner Objective | Exceptional further objective; profit alone does not justify runner mode. |
| Original R | Immutable initial structural risk basis used for later performance analysis. |
| Gross R | Structural reward/risk before current transaction-cost burden. |
| Executable Quality | Current economic usability of a structurally valid plan using fresh quote, spread, drift, latency and costs. |
| Emergency spread ceiling | Absolute circuit-breaker for clearly pathological spread; exact value is calibrated. |
| Spread/SL | Current spread divided by structural stop distance. |
| Spread/Target | Current spread divided by remaining credible target room. |
| Cost/Reward | Expected transaction-cost burden relative to expected reward. |
| Slippage allowance | Pre-fill estimate/reserve for plausible fill deterioration; calibrated from DEMO evidence. |
| Broker deviation | Bounded request tolerance for permitted price movement where execution mode supports it. |
| Decision→send latency | Time from final actionable decision to broker send; excess age normally triggers fresh revalidation rather than automatic permanent rejection. |

## 6. Risk vocabulary

| Term | Canonical meaning |
|---|---|
| DayStartEquity profile | Automatic account Risk profile resolved at the UTC risk-day boundary and fixed for that risk day. |
| SMALL | Positive DayStartEquity below $300. Normal 3.0–4.5%, elevated >4.5–6.5%, hard ceiling 7%, daily lock 12%. |
| MEDIUM | DayStartEquity $300–$999.99. Normal 2.0–3.0%, elevated >3.0–4.5%, hard ceiling 5%, daily lock 9%. |
| NORMAL | DayStartEquity >= $1,000. Normal 1.0–2.0%, elevated >2.0–3.5%, hard ceiling 4%, daily lock 7%. |
| AGGRESSIVE_SMALL_ACCOUNT | Explicit optional sub-$1,000 overlay; disabled by default and never auto-enabled from balance alone. |
| 8% aggressive ceiling | Maximum single-trade monetary SL-risk ceiling when explicitly enabled; **not a sizing target**. |
| 16% aggregate ceiling | Maximum aggregate open risk under aggressive mode. |
| 16% aggressive daily ceiling | Daily-loss ceiling under aggressive mode. |
| Minimum-lot affordability | Whether broker minimum executable volume fits active monetary policy using the real structural stop. |
| Account Safety P/L | Whole-account risk-day equity change adjusted for identifiable non-trading cash flow. |
| Bot Performance P/L | Bot-attributed trading performance, separated from manual/external activity. |
| Same-episode re-entry | Preserved baseline allowance of one genuinely fresh re-entry under current policy. |
| Global loss cooldown | Three consecutive closed bot losses → at least 30 minutes plus fresh/healthy release conditions. |
| Manual daily-loss reset | Preserved governed capability, disabled by default; cannot clear unrelated hard faults. |

## 7. Session / News vocabulary

| Term | Canonical meaning |
|---|---|
| Session Context | Asia/London/New York/overlap descriptive context and performance segmentation; soft. |
| Broker Market State | `OPEN`, `PRE_CLOSE`, `CLOSED`, `REOPEN_WARMUP` or `UNKNOWN`; hard factual authority where required. |
| News Context | Scheduled-event/macro information used for dashboard, explanation and research; **not hard trading permission**. |
| Provider Health | Acquisition-source condition such as VERIFIED, DEGRADED, STALE, UNAVAILABLE or UNKNOWN. |
| LKG cache | Last-known-good News/context data kept with original provenance/timestamps; useful for context continuity, not broker permission. |
| Provider TTL baseline | 1800 seconds retained as context-freshness baseline unless later evidence changes it. Expiry does not hard-block trading by itself. |
| Daily PRE_CLOSE baseline | T-20 no new entry / T-10 mandatory governed flatten, subject to current broker proof. |
| Weekend PRE_CLOSE baseline | T-60 no new entry / T-30 mandatory governed flatten. |
| Daily reopen baseline | One clean completed M5 plus healthy broker/execution state. |
| Weekend reopen baseline | Two clean completed M5 + gap assessment + healthy broker/execution state. |

## 8. Execution / ownership

| Term | Canonical meaning |
|---|---|
| ExecutionPermissionGate | Central ordered composition of required hard authorities for one irreversible action. |
| Gate NOT EVALUATED | An upstream owner already stopped the path; do not falsely label Gate BLOCKED. |
| ExecutionIntent | Durable unique one-shot action identity persisted before irreversible submission. |
| One-shot submission | One Intent ID has at most one irreversible send allowance. |
| Accepted Unknown | Broker effect may exist but final truth is unresolved; blind resend prohibited. |
| MT5Writer | Sole raw MetaTrader5 irreversible write boundary. |
| Reconciliation | Verify attempted action against current broker positions/orders/deals instead of guessing. |
| Controller/Fencing | Ensures only the current valid local PRIMARY holder/epoch can write for one scope. |
| Capacity | Initial one independently risk-bearing Gold position per account/symbol scope. |
| External/manual exposure | Gold exposure not proven bot-owned; never silently adopted. |
| ManagedTrade | Durable bot-owned post-entry lifecycle identity. |
| Verified close | Exact known-trade broker lineage/outcome proven sufficiently for accounting/learning. |

## 9. Management

| Term | Canonical meaning |
|---|---|
| HOLD | Thesis healthy; no justified change. |
| PROTECT | Reduce open risk after progress/structure earns protection. |
| TRAIL | Move stop using earned structure; never widen approved risk. |
| RUNNER | Exceptional continuation mode with fresh objective/evidence. |
| EXIT | Governed close because thesis, path, time efficiency, PRE_CLOSE or another owning reason requires it. |
| Time-efficiency EXIT | Normal EXIT reason when a scalp fails calibrated progress expectations; not a separate action enum. |
| Partial management | Optional broker-valid partial action where volume is divisible; minimum-lot correctness never depends on it. |

## 10. Learning / research

| Term | Canonical meaning |
|---|---|
| StrategyMemory | Durable actual-trade observations/summaries with exactly-once source identity. |
| Actual Active evidence | Verified production/DEMO outcome from the currently active family. |
| Shadow Counterfactual | What a shadow family would have done; never broker P/L. |
| Missed Opportunity | Meaningful untraded opportunity measured for recall/efficiency research. |
| Candidate | Versioned research strategy/parameter/model hypothesis with no automatic production authority. |
| Autonomous Invention | Backend generation of new declarative candidates from audited primitives/evidence. |
| Automatic Stage Progression | Candidate may progress through research/validation/holdout/stress/shadow/DEMO evidence stages where contracts allow. |
| Production Promotion | Versioned live policy change; always stops at `APPROVAL_REQUIRED` until operator approval. |
| Qualified Opportunity Recall | How many genuine qualifying opportunities were found. |
| Opportunity Capture Rate | How many qualifying opportunities became actual trades. |
| Entry/Capture/Exit Efficiency | Quality of actual entry, move capture and exit relative to available causal path. |
| 120 trades/day benchmark | Research throughput capability question; never a forced quota. |

## 11. Runtime / backup

| Term | Canonical meaning |
|---|---|
| READINESS | Read-only diagnostic/identity/data/recovery stage. |
| DRY_RUN | Full governed analytical/risk/permission path with zero irreversible broker writes. |
| DEMO PRIMARY | One active governed DEMO writer per account/symbol scope after its evidence gate. |
| Future REAL | Preserved future capability requiring separate DEMO/release proof and explicit operator approval. |
| Runtime checkpoint | Consistent verified snapshot/export of durable runtime/research state. |
| Source backup | Local Git + GitHub source/history remote; optional secret-clean milestone ZIP. |
| Sequential handoff | Stop old same-scope PRIMARY, transfer verified state, restore/reconcile on new machine, then acquire new controller. |
| Distributed DB/fencing | Same-scope active-active distributed infrastructure; explicitly deferred. |

## 12. Dashboard vocabulary

| Term | Canonical meaning |
|---|---|
| Primary graphical dashboard | Approved Swing-style one-screen institutional layout adapted to Scalp; no scrollbars. |
| Functional chart controls | M1/M5/M15/H1/H4, Indicators, Drawings and Settings controls perform real UI/state actions rather than decorative clicks. |
| Detected Setup panel | Displays what the market currently forms and why, independent of whether that family is live-eligible. |
| Active Test Family | The one strategy currently allowed to originate live trades under isolation testing. |
| Shadow Detected Setup | Valid setup detected for a non-active family; shown/researched but live action remains WAIT. |
| Current Blocker | Exact upstream owner/reason, distinct from actual Gate state. |

## 13. Evidence status vocabulary

Use precise claims:

```text
APPROVED DOCUMENTED DESIGN
DOCUMENTATION FROZEN
IMPLEMENTATION PENDING / IMPLEMENTED
DETERMINISTIC PROOF PENDING / PASS
CALIBRATION PENDING
EXTERNAL PROOF PENDING / PASS
CONNECTED DEMO PENDING / PASS
APPROVAL_REQUIRED
DEFERRED
NOT RUN
```

Never treat documentation, unit tests, replay, DEMO and profitability as the same evidence class.
