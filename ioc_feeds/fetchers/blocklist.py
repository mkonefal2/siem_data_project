import requests
from loguru import logger


def fetch_blocklist(url: str, retries: int = 3) -> list[str]:
    for attempt in range(1, retries + 1):
        try:
            logger.info("Fetching Blocklist.de data (attempt {}/{})", attempt, retries)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text.splitlines()
        except Exception as e:
            logger.error("Error fetching blocklist.de: {}", e)
            if attempt == retries:
                raise
    return []
