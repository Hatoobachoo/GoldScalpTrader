# GoldScalpTrader — Documentation Preservation Ledger

**Status:** POST-AUDIT-1 PRESERVATION LEDGER — PRESERVATION-FIRST CORRECTED
**Version:** 1.1-preserve-reference-unless-scalp-specific
**Authority:** Proof that GoldSwingTraderAI design meaning, features and defaults are preserved unless a direct scalp requirement, explicit operator instruction or proven reference defect justifies a change.

## 1. Preservation rule

GoldScalpTrader changes trading horizon, not the entire product feature set.

```text
reference feature/default
→ preserve by default
→ change only for direct scalp reason, explicit operator instruction, or proven defect
→ if uncertain, preserve now and discuss at final documentation review
```

A simpler design is not by itself a valid reason to delete an inherited feature.

## 2. Preserved reference meaning/features

| Reference subject | Current verdict |
|---|---|
| documentation-first governance | KEEP |
| one MT5 read boundary / immutable snapshot | KEEP |
| causal completed-candle chronology | KEEP |
| staged intelligence | KEEP |
| bounded analytical concurrency + one-worker fallback | KEEP |
| six strategy families | KEEP |
| BUY/SELL + Red Team | KEEP |
| persistent Opportunity vs timing | KEEP |
| structural TradePlan before Risk | KEEP |
| SMALL/MEDIUM/NORMAL Risk profiles | KEEP / RESTORED |
| reference profile risk bands/daily locks | KEEP / RESTORED |
| dynamic broker-aware min-lot sizing | KEEP |
| manual daily-loss reset capability, disabled by default | KEEP / RESTORED |
| cooldown / fresh same-episode re-entry | KEEP / RESTORED |
| PRE_CLOSE / reopen safety defaults | KEEP / RESTORED, subject to current broker proof |
| central Gate / Intent / sole writer / reconcile | KEEP |
| manual/external ownership separation | KEEP |
| ManagedTrade / verified close | KEEP |
| broker-valid partial management where divisible | KEEP |
| persistence/recovery | KEEP |
| learning/research/discovery/promotion boundaries | KEEP |
| read-only dashboards | KEEP |
| future governed REAL capability | KEEP / RESTORED, disabled until its gate |

## 3. Preserved monetary Risk defaults

```text
SMALL   positive DayStartEquity < $300
MEDIUM  $300–$999.99
NORMAL  >= $1,000
```

| Profile | Normal / target | Elevated | Hard ceiling | Daily lock |
|---|---:|---:|---:|---:|
| SMALL | 3.0%–4.5% | >4.5%–6.5% | 7% | 12% |
| MEDIUM | 2.0%–3.0% | >3.0%–4.5% | 5% | 9% |
| NORMAL | 1.0%–2.0% | >2.0%–3.5% | 4% | 7% |

Preserved operator-requested overlay:

```text
AGGRESSIVE_SMALL_ACCOUNT = disabled by default
eligible baseline: positive DayStartEquity < $1,000
8% max monetary SL-risk ceiling — NOT target
16% max aggregate open risk
16% daily loss ceiling
```

## 4. Preserved session/provider defaults

Until current broker/provider facts or a specifically justified change supersede them:

```text
Provider TTL        1800 seconds
Daily PRE_CLOSE     T-20 no entry / T-10 flatten
Weekend PRE_CLOSE   T-60 no entry / T-30 flatten
Daily reopen        1 clean completed M5
Weekend reopen      2 clean completed M5 + gap assessment
```

A broker schedule change proven externally is a fact update, not a scalp strategy redesign.

## 5. Genuine scalp-specific changes

GoldScalpTrader intentionally changes or strengthens:

- H1/M15/M5 hierarchy with H4 optional;
- M5 short-horizon setup/timing/management emphasis;
- event/trigger freshness, stale-for-entry and anti-chase semantics;
- gross plus cost-adjusted target-room truth;
- stronger spread/slippage/drift/latency observability;
- Swing 1.20R not automatically imposed as the hard scalp floor;
- true News UNKNOWN blocks new scalp entry;
- valid LKG cache can preserve accepted News truth across temporary API failure without timestamp laundering;
- Runner is exceptional;
- time/efficiency is a first-class EXIT reason;
- scalp research explicitly measures costs, latency, duration and capture efficiency.

## 6. Explicit operator-directed differences

These remain even though they are not inherently scalping changes:

### Runtime Git publication removed

```text
trading runtime → no Git commit/push/pull
```

### Development source backup

```text
major coherent remote commit
→ operator git pull --ff-only
→ local clone with full Git history
→ optional secret-clean ZIP milestone copy
```

### Aggressive small-account option

Preserved exactly as an explicit disabled-by-default operational feature, not demoted to research-only.

## 7. Earlier unintended simplifications — superseded

The following earlier Scalp draft decisions are **not current authority**:

- replacing SMALL/MEDIUM/NORMAL with one STANDARD policy;
- discarding/reopening all reference Risk percentages;
- demoting 8%/16% mode to research-only;
- reopening cooldown/re-entry defaults without scalp cause;
- removing exact PRE_CLOSE/reopen baselines without scalp cause;
- reopening 1800-second provider TTL without provider/scalp cause;
- treating bounded analytical concurrency as a removable optimization;
- describing REAL as a removed feature rather than a gated future capability;
- wording that could imply optional partial management was removed.

These are restored through the current affected-graph packet.

## 8. Historical/reference evidence boundary

GoldSwingTraderAI audit findings remain valuable lessons but do not count as GoldScalpTrader implementation PASS evidence.

Preserving a reference feature does not claim its Scalp code already exists or that its external broker evidence is current.

## 9. Final discussion rule

Before documentation freeze, the operator will be shown the remaining **genuinely scalp-specific** differences and calibration questions.

Non-scalp reference features/defaults are not reopened for redesign during that discussion unless the operator explicitly asks.