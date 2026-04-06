# Ollama / Local Runtime Execution Proof V1

## Purpose

This document records the first public-safe local runtime evidence for AION FinOps Guard Lite in Ollama / local mode.

It demonstrates that the repo is not limited to architecture framing.

It now includes a working local execution-governance wedge for open-source model jobs.

---

## Runtime scope

The local runtime evaluates model jobs before execution using:

- estimated local job cost
- estimated GPU requirement
- estimated RAM requirement
- scope level
- counterfactual nearby-future load risk

The runtime emits:

- decision
- reasons
- receipt identifier
- receipt path
- counterfactual summary

---

## Test inputs

Three local example payloads were executed:

1. `examples/example_local_allow.json`
2. `examples/example_local_warn.json`
3. `examples/example_local_block.json`

Policy file used:

- `policies/finops_local_policy_v1.json`

Runner used:

- `scripts/run_finops_guard_lite_local_eval.ps1`

Runtime engine:

- `server/finops_guard_lite_local.py`

---

## Observed outcome 1 — ALLOW

Input class:
- lightweight local inference job

Observed decision:
- `ALLOW`

Observed reason:
- `within_local_policy`

Observed receipt:
- `FINOPS_LOCAL_7833C791DAD5`

Observed receipt path:
- `runtime/receipts/FINOPS_LOCAL_7833C791DAD5.json`

Observed counterfactual summary:
- projected_daily_cost = `4.0`
- upshift_job_cost = `1.6`
- upshift_gpu_gb = `2.25`
- upshift_ram_gb = `4.5`
- fragility = `LOW`
- dominant_risk = `none`

Interpretation:
The local job remained admissible under both current policy and nearby future variants.

---

## Observed outcome 2 — WARN

Input class:
- medium local job with higher resource pressure

Observed decision:
- `WARN`

Observed reason:
- `estimated_job_cost_exceeds_warn_threshold`

Observed receipt:
- `FINOPS_LOCAL_67AD795BBAD7`

Observed receipt path:
- `runtime/receipts/FINOPS_LOCAL_67AD795BBAD7.json`

Observed counterfactual summary:
- projected_daily_cost = `17.5`
- upshift_job_cost = `7.0`
- upshift_gpu_gb = `10.5`
- upshift_ram_gb = `19.5`
- fragility = `MEDIUM`
- dominant_risk = `stricter_profile_reveals_fragility`

Interpretation:
The local job was not fully blocked, but the runtime detected fragility under nearby-future policy pressure.

---

## Observed outcome 3 — BLOCK

Input class:
- heavy blocked model / overscoped local job

Observed decision:
- `BLOCK`

Observed reason:
- `model_blocked_by_policy`

Observed receipt:
- `FINOPS_LOCAL_65A7644D836E`

Observed receipt path:
- `runtime/receipts/FINOPS_LOCAL_65A7644D836E.json`

Observed counterfactual summary:
- projected_daily_cost = `60.0`
- upshift_job_cost = `24.0`
- upshift_gpu_gb = `27.0`
- upshift_ram_gb = `48.0`
- fragility = `HIGH`
- dominant_risk = `job_cost_upshift_breaks_policy`

Interpretation:
The runtime denied execution because the requested model and surrounding resource futures were clearly outside policy.

---

## Why this matters

This local runtime evidence proves that AION FinOps Guard Lite can already govern real open-source model execution without requiring paid vendor integrations first.

It demonstrates:

- local pre-execution governance
- ALLOW / WARN / BLOCK decisions
- receipt emission
- counterfactual preview
- resource-aware local model control

---

## Boundary of this proof

This document does not claim live third-party billing integration.

It claims something narrower and concrete:

AION FinOps Guard Lite now has a real local execution-governance mode for Ollama / open-source workflows with observed runtime outcomes and attached receipts.

---

## Canonical takeaway

FinOps Guard Lite now has real local runtime evidence for:

- admissible local jobs
- fragile local jobs
- blocked local jobs

with receipts and counterfactual preview attached.
