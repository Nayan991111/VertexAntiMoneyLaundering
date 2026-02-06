import requests
import sys
import json
import time

# Script to verify Day 11 "Audit Viewer" Functionality
# Run this inside the backend container: docker-compose exec backend python verify_day11.py

URL = "http://localhost:8000/api/v1/audit/trail"

def verify_audit_endpoint():
    print(f"🔬 Testing Audit Endpoint: {URL}")
    try:
        response = requests.get(URL, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint is REACHABLE.")
            print(f"📊 Retrieved {len(data)} log entries.")
            
            if len(data) > 0:
                latest = data[0]
                print(f"📝 Latest Entry: {latest.get('event_type')} | {latest.get('timestamp')}")
                
                # Check for critical Day 11 fields
                if "hash" in latest and "previous_hash" in latest:
                    print("✅ Schema Verified: SHA-256 Hash chaining fields detected.")
                else:
                    print("❌ Schema Fail: Missing hash fields.")
                    sys.exit(1)
            else:
                print("⚠️  Log is empty. Run 'simulate_traffic.py' to generate data.")
        else:
            print(f"❌ Failed. Status Code: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_audit_endpoint()