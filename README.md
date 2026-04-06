# AION FinOps Guard Lite

## What this system is

AION FinOps Guard Lite is a public-safe proof surface and API-connectable runtime wedge for governed financial execution.

Its role is to evaluate spend-bearing or cost-bearing actions **before** irreversible financial consequence occurs.

It follows the AION primitive:

**intent â†’ preview â†’ decision â†’ consequence â†’ receipt â†’ execution gate**

In this domain, that becomes:

**financial intent â†’ spend preview â†’ decision â†’ receipt â†’ allow / warn / block**

---

## What this repo proves

This repo proves that a FinOps domain can be turned into a governed-execution system that:

- evaluates spend-bearing actions before execution
- emits deterministic `ALLOW / WARN / BLOCK` outcomes
- records receipts
- exposes counterfactual preview
- works in local open-source mode
- works through imported billing snapshot mode
- supports a Buzz-compatible import path
- can later be connected to external systems via API or ingestion paths

---

## What this repo is not

This repo is not:

- a dump of private engine source
- a full enterprise FinOps platform
- a release of sensitive billing credentials
- a release of proprietary orchestration
- a claim that every live billing connector is already wired

It is the **Lite** public-safe proof and runtime surface.

The **Pro** version is where deeper monetized capabilities live, including stronger enterprise integrations, richer policy composition, and advanced operational depth.

---

## Lite vs Pro

### Lite
- public-safe
- API-connectable wedge
- local runtime modes
- imported external evidence path
- counterfactual preview
- receipt emission
- demo-safe integration surface

### Pro
- deeper enterprise integrations
- richer live connector coverage
- stronger anomaly layers
- more advanced policy and approval composition
- monetized operational depth

---

## Real evidence index

### Main proof layers
- [Domain Execution Proof](docs/evidence/domain/DOMAIN_EXECUTION_PROOF_V1.md)
- [Runtime Execution Proof](docs/evidence/domain/RUNTIME_EXECUTION_PROOF_V1.md)
- [Ollama / Local Runtime Execution Proof](docs/evidence/domain/OLLAMA_LOCAL_RUNTIME_EXECUTION_PROOF_V1.md)
- [Imported Billing Snapshot Execution Proof](docs/evidence/domain/IMPORTED_BILLING_SNAPSHOT_EXECUTION_PROOF_V1.md)
- [Buzz-Compatible Import Execution Proof](docs/evidence/domain/BUZZ_COMPATIBLE_IMPORT_EXECUTION_PROOF_V1.md)

### Public boundary / reading control
- [Public Release Note](docs/public/PUBLIC_RELEASE_NOTE_V1.md)
- [Hardening Note](docs/public/HARDENING_NOTE_V1.md)
- [Repo Guided Tour](docs/public/REPO_GUIDED_TOUR_V1.md)

### Architecture
- [System Architecture Map](docs/architecture/SYSTEM_ARCHITECTURE_MAP_V1.md)
- [Domain Adaptation Map](docs/architecture/DOMAIN_ADAPTATION_MAP_V1.md)

### Cross-domain and invariants
- [Cross-Domain Execution Proof](docs/evidence/cross_domain/CROSS_DOMAIN_EXECUTION_PROOF_V1.md)
- [Mirror Attacks Execution Proof](docs/evidence/mirror_attacks/MIRROR_ATTACKS_EXECUTION_PROOF_V1.md)

---

## API-connectable Lite position

This repo should be read similarly to AION Guard Lite.

The Lite surface is meant to be:
- connectable by API
- connectable by imported snapshots
- connectable by upstream systems like Buzz
- suitable for end-to-end pipeline tests

That means this repo is not only a narrative proof surface.
It is also a practical integration wedge.

---

## Current integration surfaces

### 1. Minimal runtime wedge
- local evaluator
- receipt emission
- counterfactual summary

### 2. Ollama / local open-source mode
- local model execution governance
- GPU / RAM aware
- counterfactual local resource preview

### 3. Imported billing snapshot path
- manual imported financial evidence
- normalized billing snapshot evaluation
- receipt output

### 4. Buzz-compatible import path
- upstream Buzz JSON
- normalized into imported snapshot form
- evaluated through the same FinOps decision engine

---

## Recommended reading order

1. [Repo Guided Tour](docs/public/REPO_GUIDED_TOUR_V1.md)
2. [Public Release Note](docs/public/PUBLIC_RELEASE_NOTE_V1.md)
3. [Hardening Note](docs/public/HARDENING_NOTE_V1.md)
4. [System Architecture Map](docs/architecture/SYSTEM_ARCHITECTURE_MAP_V1.md)
5. [Domain Adaptation Map](docs/architecture/DOMAIN_ADAPTATION_MAP_V1.md)
6. [Domain Execution Proof](docs/evidence/domain/DOMAIN_EXECUTION_PROOF_V1.md)
7. [Runtime Execution Proof](docs/evidence/domain/RUNTIME_EXECUTION_PROOF_V1.md)
8. [Ollama / Local Runtime Execution Proof](docs/evidence/domain/OLLAMA_LOCAL_RUNTIME_EXECUTION_PROOF_V1.md)
9. [Imported Billing Snapshot Execution Proof](docs/evidence/domain/IMPORTED_BILLING_SNAPSHOT_EXECUTION_PROOF_V1.md)
10. [Buzz-Compatible Import Execution Proof](docs/evidence/domain/BUZZ_COMPATIBLE_IMPORT_EXECUTION_PROOF_V1.md)
11. [Cross-Domain Execution Proof](docs/evidence/cross_domain/CROSS_DOMAIN_EXECUTION_PROOF_V1.md)
12. [Mirror Attacks Execution Proof](docs/evidence/mirror_attacks/MIRROR_ATTACKS_EXECUTION_PROOF_V1.md)

---

## Statement

Financial consequence should not be trusted merely because a system can execute it.

It should be admitted only when legitimacy is provable.


<!-- AION_FINOPS_PRO_SKELETON_START -->
## FinOps Guard Pro skeleton

This repo now includes a Pro skeleton doc set that defines the deeper roadmap beyond Lite.

See:
- `docs/pro/FINOPS_GUARD_PRO_OVERVIEW_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_ROADMAP_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_CONNECTOR_LAYER_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_POLICY_ENGINE_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_APPROVAL_AUTHORITY_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_COUNTERFACTUAL_ENGINE_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_OPTIMIZATION_LAYER_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_ANOMALY_DRIFT_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_API_PLATFORM_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_EVIDENCE_FABRIC_V1.md`
- `docs/pro/FINOPS_GUARD_PRO_ENTERPRISE_CONTROL_PLANE_V1.md`
<!-- AION_FINOPS_PRO_SKELETON_END -->
