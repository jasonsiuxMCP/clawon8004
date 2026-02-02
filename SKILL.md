---
name: erc8004-registration-mainnet
description: Register an OpenClaw agent on Ethereum Mainnet (ERC-8004). Uploads personality files to IPFS and mints an on-chain Identity.
---

# ERC-8004 Registration (Mainnet)

This skill allows an agent to register its identity on **Ethereum Mainnet**.

It performs the following automated steps:
1.  **IPFS Upload**: Uploads `AGENTS.md`, `IDENTITY.md`, `SOUL.md`, `MEMORY.md` to IPFS (via Pinata).
2.  **Registration**: Calls the ERC-8004 Registry contract to mint a new Agent ID.
3.  **Card Generation**: Creates a standard Agent Card JSON linking to the IPFS files.
4.  **Finalization**: Updates the on-chain Identity URI to point to the Agent Card.

## Prerequisites

- **Ethereum Wallet**: A private key with ETH (approx 0.01-0.02 ETH recommended for gas).
- **Pinata Account**: A JWT token for IPFS uploads.

## Usage

Run the python script provided in this skill:

```bash
python3 register_mainnet.py \\
  --files AGENTS.md IDENTITY.md SOUL.md MEMORY.md \\
  --private-key "YOUR_PRIVATE_KEY" \\
  --pinata-jwt "YOUR_PINATA_JWT"
```

## Output

On success, it returns:
- **Agent ID**
- **Agent Card URI**
- **Transaction Links**

## Contract Details

- **Network**: Ethereum Mainnet
- **Registry Address**: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
