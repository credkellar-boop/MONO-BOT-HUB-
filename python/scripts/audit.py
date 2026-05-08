import os
import csv
from api import fetch_transactions
from logger import get_logger

logger = get_logger("audit")

def find_suspicious(transactions: list, threshold: float = 100000.0) -> list:
    """Filters transactions exceeding the security threshold."""
    suspicious = []
    for tx in transactions:
        try:
            amount = float(tx.get("amount", 0))
            if amount >= threshold:
                suspicious.append(tx)
        except (TypeError, ValueError):
            continue
    return suspicious

def run_audit():
    """Main execution loop for a single bot audit."""
    fund_type = os.getenv("FUND_TYPE", "growth")
    batch = int(os.getenv("BATCH", "1"))
    api_key = os.getenv("API_KEY")

    if not api_key:
        logger.error("API_KEY is not set.")
        return

    transactions = fetch_transactions(fund_type, batch, api_key)
    suspicious = find_suspicious(transactions)

    # Save results to the audit folder for GitHub Artifact upload
    output_all = f"audit/{fund_type}_batch_{batch}_all.csv"
    output_threats = f"audit/{fund_type}_batch_{batch}_threats.csv"
    
    # ... logic to write CSV using csv.DictWriter ...
    logger.info(f"Audit complete. Threats found: {len(suspicious)}")

if __name__ == "__main__":
    run_audit()
