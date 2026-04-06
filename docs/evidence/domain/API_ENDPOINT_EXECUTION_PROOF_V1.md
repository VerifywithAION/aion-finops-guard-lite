# API Endpoint Execution Proof V1

## Purpose

This document explains the local HTTP endpoint surface for AION FinOps Guard Lite.

The Lite system can now be called like a real product.

---

## Supported request classes

- imported billing / spend snapshots
- local open-source model job requests

---

## Canonical response shape

The API returns:
- decision
- reasons
- receipt identifier
- receipt path
- counterfactual summary
- normalized evaluated view

---

## Why this matters

This is the first true API-connectable surface for FinOps Guard Lite.

It allows upstream systems such as Buzz to call AION through a real endpoint instead of only through scripts.
