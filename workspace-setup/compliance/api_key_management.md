# API Key Management Guide

Secure handling of API keys, tokens, and credentials for sales workspace integrations.

## Overview

API keys are the keys to the kingdom. One exposed key can compromise customer data, damage our reputation, and result in significant costs. This guide provides mandatory procedures for managing integration credentials.

## Key Management Principles

### 1. Never Expose Keys
- ❌ **Never** commit keys to Git repositories
- ❌ **Never** share keys in Slack/email/docs
- ❌ **Never** log keys in debug output
- ❌ **Never** use keys in client-side code
- ✅ **Always** use environment variables
- ✅ **Always** encrypt keys at rest

### 2. Principle of Least Privilege
- Request minimum required permissions
- Use read-only access when possible
- Scope keys to specific resources
- Time-limit access when feasible

### 3. Regular Rotation
- Critical systems: Monthly
- Standard integrations: Quarterly  
- All keys: Annually minimum
- Compromised keys: Immediately

## Integration Inventory

### Current Integrations
| Service | Key Type | Permissions | Rotation Schedule | Owner |
|---------|----------|-------------|-------------------|-------|
| Slack | Bot Token | Read channels, post messages | Quarterly | Sales Ops |
| Gong | API Key + Secret | Read calls, transcripts | Quarterly | Sales Ops |
| Granola | API Key | Read meetings, notes | Quarterly | Sales Ops |
| Salesforce | OAuth | Read/write opportunities | Monthly | Sales Ops |
| Gmail | OAuth | Read emails | Quarterly | Individual |
| HubSpot | API Key | Read/write contacts | Quarterly | Sales Ops |

### Key Storage Locations
```
Environment Variables (.env files - never commit!)
├── SLACK_TOKEN
├── GONG_API_KEY
├── GONG_API_SECRET
├── GRANOLA_API_KEY
├── SALESFORCE_USERNAME
├── SALESFORCE_PASSWORD
├── SALESFORCE_TOKEN
├── GMAIL_CLIENT_ID
├── GMAIL_CLIENT_SECRET
└── HUBSPOT_API_KEY
```

## Setting Up Secure Environment

### Step 1: Create .env File
```bash
# In your workspace root
touch .env
echo ".env" >> .gitignore  # CRITICAL: Add to gitignore
```

### Step 2: Add Keys to .env
```bash
# .env file content
SLACK_TOKEN=xoxb-your-token-here
GONG_API_KEY=your-gong-key
GONG_API_SECRET=your-gong-secret
# ... other keys
```

### Step 3: Create .env.example
```bash
# .env.example (this CAN be committed)
SLACK_TOKEN=your_slack_bot_token
GONG_API_KEY=your_gong_api_key
GONG_API_SECRET=your_gong_api_secret
# ... other keys with placeholders
```

### Step 4: Load Environment Variables
```python
# Python example
import os
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv('SLACK_TOKEN')
if not slack_token:
    raise ValueError("SLACK_TOKEN not found in environment")
```

## Password Manager Setup

### Recommended Tools
1. **1Password** (Company standard)
2. **LastPass** (Alternative)
3. **Bitwarden** (Open source option)

### Storage Structure
```
Sales Workspace/
├── Integration Keys/
│   ├── Slack Bot Token
│   ├── Gong Credentials
│   ├── Granola API Key
│   └── Salesforce OAuth
├── Personal Tokens/
│   ├── GitHub PAT
│   └── Gmail OAuth
└── Shared Credentials/
    └── Demo Accounts
```

### Sharing Keys Securely
1. **Never share directly** - Use password manager
2. **Create shared vaults** - For team access
3. **Set permissions** - Limit who can view/edit
4. **Enable 2FA** - On password manager
5. **Audit access** - Review quarterly

## Key Rotation Procedures

### Planned Rotation

#### Pre-Rotation (Week Before)
1. Generate new key in provider console
2. Store in password manager
3. Test new key in development
4. Schedule rotation window
5. Notify team of upcoming change

#### Rotation Day
1. Update key in all environments
2. Test all integrations
3. Monitor for errors
4. Keep old key for 24h (emergency)
5. Revoke old key after confirmation

#### Post-Rotation
1. Update documentation
2. Confirm all systems working
3. Delete old key from provider
4. Log rotation completion
5. Schedule next rotation

### Emergency Rotation (Compromised Key)

#### Immediate Actions (0-15 min)
1. **Revoke compromised key** immediately
2. **Generate new key** in provider
3. **Update production** environment
4. **Test critical functions**
5. **Document incident**

#### Follow-up (15-60 min)
1. Update all environments
2. Investigate exposure scope
3. Check logs for unauthorized use
4. Notify security team
5. Begin incident report

#### Resolution (1-24 hours)
1. Complete incident report
2. Implement prevention measures
3. Update team on changes
4. Review key management practices
5. Schedule security training

## Integration-Specific Guidelines

### Slack
```bash
# Permissions needed:
- channels:read
- chat:write
- users:read

# Rotation impact: Minor (immediate token swap)
# Test command: curl -H "Authorization: Bearer $SLACK_TOKEN" https://slack.com/api/auth.test
```

### Gong
```bash
# Permissions needed:
- Read call data
- Read transcripts
- Read analytics

# Rotation impact: Medium (uses API key + secret)
# Test: Use Gong API health check endpoint
```

### Salesforce
```bash
# OAuth flow required
# Permissions: API, read/write opportunities
# Rotation: Refresh token rotation
# Impact: High (may affect active sessions)
```

## Security Checklist

### Daily
- [ ] Verify no keys in recent commits
- [ ] Check for keys in Slack messages
- [ ] Ensure .env not tracked in Git

### Weekly  
- [ ] Review access logs for anomalies
- [ ] Test key permissions are minimal
- [ ] Check for unused integrations

### Monthly
- [ ] Rotate high-priority keys
- [ ] Audit password manager access
- [ ] Review integration permissions
- [ ] Update key documentation

### Quarterly
- [ ] Rotate all keys
- [ ] Security training refresh
- [ ] Integration audit
- [ ] Update this guide

## Common Mistakes to Avoid

### 1. Hardcoding Keys
```python
# WRONG - Never do this
api_key = "sk-abc123xyz789"

# RIGHT - Use environment variables
api_key = os.getenv('API_KEY')
```

### 2. Logging Keys
```python
# WRONG - Exposes key in logs
print(f"Using API key: {api_key}")

# RIGHT - Log safely
print(f"Using API key: {api_key[:4]}...{api_key[-4:]}")
```

### 3. Committing .env Files
```bash
# WRONG - .env in repository
git add .env

# RIGHT - .env in .gitignore
echo ".env" >> .gitignore
```

### 4. Sharing Keys Insecurely
```
# WRONG - Slack message
"Hey team, the API key is sk-abc123xyz789"

# RIGHT - Password manager
"I've added the API key to 1Password in the Sales Workspace vault"
```

## Monitoring and Alerts

### Set Up Monitoring
1. **GitHub Secret Scanning** - Automatic
2. **GitGuardian** - Real-time monitoring
3. **Integration Logs** - Usage patterns
4. **Cost Alerts** - Unusual API usage

### Alert Response
- **GitHub Alert**: Rotate immediately
- **Unusual Usage**: Investigate within 1 hour
- **Cost Spike**: Check for leaked keys
- **Failed Auth**: Verify key validity

## Recovery Procedures

### If Key Is Committed to Git
1. Rotate key immediately (don't wait!)
2. Remove from Git history:
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```
3. Force push changes
4. Notify team of repository update
5. Document incident

### If Key Is Shared Insecurely
1. Rotate key immediately
2. Delete message/email containing key
3. Notify recipients to delete
4. Audit key usage in logs
5. Implement additional training

## Best Practices by Role

### Individual Contributors
- Use personal password manager
- Never share your personal tokens
- Report suspected exposures immediately
- Keep development keys separate
- Follow rotation schedule

### Managers
- Audit team key usage quarterly
- Ensure team training completion
- Approve key access requests
- Monitor for policy violations
- Lead by example

### Sales Operations
- Maintain integration inventory
- Coordinate rotation schedule
- Manage shared credentials
- Monitor security alerts
- Update documentation

## Resources and Tools

### Documentation
- [Environment Variable Guide](../integrations/README.md)
- [Integration Setup Guides](../integrations/)
- [Security Policy](./data_security_policy.md)

### Tools
- **direnv**: Auto-load environment variables
- **git-secrets**: Prevent secret commits
- **detect-secrets**: Pre-commit hooks

### Scripts
```bash
# Check for exposed keys
grep -r "api_key\|token\|secret\|password" . \
  --exclude-dir=.git \
  --exclude="*.md" | grep -v ".env.example"

# Rotate all keys (requires setup)
./scripts/rotate_all_keys.sh
```

---

**Remember**: A leaked key is a security incident. When in doubt, rotate it out!

**Owner**: Security Team  
**Last Updated**: [Date]  
**Next Review**: [Monthly]