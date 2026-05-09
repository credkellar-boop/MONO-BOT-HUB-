import os
from web3 import AsyncWeb3
from eth_account import Account

async def execute_flash_rescue(w3: AsyncWeb3, private_key: str):
    """
    Sweeps all native MON to a designated cold wallet by
    bribing the validators with a high priority fee.
    """
    account = Account.from_key(private_key)
    cold_wallet = os.getenv("COLD_WALLET_ADDRESS")

    if not cold_wallet:
        raise ValueError("COLD_WALLET_ADDRESS environment variable not set.")

    print(f"Initiating Flash Rescue for {account.address}...")

    # 1. Get balance and nonce
    balance = await w3.eth.get_balance(account.address)
    nonce = await w3.eth.get_transaction_count(account.address)

    if balance == 0:
        return "Zero balance - nothing to rescue."

    # 2. Calculate HFT Gas Bribe (Max out priority to frontrun)
    base_fee = (await w3.eth.get_block('latest'))['baseFeePerGas']
    max_priority_fee = w3.to_wei(50, 'gwei') # Massive tip for validators
    max_fee = base_fee + max_priority_fee

    # 3. Calculate max amount to send (Balance - Gas Cost)
    gas_limit = 21000
    total_gas_cost = gas_limit * max_fee
    rescue_amount = balance - total_gas_cost

    if rescue_amount <= 0:
        return "Insufficient funds to cover HFT gas bribe."

    # 4. Build and Sign the Rescue Tx
    tx = {
        'nonce': nonce,
        'to': cold_wallet,
        'value': rescue_amount,
        'gas': gas_limit,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
        'chainId': await w3.eth.chain_id
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"Rescue Tx Broadcasted! Hash: {tx_hash.hex()}")
    return tx_hash.hex()
