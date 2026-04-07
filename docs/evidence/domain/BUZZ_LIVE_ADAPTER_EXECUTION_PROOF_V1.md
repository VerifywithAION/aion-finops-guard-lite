# Buzz Live Adapter Execution Proof V1

## Purpose

This document defines the first live Buzz-to-FinOps adapter path for AION FinOps Guard Lite.

It is based on:
- a real sanitized Buzz payload
- a sync pre-execution call pattern
- advisory mode for the first live test

---

## Canonical flow

Buzz scores token -> Wallet Guard checks safety -> FinOps evaluates economics -> receipt

---

## Current adapter role

The adapter:
- ingests a Buzz payload
- normalizes it into FinOps import format
- preserves Buzz-unique signals in context
- calls the live FinOps import endpoint synchronously
- returns a combined result object

---

## Non-breaking posture

The adapter does not break the FinOps response shape.

It adds:
- `buzz_input`
- `normalized_snapshot`
- `buzz_overlay`
- `finops_response`

The `buzz_overlay` is advisory only for now.

---

## Why this matters

This is the first live bridge between:
- Buzz intelligence
- Wallet Guard safety
- FinOps economic consequence control
