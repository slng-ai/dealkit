# Slack Integration for Customer Intelligence

## Overview
The Slack integration automatically fetches and analyzes customer mentions across your workspace, providing real-time intelligence for sales and customer success teams.

## Features

### Automated Data Collection
- **Continuous Monitoring**: Fetches new messages every hour
- **Multi-Channel Coverage**: Monitors all configured channels
- **Customer Detection**: Identifies mentions using company names and aliases
- **Thread Context**: Captures full conversation context

### Intelligent Analysis
- **Sentiment Analysis**: Positive, negative, or neutral classification
- **Importance Scoring**: Critical, high, medium, or low priority
- **Category Classification**: Sales, support, success, product, or general
- **Keyword Detection**: Buying signals, churn risks, expansion opportunities

### Data Organization
- **Customer-Specific Storage**: Data saved to individual customer folders
- **Daily Aggregation**: Mentions grouped by date
- **Summary Generation**: Rolling summaries with key metrics
- **Alert Creation**: High-priority items flagged for immediate action

## Setup Instructions

### 1. Configure Slack App
```bash
# Set up Slack app with required permissions
export SLACK_API_TOKEN="xoxb-your-token-here"

# Required OAuth scopes:
# - channels:history
# - channels:read
# - groups:history
# - groups:read
# - im:history
# - mpim:history
```

### 2. Update Configuration
Edit `config.json` to customize:
- Channel list to monitor
- Keyword definitions
- Alert thresholds
- Integration settings

### 3. Initialize Customer Data
Ensure all customers have:
- Proper folder structure (`/customers/{customer-name}/`)
- Profile.json with company name and aliases
- Empty slack/ subdirectory for data storage

### 4. Run the Fetcher
```bash
# Run once for testing
python workspace-setup/integrations/slack/slack_fetcher.py

# Run as background service
nohup python workspace-setup/integrations/slack/slack_fetcher.py &

# Or use systemd/supervisord for production
```

## Data Structure

### Customer Slack Folder
```
customers/acme-corp/slack/
├── mentions_20240315.json      # Daily mention logs
├── mentions_20240316.json
└── slack_summary.json          # Aggregate summary
```

### Mention Record Format
```json
{
  "timestamp": "2024-03-15T10:30:00",
  "channel": "#sales",
  "context": "...Had a great call with Acme Corp today...",
  "sentiment": "positive",
  "category": "sales",
  "importance": "medium"
}
```

### Summary Format
```json
{
  "total_mentions": 127,
  "sentiment_breakdown": {
    "positive": 89,
    "negative": 12,
    "neutral": 26
  },
  "category_breakdown": {
    "sales": 45,
    "support": 23,
    "success": 34,
    "product": 15,
    "general": 10
  },
  "important_mentions": [
    {
      "timestamp": "2024-03-15T14:22:00",
      "context": "Acme Corp budget approved for Q2!",
      "channel": "#sales-wins"
    }
  ],
  "last_updated": "2024-03-15T15:00:00"
}
```

## Alert Types

### High Importance Mentions
Triggered when critical keywords detected:
- "urgent", "critical", "blocker"
- Immediate notification to account owner
- Added to morning brief report

### Negative Sentiment Spike
Triggered when 3+ negative mentions in short period:
- Indicates potential customer satisfaction issue
- Notifies customer success team
- Creates follow-up task

### Buying Signal Detection
Triggered by purchase intent keywords:
- "budget approved", "ready to buy"
- Notifies sales team immediately
- Updates opportunity in CRM

### Churn Risk Identification
Triggered by concerning language:
- "considering alternatives", "not happy"
- Escalates to customer success
- Initiates retention workflow

## Integration Points

### CRM Synchronization
- Updates customer records with Slack insights
- Adds activities for important mentions
- Adjusts health scores based on sentiment

### Reporting System
- Feeds into pulse reports for real-time alerts
- Contributes to customer health calculations
- Provides context for sales conversations

### Trigger Engine
- Activates workflows based on mention patterns
- Creates tasks for follow-up actions
- Sends notifications through configured channels

## Best Practices

### Channel Management
1. **Dedicated Customer Channels**: Create #customer-{name} channels
2. **Consistent Naming**: Use customer aliases in profile.json
3. **Access Control**: Ensure bot has access to all relevant channels
4. **Archive Old Channels**: Clean up inactive customer channels

### Data Quality
1. **Customer Aliases**: Keep aliases updated for accurate detection
2. **Keyword Maintenance**: Review and update keywords monthly
3. **False Positive Handling**: Refine patterns to reduce noise
4. **Context Window**: Adjust context size for meaningful snippets

### Performance Optimization
1. **Batch Processing**: Fetch multiple channels concurrently
2. **Rate Limiting**: Respect Slack API limits
3. **Data Retention**: Archive old data after 90 days
4. **Summary Compression**: Keep summaries focused on recent activity

## Troubleshooting

### Common Issues

**No mentions detected**
- Verify customer names and aliases
- Check channel access permissions
- Review keyword patterns

**High false positive rate**
- Refine customer name patterns
- Add negative keywords
- Adjust context boundaries

**Performance issues**
- Reduce fetch frequency
- Limit channel count
- Optimize batch sizes

**Authentication errors**
- Regenerate API token
- Verify OAuth scopes
- Check workspace settings

## Monitoring

### Health Checks
```bash
# Check if fetcher is running
ps aux | grep slack_fetcher

# View recent logs
tail -f slack_fetcher.log

# Check last fetch time
cat reporting/pulse/slack_alerts.json | jq .timestamp
```

### Metrics to Track
- Messages processed per hour
- Mentions detected per customer
- Alert generation rate
- API rate limit usage

## Security Considerations

1. **API Token Security**: Store in environment variables
2. **Data Privacy**: Respect message confidentiality
3. **Access Control**: Limit who can view Slack data
4. **Compliance**: Follow data retention policies
5. **Audit Trail**: Log all data access and processing

---

The Slack integration provides valuable real-time customer intelligence, enabling proactive sales and support actions based on actual customer conversations.