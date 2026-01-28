from app.rules.base import BaseRule, RuleResult
from app.services.watchlist_service import watchlist_service

class WatchlistRule(BaseRule):
    # This ID must match what the RuleEngine expects
    rule_name = "Global Sanctions Screen"

    # METHOD NAME: check (Matches BaseRule)
    async def check(self, transaction, customer_context: dict = None) -> RuleResult:
        # 1. Identify the Target
        target_name = transaction.counterparty_name
        
        # 2. Query the Intelligence Service (RapidFuzz)
        is_hit, match_name, score = watchlist_service.check_sanction(target_name)
        
        # 3. Decision Logic
        if is_hit:
            return RuleResult(
                rule_name=self.rule_name,
                triggered=True,
                # FIX: Changed 'risk_score_impact' to 'risk_score' to match Base definition
                risk_score=100.0,  
                reason=f"SANCTION MATCH: '{target_name}' ~ '{match_name}' (Score: {score:.1f}%)"
            )
            
        return RuleResult(
            rule_name=self.rule_name,
            triggered=False,
            # FIX: Changed 'risk_score_impact' to 'risk_score'
            risk_score=0.0,
            reason="Clear"
        )