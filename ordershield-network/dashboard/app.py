import streamlit as st
import requests
import json

st.set_page_config(page_title="OrderShield Network", page_icon="🛡️", layout="wide")

API_BASE = "http://localhost:8000"

st.title("🛡️ OrderShield Network")
st.markdown("**Blockchain-backed fraud reputation layer for food delivery platforms**")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Risk Check", "Record Outcome", "Trust Score", "Stats"])

with tab1:
    st.header("Check Fraud Risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        phone = st.text_input("Phone Number", value="9999999999")
        device_id = st.text_input("Device ID", value="device123")
        address = st.text_input("Address", value="123 Main St")
        payment_mode = st.selectbox("Payment Mode", ["COD", "PREPAID"])
        order_amount = st.number_input("Order Amount", value=850.0)
    
    with col2:
        past_orders = st.number_input("Past Orders", value=20, min_value=0)
        past_cancellations = st.number_input("Past Cancellations", value=8, min_value=0)
        past_refunds = st.number_input("Past Refunds", value=5, min_value=0)
        missing_item_claims = st.number_input("Missing Item Claims", value=4, min_value=0)
    
    if st.button("Check Risk", type="primary"):
        payload = {
            "phone": phone,
            "device_id": device_id,
            "address": address,
            "payment_mode": payment_mode,
            "order_amount": order_amount,
            "past_orders": past_orders,
            "past_cancellations": past_cancellations,
            "past_refunds": past_refunds,
            "missing_item_claims": missing_item_claims
        }
        
        try:
            response = requests.post(f"{API_BASE}/risk/check", json=payload)
            result = response.json()
            
            st.success("Risk Check Complete")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
                st.metric("Risk Score", f"{risk_color.get(result['risk_score'], '')} {result['risk_score']}")
            
            with col2:
                st.metric("Risk Points", result['risk_points'])
            
            with col3:
                st.metric("Blockchain Events", result['blockchain_events_found'])
            
            st.info(f"**Decision**: {result['decision'].replace('_', ' ')}")
            
            st.subheader("Risk Factors")
            for reason in result['reasons']:
                st.write(f"• {reason}")
            
            with st.expander("View Hashes"):
                st.code(f"User Hash: {result['user_hash']}")
                st.code(f"Device Hash: {result['device_hash']}")
                st.code(f"Address Hash: {result['address_hash']}")
        
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("Record Order Outcome")
    
    col1, col2 = st.columns(2)
    
    with col1:
        outcome_phone = st.text_input("Phone Number", value="9999999999", key="outcome_phone")
        outcome_device = st.text_input("Device ID", value="device123", key="outcome_device")
        outcome_address = st.text_input("Address", value="123 Main St", key="outcome_address")
    
    with col2:
        event_type = st.selectbox("Event Type", [
            "DELIVERED",
            "CANCELLED",
            "REFUND_REQUESTED",
            "REFUND_ABUSE",
            "FAKE_ORDER",
            "MISSING_ITEM_CLAIM"
        ])
        risk_score = st.selectbox("Risk Score", ["LOW", "MEDIUM", "HIGH"])
        order_id = st.text_input("Order ID", value="ORD123")
    
    if st.button("Record Outcome", type="primary"):
        payload = {
            "phone": outcome_phone,
            "device_id": outcome_device,
            "address": outcome_address,
            "event_type": event_type,
            "risk_score": risk_score,
            "order_id": order_id
        }
        
        try:
            response = requests.post(f"{API_BASE}/order/outcome", json=payload)
            result = response.json()
            
            st.success("Outcome Recorded on Blockchain")
            
            st.code(f"Event Hash: {result['event_hash']}")
            st.code(f"Transaction Hash: {result['tx_hash']}")
            st.info(f"Status: {result['blockchain_status']}")
            st.caption(f"Timestamp: {result['timestamp']}")
        
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.header("Check Trust Score")
    
    user_hash_input = st.text_input("Enter User Hash", placeholder="SHA256 hash of phone number")
    
    if st.button("Get Trust Score", type="primary"):
        try:
            response = requests.get(f"{API_BASE}/trust-score/{user_hash_input}")
            result = response.json()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Trust Score", f"{result['trust_score']}/100")
            
            with col2:
                risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
                st.metric("Risk Level", f"{risk_color.get(result['risk_level'], '')} {result['risk_level']}")
            
            with col3:
                st.metric("Fraud Events", result['events_found'])
            
            st.info(f"Local checks performed: {result['local_checks']}")
        
        except Exception as e:
            st.error(f"Error: {e}")

with tab4:
    st.header("Platform Statistics")
    
    if st.button("Refresh Stats"):
        try:
            response = requests.get(f"{API_BASE}/stats")
            stats = response.json()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Risk Checks", stats['total_risk_checks'])
            
            with col2:
                st.metric("High Risk Users", stats['high_risk_users'])
            
            with col3:
                st.metric("Outcomes Recorded", stats['total_outcomes_recorded'])
        
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# Demo scenarios
with st.expander("📋 Demo Scenarios"):
    st.markdown("""
    ### 1. Genuine User (Low Risk)
    - Phone: 9876543210
    - Past Orders: 50
    - Cancellations: 2
    - Refunds: 1
    - Missing Claims: 0
    - **Expected**: COD allowed, normal order
    
    ### 2. Suspicious User (Medium Risk)
    - Phone: 9999999999
    - Past Orders: 20
    - Cancellations: 8
    - Refunds: 5
    - Missing Claims: 4
    - **Expected**: COD limited, proof required
    
    ### 3. Fraud User (High Risk)
    - Phone: 8888888888
    - Past Orders: 15
    - Cancellations: 12
    - Refunds: 10
    - Missing Claims: 8
    - **Expected**: COD disabled, prepaid mandatory
    """)
