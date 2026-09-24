# GoldScalpTrader — Research and Validation

**Status:** DRAFT PRE-CHALLENGE RESEARCH CONTRACT
**Version:** 0.1-scalp-production-parity
**Authority:** Chronological replay, no-lookahead validation, dataset identity, portable datasets, session-policy replay, transaction-cost stress, holdouts and evidence packages.

## 1. Purpose

Research tests the documented scalp system without future leakage, cherry-picking, untraceable inputs or exaggerated claims.

> A positive backtest is evidence about one specified historical simulation. It is not proof of future profitability or permission to trade.

Research is an offline evidence factory. It should reuse production semantics rather than become a simplified second bot.

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
→ production intelligence/strategy/opportunity/timing/trade-plan state at T
→ freeze that decision state
→ later bars may label outcome/management only
```

Future-confirmed swings, later calendar revisions, final-candle extremes, target outcomes and post-entry regime information may not leak backward.

Same-bar STOP/TARGET ambiguity remains explicit. Research must not choose whichever result looks better.

## 4. Timeframe parity

Replay uses the currently frozen runtime roles. Pre-challenge baseline:

```text
H1  broad regime
M15 opportunity/location/path
M5  primary setup + entry + management timing
M1  diagnostic unless later promoted
H4  optional major context
```

If the fresh-zero challenge changes timeframe roles, replay and runtime change in the same affected-graph packet.

## 5. Production semantics reused by replay

Replay should call production intelligence, strategy, decision, Trade Plan, permission and Trade Manager components wherever interfaces permit.

It must preserve:

- Opportunity identity and terminal states;
- fresh-event/re-arm rules;
- one-position production capacity;
- original-R immutability;
- management action ordering;
- session/news/risk policy version;
- family-specific plan geometry;
- UNKNOWN/ambiguity semantics.

Analytical ENTER count is not the same as actual admitted trade count.

## 6. One-position capacity

P/L replay admits at most one active production trade per account/symbol scope in initial V1.

While occupied, later analytical ENTER signals are recorded as capacity-suppressed evidence and receive no overlapping production P/L.

A trade releases capacity only when the simulated close is causally established. `HORIZON_OPEN` or ambiguous close remains occupied rather than guessed flat.

## 7. Scalping execution realism

Scalping research must explicitly model transaction costs and timing assumptions.

Stress dimensions should include:

- executable-side spread;
- worse spread regimes;
- adverse entry slippage;
- signal-to-execution delay;
- order-check/send delay assumptions;
- stop/target execution slippage;
- commission/fees where known;
- modify delay/rejection;
- quote gaps/dislocation;
- event/news spread expansion;
- minimum-lot granularity.

Stress may worsen execution assumptions but must not rewrite structural invalidation or targets to improve results.

## 8. Replay realism levels

Every result package declares its realism level, for example:

```text
BAR_CLOSE_ANALYTICAL
BAR_HIGH_LOW_BRACKET
BAR_CLOSE_MANAGEMENT
COST_STRESSED_BAR_REPLAY
FORWARD_SHADOW
CONNECTED_DEMO
```

None is described as tick-perfect unless true tick/quote data and execution modelling actually support that claim.

## 9. Historical session/news policy

Historical session schedules are versioned inputs. Replay never guesses a broker clock from missing candles.

Where verified schedule intervals exist, production market-permission rules are reused.

Outside verified schedule coverage, session-aware replay becomes UNKNOWN/error rather than inventing OPEN.

Historical News evidence requires declared provider/source/version and coverage. Missing historical News cannot be silently treated as CLEAR.

## 10. Portable dataset contract

A dataset bundle may contain:

```text
dataset_manifest.json
H4.csv        optional if policy uses it
H1.csv
M15.csv
M5.csv
M1.csv        optional if supported
optional quote/spread series when available
optional verified session/news inputs
```

Manifest records source/version, symbol geometry, field definitions, bar counts, replay assumptions, hashes and chronology.

Import verifies canonical paths, hashes/counts, chronological data and no symlink/path tricks.

Credentials/account passwords are excluded.

## 11. Historical spread and cost data

Current live spread must never be a hidden fallback for historical spread.

If historical spread/quote data is absent, research uses an explicit declared assumption or refuses cost-sensitive claims.

For scalping, evidence packages should clearly state whether spread is:

- observed per bar/tick;
- broker-exported;
- median/static assumption;
- stressed variant.

## 12. Dataset identity

Dataset identity should include calculation-relevant:

- source label/version;
- all candle/quote fields;
- symbol point/tick geometry;
- spread/cost assumptions;
- session/news source/version;
- economic account context relevant to minimum-lot/risk replay;
- timeframe counts and hashes.

Mutable filenames alone are not identity.

## 13. Immutable evidence packages

Evidence packages are write-new and integrity checked.

Typical package:

```text
package_manifest.json
evidence_manifest.json
optional references to verified dataset bundle
```

Manifest binds code revision, policy version, dataset hash, input fingerprint, normalized results, limitations and evidence hash.

A package grants no production permission.

## 14. Walk-forward and final holdout

The required sequence is:

```text
DEVELOPMENT / SELECTION
→ independent validation / fixed-policy walk-forward
→ lock one candidate semantic fingerprint
→ one-shot FINAL HOLDOUT
→ stress
→ shadow
→ DEMO canary
```

No utility may repeatedly consume the final holdout while tuning.

A semantic change after lock creates a new candidate/version.

## 15. Scalp metrics

Serious research includes more than win rate:

- Net R / Average R;
- Profit Factor;
- maximum drawdown and recovery;
- win/loss/streak distribution;
- MFE/MAE;
- Entry Efficiency;
- Capture Efficiency;
- Premature Exit Cost / giveback;
- hold duration / M5 bars;
- time to first favorable/adverse excursion;
- spread/slippage/commission burden;
- net expectancy after costs;
- Opportunity Recall / meaningful missed moves;
- analytical ENTER frequency;
- capacity-admitted trade frequency;
- capacity-suppressed signals;
- family/session/regime breakdown;
- ambiguous/open coverage;
- stress sensitivity.

A higher win rate that removes most profitable opportunities is not automatically an improvement.

## 16. Ablation

Optional confluence such as FVG, OB, Trendline, Fibonacci, POC, M1 context or macro context must be tested by marginal-value ablation rather than accepted because it sounds sophisticated.

Compare base family versus base+feature with identical chronology/capacity/cost assumptions.

## 17. Small-account research

For the intended small-account context, replay should separately report:

- theoretical signal geometry;
- broker-minimum-volume affordability;
- trades blocked because 0.01 lot exceeds risk policy;
- effective actual risk after normalization;
- how often valid scalp geometry is unusable due broker granularity.

This prevents strategy quality and account affordability from being confused.

## 18. Research / learning / promotion boundary

Research episodes distinguish actual, missed, blocked, capacity-suppressed and system-fault attribution.

Discovery/invention may create declarative candidates only. Promotion owns holdout/stress/shadow/canary/approval/rollback.

Research never edits production strategy code or hard safety automatically.

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

Tests must cover chronological replay/no-lookahead, Opportunity identity parity, one-position capacity, management replay, ambiguity handling, historical session/news coverage, cost stress, portable dataset hashes, immutable evidence packages, fixed-policy walk-forward/holdout boundaries and small-account min-lot classification.

Real regime-diverse XAU history, realistic friction calibration and replay-versus-DEMO comparison remain external/research evidence.

## 21. Non-goals / open questions

Research must not guess historical session/news truth, accept tampered data, hide uncertainty, allow overlapping P/L trades production would block, use current spread as hidden historical spread or claim future profitability.

Open items: history depth, tick/quote acquisition feasibility, walk-forward sizes, minimum samples, slippage distributions, Monte Carlo/bootstrap method, cost thresholds and final M1/confluence retention criteria.
