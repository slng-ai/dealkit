# Customer Data

Central repository for all customer information and interaction history.

## Structure

### Individual Customer Profiles
Each customer gets their own directory with standardized structure:
```
customer_name/
├── profile.md          # Basic company info and contacts
├── interactions/       # All touchpoints chronologically
├── deals/             # Opportunity tracking
├── relationships/     # Stakeholder mapping
└── context/          # Aggregated insights
```

### Communication Logs
All customer interactions are tracked with consistent metadata:
- **Date/Time**: When the interaction occurred
- **Type**: Email, call, meeting, Slack, demo, etc.
- **Participants**: Who was involved from both sides
- **Summary**: Key discussion points and outcomes
- **Next Steps**: Actions and follow-ups identified
- **Sentiment**: Customer engagement level

### Deal Progression Tracking
Monitor opportunity advancement through standard stages:
1. **Qualified Lead** - ICP match confirmed
2. **Discovery** - Pain points and requirements understood
3. **Technical Validation** - PoC or technical discussions
4. **Business Case** - ROI and value proposition built
5. **Negotiation** - Contract terms and pricing
6. **Closed Won/Lost** - Final outcome

### Relationship Mapping
Track all stakeholders and their influence:
- **Champions**: Strong advocates for Your Company
- **Influencers**: Technical or business decision makers
- **Economic Buyers**: Budget holders and approvers
- **Users**: Day-to-day platform users
- **Blockers**: Potential obstacles or skeptics

## Daily Workflow

### Before Customer Meetings
1. Review latest interactions and context
2. Check deal status and next steps
3. Prepare talking points based on history
4. Update relationship map if needed

### After Customer Interactions
1. Log interaction summary immediately
2. Update deal stage if progression occurred
3. Note any new relationships or contacts
4. Schedule follow-up actions in CRM
5. Share insights with team in Slack

## Data Sources Integration

Customer data is automatically pulled from:
- **Salesforce**: Opportunity and contact data
- **Gong**: Call recordings and transcripts
- **Granola**: Meeting notes and action items
- **Slack**: Internal discussions about customer
- **Email**: Communication history
- **Calendar**: Meeting frequency and patterns

## Templates

### New Customer Setup
Use `/templates/customer_profile_template.md` for standardized onboarding.

### Interaction Logging
Use `/templates/interaction_log_template.md` for consistent tracking.

### Deal Reviews
Use `/templates/deal_review_template.md` for opportunity analysis.

## Best Practices

### Data Hygiene
- Update customer data within 24 hours of interaction
- Use consistent naming conventions
- Tag interactions with relevant topics
- Link related conversations and documents
- Archive outdated information appropriately

### Privacy & Security
- Never store sensitive data in plain text
- Use customer codenames for public channels
- Follow data retention policies
- Respect customer confidentiality agreements
- Secure access to customer directories

### Team Collaboration
- Share significant customer updates in #sales-updates
- CC relevant team members on important communications
- Use @mentions for urgent customer issues
- Document handoffs between team members
- Maintain single source of truth in CRM

## Quick Actions

### For AEs
- Review pipeline status: `./deals/pipeline_status.md`
- Check meeting prep: `./interactions/upcoming_meetings.md`
- Update opportunity: Use Salesforce integration
- Log customer call: Use interaction template

### For SDRs
- Research new prospect: Use profile template
- Track outbound sequence: `./outbound/sequences/`
- Update lead status: `./leads/qualification_status.md`
- Schedule handoff: Follow AE transition process

### For Leadership
- Review team pipeline: `../reporting/pipeline_dashboard.md`
- Check deal health: `../reporting/deal_health_metrics.md`
- Monitor customer satisfaction: `./relationships/nps_tracking.md`
- Analyze win/loss trends: `../reporting/win_loss_analysis.md`

## Integration with Knowledge Base

Customer data references and connects to:
- [ICP Analysis](../../knowledge_base/icp/) - Customer fit scoring
- [Objection Handling](../../knowledge_base/objection_handling/) - Response strategies
- [Competitive Analysis](../../knowledge_base/competitor_analysis/) - Positioning guidance
- [Case Studies](../../knowledge_base/wins/) - Reference stories
- [Pricing](../../knowledge_base/pricing/) - Deal structuring

## Metrics & KPIs

Track customer engagement through:
- **Interaction Frequency**: Touchpoints per week/month
- **Response Rates**: Email and outreach effectiveness  
- **Meeting Quality**: Discovery depth and value creation
- **Relationship Depth**: Multi-threading progress
- **Deal Velocity**: Time between stages
- **Win/Loss Ratios**: Conversion rates by source

---

*This customer data structure ensures we have comprehensive context for every customer interaction while maintaining privacy and enabling team collaboration.*