# Customer Template Structure

This document defines the standardized folder and file structure for all customer profiles in the sales workspace.

## Directory Structure

```
customers/
├── profiles/
│   └── {customer_id}/
│       ├── {customer_id}.md                    # Main customer profile (Standard 40K context)
│       ├── context_summary.md                  # Compact context (5K tokens)
│       ├── context_extended.md                 # Extended context (200K+ tokens)
│       ├── {customer_id}_jury.json            # Structured data for automation
│       ├── pricing_proposal.md                # Current pricing and proposals
│       ├── emails/                            # Email communications
│       │   ├── YYYY-MM-DD_subject.md
│       │   └── email_summary.md
│       ├── gong/                              # Call recordings and analysis
│       │   ├── YYYY-MM-DD_call_title.json
│       │   └── call_analysis_summary.md
│       ├── granola/                           # Meeting notes
│       │   ├── YYYY-MM-DD_meeting_title.md
│       │   └── meeting_summary.md
│       ├── slack/                             # Slack discussions
│       │   ├── YYYY-MM-DD_channel_topic.json
│       │   └── slack_summary.md
│       ├── usage_data/                        # Product usage analytics
│       │   ├── platform_metrics.json
│       │   ├── feature_adoption.json
│       │   └── usage_trends.md
│       ├── support/                           # Support interactions
│       │   ├── tickets/
│       │   └── support_summary.md
│       ├── contracts/                         # Legal documents
│       │   ├── msa.pdf
│       │   ├── dpa.pdf
│       │   ├── current_contract.pdf
│       │   └── contract_timeline.md
│       ├── competitive/                       # Competitive intelligence
│       │   ├── competitive_analysis.md
│       │   ├── win_loss_reports/
│       │   └── battlecards_used.md
│       └── automation/                        # Trigger and automation data
│           ├── trigger_events.json
│           ├── automation_log.md
│           └── alert_history.md
├── templates/                                 # Template files
│   ├── customer_context_compact.md           # 5K token template
│   ├── customer_context_standard.md          # 40K token template
│   ├── customer_context_extended.md          # 200K+ token template
│   ├── new_customer_template.md              # Initial setup template
│   └── CUSTOMER_TEMPLATE_STRUCTURE.md        # This file
└── workflows/                                 # Customer workflow templates
    ├── onboarding_workflow.md
    ├── renewal_workflow.md
    ├── expansion_workflow.md
    └── churn_prevention_workflow.md
```

## Context Window Strategy

### 🎯 **Compact Context (5K tokens)**
**File:** `context_summary.md`  
**Use Cases:** Daily updates, quick checks, mobile usage, trigger responses  
**Contents:**
- Current status and health score
- Recent activity (7 days)
- Key contacts and next actions
- Immediate priorities and risks
- Quick decision-making data

### 📊 **Standard Context (40K tokens)**
**File:** `{customer_id}.md` (main profile)  
**Use Cases:** Meeting preparation, deal analysis, strategic planning  
**Contents:**
- Comprehensive relationship mapping
- 30-day interaction history
- Opportunity analysis
- Product usage patterns
- Account strategy and planning

### 📈 **Extended Context (200K+ tokens)**
**File:** `context_extended.md`  
**Use Cases:** Annual reviews, complex deals, historical analysis, forensic investigation  
**Contents:**
- Complete interaction history
- Full competitive intelligence
- Comprehensive usage analytics
- Detailed financial analysis
- Predictive modeling data

## File Naming Conventions

### Date-Based Files
- **Format:** `YYYY-MM-DD_descriptive_title.ext`
- **Examples:**
  - `2024-07-27_initial_outreach.md`
  - `2024-07-27_poc_results_review.json`
  - `2024-07-27_executive_overview.md`

### Summary Files
- **email_summary.md** - Aggregated email insights
- **call_analysis_summary.md** - Gong call intelligence
- **meeting_summary.md** - Granola meeting outcomes
- **slack_summary.md** - Team discussion insights
- **usage_trends.md** - Product adoption analysis

### Structured Data Files
- **{customer_id}_jury.json** - Machine-readable customer data
- **platform_metrics.json** - Usage analytics
- **trigger_events.json** - Automation history
- **feature_adoption.json** - Product adoption data

## Data Layer Strategy

### Layer 1: Current Context (Always Fresh)
- Health score and risk assessment
- Recent activity and communications
- Active opportunities and next steps
- Immediate action items

### Layer 2: Strategic Context (Updated Weekly)
- Relationship mapping and stakeholder analysis
- Product usage patterns and adoption
- Competitive landscape and positioning
- Account strategy and growth plans

### Layer 3: Historical Context (Updated Monthly)
- Complete interaction timeline
- Long-term trends and patterns
- Strategic milestone history
- Comprehensive analytics

## Automation Integration

### Trigger Data Flow
```
External Systems → trigger_events.json → Context Updates → Alert Generation
```

### Context Refresh Schedule
- **Compact Context:** Real-time updates from triggers
- **Standard Context:** Updated on demand + weekly refresh
- **Extended Context:** Monthly comprehensive rebuild

### Integration Points
- **CRM Sync:** Salesforce/HubSpot → customer profile updates
- **Communication Sync:** Email/Slack → interaction logs
- **Call Sync:** Gong/Granola → meeting intelligence
- **Usage Sync:** Product analytics → adoption metrics

## Quality Assurance

### Data Validation Rules
- All customer_ids must be lowercase with underscores
- Dates must follow YYYY-MM-DD format
- Health scores must be 0-100 with confidence intervals
- Contact information must include role and last interaction

### Consistency Checks
- Cross-reference contact information across files
- Validate opportunity data against CRM records
- Ensure usage data aligns with contract terms
- Confirm trigger events match interaction logs

### Privacy & Security
- No sensitive data in file names
- PII handling follows data classification
- Access controls based on role requirements
- Audit trails for all data access

## Template Usage Guide

### For New Customers
1. Copy `new_customer_template.md` to `customers/profiles/{customer_id}/`
2. Rename to `{customer_id}.md`
3. Initialize with available data from CRM/initial interactions
4. Set up automated data feeds
5. Create initial compact context

### For Existing Customers
1. Migrate existing data to new structure
2. Populate historical interaction logs
3. Establish baseline health metrics
4. Configure trigger monitoring
5. Generate all three context levels

### For Context Generation
1. **Daily:** Update compact context with latest activity
2. **Weekly:** Refresh standard context with comprehensive analysis
3. **Monthly:** Rebuild extended context with full historical view
4. **On-Demand:** Generate context for specific needs (meetings, reviews)

This structure ensures scalable, consistent customer context management while optimizing for different usage patterns and context window constraints.