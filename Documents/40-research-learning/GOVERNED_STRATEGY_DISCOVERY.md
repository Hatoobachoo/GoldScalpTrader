# GoldScalpTrader — Governed Strategy Discovery

**Status:** FROZEN V1 RESEARCH GOVERNANCE — DISCOVERY IS NOT PRODUCTION
**Version:** 1.0-preservation-first-scalp-discovery
**Authority:** Parameter discovery, declarative strategy-recipe discovery, candidate comparison and evidence-driven scalp-behaviour discovery.

## 1. Purpose

Discovery searches for improvements while preserving production semantics, chronology, transaction-cost realism and hard safety.

It proposes candidates. It does not directly change the Strategy Floor, preserved Risk/session defaults or broker runtime.

## 2. Discovery pipeline / liveness

```text
ResearchEpisodeRecord — actual / missed / blocked / exit / fault
→ audited primitive mapping
→ recurring independent cluster
→ eligible + novel?
   yes → declarative StrategyCandidate
   no  → durable suppression/rejection reason
→ validation/promotion stages
→ discovery health
```

Eligible recurring evidence must produce either candidate or explicit machine-readable suppression reason.

## 3. Evidence feed

Episodes preserve attribution for actual reconciled trades, meaningful missed moves, poor/false entries, late/chased entries, transaction-cost failure, premature/weak-capture exits, blocked/capacity-suppressed opportunities and broker/system faults.

System faults are not evidence that strategy logic should change.

## 4. Discovery levels

### Level A — bounded parameter/policy discovery
May research genuine scalp-sensitive analytical/timing/management values such as event freshness, cost-room, chase distance, time-efficiency and optional confluence.

It may not silently treat preserved non-scalp defaults as ordinary tunable variables.

### Level B — strategy recipe discovery
Combines approved primitives into declarative hypotheses with required behavior, optional support, timing/freshness profile, invalidation, target and preferred regime/session.

### Level C — market-behaviour discovery
Clusters recurring independent episodes to identify behavior not represented well by current six families.

The objective is falsifiable recurring behavior, not unlimited random combinations.

## 5. Approved primitive vocabulary

```text
STRUCTURE_TREND
STRUCTURE_BREAK
MSS_SHIFT
CANDLE_REJECTION
DISPLACEMENT
COMPRESSION
TECHNICAL_LOCATION
TRENDLINE
FIBONACCI
VOLUME_PROFILE_POC
LIQUIDITY_SWEEP
FVG
ORDER_BLOCK
EMA_FLOW
RSI_MOMENTUM
ATR_VOLATILITY
SESSION_CONTEXT
TARGET_PATH
ENTRY_TIMING
EVENT_FRESHNESS
SPREAD_COST_CONTEXT
HOLD_TIME_EFFICIENCY
```

Event freshness, cost context and hold-time efficiency are accepted scalp-specific primitives. Their exact thresholds remain researchable.

M1 may appear as diagnostic/research data but not as hidden production primitive with broker authority.

Unknown strings, executable source and hard-safety concepts are rejected.

## 6. Candidate discipline

Each candidate retains typed identity/version/type, parent family where applicable, trigger/hypothesis, required/optional primitives, regime/session/timing/freshness profile, invalidation/target model, evidence IDs/chronology, cost assumptions, semantic fingerprint and state/rejection/suppression reason.

Independent Episode IDs are required; repeated observations of one episode cannot inflate evidence.

## 7. Preservation-first classification

A candidate affecting an inherited feature/default must carry one of:

```text
SCALP_SPECIFIC_CHANGE
OPERATOR_DIRECTED_CHANGE
REFERENCE_DEFECT_CORRECTION
```

before it can enter promotion toward production. Otherwise the inherited baseline remains preserved.

Examples not silently searchable away include account Risk-profile architecture/bands, manual reset default, one-fresh-reentry baseline, three-loss cooldown baseline, PRE_CLOSE/reopen defaults, one-shot Intent, reconciliation and future REAL release governance.

## 8. Similarity / durable memory

Candidates close to existing family are variants. Materially distinct recurring behavior may qualify as new family. Small timing/management changes are ENTRY_POLICY/EXIT_POLICY.

Fingerprints and similarity suppress duplicates. Rejected-candidate memory survives restart/local backup.

## 9. Complexity / anti-filter-soup rule

Recipes containing every available feature are presumed overfit until ablation, Opportunity Recall, cost-adjusted expectancy, drawdown and frequency evidence justify complexity.

Optional confluence remains bounded support rather than automatic mandatory checklist.

## 10. Hard exclusions

Discovery cannot optimize away broker/runtime identity, closed-candle/no-lookahead, required UNKNOWN handling, structural-stop integrity, one-shot submission, reconciliation, controller fencing, unknown-exposure fail-safe, original-R immutability, secret/backup integrity or sole-writer confinement.

Canonical non-scalp Risk/session defaults require explicit governed reclassification before research can propose production replacement.

## 11. Candidate evaluation / production boundary

Promotion governance owns stages. Locked fingerprint change creates new candidate/version. Final holdout is one-shot. Explicit approval required before production policy.

Production runtime reads approved policy only; it never invents strategy logic inside live broker cycle.

Future REAL authority is separately gated and cannot be granted by discovery/promotion alone.

## 12. Persistence / dashboard

Restore episode journal, clusters, CandidateRegistry, fingerprints, rejection memory, stage and health from verified StateStore/checkpoint.

Dashboard shows Discovery Health, eligible clusters, candidate count, latest ID/type/stage, suppression reason and Broker Authority `NONE`.

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
```

## 14. Planned proof

Tests cover evidence feed, candidate types, primitive validation, duplicate suppression, preservation classification, restart memory, complexity bounds, promotion handoff and hard-safety exclusions.

## 15. Research questions

Per-trigger sample sizes, similarity/complexity limits, resource scheduling, regime/session clustering, latency/cost pattern clustering and optional-confluence retention remain research/calibration items. Preserved non-scalp feature/default policy is not automatically reopened.