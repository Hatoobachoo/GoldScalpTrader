# GoldScalpTrader — Audit 5: Deep Zero-Trade Gate and Event Freshness Review

**Status:** FINAL CORRECTIVE AUDIT PROTOCOL — NOT RUN AGAINST IMPLEMENTATION
**Version:** 2.0-setup-freshness-gate
**Authority:** Deep diagnosis of stale setup reuse, terminal re-arm, active-family mismatch, M1 freshness and false Gate attribution when live trades are unexpectedly absent.

## 1. Purpose

Audit 5 is used when Audit 4 shows that apparently valid opportunities are being lost before execution and simple geometry review is insufficient.

Focus:

```text
setup identity
causal event freshness
active/shadow eligibility
Opportunity lifecycle
M1 trigger freshness
terminal lock/re-arm
upstream-vs-Gate reason truth
```

## 2. Core historical lesson

A terminal setup must not silently re-arm just because a new polling cycle or candle appears.

```text
same unchanged causal thesis
→ same terminal lineage
→ no fake new Opportunity

material fresh event
→ new/renewed causal eligibility under policy
```

## 3. Setup Detector audit

For each missed period verify:

- which family setup(s) were actually detected;
- whether active-family setup was genuinely present;
- whether an active-family score was generated despite no setup;
- whether a shadow setup was incorrectly ignored or incorrectly promoted live;
- whether multiple setup candidates shared one causal event.

A setup detector that always emits the active family is a critical defect.

## 4. Event freshness audit

For every active-family candidate record:

```text
source event ID
source event knowledge time
M5 event age
Opportunity created/updated time
M1 trigger event/time/age
Approved Entry Reference time
current executable quote time
```

Then verify no stage uses a stale timestamp as if newly created.

## 5. Opportunity lifecycle audit

Expected transitions:

```text
DISCOVERED → ARMED → WAITING/READY
READY → TRIGGERED
ARMED/WAITING/READY → MISSED/INVALIDATED
terminal → re-arm only with fresh causal event + policy permission
```

Find:

- identity reset on every loop;
- lost persistent Opportunity;
- stale READY surviving restart;
- MISSED becoming READY without fresh event;
- re-entry allowance bypass.

## 6. M1 freshness audit

M1 is subordinate but production-relevant for timing.

Check:

- M5 Opportunity existed first;
- M1 data was causally available;
- trigger age/freshness correctly computed;
- later micro trigger did not rewrite earlier M5 setup time;
- M1 WAIT did not permanently delete valid M5 setup prematurely;
- M1 alone never originated production Opportunity.

## 7. Gate audit

If a path stops because:

```text
ACTIVE_FAMILY_SETUP_NOT_PRESENT
M1_NOT_READY
M5_EVENT_STALE
ENTRY_CHASED
TradePlan invalid
quality poor
Risk blocked
```

then:

```text
Gate = NOT_EVALUATED
```

Audit searches logs/UI for false Gate BLOCKED labels.

## 8. Shadow evidence audit

If market repeatedly forms valid shadow setups while active family rarely appears, record that as strategy-evaluation evidence.

Do not fix by silently allowing shadow live trades.

Correct output may become:

```text
Active family low opportunity rate
Shadow family high opportunity + positive counterfactual evidence
→ candidate production-family switch
→ promotion governance
→ APPROVAL_REQUIRED
```

## 9. Freshness threshold review

Thresholds are not changed merely because trade count is low.

For M5 age, M1 freshness, chase and drift compare:

- entries prevented;
- after-the-fact favorable move;
- after-cost expectancy;
- adverse excursion;
- false-block rate;
- session/regime differences.

Any change becomes a versioned calibration candidate.

## 10. Required tests

```text
test_setup_detector_not_active_family_biased
test_terminal_setup_lock
test_fresh_event_rearm
test_m5_event_age
test_m1_trigger_freshness
test_m1_requires_opportunity
test_restart_ready_revalidation
test_shadow_setup_remains_shadow
test_gate_not_evaluated_for_freshness_stop
```

## 11. Current status

Protocol reflects the final one-active-family / M1-refinement architecture and remains **NOT RUN** until implementation/evidence exists.
