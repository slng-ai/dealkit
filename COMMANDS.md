# Command Reference Guide

Quick commands and shortcuts for daily sales workspace operations.

## 🚀 Essential Commands

### Setup & Configuration
```bash
# Initial setup
./workspace-setup/scripts/setup.sh

# Run workspace audit
python workspace-setup/scripts/audit_workspace.py

# Navigate workspace
./workspace-setup/scripts/navigate.sh [command] [args]
```

### Customer Operations
```bash
# View customer profile
cat customers/{customer-name}/profile.json

# Generate customer context
python generate_context.py --customer "acme-corp" --size "standard"

# Search customers
find customers -name "*acme*" -type d

# Check customer health
grep -i "health_score" customers/*/profile.json
```

### Daily Reports
```bash
# Morning brief
python reporting/pulse/morning_brief.py --user-id {your_id}

# Deal alerts
python reporting/pulse/deal_alert.py --urgent-only

# Personal performance
python reporting/personal/ae_report.py

# Team dashboard
python reporting/team/vp_sales_report.py
```

### Content & Templates
```bash
# Find email templates
ls sales-toolkit/templates/email_*.md

# Search for specific content
grep -r "follow-up" sales-toolkit/templates/

# View battlecard
cat sales-toolkit/battlecards/{competitor}_battlecard.md

# Find demo scripts
find sales-toolkit -name "*demo*.md" -type f
```

## 🔍 Search Patterns

### Find by Type
```bash
# All JSON configs
find . -name "*.json" -not -path "./venv/*"

# Python scripts
find reporting -name "*.py" -type f

# Customer profiles
find customers -name "profile.json"

# Email templates
find sales-toolkit -name "*email*.md"
```

### Advanced Searches
```bash
# High-value deals
grep -r "deal_size.*[0-9][0-9][0-9][0-9][0-9][0-9]" customers/

# Stalled opportunities
grep -r "stage.*negotiation" customers/*/profile.json | \
xargs grep -l "last_interaction" | \
xargs -I {} sh -c 'echo {} $(date -r {} +%s)'

# Win patterns
grep -r "closed_won" customers/*/profile.json
```

## ⚡ Command Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Navigation shortcuts
alias ws='cd ~/sales-workspace'
alias wsc='cd ~/sales-workspace/customers'
alias wsr='cd ~/sales-workspace/reporting'
alias wst='cd ~/sales-workspace/sales-toolkit'

# Report shortcuts
alias brief='python ~/sales-workspace/reporting/pulse/morning_brief.py'
alias deals='python ~/sales-workspace/reporting/pulse/deal_alert.py'
alias audit='python ~/sales-workspace/workspace-setup/scripts/audit_workspace.py'

# Quick searches
alias findcustomer='find ~/sales-workspace/customers -name'
alias findtemplate='find ~/sales-workspace/sales-toolkit/templates -name'
```

## 📊 Reporting Commands

### Personal Reports (Daily)
```bash
# SDR daily report
python reporting/personal/sdr_report.py --date today

# AE pipeline review
python reporting/personal/ae_report.py --include-forecast

# FDE technical status
python reporting/personal/fde_report.py --customer {name}
```

### Team Reports (Weekly)
```bash
# CRO dashboard
python reporting/team/cro_report.py --period week

# CFO metrics
python reporting/team/cfo_report.py --include-forecast

# Sales ops analysis
python reporting/team/sales_ops_report.py --deep-dive
```

### Pulse Reports (Real-time)
```bash
# All alerts
python reporting/pulse/deal_alert.py --all

# Critical only
python reporting/pulse/deal_alert.py --critical

# Customer health
python reporting/pulse/customer_health_alert.py
```

## 🛠️ Integration Commands

### Slack Monitoring
```bash
# Start Slack fetcher
./workspace-setup/integrations/slack/start_slack_fetcher.sh

# Check Slack status
./workspace-setup/integrations/slack/monitor_slack_fetcher.sh

# View recent mentions
cat customers/*/slack/mentions_*.json | jq '.[] | select(.importance=="high")'
```

### CRM Sync
```bash
# Manual sync
python workspace-setup/integrations/salesforce/sync.py

# Check sync status
python workspace-setup/integrations/check_sync_status.py

# Force update
python workspace-setup/integrations/force_sync.py --customer {name}
```

## 🔧 Maintenance Commands

### Workspace Health
```bash
# Full audit
python workspace-setup/scripts/audit_workspace.py

# Quick structure check
find . -type d -name "*_*" | grep -v "__pycache__"

# Check naming conventions
python workspace-setup/scripts/audit_workspace.py --naming-only
```

### Cleanup
```bash
# Remove temp files
find . -name "*.tmp" -o -name "*.bak" -delete

# Archive old data
find customers/*/slack -name "*.json" -mtime +30 -exec gzip {} \;

# Clean logs
find logs -name "*.log" -mtime +7 -delete
```

## 💡 Power User Tips

### Batch Operations
```bash
# Update all customer health scores
for customer in customers/*/; do
  python update_health.py --customer $(basename "$customer")
done

# Generate all contexts
find customers -name "profile.json" | while read profile; do
  customer=$(dirname "$profile" | xargs basename)
  python generate_context.py --customer "$customer" --all-sizes
done
```

### Pipeline Analysis
```bash
# Total pipeline value
jq '[.deal_size] | add' customers/*/profile.json | paste -sd+ | bc

# Average deal size
jq '.deal_size' customers/*/profile.json | \
awk '{sum+=$1; count++} END {print sum/count}'

# Stage distribution
jq -r '.stage' customers/*/profile.json | sort | uniq -c
```

## 🚨 Emergency Commands

### Deal Recovery
```bash
# Find stalled deals
python reporting/pulse/deal_alert.py --stalled --days 14

# Generate recovery plan
python generate_recovery.py --customer {name} --priority high
```

### Quick Diagnostics
```bash
# Check all integrations
python workspace-setup/integrations/health_check.py

# Verify data freshness
find customers -name "*.json" -mtime +1 | wc -l

# System status
python workspace-setup/scripts/system_status.py
```

---

**Pro tip**: Save frequently used command combinations as shell scripts in `personal/scripts/` for even faster access!