from datetime import datetime
def parse_threatfox(data: list[dict], source: str = "threatfox") -> list[dict]:
    results = []
    ts = datetime.utcnow().isoformat() + "Z"
    for item in data:
        ioc_type = item.get("ioc_type") or item.get("type")
        value = item.get("ioc") or item.get("value")
        threat = item.get("malware" ) or item.get("threat_type")
        if not value:
            continue
        results.append({
            "type": ioc_type,
            "value": value,
            "source": source,
            "threat_type": threat,
            "timestamp": ts
        })
    return results
