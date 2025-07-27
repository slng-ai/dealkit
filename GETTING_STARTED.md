# 🚀 Getting Started with Sales Workspace

Welcome to Sales Workspace! This guide will walk you through setting up your AI-powered sales intelligence system in under 30 minutes.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **API Access** to at least one of:
  - Slack workspace
  - Salesforce or HubSpot
  - Email provider (Gmail/Outlook)
- **Basic command line knowledge**

## 🎯 Quick Setup (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/sales-workspace.git
cd sales-workspace

# 2. Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the quick setup
./setup.sh
```

## 🔧 Configuration Steps

### Step 1: Set Up Your Environment Variables

Create a `.env` file in the root directory:

```bash
# Core Settings
COMPANY_NAME="Your Company Name"
WORKSPACE_ADMIN_EMAIL="admin@yourcompany.com"

# Slack Integration (Optional)
SLACK_API_TOKEN="xoxb-your-slack-bot-token"
SLACK_WORKSPACE="your-workspace"

# CRM Integration (Choose one)
SALESFORCE_CLIENT_ID="your-client-id"
SALESFORCE_CLIENT_SECRET="your-client-secret"
SALESFORCE_USERNAME="your-username"
SALESFORCE_PASSWORD="your-password"
SALESFORCE_SECURITY_TOKEN="your-token"

# OR
HUBSPOT_API_KEY="your-hubspot-key"
```

### Step 2: Initialize Your Workspace

```bash
# Run the initialization script
python initialize_workspace.py

# This will:
# - Create necessary directories
# - Set up sample customer profiles
# - Configure AI agents
# - Initialize reporting templates
```

### Step 3: Add Your First Customer

```bash
# Use the customer creation wizard
python create_customer.py

# Or manually create a profile
cat > customers/your-first-customer/profile.json << EOF
{
  "company_name": "Your First Customer Inc",
  "industry": "Technology",
  "status": "prospect",
  "deal_size": 50000,
  "stage": "discovery"
}
EOF
```

### Step 4: Configure Integrations

#### Slack Integration
```bash
# Test Slack connection
python workspace-setup/integrations/slack/test_connection.py

# Start Slack monitoring
./workspace-setup/integrations/slack/start_slack_fetcher.sh
```

#### CRM Integration
```bash
# Sync with your CRM
python workspace-setup/integrations/salesforce/sync.py

# Or for HubSpot
python workspace-setup/integrations/hubspot/sync.py
```

## 🎨 Personalization

### 1. Set Your Role

Edit `personal/config.json`:
```json
{
  "role": "AE",  // SDR, AE, Manager, CSM
  "timezone": "America/New_York",
  "working_hours": {
    "start": "09:00",
    "end": "18:00"
  },
  "notification_preferences": {
    "email": true,
    "slack": true,
    "desktop": false
  }
}
```

### 2. Customize Your Reports

```bash
# Generate your first morning brief
python reporting/pulse/morning_brief.py --user-id your-email@company.com

# View available reports for your role
python reporting/list_reports.py --role AE
```

### 3. Set Up Personal Triggers

Create `personal/triggers/my_triggers.yaml`:
```yaml
high_value_opportunity:
  conditions:
    - deal_size: "> 100000"
    - stage: "negotiation"
  actions:
    - notify: "immediately"
    - channel: "email"

competitive_mention:
  conditions:
    - keyword: ["competitor1", "competitor2"]
  actions:
    - alert: "high"
    - notify: "slack"
```

## 🚦 Verify Your Setup

Run the comprehensive check:

```bash
# Run the audit to ensure everything is configured correctly
./audit_workspace.py

# Expected output:
# ✅ Directory structure: Valid
# ✅ Integrations: Connected
# ✅ AI Agents: Initialized
# ✅ Reports: Configured
# Health Score: 95/100
```

## 📱 Daily Usage

### Morning Routine (5 minutes)
```bash
# 1. Get your morning brief
./navigate.sh report pulse
python morning_brief.py

# 2. Check priority customers
./navigate.sh customer
python reporting/pulse/deal_alert.py
```

### During the Day
```bash
# Quick customer lookup
./navigate.sh customer acme

# Find email template
./navigate.sh template follow-up

# Generate meeting context
python generate_context.py --customer "acme-corp" --type "demo"
```

### End of Day
```bash
# Update your pipeline
python update_pipeline.py

# Review team performance
python reporting/personal/ae_report.py
```

## 🆘 Troubleshooting

### Common Issues

**Issue**: Slack integration not receiving messages
```bash
# Check webhook configuration
python workspace-setup/integrations/slack/test_webhook.py

# Verify channel access
python workspace-setup/integrations/slack/list_channels.py
```

**Issue**: Reports showing no data
```bash
# Ensure CRM sync is running
python workspace-setup/integrations/check_sync_status.py

# Manually trigger sync
python workspace-setup/integrations/force_sync.py
```

**Issue**: AI agents not responding
```bash
# Check agent status
python .claude/agents/check_agents.py

# Restart agent service
python .claude/agents/restart_service.py
```

## 🎓 Next Steps

1. **Explore Templates**: Browse `/sales-toolkit/templates/` for battle-tested resources
2. **Review Playbooks**: Study `/sales-toolkit/playbooks/` for methodology guides
3. **Customize Agents**: Modify `.claude/agents/` for your specific needs
4. **Join Community**: Connect with other users for tips and best practices

## 📚 Additional Resources

- **Video Tutorials**: [YouTube Playlist](https://youtube.com/salesworkspace)
- **Community Forum**: [GitHub Discussions](https://github.com/yourusername/sales-workspace/discussions)
- **Advanced Guide**: [MASTER_CONTEXT.md](./MASTER_CONTEXT.md)
- **Quick Reference**: [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

## 🤝 Getting Help

- **Documentation**: Start with the README files in each directory
- **Issues**: [GitHub Issues](https://github.com/yourusername/sales-workspace/issues)
- **Slack Community**: [Join our Slack](https://salesworkspace.slack.com)
- **Email Support**: support@salesworkspace.io

---

🎉 **Congratulations!** You're now ready to transform your sales process with AI-powered intelligence.

Remember: The workspace gets smarter the more you use it. Start small, be consistent, and watch your sales productivity soar!