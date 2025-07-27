# Sales Tool Integrations & Automation

This directory contains integrations for common sales tools and a comprehensive **trigger automation system** that monitors various data sources and automatically executes appropriate actions.

## 🎯 Trigger Automation System

The trigger automation system monitors Slack, email, Gong calls, and metrics for specific events, then automatically:
- Sends notifications to the right people
- Updates CRM records
- Creates follow-up tasks
- Generates reports
- Schedules meetings
- Escalates critical issues

### Key Features
- **Real-time monitoring** of multiple data sources
- **Intelligent trigger detection** using keywords, patterns, and metrics
- **Automated action execution** with customizable workflows
- **Reporting integration** for insights and analytics
- **Escalation management** through the management chain

### Quick Start with Triggers
```bash
# Run the trigger system demo
python example_trigger_usage.py

# This demonstrates:
# - Buying signal detection
# - Churn risk alerts
# - Competitive mentions
# - Security inquiries
# - Usage drop monitoring
```

See **[Trigger System Documentation](#trigger-automation-system)** below for full details.

## 🔌 Tool Integrations

All integrations are designed from an individual salesperson's perspective.

## CRM Integrations

### Salesforce (`/salesforce/`)
- Fetch opportunities owned by user
- Track account activities
- Pull opportunity history and stage changes
- Search contacts by company

### HubSpot (`/hubspot/`)
- Access deals and pipeline data
- Track email engagement metrics
- Fetch contact interaction history
- Monitor email opens and clicks

### Pipedrive (`/pipedrive/`)
- View deals and activities
- Track deal flow metrics
- Access email threads per deal
- Today's task list

### Attio (`/attio/`)
- Modern CRM for relationships
- Flexible data model
- Deal pipeline tracking
- Interaction timeline
- Custom attributes

## Meeting Recording & Intelligence

### Gong.io (`/gong/`)
- Analyze calls via URL (WebFetch)
- Fetch call transcripts and stats
- Search calls by keyword
- Track talk ratios and engagement

### Zoom (`/zoom/`)
- Access meeting recordings
- Pull auto-generated transcripts
- Get participant lists
- Track attendance patterns

### Chorus.ai (`/chorus/`)
- Fetch conversation insights
- Track deal intelligence
- Search for key moments
- Identify risks and action items

## Communication Channels

### Slack (`/slack/`)
- **Already implemented**
- Fetch channel messages
- Track user mentions
- Search conversations

### Microsoft Teams (`/microsoft_teams/`)
- Pull chat conversations
- Access channel messages
- Get meeting attendance
- Search across all messages

### Email (`/email/`)
- **Gmail integration started**
- Outlook integration planned
- Thread analysis
- Attachment tracking

### LinkedIn (`/linkedin/`)
- Access messages and InMail
- Search for contacts
- Track profile views
- Sales Navigator integration

## Sales Engagement Platforms

### Outreach.io (`/outreach/`)
- Track sequences and performance
- Monitor email engagement
- View prospect touchpoints
- Daily task management

### Apollo.io (`/apollo/`)
- Enrich contact data
- Company intelligence
- Email engagement tracking
- Lead search and discovery

## Calendar & Scheduling

### Calendar (`/calendar/`)
- Google Calendar support
- Outlook Calendar support
- Track customer meetings
- Analyze meeting patterns

### Calendly (`/calendly/`)
- Track scheduling links usage
- Monitor bookings and no-shows
- Get invitee information
- Analyze booking patterns
- Search meetings by attendee

## Specialized Tools

### Granola (`/granola/`)
- Meeting notes via URL
- Action item extraction
- Decision tracking

### Notion (`/notion/`)
- Workspace documentation
- Meeting notes database
- Knowledge base articles
- Sales templates
- Customer pages

## Implementation Status

✅ **Fully Implemented:**
- Slack (complete with API and MCP support)
- Gong (API + URL analysis + MCP support)
- Granola (API + URL analysis + MCP support)
- Gmail (OAuth2 flow ready)

🔄 **Stubs Created:**
- All CRM integrations
- Meeting recording platforms
- Communication channels
- Sales engagement tools

⏳ **Next Steps:**
1. Implement OAuth2 flows for remaining platforms
2. Add actual API calls to stubs
3. Create unified data models
4. Build authentication manager

## How It Works

See **[HOW_INTEGRATIONS_WORK.md](./HOW_INTEGRATIONS_WORK.md)** for detailed documentation on:
- Integration architecture
- Data flow patterns
- MCP protocol support
- Sample data mapping
- Security considerations

## Quick Start

1. **Set up environment variables:**
   ```bash
   export SLACK_TOKEN="xoxb-..."
   export GONG_API_KEY="your-key"
   export GONG_API_SECRET="your-secret"
   export GRANOLA_API_KEY="your-key"
   ```

2. **Run example usage:**
   ```bash
   python example_usage.py
   ```
   This demonstrates all integration patterns with ACME Inc sample data.

3. **Test individual integrations:**
   ```python
   from integrations.slack.slack_integration import SlackIntegration
   
   slack = SlackIntegration()
   slack.authenticate()
   data = slack.fetch_data('acme-corp', customer_name='ACME Corp')
   ```

## Integration Patterns

### 1. Direct API Access
```python
# Fetch data via API
gong = GongIntegration()
gong.connect()
calls = gong.fetch_customer_calls("ACME Corp")
```

### 2. URL-Based Analysis
```python
# Analyze shared URLs
result = gong.analyze_call_url("https://app.gong.io/call?id=123")
result = granola.analyze_granola_url("https://app.granola.so/meeting/abc")
```

### 3. MCP Protocol (if available)
```python
# Automatic MCP detection and usage
# Set GONG_MCP_URL environment variable
# Integration will use MCP instead of direct API
```

### 4. Push Data Back
```python
# Update source systems with insights
gong.push_insights_to_gong("call-id", {
    'custom_fields': {'deal_score': 82},
    'tags': ['high-value', 'competitive']
})
```

## Environment Variables

Each integration requires specific environment variables:
- `{TOOL}_API_KEY` or
- `{TOOL}_CLIENT_ID` and `{TOOL}_CLIENT_SECRET`
- Optional: `{TOOL}_MCP_URL` for MCP support

See individual integration files for specific requirements.

---

# Trigger Automation System

## Overview

The trigger automation system monitors various data sources (Slack, email, Gong calls, metrics) for specific events and automatically executes appropriate actions. This creates a responsive sales environment that helps teams stay on top of opportunities and risks.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Trigger Engine  │    │     Actions     │
│                 │    │                  │    │                 │
│ • Slack         │───▶│ • Event Monitor  │───▶│ • Notifications │
│ • Email         │    │ • Rule Processor │    │ • CRM Updates   │
│ • Gong Calls    │    │ • Action Queue   │    │ • Task Creation │
│ • Metrics       │    │ • Reporting      │    │ • Workflows     │
│ • Granola       │    │                  │    │ • Reports       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Components

### 1. Trigger Engine (`trigger_engine.py`)
- **Core orchestrator** that coordinates monitoring and actions
- Processes events from all integration sources
- Manages trigger rules and action execution
- Provides statistics and monitoring capabilities

### 2. Trigger Types

#### Customer Triggers (`triggers/customer_triggers.py`)
- **CustomerTrigger**: Monitors specific customers for any activity
- **AccountHealthTrigger**: Tracks health metrics and risk indicators
- **NewStakeholderTrigger**: Detects when new contacts are introduced

#### Keyword Triggers (`triggers/keyword_triggers.py`)
- **BuyingSignalTrigger**: Detects purchase intent language
- **ChurnRiskTrigger**: Identifies potential churn indicators
- **CompetitiveTrigger**: Monitors competitor mentions
- **SecurityComplianceTrigger**: Catches security/compliance inquiries

#### Metric Triggers (`triggers/metric_triggers.py`)
- **UsageDropTrigger**: Alerts on significant usage decreases
- **EngagementScoreTrigger**: Monitors customer engagement levels
- **SupportTicketVolumeTrigger**: Tracks support ticket patterns
- **RevenueAtRiskTrigger**: Identifies revenue risk conditions

### 3. Action Handlers

#### Notifications (`actions/notification_action.py`)
- **EmailNotificationAction**: Send email alerts to appropriate team members
- **SlackNotificationAction**: Post messages to relevant Slack channels
- **SMSNotificationAction**: Send SMS for critical alerts

#### CRM Integration (`actions/crm_action.py`)
- **UpdateOpportunityAction**: Update CRM opportunity records
- **CreateTaskAction**: Generate follow-up tasks
- **LogActivityAction**: Record trigger events as CRM activities

#### Reporting (`actions/report_action.py`)
- **AddToReportAction**: Include trigger events in daily/weekly reports
- **GenerateReportAction**: Create summary reports from trigger data

#### Workflows (`actions/workflow_action.py`)
- **ScheduleMeetingAction**: Automatically schedule appropriate meetings
- **CreateFollowupAction**: Generate automated follow-up sequences
- **EscalationAction**: Handle escalation through management chain

### 4. Reporting Integration (`trigger_reporting_integration.py`)
- Connects trigger events to the reporting system
- Enhances customer context with trigger insights
- Provides trigger-aware report classes

## Trigger Types in Detail

### Buying Signals
**Keywords**: budget approved, ready to purchase, timeline, proposal, quote
**Patterns**: "what would it take", "when can we start", "need this by"
**Actions**: Immediate AE notification, opportunity update, demo scheduling

### Churn Risk Indicators  
**Keywords**: cancel, frustrated, switching, disappointed, competitor
**Patterns**: "considering alternatives", "not meeting our needs"
**Actions**: Emergency alerts, retention calls, CSM notification

### Competitive Mentions
**Keywords**: vercel, netlify, aws, cloudflare, competitor names
**Patterns**: "comparing with", "vs competitor", "better than"
**Actions**: Competitive intel alerts, battlecard preparation

### Security/Compliance
**Keywords**: security, HIPAA, SOC2, compliance, audit, encryption
**Patterns**: "security review", "compliance requirements"
**Actions**: Security team notification, compliance documentation

### Usage/Health Metrics
**Thresholds**: Usage drop >20%, health score <0.7, support tickets >5
**Actions**: CSM alerts, health check scheduling, usage investigation

## Quick Start

1. **Run the example**: `python example_trigger_usage.py`
2. **Configure your integrations** in the integration modules
3. **Customize trigger rules** in `personal/triggers.md`
4. **Set up action handlers** for your tools
5. **Start the engine** and monitor results

## Usage Examples

### Start the Trigger Engine

```python
from trigger_engine import TriggerEngine
from actions import EmailNotificationAction, SlackNotificationAction

# Initialize engine
engine = TriggerEngine()

# Register action handlers
engine.register_action_handler("notify_ae", EmailNotificationAction().execute)
engine.register_action_handler("send_slack", SlackNotificationAction().execute)

# Start monitoring
await engine.start()
```

### Process Events Manually

```python
# Simulate email event
email_event = {
    "customer_id": "acme_inc",
    "source": "email",
    "text": "We're ready to move forward with this project",
    "subject": "Ready to proceed",
    "sender": "cto@acme.com"
}

await engine.process_event("email", email_event)
```

### Generate Reports with Trigger Data

```python
from trigger_reporting_integration import TriggerAwareCROReport

# Generate report including trigger insights
report = TriggerAwareCROReport()
context = {"customer_id": "acme_inc", "company_name": "ACME Inc"}
report_content = report.generate(context)
```

## Integration with Sales Workspace

The trigger system integrates with all major workspace components:

- **Customer Profiles**: Trigger events enrich customer context
- **Reporting**: Automated insights in all reports
- **Integrations**: Data flows from Slack, email, Gong, etc.
- **Workflows**: Triggers initiate automated sequences
- **Analytics**: Performance tracking and optimization

## Files Structure

```
integrations/
├── trigger_engine.py              # Main trigger orchestrator
├── triggers/
│   ├── __init__.py
│   ├── base_trigger.py            # Base trigger class
│   ├── customer_triggers.py       # Customer-specific triggers
│   ├── keyword_triggers.py        # Keyword-based triggers
│   └── metric_triggers.py         # Metric-based triggers
├── actions/
│   ├── __init__.py
│   ├── base_action.py             # Base action class
│   ├── notification_action.py     # Email, Slack, SMS notifications
│   ├── crm_action.py              # CRM updates and tasks
│   ├── report_action.py           # Reporting integration
│   └── workflow_action.py         # Meetings, follow-ups, escalation
├── trigger_reporting_integration.py # Connects to reporting system
└── example_trigger_usage.py       # Demo and examples
```

The trigger automation system transforms passive sales monitoring into proactive, intelligent responses that help teams capture opportunities and prevent churn.