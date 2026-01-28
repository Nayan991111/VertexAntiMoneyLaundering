from typing import Any
from app.rules.base import BaseRule, RuleResult

class StructuringRule(BaseRule):
    rule_name = "Structuring Detection"
    
    # Configurable thresholds
    LOWER_BOUND = 9000.0
    REPORTING_THRESHOLD = 10000.0

    async def check(self, transaction: Any, customer_context: Any = None) -> RuleResult:
        amount = transaction.amount
        
        # Logic: Is it "just below" the radar?
        if self.LOWER_BOUND <= amount < self.REPORTING_THRESHOLD:
            return RuleResult(
                rule_name=self.rule_name,
                triggered=True,
                risk_score=75.0, # High risk
                reason=f"Transaction amount {amount} is just below the reporting threshold of {self.REPORTING_THRESHOLD}. Potential Structuring."
            )
        
        return RuleResult(rule_name=self.rule_name, triggered=False, risk_score=0.0)