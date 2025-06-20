from web3 import Web3

# Ethereum node connection via WebSocket
w3 = Web3(Web3.WebsocketProvider('ws://100.110.237.84:8546'))

# ABI fragments for the ERC20 `name`, `symbol`, and `decimals` methods
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    }
]

# Function to get token details
def get_token_details(token_address):
    token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    name = token_contract.functions.name().call()
    symbol = token_contract.functions.symbol().call()
    decimals = token_contract.functions.decimals().call()
    return name, symbol, decimals

# Function to fetch a transaction
def get_transaction(tx_hash):
    return w3.eth.get_transaction(tx_hash)

# Function to fetch a transaction receipt
def get_transaction_receipt(tx_hash):
    return w3.eth.get_transaction_receipt(tx_hash)

# Function to decode logs
def decode_logs(logs):
    transfer_event_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()
    
    for log in logs:
        if log['topics'][0].hex() == transfer_event_signature:
            token_contract_address = log['address']  # The contract address of the token
            sender = w3.to_checksum_address('0x' + log['topics'][1].hex()[26:])
            receiver = w3.to_checksum_address('0x' + log['topics'][2].hex()[26:])
            amount = int.from_bytes(log['data'], byteorder='big')
            
            token_name, token_symbol, token_decimals = get_token_details(token_contract_address)
            amount_normalized = amount / (10 ** token_decimals)
            
            print(f"\nTransfer from {sender} to {receiver} of {amount_normalized} {token_symbol} ({token_name}) tokens from Contract {token_contract_address}")

def trace_transaction(tx_hash):
    
    # Get the transaction receipt
    tx_receipt = get_transaction_receipt(tx_hash)
    
    if tx_receipt:
        # Decode the logs
        decode_logs(tx_receipt['logs'])
    else:
        print(f"Failed to fetch receipt for transaction: {tx_hash}")

def trace_multiple_transactions(tx_hashes):
    for index, tx_hash in enumerate(tx_hashes, start=1):
        print(f"\n\n{index}. Tracing transaction: {tx_hash}")
        trace_transaction(tx_hash)

tx_hashes = [
    '0x4606654aaf02a0c69b57e10d7ddc0cbd98d23e5d681cfe60a5a415cc4ba04986',
    '0x9820fce81e5ad1a7d963be407bceadeb5d000a07a8b08d468030748c413e6774',
    '0xf0ca92d76d405286b4aa231e3685b1057745b2b59d05b86335511d9aa4a9e34f',
    '0xae6a8a9dda931fe8eeac8f194723d57cf970c546c04a0c16f216bfc8f1c71d20',
]

trace_multiple_transactions(tx_hashes)
