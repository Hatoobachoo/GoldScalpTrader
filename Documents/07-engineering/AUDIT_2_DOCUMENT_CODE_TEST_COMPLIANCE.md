# GoldScalpTrader — Audit 2: Document → Code → Test Compliance

**Status:** CURRENT IMPLEMENTATION TRACE UPDATED / OPERATOR OFFLINE RE-VERIFICATION REQUIRED  
**Version:** 2.7-authority-shadow-stage-proof-trace  
**Authority:** Traceability from canonical contract to source owner to deterministic proof, with connected Exness facts explicitly separated.

## 1. Evidence rule

```text
canonical contract
→ actual source owner
→ deterministic/integration proof
→ full offline verifier
→ connected proof where broker reality is required
```

A lower evidence layer cannot substitute for a higher one.

## 2. Last operator-validated baseline

The last fully reported Windows offline PASS was before the current authority/shadow/stage-proof packet. Therefore current HEAD must not inherit PASS until `python scripts/verify_offline_release.py` is rerun.

## 3. High-risk current trace

| Requirement | Implementation owner | Current status |
|---|---|---|
| normalized MT5 reads | `market_data/mt5_reader.py` | IMPLEMENTED; connected broker facts external |
| market-first six-family detection | `strategies/floor.py`, `setup_detector.py` | IMPLEMENTED |
| one active / five shadow isolation | `strategies/isolation.py` | IMPLEMENTED |
| persistent M5 Opportunity | `app/opportunity_lifecycle.py` | IMPLEMENTED |
| M1 subordinate timing only | `decisions/timing.py` | IMPLEMENTED |
| durable timing/management lineage | runtime/ManagedTrade/research | IMPLEMENTED |
| frozen Risk profiles/ceilings | config/risk | IMPLEMENTED |
| durable UTC DayStartEquity live sizing | `risk/runtime.py` + `app/runtime.py` | IMPLEMENTED; new regression proof added |
| daily lock / 3-loss cooldown | risk state/runtime | IMPLEMENTED; connected deal drill external |
| hard Session authority | `app/session_authority.py`, `app/runtime.py` | IMPLEMENTED; caller override removed |
| News soft only | provider/intelligence boundary | IMPLEMENTED |
| sole public guarded DEMO runtime | `app/runtime.py` | IMPLEMENTED |
| duplicate executable core path removed | `app/runtime_core.py` | IMPLEMENTED mechanics-only |
| Gate / persist-before-send / one-shot | execution service/writer | IMPLEMENTED offline |
| controller fencing immediately before send | controller/service | IMPLEMENTED |
| ambiguous ACK reconciliation | execution/reconcile/runtime mechanics | IMPLEMENTED offline; real drill external |
| verified close / exactly-once actual learning | management/live learning | IMPLEMENTED |
| automatic causal shadow outcomes | `research/shadow_runtime.py`, `outcomes.py` | IMPLEMENTED; new deterministic proof added |
| research failure isolation | `app/demo_runner.py` | IMPLEMENTED; broker result remains authoritative |
| immutable candidate stage proof | `research/stage_orchestrator.py`, registry | IMPLEMENTED; direct arbitrary PASS issuer removed |
| runtime activation from research | candidate registry | FORBIDDEN / returns false |
| checkpoint all namespaces | persistence/checkpoint | IMPLEMENTED |
| REAL | config/startup/runtime | HARD DISABLED |

## 4. Runtime authority correction

The canonical guarded DEMO function no longer accepts a `market_open` caller override. Hard Session permission is resolved internally from scoped provider facts and broker symbol capability.

`app/runtime_core.py` no longer exposes a second full guarded DEMO cycle. It is mechanics-only.

New-entry monetary sizing is deferred until durable Risk-day authority has reconstructed/frozen DayStartEquity and passed daily-lock/cooldown/context checks. Current equity cannot silently change the Risk profile intraday.

## 5. Controller / recovery decision

GoldSwingTrader's long-lived heartbeat was reviewed. GoldScalp does not blindly copy it because its controller lease is mutation-scoped and `execute_once()` re-verifies fencing immediately before irreversible send, after broker prechecks. Adding a separate heartbeat would add moving state without a demonstrated safety gain for this architecture.

Recovery remains broker-truth-first: unresolved Intent or missing ManagedTrade position requires reconciliation/exact deal proof; UNKNOWN is not treated as flat.

## 6. SHADOW_ONLY learning correction

Qualified shadow families now have an automatic causal lifecycle:

```text
same-market qualified SHADOW_ONLY candidate
→ stable family/direction/source-event episode identity
→ subordinate M1 timing
→ family-aware hypothetical structural plan
→ contemporaneous entry/SL/target + explicit quoted-spread cost-R
→ only future completed M1 candles
→ TARGET / STOP / AMBIGUOUS / unresolved
→ durable research-only outcome
```

No Risk/Gate/Intent/writer authority exists in this path. Same-bar TP+SL ordering remains ambiguous. A terminal episode marker prevents duplicate recreation/counting.

## 7. Governed research correction

Candidate registry stage evidence can no longer be created from an arbitrary caller-provided SHA and automatically labeled PASS. The verified stage-package protocol requires:

- immutable evidence-package integrity;
- recomputed EvidenceIdentity;
- exact candidate fingerprint;
- exact next target stage;
- package-manifest SHA-256 binding;
- stage-specific required checks;
- zero runtime/broker authority.

No performance threshold is fabricated where frozen policy has not defined one. Production research stage still requires explicit operator approval and rollback lineage, and it still cannot directly activate runtime.

## 8. Research failure isolation

Timing/management/shadow evidence recording occurs after the governed broker cycle and is best-effort relative to financial authority. Research persistence failure is surfaced as degraded research evidence; it cannot make a completed broker write disappear, trigger blind resend, or relabel broker outcome as a runtime failure.

## 9. Connected proof still required

The following remain external until actually observed on the intended Windows + Exness DEMO scope:

- exact SymbolSpec/filling/stops/freeze/margin/order-check behavior;
- actual broker schedule/PRE_CLOSE/DST/holiday/maintenance;
- controlled OPEN/MODIFY/PROTECT/TRAIL/CLOSE lifecycle;
- actual fills/slippage/deviation and latency distributions;
- broker-side TP/SL visibility;
- manual known-trade close attribution;
- ambiguous ACK/no duplicate under real broker behavior;
- restart during active exposure;
- 3-loss cooldown from actual closed deals;
- fresh-machine restore/sequential handoff;
- statistically meaningful active/shadow/timing/management evidence.

## 10. Current verdict discipline

```text
SOURCE/CONTRACT FORENSIC CORRECTIONS      IMPLEMENTED
CURRENT OFFLINE VERIFIER                  NOT YET RERUN BY OPERATOR
CONNECTED EXNESS FACTS                    NOT PROVEN
FULL CONNECTED DEMO CERTIFICATION         PENDING
FUTURE REAL RELEASE                       HARD DISABLED
```

No profitability claim is made.
