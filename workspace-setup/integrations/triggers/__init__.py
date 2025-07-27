"""
Trigger system for sales workspace automation
"""

from .base_trigger import BaseTrigger, TriggerCondition
from .customer_triggers import CustomerTrigger, AccountHealthTrigger
from .keyword_triggers import KeywordTrigger, BuyingSignalTrigger, ChurnRiskTrigger
from .metric_triggers import MetricTrigger, UsageDropTrigger

__all__ = [
    'BaseTrigger',
    'TriggerCondition',
    'CustomerTrigger',
    'AccountHealthTrigger',
    'KeywordTrigger',
    'BuyingSignalTrigger',
    'ChurnRiskTrigger',
    'MetricTrigger',
    'UsageDropTrigger',
]