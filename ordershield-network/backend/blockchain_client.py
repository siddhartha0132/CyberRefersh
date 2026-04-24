from typing import List, Dict, Optional
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class BlockchainClient:
    """Client for interacting with FraudLedger smart contract"""
    
    def __init__(self):
        # For demo: use mock mode if no blockchain configured
        self.mock_mode = os.getenv("BLOCKCHAIN_MOCK", "true").lower() == "true"
        
        if not self.mock_mode:
            rpc_url = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            self.contract_address = os.getenv("CONTRACT_ADDRESS")
            self.private_key = os.getenv("PRIVATE_KEY")
            
            # Load contract ABI (simplified for demo)
            self.contract_abi = self._load_contract_abi()
            
            if self.contract_address:
                self.contract = self.w3.eth.contract(
                    address=self.contract_address,
                    abi=self.contract_abi
                )
        else:
            # Mock storage for demo
            self.mock_events = {}
    
    def _load_contract_abi(self):
        """Load contract ABI"""
        # Simplified ABI for demo
        return []
    
    def add_fraud_event(
        self,
        user_hash: str,
        device_hash: str,
        address_hash: str,
        event_type: str,
        risk_score: str,
        event_hash: str
    ) -> Optional[str]:
        """Add fraud event to blockchain"""
        
        if self.mock_mode:
            # Mock implementation
            if user_hash not in self.mock_events:
                self.mock_events[user_hash] = []
            
            self.mock_events[user_hash].append({
                "device_hash": device_hash,
                "address_hash": address_hash,
                "event_type": event_type,
                "risk_score": risk_score,
                "event_hash": event_hash
            })
            
            return f"0xmock{event_hash[:16]}"
        
        # Real blockchain implementation
        try:
            # Convert hashes to bytes32
            user_hash_bytes = bytes.fromhex(user_hash)
            device_hash_bytes = bytes.fromhex(device_hash)
            address_hash_bytes = bytes.fromhex(address_hash)
            event_hash_bytes = bytes.fromhex(event_hash)
            
            # Map risk score to uint8
            risk_score_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
            risk_score_uint = risk_score_map.get(risk_score, 1)
            
            # Build transaction
            account = self.w3.eth.account.from_key(self.private_key)
            
            tx = self.contract.functions.addFraudEvent(
                user_hash_bytes,
                device_hash_bytes,
                address_hash_bytes,
                event_type,
                risk_score_uint,
                event_hash_bytes
            ).build_transaction({
                'from': account.address,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            return tx_hash.hex()
        except Exception as e:
            print(f"Blockchain error: {e}")
            return None
    
    def get_user_events(self, user_hash: str) -> List[Dict]:
        """Get fraud events for a user"""
        
        if self.mock_mode:
            return self.mock_events.get(user_hash, [])
        
        # Real blockchain implementation
        try:
            user_hash_bytes = bytes.fromhex(user_hash)
            events = self.contract.functions.getUserEvents(user_hash_bytes).call()
            return events
        except Exception as e:
            print(f"Blockchain error: {e}")
            return []
