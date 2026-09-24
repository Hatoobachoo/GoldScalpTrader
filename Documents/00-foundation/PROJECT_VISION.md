# GoldScalpTrader — Project Vision

**Status:** DRAFT PRE-CHALLENGE PRODUCT CONTRACT
**Version:** 0.1-scalp-vision
**Authority:** Product purpose, trading personality, success criteria and non-goals.

## 1. Reader promise

After reading this document, a new contributor should understand what GoldScalpTrader is trying to do, what a qualified scalp means, what the system must protect, and why intelligence, decision, risk, execution, recovery and learning remain separate layers.

## 2. What we are building

GoldScalpTrader is a governed XAUUSD/XAUUSDm MetaTrader 5 system for selective short-duration Gold trades.

It is not an HFT system and it is not a one-indicator bot. It is an institutional-style trading floor adapted to retail MT5 execution realities.

The product objective is to participate in repeatable, cost-justified short Gold moves while avoiding low-quality noise, late chasing, cost-dominated trades and unsafe broker writes.

## 3. Trading personality

The scalp trader should:

- prefer short-duration, clearly invalidatable opportunities;
- respect higher-timeframe context without turning scalping into swing trading;
- react only to causal, fresh market evidence;
- distinguish attractive chart geometry from executable Bid/Ask geometry;
- treat spread, slippage, quote age and timing freshness as first-class constraints;
- allow several independent strategy families to identify opportunities;
- avoid requiring every optional signal to agree;
- avoid forcing trades merely to increase frequency;
- manage winners and invalidations quickly enough for scalp horizons;
- remain auditable after every decision and broker action.

## 4. Intended market scope

Initial product scope:

- instrument family: Gold / XAUUSD / broker-resolved XAUUSDm equivalent;
- execution venue: MetaTrader 5 terminal;
- broker-specific facts: discovered from the connected terminal, never hard-coded when the broker exposes authoritative values;
- operating environment: local Windows PC;
- remote source control: GitHub only for source/history/backup;
- cloud execution: not required.

Exact timeframe authority is intentionally not frozen in this draft. The fresh-zero scalp challenge must decide the final regime/opportunity/setup/trigger roles for H1/M15/M5/M1 rather than mechanically shifting the Swing hierarchy.

## 5. Product objectives

The system must:

1. read trustworthy account, symbol, quote, candle, position and deal facts from one broker-read boundary;
2. build one immutable normalized market snapshot for a decision cycle;
3. understand structure, location, liquidity, volatility, session and cost context;
4. let independent scalp strategy families produce attributable BUY/SELL hypotheses;
5. preserve disagreement rather than hiding it inside one opaque score;
6. maintain a persistent Opportunity lifecycle instead of recreating the same idea each loop;
7. separate entry timing from the higher-level opportunity thesis;
8. build structural entry/SL/target geometry before monetary sizing;
9. independently validate affordability, lot sizing and account risk;
10. compose all hard authorities centrally before a broker write;
11. persist one-shot intent before any irreversible request;
12. reconcile every attempted write against broker truth;
13. manage bot-owned open trades under the same safety boundaries;
14. survive restart without forgetting exposure, risk day, intents, opportunities or learning obligations;
15. learn only from verified causal outcomes and never self-authorize production changes;
16. expose truthful operator state without making the dashboard a second trading authority.

## 6. What “good” means

A good product is not defined by trade count or a claimed win rate.

Engineering quality means:

- deterministic behaviour for the same facts and configuration;
- explicit UNKNOWN/error states;
- no hidden broker writes;
- no duplicate order submission;
- no silent state reset after restart;
- no future leakage in replay/research;
- no undocumented decision rule;
- source/tests/documents remain synchronized;
- operator can understand why a trade was taken, missed, blocked, managed or closed.

Trading quality must later be evaluated with cost-aware metrics including, where applicable:

- expectancy after spread/slippage assumptions;
- original and realized R;
- MAE/MFE;
- entry efficiency;
- exit efficiency;
- hold duration;
- session and strategy-family attribution;
- blocked/missed opportunity analysis;
- late-entry avoidance;
- execution-cost sensitivity.

## 7. Hard non-goals

GoldScalpTrader is not intended to:

- guarantee profit or accuracy;
- trade every M1/M5 fluctuation;
- perform broker-exchange colocated HFT;
- use martingale as a loss-recovery mechanism;
- use uncontrolled grids or unlimited averaging;
- silently widen a structural stop to make lot sizing convenient;
- convert missing required truth into PASS;
- let learning or AI bypass hard risk/safety;
- let dashboards place or modify orders;
- automatically publish/push the repository during runtime shutdown;
- depend on paid GitHub/cloud infrastructure.

## 8. Small-account reality

The system may support small accounts, but account size does not justify invalid geometry or hidden leverage.

If the broker minimum lot makes a valid structural scalp unaffordable under the selected policy, Risk must block it rather than distort the stop or pretend the exposure is smaller.

Aggressive profiles, if retained after challenge, must be explicit opt-in profiles and never the default.

## 9. Safety-first liveness

The process should remain alive and truthful when safe trading is temporarily impossible.

Market closed, stale data, high spread, missing provider context, reconciliation pending, risk lock or no valid opportunity are legitimate operating states. They are not process failures and must not be “fixed” by guessing.

## 10. Reference relationship

GoldSwingTraderAI provides the proven documentation/engineering reference. Roughly reusable architectural meaning should be preserved unless scalping demands a justified change.

The scalp project must still undergo its own fresh-from-zero audit. Inheritance is not proof.
