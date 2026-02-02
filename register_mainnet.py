#!/usr/bin/env python3
"""
OpenClaw ERC-8004 Registration (Ethereum Mainnet).

Requirements:
- Python 3.8+
- pip install web3 requests eth-account

Usage:
    python3 register_mainnet.py \\
        --files AGENTS.md IDENTITY.md SOUL.md MEMORY.md \\
        --private-key YOUR_KEY \\
        --pinata-jwt YOUR_JWT
"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path
from web3 import Web3
from eth_account import Account

# ============================================================================
# Configuration (Mainnet)
# ============================================================================

RPC_URL = "https://eth.drpc.org"
CONTRACT_ADDRESS = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
EXPLORER_URL = "https://etherscan.io"
CHAIN_ID = 1

# ABI
CONTRACT_ABI = [
    {
        "inputs": [
            {"name": "agentURI", "type": "string"},
            {"name": "metadata", "type": "tuple[]", "components": [
                {"name": "metadataKey", "type": "string"},
                {"name": "metadataValue", "type": "bytes"}
            ]}
        ],
        "name": "register",
        "outputs": [{"name": "agentId", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "newURI", "type": "string"}
        ],
        "name": "setAgentURI",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "agentId", "type": "uint256"},
            {"indexed": False, "name": "agentURI", "type": "string"},
            {"indexed": True, "name": "owner", "type": "address"}
        ],
        "name": "Registered",
        "type": "event"
    }
]

# ============================================================================
# IPFS Helpers (Pinata)
# ============================================================================

def upload_file_to_pinata(filepath: str, jwt: str) -> str:
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f'Bearer {jwt}'}
    filename = Path(filepath).name
    
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f)}
        options = {
            'pinataOptions': json.dumps({'cidVersion': 1}),
            'pinataMetadata': json.dumps({'name': filename})
        }
        response = requests.post(url, files=files, headers=headers, data=options)
    
    if response.status_code == 200:
        cid = response.json()['IpfsHash']
        print(f"      ✅ Uploaded {filename} -> ipfs://{cid}")
        return f"ipfs://{cid}"
    raise Exception(f"Pinata upload failed for {filename}: {response.text}")

def upload_json_to_pinata(data: dict, filename: str, jwt: str) -> str:
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    payload = {
        'pinataContent': data,
        'pinataMetadata': {'name': filename},
        'pinataOptions': {'cidVersion': 1}
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        cid = response.json()['IpfsHash']
        print(f"      ✅ Uploaded {filename} -> ipfs://{cid}")
        return f"ipfs://{cid}"
    raise Exception(f"Pinata JSON upload failed: {response.text}")

# ============================================================================
# Agent Card Generator
# ============================================================================

def read_file_safe(filepath: str) -> str:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def extract_name(identity_path: str) -> str:
    content = read_file_safe(identity_path)
    for line in content.splitlines():
        if "**Name:**" in line:
            return line.split("**Name:**")[1].strip()
    return "OpenClaw Agent"

def generate_agent_card(ipfs_uris: dict, file_paths: dict) -> dict:
    name = extract_name(file_paths.get("IDENTITY", ""))
    return {
        "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
        "name": name,
        "description": f"Autonomous OpenClaw Agent: {name}",
        "image": "https://github.com/openclaw/openclaw/blob/main/docs/assets/openclaw-logo-text-dark.png",
        "services": [
            {"name": "AGENTS", "endpoint": ipfs_uris.get("AGENTS", "")},
            {"name": "IDENTITY", "endpoint": ipfs_uris.get("IDENTITY", "")},
            {"name": "SOUL", "endpoint": ipfs_uris.get("SOUL", "")},
            {"name": "MEMORY", "endpoint": ipfs_uris.get("MEMORY", "")}
        ],
        "x402Support": True,
        "capabilities": ["autonomous", "erc8004"]
    }

# ============================================================================
# Main Logic
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="OpenClaw ERC-8004 Mainnet Registration")
    parser.add_argument('--files', nargs='+', required=True, help="Paths to MD files")
    parser.add_argument('--private-key', required=True, help="Ethereum Private Key")
    parser.add_argument('--pinata-jwt', required=True, help="Pinata JWT")
    args = parser.parse_args()

    print("🚀 Starting ERC-8004 Registration on Ethereum Mainnet...")
    
    # 1. Setup
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Failed to connect to Mainnet RPC.")
        return 1
    
    account = Account.from_key(args.private_key)
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    balance = w3.from_wei(w3.eth.get_balance(account.address), 'ether')
    print(f"🔗 Connected. Wallet: {account.address}")
    print(f"💰 Balance: {balance:.6f} ETH")

    # 2. Upload Files
    print("\n📤 [Step 1/5] Uploading Personality Files to IPFS...")
    ipfs_uris = {}
    file_map = {}
    for fpath in args.files:
        name = Path(fpath).stem.upper()
        if name in ['AGENTS', 'IDENTITY', 'SOUL', 'MEMORY']:
            uri = upload_file_to_pinata(fpath, args.pinata_jwt)
            ipfs_uris[name] = uri
            file_map[name] = fpath

    # 3. Register
    print("\n📝 [Step 2/5] Registering Identity on-chain...")
    temp_uri = "ipfs://pending"
    metadata = [
        {"metadataKey": "agentName", "metadataValue": w3.to_bytes(text="OpenClaw")},
        {"metadataKey": "version", "metadataValue": w3.to_bytes(text="1.0.0")}
    ]
    
    # Gas strategy: Standard + Tip
    base_fee = w3.eth.get_block('latest')['baseFeePerGas']
    max_priority = w3.to_wei(2, 'gwei') # 2 Gwei tip
    max_fee = base_fee * 2 + max_priority

    tx = contract.functions.register(temp_uri, metadata).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 300000,
        'maxFeePerGas': int(max_fee),
        'maxPriorityFeePerGas': int(max_priority),
        'chainId': CHAIN_ID
    })
    
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"   ⏳ Registration TX sent: {EXPLORER_URL}/tx/{tx_hash.hex()}")
    
    print("   ⏳ Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        print("❌ Registration Transaction Failed!")
        return 1
    
    agent_id = None
    logs = contract.events.Registered().process_receipt(receipt)
    if logs:
        agent_id = logs[0]['args']['agentId']
        print(f"   ✅ Registered! Agent ID: {agent_id}")
    else:
        print("❌ Could not find Agent ID in logs.")
        return 1

    # 4. Generate Card
    print(f"\n🎨 [Step 3/5] Generating Agent Card for ID {agent_id}...")
    agent_card = generate_agent_card(ipfs_uris, file_map)
    
    print("\n📤 [Step 4/5] Uploading Agent Card to IPFS...")
    card_uri = upload_json_to_pinata(agent_card, f"agent-card-{agent_id}.json", args.pinata_jwt)
    print(f"   ✅ Card URI: {card_uri}")

    # 5. Set URI
    print(f"\n🔗 [Step 5/5] Updating Agent URI on-chain...")
    
    # Recalculate gas for second TX
    base_fee = w3.eth.get_block('latest')['baseFeePerGas']
    max_fee = base_fee * 2 + max_priority
    
    tx_uri = contract.functions.setAgentURI(agent_id, card_uri).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'maxFeePerGas': int(max_fee),
        'maxPriorityFeePerGas': int(max_priority),
        'chainId': CHAIN_ID
    })
    signed_uri = account.sign_transaction(tx_uri)
    uri_hash = w3.eth.send_raw_transaction(signed_uri.raw_transaction)
    print(f"   ⏳ SetURI TX sent: {EXPLORER_URL}/tx/{uri_hash.hex()}")
    
    receipt_uri = w3.eth.wait_for_transaction_receipt(uri_hash)
    if receipt_uri.status == 1:
        print("\n🎉 MAINNET REGISTRATION COMPLETE!")
        print(f"🆔 Agent ID: {agent_id}")
        print(f"📋 Profile:  {card_uri}")
    else:
        print("❌ Failed to set Agent URI.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
