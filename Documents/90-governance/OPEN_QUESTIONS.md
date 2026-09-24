# GoldScalpTrader — Open Questions and Closure Plan

**Status:** ACTIVE PRE-CHALLENGE QUESTION REGISTER
**Version:** 0.1-foundation-questions
**Authority:** Unresolved choices, required evidence and completion boundaries.

## 1. Why this file exists

An open question is not automatically a design failure. Some items must be fixed before build, some are implementation choices, some need historical calibration, some require connected broker proof and some may be deliberately deferred.

| Class | Meaning | Closure method |
|---|---|---|
| FIX BEFORE BUILD | safety/ownership cannot be safely guessed | contract + deterministic proof plan |
| IMPLEMENTATION CHOICE | several safe implementations exist | choose, document and test |
| CALIBRATE IN RESEARCH | architecture fixed; numerical value needs evidence | chronological replay/stress/holdout |
| EXTERNAL PROOF | only real terminal/broker/machine can answer | controlled connected evidence |
| DEFERRED V1 | intentionally outside initial scope | remain explicitly deferred |

## 2. Product/timeframe questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-001 | What are the exact H1/M15/M5/M1/tick authority roles for scalping? | FIX BEFORE BUILD | do not inherit Swing roles blindly |
| Q-002 | Is M1 production timing evidence, diagnostic only, or both under typed boundaries? | FIX BEFORE BUILD | challenge explicitly |
| Q-003 | Are forming-candle/tick facts allowed for timing, and how are they typed versus completed bars? | FIX BEFORE BUILD | causal separate type required if used |
| Q-004 | What is the expected scalp holding horizon and when does a thesis become “not a scalp”? | CALIBRATE IN RESEARCH | architecture supports time-aware management |

## 3. Strategy-floor questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-010 | Are six independent strategy families still the cleanest decomposition? | FIX BEFORE BUILD | six is starting point, not sacred number |
| Q-011 | Do Liquidity Sweep and Failed Breakout Reversal duplicate too much evidence? | FIX BEFORE BUILD | inspect correlation and ownership |
| Q-012 | Does Momentum Expansion deserve an independent family or belong inside continuation? | FIX BEFORE BUILD | challenge separately |
| Q-013 | Should Range Extreme / Mean Reversion be production V1 or research-only? | FIX BEFORE BUILD | requires clear regime ownership |
| Q-014 | What optional confluence is useful without turning the floor into filter soup? | CALIBRATE IN RESEARCH | optional/soft by default |
| Q-015 | How much opposing-family strength turns a leading thesis into CONFLICTED/WAIT? | CALIBRATE IN RESEARCH | fusion owns semantics; weights later |

## 4. Freshness and timing questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-020 | How is Opportunity expiry measured: wall-clock, completed bars, event replacement, distance or combination? | CALIBRATE IN RESEARCH | durable explicit expiry state |
| Q-021 | What makes a BOS/MSS/sweep/retest trigger stale for a scalp? | CALIBRATE IN RESEARCH | knowledge time + event lineage required |
| Q-022 | How far may current executable price drift from approved entry reference before MISSED/LATE? | CALIBRATE IN RESEARCH | use volatility/cost normalized evidence |
| Q-023 | What causal event is sufficient to re-arm a terminal opportunity? | FIX BEFORE BUILD | never simple timer reset alone |
| Q-024 | Should timing require completed M1/M5 evidence, or permit bounded tick confirmation? | FIX BEFORE BUILD | separate from strategy thesis |

## 5. Cost/execution questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-030 | Which spread representation governs entry: absolute price, points, ATR fraction, target fraction or hybrid? | CALIBRATE IN RESEARCH | cost must be target/geometry aware |
| Q-031 | What slippage/deviation policy is safe for Gold scalps? | CALIBRATE IN RESEARCH + EXTERNAL PROOF | broker behaviour required |
| Q-032 | How should Bid/Ask geometry be normalized for backtests when tick history is incomplete? | FIX BEFORE BUILD | assumptions must be explicit and conservative |
| Q-033 | What quote-age threshold is required for new entries? | CALIBRATE IN RESEARCH + EXTERNAL PROOF | diagnose first, then hard threshold |
| Q-034 | Should risk-reducing CLOSE actions ignore some entry-only spread conditions? | FIX BEFORE BUILD | action-sensitive safety likely required |

## 6. Risk questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-040 | What is default per-trade risk for V1 small accounts? | CALIBRATE IN RESEARCH | conservative default; no profit promise |
| Q-041 | Should aggressive small-account profile exist, and what hard ceiling applies? | CALIBRATE IN RESEARCH | explicit opt-in only if retained |
| Q-042 | What daily safety-loss threshold and cooldown/loss-streak policy best fits scalp frequency? | CALIBRATE IN RESEARCH | frequency interaction must be modelled |
| Q-043 | Does one-position-at-a-time remain V1? | FIX BEFORE BUILD | current default yes |
| Q-044 | What happens when minimum lot exceeds allowed monetary risk? | FIX BEFORE BUILD | block; never distort structural stop |

## 7. Trade-management questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-050 | Which management states are useful for scalping: HOLD/PROTECT/TRAIL/RUNNER/EXIT? | FIX BEFORE BUILD | preserve boundary; possibly simplify states |
| Q-051 | Should time-stop exist and how is it measured? | CALIBRATE IN RESEARCH | likely scalp-specific |
| Q-052 | When should break-even/protection occur without choking normal Gold noise? | CALIBRATE IN RESEARCH | structure/volatility aware |
| Q-053 | Are partial TP/runner mechanics justified for small positions/min lot? | CALIBRATE IN RESEARCH + EXTERNAL PROOF | broker volume-step dependent |
| Q-054 | How does spread deterioration affect holding versus closing? | CALIBRATE IN RESEARCH | action-sensitive cost logic |

## 8. Session/news questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-060 | Which sessions/windows are production-priority for XAU scalping? | CALIBRATE IN RESEARCH | London/NY/overlap candidates |
| Q-061 | Which known events require hard blackout and for how long before/after? | CALIBRATE IN RESEARCH | event tier + XAU sensitivity |
| Q-062 | How should unavailable external news provider affect permission when broker session truth is known? | FIX BEFORE BUILD | UNKNOWN visible; do not fabricate CLEAR |

## 9. Persistence/recovery questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-070 | Is local SQLite still the best V1 durable store? | IMPLEMENTATION CHOICE | strong default; zero-cost/simple |
| Q-071 | Exact checkpoint cadence and event retention? | IMPLEMENTATION CHOICE | durability without excessive I/O |
| Q-072 | What startup evidence is required before reopening new entries after crash/restart? | FIX BEFORE BUILD | full broker reconciliation first |
| Q-073 | Same-account/symbol laptop handoff workflow? | FIX BEFORE BUILD | sequential only in V1 candidate |

## 10. Local-backup questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-080 | Default local backup root? | IMPLEMENTATION CHOICE | outside repository, e.g. `C:\GoldScalpTrader_Backups` |
| Q-081 | Runtime backup cadence/retention? | IMPLEMENTATION CHOICE | rolling + graceful-shutdown; exact counts later |
| Q-082 | Should source Git bundle be created automatically on every shutdown? | IMPLEMENTATION CHOICE | current preference: no; milestone/manual to avoid unnecessary work |
| Q-083 | Should graceful shutdown always create a runtime-state backup? | IMPLEMENTATION CHOICE | yes candidate, unless no durable state exists |
| Q-084 | How is SQLite copied consistently during live runtime? | FIX BEFORE BUILD | use transactional/SQLite backup semantics, not unsafe raw copy |
| Q-085 | Should portable recovery package include logs/research datasets? | IMPLEMENTATION CHOICE | manifest-driven selectable classes |
| Q-086 | How are secrets recovered after machine loss if automatic archives exclude them? | FIX BEFORE BUILD | separate operator-managed secret recovery procedure |
| Q-087 | Do we support optional second physical drive/USB mirror? | DEFERRED/OPTIONAL V1 | yes as path option, no cloud dependency |

## 11. GitHub questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-090 | Repository visibility? | IMPLEMENTATION CHOICE | private preferred; current repo visibility is external account setting |
| Q-091 | Any runtime GitHub credential? | FIX BEFORE BUILD | no |
| Q-092 | Any shutdown GitHub publication/push? | FIX BEFORE BUILD | explicitly no |
| Q-093 | Any GitHub Actions/Codespaces requirement? | FIX BEFORE BUILD | no |

## 12. Research/learning questions

| ID | Question | Class | Current direction |
|---|---|---|---|
| Q-100 | Which scalp-specific episode metrics must StrategyMemory retain? | FIX BEFORE BUILD | include cost/duration/MAE/MFE/entry-exit efficiency |
| Q-101 | How are blocked/missed opportunities sampled without selection bias? | FIX BEFORE BUILD | causal evidence package required |
| Q-102 | What minimum evidence is required to promote a discovered strategy/parameter change? | CALIBRATE IN RESEARCH | staged holdout/stress/shadow/canary governance |
| Q-103 | Can autonomous invention propose new scalp families? | FIX BEFORE BUILD | proposal only; no executable self-modification |

## 13. Closure rule

No `FIX BEFORE BUILD` item affecting the current implementation phase may be silently guessed.

When an item closes:

1. record the decision in `DESIGN_DECISIONS.md`;
2. update the owning topic contract;
3. synchronize the full affected document graph;
4. define implementation/test/evidence ownership;
5. keep any remaining calibration/external proof explicitly pending.
