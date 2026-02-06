import json
import hashlib
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("AuditService")

# Ensure logs directory exists
LOG_DIR = Path("/app/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "audit_trail.jsonl"

class AuditService:
    def __init__(self):
        self.file_path = LOG_FILE
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not self.file_path.exists():
            with open(self.file_path, "w") as f:
                pass  # Create empty file

    def _calculate_hash(self, previous_hash: str, timestamp: str, event_type: str, user_id: str, details: Dict) -> str:
        """
        Creates a SHA-256 hash binding the current entry to the previous one.
        Structure: prev_hash | timestamp | event | user | details_json
        """
        details_str = json.dumps(details, sort_keys=True)
        payload = f"{previous_hash}|{timestamp}|{event_type}|{user_id}|{details_str}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def _get_last_hash(self) -> str:
        """
        Reads the last line of the file to get the previous hash.
        Returns 'GENESIS_HASH' if file is empty.
        """
        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    return "0" * 64  # Genesis Hash (64 zeros)
                
                last_line = lines[-1].strip()
                if not last_line:
                    return "0" * 64
                    
                data = json.loads(last_line)
                return data.get("hash", "0" * 64)
        except Exception:
            return "0" * 64

    async def log_event(self, event_type: str, severity: str, details: Dict[str, Any], user_id: str = "SYSTEM") -> Dict[str, Any]:
        """
        Appends a cryptographically signed entry to the immutable log.
        """
        timestamp = datetime.utcnow().isoformat()
        previous_hash = self._get_last_hash()
        
        current_hash = self._calculate_hash(previous_hash, timestamp, event_type, user_id, details)
        
        entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "severity": severity,
            "user_id": user_id,
            "details": details,
            "previous_hash": previous_hash,
            "hash": current_hash
        }
        
        try:
            with open(self.file_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
            return entry
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
            raise e

# --- SINGLETON INSTANCE EXPORT ---
# This was the missing piece causing imports to fail
audit_service = AuditService()