# Demo Environment Setup Guide

## Overview
This guide ensures your demo environment is always ready to impress prospects with ACME's capabilities.

## Master Demo Environment

### Access Credentials
```bash
# Demo Account
URL: https://demo.acme.app
Username: demo@acme.com
Password: [Stored in 1Password: ACME Demo Account]

# API Access
API_KEY: demo_api_key_2024
API_SECRET: [Stored in 1Password: ACME Demo API]
```

### Pre-configured Scenarios

#### 1. E-commerce Demo (Retail/Fashion)
- **Account**: demo-ecommerce
- **Features**: Auto-scaling, global CDN, A/B testing
- **Data**: 1M products, 100K daily users
- **Performance**: <100ms response time

#### 2. Media Streaming Demo (Entertainment)
- **Account**: demo-media
- **Features**: Video transcoding, edge caching, live streaming
- **Data**: 10K videos, 1M monthly views
- **Performance**: 4K streaming, <2s start time

#### 3. SaaS Application Demo (B2B)
- **Account**: demo-saas
- **Features**: Multi-tenant, API gateway, microservices
- **Data**: 100 tenants, 10K API calls/min
- **Performance**: 99.99% uptime dashboard

#### 4. Financial Services Demo (Fintech)
- **Account**: demo-fintech
- **Features**: Security controls, compliance logs, encryption
- **Data**: Synthetic transactions, audit trails
- **Performance**: <50ms API response

## Demo Data Setup

### Sample Applications
```bash
# Clone demo repositories
git clone https://github.com/acme-demos/nextjs-blog
git clone https://github.com/acme-demos/express-api
git clone https://github.com/acme-demos/static-site
git clone https://github.com/acme-demos/full-stack-app
```

### Performance Benchmarks
Store these for comparison during demos:

| Platform | Deploy Time | Response Time | Cost/Month | Scaling |
|----------|------------|---------------|------------|---------|
| ACME | 25 seconds | 47ms | $2,400 | Automatic |
| Vercel | 2 minutes | 84ms | $3,100 | Manual |
| Netlify | 3 minutes | 91ms | $2,900 | Limited |
| AWS (DIY) | 47 minutes | 120ms | $4,200 | Complex |

### Load Testing Scripts
```bash
# Basic load test
acme-load-test --url https://demo.acme.app --concurrent 1000

# Spike test
acme-load-test --url https://demo.acme.app --pattern spike

# Geographic distribution test
acme-load-test --url https://demo.acme.app --regions all
```

## Customization Checklist

### Before Each Demo
1. **Customer Research**
   - [ ] Industry vertical identified
   - [ ] Current tech stack documented
   - [ ] Pain points understood
   - [ ] Success metrics defined

2. **Environment Prep**
   - [ ] Select appropriate demo template
   - [ ] Customize with customer's branding (if possible)
   - [ ] Prepare relevant code examples
   - [ ] Test all demos flows

3. **Data Preparation**
   - [ ] Load industry-specific sample data
   - [ ] Configure relevant integrations
   - [ ] Set up monitoring dashboards
   - [ ] Prepare comparison metrics

## Demo Flow Templates

### Discovery to Demo Transition
"Based on what you shared about [specific pain point], let me show you exactly how ACME addresses this..."

### Technical Deep Dive Setup
```bash
# For technical audiences
cd ~/demos/technical

# Show infrastructure as code
cat deployment.yaml

# Demonstrate CI/CD integration
cat .github/workflows/deploy.yml

# Show monitoring setup
cat monitoring/config.yaml
```

### Business Value Setup
```bash
# For business audiences
cd ~/demos/business

# Open cost dashboard
open https://demo.acme.app/analytics/costs

# Show performance metrics
open https://demo.acme.app/analytics/performance

# Display ROI calculator
open https://demo.acme.app/calculator
```

## Common Demo Scenarios

### Scenario 1: "Show me how fast deployment is"
```bash
# Terminal 1: Show current (slow) deployment
./legacy-deploy.sh  # Takes 45+ minutes

# Terminal 2: Show ACME deployment
acme deploy  # Takes 25 seconds
```

### Scenario 2: "What about handling traffic spikes?"
```bash
# Show auto-scaling dashboard
open https://demo.acme.app/scaling

# Trigger load test
./spike-test.sh

# Show real-time scaling
watch -n 1 acme status
```

### Scenario 3: "Security is our top concern"
```bash
# Show security dashboard
open https://demo.acme.app/security

# Display audit logs
acme logs --type=audit --last=24h

# Show compliance reports
acme compliance --report=soc2
```

## Troubleshooting Common Issues

### Demo Site Slow/Down
```bash
# Quick health check
acme status --verbose

# Restart demo environment
acme restart demo-environment

# Fallback to backup demo
export DEMO_URL=https://backup-demo.acme.app
```

### Feature Not Working
```bash
# Check feature flags
acme features list

# Enable specific feature
acme features enable [feature-name]

# Clear demo cache
acme cache clear --environment=demo
```

### Customer-Specific Setup Failing
```bash
# Reset to clean state
acme reset --environment=demo

# Use generic demo
acme switch-demo generic

# Have backup screenshots ready
open ~/demos/screenshots/
```

## Post-Demo Actions

### 1. Save Demo State
```bash
# Export demo configuration
acme export-config > demos/[customer-name]-config.json

# Save performance metrics
acme metrics export --format=pdf > [customer-name]-metrics.pdf
```

### 2. Send Follow-up Resources
- Demo recording link
- Performance metrics PDF
- Custom ROI calculation
- Relevant case studies
- Technical documentation links

### 3. Prepare for Next Steps
- Schedule technical deep dive
- Set up POC environment
- Prepare security documentation
- Create custom pricing proposal

## Demo Best Practices

### DO:
- ✅ Test everything 30 minutes before
- ✅ Have backup plans for every demo
- ✅ Keep demos under 20 minutes
- ✅ Leave time for questions
- ✅ Record demos for follow-up

### DON'T:
- ❌ Wing it without preparation
- ❌ Show features they don't need
- ❌ Assume technical knowledge
- ❌ Skip the business value
- ❌ Forget to confirm next steps

---

*Pro tip: The best demos feel like the customer is driving, even though you're guiding the journey.*