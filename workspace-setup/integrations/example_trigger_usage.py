"""
Example usage of the trigger automation system
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from trigger_engine import TriggerEngine, TriggerEvent, TriggerPriority, TriggerType
from actions import (
    EmailNotificationAction,
    SlackNotificationAction,
    UpdateOpportunityAction,
    CreateTaskAction,
    LogActivityAction,
    AddToReportAction
)


async def setup_trigger_system():
    """Set up and configure the trigger automation system"""
    
    # Initialize trigger engine
    engine = TriggerEngine()
    
    # Register action handlers
    await register_action_handlers(engine)
    
    # Load custom trigger rules
    load_custom_triggers(engine)
    
    return engine


async def register_action_handlers(engine: TriggerEngine):
    """Register all action handlers with the trigger engine"""
    
    # Notification actions
    email_action = EmailNotificationAction(
        smtp_server="smtp.company.com",
        username="alerts@company.com",
        password="secure_password"
    )
    
    slack_action = SlackNotificationAction(
        webhook_url="https://hooks.slack.com/services/xxx",
        default_channel="#sales-alerts"
    )
    
    # CRM actions
    crm_update_action = UpdateOpportunityAction(
        crm_api_key="crm_api_key_here"
    )
    
    task_action = CreateTaskAction(
        default_assignee="sales-team@company.com"
    )
    
    activity_action = LogActivityAction()
    
    # Reporting actions
    report_action = AddToReportAction()
    
    # Register action handlers
    engine.register_action_handler("notify_ae", email_action.execute)
    engine.register_action_handler("notify_ae_immediately", email_action.execute)
    engine.register_action_handler("send_slack_alert", slack_action.execute)
    engine.register_action_handler("update_opportunity", crm_update_action.execute)
    engine.register_action_handler("create_task", task_action.execute)
    engine.register_action_handler("log_to_crm", activity_action.execute)
    engine.register_action_handler("add_to_report", report_action.execute)
    
    # Composite actions
    engine.register_action_handler("immediate_alert", create_immediate_alert_handler(
        email_action, slack_action
    ))
    engine.register_action_handler("full_workflow", create_full_workflow_handler(
        email_action, crm_update_action, task_action, report_action
    ))


def create_immediate_alert_handler(email_action, slack_action):
    """Create composite action for immediate alerts"""
    async def immediate_alert(trigger_data):
        # Send both email and Slack notification
        email_result = await email_action.execute(trigger_data)
        slack_result = await slack_action.execute(trigger_data)
        
        return {
            "email": email_result.to_dict(),
            "slack": slack_result.to_dict()
        }
    
    return immediate_alert


def create_full_workflow_handler(email_action, crm_action, task_action, report_action):
    """Create composite action for full workflow"""
    async def full_workflow(trigger_data):
        results = {}
        
        # Execute all actions in sequence
        results["email"] = await email_action.execute(trigger_data)
        results["crm_update"] = await crm_action.execute(trigger_data)
        results["task_creation"] = await task_action.execute(trigger_data)
        results["report_update"] = await report_action.execute(trigger_data)
        
        return {action: result.to_dict() for action, result in results.items()}
    
    return full_workflow


def load_custom_triggers(engine: TriggerEngine):
    """Load additional custom triggers beyond the default ones"""
    
    # Custom trigger for demo requests
    from triggers.keyword_triggers import KeywordTrigger
    
    demo_request_trigger = KeywordTrigger(
        trigger_id="demo_request",
        name="Demo Request Detection",
        description="Detects when customers request demos",
        priority="high",
        keywords=[
            "demo", "demonstration", "walkthrough", "show me",
            "can you demo", "product demo", "live demo"
        ],
        patterns=[
            r"schedule\s+(a\s+)?demo",
            r"book\s+(a\s+)?demo",
            r"(can|could)\s+you\s+show",
            r"would\s+like\s+to\s+see"
        ]
    )
    
    # Custom trigger for pricing discussions
    pricing_trigger = KeywordTrigger(
        trigger_id="pricing_discussion",
        name="Pricing Discussion",
        description="Detects pricing-related conversations",
        priority="high",
        keywords=[
            "pricing", "cost", "price", "quote", "proposal",
            "how much", "budget", "investment"
        ],
        patterns=[
            r"what\s+(does|would)\s+it\s+cost",
            r"pricing\s+(information|details)",
            r"send\s+(a\s+)?quote",
            r"budget\s+is"
        ]
    )
    
    # Add triggers to engine rules (this would be done differently in production)
    # For demo purposes, we'll add them to the engine's rules list
    print("Custom triggers loaded:")
    print(f"- {demo_request_trigger.name}")
    print(f"- {pricing_trigger.name}")


async def simulate_trigger_events():
    """Simulate various trigger events for demonstration"""
    
    print("🎯 Starting trigger simulation...\n")
    
    # Set up trigger system
    engine = await setup_trigger_system()
    
    # Simulate different types of events
    await simulate_buying_signal_event(engine)
    await simulate_churn_risk_event(engine)
    await simulate_competitive_mention_event(engine)
    await simulate_security_inquiry_event(engine)
    await simulate_usage_drop_event(engine)
    
    print("\n✅ Trigger simulation completed!")
    return engine


async def simulate_buying_signal_event(engine: TriggerEngine):
    """Simulate a buying signal trigger"""
    print("📈 Simulating buying signal event...")
    
    event_data = {
        "customer_id": "acme_inc",
        "source": "email",
        "text": "We're ready to move forward with this project. What would it take to get started by next month?",
        "subject": "Ready to proceed",
        "event_type": "email_received",
        "timestamp": datetime.now().isoformat(),
        "sender": "john.cto@acme.com"
    }
    
    await engine.process_event("email", event_data)
    print("  ✓ Buying signal processed\n")


async def simulate_churn_risk_event(engine: TriggerEngine):
    """Simulate a churn risk trigger"""
    print("🚨 Simulating churn risk event...")
    
    event_data = {
        "customer_id": "techcorp",
        "source": "slack",
        "text": "We're really frustrated with the performance issues and are considering switching to a competitor",
        "event_type": "slack_message",
        "timestamp": datetime.now().isoformat(),
        "channel": "#general",
        "user": "jane.smith"
    }
    
    await engine.process_event("slack", event_data)
    print("  ✓ Churn risk processed\n")


async def simulate_competitive_mention_event(engine: TriggerEngine):
    """Simulate a competitive mention trigger"""
    print("⚔️ Simulating competitive mention event...")
    
    event_data = {
        "customer_id": "financeapp",
        "source": "gong",
        "text": "We're comparing you with Vercel and they seem to have better pricing",
        "event_type": "call_transcript",
        "timestamp": datetime.now().isoformat(),
        "call_id": "call_12345"
    }
    
    await engine.process_event("gong", event_data)
    print("  ✓ Competitive mention processed\n")


async def simulate_security_inquiry_event(engine: TriggerEngine):
    """Simulate a security inquiry trigger"""
    print("🔒 Simulating security inquiry event...")
    
    event_data = {
        "customer_id": "medtech_inc",
        "source": "email",
        "text": "Can you provide HIPAA compliance documentation and SOC2 reports for our security audit?",
        "subject": "Security compliance documentation needed",
        "event_type": "email_received",
        "timestamp": datetime.now().isoformat()
    }
    
    await engine.process_event("email", event_data)
    print("  ✓ Security inquiry processed\n")


async def simulate_usage_drop_event(engine: TriggerEngine):
    """Simulate a usage drop trigger"""
    print("📉 Simulating usage drop event...")
    
    event_data = {
        "customer_id": "startup_unicorn",
        "source": "metrics",
        "metrics": {
            "usage_change_percent": -35,
            "avg_daily_requests": 1500,
            "previous_avg": 2300
        },
        "event_type": "metric_update",
        "timestamp": datetime.now().isoformat()
    }
    
    await engine.process_event("metrics", event_data)
    print("  ✓ Usage drop processed\n")


async def demonstrate_reporting_integration():
    """Demonstrate how triggers integrate with reporting"""
    print("📊 Demonstrating reporting integration...\n")
    
    from trigger_reporting_integration import TriggerReportingIntegration, TriggerAwareCROReport
    
    # Set up reporting integration
    reporting = TriggerReportingIntegration()
    
    # Add some trigger events to customer context
    await add_sample_trigger_events(reporting)
    
    # Generate report with trigger data
    context = {
        "customer_id": "acme_inc",
        "company_name": "ACME Inc",
        "generated_at": datetime.now().isoformat()
    }
    
    # Generate trigger-aware report
    report = TriggerAwareCROReport()
    report_content = report.generate(context)
    
    print("Sample CRO Report with Trigger Data:")
    print("=" * 50)
    print(report_content)
    print("=" * 50)


async def add_sample_trigger_events(reporting: TriggerReportingIntegration):
    """Add sample trigger events for reporting demonstration"""
    
    sample_events = [
        {
            "trigger_id": "buying_signals",
            "trigger_name": "Buying Signal Detection",
            "customer_id": "acme_inc",
            "priority": "high",
            "source": "email",
            "timestamp": datetime.now().isoformat(),
            "matched_conditions": ["budget approved", "timeline defined"],
            "suggested_actions": ["send_proposal", "schedule_demo"],
            "confidence": 0.85
        },
        {
            "trigger_id": "competitive_mention",
            "trigger_name": "Competitive Mention",
            "customer_id": "acme_inc", 
            "priority": "medium",
            "source": "slack",
            "timestamp": datetime.now().isoformat(),
            "matched_conditions": ["vercel mentioned"],
            "suggested_actions": ["prepare_battlecard"],
            "confidence": 0.75,
            "context": {"competitor": "vercel"}
        }
    ]
    
    for event in sample_events:
        await reporting.add_trigger_to_context("acme_inc", event)


def print_trigger_configuration():
    """Print the current trigger configuration"""
    print("🔧 Current Trigger Configuration:\n")
    
    trigger_config = {
        "monitoring_intervals": {
            "slack": "60 seconds",
            "email": "300 seconds (5 minutes)",
            "metrics": "3600 seconds (1 hour)"
        },
        "default_triggers": [
            "high_value_account_mention",
            "churn_risk_keywords", 
            "buying_signals",
            "usage_drop",
            "competitive_mentions",
            "security_inquiries"
        ],
        "action_handlers": [
            "email_notification",
            "slack_notification",
            "crm_update",
            "task_creation",
            "activity_logging",
            "report_integration"
        ],
        "escalation_levels": [
            "account_executive",
            "sales_manager",
            "sales_director",
            "cro"
        ]
    }
    
    print(json.dumps(trigger_config, indent=2))
    print()


async def main():
    """Main demonstration function"""
    print("🚀 Sales Workspace Trigger Automation Demo\n")
    
    # Show configuration
    print_trigger_configuration()
    
    # Run trigger simulation
    engine = await simulate_trigger_events()
    
    # Show trigger statistics
    stats = engine.get_trigger_stats()
    print("📈 Trigger Statistics:")
    print(json.dumps(stats, indent=2))
    print()
    
    # Demonstrate reporting integration
    await demonstrate_reporting_integration()
    
    print("🎉 Demo completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())