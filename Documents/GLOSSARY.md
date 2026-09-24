# GoldScalpTrader — Shared Glossary

**Status:** FROZEN V1 REFERENCE — CALIBRATION / EXTERNAL PROOF TERMS REMAIN CLASSIFIED
**Version:** 1.1-cache-aware-terms
**Authority:** Plain-language vocabulary shared by the canonical `Documents/` manual.

## 1. Core architecture

| Term | Canonical meaning |
|---|---|
| Documents manual | Sole active canonical documentation set used to design, build and verify GoldScalpTrader. |
| Trading Floor | Specialist analytical desks/families produce attributable evidence independently while financial/broker authority remains serial. |
| MarketSnapshot | One immutable normalized account/symbol/quote/completed-candle/exposure view for one governed cycle. |
| IntelligenceSnapshot | Shared typed causal market evidence derived from MarketSnapshot. |
| Strategy Family | One independent attributable market hypothesis; no Risk/write authority. |
| BUY / SELL Team | Independent directional thesis builders; opposition remains visible. |
| Red Team | Analytical challenge of leading thesis; never hard broker authority. |
| Floor Manager | Fusion owner producing auditable Directional/Opportunity output. |
| Opportunity | Durable identity for a qualified thesis that may persist while waiting for timing. |
| Entry Timing | Completed-M5 executable readiness of an existing Opportunity. |
| TradePlan | Structural entry/invalidation/objective geometry plus gross and cost-adjusted room before monetary sizing. |
| RiskEvaluation | Independent broker-aware monetary affordability result for an already-defined TradePlan. |
| ExecutionPermissionGate | Central ordered composition of required hard authorities for one action. |
| ExecutionIntent | Durable unique one-shot action identity persisted before irreversible submission. |
| MT5Writer | Sole raw MetaTrader5 irreversible write boundary. |
| Reconciliation | Verify attempted broker action against broker truth instead of guessing/retrying. |
| ManagedTrade | Durable bot-owned post-entry lifecycle identity. |
| Trade Manager | Post-entry owner of HOLD/PROTECT/TRAIL/RUNNER/EXIT. |

## 2. Frozen timeframe vocabulary

| Term | Canonical meaning |
|---|---|
| H1 regime | Broad soft directional/volatility context; not universal veto. |
| M15 opportunity context | Location/path/liquidity/session context for a scalp thesis. |
| M5 production timeframe | Primary completed-bar setup, entry timing and normal management structure. |
| H4 context | Optional major context only. |
| M1 context | Diagnostic/research only in V1; no independent production trigger authority. |
| Quote/current tick | Executable Bid/Ask/spread/drift/freshness condition, not structural-history proof. |

## 3. Scalping / chronology

| Term | Canonical meaning |
|---|---|
| Scalp | Selective short-duration Gold trade with fresh thesis, executable geometry and cost-aware room. |
| Knowledge time | Earliest time a fact could causally be known. |
| Completed candle | Closed bar used for bar-based production authority. |
| Forming candle | Incomplete bar; not completed structural proof. |
| Causal lineage | Proven path from raw facts to evidence without future leakage. |
| Event/trigger age | Time/bars since evidence became knowable. |
| Stale for entry | Fact remains historically true but no longer supports new entry without fresh evidence. |
| Late entry | Current executable price has moved enough that original scalp efficiency/room no longer holds. |
| Re-arm | New timing opportunity after a genuinely fresh causal event; never next-poll reset. |
| Accidental swing conversion | Failed scalp held beyond intended thesis/horizon without governed reason. |
| Time/efficiency EXIT | Normal `EXIT` reason caused by calibrated failure to progress; not a separate V1 action enum. |

## 4. Price / cost identities

| Term | Canonical meaning |
|---|---|
| Signal Price | Price where evidence formed. |
| Approved Entry Reference | Price reference used by TradePlan. |
| Executable Quote | Fresh action-side Bid/Ask immediately before submit. |
| Actual Fill | Broker-confirmed executed entry price. |
| Gross structural room | Reward/path quality before current transaction-cost burden. |
| Cost-adjusted room | Remaining executable opportunity after current known spread/friction context, without inventing future fill/slippage. |
| Cost-dominated setup | Structural room is insufficient relative to transaction costs under owning policy. |
| Price drift | Movement between Approved Entry Reference and current executable quote/fill. |

## 5. News / provider vocabulary

| Term | Canonical meaning |
|---|---|
| News CLEAR | Accepted current event-safety truth with no configured blackout/warmup. Source may be fresh provider/file or still-valid LKG cache. |
| News BLACKOUT | Positively known configured high-impact event window; hard new-entry block. |
| News UNKNOWN / NEWS_SAFETY_UNKNOWN | Current News safety cannot be proved because no accepted fresh source or valid LKG cache exists; V1 blocks new entry while management remains action-sensitive. |
| Provider Health | Condition of the acquisition source such as VERIFIED, DEGRADED, STALE, UNAVAILABLE or UNKNOWN; not identical to News truth. |
| Last-known-good (LKG) News cache | Previously accepted normalized calendar reused only while original scope/schema/coverage/TTL/integrity remain valid. |
| Cache timestamp laundering | Prohibited act of rewriting old fetch/as-of/valid-until values so stale cached News appears fresh. |
| Provider DEGRADED + valid cache | Latest refresh may have failed, but accepted cached event truth is still within its original validity; does not itself mean News UNKNOWN. |
| Cache expiry | Original TTL/coverage boundary has passed; cache becomes stale context only and cannot support News CLEAR. |

## 6. Risk / permission

| Term | Canonical meaning |
|---|---|
| STANDARD risk policy | Sole V1 production monetary-risk policy; no automatic balance-tier selection. |
| Preferred risk target | Calibrated desired per-trade monetary risk inside STANDARD. |
| Hard risk ceiling | Maximum allowed actual normalized-volume risk under STANDARD. |
| Minimum-lot affordability | Whether broker minimum executable volume fits hard policy for actual structural stop. |
| Structural stop | Thesis invalidation price; never altered merely to make volume affordable. |
| Original R | Initial structural risk preserved for later evaluation. |
| UNKNOWN | Required truth cannot be proved; never equivalent to PASS/CLEAR/zero. |
| Current Blocker | Actual owning stage currently preventing progress. |
| Gate NOT EVALUATED | Candidate stopped upstream before central Gate ran. |
| Gate BLOCKED | Central Gate actually evaluated and returned BLOCK. |

## 7. Execution / ownership

| Term | Canonical meaning |
|---|---|
| One-shot submission | One Intent ID has at most one irreversible send allowance. |
| Accepted unknown | Broker effect may exist but final certainty is missing; blind resend forbidden. |
| Controller fencing | Prevents stale/multiple runtime writers for one account/symbol scope. |
| Capacity | V1 one independently risk-bearing Gold position per scope. |
| External/manual exposure | Broker Gold exposure not proven bot-owned; never silently adopted. |
| Verified close | Exact known-trade broker lineage/outcome proven sufficiently for accounting/learning. |

## 8. Runtime modes

| Term | Canonical meaning |
|---|---|
| READINESS | Read-only diagnostic/identity/data/recovery mode. |
| DRY_RUN | Governed analytical/risk/permission path with zero irreversible broker writes. |
| PRIMARY | One active governed DEMO writer per account/symbol scope after that milestone is implemented. |
| REAL | Deferred V1; requires separate future governance. |
| STANDBY | Same-scope cross-machine role intentionally unsupported in local-state V1. |

## 9. Backup / recovery

| Term | Canonical meaning |
|---|---|
| Local working clone | Project directory plus local `.git`; primary source/history backup after `git pull --ff-only`. |
| Runtime checkpoint | Consistent verified snapshot/export of durable runtime/research state. |
| Final shutdown checkpoint | Fresh verified **local** runtime checkpoint after safe shutdown; no Git operation. |
| Source ZIP | Optional secret-clean Windows-friendly milestone snapshot; normally excludes runtime state and `.git`. |
| Git bundle | Optional advanced/manual source-history archive; not normal runtime/development requirement. |
| Recovery package | Controlled runtime package containing approved checkpoint/manifest/identity; secrets excluded. |
| Sequential handoff | Move one account/symbol scope between machines without simultaneous writers. |
| Same-scope split brain | Two independent active writers/state histories for same scope; prohibited in V1. |

## 10. Learning / research

| Term | Canonical meaning |
|---|---|
| StrategyMemory | Durable downstream memory from verified causal evidence. |
| Actual observation | Evidence from positively verified managed broker trade lifecycle. |
| Counterfactual | Later path after MISSED/BLOCKED setup; never actual P/L. |
| StrategyCandidate | Declarative proposed change with evidence/fingerprint; no broker authority. |
| Semantic lock | Candidate meaning frozen before final holdout. |
| Final holdout | Untouched evidence consumed once by locked candidate. |
| Shadow | Forward hypothetical evaluation with zero broker authority. |
| DEMO Canary | Governed candidate evaluated through normal DEMO safety gates. |

## 11. Evidence/status

| Term | Canonical meaning |
|---|---|
| FROZEN | Approved current architecture/contract; governed sync required to change. |
| IMPLEMENTED | Source behaviour exists; does not itself mean verified. |
| CALIBRATION PENDING | Architecture fixed while numeric value requires evidence. |
| EXTERNAL PROOF PENDING | Real broker/machine/provider proof remains. |
| Deterministic proof | Software-contract test evidence, not profitability/live proof. |
| Replay evidence | Chronological historical simulation with declared assumptions/costs. |
| Connected proof | Evidence from actual target terminal/broker environment. |
| Affected graph | Full docs/source/tests/operator/research/release surface made stale by a material change. |
| Fresh-zero challenge | Audit asking what would be kept/changed/removed/added if designed today from zero. |

GoldSwingTraderAI remains preservation/reference material; current GoldScalpTrader topic contracts and active Design Decisions are authority. Explicit reference differences are recorded in `90-governance/DOCUMENTATION_COMPARISON.md`.