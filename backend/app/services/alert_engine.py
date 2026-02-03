from typing import Dict, Any, List
from app.core.config import settings
from app.services.audit_service import audit_logger
from app.services.notification_service import notification_service, AlertPayload

class AlertEngine:
    async def process_transaction_risk(self, transaction_id: str, risk_score: float, risk_flags: List[str], details: Dict[str, Any]):
        """
        Evaluates a transaction's risk score and triggers active interventions.
        """
        
        # 1. ALWAYS Log the decision to the Immutable Audit Trail
        # Even low risk transactions are logged for regulatory completeness
        event_type = "TRANSACTION_RISK_EVALUATION"
        await audit_logger.log_event(
            event_type=event_type,
            actor="SYSTEM_ENGINE",
            risk_score=risk_score,
            details={
                "transaction_id": transaction_id,
                "flags": risk_flags,
                "outcome": "FLAGGED" if risk_score > settings.ALERT_THRESHOLD_SCORE else "CLEARED"
            }
        )

        # 2. Check Threshold for Active Alerting
        if risk_score > settings.ALERT_THRESHOLD_SCORE:
            alert_payload = AlertPayload(
                transaction_id=transaction_id,
                risk_score=risk_score,
                flags=risk_flags,
                details=details
            )
            
            # Fire and forget (asynchronous)
            await notification_service.send_high_risk_alert(alert_payload)
            
            return {
                "status": "BLOCKED",
                "action": "ESCALATED_TO_COMPLIANCE",
                "alert_sent": True
            }
        
        return {
            "status": "PROCESSED",
            "action": "NONE",
            "alert_sent": False
        }

alert_engine = AlertEngine()