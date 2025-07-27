from .base_report import BaseReport
from typing import Dict, Any, List
import json

class FDEReport(BaseReport):
    """Forward Deployed Engineer Report - Technical deep dive"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Executive Summary for FDE
        report += self.format_section(
            "Technical Overview",
            self._generate_technical_summary(context)
        )
        
        # Use Case Analysis
        report += self.format_section(
            "Use Case Details",
            self._analyze_use_cases(context)
        )
        
        # Model Requirements
        report += self.format_section(
            "Model & Infrastructure Requirements",
            self._analyze_model_requirements(context)
        )
        
        # Data Pipeline
        report += self.format_section(
            "Data Pipeline & Volumes",
            self._analyze_data_pipeline(context)
        )
        
        # Technical Challenges
        report += self.format_section(
            "Technical Challenges & Solutions",
            self._identify_technical_challenges(context)
        )
        
        # Integration Points
        report += self.format_section(
            "Integration Requirements",
            self._analyze_integrations(context)
        )
        
        # POC/Implementation Plan
        report += self.format_section(
            "POC & Implementation Roadmap",
            self._generate_implementation_plan(context)
        )
        
        return report
    
    def _generate_technical_summary(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        summary = ""
        summary += self.format_metric("Primary Use Case", customer_data.get('use_case', 'Not defined'))
        summary += self.format_metric("ML Maturity Level", self._assess_ml_maturity(context))
        summary += self.format_metric("Current Infrastructure", self._get_infrastructure_info(context))
        summary += self.format_metric("Technical Readiness", self._calculate_technical_readiness(context) + "/10")
        
        return summary
    
    def _analyze_use_cases(self, context: Dict[str, Any]) -> str:
        use_cases = []
        
        # Extract from various sources
        # From Gong calls
        gong_data = context.get('interactions', {}).get('gong', {})
        for call in gong_data.get('calls', []):
            if 'use_case' in call:
                use_cases.append(call['use_case'])
        
        # From meeting notes
        granola_data = context.get('interactions', {}).get('granola', {})
        for note in granola_data.get('notes', []):
            if 'use_case' in note:
                use_cases.append(note['use_case'])
        
        content = "### Identified Use Cases\n\n"
        
        if not use_cases:
            content += "⚠️ No specific use cases documented yet. Schedule technical discovery call.\n\n"
        else:
            for i, use_case in enumerate(use_cases, 1):
                content += f"**{i}. {use_case.get('name', 'Unnamed Use Case')}**\n"
                content += f"- **Models:** {use_case.get('models', 'TBD')}\n"
                content += f"- **Data Volume:** {use_case.get('data_volume', 'TBD')}\n"
                content += f"- **Latency Requirements:** {use_case.get('latency', 'TBD')}\n"
                content += f"- **Business Impact:** {use_case.get('impact', 'TBD')}\n\n"
        
        # Add recommendations
        content += "### Recommended Next Steps\n"
        content += "1. Deep dive on model architecture and requirements\n"
        content += "2. Benchmark current performance metrics\n"
        content += "3. Define success criteria for POC\n"
        
        return content
    
    def _analyze_model_requirements(self, context: Dict[str, Any]) -> str:
        content = "### Model Specifications\n\n"
        
        # Model types
        content += "**Model Types Discussed:**\n"
        content += "- Computer Vision: ❓ Needs clarification\n"
        content += "- NLP/LLMs: ❓ Needs clarification\n"
        content += "- Tabular/Classical ML: ❓ Needs clarification\n"
        content += "- Custom/Proprietary: ❓ Needs clarification\n\n"
        
        # Framework requirements
        content += "**Framework Requirements:**\n"
        content += "- PyTorch: ❓\n"
        content += "- TensorFlow: ❓\n"
        content += "- JAX: ❓\n"
        content += "- Scikit-learn: ❓\n\n"
        
        # Compute requirements
        content += "**Compute Requirements:**\n"
        content += "- GPU Type: ❓ (A100, V100, T4, etc.)\n"
        content += "- Memory Requirements: ❓\n"
        content += "- Batch vs Real-time: ❓\n"
        content += "- Expected QPS: ❓\n"
        
        return content
    
    def _analyze_data_pipeline(self, context: Dict[str, Any]) -> str:
        content = "### Data Pipeline Analysis\n\n"
        
        content += "**Data Sources:**\n"
        content += "- Primary: ❓ Needs discovery\n"
        content += "- Secondary: ❓ Needs discovery\n\n"
        
        content += "**Data Volumes:**\n"
        content += "- Training Data: ❓ TB/GB\n"
        content += "- Inference Volume: ❓ requests/day\n"
        content += "- Data Growth Rate: ❓ % monthly\n\n"
        
        content += "**Processing Requirements:**\n"
        content += "- Preprocessing Steps: ❓\n"
        content += "- Feature Engineering: ❓\n"
        content += "- Data Validation: ❓\n"
        
        return content
    
    def _identify_technical_challenges(self, context: Dict[str, Any]) -> str:
        content = "### Identified Challenges\n\n"
        
        # Extract from conversations
        challenges = []
        action_items = context.get('action_items', [])
        for item in action_items:
            if 'technical' in item.get('text', '').lower():
                challenges.append(item['text'])
        
        if challenges:
            for challenge in challenges:
                content += f"- {challenge}\n"
        else:
            content += "No specific technical challenges documented yet.\n"
        
        content += "\n### Common Challenges to Explore\n"
        content += "- Model versioning and rollback\n"
        content += "- A/B testing infrastructure\n"
        content += "- Monitoring and observability\n"
        content += "- Cost optimization\n"
        content += "- Security and compliance\n"
        
        return content
    
    def _analyze_integrations(self, context: Dict[str, Any]) -> str:
        content = "### Integration Points\n\n"
        
        content += "**Data Sources:**\n"
        content += "- [ ] S3/Cloud Storage\n"
        content += "- [ ] Streaming (Kafka/Kinesis)\n"
        content += "- [ ] Databases\n"
        content += "- [ ] APIs\n\n"
        
        content += "**Model Serving:**\n"
        content += "- [ ] REST API\n"
        content += "- [ ] gRPC\n"
        content += "- [ ] Batch Processing\n"
        content += "- [ ] Edge Deployment\n\n"
        
        content += "**Monitoring:**\n"
        content += "- [ ] Datadog\n"
        content += "- [ ] Prometheus\n"
        content += "- [ ] CloudWatch\n"
        content += "- [ ] Custom Dashboards\n"
        
        return content
    
    def _generate_implementation_plan(self, context: Dict[str, Any]) -> str:
        content = "### Suggested POC Timeline\n\n"
        
        content += "**Phase 1: Discovery (Week 1-2)**\n"
        content += "- Technical architecture review\n"
        content += "- Data pipeline assessment\n"
        content += "- Model requirements gathering\n"
        content += "- Success criteria definition\n\n"
        
        content += "**Phase 2: POC Setup (Week 3-4)**\n"
        content += "- Environment provisioning\n"
        content += "- Initial model deployment\n"
        content += "- Integration setup\n"
        content += "- Baseline performance testing\n\n"
        
        content += "**Phase 3: Optimization (Week 5-6)**\n"
        content += "- Performance tuning\n"
        content += "- Cost optimization\n"
        content += "- Scaling tests\n"
        content += "- Documentation\n\n"
        
        content += "**Success Metrics:**\n"
        content += "- [ ] Latency < X ms\n"
        content += "- [ ] Throughput > Y QPS\n"
        content += "- [ ] Cost per inference < $Z\n"
        content += "- [ ] Model accuracy maintained\n"
        
        return content
    
    def _load_customer_data(self, customer_id: str) -> Dict[str, Any]:
        try:
            with open(f'customers/{customer_id}.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _assess_ml_maturity(self, context: Dict[str, Any]) -> str:
        # Simple assessment based on available data
        score = 0
        if context.get('use_case'):
            score += 2
        if 'model' in str(context).lower():
            score += 2
        if 'data' in str(context).lower():
            score += 1
        
        if score >= 4:
            return "Advanced"
        elif score >= 2:
            return "Intermediate"
        else:
            return "Early Stage"
    
    def _get_infrastructure_info(self, context: Dict[str, Any]) -> str:
        # Extract from conversations
        infra_mentions = []
        
        # Check for cloud providers
        content_str = str(context).lower()
        if 'aws' in content_str:
            infra_mentions.append('AWS')
        if 'gcp' in content_str or 'google cloud' in content_str:
            infra_mentions.append('GCP')
        if 'azure' in content_str:
            infra_mentions.append('Azure')
        
        return ', '.join(infra_mentions) if infra_mentions else 'Not specified'
    
    def _calculate_technical_readiness(self, context: Dict[str, Any]) -> str:
        score = 5  # Base score
        
        # Add points for technical discussions
        if context.get('use_case'):
            score += 1
        if 'model' in str(context).lower():
            score += 1
        if 'infrastructure' in str(context).lower():
            score += 1
        if 'data' in str(context).lower():
            score += 1
        if len(context.get('action_items', [])) > 0:
            score += 1
        
        return str(min(score, 10))