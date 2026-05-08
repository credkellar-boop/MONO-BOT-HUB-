import os
from web3 import AsyncWeb3
from eth_account import Account

async def execute_flash_rescue(w3: AsyncWeb3, private_key: str) -> str:
    """
    Sweeps all native MON/ETH to a designated cold wallet,
    bribing the validators with a high priority fee to frontrun the attacker.
    """
    account = Account.from_key(private_key)
    cold_wallet = os.getenv("COLD_WALLET_ADDRESS")
    
    if not cold_wallet:
        raise ValueError("COLD_WALLET_ADDRESS secret is missing. Cannot rescue!")

    print(f"Initiating Flash Rescue for {account.address}...")

    # 1. Get current balance & Nonce
    balance = await w3.eth.get_balance(account.address)
    nonce = await w3.eth.get_transaction_count(account.address)
    
    if balance == 0:
        return "Zero balance - nothing to rescue."

    # 2. Calculate HFT Gas Bribe (Max out priority to frontrun)
    base_fee = (await w3.eth.get_block('latest'))['baseFeePerGas']
    max_priority_fee = w3.to_wei(50, 'gwei') # Massive tip for validators
    max_fee = base_fee + max_priority_fee

    # 3. Calculate gas limit for a standard transfer
    gas_limit = 21000
    total_gas_cost = gas_limit * max_fee
    
    # Amount to send is balance minus the massive gas cost
    rescue_amount = balance - total_gas_cost
    
    if rescue_amount <= 0:
        return "Insufficient funds to cover HFT gas bribe."

    # 4. Build the Rescue Tx
    tx = {
        'nonce': nonce,
        'to': cold_wallet,
        'value': rescue_amount,
        'gas': gas_limit,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
        'chainId': await w3.eth.chain_id
    }

    # 5. Sign and Broadcast
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"Rescue Tx Broadcasted! Frontrunning attacker...")
    
    # Wait for confirmation (timeout after 10 seconds for HFT)
    receipt = await w3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
    
    if receipt['status'] == 1:
        return tx_hash.hex()
    else:
        raise Exception("Rescue transaction failed on-chain.")
