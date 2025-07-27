# ICP (Ideal Customer Profile)

Who we're targeting and how to prioritize.

## Purpose
This section defines our ideal customer profiles, helping sales teams identify high-value prospects, qualify opportunities effectively, and focus efforts on accounts most likely to succeed with Your Company.

## Key Salesforce Fields
- **Target Account Tier**: 1 (Strategic), 2 (Enterprise), 3 (Growth)
- **Type**: New Business, Expansion, Renewal
- **Needs**: Specific use cases and requirements
- **Industry**: Vertical classification
- **Company Size**: Employee count and revenue
- **Modality**: Text, Image, Audio, Video, Multimodal

## Tier 1: Strategic Accounts

### Profile
- **Revenue**: $1B+ or high-growth unicorns
- **ML Maturity**: Dedicated ML/AI teams
- **Use Cases**: Mission-critical, customer-facing
- **Volume**: Millions of inferences/day
- **Budget**: $500K+ annual spend capability

### Examples
- Large financial institutions (fraud detection)
- Major e-commerce platforms (recommendations)
- Social media companies (content moderation)
- Enterprise SaaS (AI features)

### Why They Buy
- Need enterprise SLAs and support
- Require dedicated infrastructure
- Value engineering partnership
- Cost optimization at scale
- Compliance requirements

## Tier 2: Enterprise Accounts

### Profile
- **Revenue**: $100M-$1B
- **ML Maturity**: Growing ML initiatives
- **Use Cases**: Product differentiation
- **Volume**: Thousands to millions/day
- **Budget**: $100K-$500K annual

### Examples
- Mid-market SaaS companies
- Digital health platforms
- Online education companies
- Gaming studios
- Fintech startups

### Why They Buy
- Scaling challenges
- Need expertise and guidance
- Want to focus on ML, not infrastructure
- Cost predictability
- Faster time to market

## Tier 3: Growth Accounts

### Profile
- **Revenue**: $10M-$100M
- **ML Maturity**: Early ML adoption
- **Use Cases**: Experimental to production
- **Volume**: Hundreds to thousands/day
- **Budget**: $20K-$100K annual

### Examples
- Series A/B startups
- AI-first companies
- Digital agencies
- Small gaming studios
- Niche SaaS tools

### Why They Buy
- Need to move fast
- Limited engineering resources
- Pay-as-you-go flexibility
- Proof of concept success
- Developer experience

## Use Case Patterns

### By Industry

#### Financial Services
- **Pain Points**: Latency requirements, compliance, scale
- **Use Cases**: Fraud detection, risk scoring, document processing
- **Key Metrics**: False positive rates, processing speed
- **Competition**: In-house, SageMaker

#### Healthcare/Life Sciences
- **Pain Points**: HIPAA compliance, accuracy, explainability
- **Use Cases**: Medical imaging, clinical NLP, drug discovery
- **Key Metrics**: Accuracy, throughput, compliance
- **Competition**: Cloud providers, specialized vendors

#### E-commerce/Retail
- **Pain Points**: Peak scaling, personalization, cost
- **Use Cases**: Recommendations, visual search, dynamic pricing
- **Key Metrics**: Conversion rates, latency, cost per inference
- **Competition**: In-house, Replicate

#### Media/Entertainment
- **Pain Points**: Content volume, real-time needs, global distribution
- **Use Cases**: Content moderation, generation, personalization
- **Key Metrics**: Processing speed, accuracy, scale
- **Competition**: Modal, internal tools

#### Gaming
- **Pain Points**: Latency, player experience, dynamic content
- **Use Cases**: AI NPCs, procedural generation, anti-cheat
- **Key Metrics**: Response time, player engagement
- **Competition**: Game-specific solutions

### By Technical Pattern

#### Real-time Inference
- Sub-100ms latency requirements
- High availability needs
- Global distribution
- Example: Fraud detection, chatbots

#### Batch Processing
- Large volume processing
- Cost optimization focus
- Flexible timing
- Example: Data enrichment, analytics

#### Edge Deployment
- Local processing needs
- Privacy requirements
- Offline capability
- Example: Mobile apps, IoT

#### Multi-model Pipelines
- Complex workflows
- Multiple model types
- Orchestration needs
- Example: Document processing

## Disqualifiers

### Poor Fit Indicators
- No clear ML use case
- Extremely regulated (government)
- Require on-premise only
- Budget <$10K annually
- Looking for consulting, not platform

### Technical Misalignment
- Proprietary hardware requirements
- Exotic model architectures
- Non-standard deployment needs
- Real-time training requirements

## Prioritization Framework

### Scoring Model
1. **Use Case Fit** (0-10)
   - Clear ML need
   - Matches our strengths
   - Scalability requirements

2. **Commercial Fit** (0-10)
   - Budget availability
   - Decision timeline
   - Growth potential

3. **Technical Fit** (0-10)
   - Supported models
   - Integration feasibility
   - Performance requirements

4. **Strategic Value** (0-10)
   - Logo value
   - Expansion potential
   - Market influence

### Action by Score
- **35-40**: Immediate priority, full resources
- **25-34**: Active pursuit, standard process
- **15-24**: Nurture, automated touches
- **<15**: Decline or refer

## Trigger Events

### Company Triggers
- Funding rounds (especially B+)
- New AI/ML leadership hire
- Product launches with AI
- Public AI commitments
- Competitive pressure

### Technical Triggers
- Scaling challenges mentioned
- Cost complaints about current solution
- Security/compliance initiatives
- Performance issues
- New ML team formation

### Market Triggers
- Competitor adopts AI
- Regulatory changes
- Industry disruption
- Customer expectations shift

## Account Research Checklist

### Company Level
- [ ] Industry and vertical
- [ ] Revenue and growth rate
- [ ] Funding and investors
- [ ] Recent news and announcements
- [ ] Tech stack indicators

### ML Maturity
- [ ] ML team size
- [ ] Current ML use cases
- [ ] Public AI initiatives
- [ ] Job postings for ML roles
- [ ] Technical blog/papers

### Stakeholders
- [ ] Head of ML/AI
- [ ] VP Engineering
- [ ] CTO/VP Product
- [ ] CFO (for large deals)

## Common Prompts
- "Is [Company] a good fit for Your Company?"
- "What tier is [Company] based on [criteria]?"
- "What use cases should I probe for [industry]?"
- "What are the disqualifiers for [Company]?"
- "How should I prioritize [list of accounts]?"

## Related Sections
- [Discovery](../discovery/) - Qualifying against ICP
- [Competitor Analysis](../competitor_analysis/) - ICP overlap with competitors
- [Pricing](../pricing/) - Tier-based pricing strategies
- [Sales Frameworks](../sales_frameworks/) - ICP in qualification