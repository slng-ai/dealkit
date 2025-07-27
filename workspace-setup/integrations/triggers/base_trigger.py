"""
Base trigger class for all trigger types
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class TriggerCondition(Enum):
    """Condition operators for triggers"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    IN_LIST = "in_list"
    NOT_IN_LIST = "not_in_list"
    MATCHES_REGEX = "matches_regex"


@dataclass
class TriggerResult:
    """Result of a trigger evaluation"""
    triggered: bool
    confidence: float  # 0.0 to 1.0
    matched_conditions: List[str]
    suggested_actions: List[str]
    context: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "triggered": self.triggered,
            "confidence": self.confidence,
            "matched_conditions": self.matched_conditions,
            "suggested_actions": self.suggested_actions,
            "context": self.context
        }


class BaseTrigger(ABC):
    """Base class for all triggers"""
    
    def __init__(self, 
                 trigger_id: str,
                 name: str,
                 description: str,
                 priority: str,
                 enabled: bool = True):
        self.trigger_id = trigger_id
        self.name = name
        self.description = description
        self.priority = priority
        self.enabled = enabled
        self.last_triggered: Optional[datetime] = None
        self.trigger_count = 0
        
    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> TriggerResult:
        """
        Evaluate if the trigger conditions are met
        
        Args:
            data: The data to evaluate against trigger conditions
            
        Returns:
            TriggerResult with evaluation details
        """
        pass
    
    @abstractmethod
    def get_conditions(self) -> Dict[str, Any]:
        """Get the trigger conditions"""
        pass
    
    def should_fire(self, data: Dict[str, Any]) -> bool:
        """Check if trigger should fire based on evaluation"""
        if not self.enabled:
            return False
            
        result = self.evaluate(data)
        return result.triggered
    
    def record_trigger(self):
        """Record that this trigger has fired"""
        self.last_triggered = datetime.now()
        self.trigger_count += 1
    
    def reset_stats(self):
        """Reset trigger statistics"""
        self.last_triggered = None
        self.trigger_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get trigger statistics"""
        return {
            "trigger_id": self.trigger_id,
            "name": self.name,
            "enabled": self.enabled,
            "trigger_count": self.trigger_count,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None
        }
    
    def check_condition(self, 
                       value: Any, 
                       condition: TriggerCondition, 
                       target: Any) -> bool:
        """
        Check if a single condition is met
        
        Args:
            value: The value to check
            condition: The condition type
            target: The target value or pattern
            
        Returns:
            True if condition is met
        """
        if condition == TriggerCondition.EQUALS:
            return value == target
        elif condition == TriggerCondition.NOT_EQUALS:
            return value != target
        elif condition == TriggerCondition.CONTAINS:
            return str(target).lower() in str(value).lower()
        elif condition == TriggerCondition.NOT_CONTAINS:
            return str(target).lower() not in str(value).lower()
        elif condition == TriggerCondition.GREATER_THAN:
            return float(value) > float(target)
        elif condition == TriggerCondition.LESS_THAN:
            return float(value) < float(target)
        elif condition == TriggerCondition.GREATER_THAN_OR_EQUAL:
            return float(value) >= float(target)
        elif condition == TriggerCondition.LESS_THAN_OR_EQUAL:
            return float(value) <= float(target)
        elif condition == TriggerCondition.IN_LIST:
            return value in target
        elif condition == TriggerCondition.NOT_IN_LIST:
            return value not in target
        elif condition == TriggerCondition.MATCHES_REGEX:
            import re
            return bool(re.search(target, str(value), re.IGNORECASE))
        
        return False
    
    def calculate_confidence(self, 
                           matched_conditions: List[str], 
                           total_conditions: int) -> float:
        """
        Calculate confidence score based on matched conditions
        
        Args:
            matched_conditions: List of conditions that matched
            total_conditions: Total number of conditions
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if total_conditions == 0:
            return 0.0
            
        base_confidence = len(matched_conditions) / total_conditions
        
        # Boost confidence for certain condition types
        boost = 0.0
        for condition in matched_conditions:
            if "critical" in condition.lower():
                boost += 0.1
            elif "high_priority" in condition.lower():
                boost += 0.05
        
        return min(base_confidence + boost, 1.0)