from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import hashlib
from datetime import datetime
from risk_engine import RiskEngine
from blockchain_client import BlockchainClient
from database import Database

app = FastAPI(title="OrderShield Network API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
risk_engine = RiskEngine()
blockchain_client = BlockchainClient()
db = Database()

class RiskCheckRequest(BaseModel):
    phone: str
    device_id: str
    address: str
    payment_mode: str
    order_amount: float
    past_orders: int = 0
    past_cancellations: int = 0
    past_refunds: int = 0
    missing_item_claims: int = 0

class OrderOutcomeRequest(BaseModel):
    phone: str
    device_id: str
    address: str
    event_type: str
    risk_score: str
    order_id: str

def hash_data(data: str) -> str:
    """Generate SHA256 hash"""
    return hashlib.sha256(data.encode()).hexdigest()

@app.get("/")
def root():
    return {
        "service": "OrderShield Network",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/risk/check")
def check_risk(request: RiskCheckRequest):
    """Check fraud risk for a user order"""
    
    # Generate hashes
    user_hash = hash_data(request.phone)
    device_hash = hash_data(request.device_id)
    address_hash = hash_data(request.address)
    
    # Query blockchain for past fraud events
    blockchain_events = blockchain_client.get_user_events(user_hash)
    
    # Calculate risk score
    risk_result = risk_engine.calculate_risk(
        past_orders=request.past_orders,
        past_cancellations=request.past_cancellations,
        past_refunds=request.past_refunds,
        missing_item_claims=request.missing_item_claims,
        payment_mode=request.payment_mode,
        order_amount=request.order_amount,
        blockchain_events=blockchain_events
    )
    
    # Store in local database
    db.store_risk_check(
        user_hash=user_hash,
        device_hash=device_hash,
        address_hash=address_hash,
        risk_score=risk_result["risk_score"],
        risk_points=risk_result["risk_points"],
        decision=risk_result["decision"]
    )
    
    return {
        "user_hash": user_hash,
        "device_hash": device_hash,
        "address_hash": address_hash,
        "risk_score": risk_result["risk_score"],
        "risk_points": risk_result["risk_points"],
        "decision": risk_result["decision"],
        "reasons": risk_result["reasons"],
        "blockchain_events_found": len(blockchain_events)
    }

@app.post("/order/outcome")
def record_outcome(request: OrderOutcomeRequest):
    """Record order outcome and store fraud event on blockchain"""
    
    # Generate hashes
    user_hash = hash_data(request.phone)
    device_hash = hash_data(request.device_id)
    address_hash = hash_data(request.address)
    
    # Generate event hash
    event_data = f"{user_hash}{device_hash}{address_hash}{request.event_type}{request.risk_score}{datetime.now().isoformat()}"
    event_hash = hash_data(event_data)
    
    # Store on blockchain
    tx_hash = blockchain_client.add_fraud_event(
        user_hash=user_hash,
        device_hash=device_hash,
        address_hash=address_hash,
        event_type=request.event_type,
        risk_score=request.risk_score,
        event_hash=event_hash
    )
    
    # Store in local database
    db.store_outcome(
        user_hash=user_hash,
        device_hash=device_hash,
        address_hash=address_hash,
        event_type=request.event_type,
        risk_score=request.risk_score,
        order_id=request.order_id,
        event_hash=event_hash,
        tx_hash=tx_hash
    )
    
    return {
        "event_hash": event_hash,
        "blockchain_status": "STORED" if tx_hash else "PENDING",
        "tx_hash": tx_hash,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trust-score/{user_hash}")
def get_trust_score(user_hash: str):
    """Get trust score for a user"""
    
    # Query blockchain
    events = blockchain_client.get_user_events(user_hash)
    
    # Query local database
    local_data = db.get_user_history(user_hash)
    
    # Calculate trust score (0-100, lower is worse)
    trust_score = 100 - min(len(events) * 15, 80)
    
    risk_level = "LOW"
    if trust_score < 40:
        risk_level = "HIGH"
    elif trust_score < 70:
        risk_level = "MEDIUM"
    
    return {
        "user_hash": user_hash,
        "trust_score": trust_score,
        "risk_level": risk_level,
        "events_found": len(events),
        "local_checks": len(local_data)
    }

@app.get("/stats")
def get_stats():
    """Get platform statistics"""
    stats = db.get_stats()
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
