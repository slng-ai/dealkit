# ICP by Model Type

Segmentation based on the types of models customers need to deploy.

## Large Language Models (LLMs)

### Customer Profile
- **Industries**: Tech, media, customer service, legal
- **Company Size**: Series B+ or $100M+ revenue
- **Technical Maturity**: Have ML team, understand transformers

### Use Cases
- Chatbots and conversational AI
- Content generation and summarization
- Code generation and review
- Semantic search and retrieval
- Document analysis

### Technical Requirements
- **Model Sizes**: 7B to 70B+ parameters
- **Latency Needs**: 100ms - 5s acceptable
- **Throughput**: 10-10K requests/minute
- **Features**: Streaming, function calling, RAG

### Pain Points
- Cost of GPT-4/Claude API
- Need for customization/fine-tuning
- Data privacy concerns
- Latency for real-time applications
- Rate limits on commercial APIs

### Qualifying Questions
1. "What's your current spend on OpenAI/Anthropic?"
2. "Do you need to keep data in your environment?"
3. "Have you fine-tuned any open source models?"
4. "What latency requirements do you have?"

### Competition
- OpenAI/Anthropic APIs
- Replicate
- Modal
- In-house deployment

---

## Computer Vision

### Customer Profile
- **Industries**: Manufacturing, healthcare, retail, security
- **Company Size**: $50M+ revenue
- **Technical Maturity**: May have limited ML expertise

### Use Cases
- Quality inspection
- Medical imaging
- Object detection/tracking
- Face recognition
- Document OCR
- Visual search

### Technical Requirements
- **Model Types**: CNNs, Vision Transformers, YOLO
- **Latency Needs**: <100ms critical
- **Throughput**: 100-100K images/hour
- **Features**: Batch processing, real-time streaming

### Pain Points
- Real-time processing requirements
- High accuracy needs
- Large image sizes
- Edge deployment needs
- Multi-camera orchestration

### Qualifying Questions
1. "What's your current image processing pipeline?"
2. "Do you need real-time or batch processing?"
3. "What accuracy rates are you targeting?"
4. "Do you need edge deployment?"

### Competition
- AWS Rekognition
- Google Vision AI
- Azure Computer Vision
- Specialized vendors

---

## Speech & Audio

### Customer Profile
- **Industries**: Call centers, media, healthcare, legal
- **Company Size**: 500+ employees
- **Technical Maturity**: Varies widely

### Use Cases
- Speech-to-text transcription
- Voice authentication
- Call analytics
- Real-time translation
- Audio classification
- Voice synthesis

### Technical Requirements
- **Model Types**: Whisper, Wav2Vec, custom ASR
- **Latency Needs**: Real-time critical
- **Throughput**: Hours of audio daily
- **Features**: Streaming, multi-language

### Pain Points
- Real-time transcription latency
- Accuracy with accents/noise
- Multi-language support
- HIPAA compliance for healthcare
- Integration with telephony

### Qualifying Questions
1. "What's your current transcription accuracy?"
2. "Do you need real-time or batch processing?"
3. "How many languages do you support?"
4. "What's your audio quality like?"

### Competition
- AWS Transcribe
- Google Speech-to-Text
- Azure Speech Services
- Rev.ai, Deepgram

---

## Multimodal Models

### Customer Profile
- **Industries**: E-commerce, media, tech, education
- **Company Size**: Typically larger, $100M+
- **Technical Maturity**: Advanced ML teams

### Use Cases
- Image captioning
- Visual question answering
- Document understanding
- Video analysis
- Product search
- Content moderation

### Technical Requirements
- **Model Types**: CLIP, BLIP, Flamingo, custom
- **Latency Needs**: Varies by use case
- **Throughput**: Mixed modality inputs
- **Features**: Complex preprocessing

### Pain Points
- Complexity of deployment
- Resource requirements
- Lack of tooling
- Integration challenges
- Cost at scale

### Qualifying Questions
1. "What modalities do you need to process?"
2. "Do you have existing multimodal models?"
3. "What's your use case for combining modalities?"
4. "What scale are you operating at?"

### Competition
- Limited direct competition
- Often build in-house
- Cloud provider offerings emerging

---

## Traditional ML/Tabular

### Customer Profile
- **Industries**: Finance, insurance, retail, logistics
- **Company Size**: Any size
- **Technical Maturity**: Often have data scientists

### Use Cases
- Fraud detection
- Risk scoring
- Demand forecasting
- Recommendation engines
- Churn prediction
- Price optimization

### Technical Requirements
- **Model Types**: XGBoost, Random Forest, Neural networks
- **Latency Needs**: <50ms common
- **Throughput**: Very high (millions/day)
- **Features**: A/B testing, monitoring

### Pain Points
- Scale and performance
- Real-time feature computation
- Model versioning
- A/B testing infrastructure
- Monitoring and drift detection

### Qualifying Questions
1. "How many predictions do you serve daily?"
2. "What's your latency requirement?"
3. "How do you handle model updates?"
4. "Do you need real-time features?"

### Competition
- SageMaker
- Vertex AI
- DataBricks
- In-house solutions

---

## Generative AI (Images/Video)

### Customer Profile
- **Industries**: Media, gaming, e-commerce, marketing
- **Company Size**: Series A+ startups to enterprise
- **Technical Maturity**: Experimental to advanced

### Use Cases
- Image generation
- Video generation
- Style transfer
- Image editing
- Avatar creation
- Product visualization

### Technical Requirements
- **Model Types**: Stable Diffusion, DALL-E, custom GANs
- **Latency Needs**: 5-30s acceptable
- **Throughput**: Varies widely
- **Features**: GPU optimization crucial

### Pain Points
- GPU costs
- Generation time
- Quality consistency
- NSFW filtering
- Rights and attribution

### Qualifying Questions
1. "What's your use case for generated content?"
2. "What quality/resolution do you need?"
3. "What's your budget per generation?"
4. "Do you need content filtering?"

### Competition
- Replicate
- Modal
- Stability AI
- Midjourney API

---

## Scoring by Model Type

### Highest Value (Score 9-10)
- **LLMs**: High volume, cost sensitive
- **Real-time Vision**: Latency critical
- **Multimodal**: Complex, limited alternatives

### Medium Value (Score 6-8)
- **Speech/Audio**: Specialized needs
- **Traditional ML**: High scale
- **Batch Vision**: Cost optimization

### Lower Value (Score 3-5)
- **Simple models**: Commoditized
- **Low volume**: Limited budget
- **Experimental**: Not production ready

---

## Cross-Sell Opportunities

### LLM → Vision
"Since you're using LLMs for document processing, have you considered adding visual understanding?"

### Vision → Multimodal
"Your image classification could benefit from text context - worth exploring?"

### Traditional ML → LLMs
"Your recommendation engine could be enhanced with semantic understanding..."

### Any → Multiple
"Most customers end up deploying 3-4 model types within 6 months..."