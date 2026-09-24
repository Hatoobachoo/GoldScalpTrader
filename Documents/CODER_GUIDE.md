# GoldScalpTrader — Coder Guide

**Status:** POST-AUDIT-1 DEVELOPER MANUAL — PRESERVATION-FIRST CORRECTED, IMPLEMENTATION NOT STARTED
**Version:** 1.2-preserved-feature-handoff
**Authority:** Developer navigation, phase boundaries, source/test ownership, implementation traces and completion evidence.

## 1. Read before code

GoldScalpTrader is documentation-first. Repository truth beats remembered chat.

Current sequence:

```text
64-file canonical manual              COMPLETE
Fresh-Zero Audit 1                    COMPLETE + preservation correction
Affected-graph semantic sync          CURRENT
Metadata/cross-link normalization     PENDING
Final operator scalp-delta discussion PENDING
Implementation                        NOT STARTED
```

### Preservation-first coding rule

GoldSwingTraderAI feature/default behaviour remains baseline unless the current Scalp documents show a direct scalp-specific change, an explicit operator-directed change, or a proven reference defect correction.

Do not simplify/remove a reference feature because a smaller implementation is easier.

## 2. Authority reading order

1. `README.md` + `GLOSSARY.md`;
2. `00-foundation/SYSTEM_CONTRACT.md`;
3. owning topic contract;
4. `DESIGN_DECISIONS.md` + `OPEN_QUESTIONS.md`;
5. `DOCUMENTATION_COMPARISON.md` + `PRESERVATION_LEDGER.md` when reference behaviour is involved;
6. Architecture / Trading Floor;
7. Coding Standard;
8. Module Structure + File/Test Catalog;
9. current source/tests/evidence.

## 3. Architectural spine

```text
one normalized MT5 read boundary
→ immutable MarketSnapshot
→ staged bounded-parallel intelligence
→ six independent scalp families
→ BUY / SELL fusion + Red Team
→ persistent Opportunity
→ completed-M5 Entry Timing / event freshness
→ family-aware TradePlan
→ gross + cost-adjusted room
→ SMALL/MEDIUM/NORMAL monetary Risk
   + optional explicit disabled-by-default aggressive overlay
→ hard session/news/system/account/controller authorities
→ central Gate
→ durable one-shot Intent
→ sole MT5Writer
→ broker reconciliation
→ ManagedTrade / Trade Manager
→ verified close
→ exactly-once learning
→ research/discovery/promotion
→ local checkpoint/recovery
```

## 4. Timeframe authority

```text
H1   broad soft regime
M15  opportunity/location/path
M5   primary completed-bar setup/timing/management
H4   optional major context
M1   diagnostic/research only
quote executable Bid/Ask/spread/drift/health
```

## 5. Bounded parallel versus serial authority

Preserve bounded concurrency for dependency-independent analytical work.

Implementation requirements:

- immutable shared inputs;
- bounded workers/resources;
- deterministic result order;
- no lifecycle/broker side effects in workers;
- one-worker fallback;
- one-worker ↔ bounded-parallel semantic parity tests.

Must remain serial:

```text
TradePlan
→ Risk profile/overlay
→ hard permissions
→ Gate
→ Intent persisted
→ fresh broker checks
→ sole writer
→ reconciliation
```

## 6. Preserved Risk contract

```text
SMALL   DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal | Elevated | Hard | Daily |
|---|---:|---:|---:|---:|
| SMALL | 3.0–4.5% | >4.5–6.5% | 7% | 12% |
| MEDIUM | 2.0–3.0% | >3.0–4.5% | 5% | 9% |
| NORMAL | 1.0–2.0% | >2.0–3.5% | 4% | 7% |

Preserved explicit optional overlay:

```text
AGGRESSIVE_SMALL_ACCOUNT disabled by default
eligible baseline < $1,000
8% max monetary SL risk — NOT target
16% aggregate open-risk cap
16% daily-loss ceiling
```

Manual reset capability remains disabled by default. Baseline re-entry/cooldown remains one genuinely fresh same-episode re-entry and three consecutive closed losses → at least 30 minutes global cooldown plus release conditions.

The provisional 0.50% scaffold is not production policy.

## 7. Session / News / cache

Preserve:

```text
Provider TTL 1800s
Daily PRE_CLOSE T-20 / T-10
Weekend PRE_CLOSE T-60 / T-30
Daily reopen 1 clean M5
Weekend reopen 2 clean M5 + gap assessment
```

Current broker schedule remains external proof.

Scalp-specific News rule:

```text
true NEWS_UNKNOWN → new-entry BLOCK / LIMITED
refresh failure + valid LKG cache → use cached accepted truth
refresh failure + expired/invalid/no cache → UNKNOWN
```

Never rewrite cache timestamps/TTL to keep trading.

## 8. Scalping engineering hotspots

### Freshness
Keep bar identity, knowledge time, event time, Opportunity/TradePlan creation, decision, Intent/precheck/send/reconcile timestamps distinct.

### Cost / geometry
Keep gross geometry, Approved Entry Reference, current Bid/Ask/spread, explicit reserves and Actual Fill distinct. Never double-count costs or change SL/target to improve apparent R.

### 1.20R
Swing's 1.20R is not automatically a hard scalp entry floor. Exact scalp gross/net thresholds are a genuine scalp calibration item.

### Management
Runner is exceptional. Time weakness can produce normal `EXIT`. Optional partial management remains supported where broker-valid/divisible; correctness at minimum lot never depends on it.

## 9. Runtime capability progression

```text
READINESS / DRY_RUN
→ controlled DEMO
→ future governed REAL
```

REAL is preserved as a future feature but is disabled/unavailable until its separate DEMO/release/explicit-approval gate passes.

## 10. UNKNOWN / corrupt / ambiguous examples

```text
positions_get == []   → verified zero
positions_get == None → unavailable, not zero
News refresh fail + valid cache → accepted cached truth, provider may be DEGRADED
News refresh fail + invalid/no cache → NEWS_UNKNOWN
unknown equity/profile state → Risk UNKNOWN
ambiguous send → reconcile, never resend blindly
```

## 11. Runtime persistence / backup

```text
transactional StateStore
→ rolling local checkpoint
→ graceful-shutdown final local checkpoint
→ portable runtime recovery package when requested
```

No runtime Git operation.

Development/source backup:

```text
one coherent remote commit
→ operator git pull --ff-only
→ local clone = latest source + full Git history
→ optional clean ZIP
```

## 12. Planned source ownership

Use `MODULE_STRUCTURE.md` and `FILE_AND_TEST_CATALOG.md` as exact planned source/test maps. Key owners include:

- `market_data/*` one read boundary;
- `strategies/parallel.py` bounded analytical scheduler;
- `risk/engine.py`, `state.py`, `permissions.py` profiles/overlay/risk state;
- `app/session_news.py` provider/cache transport;
- `execution/*` Gate/Intent/writer/reconciliation;
- `management/*` post-entry management;
- `persistence/*` local durable state/recovery;
- `operator/*` read-only presentation;
- `research/*` downstream evidence/proposals.

## 13. Feature packet before coding

Every material feature defines purpose, one owner, typed inputs/freshness, outputs/state, parallel-vs-serial boundary, failure semantics, persistence, tests, operator view, research effect, release proof and full affected documentation graph.

For inherited behavior, also record whether it is preserved or a justified scalp/operator delta.

## 14. Context-loss recovery

```text
inspect main HEAD
→ README / Documentation Standard
→ System Contract / Architecture
→ Comparison / Preservation Ledger
→ relevant topic + Decisions/Open Questions
→ Module Structure / File-Test Catalog
→ current source/tests/evidence
→ continue first incomplete dependency
```

## 15. Completion classification

Use DONE / PARTIAL / MISSING / BROKEN / SCALP CALIBRATION PENDING / EXTERNAL PROOF PENDING.

Green tests alone never mean the project is complete or profitable.

## 16. Next implementation dependency

No implementation starts until Documentation Audit closes affected-graph + metadata/cross-link work and the operator completes the final documentation discussion of genuine scalp-specific differences.