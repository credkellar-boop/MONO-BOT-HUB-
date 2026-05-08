import os
import requests
from logger import get_logger
from errors import APIRequestError

logger = get_logger("api")

def fetch_transactions(fund_type: str, batch: int, api_key: str) -> list:
    """Fetches transaction data for a specific bot batch."""
    api_base_url = os.getenv("API_BASE_URL", "https://api.example.com")
    url = f"{api_base_url}/audit"
    
    params = {"fund_type": fund_type, "batch": batch}
    headers = {"Authorization": f"Bearer {api_key}"}

    logger.info(f"Requesting tx for fund={fund_type} batch={batch}")
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        
        data = resp.json()
        transactions = data.get("transactions", [])
        logger.info(f"Fetched {len(transactions)} transactions")
        return transactions

    except requests.RequestException as exc:
        logger.error(f"API request failed: {exc}")
        raise APIRequestError(f"API request failed: {exc}")
