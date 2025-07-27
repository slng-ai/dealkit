from .base_report import BaseReport
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class CROReport(BaseReport):
    """Chief Revenue Officer Report - Deal status and closing probability"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        report = self.format_header(context)
        
        # Deal Status Overview
        report += self.format_section(
            "Deal Status",
            self._generate_deal_status(context)
        )
        
        # Closing Probability
        report += self.format_section(
            "Win Probability Analysis",
            self._analyze_win_probability(context)
        )
        
        # Sales Velocity
        report += self.format_section(
            "Sales Velocity & Timeline",
            self._analyze_sales_velocity(context)
        )
        
        # Stakeholder Engagement
        report += self.format_section(
            "Stakeholder Coverage",
            self._analyze_stakeholder_coverage(context)
        )
        
        # Competitive Position
        report += self.format_section(
            "Competitive Analysis",
            self._analyze_competition(context)
        )
        
        # Deal Risks & Blockers
        report += self.format_section(
            "Risk Assessment",
            self._identify_deal_risks(context)
        )
        
        # Clear Next Steps
        report += self.format_section(
            "Recommended Actions",
            self._generate_next_steps(context)
        )
        
        return report
    
    def _generate_deal_status(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = ""
        
        # Current stage
        stage = customer_data.get('stage', 'Unknown')
        stage_emoji = self._get_stage_emoji(stage)
        content += self.format_metric("Current Stage", f"{stage_emoji} {stage.title()}")
        
        # Deal metrics
        content += self.format_metric("Deal Size", self._format_currency(customer_data.get('deal_size', 0)))
        content += self.format_metric("Days in Pipeline", self._calculate_days_in_pipeline(customer_data))
        content += self.format_metric("Last Interaction", self._format_last_interaction(customer_data))
        content += self.format_metric("Next Meeting", customer_data.get('next_meeting', 'Not scheduled'))
        
        # Stage progression
        content += "\n### Stage Progression\n"
        content += self._visualize_stage_progression(customer_data)
        
        return content
    
    def _analyze_win_probability(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        # Calculate win probability
        probability = self._calculate_win_probability(customer_data, context)
        
        content = f"### Overall Win Probability: {probability}%\n\n"
        
        # Positive indicators
        content += "**Positive Indicators:**\n"
        positive = self._get_positive_indicators(customer_data, context)
        for indicator in positive:
            content += f"- ✅ {indicator}\n"
        
        if not positive:
            content += "- ⚠️ No strong positive indicators identified\n"
        
        content += "\n**Negative Indicators:**\n"
        negative = self._get_negative_indicators(customer_data, context)
        for indicator in negative:
            content += f"- ❌ {indicator}\n"
        
        if not negative:
            content += "- ✅ No major red flags identified\n"
        
        # Probability trend
        content += "\n### Probability Trend\n"
        content += self._analyze_probability_trend(customer_data, context)
        
        return content
    
    def _analyze_sales_velocity(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Pipeline Velocity Metrics\n\n"
        
        # Time in each stage
        content += "**Stage Duration:**\n"
        stage_times = self._calculate_stage_times(customer_data)
        for stage, days in stage_times.items():
            benchmark = self._get_stage_benchmark(stage)
            status = "✅" if days <= benchmark else "⚠️"
            content += f"- {stage}: {days} days {status} (benchmark: {benchmark} days)\n"
        
        # Expected close date
        content += "\n**Timeline Analysis:**\n"
        content += self.format_metric("Original Close Date", customer_data.get('expected_close_date', 'Not set'))
        content += self.format_metric("Revised Close Date", self._calculate_revised_close_date(customer_data))
        content += self.format_metric("Confidence Level", self._calculate_close_confidence(customer_data))
        
        # Velocity score
        velocity_score = self._calculate_velocity_score(customer_data)
        content += f"\n**Deal Velocity Score: {velocity_score}/10**\n"
        
        return content
    
    def _analyze_stakeholder_coverage(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Stakeholder Map\n\n"
        
        # Primary contact
        primary = customer_data.get('primary_contact', {})
        if primary:
            content += "**Primary Contact:**\n"
            content += f"- {primary.get('name', 'Unknown')} - {primary.get('title', 'Unknown')}\n"
            content += f"  - Email: {primary.get('email', 'N/A')}\n"
            content += f"  - Engagement: {self._assess_contact_engagement(primary)}\n\n"
        
        # Additional contacts
        additional = customer_data.get('additional_contacts', [])
        if additional:
            content += f"**Additional Stakeholders ({len(additional)}):**\n"
            for contact in additional:
                role_emoji = self._get_role_emoji(contact.get('title', ''))
                content += f"- {role_emoji} {contact.get('name')} - {contact.get('title')}\n"
        else:
            content += "**Additional Stakeholders:** ❌ None identified (RISK)\n\n"
        
        # Coverage analysis
        content += "**Coverage Assessment:**\n"
        coverage = self._assess_stakeholder_coverage(customer_data)
        for role, status in coverage.items():
            emoji = "✅" if status else "❌"
            content += f"- {role}: {emoji}\n"
        
        # Multi-threading score
        thread_score = len(additional) + (1 if primary else 0)
        content += f"\n**Multi-Threading Score: {thread_score}/5**\n"
        
        return content
    
    def _analyze_competition(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Competitive Landscape\n\n"
        
        # Known competitors
        competitors = customer_data.get('assessment', {}).get('competition', [])
        if competitors:
            content += "**Identified Competitors:**\n"
            for comp in competitors:
                content += f"- {comp}\n"
        else:
            content += "**Competitors:** Not identified yet\n"
        
        # Competitive advantages
        content += "\n**Our Advantages:**\n"
        content += "- ❓ Technical superiority (needs validation)\n"
        content += "- ❓ Better pricing (needs confirmation)\n"
        content += "- ❓ Superior support (needs emphasis)\n"
        
        # Decision criteria
        criteria = customer_data.get('assessment', {}).get('decision_criteria', [])
        if criteria:
            content += "\n**Customer's Decision Criteria:**\n"
            for criterion in criteria:
                content += f"- {criterion}\n"
        
        return content
    
    def _identify_deal_risks(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        
        content = "### Risk Matrix\n\n"
        
        risks = []
        
        # Single-threading risk
        if len(customer_data.get('additional_contacts', [])) < 2:
            risks.append({
                'type': 'Single-threaded',
                'severity': 'High',
                'impact': 'Deal could stall if champion leaves',
                'mitigation': 'Get introduced to 2-3 more stakeholders'
            })
        
        # Stalled deal risk
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            if days_since > 14:
                risks.append({
                    'type': 'Stalled Engagement',
                    'severity': 'High',
                    'impact': f'No interaction in {days_since} days',
                    'mitigation': 'Schedule urgent check-in call'
                })
        
        # Budget risk
        if not customer_data.get('assessment', {}).get('budget_confirmed'):
            risks.append({
                'type': 'Unconfirmed Budget',
                'severity': 'Medium',
                'impact': 'Deal could be delayed or downsized',
                'mitigation': 'Get budget confirmation from economic buyer'
            })
        
        # Competition risk
        if customer_data.get('assessment', {}).get('competition'):
            risks.append({
                'type': 'Active Competition',
                'severity': 'Medium',
                'impact': 'Could lose on price or features',
                'mitigation': 'Emphasize unique value props and ROI'
            })
        
        # Format risks
        for risk in risks:
            severity_emoji = "🔴" if risk['severity'] == 'High' else "🟡"
            content += f"**{severity_emoji} {risk['type']}**\n"
            content += f"- Impact: {risk['impact']}\n"
            content += f"- Mitigation: {risk['mitigation']}\n\n"
        
        if not risks:
            content += "✅ No major risks identified\n"
        
        return content
    
    def _generate_next_steps(self, context: Dict[str, Any]) -> str:
        customer_data = self._load_customer_data(context.get('customer_id', ''))
        stage = customer_data.get('stage', 'discovery')
        
        content = "### Priority Actions for This Week\n\n"
        
        # Stage-specific actions
        actions = self._get_stage_specific_actions(stage, customer_data, context)
        
        for i, action in enumerate(actions[:5], 1):  # Top 5 actions
            content += f"**{i}. {action['title']}**\n"
            content += f"   - Why: {action['reason']}\n"
            content += f"   - Owner: {action['owner']}\n"
            content += f"   - Due: {action['due']}\n\n"
        
        # Call to action
        content += "### 🎯 Key CRO Action\n"
        if stage in ['negotiation', 'business_case']:
            content += "**Push for signature this week** - All indicators show deal is ready to close\n"
        elif stage == 'technical_validation':
            content += "**Secure technical win** - Get confirmation that POC met success criteria\n"
        else:
            content += "**Advance to next stage** - Focus on getting concrete next steps scheduled\n"
        
        return content
    
    # Helper methods
    def _load_customer_data(self, customer_id: str) -> Dict[str, Any]:
        try:
            with open(f'customers/{customer_id}.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _get_stage_emoji(self, stage: str) -> str:
        stage_emojis = {
            'discovery': '🔍',
            'technical_validation': '🔬',
            'business_case': '📊',
            'negotiation': '🤝',
            'closed_won': '🎉',
            'closed_lost': '❌'
        }
        return stage_emojis.get(stage.lower(), '📋')
    
    def _format_currency(self, amount: float) -> str:
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.0f}K"
        else:
            return f"${amount:.0f}"
    
    def _calculate_days_in_pipeline(self, customer_data: Dict[str, Any]) -> str:
        created = customer_data.get('created_at')
        if created:
            created_date = datetime.fromisoformat(created)
            days = (datetime.now() - created_date).days
            return f"{days} days"
        return "Unknown"
    
    def _format_last_interaction(self, customer_data: Dict[str, Any]) -> str:
        last = customer_data.get('last_interaction')
        if last:
            last_date = datetime.fromisoformat(last)
            days_ago = (datetime.now() - last_date).days
            if days_ago == 0:
                return "Today ✅"
            elif days_ago == 1:
                return "Yesterday ✅"
            elif days_ago <= 7:
                return f"{days_ago} days ago 🟡"
            else:
                return f"{days_ago} days ago 🔴"
        return "Never 🔴"
    
    def _visualize_stage_progression(self, customer_data: Dict[str, Any]) -> str:
        stages = ['discovery', 'technical_validation', 'business_case', 'negotiation', 'closed_won']
        current_stage = customer_data.get('stage', 'discovery').lower()
        
        visual = ""
        for i, stage in enumerate(stages):
            if stage == current_stage:
                visual += f"**[{stage.upper()}]** "
            elif stages.index(current_stage) > i:
                visual += f"✅ {stage} "
            else:
                visual += f"⬜ {stage} "
            
            if i < len(stages) - 1:
                visual += "→ "
        
        return visual + "\n"
    
    def _calculate_win_probability(self, customer_data: Dict[str, Any], context: Dict[str, Any]) -> int:
        probability = 20  # Base probability
        
        # Stage-based probability
        stage_probs = {
            'discovery': 20,
            'technical_validation': 40,
            'business_case': 65,
            'negotiation': 85,
            'closed_won': 100
        }
        probability = stage_probs.get(customer_data.get('stage', 'discovery').lower(), 20)
        
        # Adjustments
        if customer_data.get('assessment', {}).get('budget_confirmed'):
            probability += 10
        
        if len(customer_data.get('additional_contacts', [])) >= 3:
            probability += 10
        
        if customer_data.get('assessment', {}).get('champion_identified'):
            probability += 5
        
        # Recent engagement
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            if days_since <= 7:
                probability += 5
            elif days_since > 30:
                probability -= 20
        
        return max(0, min(100, probability))
    
    def _get_positive_indicators(self, customer_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        indicators = []
        
        if customer_data.get('assessment', {}).get('budget_confirmed'):
            indicators.append("Budget confirmed")
        
        if customer_data.get('assessment', {}).get('champion_identified'):
            indicators.append("Strong champion identified")
        
        if len(customer_data.get('additional_contacts', [])) >= 3:
            indicators.append("Multi-threaded engagement")
        
        if customer_data.get('urgency') == 'high':
            indicators.append("High urgency to solve problem")
        
        engagement = context.get('summary', {}).get('slack_activity', {}).get('engagement_level')
        if engagement == 'high':
            indicators.append("High Slack engagement")
        
        return indicators
    
    def _get_negative_indicators(self, customer_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        indicators = []
        
        if not customer_data.get('assessment', {}).get('budget_confirmed'):
            indicators.append("Budget not confirmed")
        
        if len(customer_data.get('additional_contacts', [])) < 2:
            indicators.append("Single-threaded (high risk)")
        
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            if days_since > 14:
                indicators.append(f"No interaction in {days_since} days")
        
        if customer_data.get('assessment', {}).get('competition'):
            indicators.append("Active competition in deal")
        
        return indicators
    
    def _analyze_probability_trend(self, customer_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        # This would analyze historical data to show trend
        # For now, return a simple assessment
        stage = customer_data.get('stage', 'discovery')
        
        if stage in ['business_case', 'negotiation']:
            return "📈 Probability trending upward - deal progressing well\n"
        elif stage == 'discovery':
            created = customer_data.get('created_at')
            if created:
                created_date = datetime.fromisoformat(created)
                days_old = (datetime.now() - created_date).days
                if days_old > 30:
                    return "📉 Probability trending down - stuck in discovery too long\n"
        
        return "↔️ Probability stable - maintain momentum\n"
    
    def _calculate_stage_times(self, customer_data: Dict[str, Any]) -> Dict[str, int]:
        # Simplified calculation
        current_stage = customer_data.get('stage', 'discovery')
        created = customer_data.get('created_at')
        
        if created:
            created_date = datetime.fromisoformat(created)
            total_days = (datetime.now() - created_date).days
            
            # Estimate based on current stage
            if current_stage == 'discovery':
                return {'discovery': total_days}
            elif current_stage == 'technical_validation':
                return {'discovery': total_days // 2, 'technical_validation': total_days // 2}
            # Add more logic as needed
        
        return {current_stage: 0}
    
    def _get_stage_benchmark(self, stage: str) -> int:
        benchmarks = {
            'discovery': 14,
            'technical_validation': 21,
            'business_case': 14,
            'negotiation': 14,
            'closed_won': 7
        }
        return benchmarks.get(stage.lower(), 14)
    
    def _calculate_revised_close_date(self, customer_data: Dict[str, Any]) -> str:
        # Calculate based on current stage and velocity
        stage = customer_data.get('stage', 'discovery')
        stages_remaining = {
            'discovery': 60,
            'technical_validation': 45,
            'business_case': 30,
            'negotiation': 14,
            'closed_won': 0
        }
        
        days_to_close = stages_remaining.get(stage.lower(), 60)
        close_date = datetime.now() + timedelta(days=days_to_close)
        
        return close_date.strftime('%Y-%m-%d')
    
    def _calculate_close_confidence(self, customer_data: Dict[str, Any]) -> str:
        stage = customer_data.get('stage', 'discovery')
        
        if stage == 'negotiation':
            return "High (80%+)"
        elif stage == 'business_case':
            return "Medium (50-80%)"
        else:
            return "Low (<50%)"
    
    def _calculate_velocity_score(self, customer_data: Dict[str, Any]) -> int:
        score = 5
        
        # Recent activity
        last_interaction = customer_data.get('last_interaction')
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction)
            days_since = (datetime.now() - last_date).days
            if days_since <= 3:
                score += 2
            elif days_since <= 7:
                score += 1
            elif days_since > 14:
                score -= 2
        
        # Stage progression
        stage = customer_data.get('stage', 'discovery')
        if stage in ['business_case', 'negotiation']:
            score += 2
        
        # Multi-threading
        if len(customer_data.get('additional_contacts', [])) >= 3:
            score += 1
        
        return max(1, min(10, score))
    
    def _assess_contact_engagement(self, contact: Dict[str, Any]) -> str:
        # Simplified assessment
        return "Active ✅"
    
    def _get_role_emoji(self, title: str) -> str:
        title_lower = title.lower()
        if any(x in title_lower for x in ['cto', 'chief technology', 'vp eng']):
            return '👨‍💻'
        elif any(x in title_lower for x in ['ceo', 'chief executive', 'founder']):
            return '👔'
        elif any(x in title_lower for x in ['cfo', 'chief financial', 'finance']):
            return '💰'
        elif any(x in title_lower for x in ['engineer', 'developer', 'architect']):
            return '🔧'
        else:
            return '👤'
    
    def _assess_stakeholder_coverage(self, customer_data: Dict[str, Any]) -> Dict[str, bool]:
        contacts = [customer_data.get('primary_contact', {})] + customer_data.get('additional_contacts', [])
        titles = ' '.join([c.get('title', '') for c in contacts]).lower()
        
        return {
            'Economic Buyer': any(x in titles for x in ['cfo', 'finance', 'procurement']),
            'Technical Champion': any(x in titles for x in ['engineer', 'architect', 'developer']),
            'Executive Sponsor': any(x in titles for x in ['ceo', 'cto', 'vp', 'director']),
            'End User': any(x in titles for x in ['analyst', 'scientist', 'researcher'])
        }
    
    def _get_stage_specific_actions(self, stage: str, customer_data: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        actions = []
        
        if stage == 'discovery':
            actions.extend([
                {
                    'title': 'Complete technical discovery call',
                    'reason': 'Need to understand technical requirements',
                    'owner': 'Sales + SE',
                    'due': 'This week'
                },
                {
                    'title': 'Identify and engage economic buyer',
                    'reason': 'Budget confirmation required for advancement',
                    'owner': 'AE',
                    'due': 'This week'
                }
            ])
        elif stage == 'technical_validation':
            actions.extend([
                {
                    'title': 'Define POC success criteria',
                    'reason': 'Clear metrics needed for technical win',
                    'owner': 'SE + Champion',
                    'due': 'Today'
                },
                {
                    'title': 'Schedule POC review with stakeholders',
                    'reason': 'Build consensus for business case',
                    'owner': 'AE',
                    'due': 'This week'
                }
            ])
        elif stage == 'business_case':
            actions.extend([
                {
                    'title': 'Present ROI analysis',
                    'reason': 'Justify investment to economic buyer',
                    'owner': 'AE + Sales Ops',
                    'due': 'This week'
                },
                {
                    'title': 'Get procurement involved',
                    'reason': 'Understand contract requirements early',
                    'owner': 'AE',
                    'due': 'This week'
                }
            ])
        elif stage == 'negotiation':
            actions.extend([
                {
                    'title': 'Send final contract for signature',
                    'reason': 'All terms agreed - ready to close',
                    'owner': 'AE',
                    'due': 'Today'
                },
                {
                    'title': 'Schedule implementation kickoff',
                    'reason': 'Show commitment to customer success',
                    'owner': 'CSM',
                    'due': 'Upon signature'
                }
            ])
        
        # Add risk-based actions
        if len(customer_data.get('additional_contacts', [])) < 2:
            actions.append({
                'title': 'Multi-thread the deal',
                'reason': 'Single-threaded deals have 3x higher loss rate',
                'owner': 'AE',
                'due': 'This week'
            })
        
        return actions