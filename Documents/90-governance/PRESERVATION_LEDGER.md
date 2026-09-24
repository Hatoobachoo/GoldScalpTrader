# GoldScalpTrader — Documentation Preservation Ledger

**Status:** POST-AUDIT-1 PRESERVATION LEDGER — ACTIVE
**Version:** 1.0-explicit-preservation
**Authority:** Proof that useful GoldSwingTraderAI design meaning is preserved, adapted, recalibrated or explicitly excluded in GoldScalpTrader canonical `Documents/`.

## 1. Purpose

GoldScalpTrader intentionally reuses the engineering/governance spine of GoldSwingTraderAI while changing trading horizon and several policies for scalping.

Preservation means:

```text
preserve useful rationale / safety / authority boundaries
adapt timeframe/geometry/risk/news/management semantics for scalping
explicitly remove undesired reference behaviour
record every material reference delta durably
```

It does not mean copying every threshold, runtime feature or historical result.

## 2. Preserved reference meaning

| Reference subject | GoldScalpTrader destination | Current verdict |
|---|---|---|
| product governance / non-goals | `00-foundation/*` | preserved, scalp personality substituted |
| one MT5 read boundary | `ARCHITECTURE.md`, `MARKET_DATA_AND_HISTORY.md` | KEEP |
| immutable shared snapshot | architecture/data docs | KEEP |
| causal completed-candle chronology | Candle/Structure + research docs | KEEP |
| staged specialist intelligence | Trading Floor / Intelligence docs | KEEP |
| BUY/SELL independent theses + Red Team | Strategy/Fusion docs | KEEP |
| persistent Opportunity vs timing | `ENTRY_TIMING.md` | KEEP + stronger freshness |
| structural TradePlan before Risk | `TRADE_PLAN.md`, `RISK_CONTRACT.md` | KEEP |
| one-shot Intent / sole writer / reconcile | execution docs | KEEP |
| controller/single-writer safety | execution/recovery docs | KEEP |
| ManagedTrade / verified close | Trade Manager / persistence | KEEP |
| learning/research isolation | `40-research-learning/*` | KEEP |
| read-only dashboards | `50-operator/*` | KEEP |
| documentation/code/test governance | `60-*`, `90-*` | KEEP |

## 3. Preserved only as mechanism, not as numbers

The following reference mechanisms remain while exact values are reopened:

- event/news blackout + post-event warmup;
- PRE_CLOSE no-entry then flatten sequence;
- reopen warmup/clean-bar concept;
- cooldown and same-episode re-entry controls;
- gross structural quality thresholding;
- spread/drift/execution-friction checks;
- provider/cache TTL;
- Risk preferred/hard-ceiling/daily-loss values.

Exact values remain calibration/external proof, not inherited truth.

## 4. Explicit reference policy changes

See `DOCUMENTATION_COMPARISON.md` for the full detailed table. Major accepted changes include:

- H1 broad / M15 opportunity / M5 setup-timing-management; H4 optional;
- M1 stays diagnostic/research-only after explicit challenge;
- six strategy families retained but correlation/event-lineage bounding strengthened;
- Swing 1.20R floor removed as inherited scalp policy;
- automatic SMALL/MEDIUM/NORMAL risk tiers removed in favor of one STANDARD policy;
- Swing risk percentages are not active scalp production values;
- `OPEN + News UNKNOWN → PASS` changed to conservative new-entry block;
- temporary News provider failure may reuse still-valid last-known-good cache;
- expired/invalid/no cache → News UNKNOWN → new-entry block;
- Runner becomes exceptional;
- time/efficiency becomes first-class EXIT evidence;
- physical concurrency becomes optional/profiling-driven;
- READINESS/DRY_RUN → controlled DEMO, REAL deferred V1;
- runtime Git publication removed;
- local pull/ZIP development-backup workflow added.

## 5. Explicitly removed reference behaviour

### Trading-runtime Git publication

GoldSwingTraderAI runtime repository publication is not part of GoldScalpTrader.

GoldScalpTrader runtime durability is:

```text
transactional local StateStore
→ rolling verified local checkpoints
→ final graceful-shutdown local checkpoint
→ optional portable runtime recovery package
```

Development source durability is separate:

```text
major coherent remote commit
→ user git pull --ff-only
→ local clone with full Git history
→ optional secret-clean ZIP milestone copy
```

No trading-runtime GitHub credentials or automatic push/pull.

## 6. New / stronger scalp surfaces

GoldScalpTrader explicitly elevates:

- event/trigger age and distance travelled;
- target-room transaction-cost context;
- Signal Price / Entry Reference / Executable Quote / Fill separation;
- spread/slippage/drift/processing latency;
- short-horizon hold/time efficiency;
- accidental swing-conversion prevention;
- min-lot affordability frequency;
- cost-aware replay/stress;
- News provider last-known-good cache integrity;
- local source/runtime recovery separation.

## 7. Historical audit evidence boundary

GoldSwingTraderAI audit findings remain valuable lessons—especially stale event reuse, live geometry, blocker-vs-Gate truth, reconciliation and documentation sync—but they do not count as GoldScalpTrader PASS evidence.

GoldScalpTrader Audit 1 is its own fresh-zero architecture review. Later Audits 2–7 require Scalp source/runtime evidence when their stage is reached.

## 8. Preservation completion state

Fresh-Zero Audit 1 has challenged the major inherited architecture. The remaining pre-implementation work is documentation metadata/cross-link normalization and implementation-choice/calibration/external-proof classification, not another blind reference copy.

Any future change that materially diverges from the reference or from this ledger must update:

```text
owning topic contract
DESIGN_DECISIONS
OPEN_QUESTIONS where applicable
DOCUMENTATION_COMPARISON
this PRESERVATION_LEDGER
operator/engineering consequences
```