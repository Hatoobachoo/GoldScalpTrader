# GoldScalpTrader — Project Vision

**Status:** FROZEN PRODUCT CONTRACT — PRESERVATION-FIRST CORRECTED / SCALP CALIBRATION + EXTERNAL PROOF PENDING
**Version:** 1.2-final-doc-scan
**Authority:** Product purpose, preservation boundary, trading personality, success criteria and non-goals.

## 1. What we are building

GoldScalpTrader is a governed XAUUSD/XAUUSDm MetaTrader 5 system for selective short-duration Gold trades.

It is not HFT, not a one-indicator bot and not a machine that trades every fluctuation. It preserves the GoldSwingTraderAI feature/engineering baseline except where a direct scalping requirement, explicit operator instruction or separately proven reference defect justifies a difference.

The objective is to participate in repeatable, cost-justified short Gold moves while avoiding noise, late chasing, stale triggers, cost-dominated geometry and unsafe broker writes.

## 2. Preservation-first product rule

```text
non-scalp reference feature/default → preserve
clear direct scalp requirement      → adapt explicitly
explicit operator instruction       → apply explicitly
proven reference defect             → correct through governed packet
uncertain difference                → preserve now; discuss at final documentation review
```

A simpler implementation is not by itself permission to remove a reference feature.

## 3. Trading personality

The system should:

- prefer short-duration, clearly invalidatable opportunities;
- use higher-timeframe context as context rather than universal veto;
- act only on causal, fresh evidence;
- distinguish chart geometry from executable Bid/Ask geometry;
- treat spread, slippage, drift and event age as first-class scalp concerns;
- let six independent strategy families form attributable hypotheses;
- preserve BUY/SELL disagreement rather than hide it inside one score;
- retain bounded-parallel analytical capability with deterministic one-worker fallback;
- avoid perfect-checklist paralysis and avoid forced frequency;
- maintain persistent Opportunity identity instead of recreating the same idea each loop;
- keep monetary Risk independent from strategy confidence;
- remain auditable after every decision and broker action.

## 4. Frozen timeframe roles

```text
H1   broad soft regime / major directional-volatility context
M15  opportunity location, path, liquidity/session context
M5   primary completed-bar setup, entry timing and normal management structure
H4   optional major context only
M1   diagnostic/research only
quote current executable Bid/Ask/spread/drift/health only
```

No helper may silently turn M1 into production decision authority. A later M1 promotion requires a separate governed design/evidence decision.

## 5. Intended market / deployment scope

- instrument: Gold / XAUUSD / broker-resolved XAUUSDm equivalent;
- venue: local MetaTrader 5 terminal;
- broker facts: discovered from connected terminal where official metadata exists;
- environment: local Windows PC;
- GitHub: deliberate source control/remote source backup only;
- cloud execution: not required;
- initial irreversible broker milestone: controlled DEMO after DRY_RUN and deterministic proof;
- REAL trading: preserved future governed capability, disabled/unavailable until DEMO/release/explicit-approval gate passes.

## 6. Product objectives

The system must:

1. read trustworthy account, symbol, quote, candle, position and deal facts through one broker-read boundary;
2. build one immutable normalized cycle snapshot;
3. understand structure, location, liquidity, volatility, session, news and cost context;
4. run dependency-independent analytical work with preserved bounded concurrency plus one-worker parity/fallback;
5. let six independent scalp families build attributable BUY/SELL cases;
6. preserve conflict/correlation explicitly;
7. maintain persistent Opportunity/Episode identity;
8. separate Opportunity quality from executable completed-M5 timing;
9. build structural TradePlan geometry before monetary Risk;
10. retain gross structural quality plus cost-adjusted room;
11. resolve preserved SMALL/MEDIUM/NORMAL account Risk profile and actual min-lot affordability;
12. support explicit disabled-by-default aggressive small-account policy without auto-enabling it;
13. compose hard authorities centrally before broker write;
14. persist one-shot Intent before irreversible submission;
15. reconcile every attempted write against broker truth;
16. manage verified bot-owned trades under the same safety spine;
17. survive restart without forgetting exposure, risk day/profile, Intents, Opportunities or learning obligations;
18. learn only from verified causal outcomes and never self-authorize production changes;
19. expose truthful operator state without making dashboard a second authority.

## 7. What “good” means

Engineering quality means deterministic behaviour for the same facts/configuration, explicit UNKNOWN/error states, no hidden writes, no duplicate submission, no silent restart reset, causal replay, synchronized Documents/source/tests and clear operator reasons.

Trading quality is evaluated later with evidence, not promises. Metrics include expectancy/Net R after realistic costs, gross versus cost-adjusted room, original/realized R, MAE/MFE, entry/capture/exit efficiency, hold duration, family/session/regime attribution, missed/blocked analysis, late-entry avoidance, spread/slippage/latency sensitivity and minimum-lot affordability frequency.

## 8. Strategy floor

Preserved six production families:

```text
Trend Pullback Continuation
Breakout Expansion
Breakout Retest Continuation
Liquidity Sweep Reversal
Failed Breakout Reversal
Compression Expansion
```

Correlation/event lineage prevents one episode from becoming fake multi-confirmation.

## 9. Preserved Risk personality

Automatic DayStartEquity profiles remain:

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

The operator-requested `AGGRESSIVE_SMALL_ACCOUNT` capability is preserved but disabled by default. When explicitly enabled and eligible, 8% is the maximum monetary SL-risk ceiling per trade, **not a target**, while aggregate open-risk and daily-loss ceilings are 16%.

Manual daily-loss reset capability is preserved but disabled by default. The preserved baseline also allows one genuinely fresh same-episode re-entry and applies at least 30 minutes global cooldown after three consecutive closed bot losses plus required fresh/healthy release conditions.

The provisional 0.50% Python scaffold is not canonical production Risk policy.

## 10. Genuine scalp-specific differences

Scalping explicitly changes/strengthens:

- H1/M15/M5 hierarchy with H4 optional;
- short-horizon event/trigger freshness and anti-chase semantics;
- gross plus cost-adjusted room;
- no automatic inheritance of Swing's 1.20R hard Primary floor;
- stronger spread/slippage/drift/latency observability;
- true News UNKNOWN new-entry block with valid-LKG-cache resilience;
- exceptional Runner policy;
- time/efficiency as first-class EXIT reason;
- cost/latency/duration/capture research metrics.

Exact numerical thresholds for these genuine scalp surfaces remain calibration where the topic owner says so.

## 11. Hard non-goals

GoldScalpTrader is not intended to guarantee profit/accuracy/frequency, trade every M1/M5 fluctuation, perform colocated HFT, use M1/tick history as hidden production authority, use martingale/uncontrolled grids/averaging rescue, distort structural stops for monetary convenience, convert missing truth into PASS, let learning/AI bypass hard safety, let dashboards trade, automatically Git commit/push/pull at runtime, depend on paid cloud infrastructure, permit same-scope active-active writers, require partial-profit logic for indivisible minimum volume or silently remove preserved reference features for implementation convenience.

## 12. Safety-first liveness

Market closed, stale data, wide spread, News UNKNOWN, reconciliation pending, Risk lock, no valid Opportunity or presentation degradation are legitimate states. The process stays alive/truthful where possible without inventing permission.

News UNKNOWN blocks new entry while safe management/protection/mandatory CLOSE remains action-sensitive.

## 13. Reference relationship

GoldSwingTraderAI remains the preservation/reference baseline. The permanent exact difference record is `90-governance/DOCUMENTATION_COMPARISON.md`.

Only genuine scalp-specific differences and explicit operator-directed differences remain intentional. Inheritance is not implementation or profitability proof.