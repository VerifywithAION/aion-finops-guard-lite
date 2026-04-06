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


def decide(payload, policy):
    runtime = str(payload.get("runtime", "")).strip().lower()
    model = str(payload.get("model", "")).strip().lower()
    actor = str(payload.get("actor", "unknown"))
    job_type = str(payload.get("job_type", "inference"))
    estimated_job_cost = float(payload.get("estimated_job_cost", 0.0))
    estimated_gpu_gb = float(payload.get("estimated_gpu_gb", 0.0))
    estimated_ram_gb = float(payload.get("estimated_ram_gb", 0.0))
    scope_level = int(payload.get("scope_level", 1))

    decision = "ALLOW"
    reasons = []

    allowed_runtimes = [str(x).strip().lower() for x in policy.get("allowed_runtimes", [])]
    if allowed_runtimes and runtime not in allowed_runtimes:
        decision = "BLOCK"
        reasons.append("runtime_not_allowed")

    blocked_models = [str(x).strip().lower() for x in policy.get("blocked_models", [])]
    if model in blocked_models:
        decision = "BLOCK"
        reasons.append("model_blocked_by_policy")

    if scope_level > int(policy.get("max_scope_level", 3)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("scope_exceeds_authorized_level")

    if estimated_job_cost > float(policy.get("max_estimated_job_cost", 8.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("estimated_job_cost_exceeds_max")

    if estimated_job_cost > float(policy.get("warn_estimated_job_cost", 3.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("estimated_job_cost_exceeds_warn_threshold")

    warn_models = [str(x).strip().lower() for x in policy.get("warn_models", [])]
    if model in warn_models and decision == "ALLOW":
        decision = "WARN"
        reasons.append("model_in_warn_band")

    r = policy.get("resource_thresholds", {})
    if estimated_gpu_gb > float(r.get("max_estimated_gpu_gb", 12.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("gpu_requirement_exceeds_max")

    if estimated_ram_gb > float(r.get("max_estimated_ram_gb", 24.0)) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("ram_requirement_exceeds_max")

    if estimated_gpu_gb > float(r.get("warn_estimated_gpu_gb", 6.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("gpu_requirement_exceeds_warn_threshold")

    if estimated_ram_gb > float(r.get("warn_estimated_ram_gb", 12.0)) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("ram_requirement_exceeds_warn_threshold")

    cf = None
    cf_policy = policy.get("counterfactual", {})
    if cf_policy.get("enabled", True):
        repeat_attempts = int(cf_policy.get("repeat_attempts", 5))
        job_cost_upshift_multiplier = float(cf_policy.get("job_cost_upshift_multiplier", 2.0))
        resource_upshift_multiplier = float(cf_policy.get("resource_upshift_multiplier", 1.5))
        stricter_profile_job_cost = float(cf_policy.get("stricter_profile_job_cost", 2.5))

        projected_daily_cost = estimated_job_cost * repeat_attempts
        upshift_job_cost = estimated_job_cost * job_cost_upshift_multiplier
        upshift_gpu = estimated_gpu_gb * resource_upshift_multiplier
        upshift_ram = estimated_ram_gb * resource_upshift_multiplier

        fragility = "LOW"
        dominant_risk = "none"

        if upshift_job_cost > float(policy.get("max_estimated_job_cost", 8.0)):
            fragility = "HIGH"
            dominant_risk = "job_cost_upshift_breaks_policy"
        elif projected_daily_cost > float(policy.get("max_projected_daily_cost", 20.0)):
            fragility = "HIGH"
            dominant_risk = "repeat_attempts_break_daily_budget"
        elif upshift_gpu > float(r.get("max_estimated_gpu_gb", 12.0)):
            fragility = "HIGH"
            dominant_risk = "gpu_upshift_breaks_policy"
        elif upshift_ram > float(r.get("max_estimated_ram_gb", 24.0)):
            fragility = "HIGH"
            dominant_risk = "ram_upshift_breaks_policy"
        elif estimated_job_cost > stricter_profile_job_cost:
            fragility = "MEDIUM"
            dominant_risk = "stricter_profile_reveals_fragility"

        if projected_daily_cost > float(policy.get("warn_projected_daily_cost", 10.0)) and decision == "ALLOW":
            decision = "WARN"
            reasons.append("counterfactual_projected_daily_cost_warns")

        cf = {
            "projected_daily_cost": round(projected_daily_cost, 2),
            "upshift_job_cost": round(upshift_job_cost, 2),
            "upshift_gpu_gb": round(upshift_gpu, 2),
            "upshift_ram_gb": round(upshift_ram, 2),
            "fragility": fragility,
            "dominant_risk": dominant_risk,
            "tested_variants": [
                "job_cost_upshift",
                "repeat_attempt",
                "resource_upshift",
                "stricter_profile"
            ]
        }

    if not reasons:
        reasons.append("within_local_policy")

    return {
        "decision": decision,
        "reasons": reasons,
        "counterfactual_summary": cf,
        "normalized": {
            "runtime": runtime,
            "model": model,
            "job_type": job_type,
            "actor": actor,
            "estimated_job_cost": estimated_job_cost,
            "estimated_gpu_gb": estimated_gpu_gb,
            "estimated_ram_gb": estimated_ram_gb,
            "scope_level": scope_level
        }
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python finops_guard_lite_local.py <payload.json> <policy.json>")
        sys.exit(2)

    payload_path = Path(sys.argv[1]).resolve()
    policy_path = Path(sys.argv[2]).resolve()

    payload = load_json(payload_path)
    policy = load_json(policy_path)

    result = decide(payload, policy)

    receipt_id = "FINOPS_LOCAL_" + uuid.uuid4().hex[:12].upper()
    receipt = {
        "receipt_id": receipt_id,
        "timestamp_utc": utc_now(),
        "policy_version": policy.get("version", "unknown"),
        "mode": policy.get("mode", "unknown"),
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