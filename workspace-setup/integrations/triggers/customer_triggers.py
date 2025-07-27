"""
Customer-specific triggers for sales automation
"""

from typing import Dict, Any, List
from .base_trigger import BaseTrigger, TriggerResult, TriggerCondition


class CustomerTrigger(BaseTrigger):
    """Trigger for customer-specific events"""
    
    def __init__(self, 
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 customer_ids: List[str],
                 event_types: List[str] = None,
                 enabled: bool = True):
        super().__init__(trigger_id, name, description, priority, enabled)
        self.customer_ids = customer_ids
        self.event_types = event_types or ["mention", "activity", "communication"]
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate customer-specific trigger conditions"""
        matched_conditions = []
        suggested_actions = []
        context = {}
        
        customer_id = data.get("customer_id", "")
        event_type = data.get("event_type", "")
        
        # Check if customer is in our watch list
        if customer_id in self.customer_ids:
            matched_conditions.append(f"customer_match_{customer_id}")
            context["matched_customer"] = customer_id
            suggested_actions.append("notify_account_executive")
        
        # Check event type
        if event_type in self.event_types:
            matched_conditions.append(f"event_type_match_{event_type}")
            context["event_type"] = event_type
        
        # High-value account special handling
        if customer_id in ["acme_inc", "techcorp", "financeapp"]:
            matched_conditions.append("high_value_account")
            suggested_actions.extend(["immediate_notification", "log_to_crm"])
            context["account_tier"] = "high_value"
        
        triggered = len(matched_conditions) > 0
        confidence = self.calculate_confidence(matched_conditions, 3)
        
        return TriggerResult(
            triggered=triggered,
            confidence=confidence,
            matched_conditions=matched_conditions,
            suggested_actions=suggested_actions,
            context=context
        )
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions"""
        return {
            "customer_ids": self.customer_ids,
            "event_types": self.event_types
        }


class AccountHealthTrigger(BaseTrigger):
    """Trigger for account health changes"""
    
    def __init__(self,
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 health_threshold: float = 0.7,
                 usage_drop_threshold: float = -20.0,
                 enabled: bool = True):
        super().__init__(trigger_id, name, description, priority, enabled)
        self.health_threshold = health_threshold
        self.usage_drop_threshold = usage_drop_threshold
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate account health trigger conditions"""
        matched_conditions = []
        suggested_actions = []
        context = {}
        
        # Check health score
        health_score = data.get("health_score", 1.0)
        if health_score < self.health_threshold:
            matched_conditions.append("low_health_score")
            context["health_score"] = health_score
            suggested_actions.append("schedule_health_check")
        
        # Check usage metrics
        usage_change = data.get("usage_change_percent", 0)
        if usage_change < self.usage_drop_threshold:
            matched_conditions.append("significant_usage_drop")
            context["usage_change"] = usage_change
            suggested_actions.extend(["notify_csm", "investigate_usage_drop"])
        
        # Check support ticket volume
        ticket_count = data.get("support_tickets_30d", 0)
        if ticket_count > 5:
            matched_conditions.append("high_support_volume")
            context["ticket_count"] = ticket_count
            suggested_actions.append("escalate_to_support_manager")
        
        # Check payment issues
        payment_failed = data.get("payment_failed", False)
        if payment_failed:
            matched_conditions.append("payment_failure")
            context["payment_status"] = "failed"
            suggested_actions.extend(["notify_billing", "urgent_followup"])
        
        # Check contract renewal timeline
        days_to_renewal = data.get("days_to_renewal", 999)
        if days_to_renewal <= 90:
            matched_conditions.append("renewal_approaching")
            context["days_to_renewal"] = days_to_renewal
            suggested_actions.append("initiate_renewal_process")
        
        triggered = len(matched_conditions) > 0
        confidence = self.calculate_confidence(matched_conditions, 5)
        
        # Boost confidence for critical health indicators
        if health_score < 0.5 or payment_failed:
            confidence = min(confidence + 0.2, 1.0)
        
        return TriggerResult(
            triggered=triggered,
            confidence=confidence,
            matched_conditions=matched_conditions,
            suggested_actions=suggested_actions,
            context=context
        )
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions"""
        return {
            "health_threshold": self.health_threshold,
            "usage_drop_threshold": self.usage_drop_threshold,
            "checks": [
                "health_score",
                "usage_change_percent", 
                "support_tickets_30d",
                "payment_failed",
                "days_to_renewal"
            ]
        }


class NewStakeholderTrigger(BaseTrigger):
    """Trigger when new stakeholders are introduced"""
    
    def __init__(self,
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 enabled: bool = True):
        super().__init__(trigger_id, name, description, priority, enabled)
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate new stakeholder trigger conditions"""
        matched_conditions = []
        suggested_actions = []
        context = {}
        
        # Check for new contact introduction
        new_contact = data.get("new_contact_detected", False)
        if new_contact:
            matched_conditions.append("new_contact_identified")
            context["contact_info"] = data.get("contact_info", {})
            suggested_actions.append("research_new_contact")
        
        # Check for executive level involvement
        contact_level = data.get("contact_level", "").lower()
        if contact_level in ["ceo", "cto", "cio", "cfo", "vp"]:
            matched_conditions.append("executive_level_contact")
            context["executive_level"] = contact_level
            suggested_actions.extend(["notify_ae_manager", "prepare_executive_materials"])
        
        # Check for decision maker signals
        decision_maker_signals = data.get("decision_maker_signals", [])
        if decision_maker_signals:
            matched_conditions.append("decision_maker_identified")
            context["decision_signals"] = decision_maker_signals
            suggested_actions.append("update_buying_committee")
        
        triggered = len(matched_conditions) > 0
        confidence = self.calculate_confidence(matched_conditions, 3)
        
        return TriggerResult(
            triggered=triggered,
            confidence=confidence,
            matched_conditions=matched_conditions,
            suggested_actions=suggested_actions,
            context=context
        )
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions"""
        return {
            "monitors": [
                "new_contact_detected",
                "contact_level",
                "decision_maker_signals"
            ]
        }