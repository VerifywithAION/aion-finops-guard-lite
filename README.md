# AION FinOps Guard Lite

## What this system is

AION FinOps Guard Lite is a public-safe proof surface for governed financial execution.

Its role is to evaluate financial or cost-bearing actions **before** they are executed.

The domain includes actions such as:

- API spend
- cloud / compute spend
- SaaS or subscription actions
- budget-governed approvals
- agent-triggered paid operations
- controlled treasury-like flows

This repo follows the AION governed-execution primitive:

**intent ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ preview ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ decision ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ consequence ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ receipt ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ execution gate**

In this domain, the primitive becomes:

**financial intent ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ spend preview ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ decision ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ receipt ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ allow / warn / block**

---

## What this repo proves

This repo proves that a financial execution domain can be structured as a governed-execution system by:

- evaluating cost-bearing intent before spend occurs
- previewing likely cost and policy consequence
- deciding whether spend should be allowed, warned, or blocked
- recording the decision in receipts
- demonstrating ordeal cases and mirrored invariants across the domain

---

## What this repo is not

This repo is not:

- a release of private engine source code
- a full enterprise FinOps platform
- a dump of internal policy logic
- a release of sensitive account configs
- a live billing integration dump
- a production treasury orchestration stack

It is a **public-safe proof artifact** for the FinOps branch of AION.

---

## Domain position

This repo should be understood as:

**governed financial execution before spend**

It is not merely about dashboards or after-the-fact analysis.

Its central claim is:

**financial actions should be evaluated before money is committed**

---

## Reading order

1. `docs/public/REPO_GUIDED_TOUR_V1.md`
2. `docs/public/PUBLIC_RELEASE_NOTE_V1.md`
3. `docs/public/HARDENING_NOTE_V1.md`
4. `docs/architecture/SYSTEM_ARCHITECTURE_MAP_V1.md`
5. `docs/architecture/DOMAIN_ADAPTATION_MAP_V1.md`
6. `docs/evidence/domain/DOMAIN_EXECUTION_PROOF_V1.md`
7. `docs/evidence/cross_domain/CROSS_DOMAIN_EXECUTION_PROOF_V1.md`
8. `docs/evidence/mirror_attacks/MIRROR_ATTACKS_EXECUTION_PROOF_V1.md`

---

## Statement

Spend should not be trusted merely because a system can execute it.

Spend should be admitted only when legitimacy is provable.


<!-- AION_COUNTERFACTUAL_PREVIEW_START -->
## Counterfactual preview layer

This repo also tracks an additive counterfactual preview layer.

It is non-breaking and optional.

It strengthens financial execution governance by testing nearby future spend paths around the current request.

See:
- `docs/architecture/COUNTERFACTUAL_PREVIEW_ARCHITECTURE_V1.md`
- `docs/evidence/domain/COUNTERFACTUAL_PREVIEW_EXECUTION_NOTE_V1.md`
<!-- AION_COUNTERFACTUAL_PREVIEW_END -->

<!-- AION_FINOPS_RUNTIME_START -->
## Minimal local runtime

This repo also includes a minimal local runtime wedge.

It evaluates financial actions locally and emits:

- decision
- reasons
- receipt_id
- receipt file
- optional counterfactual summary

Example runner:

`scripts/run_finops_guard_lite_eval.ps1`

Example payloads:

- `examples/example_allow.json`
- `examples/example_warn.json`
- `examples/example_block.json`

Policy:

- `policies/finops_policy_v1.json`

This runtime is intentionally minimal and public-safe.

It exists to demonstrate the execution gate, not to expose private engine logic.
<!-- AION_FINOPS_RUNTIME_END -->

<!-- AION_FINOPS_LOCAL_MODE_START -->
## Ollama / local mode

This repo also includes a local execution-governance mode for Ollama and other local open-source model workflows.

It evaluates local model jobs using:

- estimated local job cost
- GPU / RAM requirements
- scope level
- counterfactual nearby-future risk

See:
- `docs/architecture/OLLAMA_LOCAL_MODE_ARCHITECTURE_V1.md`
- `docs/evidence/domain/OLLAMA_LOCAL_MODE_EXECUTION_PROOF_V1.md`

Runner:
- `scripts/run_finops_guard_lite_local_eval.ps1`
<!-- AION_FINOPS_LOCAL_MODE_END -->

<!-- AION_FINOPS_LOCAL_RUNTIME_PROOF_START -->
## Ollama / local runtime proof

This repo now includes a public-safe runtime evidence document for local open-source model governance.

It records observed local runtime outcomes for:

- ALLOW
- WARN
- BLOCK

with receipts and counterfactual summary.

See:
- `docs/evidence/domain/OLLAMA_LOCAL_RUNTIME_EXECUTION_PROOF_V1.md`
<!-- AION_FINOPS_LOCAL_RUNTIME_PROOF_END -->

<!-- AION_FINOPS_IMPORTED_SNAPSHOT_START -->
## Imported billing snapshot path

This repo now includes a path for evaluating imported external billing or usage snapshots.

It supports:
- manual billing exports
- usage snapshots
- normalized external spend evidence

See:
- `docs/evidence/domain/IMPORTED_BILLING_SNAPSHOT_EXECUTION_PROOF_V1.md`

Runner:
- `scripts/run_finops_imported_snapshot_eval.ps1`
<!-- AION_FINOPS_IMPORTED_SNAPSHOT_END -->
