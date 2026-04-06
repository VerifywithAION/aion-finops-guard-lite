# API Surface Map V1

## Purpose

This document defines the local HTTP API surface for AION FinOps Guard Lite.

---

## Endpoints

### GET /health
Returns service availability.

### POST /v1/finops/evaluate/import
Accepts imported billing / spend snapshot JSON and returns:
- decision
- reasons
- receipt_id
- receipt_path
- counterfactual_summary
- normalized

### POST /v1/finops/evaluate/local
Accepts local model job JSON and returns:
- decision
- reasons
- receipt_id
- receipt_path
- counterfactual_summary
- normalized

---

## Why it matters

This turns FinOps Guard Lite from a script-only proof surface into a real local integration wedge other systems can call.
