# GoldScalpTrader — Trading Floor Architecture

**Status:** DRAFT PRE-CHALLENGE ARCHITECTURE CONTRACT
**Version:** 0.1-scalp-floor
**Authority:** Specialist-team ownership, staged analytical parallelism, opportunity capture and hard-authority boundaries.

## 1. Why a trading floor

GoldScalpTrader is not one giant strategy function and not a checklist bot that requires every indicator to agree.

Each specialist desk asks a bounded question, publishes a typed result, and has an explicit authority limit.

The floor has two simultaneous objectives:

1. build evidence-rich, internally challenged scalp theses;
2. preserve Opportunity Recall so valid short-duration Gold moves are not discarded merely because an optional desk is neutral or unavailable.

Soft analytical evidence and hard safety authority must remain separate.

## 2. Opportunity-first, not trade-frequency-first

Opportunity-first does not mean “trade often.” It means:

- optional disagreement stays visible as score/conflict/debate;
- one strong attributable family may lead when others are neutral;
- required safety failures remain hard blocks;
- stale or cost-dominated opportunities expire rather than being chased;
- frequency is an output of qualified market conditions, not a target that overrides quality.

## 3. Shared immutable truth

All analytical desks receive one normalized MarketSnapshot and declared upstream reports.

No desk may secretly fetch a fresher MT5 value and create a private version of reality.

Where live/tick evidence is later approved, it must enter through an explicit normalized boundary and carry its own timestamp/identity.

## 4. Proposed staged floor

### Stage A — Core fact/intelligence desks

Candidate core desks:
- Candle/Structure;
- Indicators/Volatility;
- Session Context;
- execution-cost/quote context.

These produce broadly reusable facts for the rest of the floor.

### Stage B — Specialist desks

Candidate specialist desks:
- Technical Structure/Levels;
- Liquidity/SMC;
- Fundamental/News context;
- optional Trendline/Fibonacci/Volume POC confluence;
- scalp microstructure/freshness desk if the challenge justifies a separate owner.

Specialist outputs remain evidence, not broker authority.

### Stage C — Strategy-family teams

Independent strategy families evaluate the same IntelligenceSnapshot.

GoldSwingTraderAI uses six independent families. GoldScalpTrader will preserve a six-family architecture as the starting design unless the fresh-zero scalp challenge shows a different count materially improves clarity or avoids duplicated hypotheses.

Candidate scalp families to challenge rather than freeze immediately:

1. **Trend Pullback Continuation** — short-horizon continuation after controlled retracement into valid structure/location.
2. **Breakout Retest Continuation** — fresh break/displacement followed by valid executable retest.
3. **Liquidity Sweep Reversal** — sweep/probe and reclaim with fresh reversal structure.
4. **Failed Breakout Reversal** — failed acceptance beyond a meaningful level followed by reclaim/invalidation geometry.
5. **Momentum Expansion Continuation** — fresh compression-to-expansion or displacement continuation when entry is not late/cost-dominated.
6. **Range Extreme / Mean-Reversion Scalp** — qualified range-edge rejection/reclaim under non-trending conditions.

Names, membership and exact evidence requirements are DRAFT and must be challenged before freezing.

## 5. Family independence

A strategy family:
- owns one market hypothesis;
- receives shared evidence;
- may request bounded family-specific evidence already available in typed reports;
- publishes BUY/SELL/neutral thesis information and reasons;
- preserves family attribution;
- never owns monetary sizing;
- never owns hard session/news permission;
- never owns account/controller identity;
- never sends an order.

No family may become a hidden sequential gate for every other family.

## 6. BUY and SELL teams

BUY and SELL are built independently.

Strong SELL evidence should not be represented merely by subtracting points from BUY confidence. The system preserves both theses so conflict is visible and auditable.

The directional floor should be able to answer:
- strongest BUY family and evidence;
- strongest SELL family and evidence;
- supporting/contradicting desks;
- evidence coverage/availability;
- correlation/duplication concerns;
- freshness/cost concerns;
- why one side leads or why neither is actionable.

## 7. Red Team / Debate

The leading direction is challenged before Opportunity creation.

Red Team questions may include:
- Is the move already late?
- Is the thesis using stale structure/liquidity evidence?
- Is opposing structure too close?
- Is the apparent breakout only a probe?
- Is volatility collapsing/expanding against the thesis?
- Is spread/executable cost consuming too much target room?
- Are multiple supporting signals actually the same underlying event counted several times?
- Is the setup dependent on optional unavailable evidence?

Red Team creates analytical challenge, not broker authority.

## 8. Floor Manager

The Floor Manager receives attributable family reports and debate output and publishes an auditable DecisionBoard.

It may produce:
- BUY_LEADS;
- SELL_LEADS;
- CONFLICTED;
- WAIT;
- NO_QUALIFIED_OPPORTUNITY;
- degraded/unknown analytical classifications where applicable.

It does not set monetary risk or grant final permission.

## 9. Opportunity lifecycle

A qualified directional thesis becomes a persistent Opportunity rather than a transient loop result.

Opportunity should carry enough identity to prevent duplicates and stale re-entry, including candidate fields such as:
- opportunity ID;
- direction;
- primary family;
- originating structural/liquidity event IDs/timestamps;
- location/reference zone;
- creation/knowledge time;
- policy/version identity;
- lifecycle state;
- latest valid timing window;
- terminal reason when missed/invalidated/expired/executed.

Exact fields will be specified in the decision contracts.

## 10. Entry Timing boundary

Opportunity asks “is this thesis worth stalking?”

Entry Timing asks “is it executable now?”

Entry Timing may use finer, fresh evidence but cannot silently change the original thesis into a different setup.

Scalp timing must explicitly guard against:
- chase distance;
- stale trigger;
- spread deterioration;
- trigger-to-current-price drift;
- already-consumed target room;
- false microstructure confirmation;
- duplicate entry on the same event.

## 11. Parallel execution model

Strategy families are logical peers and may later run in bounded parallel.

Rules:
- same immutable input;
- no side effects;
- deterministic output ordering;
- bounded workers;
- serial fallback produces equivalent meaning;
- worker exception is visible/degraded, not fabricated neutral evidence;
- no broker read/write inside strategy workers.

## 12. Hard-authority handoff

The floor ends before money/broker authority begins.

```text
DecisionBoard
→ Opportunity
→ Entry Timing
→ Trade Plan
---------------- analytical/geometry boundary ----------------
→ monetary Risk
→ hard permission authorities
→ central Gate
→ Intent
→ MT5Writer
```

This boundary is non-negotiable unless governance explicitly replaces it.

## 13. Dashboard relationship

The dashboard may show desk reports, leading family, BUY/SELL conflict, Opportunity state, timing state and reasons.

It may not compute a secret alternative signal or turn a display button into broker authority without a separate documented control architecture.

## 14. Research relationship

Family attribution must survive through trade, close and learning so research can evaluate each family without reconstructing strategy ownership from P/L alone.

Research may propose threshold/family changes. Production changes require governed promotion.

## 15. Fresh-zero challenge targets

The challenge must test:
- whether six families remain the best decomposition for scalping;
- overlap/correlation between reversal families;
- whether momentum expansion deserves its own family;
- whether range mean-reversion should be production or research-only;
- exact timeframe/evidence role per family;
- whether M1/tick evidence belongs in Entry Timing, Intelligence or diagnostics;
- how cost/freshness should influence Floor Manager versus later Trade Plan/Risk;
- whether any family creates sequential-filter-soup behaviour.
