from fastapi import APIRouter, HTTPException
from app.services.graph_service import graph_service

router = APIRouter()

@router.get("/health")
def graph_health():
    """Checks if the Neo4j Graph Database is reachable."""
    is_connected = graph_service.check_connection()
    if not is_connected:
        raise HTTPException(status_code=503, detail="Neo4j connection failed")
    return {"status": "connected", "database": "Neo4j"}

@router.get("/rings")
def detect_laundering_rings():
    """
    Returns detected circular money flows (A -> B -> C -> A).
    This is a high-confidence indicator of money laundering.
    """
    try:
        rings = graph_service.detect_circular_flow()
        return {"count": len(rings), "rings": rings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))