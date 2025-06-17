from web3 import Web3

# Ethereum node and QuickNode Connection
quicknode_url = 'https://long-purple-sponge.quiknode.pro/c26d5842f372ee6e32fca748626397f1fa767b5c/'
ws_url = 'ws://100.110.237.84:8546'

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

# Web3 connections Initialization
w3_quicknode = Web3(Web3.HTTPProvider(quicknode_url))
w3_ws = Web3(Web3.WebsocketProvider(ws_url))

def get_token_details(w3, token_address):
    try:
        token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        name = token_contract.functions.name().call()
        symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()
        return name, symbol, decimals
    except Exception as e:
        print(f"Error fetching token details: {e}")
        return None, None, None

def get_transaction(w3, tx_hash):
    try:
        return w3.eth.get_transaction(tx_hash)
    except Exception as e:
        print(f"Error fetching transaction: {e}")
        return None

def get_transaction_receipt(w3, tx_hash):
    try:
        return w3.eth.get_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"Error fetching transaction receipt: {e}")
        return None

def decode_logs(w3, logs):
    transfer_event_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()
    log_entries = []
    
    for log in logs:
        if log['topics'][0].hex() == transfer_event_signature:
            token_contract_address = log['address'] 
            sender = w3.to_checksum_address('0x' + log['topics'][1].hex()[26:])
            receiver = w3.to_checksum_address('0x' + log['topics'][2].hex()[26:])
            
            # Convert HexBytes to a hexadecimal string and then to an integer
            data_hex = log['data'].hex()
            amount = int(data_hex, 16)
            
            # Token details
            token_name, token_symbol, token_decimals = get_token_details(w3, token_contract_address)
            if token_name is None:
                return None
            amount_normalized = amount / (10 ** token_decimals)
            
            log_entries.append({
                "token_contract_address": token_contract_address,
                "sender": sender,
                "receiver": receiver,
                "amount_normalized": amount_normalized,
                "token_symbol": token_symbol,
                "token_name": token_name
            })
    return log_entries

def trace_transaction(w3, tx_hash):    
    # Fetch transaction receipt
    tx_receipt = get_transaction_receipt(w3, tx_hash)
    if tx_receipt is None:
        print("Failed to fetch transaction receipt")
        return []

    # Decode logs
    log_details = decode_logs(w3, tx_receipt['logs'])
    
    return log_details

def compare_outputs(output1, output2, tx_hash):
    logs1 = output1
    logs2 = output2
    
    # Compare the length of the logs
    if len(logs1) != len(logs2):
        print("Number of logs differ.")
        return False
    logs1_sorted = sorted(logs1, key=lambda x: (x['token_contract_address'], x['sender'], x['receiver'], x['amount_normalized'], x['token_symbol'], x['token_name']))
    logs2_sorted = sorted(logs2, key=lambda x: (x['token_contract_address'], x['sender'], x['receiver'], x['amount_normalized'], x['token_symbol'], x['token_name']))

    # Validate if log entry is identical
    all_identical = True
    for i, (log1, log2) in enumerate(zip(logs1_sorted, logs2_sorted)):
        if log1 != log2:
            print(f"Log entry {i} differs:")
            print("QuickNode Log:", log1)
            print("WebSocket Log:", log2)
            all_identical = False
    
    if all_identical:
        print(f"\nAll log entries are validated for transaction hash {tx_hash}")
    else:
        print("Some log entries differ.")

    return all_identical

def validate_transactions(tx_hashes):
    for i, tx_hash in enumerate(tx_hashes, 1):
        print(f"\n{i}. Validating transaction {tx_hash}")
        
        # Get logs from QuickNode
        print("\nFetching logs from QuickNode")
        log_details_quicknode = trace_transaction(w3_quicknode, tx_hash)
        for log in log_details_quicknode:
            print(f"Transfer from {log['sender']} to {log['receiver']} of {log['amount_normalized']} {log['token_symbol']} ({log['token_name']}) tokens from Contract {log['token_contract_address']}")

        # Get logs from WebSocket
        print("\nFetching logs from E-Node")
        log_details_ws = trace_transaction(w3_ws, tx_hash)
        for log in log_details_ws:
            print(f"Transfer from {log['sender']} to {log['receiver']} of {log['amount_normalized']} {log['token_symbol']} ({log['token_name']}) tokens from Contract {log['token_contract_address']}")
        
        # Compare logs
        compare_outputs(log_details_quicknode, log_details_ws, tx_hash)

# List of transaction hashes to validate
tx_hashes = [
    '0x4606654aaf02a0c69b57e10d7ddc0cbd98d23e5d681cfe60a5a415cc4ba04986',
    '0x9820fce81e5ad1a7d963be407bceadeb5d000a07a8b08d468030748c413e6774',
    '0xf0ca92d76d405286b4aa231e3685b1057745b2b59d05b86335511d9aa4a9e34f',
    '0xae6a8a9dda931fe8eeac8f194723d57cf970c546c04a0c16f216bfc8f1c71d20',   
]
validate_transactions(tx_hashes)
