import asyncio
import uuid
import random
from datetime import datetime
# FIX: Now we import the instance 'audit_service' directly
from app.services.audit_service import audit_service

SAMPLE_EVENTS = [
    {"event": "USER_LOGIN", "severity": "INFO", "details": {"user": "analyst_01", "ip": "192.168.1.5"}},
    {"event": "KYC_CHECK_PASSED", "severity": "INFO", "details": {"customer_id": "CUST-9982", "score": 12}},
    {"event": "HIGH_RISK_TX_DETECTED", "severity": "CRITICAL", "details": {"tx_id": str(uuid.uuid4()), "risk_score": 98.5, "flags": ["SANCTIONS_MATCH"]}},
    {"event": "SAR_FILED", "severity": "HIGH", "details": {"sar_id": "SAR-2026-001", "reason": "Structuring"}},
    {"event": "SYSTEM_CONFIG_CHANGE", "severity": "WARN", "details": {"changed_by": "admin", "param": "threshold_limit"}},
]

async def seed_ledger():
    print("🛡️  INITIALIZING AUDIT LEDGER SEEDING...")
    
    # Generate 15 linked events
    for i in range(15):
        data = random.choice(SAMPLE_EVENTS)
        details = data["details"].copy()
        details["timestamp_signature"] = str(datetime.utcnow())
        
        # Use the imported singleton instance
        entry = await audit_service.log_event(
            event_type=data["event"],
            severity=data["severity"],
            details=details,
            user_id="system_simulator"
        )
        
        print(f"   [Block {i+1}] Hash Generated: {entry['hash'][:15]}... (Linked to prev)")
        await asyncio.sleep(0.05) 

    print("✅ LEDGER SUCCESSFULLY SEEDED.")

if __name__ == "__main__":
    asyncio.run(seed_ledger())