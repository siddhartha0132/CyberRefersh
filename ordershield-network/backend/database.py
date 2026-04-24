import sqlite3
from datetime import datetime
from typing import List, Dict

class Database:
    """SQLite database for local storage"""
    
    def __init__(self, db_path: str = "ordershield.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Risk checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_hash TEXT NOT NULL,
                device_hash TEXT NOT NULL,
                address_hash TEXT NOT NULL,
                risk_score TEXT NOT NULL,
                risk_points INTEGER NOT NULL,
                decision TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Outcomes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_hash TEXT NOT NULL,
                device_hash TEXT NOT NULL,
                address_hash TEXT NOT NULL,
                event_type TEXT NOT NULL,
                risk_score TEXT NOT NULL,
                order_id TEXT NOT NULL,
                event_hash TEXT NOT NULL,
                tx_hash TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_risk_check(self, user_hash: str, device_hash: str, address_hash: str,
                        risk_score: str, risk_points: int, decision: str):
        """Store risk check result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO risk_checks (user_hash, device_hash, address_hash, risk_score, risk_points, decision)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_hash, device_hash, address_hash, risk_score, risk_points, decision))
        
        conn.commit()
        conn.close()
    
    def store_outcome(self, user_hash: str, device_hash: str, address_hash: str,
                     event_type: str, risk_score: str, order_id: str,
                     event_hash: str, tx_hash: str):
        """Store order outcome"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO outcomes (user_hash, device_hash, address_hash, event_type, 
                                 risk_score, order_id, event_hash, tx_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_hash, device_hash, address_hash, event_type, risk_score, 
              order_id, event_hash, tx_hash))
        
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_hash: str) -> List[Dict]:
        """Get user history from local database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM risk_checks WHERE user_hash = ?
            ORDER BY timestamp DESC
        """, (user_hash,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]
    
    def get_stats(self) -> Dict:
        """Get platform statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM risk_checks")
        total_checks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM risk_checks WHERE risk_score = 'HIGH'")
        high_risk = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM outcomes")
        total_outcomes = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_risk_checks": total_checks,
            "high_risk_users": high_risk,
            "total_outcomes_recorded": total_outcomes
        }
