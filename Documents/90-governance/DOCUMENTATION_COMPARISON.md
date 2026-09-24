# GoldScalpTrader — GoldSwingTraderAI versus GoldScalpTrader Explicit Change Record

**Status:** POST-AUDIT-1 EXPLICIT REFERENCE COMPARISON — PRESERVATION-FIRST CORRECTED
**Version:** 1.1-only-scalp-specific-deltas
**Authority:** Permanent record of what is intentionally preserved, changed for scalping, changed by explicit operator instruction, or restored after an unjustified earlier simplification.

## 1. Purpose

GoldSwingTraderAI is the reference feature/engineering baseline. GoldScalpTrader is a scalp-specialized product, **not a license to redesign unrelated features**.

```text
GoldSwingTraderAI Documents/ → default feature/behaviour baseline
GoldScalpTrader Documents/   → current scalp authority
```

Canonical preservation rule:

> Keep the Swing feature/default unless a direct scalping requirement, explicit operator instruction, or separately proven defect justifies changing it.

When uncertain, preserve first and discuss the possible scalp change at final documentation review.

## 2. What is preserved substantially as-is

Preserve:

- documentation-first governance and affected-graph synchronization;
- one normalized MT5 read boundary;
- immutable shared MarketSnapshot;
- causal completed-candle chronology / no lookahead;
- specialist intelligence desks;
- bounded parallel analytical capability plus deterministic one-worker fallback;
- six independent strategy-family hypotheses;
- independent BUY and SELL theses + Red Team/Floor Manager;
- persistent Opportunity distinct from current entry timing;
- structural TradePlan before monetary Risk;
- monetary Risk as independent hard authority;
- automatic SMALL/MEDIUM/NORMAL account profiles and reference risk bands;
- broker-aware min-lot sizing and no structural-stop distortion;
- daily safety P/L / lock / governed-reset / cooldown / same-episode state;
- hard session/system/account/exposure/controller separation;
- reference PRE_CLOSE/reopen safety defaults, subject to current broker proof;
- central execution Gate;
- persist-before-send one-shot Intent;
- sole MT5Writer;
- ambiguous acknowledgement → reconciliation, never blind retry;
- bot/manual/foreign ownership separation;
- ManagedTrade lifecycle and verified-close evidence;
- optional broker-valid partial management when volume permits;
- restart/persistence discipline;
- downstream learning/research with no broker authority;
- governed discovery/invention/promotion;
- read-only dashboard authority;
- one PRIMARY writer per account/symbol scope;
- future governed REAL capability, while disabled until its evidence/release gate;
- evidence separation between deterministic tests, replay, connected DEMO and profitability.

## 3. Actual scalp-specific changes

These differences are retained because they directly concern the scalp horizon rather than convenience/simplification.

| # | Area | Swing reference | GoldScalpTrader | Why allowed |
|---:|---|---|---|---|
| 1 | Product horizon | meaningful intraday/open-session move | selective short-duration Gold scalp | direct product change |
| 2 | Broad timeframe | H4/H1 strong broad role | H1 broad soft regime; H4 optional major context | scalp time horizon |
| 3 | Opportunity chain | H4 → H1 → M15 → M5 | H1 → M15 → M5, H4 optional | scalp hierarchy |
| 4 | M1 | diagnostic-only | diagnostic/research-only | **preserved**, not a change |
| 5 | Event freshness | important | first-class trigger age, chase distance, stale-for-entry state | short-horizon edge decay |
| 6 | Cost sensitivity | material | explicit gross + cost-adjusted room before Risk/execution | small target room makes friction central |
| 7 | 1.20R hard floor | reference Primary floor | not automatically imposed as scalp hard floor | scalp target/cost geometry differs |
| 8 | Runner | meaningful continuation path | exceptional, fresh continuation/new objective required | avoid accidental swing conversion |
| 9 | Time efficiency | secondary | first-class normal EXIT reason | scalp thesis includes expected speed |
| 10 | Latency/drift observability | useful | first-class entry/execution diagnostic | scalp edge can expire quickly |
| 11 | News UNKNOWN | Swing adaptive-pass behaviour when session independently OPEN | true News UNKNOWN blocks new scalp entry | immediate event sensitivity |
| 12 | News API outage | failure could become adaptive unknown | still-valid accepted LKG cache carries truth; expired/invalid cache → UNKNOWN | availability + stale-data safety |
| 13 | Scalp research metrics | R/MAE/MFE etc. | stronger cost, latency, duration, entry/capture efficiency | scalp-specific evaluation |

Exact scalp thresholds remain evidence/calibration items where documented.

## 4. Explicit operator-directed changes that are NOT presented as scalp-derived

These changes remain because the operator explicitly requested them, not because the system is a scalper.

| Area | Reference | GoldScalpTrader |
|---|---|---|
| Runtime Git publication | reference included graceful-shutdown repository publication | **removed**; runtime performs no Git commit/push/pull and needs no GitHub credentials |
| Development/source backup | reference publication-heavy workflow | major coherent remote commit → `git pull --ff-only` → optional secret-clean local ZIP |
| Aggressive small-account option | operator-requested project feature outside the preserved normal profile table | preserved operational option, disabled by default; 8% max SL-risk ceiling, 16% aggregate open-risk cap, 16% daily-loss ceiling |

## 5. Earlier changes that were NOT scalp-required and are now restored

The following prior Audit-1 changes were mistakes under the operator's preservation requirement. They are superseded.

| Area | Incorrect earlier Scalp change | Correct current state |
|---|---|---|
| Account Risk model | removed SMALL/MEDIUM/NORMAL for one STANDARD policy | **RESTORED** automatic SMALL/MEDIUM/NORMAL profiles |
| Profile percentages | reopened all Swing risk percentages | **RESTORED** Swing profile target/elevated/hard/daily values |
| Aggressive 8%/16% mode | demoted to future research-only / inactive | **RESTORED** as operational capability, disabled by default |
| Cooldown/re-entry | exact reference behaviour reopened | **RESTORED** one fresh re-entry; 3 closed losses → at least 30m cooldown + release conditions |
| Manual reset | only vague future capability | **RESTORED** governed feature, disabled by default |
| Physical analytical concurrency | changed to optional/profiling-only feature | **RESTORED** bounded-parallel capability as target architecture + one-worker fallback/parity |
| PRE_CLOSE defaults | exact values removed pending calibration | **RESTORED** daily T-20/T-10, weekend T-60/T-30 baseline |
| Reopen defaults | exact counts removed | **RESTORED** daily 1 clean M5; weekend 2 + gap assessment |
| Provider TTL | 1800-second reference default reopened | **RESTORED** 1800-second baseline, unless later direct provider/scalp reason changes it |
| REAL capability | described as removed/outside V1 feature | **RESTORED** as future governed capability, disabled until DEMO/release/explicit approval |
| Partial management | wording risked implying feature removal | **PRESERVED** where broker-valid/divisible; correctness at 0.01 never depends on it |

These restorations are not new strategy optimizations. They correct unintended feature/default removal.

## 6. Preserved risk contract

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal / target | Elevated | Hard ceiling | Daily loss lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

Operator-requested aggressive overlay:

```text
disabled by default
eligible baseline: positive DayStartEquity < $1,000
8%  maximum monetary SL-risk ceiling — not target
16% maximum aggregate open risk
16% daily loss ceiling
```

## 7. Preserved session/provider baselines

Unless current broker/provider evidence proves the underlying fact itself changed:

```text
Daily pre-close     T-20 no new entry / T-10 mandatory flatten
Weekend pre-close   T-60 no new entry / T-30 mandatory flatten
Daily reopen        1 clean completed M5
Weekend reopen      2 clean completed M5 + gap assessment
Provider TTL        1800 seconds baseline
```

News UNKNOWN handling remains a legitimate scalp-specific change. Last-known-good cache never has its timestamp/TTL extended on refresh failure.

## 8. Things still intentionally different for scalping

Do **not** revert these merely to make Scalp identical to Swing:

- H1/M15/M5 scalp hierarchy with H4 optional;
- event/trigger freshness and anti-chase rules;
- cost-adjusted room;
- no automatic inherited 1.20R hard scalp floor;
- stronger spread/drift/latency observability;
- true News UNKNOWN new-entry block + valid-cache resilience;
- exceptional Runner;
- time/efficiency EXIT semantics;
- scalp cost/latency/duration research metrics.

Their exact numeric thresholds may still require evidence.

## 9. Historical/reference evidence boundary

Swing audits/results remain engineering lessons and reference evidence, not GoldScalpTrader PASS results. Scalp implementation/tests/DEMO/recovery evidence must be produced on the Scalp revision.

This evidence boundary is not a removal of a Swing feature.

## 10. Final discussion rule

At final documentation-section review, explicitly discuss only the remaining proposed **scalp-specific** differences/thresholds with the operator.

Until then:

```text
non-scalp reference feature/default → preserve
clear scalp requirement             → document as scalp delta
explicit operator instruction       → document separately as operator-directed
uncertain difference                → preserve now, discuss later
```

This file is the permanent answer to “what exactly changed from SwingTrader?” and must be updated whenever a governed delta changes.