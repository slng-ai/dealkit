"""
Notification actions for triggers
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
from .base_action import BaseAction, ActionResult, ActionStatus


class EmailNotificationAction(BaseAction):
    """Send email notifications when triggers fire"""
    
    def __init__(self,
                 action_id: str = "email_notification",
                 name: str = "Email Notification",
                 description: str = "Send email alerts for trigger events",
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 username: str = "",
                 password: str = "",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute email notification"""
        try:
            recipients = self.get_recipients(trigger_data)
            if not recipients:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="No recipients found for email notification"
                )
            
            subject = self.get_subject(trigger_data)
            message = self.format_message(trigger_data)
            
            # Send email
            await self._send_email(recipients, subject, message)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Email sent to {len(recipients)} recipients",
                data={"recipients": recipients, "subject": subject}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to send email notification",
                error=str(e)
            )
    
    async def _send_email(self, recipients: List[str], subject: str, message: str):
        """Send email using SMTP"""
        # In a real implementation, you'd use proper email service
        # For now, we'll simulate sending
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Log the email (in production, actually send)
        print(f"EMAIL SENT:")
        print(f"To: {', '.join(recipients)}")
        print(f"Subject: {subject}")
        print(f"Message: {message[:100]}...")
    
    def get_recipients(self, trigger_data: Dict[str, Any]) -> List[str]:
        """Get email recipients based on trigger data"""
        recipients = []
        
        # Customer-specific notifications
        customer_id = trigger_data.get("customer_id")
        if customer_id:
            # Get account executive for customer
            ae_email = self._get_ae_email(customer_id)
            if ae_email:
                recipients.append(ae_email)
        
        # Priority-based notifications
        priority = trigger_data.get("priority", "medium")
        if priority == "critical":
            recipients.extend([
                "sales-manager@company.com",
                "cro@company.com"
            ])
        elif priority == "high":
            recipients.append("sales-team@company.com")
        
        # Trigger-specific recipients
        trigger_id = trigger_data.get("trigger_id", "")
        if "churn_risk" in trigger_id:
            recipients.append("customer-success@company.com")
        elif "buying_signal" in trigger_id:
            recipients.append("sales-team@company.com")
        elif "security" in trigger_id:
            recipients.append("security-team@company.com")
        
        return list(set(recipients))  # Remove duplicates
    
    def get_subject(self, trigger_data: Dict[str, Any]) -> str:
        """Generate email subject"""
        trigger_name = trigger_data.get("trigger_name", "Unknown Trigger")
        customer_id = trigger_data.get("customer_id", "Unknown Customer")
        priority = trigger_data.get("priority", "").upper()
        
        priority_prefix = f"[{priority}] " if priority else ""
        
        return f"{priority_prefix}Sales Alert: {trigger_name} - {customer_id}"
    
    def format_message(self, trigger_data: Dict[str, Any]) -> str:
        """Format email message"""
        trigger_name = trigger_data.get("trigger_name", "Unknown")
        customer_id = trigger_data.get("customer_id", "Unknown")
        timestamp = trigger_data.get("timestamp", "Unknown")
        source = trigger_data.get("source", "Unknown")
        
        message = f"""
Sales Alert: {trigger_name}

Customer: {customer_id}
Source: {source}
Time: {timestamp}
Priority: {trigger_data.get("priority", "Medium")}

Details:
{trigger_data.get("matched_conditions", [])}

Context:
{trigger_data.get("context", {})}

Suggested Actions:
{chr(10).join(f"• {action}" for action in trigger_data.get("suggested_actions", []))}

---
This is an automated alert from the Sales Workspace system.
"""
        return message
    
    def _get_ae_email(self, customer_id: str) -> str:
        """Get account executive email for customer"""
        # In production, this would query your CRM
        customer_mapping = {
            "acme_inc": "john.doe@company.com",
            "techcorp": "jane.smith@company.com",
            "financeapp": "mike.johnson@company.com"
        }
        return customer_mapping.get(customer_id, "sales-team@company.com")


class SlackNotificationAction(BaseAction):
    """Send Slack notifications when triggers fire"""
    
    def __init__(self,
                 action_id: str = "slack_notification",
                 name: str = "Slack Notification",
                 description: str = "Send Slack alerts for trigger events",
                 webhook_url: str = "",
                 default_channel: str = "#sales-alerts",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.webhook_url = webhook_url
        self.default_channel = default_channel
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute Slack notification"""
        try:
            channel = self.get_channel(trigger_data)
            message = self.format_slack_message(trigger_data)
            
            # Send to Slack
            await self._send_slack_message(channel, message)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Slack message sent to {channel}",
                data={"channel": channel, "message_preview": message[:100]}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to send Slack notification",
                error=str(e)
            )
    
    async def _send_slack_message(self, channel: str, message: str):
        """Send message to Slack"""
        # In production, use Slack API or webhook
        await asyncio.sleep(0.1)  # Simulate API call
        
        print(f"SLACK MESSAGE SENT:")
        print(f"Channel: {channel}")
        print(f"Message: {message}")
    
    def get_channel(self, trigger_data: Dict[str, Any]) -> str:
        """Get Slack channel based on trigger data"""
        trigger_id = trigger_data.get("trigger_id", "")
        priority = trigger_data.get("priority", "medium")
        
        if priority == "critical":
            return "#sales-critical"
        elif "churn_risk" in trigger_id:
            return "#customer-success"
        elif "buying_signal" in trigger_id:
            return "#sales-hot-leads"
        elif "competitive" in trigger_id:
            return "#competitive-intel"
        elif "security" in trigger_id:
            return "#security-team"
        else:
            return self.default_channel
    
    def format_slack_message(self, trigger_data: Dict[str, Any]) -> str:
        """Format Slack message with rich formatting"""
        trigger_name = trigger_data.get("trigger_name", "Unknown")
        customer_id = trigger_data.get("customer_id", "Unknown")
        priority = trigger_data.get("priority", "medium")
        
        # Priority emoji
        priority_emoji = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "ℹ️",
            "low": "📝"
        }.get(priority, "ℹ️")
        
        message = f"""
{priority_emoji} *Sales Alert: {trigger_name}*

*Customer:* {customer_id}
*Priority:* {priority.upper()}
*Source:* {trigger_data.get("source", "Unknown")}

*Conditions Met:*
{chr(10).join(f"• {condition}" for condition in trigger_data.get("matched_conditions", []))}

*Suggested Actions:*
{chr(10).join(f"• {action}" for action in trigger_data.get("suggested_actions", []))}
"""
        return message


class SMSNotificationAction(BaseAction):
    """Send SMS notifications for critical triggers"""
    
    def __init__(self,
                 action_id: str = "sms_notification",
                 name: str = "SMS Notification",
                 description: str = "Send SMS alerts for critical trigger events",
                 api_key: str = "",
                 phone_numbers: Dict[str, str] = None,
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.api_key = api_key
        self.phone_numbers = phone_numbers or {}
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute SMS notification"""
        try:
            # Only send SMS for critical alerts
            if trigger_data.get("priority") != "critical":
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="SMS only sent for critical priority triggers"
                )
            
            recipients = self.get_sms_recipients(trigger_data)
            if not recipients:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="No SMS recipients configured"
                )
            
            message = self.format_sms_message(trigger_data)
            
            # Send SMS
            await self._send_sms(recipients, message)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"SMS sent to {len(recipients)} recipients",
                data={"recipients": recipients}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to send SMS notification",
                error=str(e)
            )
    
    async def _send_sms(self, recipients: List[str], message: str):
        """Send SMS using SMS service"""
        # In production, use Twilio or similar service
        await asyncio.sleep(0.1)  # Simulate API call
        
        print(f"SMS SENT:")
        print(f"To: {', '.join(recipients)}")
        print(f"Message: {message}")
    
    def get_sms_recipients(self, trigger_data: Dict[str, Any]) -> List[str]:
        """Get SMS recipients for critical alerts"""
        recipients = []
        
        # Always notify sales manager for critical alerts
        if "sales_manager" in self.phone_numbers:
            recipients.append(self.phone_numbers["sales_manager"])
        
        # Customer-specific account executive
        customer_id = trigger_data.get("customer_id")
        if customer_id and customer_id in self.phone_numbers:
            recipients.append(self.phone_numbers[customer_id])
        
        return recipients
    
    def format_sms_message(self, trigger_data: Dict[str, Any]) -> str:
        """Format SMS message (keep it short)"""
        trigger_name = trigger_data.get("trigger_name", "Alert")
        customer_id = trigger_data.get("customer_id", "Unknown")
        
        return f"CRITICAL: {trigger_name} - {customer_id}. Check sales dashboard immediately."