# Supabase Integration

Integration for pulling customer data from Supabase database using customer ID.

## Overview

This integration provides comprehensive access to customer information stored in Supabase, including usage metrics, billing data, support tickets, feature adoption, and user activity. It's designed to give sales teams complete visibility into customer health and engagement.

## Features

### Customer Data Retrieval
- **Profile Information**: Basic customer details and account status
- **Usage Metrics**: API calls, model deployments, performance data
- **Billing Information**: Current plans, payment status, invoice history
- **Support Tickets**: Recent tickets, resolution times, priority breakdown
- **Feature Usage**: Adoption rates, most-used features, unused capabilities
- **API Analytics**: Endpoint usage, error rates, response times
- **User Activity**: Session data, engagement metrics, active users
- **Subscription Details**: Contract information, renewal dates, add-ons

### Health Scoring
- **Comprehensive Health Score**: Weighted calculation based on multiple factors
- **Factor Analysis**: Usage, support, feature adoption, user engagement
- **Status Classification**: Excellent, Good, At Risk, Critical
- **Recommendations**: Actionable insights based on health factors

### Change Tracking
- **Recent Activity**: Summary of customer changes over specified periods
- **Trend Analysis**: Usage patterns and engagement trends
- **Alert Capabilities**: Identification of significant changes

## Setup

### 1. Install Dependencies
```bash
pip install supabase
```

### 2. Configure Access
Update `/config/supabase_config.json` with your credentials:
```json
{
  "url": "https://your-project-id.supabase.co",
  "service_role_key": "your-service-role-key-here"
}
```

### 3. Database Schema
Ensure your Supabase database has the following tables:
- `customers` - Main customer profiles
- `usage_metrics` - API and platform usage data
- `billing` - Billing and payment information
- `invoices` - Invoice history
- `support_tickets` - Customer support interactions
- `feature_usage` - Feature adoption tracking
- `api_logs` - API usage logs
- `user_sessions` - User activity sessions
- `customer_users` - Customer user accounts
- `subscriptions` - Subscription and contract details

## Usage

### Basic Customer Data Retrieval
```python
from supabase_integration import SupabaseIntegration

# Initialize integration
supabase = SupabaseIntegration()

# Get comprehensive customer data
customer_data = supabase.fetch_customer_data("customer_123")

# Access specific data sections
profile = customer_data['profile']
usage = customer_data['usage_metrics']
billing = customer_data['billing_info']
```

### Health Score Calculation
```python
# Get customer health score
health_score = supabase.get_customer_health_score("customer_123")

print(f"Overall Score: {health_score['overall_score']}")
print(f"Status: {health_score['status']}")
print(f"Recommendations: {health_score['recommendations']}")
```

### Recent Changes Tracking
```python
# Get recent changes (last 7 days)
changes = supabase.get_recent_customer_changes("customer_123", days=7)

print(f"Changes detected: {len(changes['changes_detected'])}")
```

## Data Structure

### Customer Profile
```python
{
    'customer_id': 'customer_123',
    'company_name': 'Acme Corp',
    'industry': 'Technology',
    'company_size': '100-500',
    'plan_type': 'Enterprise',
    'signup_date': '2024-01-15T10:00:00Z',
    'status': 'active',
    'primary_contact': 'john@acme.com',
    'account_manager': 'user@yourcompany.com'
}
```

### Usage Metrics
```python
{
    'period_days': 30,
    'total_api_calls': 15000,
    'total_models_deployed': 5,
    'average_response_time': 250.5,
    'peak_usage_day': {...},
    'daily_metrics': [...]
}
```

### Health Score
```python
{
    'overall_score': 78.5,
    'status': 'Good',
    'status_color': 'yellow',
    'factors': {
        'usage': {'score': 85, 'weight': 0.3},
        'support': {'score': 70, 'weight': 0.2},
        'feature_adoption': {'score': 75, 'weight': 0.25},
        'user_engagement': {'score': 80, 'weight': 0.25}
    },
    'recommendations': [...]
}
```

## Integration with Sales Workflow

### Customer Research
Use customer data for meeting preparation:
```python
# Get comprehensive customer context
data = supabase.fetch_customer_data(customer_id)

# Prepare talking points
usage_trend = "increasing" if data['usage_metrics']['total_api_calls'] > 10000 else "stable"
support_health = "excellent" if data['support_tickets']['open_tickets'] == 0 else "needs attention"
```

### Account Review Preparation
Generate account health summaries:
```python
health = supabase.get_customer_health_score(customer_id)

if health['status'] == 'At Risk':
    print("Customer needs immediate attention")
    print(f"Recommendations: {health['recommendations']}")
```

### Renewal Planning
Check subscription and contract status:
```python
subscription = data['subscription_details']
if subscription['days_to_renewal'] and subscription['days_to_renewal'] < 60:
    print(f"Renewal approaching in {subscription['days_to_renewal']} days")
```

## Performance Considerations

### Caching
- Customer data is cached for 10 minutes by default
- Usage metrics cached for 3 minutes
- Configurable cache TTL in config file

### Rate Limiting
- Respects Supabase rate limits
- Configurable request limits
- Automatic retry with exponential backoff

### Query Optimization
- Selective field retrieval
- Date range filtering for time-series data
- Efficient aggregation queries

## Security

### Access Control
- Uses service role key for administrative access
- Row-level security policies respected
- Customer data isolation enforced

### Data Privacy
- No sensitive data logged
- Secure credential storage
- Audit trail for data access

## Monitoring

### Logging
- Comprehensive error logging
- Performance metrics tracking
- Integration health monitoring

### Alerts
- Failed query notifications
- Performance degradation alerts
- Data inconsistency warnings

## Error Handling

### Common Issues
- **Authentication Errors**: Check service role key configuration
- **Table Not Found**: Verify database schema matches configuration
- **Rate Limiting**: Implement request queuing and retry logic
- **Data Inconsistencies**: Validate data types and field mappings

### Debugging
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test connection
try:
    data = supabase.fetch_customer_data("test_customer")
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
```

## Best Practices

### Data Retrieval
- Always specify customer_id for queries
- Use appropriate date ranges for time-series data
- Cache frequently accessed data
- Handle missing data gracefully

### Performance
- Batch multiple customer requests when possible
- Use connection pooling for high-volume usage
- Monitor query performance and optimize slow queries
- Implement pagination for large result sets

### Maintenance
- Regularly update customer data mappings
- Monitor and clean up stale cache entries
- Review and optimize database indexes
- Update integration when Supabase schema changes

## Related Integrations

This integration works well with:
- [Salesforce CRM](../salesforce/) - Customer relationship data
- [Slack](../slack/) - Team communication about customers
- [Email](../email/) - Customer communication history
- [Gong](../gong/) - Call recordings and insights

## Support

For technical issues:
1. Check the logs for error details
2. Verify Supabase configuration and connectivity
3. Review database schema and permissions
4. Contact the Sales Operations team for assistance

---

*This integration provides the foundation for data-driven customer success and sales activities.*