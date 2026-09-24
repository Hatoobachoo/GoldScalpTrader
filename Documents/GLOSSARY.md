# GoldScalpTrader — Shared Glossary

**Status:** FROZEN V1 REFERENCE — PRESERVATION-FIRST CORRECTION APPLIED
**Version:** 1.2-profiled-risk-preserved-features
**Authority:** Plain-language vocabulary shared by the canonical `Documents/` manual.

## 1. Core architecture

| Term | Canonical meaning |
|---|---|
| Documents manual | Sole active canonical documentation set used to design, build and verify GoldScalpTrader. |
| Preservation-first rule | GoldSwingTraderAI feature/default stays unless a direct scalp requirement, explicit operator instruction or proven reference defect justifies changing it. |
| Trading Floor | Specialist analytical desks/families produce attributable evidence independently; bounded-parallel execution is preserved while financial/broker authority remains serial. |
| MarketSnapshot | One immutable normalized account/symbol/quote/completed-candle/exposure view for one governed cycle. |
| Strategy Family | One independent attributable market hypothesis; no Risk/write authority. |
| BUY / SELL Team | Independent directional thesis builders; opposition remains visible. |
| Red Team | Analytical challenge of leading thesis; never hard broker authority. |
| Opportunity | Durable identity for a qualified thesis that may persist while waiting for timing. |
| Entry Timing | Completed-M5 executable readiness of an existing Opportunity. |
| TradePlan | Structural entry/invalidation/objective geometry plus gross and cost-adjusted room before monetary sizing. |
| RiskEvaluation | Independent broker-aware monetary affordability result using the active account profile/overlay. |
| ExecutionPermissionGate | Central ordered composition of required hard authorities for one action. |
| ExecutionIntent | Durable unique one-shot action identity persisted before irreversible submission. |
| MT5Writer | Sole raw MetaTrader5 irreversible write boundary. |
| Reconciliation | Verify attempted broker action against broker truth instead of guessing/retrying. |
| ManagedTrade | Durable bot-owned post-entry lifecycle identity. |
| Trade Manager | Post-entry owner of HOLD/PROTECT/TRAIL/RUNNER/EXIT. |

## 2. Timeframe vocabulary

| Term | Canonical meaning |
|---|---|
| H1 regime | Broad soft directional/volatility context; not universal veto. |
| M15 opportunity context | Location/path/liquidity/session context for a scalp thesis. |
| M5 production timeframe | Primary completed-bar setup, entry timing and normal management structure. |
| H4 context | Optional major context only. |
| M1 context | Diagnostic/research only; no independent production trigger authority. |
| Quote/current tick | Executable Bid/Ask/spread/drift/freshness condition, not structural-history proof. |

## 3. Scalping / chronology

| Term | Canonical meaning |
|---|---|
| Scalp | Selective short-duration Gold trade with fresh thesis, executable geometry and cost-aware room. |
| Knowledge time | Earliest time a fact could causally be known. |
| Completed candle | Closed bar used for bar-based production authority. |
| Causal lineage | Proven path from raw facts to evidence without future leakage. |
| Event/trigger age | Time/bars since evidence became knowable. |
| Stale for entry | Historically true fact that no longer supports a new entry without fresh evidence. |
| Late entry | Current executable price has moved enough that original scalp efficiency/room no longer holds. |
| Re-arm | New timing opportunity after a genuinely fresh causal event; never next-poll reset. |
| Accidental swing conversion | Failed scalp held beyond intended thesis/horizon without governed reason. |
| Time/efficiency EXIT | Normal `EXIT` reason caused by calibrated failure to progress; not a separate action enum. |

## 4. Price / cost identities

| Term | Canonical meaning |
|---|---|
| Signal Price | Price where evidence formed. |
| Approved Entry Reference | Price reference used by TradePlan. |
| Executable Quote | Fresh action-side Bid/Ask immediately before submit. |
| Actual Fill | Broker-confirmed executed entry price. |
| Gross structural room | Reward/path quality before current transaction-cost burden. |
| Cost-adjusted room | Remaining executable opportunity after current known spread/friction context without inventing future fill/slippage. |
| Cost-dominated setup | Structural room is insufficient relative to transaction costs under owning policy. |
| Price drift | Movement between Approved Entry Reference and current executable quote/fill. |

## 5. Risk vocabulary

| Term | Canonical meaning |
|---|---|
| DayStartEquity profile | Account Risk profile resolved at UTC risk-day boundary and fixed for that risk day. |
| SMALL | Positive DayStartEquity below $300. Normal target 3.0–4.5%, elevated >4.5–6.5%, hard ceiling 7%, daily lock 12%. |
| MEDIUM | DayStartEquity $300–$999.99. Normal target 2.0–3.0%, elevated >3.0–4.5%, hard ceiling 5%, daily lock 9%. |
| NORMAL | DayStartEquity >= $1,000. Normal target 1.0–2.0%, elevated >2.0–3.5%, hard ceiling 4%, daily lock 7%. |
| AGGRESSIVE_SMALL_ACCOUNT | Explicit optional policy overlay for eligible sub-$1,000 operation; disabled by default and never auto-enabled merely from balance. |
| 8% aggressive ceiling | Maximum monetary SL risk for one new trade when aggressive mode is explicitly enabled; **not a sizing target**. |
| 16% aggregate ceiling | Maximum aggregate open risk under explicitly enabled aggressive mode. |
| 16% aggressive daily ceiling | Daily loss ceiling under explicitly enabled aggressive mode. |
| Minimum-lot affordability | Whether broker minimum executable volume fits the active hard policy for the actual structural stop. |
| Structural stop | Thesis invalidation price; never altered merely to make volume affordable. |
| Original R | Initial structural risk preserved for later evaluation. |
| Manual daily-loss reset | Preserved governed reset capability; disabled by default and unable to clear unrelated hard faults. |
| Same-episode re-entry | At most the preserved reference allowance of one genuinely fresh re-entry under current baseline policy. |
| Global loss cooldown | Reference baseline: three consecutive closed bot losses trigger at least 30 minutes plus required fresh/healthy release conditions. |

## 6. News / provider vocabulary

| Term | Canonical meaning |
|---|---|
| News CLEAR | Accepted current event-safety truth with no configured blackout/warmup. Source may be fresh provider/file or valid LKG cache. |
| News BLACKOUT | Positively known configured high-impact event window; hard new-entry block. |
| News UNKNOWN / NEWS_SAFETY_UNKNOWN | Current News safety cannot be proved because no accepted current source/cache exists; new scalp entry blocks while management remains action-sensitive. |
| Provider Health | Acquisition-source condition such as VERIFIED, DEGRADED, STALE, UNAVAILABLE or UNKNOWN; not identical to News truth. |
| Last-known-good (LKG) cache | Previously accepted normalized calendar reused only while original scope/schema/coverage/TTL/integrity remain valid. |
| Provider TTL baseline | 1800 seconds retained from reference unless a later direct provider/scalp reason supersedes it. |
| Cache timestamp laundering | Prohibited rewriting of old fetch/as-of/valid-until values so stale data appears fresh. |

## 7. Session baseline vocabulary

| Term | Canonical meaning |
|---|---|
| Daily PRE_CLOSE baseline | T-20 no new entry, T-10 mandatory flatten while broker remains tradeable. |
| Weekend PRE_CLOSE baseline | T-60 no new entry, T-30 mandatory flatten. |
| Daily reopen baseline | One clean completed M5 after verified reopen plus healthy execution/recovery state. |
| Weekend reopen baseline | Two clean completed M5 plus weekend-gap assessment and healthy execution/recovery state. |

Current broker schedule/DST/holiday facts still require external verification.

## 8. Execution / ownership

| Term | Canonical meaning |
|---|---|
| One-shot submission | One Intent ID has at most one irreversible send allowance. |
| Accepted unknown | Broker effect may exist but final certainty is missing; blind resend forbidden. |
| Controller fencing | Prevents stale/multiple runtime writers for one account/symbol scope. |
| Capacity | Initial V1 one independently risk-bearing Gold position per scope. |
| External/manual exposure | Broker Gold exposure not proven bot-owned; never silently adopted. |
| Verified close | Exact known-trade broker lineage/outcome proven sufficiently for accounting/learning. |
| Partial management | Preserved optional broker-valid partial action where volume is divisible; minimum-lot correctness never depends on it. |

## 9. Runtime modes / capability stages

| Term | Canonical meaning |
|---|---|
| READINESS | Read-only diagnostic/identity/data/recovery mode. |
| DRY_RUN | Governed analytical/risk/permission path with zero irreversible broker writes. |
| PRIMARY / DEMO | One active governed DEMO writer per account/symbol scope after its implementation/evidence gate. |
| REAL capability | Preserved future governed feature; disabled/unavailable until DEMO proof, release gates and explicit operator approval satisfy its own policy. |
| STANDBY / same-scope distributed writer | Not part of current local-state writer design without a separate shared-fencing architecture. |

## 10. Parallel / serial vocabulary

| Term | Canonical meaning |
|---|---|
| Bounded analytical concurrency | Preserved capability for dependency-independent desks/families using immutable inputs and bounded workers. |
| One-worker fallback | Deterministic fallback required to be semantically equivalent to bounded-parallel analysis. |
| Serial financial authority | TradePlan → Risk → hard permissions → Gate → Intent → writer → reconciliation; never competing broker writers. |

## 11. Backup / recovery

| Term | Canonical meaning |
|---|---|
| Local working clone | Project directory plus local `.git`; source/history backup after `git pull --ff-only`. |
| Runtime checkpoint | Consistent verified snapshot/export of durable runtime/research state. |
| Final shutdown checkpoint | Fresh verified local runtime checkpoint after safe shutdown; no Git operation. |
| Source ZIP | Optional secret-clean Windows-friendly milestone snapshot. |
| Git bundle | Optional advanced/manual source-history archive. |
| Recovery package | Controlled runtime package containing approved checkpoint/manifest/identity; secrets excluded. |

## 12. Learning / evidence

Learning/research stays downstream and cannot create broker authority. Strategy candidates cannot self-promote. Actual, counterfactual and system-fault evidence remain separate.

Evidence terms:

```text
FROZEN
PRESERVED REFERENCE DEFAULT
SCALP CALIBRATION PENDING
IMPLEMENTED
DETERMINISTIC PROOF
REPLAY EVIDENCE
CONNECTED DEMO PROOF
FUTURE REAL RELEASE PROOF
EXTERNAL PROOF PENDING
```

GoldSwingTraderAI remains the default preservation/reference baseline. Exact current differences are owned by `90-governance/DOCUMENTATION_COMPARISON.md`.