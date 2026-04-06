# Ollama / Local Mode Execution Proof V1

## Purpose

This document explains the proof meaning of the local execution mode.

---

## Safe case

A lightweight local inference job remains within allowed cost and resource thresholds.

Decision:
ALLOW

---

## Fragile case

A medium local job is still admissible but reveals resource or cost fragility under nearby futures.

Decision:
WARN

---

## Dangerous case

A heavy model or overscoped local job exceeds policy.

Decision:
BLOCK

---

## Core takeaway

AION FinOps Guard Lite can already govern real local execution before a paid-vendor integration exists.

That makes the system usable immediately while preserving the same governed-execution thesis.
