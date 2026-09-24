# GoldScalpTrader — Research and Validation

**Status:** FROZEN V1 RESEARCH ARCHITECTURE — DATASET / SCALP CALIBRATION EVIDENCE PENDING
**Version:** 1.0-production-parity-preserved-policy
**Authority:** Chronological replay, no-lookahead validation, dataset identity, portable datasets, session/Risk-policy replay, transaction-cost stress, holdouts and evidence packages.

## 1. Purpose

Research tests the documented scalp system without future leakage, cherry-picking, untraceable inputs or exaggerated claims.

> A positive backtest is evidence about one specified historical simulation. It is not proof of future profitability or permission to trade.

Research is an offline evidence factory. It reuses production semantics rather than becoming a simplified second bot.

## 2. Evidence pipeline

```text
verified portable dataset
→ dataset identity/provenance
→ chronological production-semantics replay
→ managed-trade/capacity simulation
→ transaction-cost + execution stress
→ metrics / ablation
→ fixed-policy walk-forward
→ one-shot final holdout
→ immutable evidence package
→ governed promotion review
```

No evidence artifact carries broker authority.

## 3. No-lookahead contract

At historical time `T`:

```text
facts knowable at T
→ production intelligence/strategy/opportunity/timing/TradePlan state at T
→ freeze decision state
→ later bars may label outcome/management only
```

Future-confirmed swings, later calendar revisions, final-candle extremes, target outcomes and post-entry regime information never leak backward. Same-bar STOP/TARGET ambiguity remains explicit rather than optimistically resolved.

## 4. Frozen timeframe parity

Replay uses the current production roles exactly:

```text
H1  broad soft regime/context
M15 opportunity/location/path
M5  primary completed setup + entry timing + normal management
H4  optional major context
M1  diagnostic/research only
```

These roles are no longer a pre-challenge research question. Any future production-timeframe change requires the same governed affected-graph update in runtime and replay.

## 5. Production semantics reused by replay

Replay preserves:

- six production families;
- bounded analytical scheduling semantics and deterministic one-worker parity where applicable;
- Opportunity identity/terminal states;
- fresh-event/re-arm rules;
- preserved one genuinely fresh same-episode re-entry baseline;
- one-position production capacity;
- original-R immutability;
- management ordering and optional broker-valid partial-management semantics where modelled;
- session/news/Risk policy identity;
- family-specific geometry;
- UNKNOWN/ambiguity semantics.

Analytical ENTER count is not actual admitted trade count.

## 6. Preserved monetary Risk-policy parity

Research does not replace the canonical Risk contract with one generic risk percentage.

Historical simulation records/uses the applicable policy version including:

```text
SMALL   DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

and the preserved target/elevated/hard/daily bands.

If `AGGRESSIVE_SMALL_ACCOUNT` is explicitly part of a research scenario, the evidence package states that it is an **explicit disabled-by-default production capability**, with 8% maximum SL-risk ceiling (not target), 16% aggregate cap and 16% daily ceiling. Research must never silently enable it merely because simulated equity is small.

Preserved manual-reset/cooldown/re-entry policy identity is also part of replay where applicable.

## 7. One-position capacity

P/L replay admits at most one active independently risk-bearing Gold trade per account/symbol scope under current V1. While occupied, later analytical ENTERs are recorded as capacity-suppressed evidence and receive no overlapping production P/L.

Capacity releases only after causal close. Ambiguous/HORIZON_OPEN remains occupied rather than guessed flat.

## 8. Scalping execution realism

Stress dimensions include executable-side spread, worse spread regimes, adverse entry/exit slippage, signal-to-execution delay, order-check/send delay assumptions, commission/fees, modify delay/rejection, gaps/dislocation, event/news spread expansion and minimum-lot granularity.

Stress may worsen execution assumptions but cannot rewrite structural stop/target to improve results.

## 9. Replay realism levels

Declare levels such as:

```text
BAR_CLOSE_ANALYTICAL
BAR_HIGH_LOW_BRACKET
BAR_CLOSE_MANAGEMENT
COST_STRESSED_BAR_REPLAY
FORWARD_SHADOW
CONNECTED_DEMO
```

Nothing is called tick-perfect without true tick/quote data and suitable execution modelling.

## 10. Historical session/news policy

Historical schedule/news inputs are versioned. Replay never guesses broker OPEN from missing candles and never treats missing historical News as CLEAR.

Preserved policy baselines may be replayed where the dataset/source actually supports them:

```text
provider TTL 1800s
Daily PRE_CLOSE T-20/T-10
Weekend PRE_CLOSE T-60/T-30
Daily reopen 1 clean completed M5
Weekend reopen 2 clean completed M5 + gap assessment
```

If historical broker schedule coverage is unavailable, session-aware claims become UNKNOWN/limited rather than fabricated.

## 11. Portable dataset contract

A bundle may contain:

```text
dataset_manifest.json
H4.csv optional
H1.csv
M15.csv
M5.csv
M1.csv optional diagnostics/research only
optional quote/spread series
optional verified session/news inputs
```

Manifest records source/version, symbol geometry, field definitions, counts, assumptions, hashes and chronology. Credentials are excluded.

## 12. Historical spread/cost truth

Current live spread is never a hidden historical fallback. If historical spread/quote data is absent, research uses an explicit declared assumption or refuses unsupported cost-sensitive claims.

Evidence package states whether spread is observed, broker-exported, static/median assumption or stressed variant.

## 13. Dataset / evidence identity

Dataset identity includes calculation-relevant candle/quote fields, symbol geometry, cost assumptions, session/news source/version, economic account context relevant to Risk/min-lot replay, timeframe counts and hashes.

Evidence packages are write-new/integrity checked and bind code revision, policy version, dataset hash, input fingerprint, normalized results, limitations and evidence hash.

## 14. Walk-forward / final holdout

```text
DEVELOPMENT / SELECTION
→ independent validation / fixed-policy walk-forward
→ semantic lock
→ one-shot FINAL HOLDOUT
→ stress
→ shadow
→ DEMO canary
```

Repeated tuning against final holdout destroys its claim. Semantic change after lock creates a new candidate/version.

## 15. Scalp metrics

Use more than win rate: Net/Avg R, Profit Factor, drawdown/recovery, streaks, MFE/MAE, Entry/Capture Efficiency, premature-exit cost/giveback, hold duration/M5 bars, time-to-excursion, transaction costs, Opportunity Recall, analytical ENTER frequency, capacity-admitted/suppressed counts, family/session/regime breakdown, ambiguity coverage and stress sensitivity.

## 16. Ablation

Optional confluence such as FVG, OB, Trendline, Fib, POC, M1 diagnostics or macro context is tested by marginal-value ablation with identical chronology/capacity/cost assumptions.

M1 diagnostics may be researched, but replay does not grant M1 production authority.

## 17. Small-account research

Report separately:

- theoretical signal geometry;
- applicable preserved Risk profile;
- broker-minimum-volume affordability;
- plans blocked because minimum volume exceeds active policy;
- actual normalized risk;
- explicit aggressive-overlay scenarios only when intentionally configured.

This prevents strategy quality and account affordability from being confused.

## 18. Research / promotion boundary

Actual, missed, blocked, capacity-suppressed and system-fault episodes remain distinct. Discovery/invention creates declarative candidates only. Promotion owns holdout/stress/shadow/canary/approval/rollback.

Research never edits production code/policy automatically or grants future REAL authority.

## 19. Planned implementation ownership

```text
src/gold_scalp_trader/research/replay.py
src/gold_scalp_trader/research/management_replay.py
src/gold_scalp_trader/research/session_history.py
src/gold_scalp_trader/research/stress.py
src/gold_scalp_trader/research/validation.py
src/gold_scalp_trader/research/datasets.py
src/gold_scalp_trader/research/acquisition.py
src/gold_scalp_trader/research/evidence.py
src/gold_scalp_trader/research/packages.py
src/gold_scalp_trader/research/metrics.py
src/gold_scalp_trader/research/outcomes.py
src/gold_scalp_trader/research/ablation.py
```

## 20. Planned proof

Tests cover chronological/no-lookahead replay, frozen timeframe parity, preserved Risk/profile/overlay semantics, Opportunity/re-entry/capacity parity, management replay, ambiguity, historical session/news coverage, cost stress, dataset hashes, immutable evidence packages and one-shot holdout boundaries.

## 21. Open research/calibration

History depth, tick/quote acquisition feasibility, walk-forward sizes, minimum samples, slippage distributions, Monte Carlo/bootstrap method, genuine scalp cost/freshness thresholds and final optional-confluence marginal value remain research questions.

Frozen timeframe authority and preserved non-scalp Risk/session defaults are not automatically reopened.