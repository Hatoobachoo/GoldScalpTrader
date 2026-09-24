# GoldScalpTrader — Shared Glossary

**Status:** DRAFT PRE-CHALLENGE REFERENCE
**Version:** 0.2-full-manual-terms
**Authority:** Plain-language vocabulary shared by the canonical `Documents/` manual.

## 1. How to use this file

Words that sound similar can carry different safety meaning. Topic contracts add detail but must not silently redefine canonical terms. Hard-authority meaning wins over informal dashboard wording.

## 2. Product and architecture terms

| Term | Canonical meaning |
|---|---|
| Documents manual | The only active canonical documentation set used to design, challenge, build and verify GoldScalpTrader. |
| Trading Floor | Specialist analytical desks produce bounded evidence independently while financial/broker authority remains ordered. |
| MarketSnapshot | One immutable normalized account/symbol/quote/completed-candle/exposure view for a governed cycle. |
| IntelligenceSnapshot | Shared typed causal market evidence derived from MarketSnapshot. |
| Desk | A bounded component owning one analytical question and explicit authority limit. |
| Strategy Family | Independent attributable market hypothesis; may propose directional evidence but cannot size/send orders. |
| BUY Team / SELL Team | Independent directional thesis builders; opposition remains visible. |
| Red Team / Debate | Analytical challenge of the leading thesis; never broker authority. |
| Floor Manager | Analytical fusion owner producing an auditable directional DecisionBoard. |
| Opportunity | Durable identity for a qualified thesis that may persist while waiting for executable timing. |
| Entry Timing | Current readiness of an existing Opportunity; separate from thesis validity. |
| TradePlan | Structural geometry: approved entry reference, invalidation/SL, objective hierarchy and original R before monetary sizing. |
| RiskEvaluation | Independent monetary/broker-valid affordability result for an already-defined TradePlan. |
| Hard authority | Required safety/financial/broker/lifecycle truth that can PASS, BLOCK or remain UNKNOWN; not a weighted score. |
| ExecutionPermissionGate | Central ordered composition of required authorities for one broker action. |
| ExecutionIntent | Durable unique one-shot identity persisted before irreversible broker submission. |
| MT5Writer | Sole raw MetaTrader5 irreversible write boundary. |
| Reconciliation | Verification of attempted broker action against current broker truth; uncertainty is resolved here rather than blind resend. |
| ManagedTrade | Durable bot-owned post-entry lifecycle identity. |
| Trade Manager | Post-entry owner of HOLD/PROTECT/TRAIL/RUNNER/EXIT semantics. |
| Verified close | Closure whose exact known-trade broker lineage/outcome is proven strongly enough for accounting/learning. |
| StrategyMemory | Durable downstream memory derived from verified causal evidence. |
| Research lab | Offline evidence environment that may replay/compare/discover/propose but has no broker authority. |
| Governed promotion | Evidence-bound champion/challenger process required before research changes production policy. |

## 3. Scalping terms

| Term | Canonical meaning |
|---|---|
| Scalp | Selective short-duration Gold trade with fresh thesis, executable geometry and cost-aware room. |
| Broad regime | Higher-level directional/volatility environment used as context; final timeframe role pending challenge. |
| Scalp Opportunity | Fresh short-horizon thesis/location worth tracking before trigger. |
| Trigger | Causal fresh event used by Entry Timing to classify executability. |
| Event / trigger age | Elapsed time/bars since evidence became knowable. |
| Distance since trigger | Price travel since the relevant causal event; used for chase/freshness context. |
| Late entry | Current executable price has moved enough that original scalp quality/room no longer holds. |
| Re-arm | New timing opportunity after a genuinely new causal event; never simple reset of terminal old identity. |
| Cost-dominated setup | Structural/target room is too small relative to spread/slippage/fees under the owning policy. |
| Executable geometry | Geometry checked using current action-side quote semantics and broker constraints. |
| Microstructure | M1/tick/short-horizon behaviour used only within explicitly approved role. |
| Time / efficiency exit | Scalp management concept that exits a thesis failing to progress within documented expectations. |
| Accidental swing conversion | Letting a failed scalp remain open beyond its intended thesis/horizon without governed reason. |

## 4. Price identities

| Term | Canonical meaning |
|---|---|
| Signal Price | Price where analytical evidence formed. |
| Approved Entry Reference | Price reference used to build TradePlan geometry. |
| Executable Quote | Fresh Bid/Ask available immediately before submit. |
| Actual Fill | Broker-confirmed executed entry price. |
| Price drift | Adverse/favorable movement between approved reference and fresh executable quote/fill. |

These identities must not be collapsed, especially for scalping.

## 5. Truth / chronology terms

| Term | Canonical meaning |
|---|---|
| Knowledge time | Earliest time a fact could causally be known by the system. |
| Completed candle | Candle whose close is known/immutable for bar-based analysis. |
| Forming candle | Current incomplete bar; not completed structural proof. |
| Causal lineage | Proven chain from raw facts to derived evidence without future leakage. |
| Fresh | Inside validity/freshness contract owned by relevant component. |
| Aging | Still relevant context but approaching the owning entry-validity boundary. |
| Stale for entry | Fact remains historically true but no longer supports a new scalp entry without fresh evidence. |
| UNKNOWN | Required truth cannot currently be proved; never equivalent to PASS/CLEAR/zero. |
| Degraded | Reduced evidence/health; permission effect belongs to owning contract. |
| CORRUPT | Data/state violates integrity/chronology/domain expectations and cannot be trusted. |

## 6. Risk/execution terms

| Term | Canonical meaning |
|---|---|
| Structural stop | Thesis invalidation price; never moved merely to make risk affordable. |
| Original R | Initial structural risk distance/value preserved for later evaluation. |
| Monetary risk | Account-currency exposure implied by executable entry, stop, volume and broker contract values/friction. |
| Minimum-lot affordability | Whether broker minimum executable volume fits final Risk policy for actual structural stop. |
| Account Safety P/L | Account-level safety metric separated from identifiable non-trading cash flow and bot-only attribution. |
| Bot Performance P/L | P/L attributed only to bot-owned trade lineage. |
| One-shot submission | One Intent ID has at most one irreversible send allowance. |
| Accepted unknown | Broker request may have been accepted but software lacks final certainty; blind resend forbidden. |
| Controller fencing | Prevents multiple runtime writers from controlling one account/symbol scope simultaneously. |
| Capacity | Whether initial V1's one independent Gold risk position is already occupied. |
| Risk Standby | No current TradePlan/Risk proposal exists; not a risk failure. |

## 7. Permission/operator terms

| Term | Canonical meaning |
|---|---|
| Current Blocker | Owning stage that currently prevents progress. May be analytical, TradePlan, Risk, Gate, Intent/reconciliation or system. |
| Gate NOT EVALUATED | Candidate stopped upstream before central ExecutionPermissionGate ran. |
| Gate BLOCKED | Central Gate actually evaluated and returned BLOCK. |
| ENTRY_BLOCKED | Broad runtime/operator result; never sufficient by itself to infer Gate BLOCK. |
| Soft Session | Analytical ASIA/LONDON/NEW_YORK/OVERLAP context. |
| Hard Market State | Broker schedule permission state such as OPEN/PRE_CLOSE/CLOSED/REOPEN_WARMUP/UNKNOWN. |
| News UNKNOWN | News/provider safety truth cannot be established; never renamed CLEAR. Final permission effect belongs to frozen policy. |

## 8. Runtime modes

| Term | Canonical meaning |
|---|---|
| READINESS | Read-only diagnostic/identity/data/recovery observation mode. |
| DRY_RUN | Full safe analytical/risk/permission path without irreversible broker writer calls. |
| PRIMARY | One active governed production/DEMO writer for one account/symbol scope when that milestone is implemented. |
| STANDBY | Same-scope cross-machine role intentionally unsupported in initial local-state V1. |
| REAL | Real-money broker-write authority; not implicit V1 capability and requires separate explicit governance. |

## 9. Backup / recovery terms

| Term | Canonical meaning |
|---|---|
| Local working clone | Project working directory plus local `.git` source history. |
| Runtime checkpoint | Consistent verified snapshot/export of durable runtime/research state. |
| Rolling runtime backup | Periodically retained local verified checkpoints for crash/device recovery. |
| Final shutdown checkpoint | Fresh verified local checkpoint created after broker/controller authority is safely released on graceful shutdown. |
| Local Git bundle | Portable local repository history/refs file created deliberately at source milestones, not every bot shutdown. |
| Recovery package | Controlled local package containing approved full runtime checkpoint/manifest/environment/source identity; secrets excluded. |
| Backup manifest | Metadata/hashes identifying scope, revision, schema/policy, creation time and contents. |
| Restore | Verification and reconstruction into new local state; restored context has no broker authority until reconciliation. |
| Sequential handoff | Move one account/symbol scope between machines without simultaneous production writers. |
| Same-scope split brain | Two independent active writers/state histories for same account/symbol; prohibited in V1. |

## 10. Learning / research terms

| Term | Canonical meaning |
|---|---|
| Actual observation | Evidence from positively verified managed broker trade lifecycle. |
| Counterfactual | What later market path suggests about MISSED/BLOCKED setup; never actual P/L. |
| ResearchEpisodeRecord | Durable labelled research episode preserving source/provenance/outcome class. |
| StrategyCandidate | Declarative bounded proposed change with evidence/fingerprint; no broker authority. |
| Champion | Currently approved production policy. |
| Challenger | Candidate compared against Champion through governed evidence. |
| Semantic lock | Candidate meaning frozen before final holdout; later change creates new version. |
| Final holdout | Untouched dataset/evidence consumed once by locked candidate. |
| Shadow | Forward hypothetical evaluation with zero broker authority. |
| DEMO Canary | Governed candidate evaluated through normal DEMO safety gates. |

## 11. Evidence/status terms

| Term | Canonical meaning |
|---|---|
| DRAFT PRE-CHALLENGE | Proposed contract before fresh-zero review; not frozen. |
| FROZEN | Approved current contract; change requires governed synchronization. |
| IMPLEMENTED | Corresponding source behaviour exists; does not itself imply verified. |
| NOT RUN | Audit/procedure has not yet been executed. |
| CALIBRATION PENDING | Architecture fixed/accepted while numerical value needs evidence. |
| EXTERNAL PROOF PENDING | Software contract exists but real terminal/broker/machine proof remains. |
| Deterministic proof | Test evidence for specific software behaviour, not profitability/live validity. |
| Replay evidence | Chronological historical simulation with declared data/assumptions. |
| Connected proof | Evidence from actual target terminal/broker environment. |
| Local recovery proof | Verified checkpoint/package restore plus required reconciliation on exact environment. |
| Affected graph | Full set of docs/source/tests/operator/research/release surfaces made stale by one material change. |

## 12. Reference/preservation terms

| Term | Canonical meaning |
|---|---|
| GoldSwingTraderAI reference | User-authored architecture/governance source used to preserve useful design meaning; not current scalp authority. |
| Preservation | Retain useful rationale/constraints while adapting or superseding scalp-specific trading semantics explicitly. |
| Fresh-zero challenge | Audit that asks what would be kept/changed/removed/added if GoldScalpTrader were designed today from zero. |
| Reference threshold | Numerical/behavioural value from Swing project; enters scalp project only as DRAFT/CALIBRATE/EXTERNAL/REJECTED until approved. |
