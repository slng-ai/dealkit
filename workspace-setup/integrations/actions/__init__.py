"""
Action handlers for trigger automation
"""

from .base_action import BaseAction, ActionResult
from .notification_action import (
    EmailNotificationAction, 
    SlackNotificationAction, 
    SMSNotificationAction
)
from .crm_action import (
    UpdateOpportunityAction, 
    CreateTaskAction, 
    LogActivityAction
)
from .report_action import AddToReportAction, GenerateReportAction
from .workflow_action import (
    ScheduleMeetingAction, 
    CreateFollowupAction, 
    EscalationAction
)

__all__ = [
    'BaseAction',
    'ActionResult',
    'EmailNotificationAction',
    'SlackNotificationAction',
    'SMSNotificationAction',
    'UpdateOpportunityAction',
    'CreateTaskAction',
    'LogActivityAction',
    'AddToReportAction',
    'GenerateReportAction',
    'ScheduleMeetingAction',
    'CreateFollowupAction',
    'EscalationAction',
]