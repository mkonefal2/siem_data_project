import requests
from loguru import logger


def fetch_threatfox(url: str, payload: dict, retries: int = 3, *, raise_on_fail: bool = True) -> list[dict]:
    for attempt in range(1, retries + 1):
        try:
            logger.info("Fetching ThreatFox data (attempt {}/{})", attempt, retries)
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            logger.error("Error fetching ThreatFox: {}", e)
            if attempt == retries:
                if raise_on_fail:
                    raise
                logger.error("Failed to fetch ThreatFox after {} attempts", retries)
                return []
    return []
