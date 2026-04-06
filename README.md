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

**intent → preview → decision → consequence → receipt → execution gate**

In this domain, the primitive becomes:

**financial intent → spend preview → decision → receipt → allow / warn / block**

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
