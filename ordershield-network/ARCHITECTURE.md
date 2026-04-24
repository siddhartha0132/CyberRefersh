# OrderShield Network - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Food Delivery Apps                        │
│                  (Swiggy, Zomato, Custom Apps)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OrderShield Network API                       │
│                         (FastAPI)                                │
├─────────────────────────────────────────────────────────────────┤
│  • Risk Check Endpoint                                          │
│  • Outcome Recording Endpoint                                   │
│  • Trust Score Query Endpoint                                   │
└───────────┬─────────────────────────────┬───────────────────────┘
            │                             │
            │                             │
            ▼                             ▼
┌───────────────────────┐     ┌──────────────────────────┐
│   Risk Engine         │     │  Blockchain Client       │
│   (Rule-based)        │     │  (Web3.py)               │
├───────────────────────┤     ├──────────────────────────┤
│ • Cancellation ratio  │     │ • Query fraud events     │
│ • Refund ratio        │     │ • Store event hashes     │
│ • Missing item claims │     │ • Get user history       │
│ • Device/address      │     └──────────┬───────────────┘
│   pattern detection   │                │
│ • Blockchain history  │                │
└───────────┬───────────┘                │
            │                            │
            │                            ▼
            │              ┌──────────────────────────┐
            │              │  FraudLedger Contract    │
            │              │  (Solidity)              │
            │              ├──────────────────────────┤
            │              │ • Store event hashes     │
            │              │ • Query user events      │
            │              │ • Event count tracking   │
            │              └──────────────────────────┘
            │                            │
            ▼                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Local Database (SQLite)                     │
├─────────────────────────────────────────────────────────────────┤
│ • Risk check history                                            │
│ • Order outcomes                                                │
│ • Platform statistics                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Risk Check Flow

```
User Order Request
    ↓
Generate Hashes (SHA256)
    ↓
Query Blockchain for Past Events
    ↓
Calculate Risk Score
    ↓
Store in Local DB
    ↓
Return Decision
```

### 2. Outcome Recording Flow

```
Order Outcome
    ↓
Generate Hashes
    ↓
Create Event Hash
    ↓
Store on Blockchain
    ↓
Store in Local DB
    ↓
Return Transaction Hash
```

## Privacy Architecture

### Hash Generation

```python
user_hash = SHA256(phone_number)
device_hash = SHA256(device_id)
address_hash = SHA256(address)
event_hash = SHA256(user_hash + device_hash + address_hash + event_type + risk_score + timestamp)
```

### On-Chain Storage

Only stored on blockchain:
- User hash (bytes32)
- Device hash (bytes32)
- Address hash (bytes32)
- Event type (string)
- Risk score (uint8: 1=LOW, 2=MEDIUM, 3=HIGH)
- Event hash (bytes32)
- Timestamp (uint256)

Never stored on blockchain:
- Phone numbers
- Names
- Full addresses
- Order details
- Payment information

## Risk Scoring Algorithm

### Factors

1. **Cancellation Ratio** (0-30 points)
   - >50%: +30 points
   - >30%: +15 points

2. **Refund Ratio** (0-25 points)
   - >40%: +25 points
   - >20%: +10 points

3. **Missing Item Claims** (0-20 points)
   - >5 claims: +20 points
   - >2 claims: +10 points

4. **Blockchain Events** (0-30 points)
   - >3 events: +30 points
   - >0 events: +15 points

5. **COD High Amount** (0-5 points)
   - COD + >₹1000: +5 points

6. **New User COD** (0-10 points)
   - 0 orders + COD: +10 points

### Risk Levels

- **LOW** (0-29 points): Normal order allowed
- **MEDIUM** (30-59 points): COD limited, proof required
- **HIGH** (60+ points): COD disabled, prepaid mandatory

## Decision Matrix

| Risk Level | COD | Refund | Replacement | Manual Check |
|-----------|-----|--------|-------------|--------------|
| LOW | ✅ | Instant | Allowed | No |
| MEDIUM | Limited | Proof Required | Limited | High Amount |
| HIGH | ❌ | Manual Only | Manual Only | Always |

## Smart Contract Events

```solidity
event FraudEventAdded(
    bytes32 indexed userHash,
    string eventType,
    uint8 riskScore,
    bytes32 eventHash,
    uint256 timestamp
);
```

## API Response Formats

### Risk Check Response
```json
{
  "user_hash": "0x...",
  "device_hash": "0x...",
  "address_hash": "0x...",
  "risk_score": "HIGH",
  "risk_points": 85,
  "decision": "COD_DISABLED_PREPAID_REQUIRED",
  "reasons": ["High cancellation ratio", "Repeated refund claims"],
  "blockchain_events_found": 3
}
```

### Outcome Response
```json
{
  "event_hash": "0x...",
  "blockchain_status": "STORED",
  "tx_hash": "0x...",
  "timestamp": "2024-01-15T10:30:00"
}
```

## Scalability Considerations

1. **Database**: SQLite for demo, PostgreSQL for production
2. **Caching**: Redis for frequent queries
3. **Blockchain**: Layer 2 solutions (Polygon) for lower gas fees
4. **API**: Rate limiting and authentication
5. **ML**: Future enhancement for advanced pattern detection

## Security Measures

1. **Hash-only storage**: No PII on blockchain
2. **One-way hashing**: Cannot reverse engineer user data
3. **Event-based**: Only fraud events recorded
4. **Cross-platform**: Shared intelligence without data sharing
5. **Immutable**: Blockchain ensures tamper-proof records
