# OrderShield Network

**Blockchain-backed fraud reputation layer for food delivery platforms**

## Problem Statement

Food delivery platforms lose millions due to:
- Fake COD orders with repeated cancellations
- Refund abuse and fake "missing item" claims
- Multiple accounts from same device/address
- Fake addresses and unreachable users

## Solution

OrderShield Network creates a cross-platform fraud intelligence layer where food apps can check a user's fraud risk before allowing COD, refunds, or replacements.

**Privacy-First Design**: Only cryptographic hashes stored on blockchain, never raw personal data.

## Architecture

```
User Order → Identity Signals → Hash Generation → Blockchain Query → Risk Scoring → Decision Engine → Outcome Storage
```

## Tech Stack

- **Backend**: FastAPI + Python + Pydantic
- **Database**: SQLite (demo) / PostgreSQL (production)
- **Blockchain**: Solidity + Hardhat + Polygon Mumbai/Amoy testnet
- **Risk Engine**: Rule-based scoring
- **Frontend**: Streamlit dashboard

## Quick Start

### 1. Install Dependencies

```bash
cd ordershield-network
pip install -r requirements.txt
```

### 2. Run Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. Deploy Smart Contract

```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### 4. Run Dashboard

```bash
cd dashboard
streamlit run app.py
```

## API Endpoints

### Check Risk Score
```bash
POST /risk/check
```

### Record Order Outcome
```bash
POST /order/outcome
```

### Get Trust Score
```bash
GET /trust-score/{user_hash}
```

## Demo Scenarios

1. **Genuine User**: Low risk, COD allowed
2. **Suspicious User**: Medium risk, COD limited, proof required
3. **Fraud User**: High risk, COD disabled, prepaid mandatory

## Privacy Guarantee

- Phone numbers → SHA256 hash
- Device IDs → SHA256 hash
- Addresses → SHA256 hash
- Only hashes and fraud events stored on-chain
- No personal data exposed

## Hackathon Pitch

"OrderShield Network prevents repeat scammers from abusing COD, refunds, and cancellations across food delivery apps while preserving user privacy through hash-only blockchain records."
