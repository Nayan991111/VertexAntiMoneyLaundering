from datetime import datetime, timedelta
from typing import Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.rules.base import BaseRule, RuleResult

class VelocityRule(BaseRule):
    rule_name = "Velocity/High Frequency Check"
    
    # Thresholds: More than 3 transactions in 5 minutes
    TIME_WINDOW_MINUTES = 5
    MAX_TRANSACTIONS = 3

    async def check(self, transaction: Any, customer_context: Any = None) -> RuleResult:
        # We need the DB session to check history
        if not customer_context or 'db' not in customer_context:
            return RuleResult(rule_name=self.rule_name, triggered=False, risk_score=0.0)

        db: AsyncSession = customer_context['db']
        customer_id = customer_context.get('customer_id')

        # Define the lookback window
        window_start = datetime.now() - timedelta(minutes=self.TIME_WINDOW_MINUTES)

        # Query: Count EXISTING transactions for this customer in the window
        query = select(func.count(Transaction.id)).where(
            Transaction.customer_id == customer_id,
            Transaction.timestamp >= window_start
        )
        
        result = await db.execute(query)
        count = result.scalar() or 0

        # Logic: If count is ALREADY at threshold, this new one breaks it.
        if count >= self.MAX_TRANSACTIONS:
            return RuleResult(
                rule_name=self.rule_name,
                triggered=True,
                risk_score=60.0, # Medium-High Risk
                reason=f"Velocity High: {count} prior transactions in last {self.TIME_WINDOW_MINUTES} mins."
            )

        return RuleResult(rule_name=self.rule_name, triggered=False, risk_score=0.0)