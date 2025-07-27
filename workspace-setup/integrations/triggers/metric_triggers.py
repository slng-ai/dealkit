"""
Metric-based triggers for sales automation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base_trigger import BaseTrigger, TriggerResult, TriggerCondition


class MetricTrigger(BaseTrigger):
    """Base class for metric-based triggers"""
    
    def __init__(self,
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 metric_name: str,
                 threshold: float,
                 condition: TriggerCondition,
                 time_window_hours: int = 24,
                 enabled: bool = True):
        super().__init__(trigger_id, name, description, priority, enabled)
        self.metric_name = metric_name
        self.threshold = threshold
        self.condition = condition
        self.time_window_hours = time_window_hours
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate metric trigger conditions"""
        matched_conditions = []
        suggested_actions = []
        context = {}
        
        # Get metric value
        metrics = data.get("metrics", {})
        current_value = metrics.get(self.metric_name)
        
        if current_value is None:
            return TriggerResult(
                triggered=False,
                confidence=0.0,
                matched_conditions=[],
                suggested_actions=[],
                context={"error": f"Metric {self.metric_name} not found"}
            )
        
        # Check threshold condition
        threshold_met = self.check_condition(current_value, self.condition, self.threshold)
        
        if threshold_met:
            matched_conditions.append(f"threshold_{self.condition.value}")
            context[self.metric_name] = current_value
            context["threshold"] = self.threshold
            context["condition"] = self.condition.value
        
        # Add trend analysis if historical data available
        historical_values = metrics.get(f"{self.metric_name}_history", [])
        if historical_values:
            trend = self._analyze_trend(historical_values)
            context["trend"] = trend
            
            if trend["direction"] == "declining" and trend["severity"] > 0.5:
                matched_conditions.append("declining_trend")
                suggested_actions.append("investigate_decline")
        
        triggered = len(matched_conditions) > 0
        confidence = self.calculate_confidence(matched_conditions, 2)
        
        return TriggerResult(
            triggered=triggered,
            confidence=confidence,
            matched_conditions=matched_conditions,
            suggested_actions=suggested_actions,
            context=context
        )
    
    def _analyze_trend(self, values: List[float]) -> Dict[str, Any]:
        """Analyze trend in metric values"""
        if len(values) < 2:
            return {"direction": "unknown", "severity": 0.0}
        
        # Simple trend analysis
        recent_avg = sum(values[-3:]) / min(3, len(values))
        older_avg = sum(values[:-3]) / max(1, len(values) - 3) if len(values) > 3 else values[0]
        
        change_percent = ((recent_avg - older_avg) / older_avg) * 100 if older_avg != 0 else 0
        
        if change_percent > 10:
            direction = "improving"
        elif change_percent < -10:
            direction = "declining"
        else:
            direction = "stable"
        
        severity = min(abs(change_percent) / 50, 1.0)  # Normalize to 0-1
        
        return {
            "direction": direction,
            "severity": severity,
            "change_percent": change_percent,
            "recent_average": recent_avg,
            "older_average": older_avg
        }
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions"""
        return {
            "metric_name": self.metric_name,
            "threshold": self.threshold,
            "condition": self.condition.value,
            "time_window_hours": self.time_window_hours
        }


class UsageDropTrigger(MetricTrigger):
    """Trigger for significant usage drops"""
    
    def __init__(self,
                 trigger_id: str = "usage_drop",
                 name: str = "Usage Drop Alert",
                 description: str = "Alerts when customer usage drops significantly",
                 priority: str = "high",
                 drop_threshold: float = -20.0,
                 enabled: bool = True):
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            metric_name="usage_change_percent",
            threshold=drop_threshold,
            condition=TriggerCondition.LESS_THAN,
            time_window_hours=24,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate usage drop trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add usage drop specific actions
            result.suggested_actions.extend([
                "notify_csm",
                "schedule_health_check",
                "investigate_usage_pattern",
                "check_technical_issues"
            ])
            
            # Severe drops get escalated
            usage_change = result.context.get("usage_change_percent", 0)
            if usage_change < -50:
                result.suggested_actions.append("escalate_to_manager")
                result.priority = "critical"
                result.confidence = min(result.confidence + 0.3, 1.0)
        
        return result


class EngagementScoreTrigger(MetricTrigger):
    """Trigger for low engagement scores"""
    
    def __init__(self,
                 trigger_id: str = "low_engagement",
                 name: str = "Low Engagement Score",
                 description: str = "Alerts when customer engagement score drops",
                 priority: str = "medium",
                 score_threshold: float = 0.3,
                 enabled: bool = True):
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            metric_name="engagement_score",
            threshold=score_threshold,
            condition=TriggerCondition.LESS_THAN,
            time_window_hours=72,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate engagement score trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add engagement specific actions
            result.suggested_actions.extend([
                "plan_engagement_campaign",
                "send_check_in_email",
                "offer_training_session",
                "review_onboarding_progress"
            ])
            
            # Very low engagement needs immediate attention
            engagement_score = result.context.get("engagement_score", 1.0)
            if engagement_score < 0.2:
                result.suggested_actions.append("immediate_outreach")
                result.priority = "high"
        
        return result


class SupportTicketVolumeTrigger(MetricTrigger):
    """Trigger for high support ticket volume"""
    
    def __init__(self,
                 trigger_id: str = "high_support_volume",
                 name: str = "High Support Ticket Volume",
                 description: str = "Alerts when support ticket volume is unusually high",
                 priority: str = "medium",
                 ticket_threshold: int = 5,
                 enabled: bool = True):
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            metric_name="support_tickets_30d",
            threshold=ticket_threshold,
            condition=TriggerCondition.GREATER_THAN,
            time_window_hours=24,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate support ticket volume trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add support volume specific actions
            result.suggested_actions.extend([
                "notify_support_manager",
                "analyze_ticket_patterns",
                "schedule_customer_call",
                "review_product_issues"
            ])
            
            # Very high volume indicates serious issues
            ticket_count = result.context.get("support_tickets_30d", 0)
            if ticket_count > 10:
                result.suggested_actions.extend([
                    "escalate_to_product_team",
                    "emergency_customer_review"
                ])
                result.priority = "high"
        
        return result


class RevenueAtRiskTrigger(MetricTrigger):
    """Trigger for revenue at risk conditions"""
    
    def __init__(self,
                 trigger_id: str = "revenue_at_risk",
                 name: str = "Revenue at Risk",
                 description: str = "Alerts when revenue is at risk",
                 priority: str = "critical",
                 risk_threshold: float = 0.7,
                 enabled: bool = True):
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            metric_name="churn_risk_score",
            threshold=risk_threshold,
            condition=TriggerCondition.GREATER_THAN,
            time_window_hours=24,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate revenue at risk trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add revenue protection specific actions
            result.suggested_actions.extend([
                "alert_revenue_team",
                "prepare_retention_plan",
                "schedule_executive_call",
                "review_contract_terms"
            ])
            
            # Calculate revenue impact
            customer_value = data.get("customer_value", {})
            arr = customer_value.get("annual_recurring_revenue", 0)
            
            if arr > 100000:  # High-value customer
                result.suggested_actions.extend([
                    "escalate_to_c_level",
                    "prepare_executive_briefing"
                ])
                result.context["revenue_impact"] = "high"
                result.confidence = 1.0
            
            result.context["arr_at_risk"] = arr
        
        return result


class PerformanceIssueTrigger(MetricTrigger):
    """Trigger for performance-related issues"""
    
    def __init__(self,
                 trigger_id: str = "performance_issue",
                 name: str = "Performance Issue Detection",
                 description: str = "Alerts when performance metrics indicate issues",
                 priority: str = "high",
                 response_time_threshold: float = 2000,  # milliseconds
                 enabled: bool = True):
        super().__init__(
            trigger_id=trigger_id,
            name=name,
            description=description,
            priority=priority,
            metric_name="avg_response_time_ms",
            threshold=response_time_threshold,
            condition=TriggerCondition.GREATER_THAN,
            time_window_hours=1,
            enabled=enabled
        )
    
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """Evaluate performance issue trigger conditions"""
        result = super().evaluate(data)
        
        if result.triggered:
            # Add performance issue specific actions
            result.suggested_actions.extend([
                "notify_engineering",
                "check_infrastructure",
                "proactive_customer_communication",
                "monitor_customer_impact"
            ])
            
            # Severe performance issues
            response_time = result.context.get("avg_response_time_ms", 0)
            if response_time > 5000:  # 5 seconds
                result.suggested_actions.extend([
                    "escalate_to_sre",
                    "prepare_incident_response"
                ])
                result.priority = "critical"
        
        return result