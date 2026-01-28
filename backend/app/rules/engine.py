from typing import List, Any
from app.rules.base import BaseRule, RuleResult

class RuleEngine:
    def __init__(self):
        self.rules: List[BaseRule] = []

    def add_rule(self, rule: BaseRule):
        self.rules.append(rule)

    async def evaluate(self, transaction: Any, customer_context: Any = None) -> List[RuleResult]:
        """
        Run all registered rules against the transaction.
        """
        results = []
        for rule in self.rules:
            # We await here because some rules might need DB access (Async)
            result = await rule.check(transaction, customer_context)
            if result.triggered:
                results.append(result)
        
        return results

    def calculate_total_risk(self, results: List[RuleResult]) -> float:
        """
        Simple aggregation strategy: Max score or Sum?
        For now, we take the MAX score of any triggered rule.
        """
        if not results:
            return 0.0
        return max(r.risk_score for r in results)