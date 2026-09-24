# GoldScalpTrader — Reference versus Scalp Canonical Documentation

**Status:** DRAFT COMPARISON RECORD — PRE-CHALLENGE
**Version:** 0.1-reference-to-scalp
**Authority:** Explains what is preserved from GoldSwingTraderAI, what changes for scalping and what remains evidence/calibration rather than copied truth.

## 1. Purpose

GoldSwingTraderAI and GoldScalpTrader are not competing versions of one trading personality.

They share a deliberate engineering/governance lineage while serving different trading horizons.

```text
GoldSwingTraderAI Documents/ → reference architecture and preservation source
GoldScalpTrader Documents/   → sole current authority for the scalp project
```

Reference docs never override a current scalp topic contract.

## 2. What is intentionally similar

Preserve conceptually:

- documentation-first development;
- canonical reading order/governance;
- one MT5 read boundary;
- typed immutable market facts;
- causal completed-candle chronology;
- specialist intelligence desks;
- independent strategy-family hypotheses;
- BUY/SELL debate/Floor Manager;
- persistent Opportunity versus entry timing;
- structural TradePlan before money;
- independent monetary Risk;
- session/news/system authority separation;
- central Gate;
- one-shot Intent / sole writer / reconciliation;
- controller fencing;
- ManagedTrade lifecycle;
- strict persistence/recovery;
- verified-close learning;
- research/discovery/promotion isolation;
- read-only dashboards;
- code/test/audit/governance discipline.

## 3. Main trading-personality differences

| Area | Swing reference | Scalp draft |
|---|---|---|
| objective | meaningful intraday/open-session directional move | short-duration repeatable qualified scalp |
| broad context | H4/H1 strong role | H1 primary broad baseline; H4 optional |
| opportunity | M15 | M15 location + M5 setup emphasis |
| entry | completed M5 | M5 primary, M1 role challenged |
| event freshness | important | first-class / tighter |
| cost sensitivity | material | central analytical/execution concern |
| runner | meaningful continuation path | exceptional, not default |
| time efficiency | secondary | first-class scalp management question |
| strategy families | six | same starting six, fresh-zero challenge required |
| structural R | reference floor 1.20R | not frozen; cost-aware scalp policy pending |
| risk bands | reference profiles | architecture only preserved; numbers reopened |
| News UNKNOWN | adaptive open-session behaviour | policy reopened for scalp event sensitivity |

## 4. Backup/repository difference

Reference GoldSwingTraderAI includes automatic graceful-shutdown repository publication/push.

GoldScalpTrader intentionally replaces it with:

```text
local transactional StateStore
→ rolling verified local checkpoint
→ final verified local shutdown checkpoint
→ portable local recovery package
→ optional deliberate local Git bundle at source milestones
```

No runtime Git credential or automatic push authority.

## 5. Historical audit findings

Reference audits are valuable engineering lessons, especially around:

- causal event timestamps;
- stale/live geometry;
- opportunity identity;
- TradePlan family-specific invalidation;
- blocker-vs-Gate presentation;
- close/recovery ordering;
- document/code/test synchronization.

They are not copied as GoldScalpTrader findings.

Scalp audit files begin `NOT RUN` and are populated only by scalp evidence.

## 6. Reference thresholds versus scalp policy

Any reference number enters GoldScalpTrader as one of:

```text
DRAFT seed
CALIBRATE
EXTERNAL PROOF
REJECTED
```

never “frozen by inheritance.”

Examples include risk percentages, R floor, news windows, pre-close timing, reopen clean bars, cooldown duration and M1 role.

## 7. Additional scalp-specific design surfaces

GoldScalpTrader explicitly elevates:

- event/trigger age;
- distance travelled since trigger;
- spread-to-target/stop context;
- approved-entry drift;
- decision/order latency diagnostics;
- hold duration/time exits;
- minimum-lot affordability frequency;
- cost-aware replay/stress;
- avoiding accidental swing conversion.

## 8. Final comparison process

After all 64 files exist, `AUDIT_1_FRESH_DESIGN_REVIEW.md` must decide whether each inherited architecture component is:

```text
KEEP AS-IS
SMALL IMPROVEMENT
SHOULD CHANGE
MAJOR ARCHITECTURAL CHANGE
REMOVE / SIMPLIFY
ADD
CALIBRATE
EXTERNAL PROOF
```

This comparison file then updates to final frozen differences.
