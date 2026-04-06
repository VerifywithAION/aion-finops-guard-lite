# Ollama / Local Mode Architecture V1

## Purpose

This document explains the local execution mode for AION FinOps Guard Lite.

The goal is to govern local model execution without requiring paid API vendors.

---

## Core idea

In local mode, the system does not ask:

- how much did a SaaS vendor charge?

It asks:

- should this local model job execute given projected resource cost and nearby-future load risk?

---

## Governed surfaces

Local mode can govern:

- model selection
- repeated local inference loops
- projected GPU pressure
- projected RAM pressure
- estimated local job cost
- scope escalation of local compute jobs

---

## Why this matters

This allows FinOps Guard Lite to become real immediately and cheaply.

It proves the execution-governance model without requiring live paid integrations first.

---

## Counterfactual role

The local mode also includes counterfactual preview.

It tests nearby futures such as:

- repeated attempts
- job cost upshift
- resource upshift
- stricter profile

This makes the decision layer stronger than static local resource checks.
