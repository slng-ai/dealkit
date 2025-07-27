# Pricing

For structuring deals with the right financial profile.

## Purpose
This section provides comprehensive pricing guidance, deal structuring strategies, and financial frameworks to maximize value capture while ensuring customer success. Understanding pricing flexibility and value drivers enables confident commercial conversations.

## Key Salesforce Fields
- **Amount**: Total contract value (TCV)
- **Total ARR**: Annual recurring revenue
- **Annual License Fee**: Platform/base fee
- **Annualized Commitment**: Committed usage value
- **Estimated Usage (Sales)**: Expected variable usage
- **Contract Term**: Length in months

## Pricing Structure

### Base Components

#### 1. Platform Fee
- **Starter**: $0/month (pay-as-you-go)
- **Growth**: $X/month (includes credits)
- **Pro**: Custom (includes reserved capacity)
- **Enterprise**: Custom (dedicated infrastructure)

#### 2. Usage-Based Pricing
- **CPU Inference**: $X per hour
- **GPU Inference**: Varies by type
  - T4: $X/hour
  - A10G: $X/hour  
  - A100: $X/hour
  - H100: $X/hour
- **Storage**: $X per GB/month
- **Egress**: $X per GB

#### 3. Committed Use Discounts
- 20% off: $10K+ monthly commit
- 30% off: $25K+ monthly commit
- 40% off: $50K+ monthly commit
- 50% off: $100K+ monthly commit

### Pricing Calculators

#### Simple Estimator
```
Monthly Cost = Platform Fee + (Inference Hours × Rate) + Storage + Egress

Example:
- Pro Platform: $2,000
- 1,000 A10G hours: $3,000
- 500GB storage: $50
- Total: $5,050/month
```

#### Token-Based Pricing
```
Cost per Million Tokens = (Model Size × GPU Rate) / Throughput

Example (Llama 70B):
- A100 rate: $3/hour
- Throughput: 1M tokens/hour
- Cost: $3 per million tokens
```

## Deal Structuring Strategies

### Growth Accounts (<$100K ARR)
- **Structure**: Pay-as-you-go with credits
- **Terms**: Monthly or annual
- **Discounts**: Volume-based automatic
- **Focus**: Ease of adoption

### Enterprise Accounts ($100K-$500K ARR)
- **Structure**: Platform + committed usage
- **Terms**: Annual minimum
- **Discounts**: 20-40% based on commit
- **Focus**: Predictability and scale

### Strategic Accounts (>$500K ARR)
- **Structure**: Custom enterprise agreement
- **Terms**: Multi-year preferred
- **Discounts**: 40-50%+ possible
- **Focus**: Partnership and growth

## Value-Based Pricing Conversations

### ROI Framework
1. **Current State Costs**
   - Infrastructure: $X/month
   - Engineering time: Y hours × $Z/hour
   - Opportunity cost: Lost revenue/delays

2. **With Your Company**
   - Infrastructure: 50-80% reduction
   - Engineering time: 90% reduction
   - Time to market: 10x faster

3. **Net Value Creation**
   - Direct savings: $X/month
   - Productivity gains: $Y/month
   - Revenue acceleration: $Z/month
   - Total ROI: XX% in Y months

### Value Drivers by Use Case

#### Real-time Inference
- Latency improvement → conversion increase
- Scale handling → revenue capture
- Reliability → customer satisfaction

#### Batch Processing
- Cost per inference reduction
- Processing speed increase
- Resource optimization

#### Development Velocity
- Faster deployment → quicker iteration
- Less maintenance → more feature development
- Better tooling → happier developers

## Pricing Objection Responses

### "Too Expensive"
1. **Reframe to ROI**: "Let's look at total cost of ownership..."
2. **Unbundle value**: "Which specific capabilities drive the most value?"
3. **Phase approach**: "We can start smaller and scale..."
4. **Compare alternatives**: "Versus building in-house..."

### "Cheaper Competitor"
1. **TCO comparison**: Include hidden costs
2. **Performance metrics**: Cost per successful inference
3. **Risk factors**: Reliability, support, scale
4. **Proof points**: Customer switch stories

### "Need Better Terms"
1. **Volume commits**: Larger commit = better rate
2. **Term length**: Longer term = better rate
3. **Payment terms**: Annual prepay = discount
4. **Growth commits**: Built-in expansion pricing

## Contract Structuring

### Standard Terms
- **Payment**: Net 30
- **Commits**: Monthly or annual
- **Overages**: Same rate or step-down
- **True-up**: Quarterly or annual
- **Renewal**: Auto-renew with notice

### Negotiation Levers
1. **Discount for**:
   - Longer terms (2-3 years)
   - Upfront payment
   - Case study rights
   - Reference-ability

2. **Flexibility on**:
   - Payment terms
   - Commit adjustments
   - Credit rollover
   - Termination rights

### Deal Sweeteners
- Free PoC credits
- Extended trial period
- Training and onboarding
- Priority support
- Early access features

## Financial Metrics

### Key Ratios
- **Gross Margin**: ~70-80% target
- **Payback Period**: <12 months ideal
- **LTV:CAC**: >3:1 minimum
- **Net Dollar Retention**: >120% goal

### Deal Scoring
- **Deal Size**: ARR amount
- **Margin Quality**: Gross margin %
- **Growth Potential**: Expansion likelihood
- **Strategic Value**: Logo, market impact

## Approval Matrix

### Discount Authority
- **0-20%**: AE discretion
- **20-30%**: Sales manager
- **30-40%**: VP Sales
- **40%+**: CEO/CFO

### Non-Standard Terms
- **Payment terms**: Finance approval
- **Custom SLAs**: Engineering input
- **Liability changes**: Legal review
- **Unique commits**: RevOps modeling

## Common Pricing Scenarios

### Scenario 1: Startup with Variable Load
```
Structure: Low platform + pay-as-you-go
- Starter plan: $0/month
- Usage credits: $1,000 to start
- Autoscale enabled
- Monthly reconciliation
```

### Scenario 2: Enterprise Migration
```
Structure: Committed use with migration support
- Pro platform: $5,000/month
- Committed usage: $20,000/month (30% discount)
- Migration credits: $10,000
- Annual contract with quarterly true-up
```

### Scenario 3: Strategic Partnership
```
Structure: Enterprise agreement with growth incentives
- Enterprise platform: Custom
- Base commit: $1M annual (45% discount)
- Growth tiers with increasing discounts
- 3-year term with annual escalators
```

## Pricing Communication Tips

### Email Templates
```
"Based on your usage patterns, I recommend:
- [Platform tier] at $X/month
- Estimated usage of Y hours = $Z
- Total monthly: ~$XX,XXX
- With annual commit: $XX,XXX (30% savings)"
```

### Executive Positioning
"Our pricing aligns with value creation:
- Performance improvements drive revenue
- Cost optimization improves margins  
- Faster deployment accelerates roadmap
- Investment pays back in X months"

## Related Sections
- [ICP](../icp/) - Pricing by customer tier
- [Competitor Analysis](../competitor_analysis/) - Competitive pricing
- [PoC Framework](../poc_framework/) - PoC credit strategies
- [Agreements & Contracts](../agreements_contracts/) - Legal terms