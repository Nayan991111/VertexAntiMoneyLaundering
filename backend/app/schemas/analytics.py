from pydantic import BaseModel
from typing import List, Dict, Optional

class RiskDistribution(BaseModel):
    reason: str
    count: int

class DailyStats(BaseModel):
    date: str
    total_transactions: int
    total_volume: float
    blocked_count: int
    blocked_volume: float

class DashboardMetrics(BaseModel):
    total_transactions: int
    total_volume: float
    avg_risk_score: float
    
    # Critical Compliance Metrics
    blocked_transactions: int
    blocked_volume: float
    block_rate_percentage: float
    
    # Drill-down
    risk_distribution: List[RiskDistribution]
    recent_alerts: List[Dict] # Simplified for the feed