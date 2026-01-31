import json
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

router = APIRouter()

# Path to the immutable log
LOG_FILE_PATH = Path("/app/logs/audit_trail.jsonl")

@router.get("/trail", response_model=List[Dict[str, Any]])
async def get_audit_trail():
    """
    Reads the immutable audit trail from disk and returns it structured.
    """
    if not LOG_FILE_PATH.exists():
        logger = logging.getLogger("uvicorn")
        logger.warning("Audit trail file not found.")
        return []

    data = []
    try:
        with open(LOG_FILE_PATH, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        data.append(entry)
                    except json.JSONDecodeError:
                        continue
        # Return most recent first
        return list(reversed(data))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read audit logs: {str(e)}"
        )