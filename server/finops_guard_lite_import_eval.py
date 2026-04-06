import json
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


def evaluate(snapshot, policy):
    items = snapshot.get("items", [])
    blocked_services = [str(x).strip().lower() for x in policy.get("blocked_services", [])]

    total_cost = 0.0
    max_item_cost = 0.0
    offending_services = []

    for item in items:
        amt = float(item.get("amount", 0.0))
        svc = str(item.get("service", "")).strip().lower()
        total_cost += amt
        if amt > max_item_cost:
            max_item_cost = amt
        if svc in blocked_services:
            offending_services.append(svc)

    decision = "ALLOW"
    reasons = []

    if offending_services:
        decision = "BLOCK"
        reasons.append("blocked_service_present")

    if max_item_cost > float(policy.get("max_single_item_cost", 100.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("single_item_cost_exceeds_max")

    if total_cost > float(policy.get("max_total_snapshot_cost", 150.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("total_snapshot_cost_exceeds_max")

    if max_item_cost > float(policy.get("warn_single_item_cost", 50.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("single_item_cost_exceeds_warn")

    if total_cost > float(policy.get("warn_total_snapshot_cost", 100.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("total_snapshot_cost_exceeds_warn")

    cf = None
    cf_policy = policy.get("counterfactual", {})
    if cf_policy.get("enabled", True):
        repeat_periods = int(cf_policy.get("repeat_periods", 3))
        upshift_multiplier = float(cf_policy.get("upshift_multiplier", 1.5))

        projected_repeated_total = total_cost * repeat_periods
        projected_upshift_total = total_cost * upshift_multiplier

        fragility = "LOW"
        dominant_risk = "none"

        if projected_upshift_total > float(policy.get("max_total_snapshot_cost", 150.0)):
            fragility = "HIGH"
            dominant_risk = "upshifted_snapshot_breaks_policy"
        elif projected_repeated_total > float(policy.get("max_total_snapshot_cost", 150.0)):
            fragility = "HIGH"
            dominant_risk = "repeated_periods_break_policy"
        elif projected_upshift_total > float(policy.get("warn_total_snapshot_cost", 100.0)):
            fragility = "MEDIUM"
            dominant_risk = "upshifted_snapshot_warns"

        if projected_repeated_total > float(policy.get("warn_total_snapshot_cost", 100.0)) and decision == "ALLOW":
            decision = "WARN"
            reasons.append("counterfactual_repeated_periods_warn")

        cf = {
            "projected_repeated_total": round(projected_repeated_total, 2),
            "projected_upshift_total": round(projected_upshift_total, 2),
            "fragility": fragility,
            "dominant_risk": dominant_risk,
            "tested_variants": [
                "repeated_periods",
                "cost_upshift"
            ]
        }

    if not reasons:
        reasons.append("snapshot_within_policy")

    return {
        "decision": decision,
        "reasons": reasons,
        "counterfactual_summary": cf,
        "normalized": {
            "provider": snapshot.get("provider", ""),
            "source_type": snapshot.get("source_type", ""),
            "currency": snapshot.get("currency", "USD"),
            "account_ref": snapshot.get("account_ref", ""),
            "total_cost": round(total_cost, 2),
            "max_item_cost": round(max_item_cost, 2),
            "item_count": len(items)
        }
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python finops_guard_lite_import_eval.py <snapshot.json> <policy.json>")
        sys.exit(2)

    snapshot_path = Path(sys.argv[1]).resolve()
    policy_path = Path(sys.argv[2]).resolve()

    snapshot = load_json(snapshot_path)
    policy = load_json(policy_path)

    result = evaluate(snapshot, policy)

    receipt_id = "FINOPS_IMPORT_" + uuid.uuid4().hex[:12].upper()
    receipt = {
        "receipt_id": receipt_id,
        "timestamp_utc": utc_now(),
        "policy_version": policy.get("version", "unknown"),
        "mode": policy.get("mode", "unknown"),
        "input_file": str(snapshot_path),
        "decision": result["decision"],
        "reasons": result["reasons"],
        "counterfactual_summary": result["counterfactual_summary"],
        "normalized": result["normalized"]
    }

    repo_root = Path(__file__).resolve().parent.parent
    receipt_path = repo_root / "runtime" / "receipts" / f"{receipt_id}.json"
    write_json(receipt_path, receipt)

    print(json.dumps({
        "decision": receipt["decision"],
        "reasons": receipt["reasons"],
        "receipt_id": receipt_id,
        "receipt_path": str(receipt_path),
        "counterfactual_summary": receipt["counterfactual_summary"],
        "normalized": receipt["normalized"]
    }, indent=2))


if __name__ == "__main__":
    main()