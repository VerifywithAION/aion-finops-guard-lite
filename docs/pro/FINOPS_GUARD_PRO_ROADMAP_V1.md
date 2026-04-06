# FinOps Guard Pro Roadmap V1

## Purpose

This document gives the skeleton roadmap for the Pro version.

---

## Phase 1 — live connector layer

Add real ingestion for:
- OpenAI usage and cost
- Anthropic usage and cost
- AWS billing
- Azure billing
- GCP billing
- SaaS billing
- internal spend systems
- procurement and approval exports

Outcome:
live spend data replaces manual import.

---

## Phase 2 — policy composition engine

Add:
- hierarchical policy composition
- project/team/org policy inheritance
- role-aware budget rules
- service-specific policies
- time-aware policies
- override workflows
- policy version registry

Outcome:
governance becomes a versioned runtime layer.

---

## Phase 3 — approval and authority chain

Add:
- approver identity chain
- delegated authority
- stale approval invalidation
- revoked approver handling
- scope-bounded approvals
- approval receipt linkage

Outcome:
authority becomes admissible, not assumed.

---

## Phase 4 — deep counterfactual engine

Add:
- repeated-path forecasts
- provider drift scenarios
- route alternative comparisons
- budget exhaustion horizon
- scale-to-team/project/org projections
- fragility scoring
- dominance reasoning

Outcome:
counterfactual becomes a real decision advantage.

---

## Phase 5 — optimization layer

Add:
- cheapest admissible route
- safest admissible route
- cost/performance balancing
- model tier recommendation
- batch vs realtime recommendation
- caching and reuse recommendations
- workflow alternative selection

Outcome:
the system becomes not only a blocker, but a navigator.

---

## Phase 6 — anomaly and drift layer

Add:
- spend stream anomaly detection
- baseline drift
- workload shift detection
- policy evasion signals
- runaway loop detection
- vendor behavior anomalies

Outcome:
the system becomes live-operational, not just point-in-time evaluative.

---

## Phase 7 — API and integration platform

Add:
- authenticated API
- multi-tenant surface
- webhooks
- callbacks
- queue ingestion
- streaming evaluation
- connector registry
- SDKs

Outcome:
the platform becomes embeddable infrastructure.

---

## Phase 8 — evidence fabric and control plane

Add:
- receipt registry
- decision explorer
- replay surface
- audit views
- policy diff views
- org/team/project hierarchy
- staged enforcement modes
- shadow / warn-only / block modes

Outcome:
the system becomes enterprise-usable and operationally governable.
