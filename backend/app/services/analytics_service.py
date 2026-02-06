from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.schemas.analytics import DashboardMetrics, RiskDistribution

class AnalyticsService:
    
    async def get_dashboard_metrics(self, db: AsyncSession) -> DashboardMetrics:
        """
        Aggregates core compliance metrics from Postgres.
        Uses DB-side aggregation for O(1) memory usage in Python.
        """
        # 1. Base Aggregates (Total Count, Total Volume)
        total_query = select(
            func.count(Transaction.id),
            func.sum(Transaction.amount),
            func.avg(Transaction.risk_score)
        )
        total_res = await db.execute(total_query)
        total_count, total_vol, avg_score = total_res.first()
        
        # Handle None returns for empty DB
        total_count = total_count or 0
        total_vol = total_vol or 0.0
        avg_score = avg_score or 0.0

        # 2. Blocked Aggregates (Status != 'CLEARED')
        # We assume anything with risk_score >= 80 or status "BLOCKED" is a hit
        blocked_query = select(
            func.count(Transaction.id),
            func.sum(Transaction.amount)
        ).where(Transaction.status == "BLOCKED")
        
        blocked_res = await db.execute(blocked_query)
        blocked_count, blocked_vol = blocked_res.first()
        
        blocked_count = blocked_count or 0
        blocked_vol = blocked_vol or 0.0

        # Calculate Rate
        block_rate = (blocked_count / total_count * 100) if total_count > 0 else 0.0

        # 3. Risk Distribution (Group by Flagged Reason)
        # Why are we blocking people?
        dist_query = select(
            Transaction.flagged_reason,
            func.count(Transaction.id)
        ).where(
            Transaction.status == "BLOCKED"
        ).group_by(
            Transaction.flagged_reason
        ).order_by(desc(func.count(Transaction.id)))
        
        dist_res = await db.execute(dist_query)
        distribution = [
            RiskDistribution(reason=row[0] or "Unknown", count=row[1])
            for row in dist_res.all()
        ]

        # 4. Recent Alerts (Last 5 blocked for the ticker)
        recent_query = select(Transaction).where(
            Transaction.status == "BLOCKED"
        ).order_by(Transaction.timestamp.desc()).limit(5)
        
        recent_res = await db.execute(recent_query)
        recent_alerts = [
            {
                "id": t.transaction_uuid, 
                "counterparty": t.counterparty_name,
                "amount": t.amount,
                "reason": t.flagged_reason
            }
            for t in recent_res.scalars().all()
        ]

        return DashboardMetrics(
            total_transactions=total_count,
            total_volume=total_vol,
            avg_risk_score=avg_score,
            blocked_transactions=blocked_count,
            blocked_volume=blocked_vol,
            block_rate_percentage=block_rate,
            risk_distribution=distribution,
            recent_alerts=recent_alerts
        )

analytics_service = AnalyticsService()