import time
import random
import requests
import uuid
from datetime import datetime


API_URL = "http://localhost:8000/api/v1/transactions/"
HEADERS = {"Content-Type": "application/json"}


NAMES = ["Nayan", "Vikram", "Aditya", "Rohan", "Sanya", "Kavya", "Offshore_Entity_A", "Shell_Corp_X"]
FLAGS = ["US", "IN", "UK", "AE", "KY", "PA"] 

def generate_random_transaction():
    """Generates a normal, boring transaction."""
    sender = random.choice(NAMES)
    receiver = random.choice([n for n in NAMES if n != sender])
    
    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": round(random.uniform(100.0, 5000.0), 2),
        "currency": "USD",
        "sender_account_id": f"ACC_{sender.upper()}",
        "receiver_account_id": f"ACC_{receiver.upper()}",
        "timestamp": datetime.now().isoformat(),
        "notes": "General transfer",
        "is_simulated": True
    }

def generate_laundering_loop():
    """Injects a sophisticated 'Red Ring' (A -> B -> C -> A)."""
    print("⚠️  INJECTING MONEY LAUNDERING LOOP...")
    loop_id = str(uuid.uuid4())[:8]
    
    
    sequence = [
        ("ACC_NAYAN", "ACC_SHELL_CORP_X", 9500),
        ("ACC_SHELL_CORP_X", "ACC_OFFSHORE_A", 9400), 
        ("ACC_OFFSHORE_A", "ACC_NAYAN", 9300)      
    ]
    
    for sender, receiver, amt in sequence:
        payload = {
            "transaction_id": str(uuid.uuid4()),
            "amount": amt,
            "currency": "USD",
            "sender_account_id": sender,
            "receiver_account_id": receiver,
            "timestamp": datetime.now().isoformat(),
            "notes": f"Consulting Fee REF:{loop_id}", 
            "is_simulated": True
        }
        try:
            requests.post(API_URL, json=payload, headers=HEADERS)
            print(f"   🔻 Sent: ${amt} {sender} -> {receiver}")
            time.sleep(0.2) 
        except:
            pass

def main():
    print("🚀 STARTING REAL-TIME TRAFFIC SIMULATION (VertexAML Engine)...")
    print("   Target: http://localhost:8000")
    print("   Press CTRL+C to stop.\n")

    counter = 0
    while True:
        try:
            
            if random.random() > 0.1:
                data = generate_random_transaction()
                requests.post(API_URL, json=data, headers=HEADERS)
                print(f"✅ Normal: ${data['amount']} ({data['sender_account_id']} -> {data['receiver_account_id']})")
            
            
            else:
                generate_laundering_loop()
            
            counter += 1

            time.sleep(random.uniform(0.1, 1.0))

        except Exception as e:
            print(f"❌ Error: {e} (Is the Docker Container running?)")
            time.sleep(2)

if __name__ == "__main__":
    main()