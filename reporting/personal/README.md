# Personal Reports

Individual contributor reports focused on personal performance, activities, and next steps.

## Report Types

### Sales Development Representative (SDR) Reports
- **SDR Report** (`sdr_report.py`) - Lead qualification, outreach performance, and response analysis
- **Lead Researcher Report** - Deep dive into prospect research and contact mapping
- **Outreach Performance Report** - Channel effectiveness and message optimization

### Account Executive (AE) Reports  
- **Deal Progress Report** - Individual deal status and next steps
- **Activity Summary Report** - Daily/weekly activity tracking and productivity
- **Territory Performance Report** - Geographic or vertical territory analysis

### Field Development Engineer (FDE) Reports
- **FDE Report** (`fde_report.py`) - Technical validation and proof-of-concept status
- **Technical Discovery Report** - Requirements gathering and solution fit analysis
- **Implementation Readiness Report** - Technical onboarding and setup planning

### Customer Success Manager (CSM) Reports
- **Account Health Report** - Customer satisfaction and expansion opportunities
- **Onboarding Progress Report** - Implementation milestones and success metrics
- **Renewal Risk Report** - Churn indicators and mitigation strategies

### Sales Engineering (SE) Reports
- **Demo Performance Report** - Technical demonstration effectiveness
- **Proof-of-Concept Report** - POC results and technical validation
- **Integration Assessment Report** - Technical requirements and architecture planning

## Report Characteristics

### Personal Focus
- Individual KPIs and metrics
- Personal activity tracking
- Next action recommendations
- Skill development insights

### Daily/Weekly Cadence
- Real-time activity updates
- Short-term focus (1-7 days)
- Immediate action orientation
- Personal accountability metrics

### Data Sources
- Individual CRM activities
- Email and call tracking
- Demo and meeting outcomes
- Personal goal tracking

## Usage Guidelines

### Report Generation
```python
from reporting.personal.sdr_report import SDRReport

report = SDRReport()
context = {
    'customer_id': 'acme-corp',
    'user_id': 'jane.smith',
    'time_period': 'last_7_days'
}
output = report.generate(context)
```

### Automation Schedule
- **Morning Brief**: Daily at 8 AM with yesterday's activities
- **Weekly Summary**: Monday at 9 AM with previous week's performance
- **Goal Check-in**: Friday at 5 PM with week's progress toward targets

### Customization
Each report supports:
- Time period filtering
- Goal comparison
- Activity type focus
- Performance benchmarking

## Best Practices

### Data Quality
- Ensure CRM activities are logged consistently
- Validate email and call tracking integration
- Maintain accurate opportunity stages
- Update contact information regularly

### Action Orientation
- Focus on next 24-48 hour actions
- Prioritize high-impact activities
- Include specific contact recommendations
- Provide clear success metrics

### Performance Tracking
- Track leading indicators (activities)
- Monitor conversion rates between stages
- Identify coaching opportunities
- Celebrate wins and progress