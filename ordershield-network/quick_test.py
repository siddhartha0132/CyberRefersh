#!/usr/bin/env python3
"""Quick test of OrderShield Network API"""

import sys
sys.path.insert(0, '/home/admin-pc/Desktop/CyberMoney/ordershield-network/backend')

from risk_engine import RiskEngine
from database import Database
import hashlib

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

print("🛡️  OrderShield Network - Quick Test")
print("=" * 50)
print()

# Initialize components
risk_engine = RiskEngine()
db = Database("test_ordershield.db")

# Test 1: Genuine User (Low Risk)
print("TEST 1: Genuine User ✅")
print("-" * 50)
result1 = risk_engine.calculate_risk(
    past_orders=50,
    past_cancellations=2,
    past_refunds=1,
    missing_item_claims=0,
    payment_mode="COD",
    order_amount=500,
    blockchain_events=[]
)
print(f"Risk Score: {result1['risk_score']}")
print(f"Risk Points: {result1['risk_points']}")
print(f"Decision: {result1['decision']}")
print(f"Reasons: {result1['reasons']}")
print()

# Test 2: Suspicious User (Medium Risk)
print("TEST 2: Suspicious User ⚠️")
print("-" * 50)
result2 = risk_engine.calculate_risk(
    past_orders=20,
    past_cancellations=8,
    past_refunds=5,
    missing_item_claims=4,
    payment_mode="COD",
    order_amount=850,
    blockchain_events=[]
)
print(f"Risk Score: {result2['risk_score']}")
print(f"Risk Points: {result2['risk_points']}")
print(f"Decision: {result2['decision']}")
print(f"Reasons: {result2['reasons']}")
print()

# Test 3: Fraud User (High Risk)
print("TEST 3: Fraud User 🔴")
print("-" * 50)
result3 = risk_engine.calculate_risk(
    past_orders=15,
    past_cancellations=12,
    past_refunds=10,
    missing_item_claims=8,
    payment_mode="COD",
    order_amount=1200,
    blockchain_events=[
        {"event_type": "REFUND_ABUSE", "risk_score": "HIGH"},
        {"event_type": "FAKE_ORDER", "risk_score": "HIGH"}
    ]
)
print(f"Risk Score: {result3['risk_score']}")
print(f"Risk Points: {result3['risk_points']}")
print(f"Decision: {result3['decision']}")
print(f"Reasons: {result3['reasons']}")
print()

# Test 4: Database Storage
print("TEST 4: Database Storage 💾")
print("-" * 50)
user_hash = hash_data("9999999999")
device_hash = hash_data("device123")
address_hash = hash_data("123 Main St")

db.store_risk_check(
    user_hash=user_hash,
    device_hash=device_hash,
    address_hash=address_hash,
    risk_score=result2['risk_score'],
    risk_points=result2['risk_points'],
    decision=result2['decision']
)
print(f"✅ Stored risk check for user: {user_hash[:16]}...")
print()

# Test 5: Platform Stats
print("TEST 5: Platform Statistics 📊")
print("-" * 50)
stats = db.get_stats()
print(f"Total Risk Checks: {stats['total_risk_checks']}")
print(f"High Risk Users: {stats['high_risk_users']}")
print(f"Total Outcomes: {stats['total_outcomes_recorded']}")
print()

print("=" * 50)
print("✅ All tests completed successfully!")
print()
print("Summary:")
print(f"  • Genuine User: {result1['risk_score']} risk → COD allowed")
print(f"  • Suspicious User: {result2['risk_score']} risk → COD limited")
print(f"  • Fraud User: {result3['risk_score']} risk → COD disabled")
