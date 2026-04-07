# Buzz Edge WARN Execution Proof V1

## Purpose

This document defines the first edge-case Buzz WARN-path test for AION FinOps Guard Lite.

It complements the clean ALLOW-path test by using:
- WARM classification
- non-empty security flags
- non-clean shield scan
- non-zero estimated cost

---

## Canonical test purpose

The purpose of this edge case is to validate that the Buzz-to-FinOps bridge can surface a more fragile posture before live integration.

---

## Expected behavior

This test should be suitable for demonstrating:

- advisory-only hybrid posture
- lower-confidence Buzz signal
- more fragile surrounding execution neighborhood
- a plausible `WARN` path for Thursday demo preparation

---

## Why it matters

A clean ALLOW case alone is not enough.

A serious live test should show:
- one clean pass
- one fragile case

That proves the stack is not just permissive.
