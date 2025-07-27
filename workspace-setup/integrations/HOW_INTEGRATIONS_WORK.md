# How Integrations Work with Sales Workspace

This guide explains how the integration stubs connect with the sample data structure and can be used to pull/push information from various sales tools.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Sales Workspace                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐    ┌──────────────────┐          │
│  │ Integration Hub │◄───┤ Base Integration │          │
│  └────────┬────────┘    └──────────────────┘          │
│           │                                             │
│  ┌────────┴────────┬───────────┬──────────┐           │
│  │                 │           │          │           │
│  ▼                 ▼           ▼          ▼           │
│ Slack            Gong      Granola    Email          │
│  API              API        API       API           │
│  │                 │           │          │           │
│  ▼                 ▼           ▼          ▼           │
└──┼─────────────────┼───────────┼──────────┼───────────┘
   │                 │           │          │
   ▼                 ▼           ▼          ▼
Customer          Call      Meeting     Email
Channels       Recordings    Notes    Threads
```

## Integration Patterns

### 1. Direct API Integration
Most integrations support direct API access with authentication:

```python
# Example: Fetching Slack data
slack = SlackIntegration()
slack.authenticate()  # Uses SLACK_TOKEN env var
data = slack.fetch_data('acme-corp', customer_name='ACME Corp')
```

### 2. URL-Based Analysis
For tools without API access, analyze shared URLs:

```python
# Example: Analyzing a Gong call URL
gong = GongIntegration()
result = gong.analyze_call_url("https://app.gong.io/call?id=1234567890")
# This extracts the call ID and fetches via API if possible,
# or falls back to WebFetch analysis
```

### 3. MCP Protocol Support
Integrations check for MCP servers and use them if available:

```python
# Automatic MCP detection
def _init_mcp_client(self):
    mcp_url = os.getenv('GONG_MCP_URL', 'http://localhost:3001/gong')
    # If MCP server is running, use it for all requests
```

## Data Flow Examples

### Customer Context Building

1. **Slack Integration** pulls conversations:
   ```
   slack/2024-03-15_poc_planning.json
   → Excitement about POC, technical discussions
   ```

2. **Gong Integration** analyzes calls:
   ```
   gong/2024-04-05_poc_results_review.json
   → 82% deal score, competitor mentions, next steps
   ```

3. **Granola Integration** extracts meeting notes:
   ```
   granola/2024-03-22_executive_overview.md
   → Decision makers, budget confirmed, timeline
   ```

4. **Context Aggregator** combines all sources:
   ```
   context_summary.md
   → Unified view with insights and recommendations
   ```

## Environment Variables

Each integration requires specific environment variables:

```bash
# Slack
export SLACK_TOKEN="xoxb-..."

# Gong
export GONG_API_KEY="your-api-key"
export GONG_API_SECRET="your-api-secret"

# Granola
export GRANOLA_API_KEY="your-api-key"

# Email
export GMAIL_CLIENT_ID="..."
export GMAIL_CLIENT_SECRET="..."

# Optional: MCP endpoints
export SLACK_MCP_URL="http://localhost:3001/slack"
export GONG_MCP_URL="http://localhost:3001/gong"
```

## Usage Patterns

### Pattern 1: Scheduled Data Collection
```python
# Run daily to update customer context
for customer in get_active_customers():
    # Fetch from all sources
    slack_data = slack.fetch_data(customer.id)
    gong_data = gong.fetch_customer_calls(customer.name)
    granola_data = granola.fetch_data(customer.id)
    
    # Process and save
    save_customer_data(customer.id, {
        'slack': slack_data,
        'gong': gong_data,
        'granola': granola_data
    })
```

### Pattern 2: Real-time URL Analysis
```python
# When user shares a meeting recording
@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    url = request.json['url']
    
    if 'gong.io' in url:
        result = gong.analyze_call_url(url)
    elif 'granola.so' in url:
        result = granola.analyze_granola_url(url)
    
    return jsonify(result)
```

### Pattern 3: Push Insights Back
```python
# After analysis, update source systems
# Update Gong with deal score
gong.push_data({
    'call_id': '1234567890',
    'custom_fields': {
        'deal_score': 82,
        'next_step': 'Contract review'
    }
}, 'call_custom_fields')

# Update Granola action item
granola.push_data({
    'action_id': 'abc123',
    'completed': True
}, 'action_item_status')
```

## Sample Data Structure Mapping

### From Integration → To File System

1. **Slack API Response** → `customers/profiles/acme_inc/slack/YYYY-MM-DD_topic.json`
   ```json
   {
     "channel": "#yourcompany-acme-poc",
     "messages": [...],
     "timestamp": "2024-03-15"
   }
   ```

2. **Gong Call Data** → `customers/profiles/acme_inc/gong/YYYY-MM-DD_meeting.json`
   ```json
   {
     "call_id": "1234567890",
     "talk_ratio": 0.68,
     "topics": ["pricing", "migration"],
     "action_items": [...]
   }
   ```

3. **Granola Meeting** → `customers/profiles/acme_inc/granola/YYYY-MM-DD_meeting.md`
   ```markdown
   # Executive Overview Meeting
   
   ## Attendees
   - Michael Chen (CTO)
   - Sarah Rodriguez (VP Eng)
   
   ## Action Items
   - [ ] Security review - Lisa Thompson
   - [ ] Migration plan - Alex Kumar
   ```

## Integration Development Guide

### Adding a New Integration

1. **Create integration class**:
   ```python
   class NewToolIntegration(BaseIntegration):
       def __init__(self):
           super().__init__("new_tool")
           self.config = {
               "auth_type": "oauth2",
               "base_url": "https://api.newtool.com/v1"
           }
   ```

2. **Implement required methods**:
   - `authenticate()` - Set up API connection
   - `fetch_data()` - Pull customer data
   - `process_data()` - Transform to standard format
   - `push_data()` - Update source system

3. **Add MCP support** (optional):
   ```python
   def _init_mcp_client(self):
       mcp_url = os.getenv('NEWTOOL_MCP_URL')
       # Initialize MCP client if available
   ```

4. **Handle URL analysis**:
   ```python
   def analyze_url(self, url: str):
       # Extract ID from URL
       # Fetch via API or use WebFetch
   ```

## Testing Integrations

### With Sample Data
```bash
# Test with ACME Inc sample data
python run_integration.py --integration slack --customer acme-corp --test

# This will:
# 1. Load sample data from customers/profiles/acme_inc/
# 2. Simulate API responses
# 3. Process and display results
```

### With Live APIs
```bash
# Set up credentials
export SLACK_TOKEN="xoxb-..."

# Run integration
python run_integration.py --integration slack --customer acme-corp --live
```

## Security Considerations

1. **Never commit credentials** - Use environment variables
2. **Sanitize customer data** - Remove sensitive information
3. **Use read-only access** where possible
4. **Rate limit API calls** - Respect API limits
5. **Log access** - Track who accesses what data

## Troubleshooting

### Common Issues

1. **Authentication failures**
   - Check environment variables
   - Verify API credentials
   - Check token expiration

2. **Missing data**
   - Verify customer naming conventions
   - Check date ranges
   - Confirm permissions

3. **MCP connection issues**
   - Check if MCP server is running
   - Verify MCP URL configuration
   - Fall back to direct API

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run integration with debug output
integration = SlackIntegration()
integration.logger.setLevel(logging.DEBUG)
```

## Next Steps

1. **Implement remaining integrations** for your specific tools
2. **Set up scheduled jobs** for automatic data collection
3. **Build alerting system** for important customer signals
4. **Create unified dashboard** using aggregated data
5. **Train team** on using the integrated workspace

Remember: These integrations are designed to augment human intelligence, not replace it. Always verify critical information and use your judgment when making decisions based on aggregated data.