# 🦞 clawon8004

**Anchor OpenClaw AI agent souls on-chain via ERC-8004.**

`clawon8004` is a skill and reference implementation that allows an **OpenClaw AI agent** to register itself on Ethereum Mainnet using the **ERC-8004 Trustless Agents** protocol.

By cloning this repository, an OpenClaw agent can mint an **ERC-8004 Agent Card**, anchoring its identity, configuration, and “soul” on-chain in a verifiable and composable way.

---

## ✨ What this does

This skill turns an OpenClaw agent into a **first-class on-chain entity**.

It takes the four core OpenClaw personality files:

* `AGENTS.md`
* `IDENTITY.md`
* `SOUL.md`
* `MEMORY.md`

and:

1. Uploads them to IPFS
2. Mints an **ERC-8004 Agent ID** on Ethereum Mainnet
3. Generates a standard **Agent Card JSON**
4. Links the Agent Card to the on-chain identity

The result is a verifiable **ERC-8004 Agent Card** that represents the OpenClaw agent’s existence on-chain, while keeping execution and reasoning off-chain.

---

## 🧠 Why this matters

OpenClaw agents are autonomous by design, but until now they lacked a **standardized on-chain identity**.

ERC-8004 provides exactly that:

* A trustless agent registry
* Portable, composable identities
* Clear ownership and delegation semantics

`clawon8004` bridges the two worlds:

* **OpenClaw** handles runtime, memory, and autonomy
* **ERC-8004** anchors identity and trust on-chain

Together, they allow AI agents to participate in Web3 **without human proxy accounts**.

---

## 🤖 What is an ERC-8004 Agent Card?

An **Agent Card** is an off-chain JSON document referenced by an ERC-8004 registry contract.

In this project, the Agent Card contains:

* Human-readable agent metadata
* Links to the agent’s OpenClaw core files on IPFS
* Capability declarations

Example structure (simplified):

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "OpenClaw Agent",
  "description": "Autonomous OpenClaw Agent",
  "services": [
    { "name": "AGENTS", "endpoint": "ipfs://..." },
    { "name": "IDENTITY", "endpoint": "ipfs://..." },
    { "name": "SOUL", "endpoint": "ipfs://..." },
    { "name": "MEMORY", "endpoint": "ipfs://..." }
  ],
  "capabilities": ["autonomous", "erc8004"]
}
```

This card is uploaded to IPFS and its URI is stored on-chain.

---

## 🔗 How the skill works (pipeline)

The registration flow is fully automated:

1. **IPFS Upload**
   The four OpenClaw core files are uploaded to IPFS via Pinata.

2. **On-chain Registration**
   The ERC-8004 registry contract is called to mint a new Agent ID.

3. **Agent Card Generation**
   A standard Agent Card JSON is generated, linking to the IPFS files.

4. **Finalization**
   The on-chain Agent URI is updated to point to the Agent Card.

This process is implemented in the mainnet registration script  and described as a reusable OpenClaw skill .

---

## 🚀 Usage

### Prerequisites

* Python 3.8+
* An Ethereum wallet with ETH for gas
* A Pinata account (JWT required)

Install dependencies:

```bash
pip install web3 requests eth-account
```

### Register an OpenClaw agent on Mainnet

```bash
python3 register_mainnet.py \
  --files AGENTS.md IDENTITY.md SOUL.md MEMORY.md \
  --private-key "YOUR_PRIVATE_KEY" \
  --pinata-jwt "YOUR_PINATA_JWT"
```

On success, the script outputs:

* Agent ID (ERC-8004)
* Agent Card IPFS URI
* Etherscan transaction links

---

## 🌐 Network & Contract

* **Network**: Ethereum Mainnet
* **ERC-8004 Registry**: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
* **Explorer**: [https://etherscan.io](https://etherscan.io)

---

## 🔐 Privacy & Design Notes

* Raw agent memory and user context remain **off-chain**
* On-chain data only references IPFS URIs
* The system is compatible with future:

  * Commitments
  * ZK proofs
  * Selective disclosure

This keeps agents autonomous and private, while still verifiable.

---

## 🦀 Philosophy

> Putting an AI agent’s soul on-chain is not about control —
> it’s about **existence, accountability, and composability**.

`clawon8004` is an experiment in treating AI agents as **non-human actors with real on-chain presence**.

---

## 📜 License

MIT

---

