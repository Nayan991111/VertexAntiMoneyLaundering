import logging
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.core.config import settings

# Setup simple logger for the "Mock SMTP" & "Webhook"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NotificationService")

class AlertPayload(BaseModel):
    transaction_id: str
    risk_score: float
    flags: List[str]
    details: Dict[str, Any]

class NotificationService:
    def __init__(self):
        self.enabled = settings.ENABLE_EMAIL_NOTIFICATIONS
        self.officer_email = settings.COMPLIANCE_OFFICER_EMAIL
        # In a real scenario, this comes from settings.SLACK_WEBHOOK_URL
        self.webhook_url = "https://hooks.slack.com/services/T00000/B00000/XXXXX"

    async def send_high_risk_alert(self, payload: AlertPayload):
        """
        Orchestrates notifications across Email (Mock SMTP) and Chat (Webhook).
        """
        if not self.enabled:
            return

        # 1. Email Notification
        subject = f"URGENT: High Risk Transaction Detected (Score: {payload.risk_score})"
        body = self._construct_email_body(payload)
        
        await self._mock_smtp_send(
            to_email=self.officer_email,
            subject=subject,
            body=body
        )

        # 2. Webhook Notification (Day 11 Feature)
        await self._send_webhook(payload)

    def _construct_email_body(self, payload: AlertPayload) -> str:
        return f"""
        WARNING: COMPLIANCE THRESHOLD BREACHED
        --------------------------------------
        Transaction ID: {payload.transaction_id}
        Risk Score:     {payload.risk_score} / 100
        Alerts Triggered: {', '.join(payload.flags)}
        
        Action Required: IMMEDIATE REVIEW
        
        Confidential - VertexAntiMoneyLaundering Compliance Engine
        """

    async def _mock_smtp_send(self, to_email: str, subject: str, body: str):
        """
        Simulates sending an email via SMTP.
        """
        # In production, you would use aiosmtplib here.
        logger.warning(f"--- [MOCK EMAIL SENT] ---\nTo: {to_email}\nSubject: {subject}\n{body}\n-----------------------------")

    async def _send_webhook(self, payload: AlertPayload):
        """
        DAY 11 IMPLEMENTATION:
        Constructs a structural payload for Slack/Teams and logs the dispatch.
        """
        # Format for Slack Incoming Webhook
        webhook_payload = {
            "text": f"🚨 High Risk Transaction Detected: {payload.transaction_id}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn", 
                        "text": f"*Risk Score:* {payload.risk_score}\n*Flags:* {', '.join(payload.flags)}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Amount:*\n{payload.details.get('amount', 'N/A')}"},
                        {"type": "mrkdwn", "text": f"*Currency:*\n{payload.details.get('currency', 'USD')}"}
                    ]
                }
            ]
        }
        
        # LOGIC: Mocking the HTTP Request (to avoid crashing without internet/valid URL)
        logger.info(f"🔔 [WEBHOOK TRIGGER] Target: {self.webhook_url}")
        logger.info(f"📦 [PAYLOAD]: {json.dumps(webhook_payload, indent=2)}")
        
        # NOTE FOR PRODUCTION:
        # import httpx
        # async with httpx.AsyncClient() as client:
        #     await client.post(self.webhook_url, json=webhook_payload)

notification_service = NotificationService()