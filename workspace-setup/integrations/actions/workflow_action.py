"""
Workflow automation actions for triggers
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .base_action import BaseAction, ActionResult, ActionStatus


class ScheduleMeetingAction(BaseAction):
    """Schedule meetings when triggers fire"""
    
    def __init__(self,
                 action_id: str = "schedule_meeting",
                 name: str = "Schedule Meeting",
                 description: str = "Automatically schedule meetings based on triggers",
                 calendar_api_key: str = "",
                 default_duration: int = 30,
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.calendar_api_key = calendar_api_key
        self.default_duration = default_duration
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute meeting scheduling"""
        try:
            meeting_details = self._generate_meeting_details(trigger_data)
            
            # Only schedule for appropriate triggers
            if not self._should_schedule_meeting(trigger_data):
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="Meeting not appropriate for this trigger type"
                )
            
            # Schedule the meeting
            meeting_id = await self._schedule_calendar_meeting(meeting_details)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Meeting {meeting_id} scheduled successfully",
                data={"meeting_id": meeting_id, "meeting_details": meeting_details}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to schedule meeting",
                error=str(e)
            )
    
    def _should_schedule_meeting(self, trigger_data: Dict[str, Any]) -> bool:
        """Determine if meeting should be scheduled"""
        trigger_id = trigger_data.get("trigger_id", "")
        priority = trigger_data.get("priority", "medium")
        
        # Schedule meetings for critical triggers
        if priority == "critical":
            return True
        
        # Schedule for specific trigger types
        meeting_triggers = [
            "churn_risk",
            "buying_signal", 
            "competitive_mention",
            "security_inquiry",
            "executive_engagement"
        ]
        
        return any(trigger in trigger_id for trigger in meeting_triggers)
    
    def _generate_meeting_details(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate meeting details based on trigger"""
        trigger_id = trigger_data.get("trigger_id", "")
        customer_id = trigger_data.get("customer_id", "Unknown")
        priority = trigger_data.get("priority", "medium")
        
        # Base meeting details
        meeting = {
            "customer_id": customer_id,
            "duration_minutes": self.default_duration,
            "attendees": self._get_attendees(trigger_data),
            "scheduled_by": "trigger_automation"
        }
        
        # Meeting timing based on priority
        if priority == "critical":
            meeting["start_time"] = self._get_next_available_slot(hours_from_now=2)
        elif priority == "high":
            meeting["start_time"] = self._get_next_available_slot(hours_from_now=24)
        else:
            meeting["start_time"] = self._get_next_available_slot(hours_from_now=48)
        
        # Trigger-specific meeting details
        if "churn_risk" in trigger_id:
            meeting.update({
                "title": f"URGENT: Customer Retention Call - {customer_id}",
                "description": f"Emergency call to address churn risk detected by trigger system.\n\nTrigger Details:\n{trigger_data.get('matched_conditions', [])}",
                "type": "retention_call",
                "duration_minutes": 60
            })
        elif "buying_signal" in trigger_id:
            meeting.update({
                "title": f"Sales Opportunity Call - {customer_id}",
                "description": f"Follow up on buying signal detected.\n\nBuying Signals:\n{trigger_data.get('matched_conditions', [])}",
                "type": "sales_call",
                "duration_minutes": 45
            })
        elif "competitive" in trigger_id:
            competitor = trigger_data.get("context", {}).get("competitor", "competitor")
            meeting.update({
                "title": f"Competitive Strategy Call - {customer_id}",
                "description": f"Discuss competitive situation with {competitor}.\n\nDetails:\n{trigger_data.get('matched_conditions', [])}",
                "type": "competitive_review",
                "duration_minutes": 30
            })
        elif "security" in trigger_id:
            meeting.update({
                "title": f"Security/Compliance Review - {customer_id}",
                "description": f"Address security and compliance questions.\n\nInquiry Details:\n{trigger_data.get('matched_conditions', [])}",
                "type": "technical_review",
                "duration_minutes": 45
            })
        else:
            meeting.update({
                "title": f"Customer Check-in - {customer_id}",
                "description": f"Follow up on trigger alert: {trigger_data.get('trigger_name', 'Unknown')}",
                "type": "general_checkin"
            })
        
        return meeting
    
    def _get_attendees(self, trigger_data: Dict[str, Any]) -> List[str]:
        """Get meeting attendees based on trigger"""
        attendees = []
        
        # Customer-specific account executive
        customer_id = trigger_data.get("customer_id")
        if customer_id:
            ae_mapping = {
                "acme_inc": "john.doe@company.com",
                "techcorp": "jane.smith@company.com", 
                "financeapp": "mike.johnson@company.com"
            }
            ae_email = ae_mapping.get(customer_id)
            if ae_email:
                attendees.append(ae_email)
        
        # Trigger-specific attendees
        trigger_id = trigger_data.get("trigger_id", "")
        if "churn_risk" in trigger_id:
            attendees.extend(["customer-success@company.com", "sales-manager@company.com"])
        elif "security" in trigger_id:
            attendees.append("solutions-engineer@company.com")
        elif "competitive" in trigger_id:
            attendees.append("competitive-intel@company.com")
        
        # Priority-based attendees
        priority = trigger_data.get("priority", "medium")
        if priority == "critical":
            attendees.append("sales-manager@company.com")
        
        return list(set(attendees))  # Remove duplicates
    
    def _get_next_available_slot(self, hours_from_now: int = 24) -> str:
        """Get next available meeting slot"""
        # Simple scheduling - in production, check actual calendar availability
        start_time = datetime.now() + timedelta(hours=hours_from_now)
        
        # Round to next business hour (9 AM - 5 PM)
        if start_time.hour < 9:
            start_time = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
        elif start_time.hour >= 17:
            start_time = (start_time + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        
        return start_time.isoformat()
    
    async def _schedule_calendar_meeting(self, meeting_details: Dict[str, Any]) -> str:
        """Schedule meeting in calendar system"""
        # In production, integrate with calendar API (Google Calendar, Outlook, etc.)
        await asyncio.sleep(0.1)  # Simulate API call
        
        meeting_id = f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"MEETING SCHEDULED:")
        print(f"Meeting ID: {meeting_id}")
        print(f"Title: {meeting_details.get('title')}")
        print(f"Start Time: {meeting_details.get('start_time')}")
        print(f"Attendees: {meeting_details.get('attendees', [])}")
        
        return meeting_id


class CreateFollowupAction(BaseAction):
    """Create automated follow-up sequences"""
    
    def __init__(self,
                 action_id: str = "create_followup",
                 name: str = "Create Follow-up",
                 description: str = "Create automated follow-up sequences",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute follow-up creation"""
        try:
            followup_sequence = self._generate_followup_sequence(trigger_data)
            
            # Create the follow-up sequence
            sequence_id = await self._create_followup_sequence(followup_sequence)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Follow-up sequence {sequence_id} created",
                data={"sequence_id": sequence_id, "steps": len(followup_sequence["steps"])}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to create follow-up sequence",
                error=str(e)
            )
    
    def _generate_followup_sequence(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate follow-up sequence based on trigger"""
        trigger_id = trigger_data.get("trigger_id", "")
        customer_id = trigger_data.get("customer_id", "Unknown")
        priority = trigger_data.get("priority", "medium")
        
        sequence = {
            "customer_id": customer_id,
            "trigger_id": trigger_id,
            "priority": priority,
            "steps": []
        }
        
        # Generate steps based on trigger type
        if "buying_signal" in trigger_id:
            sequence["steps"] = [
                {
                    "step": 1,
                    "delay_hours": 2,
                    "action": "send_email",
                    "template": "buying_signal_immediate_followup",
                    "subject": "Great to hear about your interest!"
                },
                {
                    "step": 2,
                    "delay_hours": 24,
                    "action": "send_email",
                    "template": "proposal_offer",
                    "subject": "Proposal for your consideration"
                },
                {
                    "step": 3,
                    "delay_hours": 72,
                    "action": "create_task",
                    "description": "Follow up on proposal response"
                }
            ]
        elif "churn_risk" in trigger_id:
            sequence["steps"] = [
                {
                    "step": 1,
                    "delay_hours": 1,
                    "action": "send_email",
                    "template": "churn_risk_immediate",
                    "subject": "Let's address your concerns"
                },
                {
                    "step": 2,
                    "delay_hours": 24,
                    "action": "schedule_call",
                    "description": "Retention call with customer success"
                },
                {
                    "step": 3,
                    "delay_hours": 48,
                    "action": "send_email",
                    "template": "retention_offer",
                    "subject": "Special offer to continue our partnership"
                }
            ]
        elif "competitive" in trigger_id:
            competitor = trigger_data.get("context", {}).get("competitor", "competitor")
            sequence["steps"] = [
                {
                    "step": 1,
                    "delay_hours": 4,
                    "action": "send_email",
                    "template": "competitive_response",
                    "subject": f"How we compare to {competitor}",
                    "context": {"competitor": competitor}
                },
                {
                    "step": 2,
                    "delay_hours": 24,
                    "action": "send_document",
                    "document": f"{competitor}_battlecard.pdf"
                }
            ]
        else:
            # General follow-up sequence
            sequence["steps"] = [
                {
                    "step": 1,
                    "delay_hours": 24,
                    "action": "send_email",
                    "template": "general_checkin",
                    "subject": "Checking in on your experience"
                }
            ]
        
        return sequence
    
    async def _create_followup_sequence(self, sequence: Dict[str, Any]) -> str:
        """Create follow-up sequence in automation system"""
        await asyncio.sleep(0.1)  # Simulate API call
        
        sequence_id = f"seq_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"FOLLOW-UP SEQUENCE CREATED:")
        print(f"Sequence ID: {sequence_id}")
        print(f"Customer: {sequence.get('customer_id')}")
        print(f"Steps: {len(sequence.get('steps', []))}")
        
        return sequence_id


class EscalationAction(BaseAction):
    """Handle escalation workflows for critical triggers"""
    
    def __init__(self,
                 action_id: str = "escalation",
                 name: str = "Escalation Workflow",
                 description: str = "Escalate critical triggers through management chain",
                 escalation_levels: List[str] = None,
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.escalation_levels = escalation_levels or [
            "account_executive",
            "sales_manager", 
            "sales_director",
            "cro"
        ]
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute escalation workflow"""
        try:
            # Only escalate critical and high priority triggers
            priority = trigger_data.get("priority", "medium")
            if priority not in ["critical", "high"]:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="Escalation only for critical/high priority triggers"
                )
            
            escalation_plan = self._generate_escalation_plan(trigger_data)
            
            # Execute escalation
            escalation_id = await self._execute_escalation(escalation_plan)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Escalation {escalation_id} initiated",
                data={"escalation_id": escalation_id, "levels": len(escalation_plan["levels"])}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to execute escalation",
                error=str(e)
            )
    
    def _generate_escalation_plan(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate escalation plan based on trigger severity"""
        trigger_id = trigger_data.get("trigger_id", "")
        customer_id = trigger_data.get("customer_id", "Unknown")
        priority = trigger_data.get("priority", "medium")
        
        escalation = {
            "customer_id": customer_id,
            "trigger_id": trigger_id,
            "priority": priority,
            "levels": []
        }
        
        # Determine escalation levels based on severity
        if priority == "critical":
            # Critical issues escalate through full chain
            escalation["levels"] = [
                {
                    "level": "immediate",
                    "delay_minutes": 0,
                    "recipients": self._get_immediate_contacts(customer_id),
                    "message_type": "sms_and_email"
                },
                {
                    "level": "manager",
                    "delay_minutes": 15,
                    "recipients": ["sales-manager@company.com"],
                    "message_type": "email_and_slack"
                },
                {
                    "level": "director",
                    "delay_minutes": 60,
                    "recipients": ["sales-director@company.com"],
                    "message_type": "email",
                    "condition": "no_response_from_previous_level"
                }
            ]
        elif priority == "high":
            # High priority goes to manager level
            escalation["levels"] = [
                {
                    "level": "immediate",
                    "delay_minutes": 0,
                    "recipients": self._get_immediate_contacts(customer_id),
                    "message_type": "email"
                },
                {
                    "level": "manager",
                    "delay_minutes": 60,
                    "recipients": ["sales-manager@company.com"],
                    "message_type": "email",
                    "condition": "no_acknowledgment"
                }
            ]
        
        return escalation
    
    def _get_immediate_contacts(self, customer_id: str) -> List[str]:
        """Get immediate contacts for customer"""
        # Customer-specific account executive
        ae_mapping = {
            "acme_inc": "john.doe@company.com",
            "techcorp": "jane.smith@company.com",
            "financeapp": "mike.johnson@company.com"
        }
        
        contacts = [ae_mapping.get(customer_id, "sales-team@company.com")]
        
        # Add customer success for existing customers
        if customer_id in ae_mapping:
            contacts.append("customer-success@company.com")
        
        return contacts
    
    async def _execute_escalation(self, escalation_plan: Dict[str, Any]) -> str:
        """Execute the escalation plan"""
        await asyncio.sleep(0.1)  # Simulate escalation initiation
        
        escalation_id = f"esc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"ESCALATION INITIATED:")
        print(f"Escalation ID: {escalation_id}")
        print(f"Customer: {escalation_plan.get('customer_id')}")
        print(f"Priority: {escalation_plan.get('priority')}")
        print(f"Levels: {len(escalation_plan.get('levels', []))}")
        
        # In production, schedule the escalation steps
        for level in escalation_plan["levels"]:
            print(f"  Level: {level['level']} (delay: {level['delay_minutes']}min)")
        
        return escalation_id