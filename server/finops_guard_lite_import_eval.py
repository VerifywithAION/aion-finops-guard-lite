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


def to_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return float(default)


def to_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return int(default)


def normalize_string(value):
    return str(value).strip()


def evaluate_aml(snapshot, policy, current_decision=None):
    aml_policy = policy.get("aml", {}) or {}
    if not aml_policy.get("enabled", True):
        return {
            "signal": "DISABLED",
            "reasons": ["aml_disabled"],
            "recommended_mode": current_decision or "ALLOW"
        }

    upstream = snapshot.get("upstream_context", {}) or {}
    risk_context = upstream.get("risk_context", {}) or {}

    security_flags = risk_context.get("security_flags", []) or []
    shield_scan = normalize_string(risk_context.get("shield_scan", "")).upper()
    classification = normalize_string(risk_context.get("classification", "")).upper()
    score = to_int(risk_context.get("score", 0), 0)
    mirofish_belief = to_float(risk_context.get("mirofish_belief", 0.0), 0.0)
    liquidity = to_float(risk_context.get("liquidity", 0.0), 0.0)
    volume_24h = to_float(risk_context.get("volume_24h", 0.0), 0.0)

    flag_count = len(security_flags)
    warm_band = classification in ["WARM", "COLD", "UNKNOWN", ""]
    low_score = score < to_int(aml_policy.get("safe_score_threshold", 80), 80)
    very_low_score = score < to_int(aml_policy.get("block_score_threshold", 60), 60)
    shield_not_clean = shield_scan not in ["CLEAN", ""]
    low_mirofish = mirofish_belief < to_float(aml_policy.get("mirofish_warn_threshold", 0.60), 0.60)
    low_liquidity = liquidity < to_float(aml_policy.get("warn_liquidity_threshold", 100000.0), 100000.0)
    low_volume = volume_24h < to_float(aml_policy.get("warn_volume_threshold", 300000.0), 300000.0)

    signal = "LOW"
    reasons = []
    recommended_mode = current_decision or "ALLOW"

    if flag_count > 0:
        reasons.append("security_flags_present")
    if shield_not_clean:
        reasons.append("shield_scan_not_clean")
    if low_score:
        reasons.append("score_below_safe_threshold")
    if very_low_score:
        reasons.append("score_below_block_threshold")
    if warm_band:
        reasons.append("classification_below_hot_band")
    if low_mirofish:
        reasons.append("mirofish_belief_below_warn_threshold")
    if low_liquidity:
        reasons.append("liquidity_below_warn_threshold")
    if low_volume:
        reasons.append("volume_below_warn_threshold")

    block_reasons = 0
    warn_reasons = 0

    for r in reasons:
        if r in ["security_flags_present", "shield_scan_not_clean", "score_below_block_threshold"]:
            block_reasons += 1
        else:
            warn_reasons += 1

    if block_reasons >= 2:
        signal = "HIGH"
        recommended_mode = "BLOCK"
    elif block_reasons >= 1:
        signal = "HIGH"
        recommended_mode = "WARN" if current_decision != "BLOCK" else "BLOCK"
    elif warn_reasons >= 3:
        signal = "ELEVATED"
        recommended_mode = "WARN" if current_decision != "BLOCK" else "BLOCK"
    elif warn_reasons >= 1:
        signal = "ELEVATED"
        recommended_mode = "WARN" if current_decision == "ALLOW" else current_decision
    else:
        signal = "LOW"
        recommended_mode = current_decision or "ALLOW"

    if not reasons:
        reasons.append("aml_within_baseline")

    return {
        "signal": signal,
        "reasons": reasons,
        "recommended_mode": recommended_mode
    }


def evaluate(snapshot, policy):
    items = snapshot.get("items", [])
    blocked_services = [str(x).strip().lower() for x in policy.get("blocked_services", [])]

    total_cost = 0.0
    max_item_cost = 0.0
    offending_services = []

    for item in items:
        amt = to_float(item.get("amount", 0.0), 0.0)
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

    if max_item_cost > to_float(policy.get("max_single_item_cost", 100.0), 100.0) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("single_item_cost_exceeds_max")

    if total_cost > to_float(policy.get("max_total_snapshot_cost", 150.0), 150.0) and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("total_snapshot_cost_exceeds_max")

    if max_item_cost > to_float(policy.get("warn_single_item_cost", 50.0), 50.0) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("single_item_cost_exceeds_warn")

    if total_cost > to_float(policy.get("warn_total_snapshot_cost", 100.0), 100.0) and decision == "ALLOW":
        decision = "WARN"
        reasons.append("total_snapshot_cost_exceeds_warn")

    cf = None
    cf_policy = policy.get("counterfactual", {})
    if cf_policy.get("enabled", True):
        repeat_periods = to_int(cf_policy.get("repeat_periods", 3), 3)
        upshift_multiplier = to_float(cf_policy.get("upshift_multiplier", 1.5), 1.5)

        projected_repeated_total = total_cost * repeat_periods
        projected_upshift_total = total_cost * upshift_multiplier

        fragility = "LOW"
        dominant_risk = "none"

        if projected_upshift_total > to_float(policy.get("max_total_snapshot_cost", 150.0), 150.0):
            fragility = "HIGH"
            dominant_risk = "upshifted_snapshot_breaks_policy"
        elif projected_repeated_total > to_float(policy.get("max_total_snapshot_cost", 150.0), 150.0):
            fragility = "HIGH"
            dominant_risk = "repeated_periods_break_policy"
        elif projected_upshift_total > to_float(policy.get("warn_total_snapshot_cost", 100.0), 100.0):
            fragility = "MEDIUM"
            dominant_risk = "upshifted_snapshot_warns"

        if projected_repeated_total > to_float(policy.get("warn_total_snapshot_cost", 100.0), 100.0) and decision == "ALLOW":
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

    aml_summary = evaluate_aml(snapshot, policy, decision)

    if aml_summary["recommended_mode"] == "BLOCK" and decision != "BLOCK":
        decision = "BLOCK"
        reasons.append("aml_recommended_block")
    elif aml_summary["recommended_mode"] == "WARN" and decision == "ALLOW":
        decision = "WARN"
        reasons.append("aml_recommended_warn")

    if not reasons:
        reasons.append("snapshot_within_policy")

    return {
        "decision": decision,
        "reasons": reasons,
        "aml_summary": aml_summary,
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
        "aml_summary": result["aml_summary"],
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
        "aml_summary": receipt["aml_summary"],
        "counterfactual_summary": receipt["counterfactual_summary"],
        "normalized": receipt["normalized"]
    }, indent=2))


if __name__ == "__main__":
    main()