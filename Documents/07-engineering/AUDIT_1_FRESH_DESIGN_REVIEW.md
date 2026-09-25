# GoldScalpTrader — Audit 1: Fresh Architecture Review and 100 Challenges

**Status:** COMPLETE DOCUMENTATION-LEVEL FRESH-ZERO / 100-CHALLENGE AUDIT
**Version:** 2.0-final-scalp-architecture-challenge
**Authority:** Architecture challenge from zero, preservation-first comparison, attack testing of design assumptions and final pre-implementation recommendation.

## 1. Audit question

> If GoldScalpTrader were built from zero today, while preserving GoldSwingTraderAI features/defaults except where Scalp needs a difference or the operator explicitly changed one, would this architecture maximize qualified accurate opportunities without becoming either a restriction machine or an unsafe overtrading machine?

## 2. Final architecture under challenge

```text
normalized MT5 facts
→ immutable MarketSnapshot
→ causal intelligence
→ market-first Setup Detector across six families
→ Strategy Isolation: 1 ACTIVE_EXECUTION + 5 SHADOW_ONLY
→ active family eligible only when its own setup exists
→ active BUY/SELL + Red Team
→ persistent M5 Opportunity
→ subordinate M1 entry refinement
→ structural TradePlan
→ fresh Executable Quality
→ preserved monetary Risk
→ objective hard broker/session/account/exposure/controller authorities
→ Gate
→ one-shot Intent
→ sole MT5Writer
→ reconciliation
→ ManagedTrade
→ verified close
→ continuous learning/discovery/invention/ML
→ automated evidence stages
→ APPROVAL_REQUIRED before production promotion
```

## 3. Verdict scale

```text
PASS            architecture already addresses challenge
STRENGTHEN      architecture valid but documentation/test requirement added
CALIBRATE       dimension valid; numerical value needs evidence
EXTERNAL PROOF  current broker/platform fact required
DEFERRED        deliberately outside current architecture
REJECT CHANGE   proposed alternative would make system worse / violate operator rule
```

# 4. 100 challenges

## A. Product objective / opportunity efficiency

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 1 | What if maximizing win rate reduces profitable opportunity count drastically? | PASS | Objective is after-cost qualified edge + recall/capture, not win rate alone. |
| 2 | What if maximizing trade count forces weak setups? | PASS | 120/day is benchmark, not quota. |
| 3 | What if low trade count is caused by architecture rather than market scarcity? | STRENGTHEN | Blocker funnel + false-block/missed-opportunity metrics required. |
| 4 | What if one position stays open and suppresses many better scalps? | CALIBRATE | Track slot-occupancy opportunity cost and time-efficiency exits; capacity remains 1 initially. |
| 5 | What if selective filters look accurate but eliminate most valid moves? | PASS | Optional evidence is family-specific, not universal; measure false blocks. |
| 6 | What if loose qualification gives 120 trades but negative after-cost expectancy? | PASS | Net expectancy/cost quality required; throughput cannot override edge. |
| 7 | What if market conditions support 150 valid trades/day? | PASS | No arbitrary daily quota/cap from 120 benchmark. |
| 8 | What if only 40 valid trades exist? | PASS | No forced additional trades. |
| 9 | What if an apparently losing strategy has better opportunity capture after costs in another session? | CALIBRATE | Family/session segmented evidence required. |
| 10 | What if the system optimizes historical precision but cannot react quickly live? | STRENGTHEN | Stage latency telemetry + M1 refinement + executable revalidation required. |

## B. Setup detection / strategy architecture

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 11 | What if active strategy is forced onto every chart? | PASS | Market-first Setup Detector precedes active-family eligibility. |
| 12 | What if no recognized setup exists? | PASS | `Detected Setup = NONE`; live WAIT. |
| 13 | What if a valid shadow-family setup exists but active family setup does not? | PASS | Live WAIT; shadow setup recorded for research. |
| 14 | What if multiple setups genuinely qualify? | PASS | Preserve multiple candidates/lineage; active policy determines live eligibility afterward. |
| 15 | What if blended six-strategy voting hides which family has edge? | PASS | One live-active family at a time; other five shadow. |
| 16 | What if shadow families contaminate live confidence? | PASS | Shadow cannot vote a production trade into existence. |
| 17 | What if active family is poor and shadow family consistently superior? | PASS | Counterfactual evidence creates governed switch candidate; production switch approval-gated. |
| 18 | What if family definitions drift until they become identical filter soups? | STRENGTHEN | Family-specific required/supportive evidence + ablation/complexity review. |
| 19 | What if a genuinely new recurring market behavior is absent from six families? | PASS | Autonomous strategy invention may create `NEW_FAMILY` candidate; no silent live promotion. |
| 20 | What if future evidence supports dynamic routing between families? | DEFERRED | Dynamic Strategy Router is future candidate after clean isolation evidence + approval. |

## C. Indicators / structure / SMC / correlation

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 21 | What if EMA is highly useful but missing alignment blocks a valid sweep reversal? | PASS | EMA importance is family-specific, not universal. |
| 22 | What if RSI overbought/oversold rules create simplistic reversals? | PASS | RSI is context; no universal 70/30 trade command. |
| 23 | What if Fib improves pullback entries but harms other families? | PASS | Family-specific contribution/ablation. |
| 24 | What if every wick gets labelled liquidity sweep? | PASS | Pre-existing pool + causal penetration/failure/reclaim rules. |
| 25 | What if every opposite candle becomes an Order Block? | PASS | OB must be linked to meaningful causal structural consequence. |
| 26 | What if FVG/OB/sweep/MSS all come from one event and are counted five times? | PASS | Causal event lineage/correlation de-dup mandatory. |
| 27 | What if trendline/Fib/support all derive from same swing geometry? | PASS | Source/anchor IDs preserve correlation. |
| 28 | What if POC/tick volume is treated as centralized exchange truth? | PASS | Broker-local source labelled explicitly. |
| 29 | What if H1 trend blocks valid short-term reversal strategy? | PASS | H1 soft context, not universal veto. |
| 30 | What if historical swings use future confirmation unknowingly? | PASS | Pivot time vs confirmation/knowledge time + replay prefix tests. |

## D. Timeframes / M1 timing / freshness

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 31 | What if completed M5 timing is too slow for scalping? | PASS | M1 subordinate entry refinement approved. |
| 32 | What if M1 noise creates overtrading? | PASS | M1 cannot create Opportunity; M5 thesis required first. |
| 33 | What if M1 trigger is stale? | CALIBRATE | Trigger freshness dimension approved. |
| 34 | What if M5 setup remains technically valid but entry has escaped? | PASS | Chase/drift/MISSED semantics. |
| 35 | What if one missed trigger permanently deletes a still-valid setup? | PASS | Opportunity persists through WAIT where thesis survives. |
| 36 | What if terminal MISSED automatically re-arms next poll? | PASS | Fresh causal event required. |
| 37 | What if a restart restores stale READY state? | PASS | Fresh revalidation required; persisted READY not permission. |
| 38 | What if M1 becomes hidden seventh strategy? | PASS | Explicit non-authority + tests. |
| 39 | What if forming M1 candle leaks future final OHLC? | PASS | Causal completion/explicit telemetry boundary required. |
| 40 | What if event-age threshold differs by strategy? | CALIBRATE | Family/event-specific age policy supported. |

## E. TradePlan / geometry / target quality

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 41 | What if broad M15 stop makes a Breakout Retest artificially poor? | PASS | Prefer valid causal M5 retest-failure boundary. |
| 42 | What if reversal event has tighter true invalidation than generic swing? | PASS | Sweep/failed-break event extreme allowed when causally proven. |
| 43 | What if tight event extreme is chosen only because it improves R? | PASS | Must match active-family causal thesis; otherwise fallback. |
| 44 | What if minimum lot is unaffordable? | PASS | Reject current plan; never tighten structural stop to force 0.01. |
| 45 | What if inherited Swing 1.20R rejects profitable scalps? | PASS | No automatic hard 1.20R inheritance; Scalp minimum R calibrated. |
| 46 | What if too-low R floor admits cost-dominated trades? | CALIBRATE | Gross minimum + net/cost-adjusted quality both studied. |
| 47 | What if target room is measured from stale entry reference? | PASS | Fresh executable quote/current remaining room revalidated separately. |
| 48 | What if current deterioration rewrites original plan history? | PASS | Original TradePlan/R immutable; quality layer handles current state. |
| 49 | What if immediate obstacle exists before attractive farther target? | PASS | Immediate Obstacle reported separately from Primary/Expansion. |
| 50 | What if runner turns scalp into accidental swing? | PASS | Runner exceptional, fresh objective/evidence required. |

## F. Spread / costs / execution timing

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 51 | What if fixed spread limit is too restrictive in wide-stop setups? | PASS | Fixed emergency ceiling + spread/SL + spread/target. |
| 52 | What if spread is small absolutely but huge relative to target? | PASS | Spread/target approved dimension. |
| 53 | What if spread is small relative to target but huge relative to stop? | PASS | Spread/SL approved dimension. |
| 54 | What if cost model double-counts spread/slippage? | STRENGTHEN | Explicit cost decomposition + unit tests. |
| 55 | What if perfect-fill assumptions fake expectancy? | PASS | Slippage allowance + actual fill learning. |
| 56 | What if broker deviation is too tight and causes rejected good entries? | CALIBRATE | Dynamic bounded deviation needs connected evidence. |
| 57 | What if deviation is too loose and destroys edge? | CALIBRATE | Hard maximum + actual fill evidence. |
| 58 | What if decision→send latency exceeds budget but opportunity remains valid? | PASS | Fresh revalidation, not automatic death. |
| 59 | What if quote becomes stale between plan and send? | PASS | Final fresh quote/precheck. |
| 60 | What if event shock damages execution without News data? | PASS | Real spread/drift/dislocation/slippage facts, not News label, own response. |

## G. Monetary Risk / account safety

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 61 | What if Scalp redesign accidentally removed SMALL/MEDIUM/NORMAL profiles? | PASS | Profiles/restored bands explicitly preserved. |
| 62 | What if confidence score increases monetary Risk? | REJECT CHANGE | Risk independent; score cannot inflate risk. |
| 63 | What if aggressive mode auto-enables on small balance? | PASS | Explicit enable only, default disabled. |
| 64 | What if 8% becomes target instead of ceiling? | PASS | Contract/test wording says maximum, not target. |
| 65 | What if deposit makes daily P/L look profitable? | PASS | AccountSafetyPL adjusts identifiable non-trading cash flow. |
| 66 | What if cash-flow history is unavailable? | PASS | UNKNOWN, never zero. |
| 67 | What if process restart resets loss lock/cooldown? | PASS | Durable Risk state. |
| 68 | What if manual reset clears unrelated faults? | PASS | Reset only owning loss-lock state; disabled by default. |
| 69 | What if repeated same episode keeps re-entering? | PASS | Preserved one fresh same-episode re-entry baseline. |
| 70 | What if three-loss cooldown time expires but conditions remain bad? | PASS | Time + fresh/healthy release conditions required. |

## H. News / session / broker-state separation

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 71 | What if a scheduled News event blocks many good trades unnecessarily? | PASS | News removed from hard trading permission. |
| 72 | What if News API fails? | PASS | Context degrades; no direct hard block. |
| 73 | What if stale News cache is displayed as fresh? | PASS | Timestamp laundering prohibited. |
| 74 | What if News event actually causes huge spread? | PASS | Actual executable quality handles it. |
| 75 | What if holiday calendar missing but broker is actually closed? | PASS | Broker session truth is independent hard authority. |
| 76 | What if soft “London” label is mistaken for broker OPEN? | PASS | Session Context soft; broker market state hard/separate. |
| 77 | What if pre-close safety is removed to increase trade count? | REJECT CHANGE | Preserve broker/session safety baseline. |
| 78 | What if broker schedule changed since reference? | EXTERNAL PROOF | Verify current Exness schedule; factual update allowed. |
| 79 | What if market reopens with gap/dislocation? | PASS | Reopen warmup + gap/execution normalization. |
| 80 | What if provider transport carries session + News in one module and mixes authority? | PASS | Typed BrokerSessionFacts vs NewsContextFacts required. |

## I. Execution / persistence / multi-machine

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 81 | What if upstream TradePlan reject is displayed as Gate BLOCKED? | PASS | Gate NOT_EVALUATED distinction. |
| 82 | What if order_check fails but send still occurs? | PASS | Precheck failure → send count 0. |
| 83 | What if timeout occurs after broker may have accepted order? | PASS | ACCEPTED_UNKNOWN + reconcile, no retry. |
| 84 | What if process crashes after persisting SUBMITTING but before observing response? | PASS | Treat as potentially sent; reconcile. |
| 85 | What if two modules can call MT5 order functions? | PASS | Sole `mt5_writer.py` boundary. |
| 86 | What if manual Gold trade exists while bot is flat? | PASS | External exposure visible; never adopted; capacity blocks as required. |
| 87 | What if operator manually closes a known bot trade? | PASS | Exact deal/volume proof; close origin EXTERNAL/MIXED; valid trade outcome lineage. |
| 88 | What if restored database says position open but broker does not? | PASS | Broker reconciliation/exit history before clearing. |
| 89 | What if two laptops become PRIMARY for same account/symbol? | PASS | Current single-primary sequential handoff; active-active deferred. |
| 90 | What if distributed fencing is added now “for safety”? | REJECT CHANGE | Adds network/split-brain complexity without current need; deferred by operator approval. |

## J. Learning / ML / dashboard / operations

| # | Challenge | Verdict | Resolution |
|---:|---|---|---|
| 91 | What if AI tunes live parameters directly? | PASS | Candidate/shadow only; production approval boundary. |
| 92 | What if autonomous strategy invention generates arbitrary executable code? | PASS | Declarative bounded primitive candidates, not arbitrary live code. |
| 93 | What if candidate repeatedly tunes against final holdout? | PASS | One-shot holdout per locked fingerprint. |
| 94 | What if failed candidates are forgotten and rediscovered forever? | PASS | Durable rejection/suppression memory. |
| 95 | What if shadow P/L is mixed with real P/L? | PASS | Evidence classes separate; counterfactual never broker P/L. |
| 96 | What if dashboard recomputes Risk/Gate differently from runtime? | PASS | Read-only DTO/presentation; authority owner remains backend. |
| 97 | What if dashboard has decorative buttons that do nothing? | PASS | Functional chart-control contract + tests. |
| 98 | What if dashboard needs scrollbars and hides critical state? | PASS | Approved one-screen/no-scroll primary layout. |
| 99 | What if GitHub becomes runtime dependency or shutdown pushes code? | PASS | No runtime Git credentials/actions; local runtime recovery separate. |
| 100 | What if documentation itself becomes stale again after implementation? | STRENGTHEN | Affected-graph sync + document verifier + release checklist/audit mandatory. |

# 5. Additional cross-challenges beyond 100

To avoid designing exactly to a checklist, six additional meta-challenges were applied:

| # | Challenge | Verdict |
|---:|---|---|
| 101 | Can the bot distinguish “no setup” from “wrong active family”? | PASS — separate reasons required. |
| 102 | Can the bot distinguish analytical WAIT from hard financial BLOCK? | PASS — owner-specific states. |
| 103 | Can a good strategy still be rejected because current execution economics are bad? | PASS — Executable Quality independent. |
| 104 | Can poor execution economics recover without deleting the underlying Opportunity? | PASS where thesis/timing remains valid; revalidate rather than blindly terminalize. |
| 105 | Can research improve frequency without touching hard monetary/execution invariants? | PASS — search space excludes hard safety. |
| 106 | Can a new AI/developer rebuild the intended system without this chat? | PASS only after final 66-doc reconstruction/link audit; this is a documentation freeze gate. |

# 6. What would be built differently from a simplistic Scalp bot

Reject a monolithic rule such as:

```text
EMA cross + RSI threshold + News filter + fixed spread + fixed SL/TP
```

Prefer the current architecture because it separates:

- factual setup discovery;
- family eligibility;
- entry timing;
- structural geometry;
- current execution economics;
- monetary affordability;
- broker authority;
- post-entry management;
- learning/research.

This separation improves both opportunity capture and diagnosability.

# 7. Final recommendations after challenge

### KEEP

- preservation-first feature baseline;
- one normalized read boundary / immutable snapshot;
- six family definitions;
- one-at-a-time live Strategy Isolation for clean evaluation;
- market-first Setup Detector;
- active BUY/SELL + Red Team;
- persistent Opportunity;
- M5 thesis + M1 refinement;
- family-aware TradePlan;
- preserved Risk profiles;
- central Gate/Intent/sole writer/reconciliation;
- time-efficiency management;
- continuous learning/invention/ML with approval gate;
- Swing-style one-screen graphical dashboard;
- local-first runtime recovery.

### CHANGE / already approved

- News removed from hard trading permission/cooldown/warmup;
- M1 promoted from diagnostic-only to subordinate production entry refinement;
- physical analytical parallelism profiling-driven;
- spread policy = fixed emergency + aware ratios/cost;
- no automatic inherited 1.20R hard Scalp floor;
- setup detection explicitly precedes active-family eligibility;
- graphical dashboard made primary approved one-screen UX.

### CALIBRATE

- M1 patterns/freshness;
- M5 event age;
- chase/drift;
- emergency spread ceiling;
- spread/SL and spread/target acceptable ranges;
- cost/reward;
- slippage/deviation/latency;
- minimum gross/net quality;
- family thresholds/weights/correlation caps;
- session performance;
- protection/trailing/time-exit/Runner/partial-close evidence;
- PRE_CLOSE/reopen-gap exact current behavior;
- throughput capability against ~120/day benchmark.

### DEFER

- same-account active-active writer;
- distributed DB/fencing/consensus;
- mandatory paid News API;
- GitHub Actions/cloud compute dependency;
- sophisticated partial-close optimizer as release dependency.

# 8. Final Audit 1 verdict

> **Architecture accepted for implementation after documentation freeze.**

The strongest remaining risks are not conceptual architecture gaps; they are evidence/calibration and implementation correctness:

1. whether actual XAU/Exness execution costs allow the desired opportunity throughput;
2. which family thresholds/M1 refinements maximize after-cost edge;
3. whether one-position capacity materially suppresses opportunities;
4. current broker schedule/spec/execution facts;
5. whether the implementation preserves one-shot/recovery/authority semantics;
6. whether autonomous research produces robust challengers without overfit.

No design change should be introduced merely to increase trade count or simplify coding without returning through the affected documentation/governance path.
