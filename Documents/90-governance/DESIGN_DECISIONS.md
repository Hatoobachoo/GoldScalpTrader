# GoldScalpTrader — Design Decision Ledger

**Status:** ACTIVE DRAFT DECISION LEDGER
**Version:** 0.1-foundation-decisions
**Authority:** Durable project decisions, supersession, rationale and challenge outcome tracking.

## 1. How to use this ledger

This ledger protects the reasoning behind the architecture.

If a decision is replaced, the historical decision remains visible and is marked SUPERSEDED. Topic contracts own exact behaviour; this ledger explains why the project chose that behaviour.

Statuses:

| Status | Meaning |
|---|---|
| ACTIVE-DRAFT | current pre-challenge direction |
| ACTIVE-FROZEN | approved current contract |
| SUPERSEDED | retained for history; a later decision owns current behaviour |
| CALIBRATE | architecture fixed; numerical value requires evidence |
| EXTERNAL | real broker/provider/machine evidence required |
| DEFERRED | intentionally outside current V1 scope |

## 2. Foundation decisions

| ID | Decision | Reason / consequence | Status |
|---|---|---|---|
| DEC-001 | `Documents/` is the only canonical project manual | durable truth must not depend on chat memory or parallel documentation trees | ACTIVE-DRAFT |
| DEC-002 | Complete design/documentation precedes feature implementation | prevents code from silently defining product behaviour | ACTIVE-DRAFT |
| DEC-003 | GoldSwingTraderAI is the engineering/reference parent, not a calibration template | preserve reusable architecture while forcing scalp-specific challenge | ACTIVE-DRAFT |
| DEC-004 | Every material change follows full affected-graph synchronization | nearest-file-only updates are insufficient | ACTIVE-DRAFT |
| DEC-005 | Runtime architecture is analytical-parallel but broker-authority-serial | preserves independent hypotheses without multiple irreversible authorities | ACTIVE-DRAFT |
| DEC-006 | One normalized MT5 read boundary owns broker facts | prevents inconsistent hidden reads between strategies | ACTIVE-DRAFT |
| DEC-007 | UNKNOWN required truth never becomes PASS/zero by convenience | fail-safe truth semantics | ACTIVE-DRAFT |
| DEC-008 | Trade Plan defines structure before Risk defines money | account size must not distort market invalidation | ACTIVE-DRAFT |
| DEC-009 | One central execution gate composes hard permission | avoids duplicated/contradictory permission logic | ACTIVE-DRAFT |
| DEC-010 | Persist-before-send one-shot Intent precedes every irreversible broker action | duplicate/retry safety and auditability | ACTIVE-DRAFT |
| DEC-011 | MT5Writer is the sole raw broker-write boundary | irreversible action ownership must be singular | ACTIVE-DRAFT |
| DEC-012 | Learning/research are downstream and cannot acquire broker authority | prevents unstable self-mutating trader behaviour | ACTIVE-DRAFT |
| DEC-013 | Operator dashboards are read-only | presentation cannot become a second trading system | ACTIVE-DRAFT |

## 3. Scalping-specific decisions

| ID | Decision | Reason / consequence | Status |
|---|---|---|---|
| DEC-020 | Scalping is selective short-duration XAU trading, not HFT and not “trade every candle” | sets realistic MT5/retail infrastructure personality | ACTIVE-DRAFT |
| DEC-021 | Spread/slippage/executable Bid/Ask geometry are first-class scalp evidence | small target room can be destroyed by transaction cost | ACTIVE-DRAFT |
| DEC-022 | Opportunity validity and current Entry Timing are separate durable concepts | avoids deleting valid thesis or chasing stale move | ACTIVE-DRAFT |
| DEC-023 | Freshness applies to event lineage, trigger and executable geometry | stale structure is especially dangerous at scalp horizons | ACTIVE-DRAFT |
| DEC-024 | Six independent strategy-family architecture is retained as the starting decomposition | aligns with reference trading floor; family membership remains challengeable | ACTIVE-DRAFT |
| DEC-025 | Final H1/M15/M5/M1/tick role mapping is not inherited blindly | timeframe authority must be optimized for scalping | ACTIVE-DRAFT |
| DEC-026 | Performance evaluation must be transaction-cost and duration aware | win rate alone is insufficient for scalp quality | ACTIVE-DRAFT |
| DEC-027 | One-position-at-a-time remains the initial default | reduces exposure/duplicate complexity for V1; challenge may review | ACTIVE-DRAFT |
| DEC-028 | Martingale, uncontrolled grids and unlimited averaging are prohibited | incompatible with bounded risk architecture | ACTIVE-DRAFT |

## 4. GitHub and local-backup decisions

| ID | Decision | Reason / consequence | Status |
|---|---|---|---|
| DEC-040 | Trading runs locally; GitHub is source/history/remote backup only | zero-cloud-compute design and broker-runtime isolation | ACTIVE-DRAFT |
| DEC-041 | No GitHub Actions/Codespaces/LFS/paid external API dependency | keep architecture compatible with $0 infrastructure target | ACTIVE-DRAFT |
| DEC-042 | Runtime/shutdown must not automatically commit or push to GitHub | removes unnecessary credential/network/account-risk coupling | ACTIVE-DRAFT |
| DEC-043 | Graceful shutdown may create local runtime backup | local recovery is useful and does not require publication | ACTIVE-DRAFT |
| DEC-044 | Automatic backups exclude `.env`, tokens, passwords and MT5 credentials | backup convenience must not create secret leakage | ACTIVE-DRAFT |
| DEC-045 | Default backup destination lives outside repository working tree | prevents recursive archives and accidental commits | ACTIVE-DRAFT |
| DEC-046 | Local recovery architecture has working clone + rolling runtime backup + portable recovery package/Git bundle | separates day-to-day recovery, corruption recovery and GitHub-independent reconstruction | ACTIVE-DRAFT |
| DEC-047 | Optional second physical drive/USB destination is supported conceptually but not required | same-disk backup does not protect against disk loss | ACTIVE-DRAFT |

## 5. Evidence/governance decisions

| ID | Decision | Reason / consequence | Status |
|---|---|---|---|
| DEC-060 | Deterministic tests do not prove profitability/live readiness | prevents exaggerated completion claims | ACTIVE-DRAFT |
| DEC-061 | Every meaningful module requires one implementation owner and proof route | reconstructability and auditability | ACTIVE-DRAFT |
| DEC-062 | Serial semantics must be proved before parallel production concurrency | performance optimization cannot change meaning | ACTIVE-DRAFT |
| DEC-063 | Fresh-from-zero challenge is mandatory before architecture freeze | inherited design must earn its place in the scalp project | ACTIVE-DRAFT |
| DEC-064 | Challenge classifications include KEEP, SMALL IMPROVEMENT, SHOULD CHANGE, MAJOR CHANGE, REMOVE/SIMPLIFY, ADD, CALIBRATE, EXTERNAL PROOF | makes architecture review explicit and comparable | ACTIVE-DRAFT |

## 6. Decisions intentionally not frozen yet

The following require the dedicated topic documents plus fresh-zero challenge:

- final timeframe roles;
- exact six scalp strategy families and overlap boundaries;
- whether M1/tick data is diagnostic, timing evidence or production authority;
- risk profiles and exact percentages;
- daily loss/cooldown numbers;
- spread/slippage thresholds;
- trigger age and Opportunity expiry thresholds;
- time-stop and exit-manager rules;
- news blackout windows;
- DEMO-only versus controlled future LIVE readiness boundary;
- local backup timing/retention counts;
- same-scope laptop handoff details;
- exact graphical dashboard stack.

## 7. Change rule

A decision change is incomplete until:

1. this ledger records the new/superseded decision;
2. owning topic contract is updated;
3. affected architecture/module/coder/operator/research/release documents are synchronized;
4. source/test ownership is synchronized once implementation exists;
5. evidence status is updated without overstating proof.
