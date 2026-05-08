import os
import asyncio
from web3 import AsyncWeb3
from web3.exceptions import TransactionNotFound

async def check_mempool_threats(w3: AsyncWeb3) -> bool:
    """
    Listens to the Monad mempool for unauthorized transactions 
    targeting the shielded wallet.
    """
    shielded_wallet = os.getenv("WALLET_PUB_KEY", "").lower()
    if not shielded_wallet:
        print("WARNING: WALLET_PUB_KEY not set. Cannot monitor threats.")
        return False

    print(f"Subscribing to pending transactions for {shielded_wallet}...")
    
    # In a true HFT setup, use wss:// for real-time subscription
    # Note: Requires a WebSocket provider in production
    try:
        pending_filter = await w3.eth.filter('pending')
        
        # Scan for max 45 seconds (GitHub Action lifecycle limit)
        for _ in range(45):
            new_entries = await pending_filter.get_new_entries()
            for tx_hash in new_entries:
                try:
                    tx = await w3.eth.get_transaction(tx_hash)
                    # Threat Condition: Tx origin is our wallet, but we didn't authorize it
                    if tx and tx['from'].lower() == shielded_wallet:
                        print(f"CRITICAL: Unauthorized outbound tx detected! Hash: {tx_hash.hex()}")
                        return True
                except TransactionNotFound:
                    # Tx dropped or not yet available
                    continue
            
            await asyncio.sleep(1) # Yield to event loop
            
    except Exception as e:
        print(f"Monitor Error: {e}")
        
    return False
