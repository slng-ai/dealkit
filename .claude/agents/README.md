# Sales Workspace Specialized Agents

This directory contains specialized Claude agents organized by the master sales workspace structure. Each agent is designed to handle specific aspects of sales operations and customer management.

## Directory Structure

```
.claude/agents/
├── customers/          # Customer-focused agents
├── reporting/          # Analytics and reporting agents  
├── sales-toolkit/      # Sales strategy and content agents
└── workspace-setup/    # Integration and architecture agents
```

## 👥 Customer Agents (`/customers/`)

### customer-context-orchestrator.md
**Purpose**: Coordinates comprehensive data collection across all customer touchpoints
**Use When**: Preparing for customer meetings, pipeline reviews, or strategic account planning
**Capabilities**: Multi-source intelligence gathering, meeting preparation, deal analysis

### customer-email-analyzer.md  
**Purpose**: Analyzes email communications with customers for insights and context
**Use When**: Need to understand email sentiment, extract requirements, or track deal progress
**Capabilities**: Email analysis, sentiment detection, requirement extraction, deal status assessment

### customer-onboarding-researcher.md
**Purpose**: Gathers comprehensive information for new customer profiles
**Use When**: Setting up new customer files or enriching existing customer data
**Capabilities**: Salesforce data collection, communication channel setup, contextual research

## 📊 Reporting Agents (`/reporting/`)

### report-generator.md
**Purpose**: Creates comprehensive reports from customer data and sales activities
**Use When**: Need role-specific reports, executive summaries, or performance analysis
**Capabilities**: CRO/CFO/FDE/SDR reports, trigger analytics, pipeline analysis, customer health assessment

## 🎯 Sales Toolkit Agents (`/sales-toolkit/`)

### sales-strategy-advisor.md
**Purpose**: Provides strategic guidance on opportunities and competitive situations
**Use When**: Developing deal strategies, handling competition, or optimizing sales processes
**Capabilities**: Deal strategy, competitive positioning, objection handling, methodology optimization

### content-creator.md
**Purpose**: Creates sales content, templates, and customer-facing materials
**Use When**: Need email sequences, presentations, proposals, or sales collateral
**Capabilities**: Email templates, pitch decks, proposals, battlecards, case studies, playbooks

## 🔧 Workspace Setup Agents (`/workspace-setup/`)

### gong-call-analyzer.md
**Purpose**: Retrieves and analyzes Gong.io call recordings and transcripts
**Use When**: Need insights from customer calls, competitive intelligence, or call analysis
**Capabilities**: Call transcript analysis, pain point identification, buying signal detection

### granola-meeting-analyzer.md
**Purpose**: Fetches and analyzes meeting notes from Granola
**Use When**: Need to extract action items, summarize meetings, or track decisions
**Capabilities**: Meeting note analysis, action item extraction, decision tracking

### project-architecture-organizer.md
**Purpose**: Organizes project structure and maintains architectural patterns
**Use When**: Need to reorganize files, update documentation, or improve project structure
**Capabilities**: File organization, README creation, architectural pattern establishment

### slack-context-analyzer.md
**Purpose**: Searches and analyzes Slack conversations for customer context
**Use When**: Need insights from team discussions, customer mentions, or historical context
**Capabilities**: Message search, conversation analysis, sentiment tracking, action item identification

## 🚀 Usage Patterns

### For Customer Research
1. **customer-onboarding-researcher** → Set up comprehensive customer profile
2. **customer-email-analyzer** → Analyze recent email communications  
3. **gong-call-analyzer** → Review recent call insights
4. **slack-context-analyzer** → Gather team discussion context
5. **customer-context-orchestrator** → Synthesize all data for strategic insights

### For Deal Strategy
1. **sales-strategy-advisor** → Develop overall deal approach
2. **content-creator** → Create customer-specific materials
3. **customer-context-orchestrator** → Prepare for customer interactions
4. **report-generator** → Generate executive briefings

### For Performance Analysis
1. **report-generator** → Create role-specific performance reports
2. **gong-call-analyzer** → Analyze call effectiveness
3. **customer-email-analyzer** → Track email engagement trends
4. **sales-strategy-advisor** → Optimize sales processes

### For Workspace Management
1. **project-architecture-organizer** → Maintain clean file structure
2. **slack-context-analyzer** → Monitor team communications
3. **granola-meeting-analyzer** → Track meeting outcomes

## 🎯 Agent Selection Guide

**Choose based on your immediate need:**

| Need | Primary Agent | Supporting Agents |
|------|---------------|------------------|
| Customer meeting prep | customer-context-orchestrator | customer-email-analyzer, gong-call-analyzer |
| Deal strategy | sales-strategy-advisor | customer-context-orchestrator, content-creator |
| Executive reporting | report-generator | customer-context-orchestrator |
| Content creation | content-creator | sales-strategy-advisor |
| Customer research | customer-onboarding-researcher | customer-email-analyzer, slack-context-analyzer |
| Call analysis | gong-call-analyzer | customer-context-orchestrator |
| Project organization | project-architecture-organizer | - |

## 🔄 Integration with Sales Workspace

These agents are designed to work seamlessly with the sales workspace structure:

- **Customer data** flows between agents and customer profiles
- **Trigger events** inform agent recommendations
- **Report insights** feed back into customer context
- **Sales toolkit** content is created and maintained by agents
- **Workspace organization** is maintained automatically

Each agent understands the workspace structure and can navigate between customers, sales-toolkit resources, reporting data, and workspace configuration as needed.