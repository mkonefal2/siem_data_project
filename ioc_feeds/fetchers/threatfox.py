import requests
from loguru import logger


def fetch_threatfox(url: str, payload: dict, headers: dict | None = None, retries: int = 3) -> list[dict]:
    """Fetch IoCs from ThreatFox API with optional authentication headers."""

    headers = headers.copy() if headers else {}
    api_key = payload.pop("api_key", None) or headers.pop("api_key", None)
    if api_key and "API-KEY" not in headers and "API-Key" not in headers:
        headers["API-KEY"] = api_key

    for attempt in range(1, retries + 1):
        try:
            logger.info("Fetching ThreatFox data (attempt {}/{})", attempt, retries)
            response = requests.post(url, json=payload, headers=headers or None, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            logger.error("Error fetching ThreatFox: {}", e)
            if attempt == retries:
                raise
    return []
