"""
Trigger Engine for Sales Workspace Automation

This engine monitors various data sources for defined triggers and executes
appropriate actions when conditions are met.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
from pathlib import Path

from .base_integration import BaseIntegration
from .slack.slack_integration import SlackIntegration
from .email.gmail_integration import GmailIntegration
from .gong.gong_integration import GongIntegration
from .granola.granola_integration import GranolaIntegration

logger = logging.getLogger(__name__)


class TriggerPriority(Enum):
    """Priority levels for triggers"""
    CRITICAL = "critical"  # Immediate response required
    HIGH = "high"         # Same day response
    MEDIUM = "medium"     # Next day response
    LOW = "low"          # Weekly digest


class TriggerType(Enum):
    """Types of triggers"""
    CUSTOMER_SPECIFIC = "customer_specific"
    PERSON_SPECIFIC = "person_specific"
    KEYWORD = "keyword"
    METRIC = "metric"
    PATTERN = "pattern"
    THRESHOLD = "threshold"


@dataclass
class TriggerEvent:
    """Represents a detected trigger event"""
    trigger_id: str
    trigger_type: TriggerType
    priority: TriggerPriority
    source: str  # Which integration detected it
    timestamp: datetime
    data: Dict[str, Any]
    customer_id: Optional[str] = None
    person_id: Optional[str] = None
    matched_pattern: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/transmission"""
        return {
            "trigger_id": self.trigger_id,
            "trigger_type": self.trigger_type.value,
            "priority": self.priority.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "customer_id": self.customer_id,
            "person_id": self.person_id,
            "matched_pattern": self.matched_pattern
        }


@dataclass
class TriggerRule:
    """Defines a trigger rule"""
    id: str
    name: str
    description: str
    type: TriggerType
    priority: TriggerPriority
    conditions: Dict[str, Any]
    actions: List[str]
    enabled: bool = True
    cooldown_minutes: int = 0  # Prevent duplicate triggers
    last_triggered: Optional[datetime] = None
    
    def should_trigger(self, event_data: Dict[str, Any]) -> bool:
        """Check if this rule should trigger based on event data"""
        if not self.enabled:
            return False
            
        # Check cooldown
        if self.last_triggered and self.cooldown_minutes > 0:
            cooldown_end = self.last_triggered + timedelta(minutes=self.cooldown_minutes)
            if datetime.now() < cooldown_end:
                return False
        
        # Check conditions based on trigger type
        if self.type == TriggerType.KEYWORD:
            return self._check_keyword_conditions(event_data)
        elif self.type == TriggerType.CUSTOMER_SPECIFIC:
            return self._check_customer_conditions(event_data)
        elif self.type == TriggerType.METRIC:
            return self._check_metric_conditions(event_data)
        # Add more condition checks as needed
        
        return False
    
    def _check_keyword_conditions(self, event_data: Dict[str, Any]) -> bool:
        """Check keyword-based conditions"""
        keywords = self.conditions.get("keywords", [])
        text = event_data.get("text", "").lower()
        
        for keyword in keywords:
            if keyword.lower() in text:
                return True
        
        # Check regex patterns
        patterns = self.conditions.get("patterns", [])
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
                
        return False
    
    def _check_customer_conditions(self, event_data: Dict[str, Any]) -> bool:
        """Check customer-specific conditions"""
        target_customers = self.conditions.get("customer_ids", [])
        event_customer = event_data.get("customer_id")
        
        return event_customer in target_customers
    
    def _check_metric_conditions(self, event_data: Dict[str, Any]) -> bool:
        """Check metric-based conditions"""
        metric_name = self.conditions.get("metric")
        threshold = self.conditions.get("threshold")
        operator = self.conditions.get("operator", "gt")  # gt, lt, eq, gte, lte
        
        metric_value = event_data.get("metrics", {}).get(metric_name)
        if metric_value is None:
            return False
        
        if operator == "gt":
            return metric_value > threshold
        elif operator == "lt":
            return metric_value < threshold
        elif operator == "eq":
            return metric_value == threshold
        elif operator == "gte":
            return metric_value >= threshold
        elif operator == "lte":
            return metric_value <= threshold
        
        return False


class TriggerEngine:
    """Main trigger engine that coordinates monitoring and actions"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.rules: List[TriggerRule] = []
        self.integrations: Dict[str, BaseIntegration] = {}
        self.action_handlers: Dict[str, Callable] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.processed_events: List[TriggerEvent] = []
        self.running = False
        
        # Load configuration
        if config_path:
            self.load_config(config_path)
        
        # Initialize integrations
        self._init_integrations()
        
        # Load trigger rules from markdown file
        self._load_trigger_rules()
    
    def _init_integrations(self):
        """Initialize available integrations"""
        # These would be configured based on environment
        self.integrations = {
            # "slack": SlackIntegration(),
            # "email": GmailIntegration(),
            # "gong": GongIntegration(),
            # "granola": GranolaIntegration(),
        }
    
    def _load_trigger_rules(self):
        """Load trigger rules from the triggers.md file"""
        triggers_path = Path(__file__).parent.parent / "personal" / "triggers.md"
        
        # For now, we'll define some example rules
        # In production, these would be parsed from the markdown file
        self.rules = [
            TriggerRule(
                id="high_value_account_mention",
                name="High Value Account Mention",
                description="Trigger when high-value accounts are mentioned",
                type=TriggerType.CUSTOMER_SPECIFIC,
                priority=TriggerPriority.HIGH,
                conditions={
                    "customer_ids": ["acme_inc", "techcorp", "financeapp"]
                },
                actions=["notify_ae", "log_to_crm", "add_to_report"]
            ),
            TriggerRule(
                id="churn_risk_keywords",
                name="Churn Risk Keywords",
                description="Detect potential churn risk from keywords",
                type=TriggerType.KEYWORD,
                priority=TriggerPriority.CRITICAL,
                conditions={
                    "keywords": ["cancel", "terminate", "disappointed", "frustrated", "switching"],
                    "patterns": [r"considering\s+alternatives", r"not\s+meeting\s+.*\s+needs"]
                },
                actions=["immediate_alert", "notify_manager", "create_save_task"]
            ),
            TriggerRule(
                id="buying_signals",
                name="Buying Signals",
                description="Detect buying intent signals",
                type=TriggerType.KEYWORD,
                priority=TriggerPriority.HIGH,
                conditions={
                    "keywords": ["budget approved", "looking for a solution", "need something by"],
                    "patterns": [r"what\s+would\s+it\s+take", r"can\s+acme\s+handle"]
                },
                actions=["notify_ae", "schedule_demo", "update_opportunity"]
            ),
            TriggerRule(
                id="usage_drop",
                name="Usage Drop Alert",
                description="Alert when customer usage drops significantly",
                type=TriggerType.METRIC,
                priority=TriggerPriority.HIGH,
                conditions={
                    "metric": "usage_change_percent",
                    "threshold": -20,
                    "operator": "lt"
                },
                actions=["notify_csm", "health_score_update", "schedule_checkin"],
                cooldown_minutes=1440  # Once per day
            )
        ]
    
    def register_action_handler(self, action_name: str, handler: Callable):
        """Register an action handler"""
        self.action_handlers[action_name] = handler
    
    async def process_event(self, source: str, event_data: Dict[str, Any]):
        """Process an incoming event from an integration"""
        # Check all rules against this event
        for rule in self.rules:
            if rule.should_trigger(event_data):
                trigger_event = TriggerEvent(
                    trigger_id=rule.id,
                    trigger_type=rule.type,
                    priority=rule.priority,
                    source=source,
                    timestamp=datetime.now(),
                    data=event_data,
                    customer_id=event_data.get("customer_id"),
                    person_id=event_data.get("person_id"),
                    matched_pattern=rule.name
                )
                
                # Add to queue for processing
                await self.event_queue.put(trigger_event)
                
                # Update last triggered time
                rule.last_triggered = datetime.now()
                
                logger.info(f"Trigger fired: {rule.name} from {source}")
    
    async def _process_trigger_queue(self):
        """Process triggers from the queue"""
        while self.running:
            try:
                # Wait for trigger events with timeout
                trigger_event = await asyncio.wait_for(
                    self.event_queue.get(), 
                    timeout=1.0
                )
                
                # Find the rule that created this trigger
                rule = next((r for r in self.rules if r.id == trigger_event.trigger_id), None)
                if not rule:
                    continue
                
                # Execute actions
                for action_name in rule.actions:
                    handler = self.action_handlers.get(action_name)
                    if handler:
                        try:
                            await handler(trigger_event)
                        except Exception as e:
                            logger.error(f"Error executing action {action_name}: {e}")
                
                # Store processed event
                self.processed_events.append(trigger_event)
                
                # Limit stored events
                if len(self.processed_events) > 10000:
                    self.processed_events = self.processed_events[-5000:]
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing trigger queue: {e}")
    
    async def monitor_slack(self, interval_seconds: int = 60):
        """Monitor Slack for triggers"""
        slack = self.integrations.get("slack")
        if not slack:
            return
            
        while self.running:
            try:
                # Fetch recent messages
                messages = await slack.fetch_recent_messages()
                for message in messages:
                    await self.process_event("slack", message)
                    
            except Exception as e:
                logger.error(f"Error monitoring Slack: {e}")
            
            await asyncio.sleep(interval_seconds)
    
    async def monitor_email(self, interval_seconds: int = 300):
        """Monitor email for triggers"""
        email = self.integrations.get("email")
        if not email:
            return
            
        while self.running:
            try:
                # Fetch recent emails
                emails = await email.fetch_recent_emails()
                for email_data in emails:
                    await self.process_event("email", email_data)
                    
            except Exception as e:
                logger.error(f"Error monitoring email: {e}")
            
            await asyncio.sleep(interval_seconds)
    
    async def start(self):
        """Start the trigger engine"""
        self.running = True
        
        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._process_trigger_queue()),
            asyncio.create_task(self.monitor_slack(60)),  # Every minute
            asyncio.create_task(self.monitor_email(300)),  # Every 5 minutes
            # Add more monitoring tasks as needed
        ]
        
        logger.info("Trigger engine started")
        
        # Wait for all tasks
        await asyncio.gather(*tasks)
    
    def stop(self):
        """Stop the trigger engine"""
        self.running = False
        logger.info("Trigger engine stopped")
    
    def get_trigger_stats(self) -> Dict[str, Any]:
        """Get statistics about triggered events"""
        stats = {
            "total_triggers": len(self.processed_events),
            "triggers_by_priority": {},
            "triggers_by_type": {},
            "triggers_by_source": {},
            "recent_triggers": []
        }
        
        for event in self.processed_events:
            # Count by priority
            priority = event.priority.value
            stats["triggers_by_priority"][priority] = stats["triggers_by_priority"].get(priority, 0) + 1
            
            # Count by type
            trigger_type = event.trigger_type.value
            stats["triggers_by_type"][trigger_type] = stats["triggers_by_type"].get(trigger_type, 0) + 1
            
            # Count by source
            source = event.source
            stats["triggers_by_source"][source] = stats["triggers_by_source"].get(source, 0) + 1
        
        # Add recent triggers
        stats["recent_triggers"] = [
            event.to_dict() for event in self.processed_events[-10:]
        ]
        
        return stats
    
    def load_config(self, config_path: str):
        """Load configuration from file"""
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Process configuration
            pass
    
    def save_state(self, filepath: str):
        """Save engine state for recovery"""
        state = {
            "processed_events": [e.to_dict() for e in self.processed_events[-1000:]],
            "rule_states": [
                {
                    "id": rule.id,
                    "last_triggered": rule.last_triggered.isoformat() if rule.last_triggered else None,
                    "enabled": rule.enabled
                }
                for rule in self.rules
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)


# Example usage
if __name__ == "__main__":
    async def example_action_handler(event: TriggerEvent):
        """Example action handler"""
        print(f"Trigger fired: {event.trigger_id} - {event.data}")
    
    async def main():
        engine = TriggerEngine()
        
        # Register action handlers
        engine.register_action_handler("notify_ae", example_action_handler)
        engine.register_action_handler("immediate_alert", example_action_handler)
        
        # Start engine
        await engine.start()
    
    asyncio.run(main())