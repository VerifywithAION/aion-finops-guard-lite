# FinOps Counterfactual Integration Notes V1

Private-ops note only.

## Current posture

Counterfactual preview is an additive layer for FinOps Guard Lite.

It should remain:

- optional
- non-breaking
- contract-preserving
- safe for Week 2 style integration demos

## Public-safe line

The runtime may retain the same core decision / receipt shape while also emitting an optional counterfactual summary.

## Example neighboring futures to test

- amount upshift
- repeat attempt
- scope escalation
- stricter budget profile
- provider drift
- compounding spend path

Do not expose:

- private heuristics
- internal scoring logic
- production-specific policy composition
- sensitive provider configs
