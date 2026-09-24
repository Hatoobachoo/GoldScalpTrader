# GoldScalpTrader — Project Vision

**Status:** FROZEN PRODUCT CONTRACT — CALIBRATION / EXTERNAL PROOF PENDING
**Version:** 1.0-post-fresh-zero
**Authority:** Product purpose, trading personality, success criteria and non-goals.

## 1. What we are building

GoldScalpTrader is a governed XAUUSD/XAUUSDm MetaTrader 5 system for selective short-duration Gold trades.

It is not HFT, not a one-indicator bot and not a machine that trades every small fluctuation. It is an institutional-style multi-desk trading floor adapted to retail MT5 execution reality.

The objective is to participate in repeatable, cost-justified short Gold moves while avoiding noise, late chasing, stale triggers, cost-dominated geometry and unsafe broker writes.

## 2. Trading personality

The system should:

- prefer short-duration, clearly invalidatable opportunities;
- use higher-timeframe context as context rather than universal veto;
- act only on causal, fresh evidence;
- distinguish chart geometry from executable Bid/Ask geometry;
- treat spread, slippage, drift and event age as first-class scalp concerns;
- let six independent strategy families form attributable hypotheses;
- preserve BUY/SELL disagreement rather than hide it inside one score;
- avoid perfect-checklist paralysis and avoid forced frequency;
- maintain persistent Opportunity identity instead of recreating the same idea each loop;
- keep monetary Risk independent from strategy confidence;
- remain auditable after every decision and broker action.

## 3. Frozen V1 timeframe roles

Audit 1 freezes:

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management structure
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health only
```

No helper may silently turn M1 into production decision authority. A later M1 promotion requires a governed design change and evidence.

## 4. Intended market / deployment scope

- instrument family: Gold / XAUUSD / broker-resolved XAUUSDm equivalent;
- venue: local MetaTrader 5 terminal;
- broker facts: discovered from the connected terminal rather than guessed when official metadata exists;
- operating environment: local Windows PC;
- GitHub: deliberate source control/remote source backup only;
- cloud execution: not required;
- V1 irreversible broker target: controlled DEMO only after DRY_RUN and deterministic proof;
- REAL trading: outside V1 unless separately governed later.

## 5. Product objectives

The system must:

1. read trustworthy account, symbol, quote, candle, position and deal facts from one broker-read boundary;
2. build one immutable normalized cycle snapshot;
3. understand structure, location, liquidity, volatility, session, news and cost context;
4. let six independent scalp families build attributable BUY/SELL cases;
5. preserve conflict/correlation explicitly;
6. maintain persistent Opportunity/Episode identity;
7. separate Opportunity quality from executable M5 timing;
8. build structural TradePlan geometry before monetary Risk;
9. retain both gross structural quality and cost-adjusted room diagnostics;
10. validate actual broker-normalized volume/min-lot affordability independently;
11. compose hard authorities centrally before a broker write;
12. persist a one-shot Intent before irreversible submission;
13. reconcile every attempted write against broker truth;
14. manage verified bot-owned trades under the same safety spine;
15. survive restart without forgetting exposure, risk day, Intents, Opportunities or learning obligations;
16. learn only from verified causal outcomes and never self-authorize production changes;
17. expose truthful operator state without making the dashboard a second authority.

## 6. What “good” means

Engineering quality means deterministic behaviour for the same facts/configuration, explicit UNKNOWN/error states, no hidden writes, no duplicate submission, no silent restart reset, causal replay, synchronized Documents/source/tests and clear operator reasons.

Trading quality is evaluated later with evidence, not promises. Metrics include where applicable:

- expectancy / Net R after realistic costs;
- gross vs cost-adjusted room;
- original/realized R;
- MAE/MFE;
- entry/capture/exit efficiency;
- hold duration;
- family/session/regime attribution;
- missed/blocked opportunity analysis;
- late-entry avoidance;
- spread/slippage/latency sensitivity;
- minimum-lot affordability frequency.

## 7. Strategy floor

Audit 1 retains six starting families:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

These remain separate hypotheses because their causal narratives differ. Correlation/event lineage prevents one episode from becoming fake multi-confirmation.

## 8. Risk personality

V1 uses one explicit STANDARD production risk policy rather than automatic account-size tiers.

Account size still matters through verified equity, structural stop distance, tick value and broker minimum/step volume.

Exact preferred per-trade risk, hard ceiling, daily-loss limit, cooldown and re-entry values remain calibration pending.

Historical aggressive small-account values are not active V1 policy. Any future aggressive experiment must be explicit, research-governed and disabled by default.

## 9. Hard non-goals

GoldScalpTrader is not intended to:

- guarantee profit, accuracy or trade frequency;
- trade every M1/M5 fluctuation;
- perform colocated/exchange HFT;
- use M1/tick history as hidden V1 decision authority;
- use martingale, uncontrolled grids or averaging-down rescue;
- widen/tighten structural stops merely to make risk convenient;
- convert missing required truth into PASS;
- let learning/AI bypass hard risk/safety;
- let dashboards place/modify orders;
- automatically Git commit/push/pull during trading runtime;
- depend on paid GitHub/cloud infrastructure;
- allow same-scope active-active laptop writers in V1;
- imply partial-profit logic is required for an indivisible 0.01 position.

## 10. Safety-first liveness

Market closed, stale data, wide spread, News UNKNOWN, reconciliation pending, risk lock, no valid opportunity or presentation degradation are legitimate operating states. The process should stay alive and truthful where possible without inventing permission.

News UNKNOWN specifically blocks **new entry** in V1 while safe management/protection/mandatory CLOSE remains action-sensitive.

## 11. Reference relationship

GoldSwingTraderAI remains the preservation/reference system. Audit 1 confirmed that most of its engineering/governance spine should be retained, while scalping required explicit changes to timeframe authority, cost/freshness semantics, risk-policy shape, News UNKNOWN policy, time-efficiency management and local development backup.

Inheritance is evidence to inspect, never proof by itself.