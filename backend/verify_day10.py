import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from app.services.alert_engine import alert_engine

async def trigger_manual_alert():
    print("--- [ STARTING DAY 10 VERIFICATION ] ---")
    
    # Simulate a high-risk transaction (Score 95 > 80)
    tx_id = "TXN-MANUAL-VERIFY-001"
    risk_score = 95.0
    flags = ["SANCTION_MATCH_IRAN", "STRUCTURED_DEPOSIT"]
    details = {"amount": 50000, "currency": "USD", "origin": "Tehran"}

    print(f"1. Injecting Transaction {tx_id} with Score {risk_score}...")
    
    result = await alert_engine.process_transaction_risk(
        transaction_id=tx_id,
        risk_score=risk_score,
        risk_flags=flags,
        details=details
    )
    
    print(f"2. Alert Engine Result: {result}")
    
    if result['alert_sent']:
        print("✅ SUCCESS: Email Notification Triggered.")
    else:
        print("❌ FAILURE: Notification NOT Triggered.")

    # Verify Audit Log
    log_path = "logs/audit_trail.jsonl"
    if os.path.exists(log_path):
        print(f"✅ SUCCESS: Audit Log found at {log_path}")
        with open(log_path, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            print(f"3. Last Log Entry:\n{last_line}")
            if "current_hash" in last_line and "previous_hash" in last_line:
                 print("✅ SUCCESS: Cryptographic Linkage Confirmed.")
            else:
                 print("❌ FAILURE: Hashing missing.")
    else:
        print(f"❌ FAILURE: Log file not found at {log_path}. Did you create the logs directory?")

if __name__ == "__main__":
    # Ensure logs dir exists for local run
    if not os.path.exists("logs"):
        os.makedirs("logs")
    asyncio.run(trigger_manual_alert())