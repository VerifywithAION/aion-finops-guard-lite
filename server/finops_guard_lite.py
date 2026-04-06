import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def decide(payload, policy):
    provider = str(payload.get("provider", "")).strip().lower()
    action = str(payload.get("action", "")).strip()
    estimated_cost = float(payload.get("estimated_cost", 0.0))
    scope_level = int(payload.get("scope_level", 1))
    actor = str(payload.get("actor", "unknown"))

    decision = "ALLOW"
    reasons = []

    if provider in [p.lower() for p in policy.get("blocked_providers", [])]:
        decision = "BLOCK"
        reasons.append("provider_blocked_by_policy")

    allowed = [p.lower() for p in policy.get("allowed_providers", [])]
    if provider and allowed and provider not in allowed and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("provider_not_allowlisted")

    if scope_level > int(policy.get("max_scope_level", 3)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("scope_exceeds_authorized_level")

    if estimated_cost > float(policy.get("max_single_action_cost", 100.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("single_action_cost_exceeds_max")

    if estimated_cost > float(policy.get("warn_single_action_cost", 50.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("single_action_cost_exceeds_warn_threshold")

    cf = None
    cf_policy = policy.get("counterfactual", {})
    if cf_policy.get("enabled", True):
        amount_upshift_multiplier = float(cf_policy.get("amount_upshift_multiplier", 2.0))
        repeat_attempts = int(cf_policy.get("repeat_attempts", 5))
        stricter_profile_single_action_cost = float(cf_policy.get("stricter_profile_single_action_cost", 40.0))

        upshift_cost = estimated_cost * amount_upshift_multiplier
        projected_daily_cost = estimated_cost * repeat_attempts

        fragility = "LOW"
        dominant_risk = "none"

        if upshift_cost > float(policy.get("max_single_action_cost", 100.0)):
            fragility = "HIGH"
            dominant_risk = "amount_upshift_breaks_policy"
        elif projected_daily_cost > float(policy.get("max_daily_projected_cost", 300.0)):
            fragility = "HIGH"
            dominant_risk = "repeat_attempts_break_daily_budget"
        elif estimated_cost > stricter_profile_single_action_cost:
            fragility = "MEDIUM"
            dominant_risk = "stricter_profile_reveals_fragility"

        if projected_daily_cost > float(policy.get("warn_daily_projected_cost", 200.0)) and decision == "ALLOW":
            decision = "WARN"
            reasons.append("counterfactual_projected_daily_cost_warns")

        cf = {
            "projected_daily_cost": round(projected_daily_cost, 2),
            "upshift_cost": round(upshift_cost, 2),
            "fragility": fragility,
            "dominant_risk": dominant_risk,
            "tested_variants": [
                "amount_upshift",
                "repeat_attempt",
                "stricter_profile"
            ]
        }

    if not reasons:
        reasons.append("within_policy")

    return {
        "decision": decision,
        "reasons": reasons,
        "counterfactual_summary": cf,
        "normalized": {
            "action": action,
            "provider": provider,
            "estimated_cost": estimated_cost,
            "scope_level": scope_level,
            "actor": actor
        }
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python finops_guard_lite.py <payload.json> <policy.json>")
        sys.exit(2)

    payload_path = Path(sys.argv[1]).resolve()
    policy_path = Path(sys.argv[2]).resolve()

    payload = load_json(payload_path)
    policy = load_json(policy_path)

    result = decide(payload, policy)

    receipt_id = "FINOPS_RUNTIME_" + uuid.uuid4().hex[:12].upper()
    receipt = {
        "receipt_id": receipt_id,
        "timestamp_utc": utc_now(),
        "policy_version": policy.get("version", "unknown"),
        "input_file": str(payload_path),
        "decision": result["decision"],
        "reasons": result["reasons"],
        "counterfactual_summary": result["counterfactual_summary"],
        "normalized": result["normalized"]
    }

    repo_root = Path(__file__).resolve().parent.parent
    runtime_receipts = repo_root / "runtime" / "receipts"
    runtime_receipts.mkdir(parents=True, exist_ok=True)
    receipt_path = runtime_receipts / f"{receipt_id}.json"
    write_json(receipt_path, receipt)

    print(json.dumps({
        "decision": receipt["decision"],
        "reasons": receipt["reasons"],
        "receipt_id": receipt_id,
        "receipt_path": str(receipt_path),
        "counterfactual_summary": receipt["counterfactual_summary"]
    }, indent=2))


if __name__ == "__main__":
    main()