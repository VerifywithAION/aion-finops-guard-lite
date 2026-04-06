import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def eval_imported_snapshot(snapshot, policy):
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


def eval_local_job(payload, policy):
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


REPO_ROOT = Path(__file__).resolve().parent.parent
IMPORT_POLICY_PATH = REPO_ROOT / "policies" / "finops_import_policy_v1.json"
LOCAL_POLICY_PATH = REPO_ROOT / "policies" / "finops_local_policy_v1.json"
RECEIPTS_DIR = REPO_ROOT / "runtime" / "receipts"
RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "AIONFinOpsLite/0.1"

    def _json_response(self, code, obj):
        body = json.dumps(obj, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            return self._json_response(200, {
                "ok": True,
                "service": "aion-finops-guard-lite",
                "timestamp_utc": utc_now()
            })
        return self._json_response(404, {"error": "not_found"})

    def do_POST(self):
        try:
            if self.path == "/v1/finops/evaluate/import":
                payload = self._read_json_body()
                policy = load_json(IMPORT_POLICY_PATH)
                result = eval_imported_snapshot(payload, policy)
                receipt_id = "FINOPS_API_IMPORT_" + uuid.uuid4().hex[:12].upper()
                receipt = {
                    "receipt_id": receipt_id,
                    "timestamp_utc": utc_now(),
                    "mode": "api_import",
                    "decision": result["decision"],
                    "reasons": result["reasons"],
                    "counterfactual_summary": result["counterfactual_summary"],
                    "normalized": result["normalized"]
                }
                receipt_path = RECEIPTS_DIR / f"{receipt_id}.json"
                write_json(receipt_path, receipt)
                return self._json_response(200, {
                    "decision": receipt["decision"],
                    "reasons": receipt["reasons"],
                    "receipt_id": receipt_id,
                    "receipt_path": str(receipt_path),
                    "counterfactual_summary": receipt["counterfactual_summary"],
                    "normalized": receipt["normalized"]
                })

            if self.path == "/v1/finops/evaluate/local":
                payload = self._read_json_body()
                policy = load_json(LOCAL_POLICY_PATH)
                result = eval_local_job(payload, policy)
                receipt_id = "FINOPS_API_LOCAL_" + uuid.uuid4().hex[:12].upper()
                receipt = {
                    "receipt_id": receipt_id,
                    "timestamp_utc": utc_now(),
                    "mode": "api_local",
                    "decision": result["decision"],
                    "reasons": result["reasons"],
                    "counterfactual_summary": result["counterfactual_summary"],
                    "normalized": result["normalized"]
                }
                receipt_path = RECEIPTS_DIR / f"{receipt_id}.json"
                write_json(receipt_path, receipt)
                return self._json_response(200, {
                    "decision": receipt["decision"],
                    "reasons": receipt["reasons"],
                    "receipt_id": receipt_id,
                    "receipt_path": str(receipt_path),
                    "counterfactual_summary": receipt["counterfactual_summary"],
                    "normalized": receipt["normalized"]
                })

            return self._json_response(404, {"error": "not_found"})
        except Exception as e:
            return self._json_response(500, {"error": "server_error", "detail": str(e)})


def main():
    host = "127.0.0.1"
    port = 8789
    httpd = HTTPServer((host, port), Handler)
    print(json.dumps({
        "ok": True,
        "service": "aion-finops-guard-lite",
        "host": host,
        "port": port,
        "timestamp_utc": utc_now()
    }, indent=2))
    httpd.serve_forever()


if __name__ == "__main__":
    main()