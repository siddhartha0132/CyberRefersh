# OrderShield Network - Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation Steps

### 1. Backend Setup

```bash
cd ordershield-network

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cd backend
cp .env.example .env
# Edit .env if needed (default uses mock blockchain)
```

### 2. Blockchain Setup

```bash
cd blockchain

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Option A: Run local Hardhat node (in separate terminal)
npx hardhat node

# Option B: Deploy to local node
npx hardhat run scripts/deploy.js --network localhost

# Option C: Deploy to Polygon Mumbai testnet
# First, add your private key and RPC URL to blockchain/.env
npx hardhat run scripts/deploy.js --network mumbai
```

### 3. Update Backend Configuration

After deploying the contract, update `backend/.env`:

```
BLOCKCHAIN_MOCK=false
CONTRACT_ADDRESS=<deployed_contract_address>
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=<your_private_key>
```

### 4. Run Backend API

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API will be available at: http://localhost:8000

### 5. Run Dashboard

```bash
cd dashboard
streamlit run app.py
```

Dashboard will open at: http://localhost:8501

## Testing

### Test Smart Contract

```bash
cd blockchain
npx hardhat test
```

### Test API Endpoints

```bash
# Check risk
curl -X POST http://localhost:8000/risk/check \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "9999999999",
    "device_id": "device123",
    "address": "123 Main St",
    "payment_mode": "COD",
    "order_amount": 850,
    "past_orders": 20,
    "past_cancellations": 8,
    "past_refunds": 5,
    "missing_item_claims": 4
  }'

# Record outcome
curl -X POST http://localhost:8000/order/outcome \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "9999999999",
    "device_id": "device123",
    "address": "123 Main St",
    "event_type": "REFUND_ABUSE",
    "risk_score": "HIGH",
    "order_id": "ORD123"
  }'

# Get trust score
curl http://localhost:8000/trust-score/<user_hash>
```

## Demo Scenarios

Use the dashboard to test these scenarios:

### Scenario 1: Genuine User
- Phone: 9876543210
- Past Orders: 50
- Cancellations: 2
- Refunds: 1
- Missing Claims: 0
- Expected: LOW risk, COD allowed

### Scenario 2: Suspicious User
- Phone: 9999999999
- Past Orders: 20
- Cancellations: 8
- Refunds: 5
- Missing Claims: 4
- Expected: MEDIUM risk, COD limited

### Scenario 3: Fraud User
- Phone: 8888888888
- Past Orders: 15
- Cancellations: 12
- Refunds: 10
- Missing Claims: 8
- Expected: HIGH risk, COD disabled

## Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check port 8000 is available

### Blockchain connection fails
- Set `BLOCKCHAIN_MOCK=true` in backend/.env for demo mode
- Ensure Hardhat node is running if using local blockchain
- Check RPC URL is correct

### Dashboard shows errors
- Ensure backend is running on port 8000
- Check API_BASE URL in dashboard/app.py
- Verify Streamlit is installed: `pip install streamlit`

## Production Deployment

For production:
1. Use PostgreSQL instead of SQLite
2. Deploy contract to Polygon mainnet or Mumbai testnet
3. Add proper authentication and rate limiting
4. Implement ML-based risk scoring
5. Add monitoring and logging
6. Use environment-specific configurations
