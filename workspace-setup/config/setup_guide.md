# Sales Workspace Configuration Guide

Step-by-step guide to configure your sales workspace environment.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Access to your company's various SaaS platforms
- Admin permissions for integrations

## Initial Setup

### 1. Environment Configuration

1. Copy the environment template:
```bash
cp config/environment_template.env .env
```

2. Fill in your actual values in the `.env` file

3. Verify configuration:
```bash
python scripts/verify_config.py
```

### 2. Workspace Configuration

1. Update `workspace.json` with your company details:
   - Replace `[Your Company]` with your actual company name
   - Update Slack channel names to match your workspace
   - Configure feature flags based on your needs

2. Test the configuration:
```bash
python scripts/test_workspace_config.py
```

## Integration Setup

### Slack Integration

1. **Create Slack App**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name: "Sales Workspace Bot"
   - Select your workspace

2. **Configure Bot Permissions**
   - Navigate to "OAuth & Permissions"
   - Add Bot Token Scopes:
     - `channels:history`
     - `channels:read`
     - `chat:write`
     - `users:read`
     - `files:read`

3. **Install to Workspace**
   - Click "Install to Workspace"
   - Copy the Bot User OAuth Token
   - Add to `.env` as `SLACK_BOT_TOKEN`

4. **Get User Token** (for advanced features)
   - Add User Token Scopes:
     - `channels:history`
     - `search:read`
   - Reinstall and copy User OAuth Token

### Salesforce Integration

1. **Create Connected App**
   - Setup → Apps → App Manager → New Connected App
   - Enable OAuth Settings
   - Callback URL: `http://localhost:8080/callback`
   - Selected OAuth Scopes:
     - Full access (full)
     - Perform requests at any time (refresh_token)

2. **Get Credentials**
   - Copy Consumer Key → `SFDC_CLIENT_ID`
   - Copy Consumer Secret → `SFDC_CLIENT_SECRET`
   - Get your Security Token (Profile → Settings → Reset Security Token)

3. **Test Connection**
```bash
python integrations/salesforce/test_connection.py
```

### Gong Integration

1. **Get API Credentials**
   - Log into Gong as admin
   - Settings → API → Create new API user
   - Copy Access Key and Secret

2. **Configure Webhooks** (optional)
   - Settings → Webhooks → Add webhook
   - URL: `https://your-domain.com/webhooks/gong`
   - Events: Call ended, Call transcribed

### Gmail Integration

1. **Enable Gmail API**
   - Go to Google Cloud Console
   - Create new project or select existing
   - Enable Gmail API

2. **Create Credentials**
   - Create OAuth 2.0 Client ID
   - Application type: Desktop app
   - Download credentials JSON

3. **Authorize Access**
```bash
python integrations/gmail/authorize.py
```

### Supabase Setup

1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create new project
   - Copy project URL and keys

2. **Initialize Database**
```bash
# Run migrations
python integrations/supabase/migrations/init.py
```

3. **Set up Real-time**
   - Enable real-time for customer_context table
   - Configure row-level security

## Data Flow Configuration

### Customer Context Aggregation

1. **Configure Sources**
   - Update `data_flows.customer_context_aggregation.sources` in workspace.json
   - Set appropriate refresh intervals

2. **Set up Scheduled Jobs**
```bash
# Install scheduler
pip install schedule

# Run scheduler
python system/scheduler.py
```

### Reporting Pipeline

1. **Configure Destinations**
   - Set up Notion databases
   - Configure Grafana dashboards
   - Set report generation schedules

2. **Test Pipeline**
```bash
python system/test_reporting_pipeline.py
```

## Security Configuration

### HashiCorp Vault Setup

1. **Initialize Vault**
```bash
vault operator init
vault operator unseal
```

2. **Configure Secrets**
```bash
vault kv put secret/sales-workspace/slack \
  bot_token="xoxb-..." \
  user_token="xoxp-..."
```

3. **Set up Authentication**
```bash
vault auth enable approle
vault policy write sales-workspace scripts/vault-policy.hcl
```

### Data Encryption

1. **Generate Encryption Keys**
```bash
python scripts/generate_keys.py
```

2. **Configure Key Rotation**
   - Set rotation schedule in Vault
   - Update `ENCRYPTION_KEY` periodically

## Monitoring Setup

### Grafana Dashboards

1. **Import Dashboards**
```bash
# Import pre-built dashboards
python scripts/import_grafana_dashboards.py
```

2. **Configure Alerts**
   - Set up alert rules for API errors
   - Configure notification channels

### Logging Configuration

1. **Set Log Levels**
   - Update `LOG_LEVEL` in .env
   - Configure log rotation

2. **Set up Log Aggregation**
   - Configure Loki/Elasticsearch
   - Set retention policies

## Testing Your Setup

### Integration Tests
```bash
# Test all integrations
python scripts/test_all_integrations.py

# Test specific integration
python scripts/test_integration.py --service=slack
```

### End-to-End Test
```bash
# Run full customer context aggregation
python scripts/e2e_test.py --customer="Test Company"
```

## Troubleshooting

### Common Issues

1. **Slack Bot Can't Access Channels**
   - Ensure bot is invited to channels
   - Check bot permissions
   - Verify OAuth scopes

2. **Salesforce Connection Errors**
   - Verify security token
   - Check IP restrictions
   - Ensure API access is enabled

3. **Rate Limiting**
   - Implement exponential backoff
   - Check rate limit headers
   - Use caching where appropriate

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python system/run.py
```

### Health Checks
```bash
# Check all services
python scripts/health_check.py

# Check specific service
curl http://localhost:8000/health/slack
```

## Next Steps

1. **Set up automated workflows**
   - Configure customer onboarding automation
   - Set up deal monitoring alerts
   - Enable competitive intelligence tracking

2. **Train your team**
   - Run through onboarding guides
   - Practice with test data
   - Set up team permissions

3. **Customize for your process**
   - Modify templates for your use cases
   - Adjust automation rules
   - Configure custom reports

## Support

- Documentation: `/sales-workspace/docs/`
- Issues: Create GitHub issue in your repo
- Slack: #sales-workspace-support channel

Remember to never commit your `.env` file or share credentials!