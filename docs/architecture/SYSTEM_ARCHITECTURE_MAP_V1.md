# System Architecture Map V1

## Purpose

This document defines the high-level structure of AION FinOps Guard Lite.

---

## Core system role

AION FinOps Guard Lite sits between financial intent and spend execution.

It is a decision layer, not merely an analytics layer.

---

## Canonical flow

1. Intent is presented
2. Cost / consequence preview is formed
3. Policy decision is produced
4. Receipt is emitted
5. Execution is allowed, warned, or blocked

---

## System layers

- intent intake layer
- preview layer
- decision layer
- receipt layer
- execution gate layer

---

## Architectural position

This system is one domain-specific lens of the broader AION governed-execution thesis.
