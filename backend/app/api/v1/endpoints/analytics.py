from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import DashboardMetrics

router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Get real-time compliance metrics.
    - Total Volume
    - Block Rates
    - Risk Distribution (Sanctions vs. Graph vs. Velocity)
    """
    try:
        metrics = await analytics_service.get_dashboard_metrics(db)
        return metrics
    except Exception as e:
        # In production, log this error securely
        print(f"Analytics Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Analytics engine failure")