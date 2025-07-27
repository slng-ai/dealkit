# Customer Templates

Standardized formats and frameworks for consistent customer data management.

## Purpose

This directory provides reusable templates that ensure consistent, comprehensive customer data collection and management across all accounts and prospects.

## Template Categories

### Profile Templates
Standardized formats for customer information:
- **[Company Profile Template](./company_profile_template.md)** - Complete business intelligence format
- **[Contact Profile Template](./contact_profile_template.md)** - Individual stakeholder information
- **[ICP Scoring Template](./icp_scoring_template.md)** - Ideal customer profile assessment
- **[Competitive Analysis Template](./competitive_analysis_template.md)** - Market positioning framework

### Interaction Templates  
Communication and meeting documentation:
- **[Call Log Template](./call_log_template.md)** - Phone conversation documentation
- **[Meeting Notes Template](./meeting_notes_template.md)** - Structured meeting capture
- **[Email Interaction Template](./email_interaction_template.md)** - Email communication logging
- **[Demo Follow-up Template](./demo_followup_template.md)** - Post-demonstration summary

### Opportunity Templates
Deal tracking and progression:
- **[Opportunity Profile Template](./opportunity_profile_template.md)** - Deal information structure
- **[MEDDPICC Assessment Template](./meddpicc_template.md)** - Qualification framework
- **[Deal Review Template](./deal_review_template.md)** - Regular opportunity analysis
- **[Close Plan Template](./close_plan_template.md)** - Mutual success planning

### Health Monitoring Templates
Customer success tracking:
- **[Health Score Template](./health_score_template.md)** - Multi-factor assessment
- **[Usage Analysis Template](./usage_analysis_template.md)** - Product adoption tracking
- **[Relationship Map Template](./relationship_map_template.md)** - Stakeholder influence diagram
- **[Risk Assessment Template](./risk_assessment_template.md)** - Churn prevention framework

## Template Structure

### Standard Format
All templates follow consistent structure:
```markdown
# [Template Name]

## Overview
[Purpose and usage instructions]

## Required Information
[Essential fields and data points]

## Optional Information  
[Additional context and details]

## Examples
[Sample completed sections]

## Integration
[How this connects to other templates]
```

### Data Field Standards
- **Required Fields**: Must be completed for all records
- **Optional Fields**: Additional context when available
- **Calculated Fields**: Auto-generated from other data
- **Integration Fields**: Populated from external systems
- **Validation Rules**: Data quality requirements

### Version Control
- **Template Version**: Track updates and improvements
- **Last Modified**: Change date and author
- **Change Log**: History of modifications
- **Approval Status**: Review and validation
- **Usage Instructions**: Implementation guidance

## Key Templates

### Company Profile Template
```markdown
# Company Profile: [Company Name]

## Basic Information
- **Company Name**: [Legal entity name]
- **Industry**: [Primary vertical/sector]  
- **Sub-Industry**: [Specific focus area]
- **Headquarters**: [City, State, Country]
- **Founded**: [Year established]
- **Website**: [Primary domain]

## Size and Scale
- **Employees**: [Headcount range]
- **Revenue**: [Annual revenue range]
- **Funding Stage**: [Bootstrap/Series A/B/C/Public]
- **Last Funding**: [Amount and date]
- **Growth Rate**: [YoY percentage]

## Technology Profile
- **Tech Stack**: [Primary technologies used]
- **Cloud Provider**: [AWS/GCP/Azure/Multi-cloud]
- **ML Maturity**: [Beginner/Intermediate/Advanced]
- **Data Volume**: [Scale of data processing]
- **Current ML Tools**: [Existing solutions]

## Business Intelligence
- **Key Initiatives**: [Strategic priorities]
- **Pain Points**: [Primary challenges]
- **Success Metrics**: [How they measure success]
- **Decision Timeline**: [Urgency and timing]
- **Budget Cycle**: [Planning and approval process]

## ICP Assessment
- **Fit Score**: [0-100 numerical rating]
- **Technology Alignment**: [How well we match their stack]
- **Use Case Relevance**: [Applicability of our solution]
- **Market Position**: [Their competitive stance]
- **Growth Trajectory**: [Scaling potential]

## Competitive Landscape
- **Current Vendors**: [Existing relationships]
- **Evaluation Alternatives**: [Other options being considered]
- **Previous Solutions**: [What they've tried before]
- **Switching Barriers**: [Obstacles to change]
- **Decision Influencers**: [External advisors/consultants]
```

### Contact Profile Template
```markdown
# Contact Profile: [First Last]

## Personal Information
- **Full Name**: [First Middle Last]
- **Job Title**: [Current position]
- **Department**: [Functional area]
- **Reports To**: [Manager name and title]
- **Team Size**: [Number of direct reports]

## Contact Information
- **Work Email**: [Primary business email]
- **Personal Email**: [Secondary contact if available]
- **Phone**: [Direct number with extension]
- **Mobile**: [Cell phone if shared]
- **LinkedIn**: [Profile URL]

## Professional Background
- **Time at Company**: [Tenure in current role]
- **Previous Experience**: [Relevant background]
- **Education**: [Degrees and institutions]
- **Certifications**: [Professional credentials]
- **Expertise Areas**: [Technical and business skills]

## Role in Decision Process
- **Decision Authority**: [Budget/Technical/User/Influencer]
- **Influence Level**: [High/Medium/Low with explanation]
- **Evaluation Involvement**: [How they participate in buying process]
- **Success Criteria**: [What matters most to them personally]
- **Concerns/Objections**: [Reservations about our solution]

## Relationship Development
- **Champion Potential**: [Likelihood to advocate internally]
- **Engagement Level**: [Current interest and responsiveness]
- **Communication Style**: [Formal/casual, detail/summary preference]
- **Best Contact Method**: [Email/phone/Slack/in-person]
- **Availability Patterns**: [Time zones and scheduling preferences]

## Interaction History
- **First Contact**: [Date and method of initial connection]
- **Last Interaction**: [Most recent communication]
- **Relationship Progression**: [Evolution of engagement]
- **Key Conversations**: [Important discussions and outcomes]
- **Shared Connections**: [Mutual contacts and referrals]
```

### MEDDPICC Assessment Template
```markdown
# MEDDPICC Assessment: [Opportunity Name]

## Metrics (M)
**What quantifiable business outcomes will drive their decision?**
- **Current Performance**: [Baseline measurements]
- **Target Improvement**: [Desired outcomes]
- **Success Metrics**: [How they'll measure value]
- **Timeline**: [When they expect to see results]
- **Measurement Process**: [How they'll track progress]

## Economic Buyer (E)  
**Who has the authority and budget to make this decision?**
- **Name and Title**: [Decision maker identification]
- **Budget Authority**: [Spending limit and approval process]
- **Decision Timeline**: [When they need to decide]
- **Success Criteria**: [What matters most to them]
- **Engagement Status**: [Have we met with them?]

## Decision Criteria (D)
**What factors will influence their vendor selection?**
- **Must-Have Requirements**: [Non-negotiable features]
- **Nice-to-Have Features**: [Preferred capabilities]
- **Evaluation Methodology**: [How they'll compare options]
- **Scoring Framework**: [Weighting of different factors]
- **Reference Requirements**: [Customer validation needs]

## Decision Process (D)
**How will they make the buying decision?**
- **Evaluation Committee**: [Who's involved and their roles]
- **Process Steps**: [Stages from evaluation to signature]
- **Timeline**: [Key milestones and deadlines]
- **Approval Workflow**: [Sign-off requirements]
- **Final Decision Date**: [When they plan to choose]

## Paper Process (P)
**What's required to get a contract signed?**
- **Legal Review**: [Contract approval requirements]
- **Procurement Process**: [Vendor onboarding and compliance]
- **Security Assessment**: [InfoSec and compliance reviews]
- **Implementation Planning**: [Technical and operational preparation]
- **Contract Execution**: [Signature authority and process]

## Implicate Pain (I)
**What happens if they don't solve this problem?**
- **Current Costs**: [Financial impact of status quo]
- **Opportunity Costs**: [What they can't do without a solution]
- **Competitive Risks**: [How this affects market position]
- **Strategic Impact**: [Effect on business objectives]
- **Urgency Drivers**: [Why they need to act now]

## Champion (C)
**Who will advocate for our solution internally?**
- **Champion Name**: [Internal advocate identification]
- **Influence Level**: [Their ability to drive decision]
- **Motivation**: [Why they support our solution]
- **Enablement**: [How we're supporting their advocacy]
- **Access**: [Their relationship with decision makers]

## Competition (C)
**What alternatives are they considering?**
- **Direct Competitors**: [Other vendor solutions]
- **Indirect Alternatives**: [Build vs buy vs status quo]
- **Competitive Advantages**: [Why we're better positioned]
- **Competitive Risks**: [Where others might win]
- **Differentiation Strategy**: [How we stand out]
```

## Usage Guidelines

### Template Selection
- **Start with Basic**: Use fundamental templates for all customers
- **Add Complexity**: Include advanced templates as relationships deepen
- **Customize as Needed**: Adapt templates to specific industries or use cases
- **Version Control**: Track template modifications and approvals

### Data Quality Standards
- **Completeness**: Aim for 80%+ field completion on core templates
- **Accuracy**: Validate information through multiple sources
- **Currency**: Update templates within 48 hours of new information
- **Consistency**: Use standardized formats and terminology
- **Integration**: Ensure data flows properly between templates

### Team Collaboration
- **Shared Access**: Make templates available to all team members
- **Update Protocols**: Define who can modify templates and when
- **Review Process**: Regular template effectiveness assessment
- **Training**: Ensure team understands proper template usage
- **Feedback Loop**: Collect input for template improvements

## Integration with Systems

### CRM Synchronization
- **Salesforce Fields**: Map template data to CRM records
- **Automated Population**: Pull data from integrated systems
- **Real-time Updates**: Sync changes across platforms
- **Data Validation**: Ensure consistency between systems
- **Workflow Triggers**: Automate actions based on template completion

### Tool Connectivity
- **Gong Integration**: Populate call data automatically
- **Granola Sync**: Import meeting notes and action items
- **Slack Updates**: Share template completions with team
- **Email Tracking**: Log communication in interaction templates
- **Calendar Integration**: Schedule follow-ups based on templates

This template system ensures consistent, high-quality customer data management that scales with your growing sales organization.