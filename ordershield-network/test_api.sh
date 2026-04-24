#!/bin/bash

# OrderShield Network API Test Script

API_BASE="http://localhost:8000"

echo "🛡️  OrderShield Network - API Test Suite"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
curl -s $API_BASE/ | jq .
echo ""
echo ""

# Test 2: Genuine User (Low Risk)
echo "Test 2: Genuine User - Low Risk"
curl -s -X POST $API_BASE/risk/check \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "9876543210",
    "device_id": "device_genuine",
    "address": "456 Real Street",
    "payment_mode": "COD",
    "order_amount": 500,
    "past_orders": 50,
    "past_cancellations": 2,
    "past_refunds": 1,
    "missing_item_claims": 0
  }' | jq .
echo ""
echo ""

# Test 3: Suspicious User (Medium Risk)
echo "Test 3: Suspicious User - Medium Risk"
curl -s -X POST $API_BASE/risk/check \
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
  }' | jq .
echo ""
echo ""

# Test 4: Fraud User (High Risk)
echo "Test 4: Fraud User - High Risk"
FRAUD_RESPONSE=$(curl -s -X POST $API_BASE/risk/check \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "8888888888",
    "device_id": "device_fraud",
    "address": "999 Fake Ave",
    "payment_mode": "COD",
    "order_amount": 1200,
    "past_orders": 15,
    "past_cancellations": 12,
    "past_refunds": 10,
    "missing_item_claims": 8
  }')
echo $FRAUD_RESPONSE | jq .
USER_HASH=$(echo $FRAUD_RESPONSE | jq -r .user_hash)
echo ""
echo ""

# Test 5: Record Fraud Outcome
echo "Test 5: Record Fraud Outcome"
curl -s -X POST $API_BASE/order/outcome \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "8888888888",
    "device_id": "device_fraud",
    "address": "999 Fake Ave",
    "event_type": "REFUND_ABUSE",
    "risk_score": "HIGH",
    "order_id": "ORD123"
  }' | jq .
echo ""
echo ""

# Test 6: Get Trust Score
echo "Test 6: Get Trust Score"
curl -s $API_BASE/trust-score/$USER_HASH | jq .
echo ""
echo ""

# Test 7: Platform Stats
echo "Test 7: Platform Statistics"
curl -s $API_BASE/stats | jq .
echo ""
echo ""

echo "✅ All tests completed!"
echo ""
echo "To run this script:"
echo "  chmod +x test_api.sh"
echo "  ./test_api.sh"
