# Imported Billing Snapshot Execution Proof V1

## Purpose

This document explains the first external-evidence path for AION FinOps Guard Lite.

The system can ingest an imported billing or usage snapshot, normalize it, evaluate it, emit a receipt, and attach counterfactual preview.

---

## Why this matters

This is the bridge between:

- local-only proof
and
- real external financial evidence

It allows the system to evaluate real exported billing data before a fully automated live connector exists.

---

## Supported posture

This path is designed for:

- manual billing exports
- manual usage snapshots
- CSV-to-JSON converted reports
- copied external provider usage snapshots
- imported cloud or SaaS billing evidence

---

## Canonical flow

1. Real billing or usage data is exported from an external provider
2. The export is converted into normalized JSON
3. AION evaluates the imported snapshot
4. A receipt is emitted
5. Counterfactual preview estimates nearby future risk

---

## Initial imported snapshot example

This repo includes a sample imported snapshot file:

- `runtime/imports/sample_billing_snapshot_realpath_v1.json`

This is the structure to replace later with real imported billing evidence from a provider you actually use.

---

## Canonical takeaway

AION FinOps Guard Lite can now evaluate imported external billing evidence, not just synthetic local actions.

This is the first honest step toward real cloud, SaaS, and vendor spend governance.
