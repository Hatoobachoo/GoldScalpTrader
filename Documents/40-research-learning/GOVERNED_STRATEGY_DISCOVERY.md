# GoldScalpTrader — Governed Strategy Discovery

**Status:** DRAFT PRE-CHALLENGE RESEARCH CONTRACT — DISCOVERY IS NOT PRODUCTION
**Version:** 0.1-scalp-governed-discovery
**Authority:** Parameter discovery, declarative strategy-recipe discovery, candidate comparison and evidence-driven scalp-behaviour discovery.

## 1. Purpose

Discovery searches for improvements while preserving production semantics, chronology, transaction-cost realism and hard safety.

It proposes candidates. It does not directly change production Strategy Floor or write to a broker.

## 2. Discovery pipeline and liveness

```text
ResearchEpisodeRecord — actual / missed / blocked / exit / fault evidence
→ audited primitive mapping
→ recurring independent episode cluster
→ eligible + novel?
   yes → declarative StrategyCandidate
   no  → durable suppression/rejection reason
→ validation/promotion stages
→ discovery health
```

Liveness requires:

```text
eligible recurring evidence
→ candidate created and registered
OR
→ explicit machine-readable suppression reason
```

Import success alone is not HEALTHY.

## 3. Automatic evidence feed

Normal operation:

```text
replay or forward outcome
→ ResearchEpisodeRecord
→ durable ResearchEpisodeRepository
→ primitive mapping
→ recurring cluster
→ discovery/invention cycle
→ CandidateRegistry
```

Episodes preserve attribution:

- actual reconciled trade;
- meaningful missed move;
- false/poor entry;
- late/chased entry;
- transaction-cost failure;
- premature/weak-capture exit;
- blocked opportunity;
- capacity-suppressed opportunity;
- broker/system fault.

System faults are not evidence that strategy logic needs changing.

## 4. Discovery levels

### Level A — parameter discovery

Researches bounded analytical/timing/management parameters.

It may not search or weaken hard safety such as identity, daily loss, risk ceiling, no-lookahead, one-shot send, reconciliation, controller fencing or secret handling.

### Level B — strategy recipe discovery

Combines approved primitives into declarative hypotheses with required behaviour, optional support, timing/freshness profile, invalidation model, target model and preferred regime/session.

### Level C — market-behaviour discovery

Clusters recurring missed/losing/winning/late-entry/exit/regime episodes to identify behaviour not represented well by current families.

The objective is falsifiable recurring behaviour, not unlimited random combinations.

## 5. Primitive vocabulary

The audited primitive registry initially includes the reference primitives plus scalp-specific context:

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

Arbitrary strings, executable source and hard-safety concepts are rejected.

## 6. Candidate discipline

Each candidate retains:

- typed ID/version/type;
- parent family where applicable;
- discovery trigger/hypothesis;
- required/optional primitive list;
- regime/session/timing/freshness profile;
- invalidation/target model;
- evidence source IDs and chronology;
- transaction-cost assumptions when relevant;
- semantic fingerprint;
- state/rejection/suppression reason.

Independent episode IDs are required. Repeating one source cannot inflate evidence.

## 7. Similarity and durable memory

Candidates close to an existing family are normally variants. Materially distinct repeated behaviour may qualify as a new family.

Small timing/management changes are ENTRY_POLICY or EXIT_POLICY.

Fingerprints and similarity suppress duplicates. Rejected candidate memory survives restart/local backup.

## 8. Complexity / anti-filter-soup rule

A recipe containing every available indicator/liquidity/confluence primitive is presumed overfit until strong out-of-sample evidence proves otherwise.

Optional confluence can provide bounded positive support but does not automatically become mandatory.

Any extra condition must justify its complexity through ablation, Opportunity Recall, cost-adjusted expectancy, drawdown and trade-frequency evidence.

## 9. Hard exclusions

Discovery cannot optimize away:

- broker/runtime identity;
- closed-candle chronology/no-lookahead;
- monetary risk ceilings / daily lock;
- one-shot submission;
- ambiguous acknowledgement reconciliation;
- controller fencing;
- unknown exposure fail-safe;
- original-R immutability;
- secret/backup integrity;
- broker-writer confinement.

## 10. Candidate evaluation

Candidate stages are owned by promotion governance, not discovery.

A locked candidate whose fingerprint changes becomes a new candidate/version.

Final holdout is one-shot. Explicit approval is required before a candidate can become production policy.

## 11. Production boundary

Discovery runs offline/research. Production runtime reads approved policy configuration only.

Production never invents strategy logic inside a live broker cycle.

## 12. Persistence/dashboard

Restore episodes, clusters, CandidateRegistry, fingerprints, rejection memory, stage and health from verified StateStore/local checkpoint.

Dashboard:

```text
DISCOVERY
Health             IDLE / HEALTHY / DEGRADED
Eligible Clusters  count
Candidate Count    count
Latest             ID • type • stage
Suppression        explicit reason
Broker Authority   NONE
```

A healthy discovery service is not evidence that a profitable candidate exists.

## 13. Planned implementation ownership

```text
src/gold_scalp_trader/research/episode_journal.py
src/gold_scalp_trader/research/discovery.py
src/gold_scalp_trader/research/invention.py
src/gold_scalp_trader/research/promotion.py
```

## 14. Planned proof

Tests cover evidence feed, candidate types, primitive validation, duplicate suppression, restart memory, complexity bounds, promotion handoff and hard-safety exclusions.

Market quality requires chronology-safe replay, fixed-policy walk-forward, untouched holdout, stress, shadow and DEMO evidence.

## 15. Open questions

Per-trigger sample sizes, similarity/complexity limits, resource scheduling, regime/session clustering, latency/cost pattern clustering and final confluence-retention criteria remain research/calibration items.
