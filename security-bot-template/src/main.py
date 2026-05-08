import os
import asyncio
from web3 import AsyncWeb3
from monitor import check_mempool_threats
from recovery import execute_flash_rescue

# Initialize async connection to Monad Node
RPC_URL = os.getenv("MONAD_RPC_URL")
w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(RPC_URL))

async def shield_guard():
    print("Initializing Shield Guard...")
    
    # Verify node connection
    if not await w3.is_connected():
        raise ConnectionError("Failed to connect to Monad RPC Node.")
        
    latest_block = await w3.eth.block_number
    print(f"Connected. Monitoring Monad from block: {latest_block}")
    
    # Run the threat detection
    threat_detected = await check_mempool_threats(w3)
    
    if threat_detected:
        print("ALERT: Threat detected in mempool. Initiating Flash Rescue...")
        # Execute the rescue transaction immediately
        tx_hash = await execute_flash_rescue(w3, os.getenv("WALLET_PRIVATE_KEY"))
        print(f"Rescue Transaction Confirmed: {tx_hash}")
        
        # Log to audit (to be picked up by the global_royalty_audit.py)
        with open("audit/latest_rescue.csv", "w") as f:
            f.write(f"Block,TxHash,Status\n{latest_block},{tx_hash},Secured")
    else:
        print("Status: Normal. No threats detected.")

if __name__ == "__main__":
    # Run the async event loop
    asyncio.run(shield_guard())
