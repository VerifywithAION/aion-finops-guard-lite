import json
import sys
from pathlib import Path

def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def normalize(payload):
    provider = payload.get("provider", "buzz_import")
    source_type = payload.get("source_type", "risk_or_spend_snapshot")
    currency = payload.get("currency", "USD")
    account_ref = payload.get("account_ref", "unknown_account")
    snapshot_timestamp_utc = payload.get("snapshot_timestamp_utc", "")
    items = payload.get("items", [])
    buzz_context = payload.get("buzz_context", {})

    normalized_items = []
    for item in items:
        normalized_items.append({
            "service": item.get("service", "unknown_service"),
            "category": item.get("category", "unknown_category"),
            "amount": float(item.get("amount", 0.0)),
            "quantity": item.get("quantity", 1),
            "unit": item.get("unit", "unit")
        })

    return {
        "snapshot_kind": "imported_billing_snapshot",
        "provider": provider,
        "source_type": source_type,
        "currency": currency,
        "snapshot_timestamp_utc": snapshot_timestamp_utc,
        "account_ref": account_ref,
        "items": normalized_items,
        "upstream_context": {
            "origin": "buzz",
            "buzz_context": buzz_context
        }
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python buzz_to_finops_import.py <buzz_payload.json> <out_snapshot.json>")
        sys.exit(2)

    in_path = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]).resolve()

    payload = load_json(in_path)
    normalized = normalize(payload)
    write_json(out_path, normalized)

    print(json.dumps({
        "status": "OK",
        "input": str(in_path),
        "output": str(out_path),
        "provider": normalized.get("provider"),
        "item_count": len(normalized.get("items", []))
    }, indent=2))

if __name__ == "__main__":
    main()