from typing import Dict, List

class RiskEngine:
    """Rule-based fraud risk scoring engine"""
    
    def calculate_risk(
        self,
        past_orders: int,
        past_cancellations: int,
        past_refunds: int,
        missing_item_claims: int,
        payment_mode: str,
        order_amount: float,
        blockchain_events: List[Dict]
    ) -> Dict:
        """Calculate risk score and decision"""
        
        risk_points = 0
        reasons = []
        
        # Cancellation ratio
        if past_orders > 0:
            cancellation_ratio = past_cancellations / past_orders
            if cancellation_ratio > 0.5:
                risk_points += 30
                reasons.append("High cancellation ratio")
            elif cancellation_ratio > 0.3:
                risk_points += 15
                reasons.append("Moderate cancellation ratio")
        
        # Refund ratio
        if past_orders > 0:
            refund_ratio = past_refunds / past_orders
            if refund_ratio > 0.4:
                risk_points += 25
                reasons.append("Repeated refund claims")
            elif refund_ratio > 0.2:
                risk_points += 10
                reasons.append("Multiple refund requests")
        
        # Missing item claims
        if missing_item_claims > 5:
            risk_points += 20
            reasons.append("Multiple missing item reports")
        elif missing_item_claims > 2:
            risk_points += 10
            reasons.append("Some missing item claims")
        
        # Blockchain fraud events
        blockchain_fraud_count = len(blockchain_events)
        if blockchain_fraud_count > 3:
            risk_points += 30
            reasons.append("Multiple fraud events on blockchain")
        elif blockchain_fraud_count > 0:
            risk_points += 15
            reasons.append("Previous fraud events detected")
        
        # COD with high amount
        if payment_mode == "COD" and order_amount > 1000:
            risk_points += 5
            reasons.append("High-value COD order")
        
        # New user with COD
        if past_orders == 0 and payment_mode == "COD":
            risk_points += 10
            reasons.append("New user attempting COD")
        
        # Determine risk level
        if risk_points >= 60:
            risk_score = "HIGH"
            decision = "COD_DISABLED_PREPAID_REQUIRED"
        elif risk_points >= 30:
            risk_score = "MEDIUM"
            decision = "COD_LIMITED_PROOF_REQUIRED"
        else:
            risk_score = "LOW"
            decision = "NORMAL_ORDER_ALLOWED"
        
        return {
            "risk_score": risk_score,
            "risk_points": risk_points,
            "decision": decision,
            "reasons": reasons if reasons else ["No risk factors detected"]
        }
