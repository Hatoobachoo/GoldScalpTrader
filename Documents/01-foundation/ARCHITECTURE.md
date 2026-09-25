# GoldScalpTrader — Runtime Architecture

**Status:** APPROVED TARGET ARCHITECTURE — DOCUMENTATION RECONSTRUCTION / IMPLEMENTATION PROOF PENDING
**Version:** 2.0-hybrid-fast-accurate-scalp
**Authority:** Whole-system topology, dependency DAG, performance model, strategy isolation, ordered financial authority, runtime/recovery boundaries and presentation/research separation.

Canonical recovery architecture: [`BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md`](../BACKUP_SYNC_AND_RECOVERY_ARCHITECTURE.md).

## 1. Purpose

This document explains how GoldScalpTrader fits together as one runtime. Detailed topic contracts own their local rules; this architecture owns:

- dependency order;
- reusable shared facts;
- what may run independently;
- where physical parallelism is useful;
- where execution must remain serial;
- active-family versus shadow-family behavior;
- M5→M1 entry sequence;
- executable-quality revalidation;
- startup/recovery/liveness;
- trade management and verified-close flow;
- learning/research background work;
- source/runtime backup boundaries;
- presentation isolation.

## 2. Architectural objective

GoldScalpTrader must be both **fast and accurate**.

The system therefore does not choose between “serial” and “parallel” globally. It uses a **hybrid dependency DAG**:

- parallelize only dependency-independent analytical work when profiling proves useful;
- share/calculate reusable facts once;
- preserve deterministic result ordering;
- keep money, lifecycle and broker authority strictly ordered;
- measure latency rather than assume concurrency is faster.

## 3. Whole-system topology

```mermaid
flowchart TB
    MT5["MT5 account/symbol/quote/candles/positions/deals"] --> READ["One normalized read boundary"]
    READ --> SNAP["Immutable MarketSnapshot"]

    SNAP --> H1["H1 regime/context"]
    SNAP --> M15["M15 location/path"]
    SNAP --> M5["M5 structure/setup facts"]
    SNAP --> IND["EMA / RSI / ATR / volatility"]
    SNAP --> LIQ["Liquidity / SMC / zones / confluence"]
    SNAP --> SESS["Session + Fundamental/News context"]

    H1 --> MERGE["Deterministic IntelligenceSnapshot"]
    M15 --> MERGE
    M5 --> MERGE
    IND --> MERGE
    LIQ --> MERGE
    SESS --> MERGE

    MERGE --> F1["Trend Pullback"]
    MERGE --> F2["Breakout Expansion"]
    MERGE --> F3["Breakout Retest"]
    MERGE --> F4["Liquidity Sweep Reversal"]
    MERGE --> F5["Failed Breakout Reversal"]
    MERGE --> F6["Compression Expansion"]

    F1 --> ISO["Strategy Isolation Controller"]
    F2 --> ISO
    F3 --> ISO
    F4 --> ISO
    F5 --> ISO
    F6 --> ISO

    ISO --> ACTIVE["Exactly 1 ACTIVE_EXECUTION family"]
    ISO --> SHADOW["5 SHADOW_ONLY families"]
    ACTIVE --> DEBATE["BUY/SELL thesis + Red Team"]
    SHADOW --> RESEARCH["Shadow attribution / challenge / research"]

    DEBATE --> OPP["Persistent M5 Opportunity"]
    OPP --> M1R["Subordinate M1 refinement"]
    M1R --> PLAN["Structural TradePlan"]
    PLAN --> QUAL["Executable Quality Engine"]
    QUAL --> RISK["Monetary Risk"]
    RISK --> HARD["Broker/account/session/exposure/controller authority"]
    HARD --> GATE["ExecutionPermissionGate"]
    GATE --> INTENT["Durable one-shot Intent"]
    INTENT --> CHECK["Fresh broker/order prechecks"]
    CHECK --> WRITE["Sole MT5Writer"]
    WRITE --> RECON["Broker reconciliation"]
    RECON --> TRADE["ManagedTrade"]
    TRADE --> TM["HOLD / PROTECT / TRAIL / RUNNER / EXIT"]
    TM --> RECON
    TM --> CLOSE["Verified close"]
    CLOSE --> LEARN["Actual learning"]
    RESEARCH --> RD["Discovery / invention / ML"]
    LEARN --> RD
    RD --> PROMO["Evidence stages → APPROVAL_REQUIRED"]
```

## 4. Data ownership and read boundaries

### 4.1 One analytical MT5 boundary

`market_data/mt5_reader.py` (planned owner) is the normal source for:

- account/server identity;
- symbol specification;
- bid/ask/current tick;
- completed H1/M15/M5 and optional H4/M1 history;
- positions/orders/deals as required;
- terminal/account/symbol trade permissions.

### 4.2 Immutable MarketSnapshot

Analytical workers consume the same normalized snapshot. This prevents:

- different desks seeing different candle cutoffs;
- repeated MT5 latency;
- hidden read-side race conditions;
- one strategy using information unavailable to another in the same cycle.

### 4.3 Legitimate fresh reads

The architecture permits fresh broker reads when **current** truth is required:

- final executable quote;
- spread/drift revalidation;
- margin/order-check;
- reconciliation;
- recovery;
- active-position management.

These fresh reads do not rewrite the causal historical snapshot.

## 5. Timeframe topology

```mermaid
flowchart LR
    H1["H1: broad regime"] --> M15["M15: location/path"]
    M15 --> M5["M5: primary setup/thesis"]
    M5 --> OPP["Opportunity"]
    OPP --> M1["M1: subordinate entry refinement"]
    M1 --> Q["Fresh Bid/Ask"]
    H4["H4 optional major context"] -. soft .-> H1
```

M1 cannot independently create a production trade. It may improve timing only after a valid active-family M5 Opportunity exists.

## 6. Analytical dependency DAG

### Stage A — reusable primitives

Potentially independent work from immutable inputs:

- H1/M15/M5 candle/structure primitives;
- EMA/RSI/ATR/volatility calculations;
- session clock/context;
- optional News/Fundamental acquisition/context;
- M1 microstructure snapshot for already-armed opportunities.

### Stage B — dependent specialist intelligence

Consumes Stage A:

- technical zones/location;
- liquidity/sweeps/reclaims/FVG/OB;
- trendline/Fibonacci;
- volume/POC context;
- target-room/path analysis.

### Stage C — family evaluation

All six family analyzers may evaluate independently from one `IntelligenceSnapshot`.

### Stage D — isolation + ordered decision

The versioned strategy-isolation policy identifies exactly one trade-producing family. Shadow families remain non-authoritative for production entry.

## 7. Physical parallelism policy

Physical concurrency is not a correctness requirement.

Optimization order:

```text
1. avoid duplicate calculations
2. use efficient vectorized operations
3. cache immutable reusable values
4. profile end-to-end latency
5. parallelize only measured bottlenecks
6. re-test semantic parity
```

```mermaid
flowchart TB
    PROFILE["Profile latency"] --> BOT{"Bottleneck independent?"}
    BOT -->|No| SERIAL["Keep serial / optimize algorithm"]
    BOT -->|Yes| PAR["Bounded worker execution"]
    PAR --> PARITY["1-worker vs parallel semantic parity"]
    PARITY -->|Fail| REJECT["Reject optimization"]
    PARITY -->|Pass| KEEP["Keep measured improvement"]
```

Constraints:

- immutable worker inputs;
- bounded worker count;
- deterministic canonical result order;
- exceptions/degradation visible;
- no worker-side broker writes;
- no worker-side lifecycle mutation;
- no different answer merely because scheduling changed.

## 8. Strategy Isolation Controller

The isolation controller is an analytical/governance component, not a broker writer.

Stored policy identity includes at least:

- `active_family`;
- policy/version ID;
- activation time/effective evaluation window;
- reason/approval lineage;
- optional benchmark/research episode ID.

```mermaid
stateDiagram-v2
    [*] --> ACTIVE_A
    ACTIVE_A --> REVIEW: evaluation period/evidence review
    REVIEW --> ACTIVE_A: continue current family
    REVIEW --> APPROVAL_REQUIRED: propose active-family switch
    APPROVAL_REQUIRED --> ACTIVE_B: operator approves
    APPROVAL_REQUIRED --> ACTIVE_A: reject / defer
```

A family switch must not rewrite old trade attribution.

## 9. Entry branch

```text
fresh immutable MarketSnapshot
→ IntelligenceSnapshot
→ all six family analyses
→ active-family BUY/SELL + Red Team
→ persistent M5 Opportunity
→ subordinate M1 refinement
→ TradePlan
→ fresh executable quote
→ fixed + aware spread/cost/drift/latency quality
→ monetary Risk
→ objective hard authorities
→ central Gate
→ durable Intent
→ fresh broker/order checks
→ sole writer
→ reconciliation
→ ManagedTrade only after verified OPEN
```

### 9.1 Why M1 is subordinate

M1 is valuable because waiting for another completed M5 bar can make a scalp late. But M1 noise is dangerous if allowed to invent standalone theses. The architecture therefore uses M1 for **precision**, not **permission to invent opportunity**.

## 10. Executable Quality Engine

This layer answers:

> “The structural trade idea is valid; is it still economically executable now?”

Inputs include:

- Approved Entry Reference;
- current Bid/Ask;
- absolute spread;
- spread/SL ratio;
- spread/target ratio;
- recent healthy spread baseline;
- estimated slippage allowance;
- cost/reward ratio;
- decision age / decision→send latency;
- price drift/chase;
- M1 trigger freshness;
- remaining target room.

Output is typed, reason-rich and separate from monetary Risk.

Excess latency/drift generally triggers revalidation. It becomes terminal only when the underlying Opportunity/geometry is no longer efficient or valid.

## 11. News/Fundamental lane

```mermaid
flowchart LR
    NEWS["Economic calendar / macro context"] --> CTX["Soft context"]
    CTX --> DASH["Dashboard"]
    CTX --> TAG["Trade/event tags"]
    CTX --> RSRCH["Research segmentation"]
    NEWS -. "NO direct hard gate" .-> GATE["Execution Gate"]
```

Provider failure affects News-context health, not broker permission. Real event-induced bad conditions are caught through measurable price/execution facts.

## 12. Session lane

Session has two meanings:

1. **analytical session context** — Asia/London/NY/overlap performance, soft;
2. **broker market/session safety** — OPEN/CLOSED/PRE_CLOSE/reopen conditions, hard.

These must not be conflated.

## 13. Risk/execution serial authority

From structural plan onward, ordering is explicit:

```mermaid
sequenceDiagram
    participant P as TradePlan
    participant Q as ExecutableQuality
    participant R as Risk
    participant H as HardAuthorities
    participant G as Gate
    participant I as IntentStore
    participant B as BrokerChecks
    participant W as MT5Writer
    participant X as Reconciler

    P->>Q: structural plan
    Q->>R: executable plan/context
    R->>H: approved monetary proposal
    H->>G: typed authority results
    G->>I: ALLOW → persist Intent
    I->>B: fresh quote/margin/order_check
    B->>I: persist SUBMITTING
    I->>W: exactly one request
    W->>X: acknowledgement/result
    X->>X: verify broker truth
```

No physical parallelism is allowed to reorder this sequence.

## 14. Startup and recovery topology

```mermaid
flowchart TB
    CFG["Validate settings/policy"] --> MT5["Initialize MT5 read boundary"]
    MT5 --> FACTS["Account/symbol/quote/history/exposure"]
    FACTS --> STATE["Open/verify StateStore"]
    STATE --> RISK["Restore/reconcile Risk day/cash flow/cooldown"]
    RISK --> ISO["Restore active strategy policy"]
    ISO --> CTRL["Acquire controller for write-capable runtime"]
    CTRL --> REC["Reconcile Intent + ManagedTrade + broker close truth"]
    REC --> READY{"Ready?"}
    READY -->|Recoverable wait| WAIT["Dashboard + bounded re-probe"]
    READY -->|Unsafe/corrupt| BLOCK["Fail closed"]
    READY -->|Yes| LOOP["Runtime loop"]
    WAIT --> FACTS
```

Restored state is context. MT5 is current exposure authority.

## 15. Runtime liveness matrix

| Condition | Process | Analysis | New entry | Management | Dashboard |
|---|---|---|---|---|---|
| healthy/open | alive | active+shadow | governed | governed | full |
| News provider unavailable | alive | yes, News context degraded | **not blocked by News alone** | governed | show degraded |
| stale required market data | alive/wait | paused/limited | blocked by data owner | safe management as possible | exact reason |
| broker CLOSED | alive | research/context may continue | blocked | governed close/none as broker permits | full |
| PRE_CLOSE | alive | entry disabled | blocked | required flatten policy | full |
| unresolved Intent | alive/reconciling | optional read-only | blocked | reconciliation first | exact lifecycle |
| persistence corruption | fail/recover | paused | blocked | recovery-safe only | fault |
| active trade exists | alive | shadow research may continue | capacity governed | managed | full |

## 16. ManagedTrade branch

```text
fresh position/broker truth
→ restore/verify ManagedTrade identity
→ current structure + executable facts
→ HOLD / PROTECT / TRAIL / RUNNER / EXIT
→ any MODIFY/CLOSE becomes a governed Intent
→ sole writer
→ broker verification
→ update local lifecycle only after verification
```

Time-efficiency is first-class for scalping: an unproductive trade may EXIT rather than silently become a swing. Exact timing is calibrated.

## 17. Broker-side/manual close recovery

```mermaid
sequenceDiagram
    participant R as Recovery
    participant I as IntentStore
    participant B as Broker deals
    participant M as ManagedTrade
    participant L as LearningQueue

    R->>I: unresolved submit/ambiguous intent?
    alt yes
        I-->>R: reconcile first
    else no
        R->>B: exact known position-ticket exit lineage
        B-->>R: roles/volume/deals
        alt incomplete/ambiguous
            R->>M: keep RECONCILING
        else exact full close
            R->>L: persist verified-close evidence
            R->>M: persist closure receipt / clear active trade
        end
    end
```

Unknown external positions are never adopted.

## 18. Learning/research architecture

Background learning/research may run independently of broker authority and may use compute parallelism appropriate to the workload.

Research lanes include:

- actual active-family trades;
- shadow-family counterfactuals;
- missed opportunities;
- blocked opportunities with exact blocker;
- invalidated setups;
- system-fault episodes;
- session/event tags;
- cost/latency/entry/exit efficiency;
- candidate invention/tuning/ML.

Production promotion remains approval-gated.

## 19. Dashboard architecture

Terminal dashboard is the primary operational view. Optional graphical dashboard is secondary/read-only.

Presentation consumes immutable/atomic DTOs and cannot:

- recalculate Risk;
- change active strategy;
- grant Gate permission;
- call MT5 writer;
- promote research candidates.

Dashboard updates may run at a faster read-only pulse than the strategy decision cycle.

## 20. Backup/recovery architecture

Runtime GitHub activity is zero.

Source/history:

```text
coherent development packet
→ Git commit/remote
→ operator git pull --ff-only
→ local full-history clone
→ optional clean ZIP/Drive recovery package
```

Runtime:

```text
transactional StateStore
→ rolling checkpoints
→ shutdown checkpoint
→ optional portable runtime/learning package
```

See the canonical backup document for cross-machine and off-site details.

## 21. Performance budgets and telemetry

Performance must be measured by stage, not guessed.

Planned telemetry categories:

| Stage | Example metrics |
|---|---|
| MT5 read | snapshot acquisition ms |
| intelligence | per-desk ms, total critical path |
| families | per-family ms, active-family ms |
| fusion/Opportunity | decision ms |
| M1 refinement | trigger age / evaluation ms |
| TradePlan/quality/Risk | evaluation ms |
| final revalidation | quote age/drift ms |
| writer | request latency |
| reconciliation | broker-confirmation latency |
| dashboard | render ms, isolated from strategy latency |
| research | asynchronous/offline throughput |

Concurrency is accepted only if it improves measured critical-path latency without semantic drift.

## 22. Current deferred architecture

Explicitly deferred:

- same-account active-active multi-machine broker writers;
- distributed DB/shared consensus/fencing infrastructure;
- sophisticated partial-close optimization as a release dependency;
- paid News API requirement;
- GitHub Actions/cloud compute dependency.

These are deferred, not accidentally omitted.

## 23. Final architecture invariant

> **Parallelize facts and hypotheses only where it makes the measured critical path faster; serialize money and broker authority; let exactly one strategy family produce live trades at a time for clean efficiency attribution; use M1 to sharpen a valid M5 opportunity rather than invent one; and let real executable market facts—not News labels—decide whether a scalp remains economically tradeable.**
