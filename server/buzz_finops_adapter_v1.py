import json
import sys
import urllib.request
from pathlib import Path

API_URL = "http://127.0.0.1:8789/v1/finops/evaluate/import"

def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def classify_buzz_overlay(payload):
    score = int(payload.get("score", 0))
    classification = str(payload.get("classification", "")).upper()
    shield_scan = str(payload.get("shield_scan", "")).upper()
    security_flags = payload.get("security_flags", []) or []
    mirofish_belief = float(payload.get("mirofish_belief", 0.0))
    est_cost = float(payload.get("estimated_cost_usd", 0.0))

    overlay = {
        "mode": "advisory_only",
        "intelligence_signal": "NEUTRAL",
        "hybrid_candidate": "WARN_CANDIDATE",
        "notes": []
    }

    if shield_scan == "CLEAN" and len(security_flags) == 0 and score >= 90 and classification == "HOT":
        overlay["intelligence_signal"] = "STRONG"
        overlay["hybrid_candidate"] = "ALLOW_CANDIDATE"
        overlay["notes"].append("strong_buzz_signal")
    elif len(security_flags) > 0 or shield_scan != "CLEAN" or score < 70:
        overlay["intelligence_signal"] = "FRAGILE"
        overlay["hybrid_candidate"] = "BLOCK_CANDIDATE"
        overlay["notes"].append("buzz_risk_signal_present")
    else:
        overlay["intelligence_signal"] = "MIXED"
        overlay["hybrid_candidate"] = "WARN_CANDIDATE"
        overlay["notes"].append("intermediate_buzz_signal")

    if mirofish_belief >= 0.75:
        overlay["notes"].append("high_mirofish_belief")
    if est_cost == 0:
        overlay["notes"].append("zero_direct_cost_action")

    return overlay

def normalize_buzz_payload(payload):
    estimated_cost = float(payload.get("estimated_cost_usd", 0.0))
    token = payload.get("token", "UNKNOWN")
    chain = payload.get("chain", "unknown")
    action = payload.get("action", "unknown_action")

    normalized = {
        "snapshot_kind": "imported_billing_snapshot",
        "provider": "buzz_import",
        "source_type": "buzz_action_evaluation",
        "currency": "USD",
        "account_ref": f"buzz::{chain}::{action}",
        "items": [
            {
                "service": "buzz_action",
                "category": action,
                "amount": estimated_cost,
                "quantity": 1,
                "unit": "action"
            }
        ],
        "upstream_context": {
            "origin": "buzz",
            "token": token,
            "chain": chain,
            "action": action,
            "risk_context": {
                "market_cap": payload.get("market_cap"),
                "liquidity": payload.get("liquidity"),
                "volume_24h": payload.get("volume_24h"),
                "score": payload.get("score"),
                "classification": payload.get("classification"),
                "security_flags": payload.get("security_flags", []),
                "scoring_rules_applied": payload.get("scoring_rules_applied"),
                "mirofish_belief": payload.get("mirofish_belief"),
                "shield_scan": payload.get("shield_scan"),
                "source": payload.get("source")
            }
        }
    }
    return normalized

def call_finops_api(normalized):
    data = json.dumps(normalized).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)

def main():
    if len(sys.argv) < 2:
        print("Usage: python buzz_finops_adapter_v1.py <buzz_payload.json> [output.json]")
        sys.exit(2)

    payload_path = Path(sys.argv[1]).resolve()
    output_path = None
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).resolve()

    payload = load_json(payload_path)
    normalized = normalize_buzz_payload(payload)
    buzz_overlay = classify_buzz_overlay(payload)
    finops_response = call_finops_api(normalized)

    result = {
        "adapter": "buzz_finops_adapter_v1",
        "mode": "sync",
        "buzz_input": {
            "token": payload.get("token"),
            "chain": payload.get("chain"),
            "action": payload.get("action"),
            "classification": payload.get("classification"),
            "score": payload.get("score"),
            "security_flags": payload.get("security_flags", []),
            "mirofish_belief": payload.get("mirofish_belief"),
            "shield_scan": payload.get("shield_scan")
        },
        "normalized_snapshot": normalized,
        "buzz_overlay": buzz_overlay,
        "finops_response": finops_response
    }

    if output_path is not None:
        write_json(output_path, result)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()