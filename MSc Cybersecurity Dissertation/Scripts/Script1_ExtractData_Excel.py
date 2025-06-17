import pandas as pd
from web3 import Web3

# Ethereum node Connection via WebSocket
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

# DNS - Ethereum addresses to names
address_book = {
    '0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559': 'Odos: Router V2',
    '0xF977814e90dA44bFA03b6295A0616a897441aceC': 'Binance 8',
    '0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503': 'Binance: Binance-Peg Tokens',
    '0x95C4F5b83aA70810D4f142d58e5F7242Bd891CB0': 'DODO: Multisig 2',
    '0x5754284f345afc66a98fbB0a0Afe71e0F007B949': 'Tether: Treasury',
    '0x1dBbBC3Fdb2C4FaBd28fd9b84Ed99ceb84BfBeC5': 'Tether: USDT Stablecoin',
    '0x5041ed759Dd4aFc3a72b8192C143F72f4724081A': 'OKX 7',
    '0x77134cbC06cB00b66F4c7e623D5fdBF6777635EC': 'Bitfinex: Hot Wallet',
    '0xA9D1e08C7793af67e9d92fe308d5697FB81d3E43': 'Coinbase 10',
    '0xaB782bc7D4a2b306825de5a7730034F8F63ee1bC': 'Bitvavo: Hot 3',
    '0x28C6c06298d514Db089934071355E5743bf21d60': 'Binance 14',
}

def get_token_details(token_address):
    token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    name = token_contract.functions.name().call()
    symbol = token_contract.functions.symbol().call()
    decimals = token_contract.functions.decimals().call()
    return name, symbol, decimals

def get_transaction(tx_hash):
    return w3.eth.get_transaction(tx_hash)

def get_transaction_receipt(tx_hash):
    return w3.eth.get_transaction_receipt(tx_hash)

def get_name_from_address(address):
    return address_book.get(address, "Unknown")

def decode_logs(logs, tx_hash, block_number):
    transfer_event_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()
    decoded_logs = []
    for log in logs:
        if log['topics'][0].hex() == transfer_event_signature:
            token_contract_address = log['address']  # The contract address of the token
            sender = w3.to_checksum_address('0x' + log['topics'][1].hex()[26:])
            receiver = w3.to_checksum_address('0x' + log['topics'][2].hex()[26:])
            amount_hex = log['data'].hex()  # Convert HexBytes to hex string
            
            # Check if amount_hex is empty or just '0x'
            if amount_hex != '0x':
                amount = int(amount_hex, 16)
                # Get the token details
                token_name, token_symbol, token_decimals = get_token_details(token_contract_address)
                amount_normalized = amount / (10 ** token_decimals)
                
                # Determine the sender and receiver names
                sender_name = get_name_from_address(sender)
                receiver_name = get_name_from_address(receiver)
                
                if sender_name == "Unknown":
                    sender_name = sender
                if receiver_name == "Unknown":
                    receiver_name = receiver

                decoded_logs.append({
                    "Transaction Hash": tx_hash,
                    "Block Number": block_number,
                    "Sender Address": sender,
                    "Sender Name": sender_name,
                    "Receiver Address": receiver,
                    "Receiver Name": receiver_name,
                    "Amount": amount_normalized,
                    "Token Symbol": token_symbol,
                    "Token Name": token_name,
                    "Contract Address": token_contract_address
                })
            else:
                print(f"Skipping log with empty amount in transaction {tx_hash}")
                
    return decoded_logs

def trace_transaction(tx_hash):
    print(f"\nTracing transaction: {tx_hash}")
    
    tx_receipt = get_transaction_receipt(tx_hash)
    if tx_receipt:
        return decode_logs(tx_receipt['logs'], tx_hash, tx_receipt['blockNumber'])
    else:
        print("Transaction receipt not found")
        return []

def collect_and_store_data(transaction_hashes, output_file):
    all_logs = []
    for tx_hash in transaction_hashes:
        logs = trace_transaction(tx_hash)
        all_logs.extend(logs)
    
    df = pd.DataFrame(all_logs)
    df.to_excel(output_file, index=False)

transaction_hashes = [
    '0x4606654aaf02a0c69b57e10d7ddc0cbd98d23e5d681cfe60a5a415cc4ba04986',
    '0x9820fce81e5ad1a7d963be407bceadeb5d000a07a8b08d468030748c413e6774',
    '0xf0ca92d76d405286b4aa231e3685b1057745b2b59d05b86335511d9aa4a9e34f',
    '0xae6a8a9dda931fe8eeac8f194723d57cf970c546c04a0c16f216bfc8f1c71d20',   
]

# Output file
output_file = 'transaction_data.xlsx'

collect_and_store_data(transaction_hashes, output_file)
