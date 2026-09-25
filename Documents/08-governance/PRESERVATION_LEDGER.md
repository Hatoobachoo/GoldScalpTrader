# GoldScalpTrader — Documentation Preservation Ledger

**Status:** FINAL PRESERVATION LEDGER — DOCUMENTATION FREEZE BASELINE
**Version:** 2.0-reference-preserved-final
**Authority:** Proof that reference features/defaults remain unless classified as Scalp-specific, operator-directed or defect/fact correction.

## 1. Preservation rule

```text
GoldSwingTraderAI feature/default
→ preserve by default
→ change only for direct Scalp reason
   OR explicit operator instruction
   OR proven reference defect/current factual correction
```

A simpler implementation is never enough reason to remove a feature.

## 2. Preservation classification

Every inherited subject must be one of:

```text
PRESERVED
SCALP-SPECIFIC CHANGE
OPERATOR-DIRECTED CHANGE
REFERENCE DEFECT CORRECTION
EXTERNAL FACT UPDATE
CALIBRATION PENDING
DEFERRED BY APPROVAL
```

Unclassified removal is a documentation defect.

## 3. Preserved system spine

| Reference subject | Final status |
|---|---|
| documentation-first governance | PRESERVED |
| one normalized MT5 read boundary | PRESERVED |
| immutable MarketSnapshot | PRESERVED |
| causal completed-candle chronology | PRESERVED |
| staged specialist intelligence | PRESERVED |
| six strategy families | PRESERVED |
| BUY/SELL independence + Red Team | PRESERVED, applied inside active family during isolation |
| persistent Opportunity distinct from timing | PRESERVED |
| structural TradePlan before Risk | PRESERVED |
| automatic SMALL/MEDIUM/NORMAL profiles | PRESERVED |
| exact reference monetary profile bands/daily locks | PRESERVED |
| dynamic broker-aware sizing/min-lot actual-risk | PRESERVED |
| manual daily-loss reset capability | PRESERVED, disabled by default |
| fresh same-episode re-entry baseline | PRESERVED |
| three-loss/30m cooldown baseline | PRESERVED |
| PRE_CLOSE/reopen safety | PRESERVED pending current broker facts |
| central Gate | PRESERVED |
| one-shot Intent | PRESERVED |
| sole MT5Writer | PRESERVED |
| no-blind-retry reconciliation | PRESERVED |
| manual/external ownership separation | PRESERVED |
| ManagedTrade / verified close | PRESERVED |
| optional partial management | PRESERVED where broker-valid/divisible |
| persistence/restart/recovery | PRESERVED, runtime Git publication removed by operator direction |
| StrategyMemory / learning | PRESERVED |
| autonomous discovery/invention | PRESERVED |
| advanced ML research | PRESERVED |
| candidate promotion governance | PRESERVED / strengthened with explicit operator production approval |
| future REAL capability | PRESERVED, gated |
| graphical dashboard | PRESERVED and adopted as approved primary visual baseline |

## 4. Preserved monetary Risk — exact reference

| Profile | DayStartEquity | Normal | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|---:|
| SMALL | positive < $300 | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | $300–$999.99 | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | >= $1,000 | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Preserved optional operator-requested capability:

```text
AGGRESSIVE_SMALL_ACCOUNT = disabled by default
8%  max single-trade monetary SL-risk ceiling — NOT target
16% max aggregate open risk
16% daily loss ceiling
```

The provisional 0.50% scaffold is not canonical production policy.

## 5. Preserved loss/re-entry controls

```text
manual daily-loss reset capability = preserved, disabled by default
same-episode re-entry              = one genuinely fresh re-entry baseline
consecutive-loss cooldown          = 3 closed bot losses → at least 30m + release conditions
```

These may be researched but do not silently change production.

## 6. Preserved broker/session baseline

Pending current connected Exness verification:

```text
Daily PRE_CLOSE   T-20 no entry / T-10 flatten
Weekend PRE_CLOSE T-60 no entry / T-30 flatten
Daily reopen      1 clean completed M5
Weekend reopen    2 clean completed M5 + gap assessment
```

A current broker schedule correction is an external fact update, not a design simplification.

## 7. Preserved six families

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

No family has been deleted.

The final operator-directed Strategy Isolation policy changes live eligibility, not family existence:

```text
1 ACTIVE_EXECUTION
5 SHADOW_ONLY
```

## 8. Preserved AI / autonomous improvement

These are **not deferred away**:

- autonomous strategy invention;
- candidate parameter optimization;
- advanced ML research;
- automatic candidate evidence-stage progression.

They operate in backend research and stop at `APPROVAL_REQUIRED` before production/live promotion.

This preserves the improvement purpose while maintaining production governance.

## 9. Preserved dashboard capability

The approved SwingTrader graphical dashboard concept remains the visual baseline:

- institutional dark/cyan/gold one-screen composition;
- no scrollbars;
- central chart;
- functional chart timeframe controls;
- functional indicators/drawings/settings;
- operational/account/risk/execution/learning/system panels.

Scalp-specific/operator-directed additions clarify:

```text
Detected Setup
Active Test Family
Shadow Setup / Shadow Families
M1 timing
Scalp executable-quality metrics
```

These additions do not remove the Swing dashboard capability.

## 10. Genuine Scalp changes preserved as intentional differences

Do not “restore” these back to Swing simply for parity:

- H4 optional / H1 soft / M15 location / M5 setup-management hierarchy;
- M1 subordinate production entry refinement;
- first-class event freshness/chase/drift;
- fixed+aware spread/cost quality;
- no automatic inherited 1.20R hard Scalp floor;
- time-efficiency EXIT;
- exceptional Runner;
- stronger cost/slippage/latency/throughput research.

## 11. Operator-directed differences preserved

- market-first Setup Detector; never force active strategy onto chart;
- exactly one live-active strategy family at a time during evaluation;
- News/Fundamental removed from hard trading permission/cooldown/warmup;
- physical analytical parallelism profiling-driven rather than mandatory;
- no runtime Git publication;
- coherent remote source commit → local `git pull --ff-only` → optional clean ZIP;
- same-scope active-active/distributed DB/fencing deferred;
- mandatory paid News API and GitHub cloud compute not required;
- sophisticated partial-close optimization not a release dependency.

## 12. Earlier unintended simplifications — permanently superseded

Do not reintroduce:

```text
one STANDARD Risk policy
changed/reopened monetary bands without approval
aggressive 8%/16% mode research-only
M1 diagnostic-only final Scalp role
News BLACKOUT/UNKNOWN hard entry gate
News cooldown/warmup
mandatory physical parallelism
removal of partial management
removal of future REAL capability
64-file manual complete claim
```

## 13. Evidence boundary

Preservation means design/feature intent is kept. It does **not** prove:

- current Scalp implementation exists;
- old Swing tests pass in Scalp;
- current broker facts are unchanged;
- profitability.

Every Scalp feature still needs its own implementation/test/connected evidence.

## 14. Final invariant

> **The Scalp project may specialize speed, timing, costs and setup routing, but it may not silently delete SwingTrader capabilities the operator wanted preserved. Any future removal or behavioral change must update the comparison ledger, decision record, affected contracts and evidence plan in the same governed packet.**
