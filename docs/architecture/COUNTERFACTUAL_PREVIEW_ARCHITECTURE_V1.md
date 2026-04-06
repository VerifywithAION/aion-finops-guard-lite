# Counterfactual Preview Architecture V1

## Purpose

This document explains the additive counterfactual layer for AION FinOps Guard Lite.

This layer does not replace the base execution gate.

It enriches preview.

---

## Core principle

A normal FinOps system asks:

- what is the current spend?
- did the budget already move?
- how should we optimize after cost appeared?

AION FinOps Guard Lite asks first:

- should this spend happen at all?

The counterfactual preview layer adds one more question:

- what nearby future spend paths become plausible if this action is allowed?

---

## Additive design rule

The counterfactual layer is:

- optional
- non-breaking
- additive to the current decision path
- suitable for public-safe explanation without exposing internal logic

The core contract remains:

**intent → preview → decision → receipt → execution gate**

The counterfactual layer enriches preview with a bounded neighboring-futures summary.

---

## Example neighboring futures

A spend request may be tested against nearby variations such as:

- amount upshift
- repeat attempt
- scope escalation
- stricter budget profile
- provider drift
- compounding execution path

---

## Example optional output shape

Example:

{
  "decision": "WARN",
  "reason": "within current threshold but fragile under nearby futures",
  "counterfactual_summary": {
    "projected_daily_cost": 450,
    "fragility": "HIGH",
    "dominant_risk": "budget_exceeded_in_6_hours"
  }
}

This does not break the base contract.

It strengthens the gate by showing how fragile the surrounding spend neighborhood is.

---

## Category value

This is one of the main differences between AION FinOps Guard Lite and ordinary cost-control tools.

The system is not only evaluating the current spend surface.

It is previewing the risk of adjacent financial futures before execution.
