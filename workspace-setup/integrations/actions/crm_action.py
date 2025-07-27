"""
CRM-related actions for triggers
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .base_action import BaseAction, ActionResult, ActionStatus


class UpdateOpportunityAction(BaseAction):
    """Update opportunity records in CRM when triggers fire"""
    
    def __init__(self,
                 action_id: str = "update_opportunity",
                 name: str = "Update Opportunity",
                 description: str = "Update CRM opportunity based on trigger events",
                 crm_api_key: str = "",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.crm_api_key = crm_api_key
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute opportunity update"""
        try:
            customer_id = trigger_data.get("customer_id")
            if not customer_id:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message="No customer_id provided for opportunity update"
                )
            
            # Get opportunity ID for customer
            opportunity_id = await self._get_opportunity_id(customer_id)
            if not opportunity_id:
                return ActionResult(
                    status=ActionStatus.SKIPPED,
                    message=f"No active opportunity found for {customer_id}"
                )
            
            # Determine updates based on trigger
            updates = self._get_opportunity_updates(trigger_data)
            
            # Update the opportunity
            await self._update_crm_opportunity(opportunity_id, updates)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Opportunity {opportunity_id} updated successfully",
                data={"opportunity_id": opportunity_id, "updates": updates}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to update opportunity",
                error=str(e)
            )
    
    def _get_opportunity_updates(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine what updates to make based on trigger"""
        updates = {}
        trigger_id = trigger_data.get("trigger_id", "")
        priority = trigger_data.get("priority", "medium")
        
        # Buying signal triggers
        if "buying_signal" in trigger_id:
            updates.update({
                "stage": "Proposal",
                "probability": 75,
                "next_step": "Prepare and send proposal",
                "notes": f"Buying signal detected: {trigger_data.get('matched_conditions', [])}"
            })
        
        # Churn risk triggers
        elif "churn_risk" in trigger_id:
            updates.update({
                "health_score": "At Risk",
                "next_step": "Emergency retention call",
                "notes": f"Churn risk detected: {trigger_data.get('matched_conditions', [])}"
            })
        
        # Competitive triggers
        elif "competitive" in trigger_id:
            competitor = trigger_data.get("context", {}).get("competitor", "Unknown")
            updates.update({
                "competitor": competitor,
                "next_step": f"Prepare {competitor} competitive materials",
                "notes": f"Competitor {competitor} mentioned in customer communication"
            })
        
        # Security/compliance triggers
        elif "security" in trigger_id or "compliance" in trigger_id:
            updates.update({
                "next_step": "Schedule security/compliance review",
                "notes": f"Security/compliance inquiry: {trigger_data.get('matched_conditions', [])}"
            })
        
        # General updates for all triggers
        updates.update({
            "last_activity": datetime.now().isoformat(),
            "trigger_alert": f"{trigger_id} fired at {trigger_data.get('timestamp')}"
        })
        
        return updates
    
    async def _get_opportunity_id(self, customer_id: str) -> Optional[str]:
        """Get active opportunity ID for customer"""
        # In production, query your CRM API
        await asyncio.sleep(0.1)  # Simulate API call
        
        # Mock opportunity mapping
        opportunity_mapping = {
            "acme_inc": "opp_001",
            "techcorp": "opp_002", 
            "financeapp": "opp_003",
            "medtech_inc": "opp_004"
        }
        
        return opportunity_mapping.get(customer_id)
    
    async def _update_crm_opportunity(self, opportunity_id: str, updates: Dict[str, Any]):
        """Update opportunity in CRM"""
        # In production, make actual CRM API call
        await asyncio.sleep(0.1)  # Simulate API call
        
        print(f"CRM OPPORTUNITY UPDATE:")
        print(f"Opportunity ID: {opportunity_id}")
        print(f"Updates: {updates}")


class CreateTaskAction(BaseAction):
    """Create follow-up tasks in CRM when triggers fire"""
    
    def __init__(self,
                 action_id: str = "create_task",
                 name: str = "Create Task",
                 description: str = "Create CRM tasks based on trigger events",
                 default_assignee: str = "",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.default_assignee = default_assignee
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute task creation"""
        try:
            task_details = self._generate_task_details(trigger_data)
            
            # Create the task
            task_id = await self._create_crm_task(task_details)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Task {task_id} created successfully",
                data={"task_id": task_id, "task_details": task_details}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to create task",
                error=str(e)
            )
    
    def _generate_task_details(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate task details based on trigger"""
        trigger_id = trigger_data.get("trigger_id", "")
        customer_id = trigger_data.get("customer_id", "Unknown")
        priority = trigger_data.get("priority", "medium")
        
        # Base task details
        task = {
            "customer_id": customer_id,
            "priority": priority,
            "created_by": "trigger_system",
            "due_date": self._calculate_due_date(priority),
            "assignee": self._get_assignee(trigger_data)
        }
        
        # Trigger-specific task details
        if "buying_signal" in trigger_id:
            task.update({
                "title": f"Follow up on buying signal - {customer_id}",
                "description": f"Customer showed buying intent: {trigger_data.get('matched_conditions', [])}",
                "type": "sales_followup"
            })
        elif "churn_risk" in trigger_id:
            task.update({
                "title": f"URGENT: Address churn risk - {customer_id}",
                "description": f"Churn risk detected: {trigger_data.get('matched_conditions', [])}",
                "type": "retention_call",
                "priority": "critical"
            })
        elif "competitive" in trigger_id:
            competitor = trigger_data.get("context", {}).get("competitor", "competitor")
            task.update({
                "title": f"Competitive response needed - {customer_id}",
                "description": f"Customer mentioned {competitor}. Prepare competitive materials.",
                "type": "competitive_response"
            })
        elif "security" in trigger_id:
            task.update({
                "title": f"Security inquiry response - {customer_id}",
                "description": f"Customer has security/compliance questions: {trigger_data.get('matched_conditions', [])}",
                "type": "technical_response"
            })
        else:
            task.update({
                "title": f"Follow up on trigger - {customer_id}",
                "description": f"Trigger {trigger_id} fired. Review and take appropriate action.",
                "type": "general_followup"
            })
        
        return task
    
    def _calculate_due_date(self, priority: str) -> str:
        """Calculate task due date based on priority"""
        now = datetime.now()
        
        if priority == "critical":
            due_date = now + timedelta(hours=2)
        elif priority == "high":
            due_date = now + timedelta(hours=24)
        elif priority == "medium":
            due_date = now + timedelta(days=2)
        else:
            due_date = now + timedelta(days=7)
        
        return due_date.isoformat()
    
    def _get_assignee(self, trigger_data: Dict[str, Any]) -> str:
        """Determine task assignee"""
        customer_id = trigger_data.get("customer_id")
        trigger_id = trigger_data.get("trigger_id", "")
        
        # Customer-specific assignment
        if customer_id:
            ae_mapping = {
                "acme_inc": "john.doe@company.com",
                "techcorp": "jane.smith@company.com",
                "financeapp": "mike.johnson@company.com"
            }
            return ae_mapping.get(customer_id, self.default_assignee)
        
        # Trigger-specific assignment
        if "churn_risk" in trigger_id:
            return "customer-success@company.com"
        elif "security" in trigger_id:
            return "solutions-engineer@company.com"
        
        return self.default_assignee
    
    async def _create_crm_task(self, task_details: Dict[str, Any]) -> str:
        """Create task in CRM"""
        # In production, make actual CRM API call
        await asyncio.sleep(0.1)  # Simulate API call
        
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"CRM TASK CREATED:")
        print(f"Task ID: {task_id}")
        print(f"Details: {task_details}")
        
        return task_id


class LogActivityAction(BaseAction):
    """Log trigger events as activities in CRM"""
    
    def __init__(self,
                 action_id: str = "log_activity",
                 name: str = "Log Activity",
                 description: str = "Log trigger events as CRM activities",
                 activity_type: str = "trigger_event",
                 enabled: bool = True):
        super().__init__(action_id, name, description, enabled)
        self.activity_type = activity_type
    
    async def _execute_impl(self, trigger_data: Dict[str, Any]) -> ActionResult:
        """Execute activity logging"""
        try:
            activity_details = self._format_activity(trigger_data)
            
            # Log the activity
            activity_id = await self._log_crm_activity(activity_details)
            
            return ActionResult(
                status=ActionStatus.SUCCESS,
                message=f"Activity {activity_id} logged successfully",
                data={"activity_id": activity_id}
            )
            
        except Exception as e:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Failed to log activity",
                error=str(e)
            )
    
    def _format_activity(self, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format trigger data as CRM activity"""
        return {
            "customer_id": trigger_data.get("customer_id"),
            "type": self.activity_type,
            "subject": f"Trigger Alert: {trigger_data.get('trigger_name', 'Unknown')}",
            "description": self._build_activity_description(trigger_data),
            "timestamp": trigger_data.get("timestamp", datetime.now().isoformat()),
            "source": "automation_trigger",
            "priority": trigger_data.get("priority", "medium")
        }
    
    def _build_activity_description(self, trigger_data: Dict[str, Any]) -> str:
        """Build detailed activity description"""
        description = f"""
Trigger Event Details:
- Trigger: {trigger_data.get('trigger_name', 'Unknown')}
- Source: {trigger_data.get('source', 'Unknown')}
- Priority: {trigger_data.get('priority', 'Medium')}

Conditions Met:
{chr(10).join(f"• {condition}" for condition in trigger_data.get('matched_conditions', []))}

Suggested Actions:
{chr(10).join(f"• {action}" for action in trigger_data.get('suggested_actions', []))}

Context:
{trigger_data.get('context', {})}
"""
        return description.strip()
    
    async def _log_crm_activity(self, activity_details: Dict[str, Any]) -> str:
        """Log activity in CRM"""
        # In production, make actual CRM API call
        await asyncio.sleep(0.1)  # Simulate API call
        
        activity_id = f"activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"CRM ACTIVITY LOGGED:")
        print(f"Activity ID: {activity_id}")
        print(f"Customer: {activity_details.get('customer_id')}")
        print(f"Subject: {activity_details.get('subject')}")
        
        return activity_id