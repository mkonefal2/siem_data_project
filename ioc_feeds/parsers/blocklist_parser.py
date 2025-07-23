from datetime import datetime


def parse_blocklist(lines: list[str], source: str = "blocklist.de") -> list[dict]:
    results = []
    ts = datetime.utcnow().isoformat() + "Z"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        results.append({
            "type": "ip",
            "value": line,
            "source": source,
            "threat_type": None,
            "timestamp": ts
        })
    return results
