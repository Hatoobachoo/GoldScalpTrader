# GoldScalpTrader — Shared Glossary

**Status:** DRAFT PRE-CHALLENGE REFERENCE
**Version:** 0.1-foundation-terms
**Authority:** Plain-language vocabulary shared by the canonical `Documents/` manual.

## 1. How to use this file

Words that sound similar can carry different safety meaning. Topic contracts may add detail but must not silently redefine canonical terms. Hard-authority meaning wins over informal dashboard wording.

## 2. Product and architecture terms

| Term | Canonical meaning |
|---|---|
| Documents manual | The only active canonical documentation set used to design, build and verify GoldScalpTrader. |
| Trading Floor | Architecture where specialist analytical desks produce bounded evidence independently while broker authority remains ordered. |
| MarketSnapshot | One immutable normalized account/symbol/quote/candle/exposure view for a decision cycle. |
| IntelligenceSnapshot | Shared typed analytical evidence derived causally from MarketSnapshot. |
| Desk | A bounded analytical component that owns one question and cannot exceed its declared authority. |
| Strategy Family | An independent, attributable market hypothesis that may propose BUY/SELL/neutral analytical evidence but cannot size/send orders. |
| BUY Team / SELL Team | Independent directional thesis builders; opposition stays visible rather than being hidden by one net score. |
| Red Team / Debate | Analytical challenge of the leading thesis; never broker authority. |
| Floor Manager | Analytical fusion owner publishing an auditable directional DecisionBoard. |
| Opportunity | Durable identity for a qualified thesis that may persist while waiting for executable timing. |
| Entry Timing | Current-entry readiness of an existing Opportunity; separate from whether the opportunity thesis is valid. |
| Trade Plan | Structural/executable geometry: entry reference, invalidation, SL, target hierarchy and original R before monetary sizing. |
| RiskEvaluation | Independent monetary/broker-valid affordability result for an already-defined Trade Plan. |
| Hard authority | Required safety/financial/broker/lifecycle truth that can PASS, BLOCK or remain UNKNOWN; it is not a weighted score. |
| ExecutionPermissionGate | Central ordered composition of all required authorities for a specific broker action. |
| ExecutionIntent | Durable unique one-shot identity persisted before an irreversible broker request. |
| MT5Writer | Sole raw MetaTrader5 write boundary. |
| Reconciliation | Verification of attempted broker actions against current broker truth; uncertainty is resolved here rather than by blind resend. |
| ManagedTrade | Durable bot-owned post-entry lifecycle identity. |
| Trade Manager | Post-entry decision component for HOLD/PROTECT/TRAIL/RUNNER/EXIT semantics where retained. |
| Verified close | Closure whose bot ownership and broker outcome are proven strongly enough for accounting/learning. |
| StrategyMemory | Durable downstream learning memory derived from verified causal evidence. |
| Research lab | Offline evidence environment that may replay, compare, discover and propose but has no broker authority. |
| Governed promotion | Evidence-bound champion/challenger process required before research changes production policy. |

## 3. Scalping terms

| Term | Canonical meaning |
|---|---|
| Scalp | Selective short-duration Gold trade with explicit fresh thesis, executable geometry and cost-aware target room. |
| Broad regime | Higher-level directional/volatility environment used as context; exact timeframe pending challenge. |
| Scalp opportunity | Fresh short-horizon thesis and location worth stalking before a trigger exists. |
| Trigger | Causal fresh event used by Entry Timing to classify current executability. |
| Trigger age | Time/bars/ticks since the trigger became knowable; exact units/thresholds belong to timing contracts. |
| Late entry | Current executable price has moved sufficiently beyond approved reference/room that original scalp quality is no longer valid. |
| Re-arm | Creation or activation of a new timing opportunity after a genuinely new qualifying causal event; never simple reset of a terminal old thesis. |
| Cost-dominated setup | Expected structural/target room is insufficient after spread/slippage/executable-price considerations. |
| Executable geometry | Entry/SL/TP distances evaluated using the actual action-side price semantics (e.g. Ask for BUY entry, Bid for SELL entry) and broker rules. |
| Microstructure | Short-horizon/tick/M1 behaviour used only within explicitly approved roles; it is not automatic authority. |
| Time stop | Scalp-specific exit concept where a position that fails to progress within a documented horizon may be exited even without touching structural SL. |

## 4. Truth/chronology terms

| Term | Canonical meaning |
|---|---|
| Knowledge time | Earliest time a fact could causally be known by the system. |
| Completed candle | Candle whose close is known and immutable for bar-based analysis. |
| Forming candle | Current incomplete bar; must be separately typed if used. |
| Causal lineage | Proven chain from raw facts to derived evidence without future leakage. |
| Fresh | Within the validity/freshness contract owned by the relevant component. |
| Stale | Outside a declared validity/freshness boundary. |
| UNKNOWN | Required truth cannot currently be proved; never equivalent to PASS/CLEAR/zero. |
| Degraded | Component has reduced evidence/health but may not necessarily remove all system liveness; exact permission effect belongs to its authority contract. |

## 5. Risk/execution terms

| Term | Canonical meaning |
|---|---|
| Structural stop | Price invalidation derived from trade thesis/geometry; not moved merely to make risk affordable. |
| Original R | Initial structural risk distance/value preserved for later evaluation even if management changes the stop. |
| Monetary risk | Account-currency exposure implied by executable entry, stop, volume and broker contract values. |
| Minimum-lot affordability | Whether broker minimum volume fits the risk policy for the actual structural stop. |
| Daily safety P/L | Account-level safety metric separated from non-trading cash flow and bot-only performance attribution. |
| One-shot submission | An Intent is sent once unless reconciliation proves a specifically documented safe retry path. |
| Accepted unknown | Broker request may have been accepted but current software lacks final certainty; blind resend is forbidden. |
| Controller fencing | Rule preventing multiple runtime writers from simultaneously controlling one account/symbol scope. |

## 6. Backup/recovery terms

| Term | Canonical meaning |
|---|---|
| Local working clone | Normal project working directory plus local `.git` history. |
| Runtime backup | Consistent local copy of durable runtime/research state for recovery. |
| Local Git bundle | Portable local file containing repository Git history/refs, created without network publication. |
| Recovery package | Controlled local package combining approved source/history and runtime-state artifacts plus a manifest; secrets excluded automatically. |
| Backup manifest | Metadata/fingerprints identifying revision, schema/policy, timestamp and included files. |
| Restore | Creating/validating recoverable state from a backup; restored state remains context until reconciled against broker truth. |
| Sequential handoff | Moving one account/symbol scope between machines without simultaneous production writers. |

## 7. Evidence/status terms

| Term | Canonical meaning |
|---|---|
| DRAFT PRE-CHALLENGE | Proposed contract written before fresh-zero challenge; not yet frozen. |
| FROZEN | Approved current contract; changes require governed synchronization. |
| CALIBRATION PENDING | Architecture fixed, numerical threshold needs evidence. |
| EXTERNAL PROOF PENDING | Software contract exists but real terminal/broker/machine evidence is still required. |
| Deterministic proof | Test evidence for specific software behaviour, not profitability or live-market validity. |
| Replay evidence | Chronological historical simulation evidence with declared dataset/assumptions. |
| Connected proof | Evidence collected from an actual target terminal/broker environment. |
| Affected graph | Full set of documents/source/tests/operator/research/release surfaces made stale by one material change. |
